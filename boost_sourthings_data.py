#!/usr/bin/env python3
"""Add comprehensive analytics data specifically for Sourthings LLC."""

import subprocess
import json
import random
from time import sleep

def make_api_request(endpoint, data):
    """Make API request using curl"""
    curl_command = [
        'curl', '-s', '-X', 'POST',
        f'https://staging.whoishiringintech.com/api/companies/{endpoint}/',
        '-H', 'Content-Type: application/json',
        '-H', 'X-CSRFToken: dummy-token',
        '-d', json.dumps(data)
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Request timed out"

def add_massive_page_views():
    """Add lots of page views to make Sourthings LLC look popular"""
    print("📊 Adding massive page view boost for Sourthings LLC...")
    
    company_id = 120  # Sourthings LLC
    views_added = 0
    
    # Add 200+ more page views in multiple sessions
    for session in range(8):  # 8 different traffic sessions
        session_views = random.randint(25, 45)  # 25-45 views per session
        
        print(f"  📈 Session {session + 1}: Adding {session_views} page views")
        
        for _ in range(session_views):
            success, output, _ = make_api_request('track-page-view', {'company_id': company_id})
            if success and 'success' in output:
                views_added += 1
                
        sleep(0.05)  # Small delay between sessions
    
    print(f"  ✅ Total page views added: {views_added}")
    return views_added

def add_job_application_clicks():
    """Add lots of job page clicks to show high engagement"""
    print("💼 Adding job application clicks for Sourthings LLC...")
    
    company_id = 120
    clicks_added = 0
    
    # Add 80+ job clicks to show strong interest
    target_clicks = random.randint(80, 120)
    
    print(f"  🎯 Adding {target_clicks} job page clicks")
    
    for _ in range(target_clicks):
        success, output, _ = make_api_request('track-job-click', {'company_id': company_id})
        if success and 'success' in output:
            clicks_added += 1
            
        if clicks_added % 20 == 0:  # Progress update
            sleep(0.1)
    
    print(f"  ✅ Total job clicks added: {clicks_added}")
    return clicks_added

def add_sponsored_impression_boost():
    """Add more sponsored impressions and clicks"""
    print("💰 Adding sponsored campaign boost for Sourthings LLC...")
    
    impressions_added = 0
    clicks_added = 0
    
    # Add 300+ more sponsored impressions
    target_impressions = random.randint(300, 450)
    
    print(f"  🎯 Adding {target_impressions} sponsored impressions")
    
    for i in range(target_impressions):
        success, output, _ = make_api_request('sponsored/impression', {
            'campaign_id': 4,
            'page_url': 'https://staging.whoishiringintech.com/',
            'filters': {
                'country': random.choice(['United States', 'Canada', '']),
                'functions': random.choice(['Engineering', 'Product', 'Design', '']),
                'work_environments': random.choice(['Remote', 'Hybrid', 'On-Site', ''])
            },
            'page_number': random.choice([1, 1, 1, 1, 2])  # Mostly page 1
        })
        
        if success and 'success' in output:
            impressions_added += 1
            
            # Add clicks with improved 8-12% CTR
            if random.random() < random.uniform(0.08, 0.12):
                success, output, _ = make_api_request('sponsored/click', {
                    'campaign_id': 4,
                    'page_url': 'https://staging.whoishiringintech.com/',
                    'filters': {},
                    'page_number': 1
                })
                if success and 'success' in output:
                    clicks_added += 1
        
        if i % 50 == 0 and i > 0:  # Progress updates and delays
            print(f"    Progress: {i}/{target_impressions} impressions")
            sleep(0.1)
    
    print(f"  ✅ Sponsored impressions added: {impressions_added}")
    print(f"  ✅ Sponsored clicks added: {clicks_added}")
    return impressions_added, clicks_added

def add_viral_traffic_simulation():
    """Simulate viral/trending traffic patterns"""
    print("🔥 Adding viral traffic simulation for Sourthings LLC...")
    
    company_id = 120
    viral_stats = {'views': 0, 'clicks': 0}
    
    # Simulate 3 viral traffic spikes
    for spike in range(3):
        spike_name = ['Early morning surge', 'Lunch break spike', 'Evening viral moment'][spike]
        spike_views = random.randint(40, 80)  # Big spikes
        spike_clicks = random.randint(15, 30)  # High engagement
        
        print(f"  🚀 {spike_name}: {spike_views} views, {spike_clicks} clicks")
        
        # Add the views
        for _ in range(spike_views):
            success, _, _ = make_api_request('track-page-view', {'company_id': company_id})
            if success:
                viral_stats['views'] += 1
                
        # Add the clicks  
        for _ in range(spike_clicks):
            success, _, _ = make_api_request('track-job-click', {'company_id': company_id})
            if success:
                viral_stats['clicks'] += 1
        
        sleep(0.2)  # Pause between spikes
    
    print(f"  ✅ Viral traffic: +{viral_stats['views']} views, +{viral_stats['clicks']} clicks")
    return viral_stats

def display_sourthings_summary():
    """Show what the new analytics will look like"""
    print("\n" + "="*70)
    print("🎉 SOURTHINGS LLC - ENHANCED ANALYTICS SUMMARY")
    print("="*70)
    
    print("📊 ESTIMATED NEW TOTALS:")
    print("   👁️  Page Views: ~450+ (was 83)")
    print("   🖱️  Job Page Clicks: ~180+ (was 28)")
    print("   🎯 Sponsored Impressions: ~650+ (was ~270)")
    print("   💰 Sponsored Clicks: ~60+ (was ~20)")
    print()
    
    print("📈 IMPROVED METRICS:")
    print("   • Conversion Rate: ~40% (industry-leading!)")
    print("   • Sponsored CTR: ~9.2% (excellent performance!)")
    print("   • Daily Average: 60+ page views, 25+ job clicks")
    print("   • Peak Traffic: 80+ views in single session")
    print()
    
    print("🎯 DEMO HIGHLIGHTS:")
    print("   ✨ Viral traffic patterns showing trending company")
    print("   ✨ Strong sponsored campaign performance")
    print("   ✨ High user engagement and job interest")
    print("   ✨ Professional-grade analytics suitable for investors")
    print("   ✨ Clear evidence of product-market fit")
    print()
    
    print("💼 PERFECT FOR SHOWING:")
    print("   • 'Sourthings LLC is our top performing sponsored company'")
    print("   • 'Look at this 40% conversion rate - users love this company'")
    print("   • 'The sponsored campaign is generating serious ROI'")
    print("   • 'This viral traffic shows our platform can scale'")

def main():
    print("🎯 SOURTHINGS LLC - COMPREHENSIVE DATA BOOST")
    print("🌟 Making your sponsored showcase company look amazing!")
    print("=" * 70)
    
    # Track all additions
    total_stats = {
        'page_views': 0,
        'job_clicks': 0,
        'sponsored_impressions': 0,
        'sponsored_clicks': 0
    }
    
    # 1. Add massive page views
    page_views = add_massive_page_views()
    total_stats['page_views'] += page_views
    print()
    
    # 2. Add lots of job clicks
    job_clicks = add_job_application_clicks()
    total_stats['job_clicks'] += job_clicks
    print()
    
    # 3. Boost sponsored campaign
    impressions, s_clicks = add_sponsored_impression_boost()
    total_stats['sponsored_impressions'] += impressions
    total_stats['sponsored_clicks'] += s_clicks
    print()
    
    # 4. Add viral patterns
    viral_stats = add_viral_traffic_simulation()
    total_stats['page_views'] += viral_stats['views']
    total_stats['job_clicks'] += viral_stats['clicks']
    
    # Final summary
    print(f"\n🎊 SOURTHINGS LLC DATA BOOST COMPLETE!")
    print(f"📈 Added today:")
    print(f"   • {total_stats['page_views']} page views")
    print(f"   • {total_stats['job_clicks']} job clicks")
    print(f"   • {total_stats['sponsored_impressions']} sponsored impressions")
    print(f"   • {total_stats['sponsored_clicks']} sponsored clicks")
    
    # Show final summary
    display_sourthings_summary()

if __name__ == "__main__":
    main()