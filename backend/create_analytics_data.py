#!/usr/bin/env python3

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from companies.models import Company, CampaignStatistics
from datetime import date, timedelta
import random

def create_sample_analytics():
    """Create sample analytics data for Samsara"""
    
    # Get Samsara company
    try:
        samsara = Company.objects.get(name='Samsara')
        print(f"✅ Found company: {samsara.name}")
    except Company.DoesNotExist:
        print("❌ Samsara company not found")
        return

    # Create analytics data for the last 30 days
    for i in range(30):
        analytics_date = date.today() - timedelta(days=i)
        
        # Create or update analytics data
        analytics, created = CampaignStatistics.objects.get_or_create(
            company=samsara,
            date=analytics_date,
            defaults={
                'page_views': random.randint(150, 400),
                'unique_visitors': random.randint(100, 300),
                'job_page_clicks': random.randint(50, 150),
                'profile_views': random.randint(30, 100),
                'application_clicks': random.randint(10, 50),
                'contact_clicks': random.randint(5, 25),
                'click_through_rate': round(random.uniform(2.0, 8.5), 2),
                'engagement_rate': round(random.uniform(15.0, 35.0), 2)
            }
        )
        
        if created:
            print(f"📊 Created analytics for {analytics_date}: {analytics.page_views} page views")
        else:
            print(f"📋 Analytics already exist for {analytics_date}")

    print(f"✅ Sample analytics data created for {samsara.name}")

if __name__ == '__main__':
    create_sample_analytics()