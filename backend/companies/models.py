from django.db import models


class Company(models.Model):
    """Model representing a company that is hiring."""
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255, unique=True)
    logo = models.URLField(max_length=500, blank=True, null=True)
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
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country', 'state', 'city']),
            models.Index(fields=['status']),
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
        help_text='Upload banner image'
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
