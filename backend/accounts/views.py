from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.utils import timezone
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
        
        # Create token for automatic login
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
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
