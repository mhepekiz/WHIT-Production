import csv
from django.core.management.base import BaseCommand
from companies.models import Company, Function


class Command(BaseCommand):
    help = 'Import companies from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        self.stdout.write(self.style.WARNING(f'Importing companies from {csv_file}...'))
        
        imported = 0
        updated = 0
        errors = 0
        
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Clean and prepare data
                    functions_text = row.get('Function', '').strip()
                    
                    company_data = {
                        'name': row.get('Company Name', '').strip(),
                        'logo': row.get('Logo', '').strip() or None,
                        'jobs_page_url': row.get('Jobs Page URL', '').strip(),
                        'company_reviews': row.get('Company Reviews', '').strip() or None,
                        'country': row.get('Country', '').strip(),
                        'state': row.get('State', '').strip() or None,
                        'city': row.get('City', '').strip() or None,
                        'work_environment': row.get('WorkEnvironment', '').strip(),
                        'functions_text': functions_text,
                        'engineering_positions': row.get('EngineeringPositions', '').strip().lower() == 'checked',
                        'status': row.get('Status', 'Active').strip(),
                    }
                    
                    if not company_data['name'] or not company_data['jobs_page_url']:
                        errors += 1
                        continue
                    
                    # Create or update company
                    company, created = Company.objects.update_or_create(
                        name=company_data['name'],
                        defaults=company_data
                    )
                    
                    # Parse and assign functions
                    if functions_text:
                        function_names = [f.strip() for f in functions_text.split(',') if f.strip()]
                        company.functions.clear()
                        
                        for func_name in function_names:
                            func, _ = Function.objects.get_or_create(name=func_name)
                            company.functions.add(func)
                    
                    if created:
                        imported += 1
                        self.stdout.write(self.style.SUCCESS(f'✓ Imported: {company.name}'))
                    else:
                        updated += 1
                        self.stdout.write(self.style.WARNING(f'↻ Updated: {company.name}'))
                        
                except Exception as e:
                    errors += 1
                    self.stdout.write(self.style.ERROR(f'✗ Error processing row: {str(e)}'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(f'Import completed!'))
        self.stdout.write(self.style.SUCCESS(f'Imported: {imported}'))
        self.stdout.write(self.style.WARNING(f'Updated: {updated}'))
        self.stdout.write(self.style.ERROR(f'Errors: {errors}'))
        self.stdout.write(self.style.SUCCESS('='*50))
