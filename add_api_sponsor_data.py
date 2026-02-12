#!/usr/bin/env python3
"""Script to add sponsored ad data via API calls."""

import subprocess
import json
import random

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

def add_impressions_and_clicks():
    """Add impression and click data via API calls"""
    
    campaign_id = 4  # Sourthings LLC campaign
    print(f"Adding sponsored ad data for Campaign ID: {campaign_id}")
    
    total_impressions = 0
    total_clicks = 0
    
    # Add multiple impression and click records
    for i in range(20):  # 20 impressions
        # Add impression
        impression_data = {
            'campaign_id': campaign_id,
            'page_url': 'https://staging.whoishiringintech.com/',
            'filters': {},
            'page_number': 1
        }
        
        success, output, error = make_api_request('sponsored/impression', impression_data)
        
        if success and 'success' in output:
            total_impressions += 1
            print(f"✅ Impression {i+1} recorded")
        else:
            print(f"❌ Impression {i+1} failed: {output[:100]}")
        
        # Add clicks (roughly 10% click-through rate)
        if random.random() < 0.1:  # 10% chance
            click_data = {
                'campaign_id': campaign_id,
                'page_url': 'https://staging.whoishiringintech.com/',
                'filters': {},
                'page_number': 1
            }
            
            success, output, error = make_api_request('sponsored/click', click_data)
            
            if success and 'success' in output:
                total_clicks += 1
                print(f"  🖱️  Click {total_clicks} recorded")
            else:
                print(f"  ❌ Click failed: {output[:100]}")
    
    return total_impressions, total_clicks

def main():
    print("🚀 Adding sponsored ad data via API...")
    print("=" * 50)
    
    impressions, clicks = add_impressions_and_clicks()
    
    print("\n📊 Summary:")
    print(f"Total Impressions: {impressions}")
    print(f"Total Clicks: {clicks}")
    if impressions > 0:
        ctr = (clicks / impressions) * 100
        print(f"CTR: {ctr:.1f}%")
    
    print(f"\n✅ Sponsored ad data added for Sourthings LLC!")
    print("The company should now show impression and click statistics.")

if __name__ == "__main__":
    main()