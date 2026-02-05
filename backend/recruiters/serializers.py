from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import (
    Recruiter, RecruiterPackage, JobOpening, JobApplication,
    CandidateSearch, RecruiterUsage, RecruiterMessage
)


class RecruiterPackageSerializer(serializers.ModelSerializer):
    """Serializer for recruiter packages"""
    class Meta:
        model = RecruiterPackage
        fields = [
            'id', 'name', 'description', 'price',
            'monthly_job_openings', 'analytics_level',
            'monthly_candidate_searches', 'candidate_profile_access',
            'messaging_enabled', 'monthly_messages',
            'featured_job_posts', 'priority_support', 'can_export_data',
            'is_active'
        ]
        read_only_fields = ['id']


class RecruiterRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for recruiter registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    # Company information
    company_name = serializers.CharField(required=True)
    company_website = serializers.URLField(required=False, allow_blank=True)
    company_description = serializers.CharField(required=False, allow_blank=True)
    contact_email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    
    # Address
    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    
    # Package selection
    package_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'first_name', 'last_name',
            'company_name', 'company_website', 'company_description',
            'contact_email', 'phone_number', 'address', 'city', 'state',
            'country', 'postal_code', 'package_id'
        ]
    
    def validate_email(self, value):
        """Validate that the email is a company email (not a generic provider)"""
        import re
        
        print(f"DEBUG: validate_email called with value: {value}")
        
        generic_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'mail.com', 'protonmail.com',
            'zoho.com', 'yandex.com', 'gmx.com', 'inbox.com',
            'live.com', 'msn.com', 'me.com', 'mac.com'
        ]
        
        # Generic domain patterns to catch variations and typos
        generic_patterns = [
            r'.*gmail\..*',
            r'.*yahoo\..*', 
            r'.*hotmail\..*',
            r'.*outlook\..*',
            r'.*aol\..*',
            r'.*icloud\..*',
            r'.*mail\.com.*',
            r'.*proton.*mail\..*',
            r'.*live\..*',
            r'.*msn\..*'
        ]
        
        email_domain = value.split('@')[-1].lower()
        print(f"DEBUG: Extracted domain: {email_domain}")
        
        # Check exact matches
        if email_domain in generic_domains:
            print(f"DEBUG: Domain {email_domain} found in generic_domains list")
            raise serializers.ValidationError(
                "Please use a company email address. Generic email providers (Gmail, Yahoo, etc.) are not allowed for recruiter registration."
            )
        
        # Check patterns to catch typos like gmail.cmo
        for pattern in generic_patterns:
            if re.match(pattern, email_domain):
                print(f"DEBUG: Domain {email_domain} matched pattern {pattern}")
                raise serializers.ValidationError(
                    "Please use a company email address. Generic email providers (Gmail, Yahoo, etc.) are not allowed for recruiter registration."
                )
        
        print(f"DEBUG: Email {value} passed validation")
        return value
    
    def validate_contact_email(self, value):
        """Validate that the contact email is a company email"""
        import re
        
        print(f"DEBUG: validate_contact_email called with value: {value}")
        
        generic_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'mail.com', 'protonmail.com',
            'zoho.com', 'yandex.com', 'gmx.com', 'inbox.com',
            'live.com', 'msn.com', 'me.com', 'mac.com'
        ]
        
        # Generic domain patterns to catch variations and typos
        generic_patterns = [
            r'.*gmail\..*',
            r'.*yahoo\..*',
            r'.*hotmail\..*',
            r'.*outlook\..*',
            r'.*aol\..*',
            r'.*icloud\..*',
            r'.*mail\.com.*',
            r'.*proton.*mail\..*',
            r'.*live\..*',
            r'.*msn\..*'
        ]
        
        email_domain = value.split('@')[-1].lower()
        print(f"DEBUG: Contact email domain: {email_domain}")
        
        # Check exact matches
        if email_domain in generic_domains:
            print(f"DEBUG: Contact domain {email_domain} found in generic_domains list")
            raise serializers.ValidationError(
                "Please use a company email address for contact information."
            )
        
        # Check patterns to catch typos like gmail.cmo
        for pattern in generic_patterns:
            if re.match(pattern, email_domain):
                print(f"DEBUG: Contact domain {email_domain} matched pattern {pattern}")
                raise serializers.ValidationError(
                    "Please use a company email address for contact information."
                )
        
        print(f"DEBUG: Contact email {value} passed validation")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})  # nosec B105
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        # Check if package exists and is active
        try:
            package = RecruiterPackage.objects.get(id=attrs['package_id'], is_active=True)
        except RecruiterPackage.DoesNotExist:
            raise serializers.ValidationError({"package_id": "Invalid or inactive package selected."})
        
        return attrs
    
    def create(self, validated_data):
        # Remove password2 and recruiter-specific fields
        validated_data.pop('password2')
        company_name = validated_data.pop('company_name')
        company_website = validated_data.pop('company_website', '')
        company_description = validated_data.pop('company_description', '')
        contact_email = validated_data.pop('contact_email')
        phone_number = validated_data.pop('phone_number', '')
        address = validated_data.pop('address', '')
        city = validated_data.pop('city', '')
        state = validated_data.pop('state', '')
        country = validated_data.pop('country', '')
        postal_code = validated_data.pop('postal_code', '')
        package_id = validated_data.pop('package_id')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # Create recruiter profile
        package = RecruiterPackage.objects.get(id=package_id)
        recruiter = Recruiter.objects.create(
            user=user,
            package=package,
            company_name=company_name,
            company_website=company_website,
            company_description=company_description,
            contact_email=contact_email,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code
        )
        
        # Create initial usage record for current month
        from django.utils import timezone
        now = timezone.now()
        RecruiterUsage.objects.create(
            recruiter=recruiter,
            year=now.year,
            month=now.month
        )
        
        return user


