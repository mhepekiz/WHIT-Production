#!/usr/bin/env python3
"""
Sponsor Dashboard Access Instructions

To access the new Sponsor Stats Dashboard in your Django admin:

1. Start your Django development server:
   python manage.py runserver

2. Go to your admin interface:
   http://localhost:8000/admin/

3. Navigate to Companies section

4. You'll see a new "📊 Sponsor Dashboard" button in the top-right of the Company list page

5. Or go directly to:
   http://localhost:8000/admin/companies/company/sponsor-dashboard/

Features of the Sponsor Dashboard:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Real-time Stats Cards:
   • Today's Impressions, Clicks, CTR
   • Active Campaigns Count

📈 Interactive Performance Chart:
   • Last 7/14/30 days performance
   • Shows Impressions, Clicks, and CTR over time
   • Dynamic chart updates with period selection

🏆 Top Performing Campaigns:
   • Weekly leaderboard of best performing campaigns
   • Shows Company, Impressions, Clicks, CTR

🎯 Active Campaigns List:
   • All currently running campaigns
   • Campaign status and company information

🔄 API Integration:
   • Real-time data updates
   • RESTful API endpoint for stats
   • JSON data format for external integrations

API Endpoint:
GET /admin/companies/company/sponsor-dashboard/api/stats/?period=7

Response Format:
{
    "daily_stats": {
        "2024-02-01": {"impressions": 1234, "clicks": 56, "ctr": 4.54}
    },
    "campaign_stats": {
        "Campaign Name": {"impressions": 500, "clicks": 25, "ctr": 5.0, "company": "Company Name"}
    },
    "company_stats": {
        "Company Name": {"impressions": 500, "clicks": 25, "ctr": 5.0}
    },
    "period": "7 days"
}

Database Tables Used:
• SponsorCampaign - Campaign information
• SponsorStatsDaily - Daily aggregated stats  
• SponsorDeliveryLog - Individual impression/click events

The dashboard automatically calculates:
• Click-through rates (CTR)
• Daily performance trends
• Campaign rankings
• Company performance comparisons
"""

print(__doc__)