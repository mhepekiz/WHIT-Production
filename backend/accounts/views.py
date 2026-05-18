from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .emailing import send_account_email
from .models import UserProfile, JobPreference
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    UserProfileSerializer,
    JobPreferenceSerializer,
    UserDashboardSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_account_email('account_created', user)
        send_account_email('email_verification', user)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully. Please verify your email before logging in.'
        }, status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    """Custom login endpoint that returns user data with token."""
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profile management."""
    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile."""
        profile = UserProfile.objects.get(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(profile, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def upload_resume(self, request):
        """Upload resume file."""
        profile = UserProfile.objects.get(user=request.user)
        
        if 'resume' not in request.FILES:
            return Response(
                {'error': 'No resume file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resume_file = request.FILES['resume']
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if resume_file.size > max_size:
            return Response(
                {'error': 'Resume file must be under 10MB'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file type
        allowed_types = ['application/pdf', 'application/msword',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if resume_file.content_type not in allowed_types:
            return Response(
                {'error': 'Only PDF and Word documents are allowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file extension
        import os
        ext = os.path.splitext(resume_file.name)[1].lower()
        if ext not in ['.pdf', '.doc', '.docx']:
            return Response(
                {'error': 'Invalid file extension. Allowed: .pdf, .doc, .docx'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile.resume = resume_file
        profile.resume_uploaded_at = timezone.now()
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class JobPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for job preference management."""
    
    serializer_class = JobPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return JobPreference.objects.filter(user=self.request.user)
    
    def get_object(self):
        return JobPreference.objects.get(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's job preferences."""
        preference = JobPreference.objects.get(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(preference)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(preference, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class DashboardView(generics.RetrieveAPIView):
    """User dashboard with all user data."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserDashboardSerializer
    
    def get_object(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        job_preference = JobPreference.objects.get(user=user)
        
        return {
            'user': user,
            'profile': profile,
            'job_preference': job_preference,
        }


def get_user_from_uid(uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    user = get_user_from_uid(request.data.get('uid', ''))
    token = request.data.get('token', '')

    if not user or not default_token_generator.check_token(user, token):
        return Response({'error': 'This verification link is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.save(update_fields=['is_active'])
    profile = UserProfile.objects.filter(user=user).first()
    if profile and not profile.email_verified_at:
        profile.email_verified_at = timezone.now()
        profile.save(update_fields=['email_verified_at'])

    return Response({'message': 'Email verified successfully. You can now log in.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email(request):
    email = request.data.get('email', '').strip()
    user = User.objects.filter(email__iexact=email).first()
    if user and not user.is_active:
        send_account_email('email_verification', user)
    return Response({'message': 'If an unverified account exists, a new verification email has been sent.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email', '').strip()
    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if user:
        send_account_email('password_reset', user)
    return Response({'message': 'If an active account exists for this email, a password reset link has been sent.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    user = get_user_from_uid(request.data.get('uid', ''))
    token = request.data.get('token', '')
    password = request.data.get('password', '')
    password2 = request.data.get('password2', '')

    if not user or not default_token_generator.check_token(user, token):
        return Response({'error': 'This password reset link is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)
    if password != password2:
        return Response({'password2': ['Password fields did not match.']}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password, user)
    except DjangoValidationError as exc:
        return Response({'password': exc.messages}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save(update_fields=['password'])
    Token.objects.filter(user=user).delete()
    return Response({'message': 'Password reset successfully. Please log in with your new password.'})
