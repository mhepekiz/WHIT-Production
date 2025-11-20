from django.db import models
from django.contrib.auth.models import User
from companies.models import Function, WorkEnvironment


class UserProfile(models.Model):
    """Extended user profile with job seeker information."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True, help_text="Brief description about yourself")
    
    # Professional Information
    current_title = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)
    portfolio_url = models.URLField(max_length=500, blank=True, null=True)
    github_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Resume
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_uploaded_at = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s profile"


class JobPreference(models.Model):
    """User's job search preferences."""
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    SALARY_RANGE_CHOICES = [
        ('0-50k', '$0 - $50,000'),
        ('50k-75k', '$50,000 - $75,000'),
        ('75k-100k', '$75,000 - $100,000'),
        ('100k-150k', '$100,000 - $150,000'),
        ('150k-200k', '$150,000 - $200,000'),
        ('200k+', '$200,000+'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_preference')
    
    # Job Preferences
    desired_functions = models.ManyToManyField(Function, blank=True, related_name='job_seekers')
    work_environments = models.ManyToManyField(WorkEnvironment, blank=True, related_name='job_seekers')
    employment_types = models.CharField(max_length=255, blank=True, help_text="Comma-separated employment types")
    
    # Location Preferences
    preferred_locations = models.TextField(blank=True, help_text="Comma-separated locations")
    willing_to_relocate = models.BooleanField(default=False)
    remote_only = models.BooleanField(default=False)
    
    # Salary Preferences
    minimum_salary = models.CharField(max_length=20, choices=SALARY_RANGE_CHOICES, blank=True, null=True)
    
    # Other Preferences
    industries = models.TextField(blank=True, help_text="Comma-separated industries")
    company_size_preference = models.CharField(max_length=255, blank=True, help_text="e.g., Startup, Mid-size, Enterprise")
    
    # Notifications
    email_notifications = models.BooleanField(default=True)
    job_alerts = models.BooleanField(default=True)
    
    # Job Search Status
    actively_looking = models.BooleanField(default=False, help_text="User is actively looking for job opportunities")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Job Preference'
        verbose_name_plural = 'Job Preferences'
    
    def __str__(self):
        return f"{self.user.username}'s job preferences"
