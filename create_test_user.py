#!/usr/bin/env python3
"""
Quick test user creation
"""
import os, sys, django

# Set up Django
sys.path.insert(0, '/Users/mustafahepekiz/Desktop/whit-release/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from django.contrib.auth.models import User
from recruiters.models import Recruiter, RecruiterPackage

# Create basic package if it doesn't exist
package, created = RecruiterPackage.objects.get_or_create(
    name='Test Package',
    defaults={
        'description': 'Test package',
        'price': 0,
        'monthly_job_openings': 10,
        'analytics_level': 'basic',
        'monthly_candidate_searches': 50,
        'candidate_profile_access': True,
        'messaging_enabled': True,
        'monthly_messages': 100
    }
)

# Delete existing user if exists
User.objects.filter(email='analytics@test.com').delete()

# Create fresh user
user = User.objects.create_user(
    username='analytics_tester',
    email='analytics@test.com',
    password='testpass123',
    first_name='Analytics',
    last_name='Tester',
    is_active=True
)

# Create recruiter profile
recruiter = Recruiter.objects.create(
    user=user,
    package=package,
    company_name='Test Analytics Company',
    contact_email='analytics@test.com',
    phone_number='555-0123',
    is_verified=True,
    is_active=True
)

print(f"✅ Created user: {user.email}")
print(f"✅ Created recruiter: {recruiter.company_name}")

# Test authentication
from django.contrib.auth import authenticate
test_user = authenticate(username='analytics@test.com', password='testpass123')
if test_user and hasattr(test_user, 'recruiter_profile'):
    print("✅ Authentication test PASSED")
else:
    print("❌ Authentication test FAILED")