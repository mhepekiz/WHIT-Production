from django.core.management.base import BaseCommand
from companies.models import Function


class Command(BaseCommand):
    help = 'Create job functions with colors from the screenshot'

    def handle(self, *args, **options):
        # Define functions with colors based on the screenshot
        functions_data = [
            {'name': 'Engineering', 'color': '#e8f5e9', 'text_color': '#2e7d32'},
            {'name': 'Product', 'color': '#fff9c4', 'text_color': '#f57f17'},
            {'name': 'Customer Success', 'color': '#fce4ec', 'text_color': '#c2185b'},
            {'name': 'Support', 'color': '#f3e5f5', 'text_color': '#7b1fa2'},
            {'name': 'Data', 'color': '#e1f5fe', 'text_color': '#0277bd'},
            {'name': 'Sales', 'color': '#fff3e0', 'text_color': '#e65100'},
            {'name': 'Finance', 'color': '#e0f2f1', 'text_color': '#00695c'},
            {'name': 'Marketing', 'color': '#fce4ec', 'text_color': '#c2185b'},
            {'name': 'Design', 'color': '#f3e5f5', 'text_color': '#7b1fa2'},
            {'name': 'HR', 'color': '#e8eaf6', 'text_color': '#3f51b5'},
            {'name': 'Internship', 'color': '#fce4ec', 'text_color': '#c2185b'},
            {'name': 'Custom', 'color': '#fff9c4', 'text_color': '#f57f17'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for func_data in functions_data:
            func, created = Function.objects.update_or_create(
                name=func_data['name'],
                defaults={
                    'color': func_data['color'],
                    'text_color': func_data['text_color']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {func.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {func.name}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
        ))
