#!/usr/bin/env python3
"""Script to add sponsored ad impression and click data for Sourthings LLC."""

import json
import subprocess
import random
from datetime import datetime, timedelta

def run_ssh_command(command):
    """Execute command via SSH on the staging server"""
    ssh_command = f'sshpass -p "sm0ky&&G0nc4" ssh -o StrictHostKeyChecking=no root@45.79.211.144 \'{command}\''
    try:
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def add_sponsor_data():
    """Add sponsored campaign impression and click data"""
    
    print("Adding sponsored ad data for Sourthings LLC (Campaign ID: 4)...")
    
    # Create Django management command to add data
    django_script = '''
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whit.settings")
sys.path.append("/var/www/whit/backend")
django.setup()

from companies.models import SponsorCampaign, SponsorStatsDaily, SponsorDeliveryLog
from django.utils import timezone

try:
    # Get the campaign
    campaign = SponsorCampaign.objects.get(id=4)
    print(f"Found campaign: {campaign.name} for {campaign.company.name}")
    
    # Add data for the last 7 days
    for i in range(7):
        date = (timezone.now() - timedelta(days=i)).date()
        
        # Generate realistic numbers (impressions between 50-200, clicks 2-15)
        impressions = random.randint(50, 200)
        clicks = random.randint(2, min(15, impressions // 10))  # CTR around 1-10%
        
        # Create or update daily stats
        stats, created = SponsorStatsDaily.objects.get_or_create(
            campaign=campaign,
            date=date,
            defaults={"impressions": impressions, "clicks": clicks}
        )
        
        if not created:
            # Update existing stats
            stats.impressions += impressions
            stats.clicks += clicks
            stats.save()
            
        print(f"Date {date}: {stats.impressions} impressions, {stats.clicks} clicks")
        
        # Add some delivery log entries for realism  
        for j in range(min(5, clicks)):
            user_hash = f"user_{random.randint(1000, 9999)}_{i}_{j}"
            
            # Add impression log
            SponsorDeliveryLog.objects.get_or_create(
                campaign=campaign,
                user_hash=user_hash,
                action="impression",
                page_key=f"browse:page=1:filters=hash_{random.randint(100,999)}",
                defaults={
                    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "ip_address": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
                    "referrer": "https://staging.whoishiringintech.com/"
                }
            )
            
            # Add click log
            SponsorDeliveryLog.objects.get_or_create(
                campaign=campaign,
                user_hash=user_hash,
                action="click", 
                page_key=f"browse:page=1:filters=hash_{random.randint(100,999)}",
                defaults={
                    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "ip_address": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
                    "referrer": "https://staging.whoishiringintech.com/"
                }
            )
    
    print("Successfully added sponsored ad data!")
    
    # Show summary
    total_stats = SponsorStatsDaily.objects.filter(campaign=campaign)
    total_impressions = sum(s.impressions for s in total_stats)
    total_clicks = sum(s.clicks for s in total_stats)
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    
    print(f"\\nCampaign Summary:")
    print(f"Total Impressions: {total_impressions}")
    print(f"Total Clicks: {total_clicks}")  
    print(f"CTR: {ctr:.2f}%")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
'''

    # Write the script to a temporary file on the server
    script_path = "/tmp/add_sponsor_data.py"
    
    # First, create the script file on the server
    success, out, err = run_ssh_command(f'cat > {script_path} << \'EOF\'\n{django_script}\nEOF')
    
    if not success:
        print(f"Failed to create script file: {err}")
        return False
        
    # Run the script using python3 directly (without venv since Django might not be installed in venv)
    command = f'cd /var/www/whit && PYTHONPATH=/var/www/whit/backend /usr/bin/python3 {script_path} 2>&1'
    success, output, error = run_ssh_command(command)
    
    print("Script output:")
    print(output)
    if error:
        print("Script errors:")
        print(error)
    
    # Clean up the temporary script
    run_ssh_command(f'rm {script_path}')
    
    return success

def main():
    print("🚀 Adding sponsored ad data for Sourthings LLC...")
    print("=" * 50)
    
    if add_sponsor_data():
        print("\n✅ Successfully added sponsored ad data!")
        print("\nYou can now check the staging website to see Sourthings LLC")
        print("with sponsored ad impression and click statistics.")
    else:
        print("\n❌ Failed to add sponsored data. Check the output above for details.")

if __name__ == "__main__":
    main()