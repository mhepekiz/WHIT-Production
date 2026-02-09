from django.contrib.auth.models import User
from recruiters.models import Recruiter, RecruiterPackage
from companies.models import Company, CompanyRecruiterAccess, CampaignStatistics
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
import random

print("🚀 Creating test data...")

# Create packages
premium_pkg, _ = RecruiterPackage.objects.get_or_create(
    name='Premium Package',
    defaults={
        'price': 299.99,
        'job_postings_limit': 20,
        'featured_listings': 5,
        'analytics_access': True,
        'messaging_enabled': True,
        'priority_support': True
    }
)

# Create test user and recruiter
user, created = User.objects.get_or_create(
    username='test_recruiter',
    defaults={
        'email': 'test@recruiter.com',
        'first_name': 'Test',
        'last_name': 'Recruiter',
        'is_active': True
    }
)

if created:
    user.set_password('testpass123')
    user.save()
    print(f"✅ Created user: {user.username}")

recruiter, created = Recruiter.objects.get_or_create(
    user=user,
    defaults={
        'company_name': 'Test Recruiting Agency',
        'phone': '+1-555-0123',
        'package': premium_pkg,
        'is_verified': True
    }
)

if created:
    print(f"✅ Created recruiter: {recruiter.company_name}")

# Create token
token, _ = Token.objects.get_or_create(user=user)
print(f"🔑 Token: {token.key}")

# Create test companies
companies_data = [
    ('TechFlow Analytics', True),
    ('DataStream Systems', True),
    ('CloudTech Solutions', True),
    ('Regular Company', False)
]

companies = []
for name, is_sponsored in companies_data:
    company, created = Company.objects.get_or_create(
        name=name,
        defaults={
            'website': f'https://{name.lower().replace(" ", "")}.com',
            'description': f'{name} - Technology company',
            'is_sponsored': is_sponsored,
            'is_hiring': True
        }
    )
    if created:
        print(f"✅ Company: {name} (Sponsored: {is_sponsored})")
    companies.append(company)

# Create access relationships for sponsored companies only
sponsored_companies = [c for c in companies if c.is_sponsored]
for i, company in enumerate(sponsored_companies):
    access_levels = ['view', 'manage', 'analytics', 'full']
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
        print(f"✅ Access: {company.name} ({level})")

# Create statistics for last 30 days
print("📊 Creating campaign statistics...")
for company in sponsored_companies:
    for days_ago in range(30):
        stats_date = date.today() - timedelta(days=days_ago)
        
        # Generate realistic data
        base_views = random.randint(100, 300)
        page_views = base_views + random.randint(-20, 50)
        unique_visitors = int(page_views * random.uniform(0.7, 0.9))
        job_clicks = int(page_views * random.uniform(0.2, 0.4))
        profile_views = int(page_views * random.uniform(0.3, 0.5))
        app_clicks = int(job_clicks * random.uniform(0.5, 0.8))
        contact_clicks = int(profile_views * random.uniform(0.1, 0.3))
        
        ctr = min(job_clicks / page_views if page_views > 0 else 0, 1.0)
        engagement = min((app_clicks + contact_clicks) / unique_visitors if unique_visitors > 0 else 0, 1.0)
        
        CampaignStatistics.objects.get_or_create(
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
    print(f"✅ Stats for {company.name}")

print("\n🎉 Test data created successfully!")
print("\n🔑 LOGIN INFO:")
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Password: testpass123")
print(f"Token: {token.key}")
print(f"\n📊 Created data for {len(sponsored_companies)} sponsored companies")
print("Ready to test the Analytics dashboard!")