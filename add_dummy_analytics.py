#!/usr/bin/env python3
"""
Django management script to add comprehensive dummy analytics data 
directly to the CampaignStatistics model for Sourthings LLC
"""

import os
import sys
import django
from datetime import date, timedelta
import random

# Add the backend directory to Python path
sys.path.append('/Users/mustafahepekiz/Desktop/whit-release/backend')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from companies.models import Company, CampaignStatistics

def add_dummy_analytics_for_sourthings():
    """Add comprehensive dummy analytics data for Sourthings LLC"""
    
    print("🎯 SOURTHINGS LLC - DUMMY ANALYTICS DATA GENERATOR")
    print("🚀 Eliminating ALL zeros from the dashboard!")
    print("=" * 60)
    
    # Get Sourthings LLC
    try:
        sourthings = Company.objects.get(name="Sourthings LLC")
        print(f"✅ Found company: {sourthings.name} (ID: {sourthings.id})")
    except Company.DoesNotExist:
        print("❌ Sourthings LLC not found in database")
        return
    
    # Generate analytics for last 30 days
    total_records_created = 0
    total_records_updated = 0
    
    print(f"\n📊 Generating analytics data for last 30 days...")
    
    for i in range(30):
        analytics_date = date.today() - timedelta(days=i)
        
        # Generate realistic dummy data
        page_views = random.randint(20, 80)  # Reasonable daily page views
        unique_visitors = random.randint(15, int(page_views * 0.8))  # 60-80% of page views
        job_page_clicks = random.randint(8, int(page_views * 0.6))  # 20-60% of page views
        profile_views = random.randint(5, int(page_views * 0.4))  # 10-40% of page views
        application_clicks = random.randint(3, int(job_page_clicks * 0.8))  # 40-80% of job clicks
        contact_clicks = random.randint(1, int(profile_views * 0.5))  # 10-50% of profile views
        
        # Calculate performance metrics
        click_through_rate = round((job_page_clicks / page_views) * 100, 2) if page_views > 0 else 0
        engagement_rate = round(((application_clicks + contact_clicks) / unique_visitors) * 100, 2) if unique_visitors > 0 else 0
        
        # Create or update the record
        stats, created = CampaignStatistics.objects.get_or_create(
            company=sourthings,
            date=analytics_date,
            defaults={
                'page_views': page_views,
                'unique_visitors': unique_visitors,
                'job_page_clicks': job_page_clicks,
                'profile_views': profile_views,
                'application_clicks': application_clicks,
                'contact_clicks': contact_clicks,
                'click_through_rate': click_through_rate,
                'engagement_rate': engagement_rate,
            }
        )
        
        if created:
            total_records_created += 1
            print(f"  📅 {analytics_date}: Created stats (PV:{page_views}, UV:{unique_visitors}, JC:{job_page_clicks}, PrV:{profile_views}, AC:{application_clicks}, CC:{contact_clicks})")
        else:
            # Update existing record if it has zeros
            update_needed = False
            
            if stats.unique_visitors == 0:
                stats.unique_visitors = unique_visitors
                update_needed = True
            
            if stats.profile_views == 0:
                stats.profile_views = profile_views
                update_needed = True
                
            if stats.application_clicks == 0:
                stats.application_clicks = application_clicks
                update_needed = True
                
            if stats.contact_clicks == 0:
                stats.contact_clicks = contact_clicks
                update_needed = True
                
            if stats.click_through_rate == 0:
                stats.click_through_rate = click_through_rate
                update_needed = True
                
            if stats.engagement_rate == 0:
                stats.engagement_rate = engagement_rate
                update_needed = True
            
            if update_needed:
                stats.save()
                total_records_updated += 1
                print(f"  📅 {analytics_date}: Updated stats (UV:{stats.unique_visitors}, PrV:{stats.profile_views}, AC:{stats.application_clicks}, CC:{stats.contact_clicks})")
            else:
                print(f"  📅 {analytics_date}: No update needed")
    
    print(f"\n🎉 ANALYTICS DATA GENERATION COMPLETE!")
    print(f"📈 Records created: {total_records_created}")
    print(f"🔄 Records updated: {total_records_updated}")
    
    # Show summary of current data
    print(f"\n📊 CURRENT SOURTHINGS LLC ANALYTICS SUMMARY:")
    recent_stats = CampaignStatistics.objects.filter(company=sourthings).order_by('-date')[:7]
    
    total_page_views = sum(stat.page_views for stat in recent_stats)
    total_unique_visitors = sum(stat.unique_visitors for stat in recent_stats)
    total_job_clicks = sum(stat.job_page_clicks for stat in recent_stats)
    total_profile_views = sum(stat.profile_views for stat in recent_stats)
    total_application_clicks = sum(stat.application_clicks for stat in recent_stats)
    total_contact_clicks = sum(stat.contact_clicks for stat in recent_stats)
    
    avg_ctr = sum(float(stat.click_through_rate) for stat in recent_stats) / len(recent_stats) if recent_stats else 0
    avg_engagement = sum(float(stat.engagement_rate) for stat in recent_stats) / len(recent_stats) if recent_stats else 0
    
    print(f"  📊 Last 7 Days Totals:")
    print(f"     👁️  Page Views: {total_page_views}")
    print(f"     👥 Unique Visitors: {total_unique_visitors}")
    print(f"     🖱️  Job Page Clicks: {total_job_clicks}")
    print(f"     👤 Profile Views: {total_profile_views}")
    print(f"     📝 Application Clicks: {total_application_clicks}")
    print(f"     📞 Contact Clicks: {total_contact_clicks}")
    print(f"     📊 Avg CTR: {avg_ctr:.2f}%")
    print(f"     💫 Avg Engagement: {avg_engagement:.2f}%")
    
    print(f"\n✨ NO MORE ZEROS! All analytics cards should now show realistic data!")
    print(f"🚀 Visit https://staging.whoishiringintech.com to see the updated dashboard!")

if __name__ == "__main__":
    add_dummy_analytics_for_sourthings()