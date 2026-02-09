from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recruiters.models import Recruiter, RecruiterPackage
from companies.models import Company, CompanyRecruiterAccess, CampaignStatistics
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Create test data for company analytics dashboard'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Creating test data...")

        # Create package
        premium_pkg, _ = RecruiterPackage.objects.get_or_create(
            name='Premium Test Package',
            defaults={
                'description': 'Premium package for analytics testing',
                'price': 299.99,
                'monthly_job_openings': 20,
                'analytics_level': 'premium',
                'monthly_candidate_searches': 100,
                'candidate_profile_access': True,
                'messaging_enabled': True,
                'monthly_messages': 50
            }
        )

        # Create test user and recruiter
        user, created = User.objects.get_or_create(
            username='analytics_tester',
            defaults={
                'email': 'analytics@test.com',
                'first_name': 'Analytics',
                'last_name': 'Tester',
                'is_active': True
            }
        )

        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f"✅ Created user: {user.username}")

        recruiter, created = Recruiter.objects.get_or_create(
            user=user,
            defaults={
                'company_name': 'Analytics Testing Agency',
                'phone_number': '+1-555-0123',
                'contact_email': user.email,
                'package': premium_pkg,
                'is_verified': True
            }
        )

        if created:
            self.stdout.write(f"✅ Created recruiter: {recruiter.company_name}")

        # Create token
        token, _ = Token.objects.get_or_create(user=user)
        self.stdout.write(f"🔑 Token: {token.key}")

        # Create test companies
        companies_data = [
            ('Analytics Demo Corp', True),
            ('DataViz Solutions', True), 
            ('MetricFlow Systems', True),
            ('Regular Tech Co', False)
        ]

        companies = []
        for name, is_sponsored in companies_data:
            company, created = Company.objects.get_or_create(
                name=name,
                defaults={
                    'jobs_page_url': f'https://{name.lower().replace(" ", "").replace(",", "")}.com/careers',
                    'country': 'United States',
                    'work_environment': 'Remote',
                    'engineering_positions': True,
                    'status': 'Active',
                    'is_sponsored': is_sponsored
                }
            )
            if created:
                self.stdout.write(f"✅ Company: {name} (Sponsored: {is_sponsored})")
            companies.append(company)

        # Create access relationships
        sponsored_companies = [c for c in companies if c.is_sponsored]
        access_levels = ['view', 'manage', 'analytics', 'full']
        
        for i, company in enumerate(sponsored_companies):
            level = access_levels[i % len(access_levels)]
            
            permissions = {
                'view': {'can_see_sponsored_stats': True, 'can_manage_campaigns': False, 'can_view_analytics': True, 'can_export_data': False},
                'manage': {'can_see_sponsored_stats': True, 'can_manage_campaigns': True, 'can_view_analytics': True, 'can_export_data': True},
                'analytics': {'can_see_sponsored_stats': True, 'can_manage_campaigns': False, 'can_view_analytics': True, 'can_export_data': True},
                'full': {'can_see_sponsored_stats': True, 'can_manage_campaigns': True, 'can_view_analytics': True, 'can_export_data': True}
            }
            
            access, created = CompanyRecruiterAccess.objects.get_or_create(
                company=company,
                recruiter=recruiter,
                defaults={
                    'access_level': level,
                    **permissions[level]
                }
            )
            if created:
                self.stdout.write(f"✅ Access: {company.name} ({level})")

        # Create campaign statistics
        self.stdout.write("📊 Creating campaign statistics...")
        
        for company in sponsored_companies:
            stats_created = 0
            for days_ago in range(30):
                stats_date = date.today() - timedelta(days=days_ago)
                
                # Generate realistic varied data
                base_multiplier = random.uniform(0.8, 1.4)
                day_of_week_factor = 1.2 if stats_date.weekday() < 5 else 0.8
                
                page_views = int(random.randint(120, 250) * base_multiplier * day_of_week_factor)
                unique_visitors = int(page_views * random.uniform(0.75, 0.9))
                job_clicks = int(page_views * random.uniform(0.25, 0.4))
                profile_views = int(page_views * random.uniform(0.35, 0.5))
                app_clicks = int(job_clicks * random.uniform(0.6, 0.85))
                contact_clicks = int(profile_views * random.uniform(0.15, 0.35))
                
                ctr = min(job_clicks / page_views if page_views > 0 else 0, 1.0)
                engagement = min((app_clicks + contact_clicks) / unique_visitors if unique_visitors > 0 else 0, 1.0)
                
                stats, created = CampaignStatistics.objects.get_or_create(
                    company=company,
                    date=stats_date,
                    defaults={
                        'page_views': page_views,
                        'unique_visitors': unique_visitors,
                        'job_page_clicks': job_clicks,
                        'profile_views': profile_views,
                        'application_clicks': app_clicks,
                        'contact_clicks': contact_clicks,
                        'click_through_rate': round(ctr, 4),
                        'engagement_rate': round(engagement, 4)
                    }
                )
                if created:
                    stats_created += 1
            
            self.stdout.write(f"✅ Created {stats_created} stats for {company.name}")

        self.stdout.write("\n" + "="*60)
        self.stdout.write("🎉 TEST DATA CREATION COMPLETE!")
        self.stdout.write("="*60)
        
        self.stdout.write("\n🔑 LOGIN CREDENTIALS:")
        self.stdout.write(f"Username: {user.username}")
        self.stdout.write(f"Email: {user.email}")
        self.stdout.write(f"Password: testpass123")
        self.stdout.write(f"API Token: {token.key}")
        
        self.stdout.write(f"\n📊 SUMMARY:")
        self.stdout.write(f"• 1 test recruiter created")
        self.stdout.write(f"• {len(companies)} companies created ({len(sponsored_companies)} sponsored)")
        self.stdout.write(f"• {len(sponsored_companies)} access relationships created")
        self.stdout.write(f"• {30 * len(sponsored_companies)} campaign statistics created")
        
        self.stdout.write("\n🌐 TESTING INSTRUCTIONS:")
        self.stdout.write("1. Go to: http://localhost:5173/recruiter/login")
        self.stdout.write("2. Login with the credentials above")
        self.stdout.write("3. Navigate to 'Analytics' in the dashboard")
        self.stdout.write("4. Test company selection and statistics viewing")
        self.stdout.write("5. Try the data export functionality")
        
        self.stdout.write("\n🎯 Ready for testing!")