from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django import forms
from .models import (
    Company, Function, WorkEnvironment, AdSlot, SiteSettings, FormLayout,
    HowItWorksSection, HowItWorksStep, RecruiterSection, CompanyRecruiterAccess,
    CampaignStatistics
)


class CompanyAdminForm(forms.ModelForm):
    """Custom form for Company admin to handle M2M fields properly."""
    
    class Meta:
        model = Company
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make functions field not required
        if 'functions' in self.fields:
            self.fields['functions'].required = False


class CompanyRecruiterAccessInline(admin.TabularInline):
    """Inline for managing recruiter access to companies"""
    model = CompanyRecruiterAccess
    extra = 0
    fields = (
        'recruiter', 'access_level', 'can_see_sponsored_stats',
        'can_manage_campaigns', 'can_view_analytics', 'can_export_data', 'notes'
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recruiter__user')


class CampaignStatisticsInline(admin.TabularInline):
    """Inline for viewing campaign statistics"""
    model = CampaignStatistics
    extra = 0
    fields = (
        'date', 'page_views', 'unique_visitors', 'job_page_clicks',
        'profile_views', 'application_clicks', 'contact_clicks',
        'click_through_rate', 'engagement_rate'
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request, obj=None):
        return False  # Don't allow adding through inline


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model."""
    
    form = CompanyAdminForm
    inlines = [CompanyRecruiterAccessInline, CampaignStatisticsInline]
    
    list_display = [
        'name',
        'logo_preview',
        'country',
        'state',
        'city',
        'status',
        'is_sponsored',
        'sponsor_order',
        'engineering_positions',
        'updated_at',
    ]
    
    list_filter = [
        'status',
        'is_sponsored',
        'engineering_positions',
        'country',
        'state',
    ]
    
    search_fields = [
        'name',
        'city',
        'functions',
    ]
    
    readonly_fields = ['created_at', 'updated_at', 'logo_preview']
    
    def get_fields(self, request, obj=None):
        """Override get_fields to exclude M2M fields when adding new objects."""
        fields = list(super().get_fields(request, obj))
        if obj is None:  # Adding new object
            # Exclude functions field to avoid M2M error
            if 'functions' in fields:
                fields.remove('functions')
        return fields
    
    def get_form(self, request, obj=None, **kwargs):
        """Override get_form to handle M2M fields properly."""
        form = super().get_form(request, obj, **kwargs)
        # Only show filter_horizontal for existing objects
        if obj is not None:
            self.filter_horizontal = ['functions']
        else:
            self.filter_horizontal = []
        return form
    
    def save_model(self, request, obj, form, change):
        # Check sponsored limit before saving
        if obj.is_sponsored:
            sponsored_count = Company.objects.filter(is_sponsored=True).exclude(pk=obj.pk).count()
            if sponsored_count >= 3:
                messages.error(request, "Maximum of 3 sponsored companies allowed. Please unmark another company as sponsored first.")
                return
        super().save_model(request, obj, form, change)
    
    def response_add(self, request, obj, post_url_continue=None):
        """Override response_add to redirect to change form after adding so user can set functions."""
        if obj:
            # Add a success message mentioning they can now set functions
            messages.success(request, f'Company "{obj.name}" was added successfully. You can now set functions and other details.')
        return super().response_add(request, obj, post_url_continue)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'logo_preview', 'jobs_page_url', 'company_reviews')
        }),
        ('Location', {
            'fields': ('country', 'state', 'city')
        }),
        ('Work Details', {
            'fields': ('work_environment', 'functions', 'engineering_positions')
        }),
        ('Sponsorship', {
            'fields': ('is_sponsored', 'sponsor_order'),
            'description': 'Maximum 3 sponsored companies allowed. Lower sponsor_order numbers appear first.'
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 50
    
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status='Active')
        self.message_user(request, f'{updated} companies marked as active.')
    mark_as_active.short_description = 'Mark selected companies as Active'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(status='Inactive')
        self.message_user(request, f'{updated} companies marked as inactive.')
    mark_as_inactive.short_description = 'Mark selected companies as Inactive'


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    """Admin interface for Function model."""
    
    list_display = ['name', 'color', 'text_color']
    search_fields = ['name']
    list_editable = ['color', 'text_color']


@admin.register(WorkEnvironment)
class WorkEnvironmentAdmin(admin.ModelAdmin):
    """Admin interface for WorkEnvironment model."""
    
    list_display = ['name']
    search_fields = ['name']


@admin.register(AdSlot)
class AdSlotAdmin(admin.ModelAdmin):
    """Admin interface for AdSlot model."""
    
    list_display = ['slot_name', 'ad_type', 'is_active', 'updated_at']
    list_filter = ['is_active', 'ad_type']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Ad Slot Configuration', {
            'fields': ('slot_name', 'ad_type', 'is_active')
        }),
        ('Ad Code Option', {
            'fields': ('ad_code',),
            'description': 'Use this for Google AdSense or custom ad scripts'
        }),
        ('Image Banner Option', {
            'fields': ('banner_image', 'mobile_banner_image', 'banner_link', 'banner_alt_text', 'open_in_new_tab'),
            'description': 'Upload banner images and provide a click-through URL. Mobile banner is optional - desktop banner will be used if mobile is not provided.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin interface for SiteSettings model."""
    
    list_display = ['homepage_companies', 'homepage_sort_order', 'companies_per_page', 'companies_per_group', 'label_size', 'updated_at']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Homepage Settings', {
            'fields': ('homepage_companies', 'homepage_sort_order'),
            'description': 'Number of companies and sort order on the homepage before the "Show All Companies" button.'
        }),
        ('Listing Page Settings', {
            'fields': ('companies_per_page', 'companies_per_group'),
            'description': 'Settings for the /all-companies listing page.'
        }),
        ('Display Settings', {
            'fields': ('label_size',)
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent creating multiple instances
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the settings
        return False


@admin.register(FormLayout)
class FormLayoutAdmin(admin.ModelAdmin):
    """Admin interface for FormLayout model."""
    
    list_display = ['page_name', 'form_position', 'side_heading', 'updated_at']
    list_filter = ['page_name', 'form_position']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Page Configuration', {
            'fields': ('page_name', 'form_position', 'image_width_percentage')
        }),
        ('Side Panel Content', {
            'fields': (
                ('side_heading', 'side_heading_tag'),
                ('side_subheading', 'side_subheading_tag'),
                ('side_text', 'side_text_tag'),
                'side_image',
                'side_image_url',
                'text_overlay_position'
            ),
            'description': 'Content displayed on the opposite side when form is positioned left or right'
        }),
        ('Styling', {
            'fields': ('background_color', 'text_color', 'button_color'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Sponsor Campaign Admin
from .models import SponsorCampaign, SponsorStatsDaily, SponsorDeliveryLog


@admin.register(SponsorCampaign)
class SponsorCampaignAdmin(admin.ModelAdmin):
    """Admin interface for managing sponsor campaigns."""
    
    list_display = [
        'name',
        'company',
        'status', 
        'start_at',
        'end_at',
        'priority',
        'daily_impression_cap',
        'impressions_today_display',
        'clicks_today_display',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'priority',
        'pacing',
        'start_at',
        'end_at',
        'company'
    ]
    
    search_fields = ['name', 'company__name']
    
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'impressions_today_display',
        'clicks_today_display',
        'campaign_performance'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company', 'status')
        }),
        ('Schedule', {
            'fields': ('start_at', 'end_at')
        }),
        ('Delivery Settings', {
            'fields': (
                'priority', 
                'weight',
                'daily_impression_cap', 
                'daily_click_cap',
                'pacing'
            )
        }),
        ('Targeting', {
            'fields': (
                'targeting_countries',
                'targeting_functions', 
                'targeting_work_env'
            ),
            'classes': ('collapse',)
        }),
        ('Advanced', {
            'fields': ('bid_cpm', 'created_by'),
            'classes': ('collapse',)
        }),
        ('Performance (Read-Only)', {
            'fields': (
                'impressions_today_display',
                'clicks_today_display', 
                'campaign_performance'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def impressions_today_display(self, obj):
        """Display today's impression count"""
        return f"{obj.impressions_today()} / {obj.daily_impression_cap}"
    impressions_today_display.short_description = "Today's Impressions"
    
    def clicks_today_display(self, obj):
        """Display today's click count"""
        clicks = obj.clicks_today()
        if obj.daily_click_cap:
            return f"{clicks} / {obj.daily_click_cap}"
        return str(clicks)
    clicks_today_display.short_description = "Today's Clicks"
    
    def campaign_performance(self, obj):
        """Display campaign performance summary"""
        from django.utils.html import format_html
        from django.utils import timezone
        
        stats = obj.stats_daily.filter(
            date__gte=timezone.now().date() - timezone.timedelta(days=7)
        ).order_by('-date')
        
        if not stats.exists():
            return "No recent activity"
            
        total_impressions = sum(s.impressions for s in stats)
        total_clicks = sum(s.clicks for s in stats)
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        
        return format_html(
            "<strong>Last 7 days:</strong><br/>"
            "Impressions: {}<br/>"
            "Clicks: {}<br/>"
            "CTR: {:.2f}%",
            total_impressions,
            total_clicks,
            ctr
        )
    campaign_performance.short_description = "Performance Summary"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new campaign
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SponsorStatsDaily)
class SponsorStatsDailyAdmin(admin.ModelAdmin):
    """Admin interface for daily sponsor stats."""
    
    list_display = [
        'campaign',
        'date', 
        'impressions',
        'clicks',
        'ctr_display'
    ]
    
    list_filter = ['date', 'campaign__company']
    search_fields = ['campaign__name', 'campaign__company__name']
    readonly_fields = ['ctr_display']
    
    def ctr_display(self, obj):
        """Calculate and display CTR"""
        if obj.impressions > 0:
            ctr = (obj.clicks / obj.impressions) * 100
            return f"{ctr:.2f}%"
        return "0.00%"
    ctr_display.short_description = "CTR"


@admin.register(SponsorDeliveryLog) 
class SponsorDeliveryLogAdmin(admin.ModelAdmin):
    """Admin interface for sponsor delivery logs."""
    
    list_display = [
        'campaign',
        'user_hash_short',
        'action',
        'page_key_short',
        'shown_at'
    ]
    
    list_filter = ['action', 'shown_at', 'campaign__company']
    search_fields = ['campaign__name', 'user_hash', 'page_key']
    readonly_fields = ['shown_at']
    
    def user_hash_short(self, obj):
        """Display shortened user hash"""
        return obj.user_hash[:12] + "..." if len(obj.user_hash) > 12 else obj.user_hash
    user_hash_short.short_description = "User"
    
    def page_key_short(self, obj):
        """Display shortened page key"""
        return obj.page_key[:30] + "..." if len(obj.page_key) > 30 else obj.page_key
    page_key_short.short_description = "Page Context"


class HowItWorksStepInline(admin.TabularInline):
    """Inline admin for How It Works Steps"""
    model = HowItWorksStep
    extra = 3
    fields = ['step_number', 'icon', 'title', 'description', 'is_active', 'order']
    ordering = ['order', 'step_number']


@admin.register(HowItWorksSection)
class HowItWorksSectionAdmin(admin.ModelAdmin):
    """Admin interface for How It Works Section"""
    
    list_display = [
        'title',
        'is_active',
        'order',
        'steps_count',
        'updated_at'
    ]
    
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['created_at', 'updated_at']
    
    inlines = [HowItWorksStepInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'section_header', 'description')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def steps_count(self, obj):
        """Display number of steps"""
        return obj.steps.count()
    steps_count.short_description = "Steps"


@admin.register(RecruiterSection)
class RecruiterSectionAdmin(admin.ModelAdmin):
    """Admin interface for Recruiter Section"""
    
    list_display = [
        'title',
        'button_text',
        'is_active',
        'order',
        'updated_at'
    ]
    
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'button_text', 'button_link')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Styling', {
            'fields': ('background_color', 'text_color', 'button_color'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(CompanyRecruiterAccess)
class CompanyRecruiterAccessAdmin(admin.ModelAdmin):
    """Admin interface for managing recruiter access to companies"""
    
    list_display = [
        'company',
        'recruiter',
        'access_level',
        'can_see_sponsored_stats',
        'can_manage_campaigns',
        'can_view_analytics',
        'can_export_data',
        'created_at'
    ]
    
    list_filter = [
        'access_level',
        'can_see_sponsored_stats',
        'can_manage_campaigns',
        'can_view_analytics',
        'can_export_data'
    ]
    
    search_fields = [
        'company__name',
        'recruiter__company_name',
        'recruiter__user__email'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Assignment', {
            'fields': ('company', 'recruiter')
        }),
        ('Access Level', {
            'fields': ('access_level', 'can_see_sponsored_stats')
        }),
        ('Detailed Permissions', {
            'fields': ('can_manage_campaigns', 'can_view_analytics', 'can_export_data'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'company', 'recruiter__user'
        )


@admin.register(CampaignStatistics)
class CampaignStatisticsAdmin(admin.ModelAdmin):
    """Admin interface for campaign statistics"""
    
    list_display = [
        'company',
        'date',
        'page_views',
        'unique_visitors',
        'job_page_clicks',
        'profile_views',
        'click_through_rate',
        'engagement_rate'
    ]
    
    list_filter = [
        'date',
        'company__is_sponsored'
    ]
    
    search_fields = [
        'company__name'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('company', 'date')
        }),
        ('Traffic Metrics', {
            'fields': ('page_views', 'unique_visitors', 'job_page_clicks')
        }),
        ('Engagement Metrics', {
            'fields': ('profile_views', 'application_clicks', 'contact_clicks')
        }),
        ('Performance Metrics', {
            'fields': ('click_through_rate', 'engagement_rate')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
