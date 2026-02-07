from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Recruiter, RecruiterPackage, JobOpening, JobApplication,
    CandidateSearch, RecruiterUsage, RecruiterMessage
)
from .serializers import (
    RecruiterPackageSerializer, RecruiterRegistrationSerializer,
    RecruiterSerializer, RecruiterUsageSerializer, JobOpeningSerializer,
    JobApplicationSerializer, CandidateSearchSerializer, RecruiterMessageSerializer
)
from accounts.models import UserProfile


class IsRecruiter(permissions.BasePermission):
    """Custom permission to only allow recruiters"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'recruiter_profile')


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def recruiter_register(request):
    """Register a new recruiter"""
    print(f"DEBUG: Received registration request with data: {request.data}")
    serializer = RecruiterRegistrationSerializer(data=request.data)
    print(f"DEBUG: Serializer created, checking validity...")
    if serializer.is_valid():
        print(f"DEBUG: Serializer is valid, creating user...")
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        print(f"DEBUG: User created successfully: {user.email}")
        
        return Response({
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'token': token.key,
            'message': 'Recruiter registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    print(f"DEBUG: Serializer validation failed with errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def recruiter_login(request):
    """Login for recruiters"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Please provide both email and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=email, password=password)
    
    if user is None:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if user is a recruiter
    if not hasattr(user, 'recruiter_profile'):
        return Response({
            'error': 'This account is not registered as a recruiter'
        }, status=status.HTTP_403_FORBIDDEN)
    
    recruiter = user.recruiter_profile
    
    # Check if recruiter is active
    if not recruiter.is_active:
        return Response({
            'error': 'This recruiter account is inactive'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Generate token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'user': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'recruiter_id': recruiter.id,
            'company_name': recruiter.company_name
        },
        'token': token.key
    }, status=status.HTTP_200_OK)


class RecruiterPackageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing recruiter packages"""
    queryset = RecruiterPackage.objects.filter(is_active=True)
    serializer_class = RecruiterPackageSerializer
    permission_classes = [AllowAny]


class RecruiterProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for recruiter profile management"""
    serializer_class = RecruiterSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    
    def get_queryset(self):
        # Recruiters can only see their own profile
        return Recruiter.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current recruiter's profile"""
        recruiter = request.user.recruiter_profile
        serializer = self.get_serializer(recruiter)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def usage(self, request):
        """Get current month's usage statistics"""
        recruiter = request.user.recruiter_profile
        now = timezone.now()
        
        usage, created = RecruiterUsage.objects.get_or_create(
            recruiter=recruiter,
            year=now.year,
            month=now.month
        )
        
        serializer = RecruiterUsageSerializer(usage)
        return Response(serializer.data)


