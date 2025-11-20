import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from recruiters.models import Recruiter, JobOpening, JobApplication
from django.contrib.auth.models import User
from decimal import Decimal

def create_dummy_jobs_and_applications():
    # Get the recruiter (assuming Mustafa is the recruiter)
    try:
        recruiter_user = User.objects.get(email='mhepekiz@cisco.com')
        recruiter = Recruiter.objects.get(user=recruiter_user)
    except:
        print("Recruiter not found. Please make sure you're logged in as a recruiter first.")
        return

    # Get job seeker users
    job_seekers = User.objects.filter(
        username__in=['john.doe', 'sarah.johnson', 'michael.chen', 'emily.rodriguez', 
                      'david.kim', 'lisa.thompson', 'james.wilson', 'amanda.patel']
    )

    print(f"Found {job_seekers.count()} job seekers")

    # Create dummy job openings
    jobs_data = [
        {
            'title': 'Senior Software Engineer',
            'department': 'Engineering',
            'employment_type': 'full-time',
            'experience_level': 'senior',
            'description': 'We are seeking an experienced Senior Software Engineer to join our team. You will be responsible for designing and implementing scalable solutions.',
            'requirements': 'Bachelor\'s degree in Computer Science or related field\n5+ years of software development experience\nProficiency in Python, JavaScript, and React\nExperience with cloud platforms (AWS/GCP/Azure)\nStrong problem-solving skills',
            'responsibilities': 'Design and develop high-quality software solutions\nMentor junior developers\nParticipate in code reviews\nCollaborate with product managers and designers\nEnsure best practices and coding standards',
            'location': 'San Francisco, CA',
            'city': 'San Francisco',
            'state': 'CA',
            'country': 'United States',
            'remote_allowed': True,
            'salary_min': Decimal('150000'),
            'salary_max': Decimal('200000'),
            'salary_currency': 'USD',
            'status': 'active',
            'application_deadline': datetime.now() + timedelta(days=30),
            'application_email': 'careers@cisco.com',
            'skills_required': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes'],
        },
        {
            'title': 'Product Designer',
            'department': 'Design',
            'employment_type': 'full-time',
            'experience_level': 'mid',
            'description': 'Join our design team to create beautiful and intuitive user experiences for our enterprise products.',
            'requirements': 'Bachelor\'s degree in Design, HCI, or related field\n3+ years of product design experience\nProficiency in Figma, Sketch, or similar tools\nStrong portfolio demonstrating UX/UI skills\nExperience with design systems',
            'responsibilities': 'Create wireframes, prototypes, and high-fidelity designs\nConduct user research and usability testing\nCollaborate with engineers and product managers\nMaintain and evolve design system\nPresent designs to stakeholders',
            'location': 'Austin, TX',
            'city': 'Austin',
            'state': 'TX',
            'country': 'United States',
            'remote_allowed': True,
            'salary_min': Decimal('100000'),
            'salary_max': Decimal('140000'),
            'salary_currency': 'USD',
            'status': 'active',
            'application_deadline': datetime.now() + timedelta(days=45),
            'application_email': 'careers@cisco.com',
            'skills_required': ['Figma', 'Sketch', 'UX Design', 'UI Design', 'Prototyping'],
        },
        {
            'title': 'Data Scientist',
            'department': 'Data & Analytics',
            'employment_type': 'full-time',
            'experience_level': 'senior',
            'description': 'We\'re looking for a talented Data Scientist to help us unlock insights from our data and build predictive models.',
            'requirements': 'Master\'s or PhD in Computer Science, Statistics, or related field\n5+ years of data science experience\nExpertise in Python, R, SQL\nExperience with machine learning frameworks (TensorFlow, PyTorch)\nStrong statistical analysis skills',
            'responsibilities': 'Develop and deploy machine learning models\nAnalyze large datasets to extract insights\nCollaborate with engineering teams\nCommunicate findings to stakeholders\nStay current with latest ML/AI techniques',
            'location': 'Seattle, WA',
            'city': 'Seattle',
            'state': 'WA',
            'country': 'United States',
            'remote_allowed': False,
            'salary_min': Decimal('180000'),
            'salary_max': Decimal('250000'),
            'salary_currency': 'USD',
            'status': 'active',
            'application_deadline': datetime.now() + timedelta(days=60),
            'application_email': 'careers@cisco.com',
            'skills_required': ['Python', 'R', 'Machine Learning', 'TensorFlow', 'PyTorch', 'SQL'],
        },
        {
            'title': 'Marketing Manager',
            'department': 'Marketing',
            'employment_type': 'full-time',
            'experience_level': 'mid',
            'description': 'Lead our marketing efforts and drive growth through innovative campaigns and strategies.',
            'requirements': 'Bachelor\'s degree in Marketing or related field\n4+ years of marketing experience\nExperience with digital marketing and analytics\nStrong communication and leadership skills\nB2B SaaS experience preferred',
            'responsibilities': 'Develop and execute marketing strategies\nManage marketing campaigns across channels\nAnalyze campaign performance and ROI\nCollaborate with sales and product teams\nManage marketing budget',
            'location': 'New York, NY',
            'city': 'New York',
            'state': 'NY',
            'country': 'United States',
            'remote_allowed': True,
            'salary_min': Decimal('100000'),
            'salary_max': Decimal('140000'),
            'salary_currency': 'USD',
            'status': 'active',
            'application_deadline': datetime.now() + timedelta(days=30),
            'application_email': 'careers@cisco.com',
            'skills_required': ['Digital Marketing', 'SEO', 'SEM', 'Analytics', 'Content Marketing'],
        },
        {
            'title': 'Frontend Developer',
            'department': 'Engineering',
            'employment_type': 'full-time',
            'experience_level': 'entry',
            'description': 'Join our frontend team to build modern, responsive web applications using the latest technologies.',
            'requirements': 'Bachelor\'s degree in Computer Science or related field\n2+ years of frontend development experience\nProficiency in React, JavaScript, HTML, CSS\nUnderstanding of responsive design\nExperience with version control (Git)',
            'responsibilities': 'Develop user-facing features\nEnsure cross-browser compatibility\nOptimize applications for speed and scalability\nCollaborate with designers and backend developers\nWrite clean, maintainable code',
            'location': 'Los Angeles, CA',
            'city': 'Los Angeles',
            'state': 'CA',
            'country': 'United States',
            'remote_allowed': True,
            'salary_min': Decimal('80000'),
            'salary_max': Decimal('110000'),
            'salary_currency': 'USD',
            'status': 'active',
            'application_deadline': datetime.now() + timedelta(days=45),
            'application_email': 'careers@cisco.com',
            'skills_required': ['React', 'JavaScript', 'HTML', 'CSS', 'Git'],
        },
        {
            'title': 'DevOps Engineer',
            'department': 'Engineering',
            'employment_type': 'full-time',
            'experience_level': 'mid',
            'description': 'Help us build and maintain our cloud infrastructure and CI/CD pipelines.',
            'requirements': 'Bachelor\'s degree in Computer Science or related field\n3+ years of DevOps experience\nExperience with AWS, Docker, Kubernetes\nProficiency in scripting (Python, Bash)\nStrong understanding of CI/CD practices',
            'responsibilities': 'Manage cloud infrastructure\nBuild and maintain CI/CD pipelines\nMonitor system performance and reliability\nAutomate deployment processes\nEnsure security best practices',
            'location': 'Chicago, IL',
            'city': 'Chicago',
            'state': 'IL',
            'country': 'United States',
            'remote_allowed': True,
            'salary_min': Decimal('130000'),
            'salary_max': Decimal('170000'),
            'salary_currency': 'USD',
            'status': 'draft',
            'application_deadline': datetime.now() + timedelta(days=30),
            'application_email': 'careers@cisco.com',
            'skills_required': ['AWS', 'Docker', 'Kubernetes', 'Python', 'Bash', 'CI/CD'],
        },
    ]

    all_jobs = []
    created_jobs = []
    for job_data in jobs_data:
        job, created = JobOpening.objects.get_or_create(
            recruiter=recruiter,
            title=job_data['title'],
            defaults=job_data
        )
        all_jobs.append(job)
        if created:
            created_jobs.append(job)
            print(f"Created job: {job.title}")
        else:
            print(f"Job already exists: {job.title}")

    # Create applications for active jobs only
    active_jobs = [job for job in all_jobs if job.status == 'active']
    
    # Application templates
    applications_data = [
        {
            'job': active_jobs[0] if len(active_jobs) > 0 else None,  # Senior Software Engineer
            'applicants': ['john.doe', 'james.wilson'],
            'cover_letters': [
                'I am excited to apply for the Senior Software Engineer position. With over 5 years of experience in full-stack development, I have a proven track record of building scalable applications.',
                'As a DevOps Engineer with strong development skills, I am interested in transitioning to a more development-focused role. My experience with cloud infrastructure would be valuable to your team.',
            ],
            'statuses': ['under_review', 'pending'],
        },
        {
            'job': active_jobs[1] if len(active_jobs) > 1 else None,  # Product Designer
            'applicants': ['sarah.johnson', 'amanda.patel'],
            'cover_letters': [
                'I would love to bring my 7 years of product design experience to your team. My portfolio demonstrates my ability to create user-centered designs.',
                'As a UX researcher with design skills, I am passionate about creating intuitive user experiences through research-driven design.',
            ],
            'statuses': ['interview', 'under_review'],
        },
        {
            'job': active_jobs[2] if len(active_jobs) > 2 else None,  # Data Scientist
            'applicants': ['michael.chen'],
            'cover_letters': [
                'With a PhD in Computer Science and 6 years of experience in machine learning, I am well-suited for this Data Scientist role. I have published research in top AI conferences.',
            ],
            'statuses': ['accepted'],
        },
        {
            'job': active_jobs[3] if len(active_jobs) > 3 else None,  # Marketing Manager
            'applicants': ['emily.rodriguez'],
            'cover_letters': [
                'I am excited about the opportunity to lead your marketing efforts. My 4 years of B2B SaaS marketing experience have prepared me for this role.',
            ],
            'statuses': ['interview'],
        },
        {
            'job': active_jobs[4] if len(active_jobs) > 4 else None,  # Frontend Developer
            'applicants': ['david.kim', 'john.doe'],
            'cover_letters': [
                'I am passionate about building beautiful and functional user interfaces. My portfolio showcases my React and modern web development skills.',
                'While I am currently a Senior Engineer, I am interested in focusing more on frontend development and would love to contribute to your team.',
            ],
            'statuses': ['pending', 'rejected'],
        },
    ]

    application_count = 0
    for app_data in applications_data:
        if not app_data['job']:
            continue
            
        for idx, username in enumerate(app_data['applicants']):
            try:
                applicant = User.objects.get(username=username)
                
                application, created = JobApplication.objects.get_or_create(
                    job_opening=app_data['job'],
                    candidate_user=applicant,
                    defaults={
                        'cover_letter': app_data['cover_letters'][idx],
                        'status': app_data['statuses'][idx],
                    }
                )
                
                if created:
                    application_count += 1
                    print(f"Created application: {applicant.get_full_name()} -> {app_data['job'].title} ({app_data['statuses'][idx]})")
                else:
                    print(f"Application already exists: {applicant.get_full_name()} -> {app_data['job'].title}")
            except User.DoesNotExist:
                print(f"User not found: {username}")

    print(f"\nSummary:")
    print(f"Jobs created: {len(created_jobs)}")
    print(f"Applications created: {application_count}")

if __name__ == '__main__':
    create_dummy_jobs_and_applications()
