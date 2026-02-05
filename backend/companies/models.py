from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


class Company(models.Model):
    """Model representing a company that is hiring."""
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, help_text='Upload company logo image')
    jobs_page_url = models.URLField(max_length=500)
    company_reviews = models.URLField(max_length=500, blank=True, null=True)
    
    # Location
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    # Work Details
    work_environment = models.CharField(max_length=255, help_text="e.g., Remote, On-Site, Hybrid")
    functions = models.ManyToManyField('Function', related_name='companies', blank=True)
    
    # Legacy field for migration
    functions_text = models.TextField(blank=True, help_text="Legacy comma-separated list of functions")
    
    # Status
    engineering_positions = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    
    # Sponsorship
    is_sponsored = models.BooleanField(default=False, help_text="Mark as sponsored company")
    sponsor_order = models.PositiveIntegerField(default=0, help_text="Order for sponsored companies (lower numbers first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['-is_sponsored', 'sponsor_order', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country', 'state', 'city']),
            models.Index(fields=['status']),
            models.Index(fields=['is_sponsored', 'sponsor_order']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_functions_list(self):
        """Return functions as a list of dicts with name and color."""
        return [
            {
                'name': func.name,
                'color': func.color,
                'text_color': func.text_color
            }
            for func in self.functions.all()
        ]
    
    def get_work_environment_list(self):
        """Return work environment options as a list."""
        if self.work_environment:
            return [w.strip() for w in self.work_environment.split(',')]
        return []
    
    def logo_preview(self):
        """Return HTML for logo preview in admin."""
        if self.logo:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: contain;" />',
                self.logo.url
            )
        return 'No logo'
    logo_preview.short_description = 'Logo Preview'


class Function(models.Model):
    """Model for storing unique function/department names with colors."""
    
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#e3f2fd', help_text='Hex color code for the tag')
    text_color = models.CharField(max_length=7, default='#1976d2', help_text='Hex color code for the text')
    
    class Meta:
        verbose_name = 'Function'
        verbose_name_plural = 'Functions'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class WorkEnvironment(models.Model):
    """Model for storing work environment types."""
    
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Work Environment'
        verbose_name_plural = 'Work Environments'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class AdSlot(models.Model):
    """Model for managing ad slots between company listings."""
    
    SLOT_CHOICES = [
        ('slot1', 'Ad Slot 1 (After first 10 companies)'),
        ('slot2', 'Ad Slot 2 (After second 10 companies)'),
    ]
    
    AD_TYPE_CHOICES = [
        ('code', 'Ad Code (Google AdSense, etc.)'),
        ('image', 'Image Banner with Link'),
    ]
    
    slot_name = models.CharField(max_length=20, choices=SLOT_CHOICES, unique=True)
    ad_type = models.CharField(
        max_length=10,
        choices=AD_TYPE_CHOICES,
        default='code',
        help_text='Choose ad type: code or image banner'
    )
    
    # For ad code type
    ad_code = models.TextField(
        blank=True,
        help_text='Paste your Google AdSense or ad network code here'
    )
    
    # For image banner type
    banner_image = models.ImageField(
        upload_to='ad_banners/',
        blank=True,
        null=True,
        help_text='Upload desktop banner image'
    )
    mobile_banner_image = models.ImageField(
        upload_to='ad_banners/',
        blank=True,
        null=True,
        help_text='Upload mobile banner image (optional - will use desktop banner if not provided)'
    )
    banner_link = models.URLField(
        max_length=500,
        blank=True,
        help_text='URL to redirect when banner is clicked'
    )
    banner_alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text='Alt text for banner image (optional)'
    )
    open_in_new_tab = models.BooleanField(
        default=True,
        help_text='Open banner link in new tab'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ad Slot'
        verbose_name_plural = 'Ad Slots'
        ordering = ['slot_name']
    
    def __str__(self):
        return f'{self.get_slot_name_display()}'


class SiteSettings(models.Model):
    """Singleton model for site-wide settings."""
    
    LABEL_SIZE_CHOICES = [
        ('small', 'Small (0.5rem)'),
        ('medium', 'Medium (0.7rem)'),
        ('large', 'Large (0.9rem)'),
        ('extra-large', 'Extra Large (1.1rem)'),
    ]
    
    companies_per_page = models.IntegerField(
        default=30,
        help_text='Number of companies to display per page'
    )
    companies_per_group = models.IntegerField(
        default=10,
        help_text='Number of companies in each group (between ad slots)'
    )
    label_size = models.CharField(
        max_length=20,
        choices=LABEL_SIZE_CHOICES,
        default='medium',
        help_text='Size of function and work environment labels'
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return 'Site Settings'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class FormLayout(models.Model):
    """Model for managing form page layouts (login, register, etc.)."""
    
    PAGE_CHOICES = [
        ('login', 'Login Page'),
        ('register', 'Register Page'),
    ]
    
    POSITION_CHOICES = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ]
    
    TEXT_OVERLAY_CHOICES = [
        ('top-left', 'Top Left'),
        ('top-center', 'Top Center'),
        ('top-right', 'Top Right'),
        ('center-left', 'Center Left'),
        ('center-center', 'Center Center'),
        ('center-right', 'Center Right'),
        ('bottom-left', 'Bottom Left'),
        ('bottom-center', 'Bottom Center'),
        ('bottom-right', 'Bottom Right'),
    ]
    
    HTML_TAG_CHOICES = [
        ('h1', 'H1 - Main Heading'),
        ('h2', 'H2 - Subheading'),
        ('h3', 'H3 - Subheading'),
        ('h4', 'H4 - Subheading'),
        ('h5', 'H5 - Subheading'),
        ('h6', 'H6 - Subheading'),
        ('p', 'P - Paragraph'),
        ('span', 'Span - Inline Text'),
        ('div', 'Div - Block Text'),
    ]
    
    page_name = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    form_position = models.CharField(
        max_length=10,
        choices=POSITION_CHOICES,
        default='center',
        help_text='Position of the form on the page'
    )
    
    # Content for the opposite side (when form is left or right)
    side_heading = models.CharField(
        max_length=200,
        blank=True,
        help_text='Heading text for the opposite side'
    )
    side_heading_tag = models.CharField(
        max_length=10,
        choices=HTML_TAG_CHOICES,
        default='h1',
        help_text='HTML tag for the heading'
    )
    side_subheading = models.CharField(
        max_length=300,
        blank=True,
        help_text='Subheading text for the opposite side'
    )
    side_subheading_tag = models.CharField(
        max_length=10,
        choices=HTML_TAG_CHOICES,
        default='h2',
        help_text='HTML tag for the subheading'
    )
    side_text = models.TextField(
        blank=True,
        help_text='Additional text content for the opposite side'
    )
    side_text_tag = models.CharField(
        max_length=10,
        choices=HTML_TAG_CHOICES,
        default='p',
        help_text='HTML tag for the text'
    )
    side_image = models.FileField(
        upload_to='form_layouts/',
        blank=True,
        null=True,
        help_text='Image to display on the opposite side'
    )
    side_image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Or use an external image URL'
    )
    text_overlay_position = models.CharField(
        max_length=20,
        choices=TEXT_OVERLAY_CHOICES,
        default='center-center',
        help_text='Position of text overlay on the image'
    )
    
    # Styling
    background_color = models.CharField(
        max_length=7,
        default='#ffffff',
        help_text='Hex color code for side panel background'
    )
    text_color = models.CharField(
        max_length=7,
        default='#000000',
        help_text='Hex color code for text'
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Form Layout'
        verbose_name_plural = 'Form Layouts'
        ordering = ['page_name']
    
    def __str__(self):
        return f'{self.get_page_name_display()} - {self.get_form_position_display()}'
    
    def get_image_url(self):
        """Return image URL, preferring uploaded file over external URL."""
        if self.side_image:
            return self.side_image.url
        return self.side_image_url


# Sponsor Campaign Models
class SponsorCampaign(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('draft', 'Draft'),
    ]
    
    PACING_CHOICES = [
        ('even', 'Even Distribution'),
        ('asap', 'As Soon As Possible'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sponsor_campaigns')
    name = models.CharField(max_length=200, help_text="Campaign name for internal tracking")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Date range
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    
    # Delivery settings
    priority = models.IntegerField(default=1, validators=[MinValueValidator(1)], 
                                 help_text="Higher numbers get more exposure")
    daily_impression_cap = models.IntegerField(validators=[MinValueValidator(1)], 
                                              help_text="Maximum impressions per day")
    daily_click_cap = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)], 
                                         help_text="Optional daily click limit")
    
    # Targeting (JSON fields)
    targeting_countries = models.JSONField(default=list, blank=True, 
                                          help_text="List of country codes. Empty = all countries")
    targeting_functions = models.JSONField(default=list, blank=True, 
                                          help_text="List of function names. Empty = all functions")  
    targeting_work_env = models.JSONField(default=list, blank=True, 
                                         help_text="List of work environments. Empty = all")
    
    # Advanced settings
    bid_cpm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                 help_text="Cost per thousand impressions (optional)")
    weight = models.IntegerField(default=1, validators=[MinValueValidator(1)], 
                                help_text="Weight for selection algorithm")
    pacing = models.CharField(max_length=10, choices=PACING_CHOICES, default='even')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'start_at', 'end_at']),
            models.Index(fields=['company', 'status']),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.name}"

    def is_active(self, now=None):
        """Check if campaign is currently active"""
        if now is None:
            now = timezone.now()
        return (
            self.status == 'active' and 
            self.start_at <= now <= self.end_at
        )

    def matches_targeting(self, filters):
        """Check if campaign matches current page filters"""
        # Country targeting
        if self.targeting_countries and filters.get('country'):
            if filters['country'] not in self.targeting_countries:
                return False
                
        # Function targeting  
        if self.targeting_functions and filters.get('function'):
            if filters['function'] not in self.targeting_functions:
                return False
                
        # Work environment targeting
        if self.targeting_work_env and filters.get('work_environment'):
            if filters['work_environment'] not in self.targeting_work_env:
                return False
                
        return True

    def impressions_today(self, date=None):
        """Get impression count for today"""
        if date is None:
            date = timezone.now().date()
        stats = self.stats_daily.filter(date=date).first()
        return stats.impressions if stats else 0

    def clicks_today(self, date=None):
        """Get click count for today"""
        if date is None:
            date = timezone.now().date()
        stats = self.stats_daily.filter(date=date).first()
        return stats.clicks if stats else 0

    def under_daily_caps(self, date=None):
        """Check if campaign is under daily impression/click caps"""
        if date is None:
            date = timezone.now().date()
            
        # Check impression cap
        if self.impressions_today(date) >= self.daily_impression_cap:
            return False
            
        # Check click cap (if set)
        if self.daily_click_cap and self.clicks_today(date) >= self.daily_click_cap:
            return False
            
        return True


