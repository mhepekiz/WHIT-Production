#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from companies.models import Company, CompanyRecruiterAccess, CampaignStatistics
from recruiters.models import Recruiter

def create_test_data():
    print("Creating test data for CompanyAnalyticsDashboard...")
    
    # Get or create a test company
    company, created = Company.objects.get_or_create(
        name="Test Tech Company", 
        defaults={
            'website': 'https://test-tech.com',
            'description': 'A test technology company for analytics testing',
            'is_sponsored': True
        }
    )
    print(f"Company: {company.name} ({'created' if created else 'exists'})")
    
    # Get or create another test company
    company2, created2 = Company.objects.get_or_create(
        name="Analytics Demo Corp", 
        defaults={
            'website': 'https://analytics-demo.com',
            'description': 'Another test company for analytics',
            'is_sponsored': True
        }
    )
    print(f"Company: {company2.name} ({'created' if created2 else 'exists'})")
    
    # Get first recruiter
    recruiter = Recruiter.objects.first()
    if not recruiter:
        print("No recruiters found. Please create a recruiter account first.")
        return
        
    print(f"Using recruiter: {recruiter.user.username}")
    
    # Create access relationships
    access1, created = CompanyRecruiterAccess.objects.get_or_create(
        company=company,
        recruiter=recruiter,
        defaults={
            'access_level': 'full',
            'can_see_sponsored_stats': True,
            'can_manage_campaigns': True,
            'can_view_analytics': True,
            'can_export_data': True
        }
    )
    print(f"Access to {company.name}: {access1.access_level}")
    
    access2, created = CompanyRecruiterAccess.objects.get_or_create(
        company=company2,
        recruiter=recruiter,
        defaults={
            'access_level': 'analytics',
            'can_see_sponsored_stats': True,
            'can_manage_campaigns': False,
            'can_view_analytics': True,
            'can_export_data': True
        }
    )
    print(f"Access to {company2.name}: {access2.access_level}")
    
    # Create test statistics for the last 30 days
    print("Creating campaign statistics...")
    for i in range(30):
        stats_date = date.today() - timedelta(days=i)
        
        # Statistics for company 1
        stats1, created = CampaignStatistics.objects.get_or_create(
            company=company,
            date=stats_date,
            defaults={
                'page_views': 120 + (i * 5) + (i % 7) * 20,
                'unique_visitors': 95 + (i * 4) + (i % 5) * 15,
                'job_page_clicks': 30 + (i * 2) + (i % 3) * 8,
                'profile_views': 55 + (i * 3) + (i % 4) * 12,
                'application_clicks': 20 + i + (i % 6) * 5,
                'contact_clicks': 12 + (i // 2) + (i % 2) * 3,
                'click_through_rate': 0.25 + (i * 0.01) + (i % 10) * 0.005,
                'engagement_rate': 0.40 + (i * 0.008) + (i % 8) * 0.01
            }
        )
        
        # Statistics for company 2 
        stats2, created = CampaignStatistics.objects.get_or_create(
            company=company2,
            date=stats_date,
            defaults={
                'page_views': 85 + (i * 3) + (i % 5) * 15,
                'unique_visitors': 70 + (i * 2) + (i % 7) * 10,
                'job_page_clicks': 20 + i + (i % 4) * 6,
                'profile_views': 35 + (i * 2) + (i % 6) * 8,
                'application_clicks': 15 + (i // 2) + (i % 5) * 3,
                'contact_clicks': 8 + (i // 3) + (i % 3) * 2,
                'click_through_rate': 0.23 + (i * 0.008) + (i % 12) * 0.003,
                'engagement_rate': 0.35 + (i * 0.006) + (i % 9) * 0.008
            }
        )
    
    print(f"Created 30 days of statistics for both companies")
    print("\nTest data creation completed!")
    print("\nYou can now:")
    print("1. Login as a recruiter at http://localhost:5174/recruiter/login")
    print("2. Navigate to Analytics in the dashboard")
    print("3. View company analytics and statistics")

if __name__ == "__main__":
    create_test_data()