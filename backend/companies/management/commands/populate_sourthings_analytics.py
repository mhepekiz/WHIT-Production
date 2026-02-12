from django.core.management.base import BaseCommand
from companies.models import Company, CampaignStatistics
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate realistic analytics data for Sourthings LLC'

    def handle(self, *args, **options):
        try:
            company = Company.objects.get(name='Sourthings LLC')
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR('Company "Sourthings LLC" not found'))
            return

        self.stdout.write(f'Found company: {company.name} (id={company.id})')

        today = date.today()
        updated = 0
        created = 0

        for days_ago in range(30):
            stats_date = today - timedelta(days=days_ago)

            # Weekday traffic is higher
            is_weekday = stats_date.weekday() < 5
            base_multiplier = random.uniform(1.0, 1.3) if is_weekday else random.uniform(0.5, 0.8)

            try:
                stat = CampaignStatistics.objects.get(company=company, date=stats_date)
                # Keep existing page_views and job_page_clicks if they have real data
                existing_pv = stat.page_views
                existing_jpc = stat.job_page_clicks

                if existing_pv > 0:
                    page_views = existing_pv
                else:
                    page_views = int(random.randint(25, 45) * base_multiplier)

                if existing_jpc > 0:
                    job_clicks = existing_jpc
                else:
                    job_clicks = int(page_views * random.uniform(0.30, 0.45))

                # Fill in the zeros with realistic proportional data
                stat.unique_visitors = int(page_views * random.uniform(0.55, 0.75))
                stat.profile_views = int(page_views * random.uniform(0.15, 0.30))
                stat.application_clicks = int(job_clicks * random.uniform(0.25, 0.50))
                stat.contact_clicks = int(stat.profile_views * random.uniform(0.10, 0.30))

                # Recalculate rates
                stat.click_through_rate = round(
                    job_clicks / page_views if page_views > 0 else 0, 4
                )
                total_engagement = stat.application_clicks + stat.contact_clicks
                stat.engagement_rate = round(
                    total_engagement / stat.unique_visitors if stat.unique_visitors > 0 else 0, 4
                )

                stat.page_views = page_views
                stat.job_page_clicks = job_clicks
                stat.save()
                updated += 1

            except CampaignStatistics.DoesNotExist:
                # Create new record for dates without any data
                page_views = int(random.randint(25, 45) * base_multiplier)
                unique_visitors = int(page_views * random.uniform(0.55, 0.75))
                job_clicks = int(page_views * random.uniform(0.30, 0.45))
                profile_views = int(page_views * random.uniform(0.15, 0.30))
                app_clicks = int(job_clicks * random.uniform(0.25, 0.50))
                contact_clicks = int(profile_views * random.uniform(0.10, 0.30))

                ctr = round(job_clicks / page_views if page_views > 0 else 0, 4)
                engagement = round(
                    (app_clicks + contact_clicks) / unique_visitors if unique_visitors > 0 else 0, 4
                )

                CampaignStatistics.objects.create(
                    company=company,
                    date=stats_date,
                    page_views=page_views,
                    unique_visitors=unique_visitors,
                    job_page_clicks=job_clicks,
                    profile_views=profile_views,
                    application_clicks=app_clicks,
                    contact_clicks=contact_clicks,
                    click_through_rate=ctr,
                    engagement_rate=engagement,
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! Updated {updated} records, created {created} new records for {company.name}'
        ))
