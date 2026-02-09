#!/usr/bin/env python3
"""
Create sample sponsor stats data for dashboard demonstration
"""
import os
import sys
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from companies.models import SponsorCampaign, SponsorStatsDaily

def create_sample_stats():
    """Create sample statistics for the past week"""
    campaigns = SponsorCampaign.objects.all()
    
    if not campaigns.exists():
        print("No campaigns found. Please create some campaigns first.")
        return
    
    print(f"Creating sample stats for {campaigns.count()} campaigns...")
    
    # Create stats for the past 7 days
    for i in range(7):
        stats_date = date.today() - timedelta(days=i)
        
        for campaign in campaigns:
            # Generate realistic sample data
            base_impressions = 100 + (i * 20)
            impressions = base_impressions + (hash(campaign.name) % 50)
            clicks = int(impressions * 0.03) + (i % 3)  # ~3% CTR with variation
            
            # Create or update daily stats
            stats, created = SponsorStatsDaily.objects.get_or_create(
                campaign=campaign,
                date=stats_date,
                defaults={
                    'impressions': impressions,
                    'clicks': clicks
                }
            )
            
            if created:
                print(f"  Created stats for {campaign.name} on {stats_date}: {impressions} impressions, {clicks} clicks")
            else:
                print(f"  Stats already exist for {campaign.name} on {stats_date}")

if __name__ == '__main__':
    create_sample_stats()
    
    # Show summary
    total_stats = SponsorStatsDaily.objects.count()
    print(f"\nTotal stats records: {total_stats}")
    
    # Show today's stats
    today_stats = SponsorStatsDaily.objects.filter(date=date.today())
    if today_stats.exists():
        print(f"Today's stats: {today_stats.count()} campaigns")
        for stat in today_stats:
            ctr = (stat.clicks / stat.impressions * 100) if stat.impressions > 0 else 0
            print(f"  {stat.campaign.name}: {stat.impressions} impressions, {stat.clicks} clicks, {ctr:.2f}% CTR")
    else:
        print("No stats for today yet.")