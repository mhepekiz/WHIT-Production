import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, '/Users/mustafahepekiz/Desktop/whit/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whitbackend.settings')
django.setup()

from recruiters.models import JobApplication, JobOpening, Recruiter
from django.contrib.auth.models import User

# Get the recruiter
recruiter_user = User.objects.get(email='mhepekiz@cisco.com')
recruiter = Recruiter.objects.get(user=recruiter_user)

print(f'Recruiter: {recruiter.company_name}')
print(f'Recruiter email: {recruiter_user.email}')

# Get applications for this recruiter's jobs
applications = JobApplication.objects.filter(job_opening__recruiter=recruiter)
print(f'\nTotal applications for this recruiter: {applications.count()}')

for app in applications:
    print(f'\nApplication ID: {app.id}')
    print(f'Job: {app.job_opening.title}')
    print(f'Candidate: {app.candidate_user.get_full_name()}')
    print(f'Status: {app.status}')
    print(f'Job belongs to recruiter: {app.job_opening.recruiter == recruiter}')
