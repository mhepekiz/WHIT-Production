#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from django.contrib.auth.models import User
from recruiters.models import Recruiter, RecruiterPackage
from companies.models import Company, CompanyRecruiterAccess, CampaignStatistics
from rest_framework.authtoken.models import Token

def create_comprehensive_test_data():
    print("🚀 Creating comprehensive test data for CompanyAnalyticsDashboard...")
    
    # Create recruiter packages first
    package_data = [
        {
            'name': 'Basic Package',
            'price': 99.99,
            'job_postings_limit': 5,
            'featured_listings': 1,
            'analytics_access': True,
            'messaging_enabled': False,
            'priority_support': False
        },
        {
            'name': 'Premium Package', 
            'price': 299.99,
            'job_postings_limit': 20,
            'featured_listings': 5,
            'analytics_access': True,
            'messaging_enabled': True,
            'priority_support': True
        }
    ]
    
    for pkg_data in package_data:
        package, created = RecruiterPackage.objects.get_or_create(
            name=pkg_data['name'],
            defaults=pkg_data
        )
        if created:
            print(f"✅ Created package: {package.name}")
    
    # Create test users and recruiters
    recruiter_data = [
        {
            'username': 'recruiter_sarah',
            'email': 'sarah@techrecruiter.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'company_name': 'TechTalent Solutions',
            'phone': '+1-555-0101'
        },
        {
            'username': 'recruiter_mike', 
            'email': 'mike@hiringpro.com',
            'first_name': 'Mike',
            'last_name': 'Chen',
            'company_name': 'HiringPro Inc',
            'phone': '+1-555-0102'
        },
        {
            'username': 'recruiter_ana',
            'email': 'ana@toptalent.com', 
            'first_name': 'Ana',
            'last_name': 'Rodriguez',
            'company_name': 'TopTalent Agency',
            'phone': '+1-555-0103'
        }
    ]
    
    recruiters = []
    premium_package = RecruiterPackage.objects.get(name='Premium Package')
    basic_package = RecruiterPackage.objects.get(name='Basic Package')
    
    for i, rec_data in enumerate(recruiter_data):
        user, created = User.objects.get_or_create(
            username=rec_data['username'],
            defaults={
                'email': rec_data['email'],
                'first_name': rec_data['first_name'], 
                'last_name': rec_data['last_name'],
                'is_active': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"✅ Created user: {user.username}")
        
        # Create or update recruiter
        recruiter, created = Recruiter.objects.get_or_create(
            user=user,
            defaults={
                'company_name': rec_data['company_name'],
                'phone': rec_data['phone'],
                'package': premium_package if i == 0 else basic_package,
                'is_verified': True
            }
        )
        if created:
            print(f"✅ Created recruiter: {recruiter.company_name}")
        
        # Create auth token
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"🔑 Created token for {user.username}: {token.key}")
        
        recruiters.append(recruiter)
    
    # Create test companies with sponsored status
    company_data = [
        {
            'name': 'DataFlow Systems',
            'website': 'https://dataflow-systems.com',
            'description': 'Leading data analytics and machine learning platform',
            'is_sponsored': True,
            'is_hiring': True
        },
        {
            'name': 'CloudNative Technologies', 
            'website': 'https://cloudnative-tech.com',
            'description': 'Kubernetes and cloud infrastructure specialists',
            'is_sponsored': True,
            'is_hiring': True
        },
        {
            'name': 'AI Innovations Lab',
            'website': 'https://ai-innovations.com', 
            'description': 'Cutting-edge artificial intelligence research and development',
            'is_sponsored': True,
            'is_hiring': True
        },
        {
            'name': 'CyberSecure Solutions',
            'website': 'https://cybersecure.com',
            'description': 'Enterprise cybersecurity and threat detection',
            'is_sponsored': True, 
            'is_hiring': True
        },
        {
            'name': 'FinTech Revolution',
            'website': 'https://fintech-revolution.com',
            'description': 'Digital banking and financial technology solutions',
            'is_sponsored': True,
            'is_hiring': True
        },
        {
            'name': 'Regular Tech Corp',
            'website': 'https://regulartech.com', 
            'description': 'Standard technology company (not sponsored)',
            'is_sponsored': False,
            'is_hiring': True
        }
    ]
    
    companies = []
    for comp_data in company_data:
        company, created = Company.objects.get_or_create(
            name=comp_data['name'],
            defaults=comp_data
        )
        if created:
            print(f"✅ Created company: {company.name} (Sponsored: {company.is_sponsored})")
        companies.append(company)
    
    # Create recruiter-company access relationships
    access_relationships = [
        # Sarah (premium recruiter) gets access to multiple companies
        (recruiters[0], companies[0], 'full'),      # DataFlow - full access
        (recruiters[0], companies[1], 'analytics'), # CloudNative - analytics only
        (recruiters[0], companies[2], 'manage'),    # AI Innovations - manage campaigns
        
        # Mike gets access to different companies
        (recruiters[1], companies[2], 'view'),      # AI Innovations - view only
        (recruiters[1], companies[3], 'full'),      # CyberSecure - full access
        
        # Ana gets access to FinTech
        (recruiters[2], companies[4], 'analytics'), # FinTech - analytics access
    ]
    
    access_permissions = {
        'view': {'can_see_sponsored_stats': True, 'can_manage_campaigns': False, 'can_view_analytics': True, 'can_export_data': False},
        'manage': {'can_see_sponsored_stats': True, 'can_manage_campaigns': True, 'can_view_analytics': True, 'can_export_data': True},
        'analytics': {'can_see_sponsored_stats': True, 'can_manage_campaigns': False, 'can_view_analytics': True, 'can_export_data': True},
        'full': {'can_see_sponsored_stats': True, 'can_manage_campaigns': True, 'can_view_analytics': True, 'can_export_data': True}
    }
    
    for recruiter, company, access_level in access_relationships:
        # Only create relationships for sponsored companies
        if company.is_sponsored:
            access, created = CompanyRecruiterAccess.objects.get_or_create(
                company=company,
                recruiter=recruiter,
                defaults={
                    'access_level': access_level,
                    **access_permissions[access_level]
                }
            )
            if created:
                print(f"✅ Created access: {recruiter.company_name} → {company.name} ({access_level})")
    
    # Create campaign statistics for sponsored companies
    print("\n📊 Creating campaign statistics...")
    sponsored_companies = [c for c in companies if c.is_sponsored]
    
    for company in sponsored_companies:
        print(f"Creating stats for {company.name}...")
        
        for days_ago in range(45):  # 45 days of data
            stats_date = date.today() - timedelta(days=days_ago)
            
            # Create realistic but varied statistics
            base_views = random.randint(80, 200)
            base_visitors = int(base_views * random.uniform(0.7, 0.9))
            
            # Add some weekly patterns (higher on weekdays)
            weekday_multiplier = 1.3 if stats_date.weekday() < 5 else 0.7
            base_views = int(base_views * weekday_multiplier)
            base_visitors = int(base_visitors * weekday_multiplier)
            
            # Add some randomness and trends
            trend_factor = 1 + (days_ago * 0.002)  # Slight upward trend over time
            noise_factor = random.uniform(0.8, 1.2)
            
            page_views = max(int(base_views * trend_factor * noise_factor), 10)
            unique_visitors = max(int(base_visitors * trend_factor * noise_factor), 8)
            
            job_page_clicks = max(int(page_views * random.uniform(0.15, 0.35)), 1)
            profile_views = max(int(page_views * random.uniform(0.25, 0.45)), 2)
            application_clicks = max(int(job_page_clicks * random.uniform(0.4, 0.8)), 1)
            contact_clicks = max(int(profile_views * random.uniform(0.1, 0.3)), 0)
            
            click_through_rate = min(job_page_clicks / page_views if page_views > 0 else 0, 1.0)
            engagement_rate = min((application_clicks + contact_clicks) / unique_visitors if unique_visitors > 0 else 0, 1.0)
            
            stats, created = CampaignStatistics.objects.get_or_create(
                company=company,
                date=stats_date,
                defaults={
                    'page_views': page_views,
                    'unique_visitors': unique_visitors,
                    'job_page_clicks': job_page_clicks,
                    'profile_views': profile_views,
                    'application_clicks': application_clicks,
                    'contact_clicks': contact_clicks,
                    'click_through_rate': round(click_through_rate, 4),
                    'engagement_rate': round(engagement_rate, 4)
                }
            )
            
            if created and days_ago % 10 == 0:  # Print every 10th day to avoid spam
                print(f"  📅 {stats_date}: {page_views} views, {unique_visitors} visitors")
    
    print(f"\n✅ Created 45 days of statistics for {len(sponsored_companies)} sponsored companies")
    
    # Print summary and login instructions
    print("\n" + "="*60)
    print("🎉 TEST DATA CREATION COMPLETE!")
    print("="*60)
    
    print("\n📊 SUMMARY:")
    print(f"• {len(recruiters)} recruiters created")
    print(f"• {len(companies)} companies created ({len(sponsored_companies)} sponsored)")
    print(f"• {len(access_relationships)} access relationships created")
    print(f"• {45 * len(sponsored_companies)} campaign statistics created")
    
    print("\n🔑 LOGIN CREDENTIALS:")
    for i, recruiter in enumerate(recruiters):
        token = Token.objects.get(user=recruiter.user)
        accessible_companies = CompanyRecruiterAccess.objects.filter(recruiter=recruiter).count()
        print(f"\n{i+1}. {recruiter.company_name}")
        print(f"   Username: {recruiter.user.username}")
        print(f"   Email: {recruiter.user.email}")
        print(f"   Password: testpass123")
        print(f"   API Token: {token.key}")
        print(f"   Accessible Companies: {accessible_companies}")
    
    print("\n🌐 TESTING INSTRUCTIONS:")
    print("1. Start the backend server: cd backend && python manage.py runserver")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Go to: http://localhost:5173/recruiter/login")
    print("4. Login with any of the credentials above")
    print("5. Navigate to 'Analytics' in the dashboard")
    print("6. Test the company selection and statistics viewing")
    print("7. Try the data export functionality")
    
    print("\n📈 API TESTING:")
    print("Test API endpoints with:")
    for recruiter in recruiters[:1]:  # Just show one example
        token = Token.objects.get(user=recruiter.user)
        print(f"curl -H 'Authorization: Token {token.key}' http://localhost:8000/api/recruiters/dashboard/accessible_companies/")
        break
    
    print("\n🎯 Ready for comprehensive testing!")

if __name__ == "__main__":
    create_comprehensive_test_data()