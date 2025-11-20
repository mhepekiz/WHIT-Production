from django.contrib import admin
from .models import Company, Function, WorkEnvironment, AdSlot, SiteSettings, FormLayout


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model."""
    
    list_display = [
        'name',
        'country',
        'state',
        'city',
        'status',
        'engineering_positions',
        'updated_at',
    ]
    
    list_filter = [
        'status',
        'engineering_positions',
        'country',
        'state',
    ]
    
    search_fields = [
        'name',
        'city',
        'functions',
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    filter_horizontal = ['functions']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'jobs_page_url', 'company_reviews')
        }),
        ('Location', {
            'fields': ('country', 'state', 'city')
        }),
        ('Work Details', {
            'fields': ('work_environment', 'functions', 'engineering_positions')
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
            'fields': ('banner_image', 'banner_link', 'banner_alt_text', 'open_in_new_tab'),
            'description': 'Upload a banner image and provide a click-through URL'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin interface for SiteSettings model."""
    
    list_display = ['companies_per_page', 'companies_per_group', 'label_size', 'updated_at']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Pagination Settings', {
            'fields': ('companies_per_page', 'companies_per_group')
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
            'fields': ('page_name', 'form_position')
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
            'fields': ('background_color', 'text_color'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
