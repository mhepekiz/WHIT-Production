from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class RecruiterPackage(models.Model):
    """Different subscription packages for recruiters"""
    ANALYTICS_LEVEL_CHOICES = [
        ('basic', 'Basic Analytics'),
        ('standard', 'Standard Analytics'),
        ('advanced', 'Advanced Analytics'),
        ('premium', 'Premium Analytics'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Job posting limits
    monthly_job_openings = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of job openings that can be created per month (0 = unlimited)"
    )
    
    # Analytics features
    analytics_level = models.CharField(
        max_length=20,
        choices=ANALYTICS_LEVEL_CHOICES,
        default='basic'
    )
    
    # Candidate search limits
    monthly_candidate_searches = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of candidate profiles that can be searched/viewed per month (0 = unlimited)"
    )
    candidate_profile_access = models.BooleanField(
        default=True,
        help_text="Can view detailed candidate profiles"
    )
    
    # Messaging features
    messaging_enabled = models.BooleanField(default=False)
    monthly_messages = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        help_text="Number of messages that can be sent per month (0 = unlimited if messaging enabled)"
    )
    
    # Additional features
    featured_job_posts = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        help_text="Number of jobs that can be featured per month"
    )
    priority_support = models.BooleanField(default=False)
    can_export_data = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ${self.price}/month"


class Recruiter(models.Model):
    """Recruiter profile - separate from regular users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    package = models.ForeignKey(RecruiterPackage, on_delete=models.PROTECT, related_name='recruiters')
    
    # Company information
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to='recruiter_logos/', blank=True, null=True)
    company_description = models.TextField(blank=True)
    
    # Contact information
    phone_number = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField()
    
    # Address
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    subscription_start_date = models.DateField(default=timezone.now)
    subscription_end_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.user.email}"
    
    def reset_monthly_usage(self):
        """Reset monthly usage counters"""
        self.usage.filter(
            year=timezone.now().year,
            month=timezone.now().month
        ).update(
            job_openings_created=0,
            candidates_searched=0,
            messages_sent=0
        )


class RecruiterUsage(models.Model):
    """Track monthly usage for package limits"""
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='usage')
    year = models.IntegerField()
    month = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Usage counters
    job_openings_created = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    candidates_searched = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    messages_sent = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    featured_jobs_used = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['recruiter', 'year', 'month']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.recruiter.company_name} - {self.year}/{self.month}"
    
    def can_create_job_opening(self):
        """Check if recruiter can create more job openings"""
        limit = self.recruiter.package.monthly_job_openings
        if limit == 0:  # Unlimited
            return True
        return self.job_openings_created < limit
    
    def can_search_candidate(self):
        """Check if recruiter can search more candidates"""
        limit = self.recruiter.package.monthly_candidate_searches
        if limit == 0:  # Unlimited
            return True
        return self.candidates_searched < limit
    
    def can_send_message(self):
        """Check if recruiter can send more messages"""
        if not self.recruiter.package.messaging_enabled:
            return False
        limit = self.recruiter.package.monthly_messages
        if limit == 0:  # Unlimited
            return True
        return self.messages_sent < limit


class JobOpening(models.Model):
    """Job openings posted by recruiters"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead/Manager'),
        ('executive', 'Executive'),
    ]
    
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='job_openings')
    
    # Job details
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField(blank=True)
    
    # Job specifics
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    
    # Location
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    remote_allowed = models.BooleanField(default=False)
    
    # Skills and categories
    skills_required = models.JSONField(default=list, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    # Status and features
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # Application details
    application_deadline = models.DateField(null=True, blank=True)
    application_url = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)
    
    # Analytics
    views_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    applications_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['recruiter', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recruiter.company_name}"
    
    def publish(self):
        """Publish the job opening"""
        if self.status == 'draft':
            self.status = 'active'
            self.published_at = timezone.now()
            self.save()


class JobApplication(models.Model):
    """Track applications to job openings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('interview', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    candidate_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    
    # Application details
    cover_letter = models.TextField(blank=True)
    resume_file = models.FileField(upload_to='applications/resumes/', blank=True, null=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    recruiter_notes = models.TextField(blank=True)
    interview_date = models.DateTimeField(blank=True, null=True, help_text="Scheduled interview date and time")
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job_opening', 'candidate_user']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.candidate_user.get_full_name()} - {self.job_opening.title}"


class CandidateSearch(models.Model):
    """Track candidate profile searches by recruiters"""
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='candidate_searches')
    candidate_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_searches')
    
    # Search context
    search_query = models.CharField(max_length=255, blank=True)
    viewed_full_profile = models.BooleanField(default=False)
    
    # Notes
    recruiter_notes = models.TextField(blank=True)
    is_saved = models.BooleanField(default=False)
    
    # Timestamps
    searched_at = models.DateTimeField(auto_now_add=True)
    last_viewed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-searched_at']
        indexes = [
            models.Index(fields=['recruiter', '-searched_at']),
            models.Index(fields=['is_saved']),
        ]
    
    def __str__(self):
        return f"{self.recruiter.company_name} viewed {self.candidate_user.get_full_name()}"


class RecruiterMessage(models.Model):
    """Messages between recruiters and candidates"""
    sender_recruiter = models.ForeignKey(
        Recruiter, 
        on_delete=models.CASCADE, 
        related_name='sent_messages',
        null=True,
        blank=True
    )
    sender_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_recruiter_messages',
        null=True,
        blank=True
    )
    recipient_recruiter = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        related_name='received_messages',
        null=True,
        blank=True
    )
    recipient_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_recruiter_messages',
        null=True,
        blank=True
    )
    
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Related job (optional)
    related_job = models.ForeignKey(
        JobOpening,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        sender = self.sender_recruiter or self.sender_user
        recipient = self.recipient_recruiter or self.recipient_user
        return f"{sender} to {recipient}: {self.subject}"