class SponsorStatsDaily(models.Model):
    """Daily aggregated stats per campaign"""
    campaign = models.ForeignKey(SponsorCampaign, on_delete=models.CASCADE, related_name='stats_daily')
    date = models.DateField()
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['campaign', 'date']
        indexes = [
            models.Index(fields=['campaign', 'date']),
        ]

    def __str__(self):
        return f"{self.campaign} - {self.date} ({self.impressions}i/{self.clicks}c)"


class SponsorDeliveryLog(models.Model):
    """Log of sponsor deliveries to users for anti-fatigue"""
    ACTION_CHOICES = [
        ('impression', 'Impression'),
        ('click', 'Click'),
    ]

    campaign = models.ForeignKey(SponsorCampaign, on_delete=models.CASCADE, related_name='delivery_logs')
    user_hash = models.CharField(max_length=64, db_index=True, 
                                help_text="Anonymized user identifier")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    page_key = models.CharField(max_length=500, 
                               help_text="Page context: browse:page=1:filters=hash")
    
    # Request context
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    referrer = models.URLField(blank=True)
    
    shown_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['campaign', 'user_hash', 'shown_at']),
            models.Index(fields=['user_hash', 'shown_at']),
        ]

    def __str__(self):
        return f"{self.campaign} -> {self.user_hash[:8]} ({self.action})"


