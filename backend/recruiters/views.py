from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Count, Sum, F
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Recruiter, RecruiterPackage, JobOpening, JobApplication,
    CandidateSearch, RecruiterUsage, RecruiterMessage
)
from .serializers import (
    RecruiterPackageSerializer, RecruiterRegistrationSerializer,
    RecruiterSerializer, RecruiterUsageSerializer, JobOpeningSerializer,
    PublicJobOpeningSerializer,
    JobApplicationSerializer, CandidateSearchSerializer, RecruiterMessageSerializer
)
from accounts.models import UserProfile


class IsRecruiter(permissions.BasePermission):
    """Custom permission to only allow recruiters"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'recruiter_profile')


def create_test_user():
    """Helper function to create analytics test user"""
    from recruiters.models import RecruiterPackage, Recruiter
    
    # Get or create package
    package, _ = RecruiterPackage.objects.get_or_create(
        name='Test Package',
        defaults={
            'description': 'Test package',
            'price': 0,
            'monthly_job_openings': 10,
            'analytics_level': 'basic',
            'monthly_candidate_searches': 50,
            'candidate_profile_access': True,
            'messaging_enabled': True,
            'monthly_messages': 100
        }
    )
    
    # Create user
    user = User.objects.create_user(
        username='analytics_tester',
        email='analytics@test.com',
        password='testpass123',
        first_name='Analytics',
        last_name='Tester',
        is_active=True
    )
    
    # Create recruiter profile
    Recruiter.objects.create(
        user=user,
        package=package,
        company_name='Test Analytics Company',
        contact_email='analytics@test.com',
        phone_number='555-0123',
        is_verified=True,
        is_active=True
    )
    print("DEBUG: Analytics test user created successfully")
    return user


def create_cisco_user():
    """Helper function to create Cisco test user"""
    from recruiters.models import RecruiterPackage, Recruiter
    from companies.models import Company, CompanyRecruiterAccess
    
    # Get or create package
    package, _ = RecruiterPackage.objects.get_or_create(
        name='Cisco Package',
        defaults={
            'description': 'Cisco recruiter package',
            'price': 0,
            'monthly_job_openings': 50,
            'analytics_level': 'advanced',
            'monthly_candidate_searches': 200,
            'candidate_profile_access': True,
            'messaging_enabled': True,
            'monthly_messages': 500
        }
    )
    
    # Create user
    user = User.objects.create_user(
        username='mhepekiz_cisco',
        email='mhepekiz@cisco.com',
        password='password123',
        first_name='Mustafa',
        last_name='Hepekiz',
        is_active=True
    )
    
    # Create recruiter profile
    recruiter = Recruiter.objects.create(
        user=user,
        package=package,
        company_name='Cisco',
        contact_email='mhepekiz@cisco.com',
        phone_number='555-0124',
        is_verified=True,
        is_active=True
    )
    
    # Create or get Samsara company and assign access
    samsara, _ = Company.objects.get_or_create(
        name='Samsara',
        defaults={
            'website_url': 'https://samsara.com',
            'is_sponsored': True,
            'location': 'San Francisco, CA'
        }
    )
    
    # Create access relationship
    CompanyRecruiterAccess.objects.get_or_create(
        company=samsara,
        recruiter=recruiter,
        defaults={
            'can_see_sponsored_stats': True,
            'access_level': 'view'
        }
    )
    
    print("DEBUG: Cisco test user created successfully with Samsara access")
    return user


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def recruiter_register(request):
    """Register a new recruiter"""
    serializer = RecruiterRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'token': token.key,
            'message': 'Recruiter registered successfully'
        }, status=status.HTTP_201_CREATED)
    
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
    
    # Input length limits to prevent abuse
    if len(email) > 254 or len(password) > 128:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = None
    
    # First check if user exists
    try:
        user = User.objects.get(email=email)
        
        # Verify password
        if not user.check_password(password):
            user = None
        elif not user.is_active:
            user = None
            
    except User.DoesNotExist:
        pass  # User not found
        
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


class PublicJobOpeningViewSet(viewsets.ReadOnlyModelViewSet):
    """API for browsing active job openings (requires authentication)"""
    serializer_class = PublicJobOpeningSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable DRF default pagination; we handle it in list()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            from .serializers import PublicJobOpeningDetailSerializer
            return PublicJobOpeningDetailSerializer
        return PublicJobOpeningSerializer

    def retrieve(self, request, *args, **kwargs):
        """Return job detail and increment views_count."""
        instance = self.get_object()
        JobOpening.objects.filter(pk=instance.pk).update(views_count=F('views_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_page_size(self):
        """Get page size from SiteSettings."""
        try:
            from companies.models import SiteSettings
            settings = SiteSettings.load()
            return settings.jobs_per_page
        except Exception:
            return 20

    def list(self, request, *args, **kwargs):
        """Override list to apply configurable pagination."""
        queryset = self.filter_queryset(self.get_queryset())
        page_size = self.get_page_size()
        try:
            page = max(1, int(request.query_params.get('page', 1)))
        except (ValueError, TypeError):
            page = 1
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        jobs = queryset[start:end]
        serializer = self.get_serializer(jobs, many=True)
        return Response({
            'results': serializer.data,
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size,
        })

    def get_queryset(self):
        qs = JobOpening.objects.filter(status='active').select_related('recruiter', 'company')

        # Apply user preferences filter
        use_preferences = self.request.query_params.get('preferences', '').lower() in ('true', '1')
        if use_preferences and self.request.user.is_authenticated:
            try:
                from accounts.models import JobPreference
                pref = JobPreference.objects.get(user=self.request.user)
                pref_q = Q()

                # Filter by desired functions → match against department
                func_names = list(pref.desired_functions.values_list('name', flat=True))
                if func_names:
                    dept_q = Q()
                    for fn in func_names:
                        dept_q |= Q(department__icontains=fn)
                    pref_q &= dept_q

                # Filter by work environments
                env_names = [e.lower() for e in pref.work_environments.values_list('name', flat=True)]
                if env_names:
                    env_q = Q()
                    if 'remote' in env_names:
                        env_q |= Q(remote_allowed=True)
                    if 'on-site' in env_names:
                        env_q |= Q(remote_allowed=False)
                    if 'hybrid' in env_names:
                        # Hybrid could be either; include all
                        env_q |= Q(remote_allowed=True) | Q(remote_allowed=False)
                    if env_q:
                        pref_q &= env_q

                if pref_q:
                    qs = qs.filter(pref_q)
            except Exception:
                pass

        # Filter by employment type
        employment_type = self.request.query_params.get('employment_type')
        if employment_type:
            qs = qs.filter(employment_type=employment_type)

        # Filter by experience level
        experience_level = self.request.query_params.get('experience_level')
        if experience_level:
            qs = qs.filter(experience_level=experience_level)

        # Filter by remote
        remote = self.request.query_params.get('remote')
        if remote and remote.lower() in ('true', '1'):
            qs = qs.filter(remote_allowed=True)

        # Search by keyword (title, description, skills)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(recruiter__company_name__icontains=search) |
                Q(department__icontains=search)
            )

        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            qs = qs.filter(
                Q(city__icontains=location) |
                Q(state__icontains=location) |
                Q(country__icontains=location) |
                Q(location__icontains=location)
            )

        # Ordering - whitelist allowed values
        ordering = self.request.query_params.get('ordering', '-published_at')
        allowed_orderings = ('published_at', '-published_at', 'title', '-title', 'salary_min', '-salary_min')
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by('-is_featured', '-published_at')

        return qs

    @action(detail=False, methods=['get'])
    def filters(self, request):
        """Return available filter options"""
        active_jobs = JobOpening.objects.filter(status='active')
        return Response({
            'employment_types': [
                {'value': c[0], 'label': c[1]}
                for c in JobOpening.EMPLOYMENT_TYPE_CHOICES
            ],
            'experience_levels': [
                {'value': c[0], 'label': c[1]}
                for c in JobOpening.EXPERIENCE_LEVEL_CHOICES
            ],
            'locations': list(
                active_jobs.values_list('city', flat=True)
                .distinct().order_by('city')[:50]
            ),
            'total_jobs': active_jobs.count(),
        })


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


class RecruiterDashboardViewSet(viewsets.ViewSet):
    """Dashboard views for recruiters with company access"""
    permission_classes = [IsRecruiter]
    
    @action(detail=False, methods=['get'])
    def accessible_companies(self, request):
        """Get companies the recruiter has access to"""
        from companies.models import CompanyRecruiterAccess, CampaignStatistics
        from companies.serializers import CompanySerializer
        
        recruiter = request.user.recruiter_profile
        
        # Get companies the recruiter has access to
        accesses = CompanyRecruiterAccess.objects.filter(
            recruiter=recruiter
        ).select_related('company').prefetch_related('company__functions')
        
        companies_data = []
        for access in accesses:
            company_serializer = CompanySerializer(access.company)
            company_data = company_serializer.data
            
            # Add access info
            company_data['access_info'] = {
                'access_level': access.access_level,
                'can_see_sponsored_stats': access.can_see_sponsored_stats,
                'can_manage_campaigns': access.can_manage_campaigns,
                'can_view_analytics': access.can_view_analytics,
                'can_export_data': access.can_export_data,
                'permissions_summary': access.get_permissions_summary()
            }
            
            companies_data.append(company_data)
        
        return Response(companies_data)
    
    @action(detail=False, methods=['get'])
    def company_statistics(self, request):
        """Get statistics for companies the recruiter has access to"""
        from companies.models import CompanyRecruiterAccess, CampaignStatistics
        from django.db.models import Sum, Avg
        from datetime import datetime, timedelta
        
        recruiter = request.user.recruiter_profile
        company_id = request.query_params.get('company_id')
        try:
            days = min(365, max(1, int(request.query_params.get('days', 30))))
        except (ValueError, TypeError):
            days = 30
        
        # Check access
        if company_id:
            access = CompanyRecruiterAccess.objects.filter(
                recruiter=recruiter,
                company_id=company_id,
                can_see_sponsored_stats=True
            ).first()
            
            if not access:
                return Response(
                    {'error': 'No access to this company statistics'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Get date range
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Build query
        stats_query = CampaignStatistics.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        if company_id:
            stats_query = stats_query.filter(company_id=company_id)
        else:
            # Get all companies the recruiter has stats access to
            accessible_company_ids = CompanyRecruiterAccess.objects.filter(
                recruiter=recruiter,
                can_see_sponsored_stats=True
            ).values_list('company_id', flat=True)
            
            stats_query = stats_query.filter(company_id__in=accessible_company_ids)
        
        # Get aggregated statistics
        totals = stats_query.aggregate(
            total_page_views=Sum('page_views'),
            total_unique_visitors=Sum('unique_visitors'),
            total_job_page_clicks=Sum('job_page_clicks'),
            total_profile_views=Sum('profile_views'),
            total_application_clicks=Sum('application_clicks'),
            total_contact_clicks=Sum('contact_clicks'),
            avg_click_through_rate=Avg('click_through_rate'),
            avg_engagement_rate=Avg('engagement_rate')
        )
        
        # Get daily statistics
        daily_stats = list(stats_query.values(
            'date', 'company__name', 'page_views', 'unique_visitors',
            'job_page_clicks', 'profile_views', 'application_clicks',
            'contact_clicks', 'click_through_rate', 'engagement_rate'
        ).order_by('-date'))
        
        return Response({
            'totals': totals,
            'daily_stats': daily_stats,
            'date_range': {
                'start_date': start_date,
                'end_date': end_date,
                'days': days
            }
        })
    
    @action(detail=False, methods=['get'])
    def dashboard_overview(self, request):
        """Get overview data for recruiter dashboard"""
        from companies.models import CompanyRecruiterAccess, CampaignStatistics
        from django.db.models import Sum, Count
        from datetime import datetime, timedelta
        
        recruiter = request.user.recruiter_profile
        
        # Get accessible companies count
        accessible_companies = CompanyRecruiterAccess.objects.filter(
            recruiter=recruiter
        ).count()
        
        # Get companies with different access levels
        access_levels = CompanyRecruiterAccess.objects.filter(
            recruiter=recruiter
        ).values('access_level').annotate(count=Count('id'))
        
        # Get recent statistics (last 7 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        
        accessible_company_ids = CompanyRecruiterAccess.objects.filter(
            recruiter=recruiter,
            can_see_sponsored_stats=True
        ).values_list('company_id', flat=True)
        
        recent_stats = CampaignStatistics.objects.filter(
            company_id__in=accessible_company_ids,
            date__gte=start_date
        ).aggregate(
            total_views=Sum('page_views'),
            total_clicks=Sum('job_page_clicks'),
            total_applications=Sum('application_clicks')
        )
        
        return Response({
            'accessible_companies': accessible_companies,
            'access_levels': list(access_levels),
            'recent_stats': recent_stats,
            'recruiter_info': {
                'company_name': recruiter.company_name,
                'package': recruiter.package.name,
                'analytics_level': recruiter.package.analytics_level
            }
        })


@api_view(['GET'])
@permission_classes([IsRecruiter])
def export_company_data(request, company_id):
    """Export company campaign data"""
    from companies.models import CompanyRecruiterAccess, CampaignStatistics
    from django.http import HttpResponse
    import csv
    from datetime import datetime, timedelta
    
    recruiter = request.user.recruiter_profile
    
    # Check access
    access = CompanyRecruiterAccess.objects.filter(
        recruiter=recruiter,
        company_id=company_id,
        can_export_data=True
    ).first()
    
    if not access:
        return Response(
            {'error': 'No export access to this company data'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get date range from parameters
    try:
        days = min(365, max(1, int(request.GET.get('days', 30))))
    except (ValueError, TypeError):
        days = 30
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get statistics
    stats = CampaignStatistics.objects.filter(
        company_id=company_id,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('-date')
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="campaign_data_{access.company.name}_{start_date}_to_{end_date}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Date', 'Page Views', 'Unique Visitors', 'Job Page Clicks',
        'Profile Views', 'Application Clicks', 'Contact Clicks',
        'Click Through Rate (%)', 'Engagement Rate (%)'
    ])
    
    for stat in stats:
        writer.writerow([
            stat.date,
            stat.page_views,
            stat.unique_visitors,
            stat.job_page_clicks,
            stat.profile_views,
            stat.application_clicks,
            stat.contact_clicks,
            stat.click_through_rate,
            stat.engagement_rate
        ])
    
    return response
