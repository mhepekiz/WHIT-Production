#!/usr/bin/env python
"""
Debug script to test homepage sections API locally and create sample data.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from companies.models import HowItWorksSection, HowItWorksStep, RecruiterSection
from companies.serializers import HowItWorksSectionSerializer, RecruiterSectionSerializer

def test_homepage_sections():
    print("=== Homepage Sections Debug ===")
    
    # Check if data exists
    how_it_works_count = HowItWorksSection.objects.count()
    recruiter_count = RecruiterSection.objects.count()
    
    print(f"HowItWorksSection count: {how_it_works_count}")
    print(f"RecruiterSection count: {recruiter_count}")
    
    if how_it_works_count == 0:
        print("Creating sample How It Works data...")
        # Create sample data similar to management command
        hiw_section = HowItWorksSection.objects.create(
            title="Best-performing patterns for tools like yours",
            is_active=True,
            order=1
        )
        
        steps_data = [
            {"title": "Browse Companies", "description": "Explore verified hiring companies", "icon": "🏢", "order": 1},
            {"title": "Filter & Search", "description": "Find opportunities that match your skills", "icon": "🔍", "order": 2},
            {"title": "Apply Directly", "description": "Connect with companies directly through their job pages", "icon": "📧", "order": 3}
        ]
        
        for step_data in steps_data:
            HowItWorksStep.objects.create(
                section=hiw_section,
                **step_data
            )
    
    if recruiter_count == 0:
        print("Creating sample Recruiter section data...")
        RecruiterSection.objects.create(
            title="Are you hiring?",
            subtitle="Showcase your company to thousands of qualified tech professionals",
            description="Join our platform to connect with talented engineers, designers, and other tech professionals actively looking for opportunities.",
            cta_text="Get Started",
            cta_url="mailto:partnerships@whoishiringintech.com?subject=Partnership Inquiry",
            background_color="#f8f9fa",
            text_color="#2c3e50",
            is_active=True,
            order=1
        )
    
    # Test API serialization
    print("\n=== Testing API Response ===")
    how_it_works_sections = HowItWorksSection.objects.filter(is_active=True).order_by('order')
    recruiter_sections = RecruiterSection.objects.filter(is_active=True).order_by('order')
    
    how_it_works_data = HowItWorksSectionSerializer(how_it_works_sections, many=True).data
    recruiter_data = RecruiterSectionSerializer(recruiter_sections, many=True).data
    
    response_data = {
        'how_it_works_sections': how_it_works_data,
        'recruiter_sections': recruiter_data
    }
    
    print("API Response:")
    import json
    print(json.dumps(response_data, indent=2))
    print("=== Debug Complete ===")

if __name__ == '__main__':
    test_homepage_sections()