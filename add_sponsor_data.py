#!/usr/bin/env python3
"""Script to add sponsored ad data for Sourthings LLC on the staging server."""

import requests
import json
from datetime import datetime, timedelta
import random

# API Configuration
API_BASE = "https://staging.whoishiringintech.com/api"

def get_company_id():
    """Get the company ID for Sourthings LLC"""
    print("Fetching companies to find Sourthings LLC...")
    
    response = requests.get(f"{API_BASE}/companies/")
    if response.status_code == 200:
        companies = response.json()
        
        for company in companies.get('results', companies):
            if "Sourthings" in company.get('name', ''):
                print(f"Found company: {company['name']} (ID: {company['id']})")
                return company['id']
                
    print("Could not find Sourthings LLC in the companies list")
    return None

def record_sponsored_impression(campaign_id):
    """Record a sponsored impression via API"""
    data = {
        'campaign_id': campaign_id,
        'page_url': 'https://staging.whoishiringintech.com/',
        'filters': {},
        'page_number': 1
    }
    
    response = requests.post(f"{API_BASE}/companies/sponsored/impression/", json=data)
    return response.status_code == 200

def record_sponsored_click(campaign_id):
    """Record a sponsored click via API"""
    data = {
        'campaign_id': campaign_id,
        'page_url': 'https://staging.whoishiringintech.com/',
        'filters': {},
        'page_number': 1
    }
    
    response = requests.post(f"{API_BASE}/companies/sponsored/click/", json=data)
    return response.status_code == 200

def main():
    print("Adding sponsored ad data for Sourthings LLC...")
    
    # First get the company ID
    company_id = get_company_id()
    if not company_id:
        return
    
    print(f"Found Sourthings LLC with ID: {company_id}")
    
    # Note: We would need Django admin access or direct database access to create a SponsorCampaign
    # For now, let's check what campaigns might exist
    print("This script requires direct database access to create a SponsorCampaign.")
    print("We can create the campaign via Django admin or direct database query.")
    
    print("Company ID for Sourthings LLC:", company_id)

if __name__ == "__main__":
    main()