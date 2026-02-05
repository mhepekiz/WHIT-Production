from django.core.management.base import BaseCommand
from companies.models import HowItWorksSection, HowItWorksStep, RecruiterSection

class Command(BaseCommand):
    help = 'Force create homepage sections data for production'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creating homepage sections data...'))
        
        # Clean existing data first
        HowItWorksSection.objects.all().delete()
        RecruiterSection.objects.all().delete()
        
        # Create How It Works section
        hiw_section = HowItWorksSection.objects.create(
            title="Best-performing patterns for tools like yours",
            subtitle="After a results preview, the best-performing sections are:",
            section_header="Option A — How It Works (compact)",
            description="This builds instant understanding + trust.",
            is_active=True,
            order=1
        )
        
        # Create steps
        steps_data = [
            {
                "step_number": 1,
                "icon": "1️⃣",
                "title": "We track companies",
                "description": "Monitor hiring activities across tech companies",
                "is_active": True,
                "order": 1
            },
            {
                "step_number": 2,
                "icon": "2️⃣",
                "title": "We detect hiring signals", 
                "description": "Identify active recruitment patterns and job postings",
                "is_active": True,
                "order": 2
            },
            {
                "step_number": 3,
                "icon": "3️⃣",
                "title": "You discover who's actively hiring",
                "description": "Get matched with companies that fit your preferences",
                "is_active": True,
                "order": 3
            }
        ]
        
        for step_data in steps_data:
            HowItWorksStep.objects.create(
                section=hiw_section,
                **step_data
            )
        
        # Create Recruiter section
        RecruiterSection.objects.create(
            title="Are you hiring?",
            description="Add your company and get discovered by candidates tracking active hiring signals.",
            button_text="Add Company",
            button_link="/add-company",
            is_active=True,
            order=2,
            background_color="#f8f9fa",
            text_color="#212529",
            button_color="#007bff"
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {HowItWorksSection.objects.count()} How It Works sections '
                f'and {RecruiterSection.objects.count()} Recruiter sections'
            )
        )
        
        # Verify data was created
        hiw_count = HowItWorksSection.objects.count()
        recruiter_count = RecruiterSection.objects.count()
        steps_count = HowItWorksStep.objects.count()
        
        self.stdout.write(f'Final counts: HowItWorks: {hiw_count}, Recruiters: {recruiter_count}, Steps: {steps_count}')