#!/usr/bin/env python3
"""Add advanced analytics patterns and historical data for impressive demo."""

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

def add_high_traffic_simulation():
    """Simulate high-traffic companies with impressive numbers"""
    
    # Popular tech companies that should have high engagement
    popular_companies = [
        {'id': 11, 'name': 'Apple', 'factor': 3.0},
        {'id': 10, 'name': 'Anthropic', 'factor': 2.5}, 
        {'id': 15, 'name': 'Atlassian', 'factor': 2.2},
        {'id': 19, 'name': 'Block', 'factor': 2.0},
        {'id': 8, 'name': 'AngelList', 'factor': 1.8},
    ]
    
    print("🔥 Adding high-traffic simulation for popular companies...")
    
    total_added = {'views': 0, 'clicks': 0}
    
    for company in popular_companies:
        company_id = company['id']
        name = company['name']
        factor = company['factor']
        
        # Add many page views
        views = int(random.randint(20, 40) * factor)
        clicks = int(random.randint(8, 15) * factor * 0.7)  # Slightly lower conversion for big companies
        
        print(f"  🚀 {name}: Adding {views} views, {clicks} clicks")
        
        for _ in range(views):
            success, _, _ = make_api_request('track-page-view', {'company_id': company_id})
            if success:
                total_added['views'] += 1
                
        for _ in range(clicks):
            success, _, _ = make_api_request('track-job-click', {'company_id': company_id})
            if success:
                total_added['clicks'] += 1
        
        sleep(0.1)  # Small delay
    
    print(f"  ✅ High-traffic simulation: +{total_added['views']} views, +{total_added['clicks']} clicks")
    return total_added

def add_startup_engagement_patterns():
    """Add engagement patterns typical of growing startups"""
    
    startup_companies = [
        {'id': 5, 'name': 'AeroLab'},
        {'id': 9, 'name': 'Anterior'},
        {'id': 24, 'name': 'Cedar'},
        {'id': 26, 'name': 'Chronosphere'},
        {'id': 16, 'name': 'Benchling'},
    ]
    
    print("🌟 Adding startup engagement patterns...")
    
    total_added = {'views': 0, 'clicks': 0}
    
    for company in startup_companies:
        company_id = company['id']
        name = company['name']
        
        # Startups often have higher conversion rates but less overall traffic
        views = random.randint(12, 25)
        clicks = random.randint(6, 12)  # Higher conversion rate
        
        print(f"  🚀 {name}: Adding {views} views, {clicks} clicks")
        
        for _ in range(views):
            success, _, _ = make_api_request('track-page-view', {'company_id': company_id})
            if success:
                total_added['views'] += 1
                
        for _ in range(clicks):
            success, _, _ = make_api_request('track-job-click', {'company_id': company_id})
            if success:
                total_added['clicks'] += 1
        
        sleep(0.05)
    
    print(f"  ✅ Startup patterns: +{total_added['views']} views, +{total_added['clicks']} clicks")
    return total_added

def add_enterprise_patterns():
    """Add patterns for enterprise companies"""
    
    enterprise_companies = [
        {'id': 21, 'name': 'Broadcom'},
        {'id': 25, 'name': 'CGI'},
        {'id': 23, 'name': 'Capgemini'},
        {'id': 28, 'name': 'Cirrus Logic'},
    ]
    
    print("🏢 Adding enterprise engagement patterns...")
    
    total_added = {'views': 0, 'clicks': 0}
    
    for company in enterprise_companies:
        company_id = company['id']
        name = company['name']
        
        # Enterprise companies often have steady, moderate engagement
        views = random.randint(15, 30)
        clicks = random.randint(4, 8)  # Lower conversion but steady
        
        print(f"  🏢 {name}: Adding {views} views, {clicks} clicks")
        
        for _ in range(views):
            success, _, _ = make_api_request('track-page-view', {'company_id': company_id})
            if success:
                total_added['views'] += 1
                
        for _ in range(clicks):
            success, _, _ = make_api_request('track-job-click', {'company_id': company_id})
            if success:
                total_added['clicks'] += 1
        
        sleep(0.05)
    
    print(f"  ✅ Enterprise patterns: +{total_added['views']} views, +{total_added['clicks']} clicks")
    return total_added

