"""
Management command to create a test sponsor campaign for demonstration.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from companies.models import Company, SponsorCampaign


class Command(BaseCommand):
    help = 'Create a test sponsor campaign for Samsara'

    def add_arguments(self, parser):
        parser.add_argument(
            '--company-name', 
            type=str, 
            default='Samsara',
            help='Name of the company to create campaign for'
        )
        parser.add_argument(
            '--days', 
            type=int, 
            default=30,
            help='Number of days the campaign should run'
        )
        parser.add_argument(
            '--daily-cap', 
            type=int, 
            default=1000,
            help='Daily impression cap'
        )

    def handle(self, *args, **options):
        company_name = options['company_name']
        days = options['days']
        daily_cap = options['daily_cap']
        
        try:
            # Get the company
            company = Company.objects.get(name=company_name)
            self.stdout.write(f"Found company: {company.name}")
            
            # Check if campaign already exists
            existing = SponsorCampaign.objects.filter(company=company, status='active').first()
            if existing:
                self.stdout.write(
                    self.style.WARNING(f"Active campaign already exists: {existing.name}")
                )
                return
                
            # Create campaign
            start_date = timezone.now()
            end_date = start_date + timedelta(days=days)
            
            campaign = SponsorCampaign.objects.create(
                company=company,
                name=f"{company.name} Test Campaign",
                status='active',
                start_at=start_date,
                end_at=end_date,
                priority=1,
                weight=1,
                daily_impression_cap=daily_cap,
                targeting_countries=[],  # All countries
                targeting_functions=[],  # All functions 
                targeting_work_env=[],   # All work environments
                pacing='even'
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created campaign: {campaign.name}\n"
                    f"  - Company: {company.name}\n"
                    f"  - Status: {campaign.status}\n"
                    f"  - Duration: {start_date.date()} to {end_date.date()}\n"
                    f"  - Daily cap: {daily_cap} impressions\n"
                    f"  - Priority: {campaign.priority}\n"
                    f"  - Targeting: All countries, functions, work environments"
                )
            )
            
        except Company.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(f"Company '{company_name}' not found")
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error creating campaign: {str(e)}")
            )