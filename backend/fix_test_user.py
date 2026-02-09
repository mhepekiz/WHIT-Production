#!/usr/bin/env python3
"""
Fix test user script for recruiter login
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/mustafahepekiz/Desktop/whit-release/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from django.contrib.auth.models import User
from recruiters.models import Recruiter, RecruiterPackage

def create_test_user():
    """Create or fix the test user for login"""
    
    # Get or create a basic package
    package, _ = RecruiterPackage.objects.get_or_create(
        name='Basic Test Package',
        defaults={
            'description': 'Test package for development',
            'price': 0.00,
            'monthly_job_openings': 10,
            'analytics_level': 'basic',
            'monthly_candidate_searches': 50,
            'candidate_profile_access': True,
            'messaging_enabled': True,
            'monthly_messages': 100
        }
    )
    
    # Check if user exists
    try:
        user = User.objects.get(email='analytics@test.com')
        print(f'✅ Found existing user: {user.username} ({user.email})')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='analytics_tester',
            email='analytics@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Recruiter',
            is_active=True
        )
        print(f'✅ Created new user: {user.username} ({user.email})')
    
    # Ensure password is correct
    if not user.check_password('testpass123'):
        user.set_password('testpass123')
        user.save()
        print('✅ Password reset to testpass123')
    
    # Check if recruiter profile exists
    try:
        recruiter = user.recruiter_profile
        print(f'✅ Found existing recruiter profile: {recruiter.company_name}')
    except Recruiter.DoesNotExist:
        recruiter = Recruiter.objects.create(
            user=user,
            package=package,
            company_name='Analytics Test Company',
            contact_email='analytics@test.com',
            phone_number='555-0123',
            is_verified=True,
            is_active=True
        )
        print(f'✅ Created recruiter profile: {recruiter.company_name}')
    
    # Test authentication
    from django.contrib.auth import authenticate
    test_user = authenticate(username='analytics@test.com', password='testpass123')
    if test_user:
        print('✅ Authentication test passed')
        print(f'   - User ID: {test_user.id}')
        print(f'   - Has recruiter_profile: {hasattr(test_user, "recruiter_profile")}')
        if hasattr(test_user, 'recruiter_profile'):
            print(f'   - Company: {test_user.recruiter_profile.company_name}')
            print(f'   - Is active: {test_user.recruiter_profile.is_active}')
    else:
        print('❌ Authentication test failed')
    
    return user, recruiter

if __name__ == '__main__':
    user, recruiter = create_test_user()
    print('\n🎉 Test user is ready for login!')
    print(f'Login URL: http://localhost:5175/recruiter/login')
    print(f'Email: analytics@test.com')
    print(f'Password: testpass123')