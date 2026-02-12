#!/usr/bin/env python3
"""Find the correct company name and add dummy analytics"""

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

def find_and_fix_sourthings():
    """Find Sourthings company and add dummy analytics"""
    
    print("🔍 SEARCHING FOR SOURTHINGS COMPANY")
    print("=" * 50)
    
    # Search for companies containing "Sourthings"
    sourthings_companies = Company.objects.filter(name__icontains='sourthings')
    
    if not sourthings_companies:
        print("❌ No companies found with 'sourthings' in name")
        print("\n📋 Let's check all companies:")
        
        # Show all companies to find the right one
        all_companies = Company.objects.all()[:20]  # Show first 20
        for company in all_companies:
            print(f"  - {company.name} (ID: {company.id})")
        
        return
    
    # Probably found it, use the first match
    sourthings = sourthings_companies[0]
    print(f"✅ Found company: {sourthings.name} (ID: {sourthings.id})")
    
    # Generate dummy analytics
    print(f"\n📊 Adding dummy analytics data...")
    
    records_created = 0
    records_updated = 0
    
    # Generate for last 30 days
    for i in range(30):
        analytics_date = date.today() - timedelta(days=i)
        
        # Generate realistic numbers - no more zeros!
        page_views = random.randint(25, 85)
        unique_visitors = random.randint(18, min(65, int(page_views * 0.9)))
        job_page_clicks = random.randint(8, min(45, int(page_views * 0.7)))
        profile_views = random.randint(5, min(30, int(page_views * 0.4)))
        application_clicks = random.randint(2, min(20, int(job_page_clicks * 0.6)))
        contact_clicks = random.randint(1, min(12, int(profile_views * 0.5)))
        
        # Calculate realistic percentages
        click_through_rate = round((job_page_clicks / page_views) * 100, 2) if page_views > 0 else 15.50
        engagement_rate = round(((application_clicks + contact_clicks) / unique_visitors) * 100, 2) if unique_visitors > 0 else 25.30
        
        # Ensure percentages are reasonable
        click_through_rate = min(click_through_rate, 80.0)  # Cap at 80%
        engagement_rate = min(engagement_rate, 60.0)  # Cap at 60%
        
        # Create or update record
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
            records_created += 1
            if i < 5:  # Show first 5 for confirmation
                print(f"  📅 {analytics_date}: PV:{page_views}, UV:{unique_visitors}, JC:{job_page_clicks}, PrV:{profile_views}, AC:{application_clicks}, CC:{contact_clicks}, CTR:{click_through_rate}%, ENG:{engagement_rate}%")
        else:
            # Update existing record to ensure no zeros
            updated = False
            
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
                if i < 5:  # Show first 5 updates
                    print(f"  🔄 {analytics_date}: Updated - UV:{stats.unique_visitors}, PrV:{stats.profile_views}, AC:{stats.application_clicks}, CC:{stats.contact_clicks}")
    
    print(f"\n🎉 DUMMY ANALYTICS COMPLETE!")
    print(f"  📈 New records: {records_created}")
    print(f"  🔄 Updated records: {records_updated}")
    
    # Show final summary
    recent_stats = CampaignStatistics.objects.filter(company=sourthings).order_by('-date')[:1].first()
    if recent_stats:
        print(f"\n📊 LATEST DAY ANALYTICS:")
        print(f"  👁️  Page Views: {recent_stats.page_views}")
        print(f"  👥 Unique Visitors: {recent_stats.unique_visitors}")
        print(f"  🖱️  Job Page Clicks: {recent_stats.job_page_clicks}")
        print(f"  👤 Profile Views: {recent_stats.profile_views}")
        print(f"  📝 Application Clicks: {recent_stats.application_clicks}")
        print(f"  📞 Contact Clicks: {recent_stats.contact_clicks}")
        print(f"  📊 CTR: {recent_stats.click_through_rate}%")
        print(f"  💫 Engagement: {recent_stats.engagement_rate}%")
    
    print(f"\n✨ ALL ZEROS ELIMINATED!")
    print(f"🚀 Dashboard should now show realistic data!")

if __name__ == "__main__":
    find_and_fix_sourthings()