class JobOpeningViewSet(viewsets.ModelViewSet):
    """ViewSet for job opening management"""
    serializer_class = JobOpeningSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    
    def get_queryset(self):
        # Recruiters can only see their own job openings
        return JobOpening.objects.filter(recruiter__user=self.request.user)
    
    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter_profile
        now = timezone.now()
        
        # Get or create usage record
        usage, created = RecruiterUsage.objects.get_or_create(
            recruiter=recruiter,
            year=now.year,
            month=now.month
        )
        
        # Check if recruiter can create more job openings
        if not usage.can_create_job_opening():
            return Response({
                'error': 'Monthly job opening limit reached for your package'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Create job opening
        job = serializer.save(recruiter=recruiter)
        
        # Increment usage counter
        usage.job_openings_created += 1
        usage.save()
        
        return Response(
            JobOpeningSerializer(job).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a draft job opening"""
        job = self.get_object()
        if job.status != 'draft':
            return Response({
                'error': 'Only draft jobs can be published'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        job.publish()
        return Response({
            'message': 'Job opening published successfully',
            'job': JobOpeningSerializer(job).data
        })
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get analytics for all job openings"""
        jobs = self.get_queryset()
        
        total_views = jobs.aggregate(Sum('views_count'))['views_count__sum'] or 0
        total_applications = jobs.aggregate(Sum('applications_count'))['applications_count__sum'] or 0
        
        status_breakdown = jobs.values('status').annotate(count=Count('id'))
        
        return Response({
            'total_jobs': jobs.count(),
            'total_views': total_views,
            'total_applications': total_applications,
            'status_breakdown': list(status_breakdown),
            'active_jobs': jobs.filter(status='active').count(),
            'draft_jobs': jobs.filter(status='draft').count(),
        })


class JobApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for job application management"""
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # If recruiter, show applications to their jobs
        if hasattr(user, 'recruiter_profile'):
            return JobApplication.objects.filter(
                job_opening__recruiter__user=user
            )
        
        # If candidate, show their applications
        return JobApplication.objects.filter(candidate_user=user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update application status (recruiter only)"""
        if not hasattr(request.user, 'recruiter_profile'):
            return Response({
                'error': 'Only recruiters can update application status'
            }, status=status.HTTP_403_FORBIDDEN)
        
        application = self.get_object()
        
        # Verify the application belongs to this recruiter's job
        if application.job_opening.recruiter.user != request.user:
            return Response({
                'error': 'You can only update applications for your own job openings'
            }, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        notes = request.data.get('recruiter_notes', '')
        interview_date = request.data.get('interview_date')
        
        if new_status not in dict(JobApplication.STATUS_CHOICES):
            return Response({
                'error': 'Invalid status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = new_status
        if notes:
            application.recruiter_notes = notes
        if interview_date:
            application.interview_date = interview_date
        application.save()
        
        return Response(JobApplicationSerializer(application).data)


class CandidateSearchViewSet(viewsets.ModelViewSet):
    """ViewSet for candidate search functionality"""
    serializer_class = CandidateSearchSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    
    def get_queryset(self):
        # Recruiters can only see their own searches
        return CandidateSearch.objects.filter(recruiter__user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def search_candidates(self, request):
        """Search for candidates based on various criteria"""
        recruiter = request.user.recruiter_profile
        now = timezone.now()
        
        # Get or create usage record
        usage, created = RecruiterUsage.objects.get_or_create(
            recruiter=recruiter,
            year=now.year,
            month=now.month
        )
        
        # Check if recruiter can search more candidates
        if not usage.can_search_candidate():
            return Response({
                'error': 'Monthly candidate search limit reached for your package',
                'limit': recruiter.package.monthly_candidate_searches,
                'used': usage.candidates_searched
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get search parameters
        query = request.data.get('query', '')
        skills = request.data.get('skills', [])
        location = request.data.get('location', '')
        experience_level = request.data.get('experience_level', '')
        employment_type = request.data.get('employment_type', '')
        remote_only = request.data.get('remote_only', False)
        actively_looking = request.data.get('actively_looking', False)
        
        # Search in UserProfile with related job preferences
        from accounts.models import JobPreference
        from companies.models import Function
        
        candidates = UserProfile.objects.select_related('user').filter(
            user__is_active=True
        )
        
        # Filter by query (name, title, bio)
        if query:
            candidates = candidates.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(current_title__icontains=query) |
                Q(bio__icontains=query)
            )
        
        # Filter by skills (desired functions)
        if skills and len(skills) > 0:
            # Get job preferences that have matching desired functions
            matching_prefs = JobPreference.objects.filter(
                desired_functions__name__in=skills
            ).values_list('user_id', flat=True).distinct()
            
            candidates = candidates.filter(user_id__in=matching_prefs)
        
        # Filter by location
        if location:
            candidates = candidates.filter(
                Q(location__icontains=location)
            )
        
        # Filter by experience level
        if experience_level:
            exp_ranges = {
                'entry': (0, 2),
                'mid': (3, 5),
                'senior': (6, 10),
                'lead': (11, 100)
            }
            if experience_level in exp_ranges:
                min_exp, max_exp = exp_ranges[experience_level]
                candidates = candidates.filter(
                    years_of_experience__gte=min_exp,
                    years_of_experience__lte=max_exp
                )
        
        # Filter by job preferences
        if remote_only or actively_looking or employment_type:
            candidate_ids = []
            for profile in candidates:
                try:
                    pref = JobPreference.objects.get(user=profile.user)
                    
                    # Check remote only
                    if remote_only and not pref.remote_only:
                        continue
                    
                    # Check actively looking
                    if actively_looking and not pref.actively_looking:
                        continue
                    
                    # Check employment type
                    if employment_type and employment_type not in pref.employment_types:
                        continue
                    
                    candidate_ids.append(profile.id)
                except JobPreference.DoesNotExist:
                    pass
            
            candidates = candidates.filter(id__in=candidate_ids)
        
        # Return limited results based on package
        results = []
        for profile in candidates[:20]:  # Limit to 20 results
            # Get job preference if exists
            try:
                job_pref = JobPreference.objects.get(user=profile.user)
            except JobPreference.DoesNotExist:
                job_pref = None
            
            # Return basic info
            candidate_data = {
                'id': profile.user.id,
                'name': profile.user.get_full_name(),
                'current_title': profile.current_title,
                'location': profile.location,
                'bio': profile.bio,
                'years_of_experience': profile.years_of_experience,
                'linkedin_url': profile.linkedin_url,
                'portfolio_url': profile.portfolio_url,
                'github_url': profile.github_url,
            }
            
            # Add job preference data if available
            if job_pref:
                candidate_data.update({
                    'desired_functions': list(job_pref.desired_functions.values_list('name', flat=True)),
                    'work_environments': list(job_pref.work_environments.values_list('name', flat=True)),
                    'employment_types': job_pref.employment_types,
                    'remote_only': job_pref.remote_only,
                    'actively_looking': job_pref.actively_looking,
                    'minimum_salary': job_pref.minimum_salary,
                    'willing_to_relocate': job_pref.willing_to_relocate,
                })
            
            # Add contact info if package allows
            if recruiter.package.candidate_profile_access:
                candidate_data.update({
                    'email': profile.user.email,
                    'phone': profile.phone,
                })
            
            results.append(candidate_data)
            
            # Track the search
            search, created = CandidateSearch.objects.get_or_create(
                recruiter=recruiter,
                candidate_user=profile.user,
                defaults={'search_query': query}
            )
            
            if created:
                usage.candidates_searched += 1
                usage.save()
        
        return Response({
            'results': results,
            'count': len(results),
            'usage': {
                'limit': recruiter.package.monthly_candidate_searches,
                'used': usage.candidates_searched,
                'remaining': recruiter.package.monthly_candidate_searches - usage.candidates_searched
                    if recruiter.package.monthly_candidate_searches > 0 else 'unlimited'
            }
        })
    
    @action(detail=False, methods=['get'])
    def saved(self, request):
        """Get saved candidates"""
        saved = self.get_queryset().filter(is_saved=True)
        serializer = self.get_serializer(saved, many=True)
        return Response(serializer.data)


class RecruiterMessageViewSet(viewsets.ModelViewSet):
    """ViewSet for recruiter messaging"""
    serializer_class = RecruiterMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # If recruiter, show their messages
        if hasattr(user, 'recruiter_profile'):
            return RecruiterMessage.objects.filter(
                Q(sender_recruiter__user=user) |
                Q(recipient_recruiter__user=user)
            )
        
        # If candidate, show their messages with recruiters
        return RecruiterMessage.objects.filter(
            Q(sender_user=user) |
            Q(recipient_user=user)
        )
    
    def perform_create(self, serializer):
        user = self.request.user
        
        # If recruiter, check messaging limits
        if hasattr(user, 'recruiter_profile'):
            recruiter = user.recruiter_profile
            
            if not recruiter.package.messaging_enabled:
                return Response({
                    'error': 'Messaging is not enabled for your package'
                }, status=status.HTTP_403_FORBIDDEN)
            
            now = timezone.now()
            usage, created = RecruiterUsage.objects.get_or_create(
                recruiter=recruiter,
                year=now.year,
                month=now.month
            )
            
            if not usage.can_send_message():
                return Response({
                    'error': 'Monthly message limit reached for your package'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Create message
            message = serializer.save(sender_recruiter=recruiter)
            
            # Increment usage counter
            usage.messages_sent += 1
            usage.save()
            
            return Response(
                RecruiterMessageSerializer(message).data,
                status=status.HTTP_201_CREATED
            )
        else:
            # Candidate sending message
            serializer.save(sender_user=user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        
        return Response({'status': 'Message marked as read'})
