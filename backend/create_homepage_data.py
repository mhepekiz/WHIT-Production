#!/usr/bin/env python
import os
import sys
import django

# Add the current directory to the path
sys.path.append('/Users/mustafahepekiz/Desktop/whit-release/backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from companies.models import HowItWorksSection, HowItWorksStep, RecruiterSection

def create_homepage_sections():
    # Create How It Works section
    how_it_works = HowItWorksSection.objects.get_or_create(
        title='Best-performing patterns for tools like yours',
        defaults={
            'subtitle': 'After a results preview, the best-performing sections are:',
            'section_header': 'Option A — How It Works (compact)',
            'description': 'This builds instant understanding + trust.',
            'is_active': True,
            'order': 1
        }
    )[0]
    
    # Create steps
    steps = [
        {'step_number': 1, 'icon': '1️⃣', 'title': 'We track companies', 'description': 'Monitor hiring activities across tech companies'},
        {'step_number': 2, 'icon': '2️⃣', 'title': 'We detect hiring signals', 'description': 'Identify active recruitment patterns and job postings'},
        {'step_number': 3, 'icon': '3️⃣', 'title': 'You discover who\'s actively hiring', 'description': 'Get matched with companies that fit your preferences'}
    ]
    
    for step_data in steps:
        step, created = HowItWorksStep.objects.get_or_create(
            section=how_it_works,
            step_number=step_data['step_number'],
            defaults={
                'icon': step_data['icon'],
                'title': step_data['title'],
                'description': step_data['description'],
                'is_active': True,
                'order': step_data['step_number']
            }
        )
        if created:
            print(f"Created step {step_data['step_number']}: {step_data['title']}")
    
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
        print("Created recruiter section")
    
    print('Homepage sections setup completed!')
    
    # Display current data
    print(f"\nHow It Works Sections: {HowItWorksSection.objects.count()}")
    print(f"How It Works Steps: {HowItWorksStep.objects.count()}")
    print(f"Recruiter Sections: {RecruiterSection.objects.count()}")

if __name__ == '__main__':
    create_homepage_sections()