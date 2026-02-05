from django.core.management.base import BaseCommand
from companies.models import Company


class Command(BaseCommand):
    help = 'Create test sponsored companies'

    def handle(self, *args, **options):
        try:
            # Get first 3 companies and make them sponsored
            companies = Company.objects.filter(status='Active')[:3]
            
            for i, company in enumerate(companies):
                company.is_sponsored = True
                company.sponsor_order = i + 1
                company.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully made "{company.name}" a sponsored company with order {i + 1}'
                    )
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {len(companies)} sponsored companies'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating sponsored companies: {str(e)}')
            )