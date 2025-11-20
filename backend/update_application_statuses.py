import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, '/Users/mustafahepekiz/Desktop/whit/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whitbackend.settings')
django.setup()

from recruiters.models import JobApplication

print("Updating application statuses to match model...")

# Map old statuses to new ones
status_mapping = {
    'under_review': 'reviewing',
    'interview': 'interviewed',
    'accepted': 'offered',  # Keep one as offered to show progression
}

applications = JobApplication.objects.all()
updated_count = 0

for app in applications:
    if app.status in status_mapping:
        old_status = app.status
        app.status = status_mapping[old_status]
        app.save()
        print(f"Updated application {app.id}: {old_status} -> {app.status}")
        updated_count += 1
    else:
        print(f"Application {app.id}: {app.status} (no change)")

print(f"\nTotal applications updated: {updated_count}")
print("\nCurrent status distribution:")
for status, label in JobApplication.STATUS_CHOICES:
    count = JobApplication.objects.filter(status=status).count()
    if count > 0:
        print(f"  {label}: {count}")
