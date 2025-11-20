from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import UserProfile, JobPreference


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    
    list_display = ['user', 'current_title', 'location', 'years_of_experience', 'has_resume', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'current_title', 'location']
    list_filter = ['created_at', 'updated_at', 'years_of_experience']
    readonly_fields = ['created_at', 'updated_at', 'resume_uploaded_at', 'resume_link']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',),
            'description': 'Associated user account'
        }),
        ('Personal Information', {
            'fields': ('phone', 'location', 'bio'),
            'description': 'Contact and location details'
        }),
        ('Professional Information', {
            'fields': ('current_title', 'years_of_experience', 'linkedin_url', 'portfolio_url', 'github_url'),
            'description': 'Professional background and social links'
        }),
        ('Resume', {
            'fields': ('resume', 'resume_link', 'resume_uploaded_at'),
            'description': 'Upload and manage candidate resume'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_resume(self, obj):
        """Display if user has uploaded a resume"""
        if obj.resume:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: red;">✗ No</span>')
    has_resume.short_description = 'Resume'
    
    def resume_link(self, obj):
        """Display clickable link to view/download resume"""
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank" style="padding: 5px 10px; background: #2563eb; color: white; text-decoration: none; border-radius: 4px;">View Resume</a>',
                obj.resume.url
            )
        return format_html('<span style="color: #999;">No resume uploaded</span>')
    resume_link.short_description = 'View Resume'
    
    def save_model(self, request, obj, form, change):
        """Auto-update resume_uploaded_at when resume is uploaded"""
        if 'resume' in form.changed_data and obj.resume:
            obj.resume_uploaded_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(JobPreference)
class JobPreferenceAdmin(admin.ModelAdmin):
    """Admin interface for JobPreference model."""
    
    list_display = ['user', 'remote_only', 'willing_to_relocate', 'email_notifications', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['remote_only', 'willing_to_relocate', 'email_notifications', 'job_alerts']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['desired_functions', 'work_environments']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Job Preferences', {
            'fields': ('desired_functions', 'work_environments', 'employment_types')
        }),
        ('Location Preferences', {
            'fields': ('preferred_locations', 'willing_to_relocate', 'remote_only')
        }),
        ('Salary & Company', {
            'fields': ('minimum_salary', 'industries', 'company_size_preference')
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'job_alerts')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
