#!/usr/bin/env python3
"""Add comprehensive dummy analytics data for demo purposes."""

import subprocess
import json
import random
from datetime import datetime, timedelta

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

def get_top_companies():
    """Get list of companies from the API"""
    curl_command = [
        'curl', '-s', 
        'https://staging.whoishiringintech.com/api/companies/'
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('results', [])[:15]  # Get first 15 companies
    except:
        pass
    return []

def add_page_views(company_id, company_name):
    """Add realistic page view data"""
    views_added = 0
    
    # Add multiple page view sessions
    for session in range(random.randint(5, 12)):  # 5-12 different sessions
        success, output, _ = make_api_request('track-page-view', {
            'company_id': company_id
        })
        if success and 'success' in output:
            views_added += 1
    
    print(f"  📊 {company_name}: {views_added} page views added")
    return views_added

def add_job_clicks(company_id, company_name):
    """Add realistic job click data"""
    clicks_added = 0
    
    # Add job page clicks (conversion from page views)
    click_count = random.randint(2, 8)  # 2-8 job clicks
    for click in range(click_count):
        success, output, _ = make_api_request('track-job-click', {
            'company_id': company_id
        })
        if success and 'success' in output:
            clicks_added += 1
    
    print(f"  🖱️  {company_name}: {clicks_added} job page clicks added")
    return clicks_added

def add_sponsored_activity(company_id, company_name, is_sponsored=False):
    """Add sponsored campaign activity if applicable"""
    if not is_sponsored:
        return 0, 0
        
    impressions = 0
    clicks = 0
    
    # Add sponsored impressions
    impression_count = random.randint(25, 80)
    for i in range(impression_count):
        success, output, _ = make_api_request('sponsored/impression', {
            'campaign_id': 4,  # Assuming Sourthings LLC campaign
            'page_url': 'https://staging.whoishiringintech.com/',
            'filters': {},
            'page_number': 1
        })
        if success and 'success' in output:
            impressions += 1
            
        # Add sponsored clicks (5-12% CTR)
        if random.random() < random.uniform(0.05, 0.12):
            success, output, _ = make_api_request('sponsored/click', {
                'campaign_id': 4,
                'page_url': 'https://staging.whoishiringintech.com/',
                'filters': {},
                'page_number': 1
            })
            if success and 'success' in output:
                clicks += 1
    
    if impressions > 0 or clicks > 0:
        print(f"  🎯 {company_name} (SPONSORED): {impressions} impressions, {clicks} clicks")
    
    return impressions, clicks

def simulate_realistic_activity():
    """Add realistic activity across multiple companies"""
    
    print("🎭 Adding comprehensive dummy analytics data...")
    print("=" * 60)
    
    companies = get_top_companies()
    if not companies:
        print("❌ Could not fetch companies")
        return
        
    print(f"📈 Adding analytics data for {len(companies)} companies...")
    
    total_stats = {
        'page_views': 0,
        'job_clicks': 0, 
        'sponsored_impressions': 0,
        'sponsored_clicks': 0,
        'companies_processed': 0
    }
    
    # Process each company
    for i, company in enumerate(companies):
        company_id = company['id']
        company_name = company['name']
        is_sponsored = company.get('is_sponsored', False)
        
        print(f"\n🏢 Processing: {company_name}" + (" (SPONSORED)" if is_sponsored else ""))
        
        # Add page views (every company gets some traffic)
        page_views = add_page_views(company_id, company_name)
        total_stats['page_views'] += page_views
        
        # Add job clicks (conversion from page views)
        job_clicks = add_job_clicks(company_id, company_name)
        total_stats['job_clicks'] += job_clicks
        
        # Add sponsored activity for sponsored companies
        if is_sponsored:
            impressions, clicks = add_sponsored_activity(company_id, company_name, True)
            total_stats['sponsored_impressions'] += impressions
            total_stats['sponsored_clicks'] += clicks
        
        total_stats['companies_processed'] += 1
        
        # Small delay to be respectful to server
        if i % 3 == 0:
            import time
            time.sleep(0.1)
    
    return total_stats

def add_additional_engagement_data():
    """Add more diverse engagement patterns"""
    print(f"\n🎨 Adding diverse engagement patterns...")
    
    # Simulate weekend vs weekday traffic
    weekend_companies = random.sample(range(5, 25), 5)  # Random company IDs
    
    for company_id in weekend_companies:
        # Weekend traffic is usually lower but more engaged
        for _ in range(random.randint(2, 5)):  # Fewer page views
            make_api_request('track-page-view', {'company_id': company_id})
            
        for _ in range(random.randint(1, 3)):  # But higher conversion
            make_api_request('track-job-click', {'company_id': company_id})
    
    print("  📅 Added weekend engagement patterns")
    
    # Simulate mobile vs desktop patterns
    mobile_heavy_companies = random.sample(range(10, 30), 3)
    
    for company_id in mobile_heavy_companies:
        # Mobile users typically have more page views but fewer conversions
        for _ in range(random.randint(8, 15)):  # More browsing
            make_api_request('track-page-view', {'company_id': company_id})
            
        for _ in range(random.randint(1, 2)):  # Lower conversion
            make_api_request('track-job-click', {'company_id': company_id})
    
    print("  📱 Added mobile engagement patterns")

def main():
    print("🚀 Creating comprehensive demo analytics data...")
    print("🎯 Perfect for showcasing to friends!")
    print("=" * 70)
    
    # Main analytics simulation
    stats = simulate_realistic_activity()
    
    if not stats:
        return
        
    # Add diverse patterns for realism
    add_additional_engagement_data()
    
    # Final summary
    print(f"\n" + "="*70)
    print("📊 DEMO DATA SUMMARY")
    print("="*70)
    print(f"🏢 Companies with data: {stats['companies_processed']}")
    print(f"👁️  Total page views: {stats['page_views']}")
    print(f"🖱️  Total job clicks: {stats['job_clicks']}")
    print(f"🎯 Sponsored impressions: {stats['sponsored_impressions']}")
    print(f"💰 Sponsored clicks: {stats['sponsored_clicks']}")
    
    if stats['page_views'] > 0:
        conversion_rate = (stats['job_clicks'] / stats['page_views']) * 100
        print(f"📈 Overall conversion rate: {conversion_rate:.1f}%")
        
    if stats['sponsored_impressions'] > 0:
        sponsor_ctr = (stats['sponsored_clicks'] / stats['sponsored_impressions']) * 100
        print(f"🎯 Sponsored CTR: {sponsor_ctr:.1f}%")
    
    print(f"\n✅ Demo data ready! Your friends will see:")
    print("   • Companies with realistic traffic patterns")
    print("   • Varied engagement levels across different companies") 
    print("   • Sponsored content performance metrics")
    print("   • Professional-looking analytics data")
    print(f"\n🌐 View at: https://staging.whoishiringintech.com")

if __name__ == "__main__":
    main()