class RecruiterSerializer(serializers.ModelSerializer):
    """Serializer for recruiter profile"""
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    package = RecruiterPackageSerializer(read_only=True)
    package_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Recruiter
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'company_name', 'company_website', 'company_logo', 'company_description',
            'phone_number', 'contact_email', 'address', 'city', 'state',
            'country', 'postal_code', 'is_verified', 'is_active',
            'subscription_start_date', 'subscription_end_date',
            'package', 'package_id', 'created_at'
        ]
        read_only_fields = ['id', 'email', 'is_verified', 'is_active', 'created_at']
    
    def update(self, instance, validated_data):
        # Update user fields
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()
        
        # Update package if provided
        package_id = validated_data.pop('package_id', None)
        if package_id:
            try:
                package = RecruiterPackage.objects.get(id=package_id, is_active=True)
                instance.package = package
            except RecruiterPackage.DoesNotExist:
                pass
        
        # Update recruiter fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class RecruiterUsageSerializer(serializers.ModelSerializer):
    """Serializer for recruiter usage tracking"""
    package_limits = serializers.SerializerMethodField()
    
    class Meta:
        model = RecruiterUsage
        fields = [
            'id', 'year', 'month', 'job_openings_created',
            'candidates_searched', 'messages_sent', 'featured_jobs_used',
            'package_limits'
        ]
        read_only_fields = ['id']
    
    def get_package_limits(self, obj):
        package = obj.recruiter.package
        return {
            'monthly_job_openings': package.monthly_job_openings,
            'monthly_candidate_searches': package.monthly_candidate_searches,
            'monthly_messages': package.monthly_messages,
            'featured_job_posts': package.featured_job_posts,
            'can_create_job_opening': obj.can_create_job_opening(),
            'can_search_candidate': obj.can_search_candidate(),
            'can_send_message': obj.can_send_message(),
        }


