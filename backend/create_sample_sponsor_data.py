#!/usr/bin/env python3
"""
Script to create sample sponsor statistics data for testing
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from companies.models import Company, SponsorStatsDaily, SponsorCampaign

def create_sample_sponsor_data():
    """Create sample sponsor statistics data for testing"""
    
    # Get or create Samsara company (should exist)
    samsara = Company.objects.filter(name='Samsara').first()
    if not samsara:
        print("❌ Samsara company not found")
        return
    
    # Create a sponsor campaign for Samsara
    campaign, created = SponsorCampaign.objects.get_or_create(
        company=samsara,
        name='Q1 2024 Hiring Campaign',
        defaults={
            'start_at': datetime.now() - timedelta(days=30),
            'end_at': datetime.now() + timedelta(days=30),
            'status': 'active',
            'priority': 5,
            'daily_impression_cap': 2000,
            'daily_click_cap': 100,
        }
    )
    
    if created:
        print(f"✅ Created campaign: {campaign.name}")
    else:
        print(f"📋 Campaign already exists: {campaign.name}")
    
    # Generate sample daily stats for the last 30 days
    stats_created = 0
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).date()
        
        # Generate realistic random data
        base_impressions = 1000 + (i * 50)  # Growing impressions
        impressions = base_impressions + (i % 7) * 200  # Weekly variation
        clicks = int(impressions * (0.015 + (i % 10) * 0.002))  # 1.5-3.5% CTR
        
        stat, stat_created = SponsorStatsDaily.objects.get_or_create(
            campaign=campaign,
            date=date,
            defaults={
                'impressions': impressions,
                'clicks': clicks,
            }
        )
        
        if stat_created:
            stats_created += 1
    
    print(f"✅ Created {stats_created} daily statistics records")
    print(f"📊 Total sponsor stats in database: {SponsorStatsDaily.objects.count()}")
    
    # Display summary
    total_stats = SponsorStatsDaily.objects.filter(campaign__company=samsara)
    total_clicks = sum(stat.clicks for stat in total_stats)
    total_impressions = sum(stat.impressions for stat in total_stats)
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    
    print(f"\n📈 Summary for {samsara.name}:")
    print(f"   Total Clicks: {total_clicks:,}")
    print(f"   Total Impressions: {total_impressions:,}")
    print(f"   Average CTR: {avg_ctr:.2f}%")

if __name__ == '__main__':
    print("🚀 Creating sample sponsor statistics data...")
    create_sample_sponsor_data()
    print("✅ Sample data creation complete!")