from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import (
    RecruiterPackage, Recruiter, RecruiterUsage,
    JobOpening, JobApplication, CandidateSearch, RecruiterMessage
)


@admin.register(RecruiterPackage)
class RecruiterPackageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'price', 'monthly_job_openings', 'analytics_level',
        'monthly_candidate_searches', 'messaging_enabled', 'is_active'
    ]
    list_filter = ['is_active', 'analytics_level', 'messaging_enabled']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'is_active')
        }),
        ('Job Posting Limits', {
            'fields': ('monthly_job_openings', 'featured_job_posts')
        }),
        ('Analytics', {
            'fields': ('analytics_level',)
        }),
        ('Candidate Search', {
            'fields': ('monthly_candidate_searches', 'candidate_profile_access')
        }),
        ('Messaging', {
            'fields': ('messaging_enabled', 'monthly_messages')
        }),
        ('Additional Features', {
            'fields': ('priority_support', 'can_export_data')
        }),
    )


class RecruiterUsageInline(admin.TabularInline):
    model = RecruiterUsage
    extra = 0
    readonly_fields = ['year', 'month', 'job_openings_created', 'candidates_searched', 'messages_sent']
    can_delete = False


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'get_email', 'package', 'is_verified',
        'is_active', 'subscription_start_date', 'created_at', 'password_change_link'
    ]
    list_filter = ['is_verified', 'is_active', 'package', 'created_at']
    search_fields = ['company_name', 'user__email', 'contact_email', 'city', 'country']
    readonly_fields = ['created_at', 'updated_at', 'password_change_link']
    inlines = [RecruiterUsageInline]
    actions = ['change_password_action']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('user', 'package', 'is_verified', 'is_active', 'password_change_link')
        }),
        ('Company Information', {
            'fields': ('company_name', 'company_website', 'company_logo', 'company_description')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'phone_number')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Subscription', {
            'fields': ('subscription_start_date', 'subscription_end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

    def password_change_link(self, obj):
        if obj.pk:
            url = reverse('admin:auth_user_password_change', args=[obj.user.pk])
            return format_html('<a href="{}" class="button">Change Password</a>', url)
        return "-"
    password_change_link.short_description = 'Password'
    password_change_link.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:recruiter_id>/change-password/',
                self.admin_site.admin_view(self.change_password_view),
                name='recruiters_recruiter_change_password',
            ),
        ]
        return custom_urls + urls

    def change_password_view(self, request, recruiter_id):
        recruiter = self.get_object(request, recruiter_id)
        if recruiter is None:
            messages.error(request, 'Recruiter not found.')
            return redirect('admin:recruiters_recruiter_changelist')
        
        # Redirect to the user's password change form
        url = reverse('admin:auth_user_password_change', args=[recruiter.user.pk])
        return HttpResponseRedirect(url)

    def change_password_action(self, request, queryset):
        """Admin action to change password for selected recruiters"""
        if queryset.count() == 1:
            recruiter = queryset.first()
            url = reverse('admin:auth_user_password_change', args=[recruiter.user.pk])
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Please select only one recruiter to change password.')
            return None
    change_password_action.short_description = "Change password for selected recruiter"


@admin.register(RecruiterUsage)
class RecruiterUsageAdmin(admin.ModelAdmin):
    list_display = [
        'recruiter', 'year', 'month', 'job_openings_created',
        'candidates_searched', 'messages_sent', 'featured_jobs_used'
    ]
    list_filter = ['year', 'month', 'recruiter']
    search_fields = ['recruiter__company_name']
    readonly_fields = ['created_at', 'updated_at']


class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    readonly_fields = ['candidate_user', 'applied_at', 'status']
    fields = ['candidate_user', 'status', 'applied_at']
    can_delete = False


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'get_company', 'employment_type', 'location',
        'status', 'is_featured', 'views_count', 'applications_count', 'created_at'
    ]
    list_filter = ['status', 'employment_type', 'experience_level', 'is_featured', 'remote_allowed']
    search_fields = ['title', 'recruiter__company_name', 'city', 'country', 'department']
    readonly_fields = ['views_count', 'applications_count', 'created_at', 'updated_at', 'published_at']
    inlines = [JobApplicationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recruiter', 'title', 'status', 'is_featured')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'responsibilities', 'department')
        }),
        ('Job Specifics', {
            'fields': (
                'employment_type', 'experience_level',
                ('salary_min', 'salary_max', 'salary_currency')
            )
        }),
        ('Location', {
            'fields': ('location', 'city', 'state', 'country', 'remote_allowed')
        }),
        ('Skills', {
            'fields': ('skills_required',)
        }),
        ('Application', {
            'fields': ('application_deadline', 'application_url', 'application_email')
        }),
        ('Analytics', {
            'fields': ('views_count', 'applications_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_company(self, obj):
        return obj.recruiter.company_name
    get_company.short_description = 'Company'
    get_company.admin_order_field = 'recruiter__company_name'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'get_candidate', 'get_job', 'get_company',
        'status', 'applied_at'
    ]
    list_filter = ['status', 'applied_at']
    search_fields = [
        'candidate_user__first_name', 'candidate_user__last_name',
        'candidate_user__email', 'job_opening__title'
    ]
    readonly_fields = ['applied_at', 'updated_at']
    
    fieldsets = (
        ('Application Information', {
            'fields': ('job_opening', 'candidate_user', 'status')
        }),
        ('Application Details', {
            'fields': ('cover_letter', 'resume_file')
        }),
        ('Recruiter Notes', {
            'fields': ('recruiter_notes',)
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_candidate(self, obj):
        return obj.candidate_user.get_full_name()
    get_candidate.short_description = 'Candidate'
    
    def get_job(self, obj):
        return obj.job_opening.title
    get_job.short_description = 'Job'
    
    def get_company(self, obj):
        return obj.job_opening.recruiter.company_name
    get_company.short_description = 'Company'


@admin.register(CandidateSearch)
class CandidateSearchAdmin(admin.ModelAdmin):
    list_display = [
        'get_company', 'get_candidate', 'search_query',
        'viewed_full_profile', 'is_saved', 'searched_at'
    ]
    list_filter = ['viewed_full_profile', 'is_saved', 'searched_at']
    search_fields = [
        'recruiter__company_name', 'candidate_user__first_name',
        'candidate_user__last_name', 'search_query'
    ]
    readonly_fields = ['searched_at', 'last_viewed_at']
    
    def get_company(self, obj):
        return obj.recruiter.company_name
    get_company.short_description = 'Company'
    
    def get_candidate(self, obj):
        return obj.candidate_user.get_full_name()
    get_candidate.short_description = 'Candidate'


@admin.register(RecruiterMessage)
class RecruiterMessageAdmin(admin.ModelAdmin):
    list_display = [
        'get_sender', 'get_recipient', 'subject',
        'is_read', 'created_at'
    ]
    list_filter = ['is_read', 'created_at']
    search_fields = ['subject', 'message']
    readonly_fields = ['created_at', 'read_at']
    
    fieldsets = (
        ('Message Information', {
            'fields': (
                'sender_recruiter', 'sender_user',
                'recipient_recruiter', 'recipient_user',
                'related_job'
            )
        }),
        ('Content', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_sender(self, obj):
        if obj.sender_recruiter:
            return obj.sender_recruiter.company_name
        return obj.sender_user.get_full_name()
    get_sender.short_description = 'From'
    
    def get_recipient(self, obj):
        if obj.recipient_recruiter:
            return obj.recipient_recruiter.company_name
        return obj.recipient_user.get_full_name()
    get_recipient.short_description = 'To'