class JobOpeningSerializer(serializers.ModelSerializer):
    """Serializer for job openings"""
    recruiter_company = serializers.CharField(source='recruiter.company_name', read_only=True)
    
    class Meta:
        model = JobOpening
        fields = [
            'id', 'recruiter', 'recruiter_company', 'title', 'description',
            'requirements', 'responsibilities', 'employment_type', 'experience_level',
            'salary_min', 'salary_max', 'salary_currency', 'location', 'city',
            'state', 'country', 'remote_allowed', 'skills_required', 'department',
            'status', 'is_featured', 'application_deadline', 'application_url',
            'application_email', 'views_count', 'applications_count',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'id', 'recruiter', 'recruiter_company', 'views_count',
            'applications_count', 'created_at', 'updated_at', 'published_at'
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for job applications with full candidate details"""
    job_title = serializers.CharField(source='job_opening.title', read_only=True)
    job_department = serializers.CharField(source='job_opening.department', read_only=True)
    candidate_name = serializers.SerializerMethodField()
    candidate_email = serializers.SerializerMethodField()
    candidate_phone = serializers.SerializerMethodField()
    candidate_profile = serializers.SerializerMethodField()
    can_view_contact = serializers.SerializerMethodField()
    profile_resume = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job_opening', 'job_title', 'job_department', 'candidate_user',
            'candidate_name', 'candidate_email', 'candidate_phone', 
            'candidate_profile', 'can_view_contact', 'cover_letter',
            'resume_file', 'profile_resume', 'status', 'recruiter_notes',
            'interview_date', 'applied_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'job_title', 'job_department', 'candidate_name', 
            'candidate_email', 'candidate_phone', 'candidate_profile',
            'can_view_contact', 'profile_resume', 'applied_at', 'updated_at'
        ]
    
    def get_candidate_name(self, obj):
        return obj.candidate_user.get_full_name()
    
    def get_can_view_contact(self, obj):
        """Check if recruiter can view contact details based on package"""
        request = self.context.get('request')
        if request and hasattr(request.user, 'recruiter_profile'):
            recruiter = request.user.recruiter_profile
            # Free tier cannot see contact details
            return recruiter.package.name.lower() != 'free'
        return False
    
    def get_candidate_email(self, obj):
        """Return email only if recruiter has premium package"""
        if self.get_can_view_contact(obj):
            return obj.candidate_user.email
        return None
    
    def get_candidate_phone(self, obj):
        """Return phone only if recruiter has premium package"""
        if self.get_can_view_contact(obj):
            try:
                profile = obj.candidate_user.profile
                return profile.phone if hasattr(profile, 'phone') else None
            except Exception:
                return None
        return None
    
    def get_profile_resume(self, obj):
        """Return resume URL from user's profile"""
        try:
            profile = obj.candidate_user.profile
            if profile.resume:
                return profile.resume.url
        except AttributeError:
            # Resume not available
            pass  # nosec B110
        return None
    
    def get_candidate_profile(self, obj):
        """Return full candidate profile details"""
        try:
            profile = obj.candidate_user.profile
        except Exception as e:
            print(f"Error getting profile: {e}")
            return {}
        
        try:
            job_pref = obj.candidate_user.job_preference
        except Exception:
            job_pref = None
        
        # Get desired functions as list of strings
        desired_functions = []
        if job_pref and hasattr(job_pref, 'desired_functions'):
            try:
                desired_functions = [func.name for func in job_pref.desired_functions.all()]
            except (AttributeError, Exception):
                # Job preferences not available
                pass  # nosec B110
        
        return {
            'current_title': profile.current_title or '',
            'location': profile.location or '',
            'bio': profile.bio or '',
            'years_of_experience': profile.years_of_experience or 0,
            'linkedin_url': profile.linkedin_url or '',
            'github_url': profile.github_url or '',
            'portfolio_url': profile.portfolio_url or '',
            'desired_roles': desired_functions,
            'employment_type': job_pref.employment_types if job_pref else '',
            'remote_only': job_pref.remote_only if job_pref else False,
            'expected_salary_min': job_pref.minimum_salary if job_pref else None,
            'expected_salary_max': job_pref.minimum_salary if job_pref else None,
            'actively_looking': job_pref.actively_looking if job_pref else False,
        }


class CandidateSearchSerializer(serializers.ModelSerializer):
    """Serializer for candidate searches"""
    candidate_name = serializers.SerializerMethodField()
    candidate_email = serializers.EmailField(source='candidate_user.email', read_only=True)
    
    class Meta:
        model = CandidateSearch
        fields = [
            'id', 'recruiter', 'candidate_user', 'candidate_name',
            'candidate_email', 'search_query', 'viewed_full_profile',
            'recruiter_notes', 'is_saved', 'searched_at', 'last_viewed_at'
        ]
        read_only_fields = [
            'id', 'recruiter', 'candidate_name', 'candidate_email',
            'searched_at', 'last_viewed_at'
        ]
    
    def get_candidate_name(self, obj):
        return obj.candidate_user.get_full_name()


class RecruiterMessageSerializer(serializers.ModelSerializer):
    """Serializer for recruiter messages"""
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = RecruiterMessage
        fields = [
            'id', 'sender_recruiter', 'sender_user', 'recipient_recruiter',
            'recipient_user', 'sender_name', 'recipient_name', 'subject',
            'message', 'is_read', 'read_at', 'related_job', 'created_at'
        ]
        read_only_fields = ['id', 'sender_name', 'recipient_name', 'created_at', 'read_at']
    
    def get_sender_name(self, obj):
        if obj.sender_recruiter:
            return obj.sender_recruiter.company_name
        elif obj.sender_user:
            return obj.sender_user.get_full_name()
        return "Unknown"
    
    def get_recipient_name(self, obj):
        if obj.recipient_recruiter:
            return obj.recipient_recruiter.company_name
        elif obj.recipient_user:
            return obj.recipient_user.get_full_name()
        return "Unknown"
