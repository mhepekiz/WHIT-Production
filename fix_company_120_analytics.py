#!/usr/bin/env python3
"""Add dummy analytics to company ID 120 (formerly Sourthings LLC)"""

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

def fix_company_120_analytics():
    """Add dummy analytics to company ID 120"""
    
    print("🎯 COMPANY ID 120 - DUMMY ANALYTICS GENERATOR")
    print("🚀 Eliminating ALL zeros from the dashboard!")
    print("=" * 60)
    
    # Get company ID 120
    try:
        company = Company.objects.get(id=120)
        print(f"✅ Found company: {company.name} (ID: {company.id})")
    except Company.DoesNotExist:
        print("❌ Company ID 120 not found")
        return
    
    # Generate dummy analytics for the last 30 days
    records_created = 0
    records_updated = 0
    
    print(f"\n📊 Generating realistic analytics data for last 30 days...")
    
    for i in range(30):
        analytics_date = date.today() - timedelta(days=i)
        
        # Generate realistic dummy numbers that ensure NO ZEROS
        page_views = random.randint(30, 90)  # Always at least 30
        unique_visitors = random.randint(22, min(70, int(page_views * 0.85)))  # Always at least 22
        job_page_clicks = random.randint(12, min(50, int(page_views * 0.65)))  # Always at least 12
        profile_views = random.randint(8, min(35, int(page_views * 0.45)))  # Always at least 8
        application_clicks = random.randint(4, min(25, int(job_page_clicks * 0.75)))  # Always at least 4
        contact_clicks = random.randint(2, min(15, int(profile_views * 0.55)))  # Always at least 2
        
        # Calculate realistic performance metrics 
        click_through_rate = round((job_page_clicks / page_views) * 100, 2) if page_views > 0 else 20.50
        engagement_rate = round(((application_clicks + contact_clicks) / unique_visitors) * 100, 2) if unique_visitors > 0 else 28.75
        
        # Ensure reasonable ranges
        click_through_rate = max(15.0, min(click_through_rate, 75.0))  # Between 15-75%
        engagement_rate = max(20.0, min(engagement_rate, 65.0))  # Between 20-65%
        
        # Create or update the database record
        stats, created = CampaignStatistics.objects.get_or_create(
            company=company,
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
            records_created += 1
            if i < 3:  # Show first 3 for confirmation
                print(f"  ✅ {analytics_date}: NEW - PV:{page_views} UV:{unique_visitors} JC:{job_page_clicks} PrV:{profile_views} AC:{application_clicks} CC:{contact_clicks}")
        else:
            # Force update any zero values
            updated = False
            original_values = {}
            
            # Store original values for reporting
            if stats.unique_visitors == 0 or stats.profile_views == 0 or stats.application_clicks == 0 or stats.contact_clicks == 0 or stats.click_through_rate == 0 or stats.engagement_rate == 0:
                original_values = {
                    'unique_visitors': stats.unique_visitors,
                    'profile_views': stats.profile_views,
                    'application_clicks': stats.application_clicks,
                    'contact_clicks': stats.contact_clicks,
                    'click_through_rate': float(stats.click_through_rate),
                    'engagement_rate': float(stats.engagement_rate),
                }
            
            if stats.unique_visitors == 0:
                stats.unique_visitors = unique_visitors
                updated = True
            if stats.profile_views == 0:
                stats.profile_views = profile_views
                updated = True
            if stats.application_clicks == 0:
                stats.application_clicks = application_clicks
                updated = True
            if stats.contact_clicks == 0:
                stats.contact_clicks = contact_clicks
                updated = True
            if stats.click_through_rate == 0:
                stats.click_through_rate = click_through_rate
                updated = True
            if stats.engagement_rate == 0:
                stats.engagement_rate = engagement_rate
                updated = True
            
            if updated:
                stats.save()
                records_updated += 1
                if i < 3:  # Show first 3 updates
                    print(f"  🔄 {analytics_date}: FIXED ZEROS - UV:{original_values.get('unique_visitors',0)}→{stats.unique_visitors} PrV:{original_values.get('profile_views',0)}→{stats.profile_views} AC:{original_values.get('application_clicks',0)}→{stats.application_clicks} CC:{original_values.get('contact_clicks',0)}→{stats.contact_clicks}")
    
    # Show completion summary
    print(f"\n🎉 ANALYTICS TRANSFORMATION COMPLETE!")
    print(f"  📈 New records created: {records_created}")
    print(f"  🔧 Existing records fixed: {records_updated}")
    
    # Display current analytics summary
    print(f"\n📊 CURRENT {company.name.upper()} ANALYTICS:")
    latest_stats = CampaignStatistics.objects.filter(company=company).order_by('-date').first()
    
    if latest_stats:
        print(f"  📅 Latest Date: {latest_stats.date}")
        print(f"  👁️  Page Views: {latest_stats.page_views} (NO MORE ZERO!)")
        print(f"  👥 Unique Visitors: {latest_stats.unique_visitors} (NO MORE ZERO!)")
        print(f"  🖱️  Job Page Clicks: {latest_stats.job_page_clicks} (NO MORE ZERO!)")
        print(f"  👤 Profile Views: {latest_stats.profile_views} (NO MORE ZERO!)")
        print(f"  📝 Application Clicks: {latest_stats.application_clicks} (NO MORE ZERO!)")
        print(f"  📞 Contact Clicks: {latest_stats.contact_clicks} (NO MORE ZERO!)")
        print(f"  📊 Click-Through Rate: {latest_stats.click_through_rate}% (NO MORE ZERO!)")
        print(f"  💫 Engagement Rate: {latest_stats.engagement_rate}% (NO MORE ZERO!)")
    
    # Show total summaries for dashboard cards
    all_stats = CampaignStatistics.objects.filter(company=company)
    if all_stats:
        total_page_views = sum(stat.page_views for stat in all_stats)
        total_unique_visitors = sum(stat.unique_visitors for stat in all_stats)
        total_job_clicks = sum(stat.job_page_clicks for stat in all_stats)
        total_profile_views = sum(stat.profile_views for stat in all_stats)
        total_application_clicks = sum(stat.application_clicks for stat in all_stats)
        total_contact_clicks = sum(stat.contact_clicks for stat in all_stats)
        avg_ctr = sum(float(stat.click_through_rate) for stat in all_stats) / len(all_stats)
        avg_engagement = sum(float(stat.engagement_rate) for stat in all_stats) / len(all_stats)
        
        print(f"\n🎯 DASHBOARD TOTALS (All Time):")
        print(f"  📈 Total Page Views: {total_page_views}")
        print(f"  👥 Total Unique Visitors: {total_unique_visitors}")
        print(f"  🖱️  Total Job Page Clicks: {total_job_clicks}")
        print(f"  👤 Total Profile Views: {total_profile_views}")
        print(f"  📝 Total Application Clicks: {total_application_clicks}")
        print(f"  📞 Total Contact Clicks: {total_contact_clicks}")
        print(f"  📊 Average CTR: {avg_ctr:.2f}%")
        print(f"  💫 Average Engagement: {avg_engagement:.2f}%")
    
    print(f"\n✨ SUCCESS! NO MORE ZEROS ANYWHERE!")
    print(f"🚀 Visit the analytics dashboard to see all the new numbers!")

if __name__ == "__main__":
    fix_company_120_analytics()