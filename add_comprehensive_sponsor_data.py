#!/usr/bin/env python3
"""Add more comprehensive sponsored ad data over multiple days."""

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

def simulate_daily_activity():
    """Simulate realistic daily sponsored ad activity"""
    campaign_id = 4
    total_impressions = 0
    total_clicks = 0
    
    print("Simulating realistic sponsored ad activity for Sourthings LLC...")
    
    # Simulate activity over different times of day
    for session in range(5):  # 5 different simulated sessions
        impressions_this_session = random.randint(15, 35)  # 15-35 impressions per session
        clicks_this_session = 0
        
        print(f"\n📈 Session {session + 1}: Adding {impressions_this_session} impressions")
        
        for i in range(impressions_this_session):
            # Add impression
            impression_data = {
                'campaign_id': campaign_id,
                'page_url': 'https://staging.whoishiringintech.com/',
                'filters': {
                    'country': random.choice(['United States', '', 'Canada']),
                    'functions': random.choice(['Engineering', 'Product', '']),
                    'work_environments': random.choice(['Remote', 'Hybrid', ''])
                },
                'page_number': random.choice([1, 1, 1, 2])  # Most views on page 1
            }
            
            success, output, _ = make_api_request('sponsored/impression', impression_data)
            if success and 'success' in output:
                total_impressions += 1
                
                # Realistic click rate: 3-8% 
                if random.random() < random.uniform(0.03, 0.08):
                    click_data = impression_data.copy()
                    success, output, _ = make_api_request('sponsored/click', click_data)
                    if success and 'success' in output:
                        total_clicks += 1
                        clicks_this_session += 1
                        print(f"  🖱️  Click recorded (Session {session + 1})")
            
            # Small delay to be respectful to the server
            if i % 10 == 0 and i > 0:
                sleep(0.1)
        
        print(f"  ✅ Session {session + 1} complete: {clicks_this_session} clicks")
    
    return total_impressions, total_clicks

def main():
    print("🎯 Adding comprehensive sponsored ad data...")
    print("=" * 60)
    
    impressions, clicks = simulate_daily_activity()
    
    print(f"\n📊 Final Summary:")
    print(f"Total Impressions Added: {impressions}")
    print(f"Total Clicks Added: {clicks}")
    if impressions > 0:
        ctr = (clicks / impressions) * 100
        print(f"Click-Through Rate: {ctr:.2f}%")
    
    print(f"\n✅ Comprehensive sponsored ad data added successfully!")
    print("Sourthings LLC now has realistic sponsored campaign metrics.")
    print("\nYou can verify this by:")
    print("1. Visiting https://staging.whoishiringintech.com")
    print("2. Checking if Sourthings LLC appears at the top (sponsored position)")
    print("3. Looking for sponsored indicators in the UI")

if __name__ == "__main__":
    main()