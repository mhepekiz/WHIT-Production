from django.core.management.base import BaseCommand
from companies.models import HowItWorksSection, HowItWorksStep, RecruiterSection


class Command(BaseCommand):
    help = 'Set up default homepage sections'

    def handle(self, *args, **options):
        self.stdout.write('Setting up default homepage sections...')
        
        # Create How It Works section
        how_it_works, created = HowItWorksSection.objects.get_or_create(
            title='Best-performing patterns for tools like yours',
            defaults={
                'subtitle': 'After a results preview, the best-performing sections are:',
                'section_header': 'Option A — How It Works (compact)',
                'description': 'This builds instant understanding + trust.',
                'is_active': True,
                'order': 1
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created How It Works section'))
            
            # Create steps
            steps_data = [
                {'step_number': 1, 'icon': '1️⃣', 'title': 'We track companies', 'description': 'Monitor hiring activities across tech companies'},
                {'step_number': 2, 'icon': '2️⃣', 'title': 'We detect hiring signals', 'description': 'Identify active recruitment patterns and job postings'},
                {'step_number': 3, 'icon': '3️⃣', 'title': 'You discover who\'s actively hiring', 'description': 'Get matched with companies that fit your preferences'}
            ]
            
            for step_data in steps_data:
                HowItWorksStep.objects.create(
                    section=how_it_works,
                    step_number=step_data['step_number'],
                    icon=step_data['icon'],
                    title=step_data['title'],
                    description=step_data['description'],
                    is_active=True,
                    order=step_data['step_number']
                )
                self.stdout.write(f'Created step: {step_data["title"]}')
        else:
            self.stdout.write('How It Works section already exists')
        
        # Create Recruiter section
        recruiter_section, created = RecruiterSection.objects.get_or_create(
            title='Are you hiring?',
            defaults={
                'description': 'Add your company and get discovered by candidates tracking active hiring signals.',
                'button_text': 'Add Company',
                'button_link': '/add-company',
                'is_active': True,
                'order': 2,
                'background_color': '#f8f9fa',
                'text_color': '#212529',
                'button_color': '#007bff'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created Recruiter section'))
        else:
            self.stdout.write('Recruiter section already exists')
        
        self.stdout.write(self.style.SUCCESS('Homepage sections setup complete!'))
        
        # Display current status
        how_it_works_count = HowItWorksSection.objects.filter(is_active=True).count()
        steps_count = HowItWorksStep.objects.filter(is_active=True).count()
        recruiter_count = RecruiterSection.objects.filter(is_active=True).count()
        
        self.stdout.write(f'Active How It Works sections: {how_it_works_count}')
        self.stdout.write(f'Active How It Works steps: {steps_count}')
        self.stdout.write(f'Active Recruiter sections: {recruiter_count}')