class SponsorImpressionEvent(models.Model):
    """Real-time impression events for immediate processing"""
    campaign = models.ForeignKey(SponsorCampaign, on_delete=models.CASCADE, related_name='impression_events')
    user_hash = models.CharField(max_length=64, db_index=True)
    session_id = models.CharField(max_length=100, blank=True)
    page_url = models.URLField()
    
    # Viewport tracking
    is_above_fold = models.BooleanField(default=False)
    viewport_time_ms = models.IntegerField(null=True, blank=True, 
                                          help_text="Time spent in viewport in milliseconds")
    
    # Context
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'processed']),
            models.Index(fields=['campaign', 'user_hash']),
        ]


class HowItWorksSection(models.Model):
    """Homepage 'How It Works' section configuration"""
    
    title = models.CharField(max_length=200, default="Best-performing patterns for tools like yours")
    subtitle = models.CharField(max_length=300, default="After a results preview, the best-performing sections are:")
    section_header = models.CharField(max_length=100, default="Option A — How It Works (compact)")
    description = models.CharField(max_length=200, default="This builds instant understanding + trust.")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1, help_text="Display order on homepage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'How It Works Section'
        verbose_name_plural = 'How It Works Sections'
    
    def __str__(self):
        return f"How It Works - {self.title[:50]}"


class HowItWorksStep(models.Model):
    """Individual steps for the How It Works section"""
    
    section = models.ForeignKey(HowItWorksSection, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    icon = models.CharField(max_length=50, help_text="Emoji or icon character", default="🔍")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['section', 'order', 'step_number']
        verbose_name = 'How It Works Step'
        verbose_name_plural = 'How It Works Steps'
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class RecruiterSection(models.Model):
    """Homepage recruiter section configuration"""
    
    title = models.CharField(max_length=100, default="Are you hiring?")
    description = models.TextField(default="Add your company and get discovered by candidates tracking active hiring signals.")
    button_text = models.CharField(max_length=50, default="Add Company")
    button_link = models.CharField(max_length=100, default="/add-company", help_text="Internal link or external URL")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=2, help_text="Display order on homepage")
    
    # Styling options
    background_color = models.CharField(max_length=7, default="#f8f9fa", help_text="Hex color code")
    text_color = models.CharField(max_length=7, default="#212529", help_text="Hex color code")
    button_color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Recruiter Section'
        verbose_name_plural = 'Recruiter Sections'
    
    def __str__(self):
        return f"Recruiter Section - {self.title}"