def add_bonus_sponsored_activity():
    """Add more sponsored activity to make it impressive"""
    
    print("💰 Adding bonus sponsored activity...")
    
    # Add more sponsored impressions and clicks
    impressions_added = 0
    clicks_added = 0
    
    for _ in range(150):  # Add 150 more impressions
        success, output, _ = make_api_request('sponsored/impression', {
            'campaign_id': 4,
            'page_url': 'https://staging.whoishiringintech.com/',
            'filters': {'country': random.choice(['United States', 'Canada', ''])},
            'page_number': random.choice([1, 1, 1, 2])
        })
        if success and 'success' in output:
            impressions_added += 1
            
            # Add clicks with realistic CTR (6-10%)
            if random.random() < random.uniform(0.06, 0.10):
                success, output, _ = make_api_request('sponsored/click', {
                    'campaign_id': 4,
                    'page_url': 'https://staging.whoishiringintech.com/',
                    'filters': {},
                    'page_number': 1
                })
                if success and 'success' in output:
                    clicks_added += 1
    
    print(f"  🎯 Bonus sponsored activity: +{impressions_added} impressions, +{clicks_added} clicks")
    return impressions_added, clicks_added

def main():
    print("🎯 Adding ADVANCED analytics data for impressive demo!")
    print("🌟 Your friends will be amazed!")
    print("=" * 65)
    
    # Track all additions
    total_stats = {
        'views': 0,
        'clicks': 0, 
        'impressions': 0,
        'sponsored_clicks': 0
    }
    
    # Add high-traffic patterns
    high_traffic = add_high_traffic_simulation()
    total_stats['views'] += high_traffic['views']
    total_stats['clicks'] += high_traffic['clicks']
    
    print()
    
    # Add startup patterns
    startup_stats = add_startup_engagement_patterns()
    total_stats['views'] += startup_stats['views']
    total_stats['clicks'] += startup_stats['clicks']
    
    print()
    
    # Add enterprise patterns
    enterprise_stats = add_enterprise_patterns()
    total_stats['views'] += enterprise_stats['views']
    total_stats['clicks'] += enterprise_stats['clicks']
    
    print()
    
    # Add bonus sponsored activity
    bonus_impressions, bonus_clicks = add_bonus_sponsored_activity()
    total_stats['impressions'] += bonus_impressions
    total_stats['sponsored_clicks'] += bonus_clicks
    
    # Final impressive summary
    print(f"\n" + "="*65)
    print("🎉 ADVANCED DEMO DATA COMPLETE!")
    print("="*65)
    print(f"📈 Additional page views: +{total_stats['views']}")
    print(f"💼 Additional job clicks: +{total_stats['clicks']}")
    print(f"🎯 Additional sponsored impressions: +{total_stats['impressions']}")
    print(f"💰 Additional sponsored clicks: +{total_stats['sponsored_clicks']}")
    
    print(f"\n🔥 COMBINED TOTALS (Today's Demo Data):")
    print(f"   👁️  Page views: ~{130 + total_stats['views']:,}")
    print(f"   🖱️  Job clicks: ~{68 + total_stats['clicks']:,}")
    print(f"   🎯 Sponsored impressions: ~{74 + total_stats['impressions']:,}")
    print(f"   💰 Sponsored clicks: ~{7 + total_stats['sponsored_clicks']:,}")
    
    overall_conversion = ((68 + total_stats['clicks']) / (130 + total_stats['views'])) * 100
    sponsor_ctr = ((7 + total_stats['sponsored_clicks']) / (74 + total_stats['impressions'])) * 100
    
    print(f"\n📊 IMPRESSIVE METRICS:")
    print(f"   📈 Conversion rate: {overall_conversion:.1f}%")
    print(f"   🎯 Sponsored CTR: {sponsor_ctr:.1f}%")
    
    print(f"\n✨ DEMO HIGHLIGHTS FOR YOUR FRIENDS:")
    print("   • High-traffic companies (Apple, Anthropic, etc.) with lots of engagement")
    print("   • Startup companies with high conversion rates") 
    print("   • Enterprise companies with steady patterns")
    print("   • Active sponsored campaigns with realistic performance")
    print("   • Professional analytics that look like a real business!")
    
    print(f"\n🚀 Ready to impress! Show them: https://staging.whoishiringintech.com")

if __name__ == "__main__":
    main()