from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recruiters.models import Recruiter, RecruiterPackage


class Command(BaseCommand):
    help = 'Create test user for recruiter login'

    def handle(self, *args, **options):
        # Get or create basic package
        package, created = RecruiterPackage.objects.get_or_create(
            name='Test Package',
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

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user: {user.email}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created recruiter: {recruiter.company_name}')
        )

        # Test authentication
        from django.contrib.auth import authenticate
        test_user = authenticate(username='analytics@test.com', password='testpass123')
        if test_user and hasattr(test_user, 'recruiter_profile'):
            self.stdout.write(self.style.SUCCESS('Authentication test PASSED'))
        else:
            self.stdout.write(self.style.ERROR('Authentication test FAILED'))