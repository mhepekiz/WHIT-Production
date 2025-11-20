import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, JobPreference
from companies.models import Function, WorkEnvironment

def create_dummy_users():
    # Create dummy users with profiles and preferences
    dummy_users = [
        {
            'username': 'john.doe',
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'profile': {
                'phone': '+1-555-0101',
                'location': 'San Francisco, CA',
                'bio': 'Experienced software engineer with 5+ years in full-stack development. Passionate about building scalable web applications.',
                'current_title': 'Senior Software Engineer',
                'years_of_experience': 5,
                'linkedin_url': 'https://linkedin.com/in/johndoe',
                'github_url': 'https://github.com/johndoe',
            },
            'preferences': {
                'desired_functions': ['Engineering', 'Product'],
                'work_environments': ['Remote', 'Hybrid'],
                'employment_types': 'full-time',
                'preferred_locations': 'San Francisco, CA, New York, NY',
                'willing_to_relocate': True,
                'remote_only': False,
                'minimum_salary': '150k-200k',
                'industries': 'SaaS, FinTech, HealthTech',
                'company_size_preference': 'Startup, Mid-size',
                'actively_looking': True,
            }
        },
        {
            'username': 'sarah.johnson',
            'email': 'sarah.johnson@example.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'profile': {
                'phone': '+1-555-0102',
                'location': 'Austin, TX',
                'bio': 'Product designer with a keen eye for user experience. 7 years of experience creating beautiful and functional interfaces.',
                'current_title': 'Lead Product Designer',
                'years_of_experience': 7,
                'linkedin_url': 'https://linkedin.com/in/sarahjohnson',
                'portfolio_url': 'https://sarahjohnson.design',
            },
            'preferences': {
                'desired_functions': ['Design'],
                'work_environments': ['Remote'],
                'employment_types': 'full-time,contract',
                'preferred_locations': 'Austin, TX, Remote',
                'willing_to_relocate': False,
                'remote_only': True,
                'minimum_salary': '100k-150k',
                'industries': 'SaaS, E-commerce, EdTech',
                'company_size_preference': 'Startup, Mid-size',
                'actively_looking': True,
            }
        },
        {
            'username': 'michael.chen',
            'email': 'michael.chen@example.com',
            'first_name': 'Michael',
            'last_name': 'Chen',
            'profile': {
                'phone': '+1-555-0103',
                'location': 'Seattle, WA',
                'bio': 'Data scientist specializing in machine learning and predictive analytics. PhD in Computer Science.',
                'current_title': 'Senior Data Scientist',
                'years_of_experience': 6,
                'linkedin_url': 'https://linkedin.com/in/michaelchen',
                'github_url': 'https://github.com/michaelchen',
            },
            'preferences': {
                'desired_functions': ['Data Science', 'Engineering'],
                'work_environments': ['Hybrid', 'On-site'],
                'employment_types': 'full-time',
                'preferred_locations': 'Seattle, WA, San Francisco, CA',
                'willing_to_relocate': True,
                'remote_only': False,
                'minimum_salary': '200k+',
                'industries': 'AI/ML, FinTech, Healthcare',
                'company_size_preference': 'Mid-size, Enterprise',
                'actively_looking': False,
            }
        },
        {
            'username': 'emily.rodriguez',
            'email': 'emily.rodriguez@example.com',
            'first_name': 'Emily',
            'last_name': 'Rodriguez',
            'profile': {
                'phone': '+1-555-0104',
                'location': 'New York, NY',
                'bio': 'Marketing professional with expertise in digital marketing and growth strategies. B2B SaaS specialist.',
                'current_title': 'Marketing Manager',
                'years_of_experience': 4,
                'linkedin_url': 'https://linkedin.com/in/emilyrodriguez',
            },
            'preferences': {
                'desired_functions': ['Marketing', 'Sales'],
                'work_environments': ['Hybrid', 'Remote'],
                'employment_types': 'full-time',
                'preferred_locations': 'New York, NY, Boston, MA',
                'willing_to_relocate': False,
                'remote_only': False,
                'minimum_salary': '100k-150k',
                'industries': 'SaaS, B2B, FinTech',
                'company_size_preference': 'Startup, Mid-size',
                'actively_looking': True,
            }
        },
        {
            'username': 'david.kim',
            'email': 'david.kim@example.com',
            'first_name': 'David',
            'last_name': 'Kim',
            'profile': {
                'phone': '+1-555-0105',
                'location': 'Los Angeles, CA',
                'bio': 'Frontend developer passionate about React and modern web technologies. Love building responsive and accessible UIs.',
                'current_title': 'Frontend Developer',
                'years_of_experience': 3,
                'linkedin_url': 'https://linkedin.com/in/davidkim',
                'github_url': 'https://github.com/davidkim',
                'portfolio_url': 'https://davidkim.dev',
            },
            'preferences': {
                'desired_functions': ['Engineering'],
                'work_environments': ['Remote'],
                'employment_types': 'full-time,contract',
                'preferred_locations': 'Los Angeles, CA, Remote',
                'willing_to_relocate': False,
                'remote_only': True,
                'minimum_salary': '75k-100k',
                'industries': 'Tech, E-commerce, Media',
                'company_size_preference': 'Startup',
                'actively_looking': True,
            }
        },
        {
            'username': 'lisa.thompson',
            'email': 'lisa.thompson@example.com',
            'first_name': 'Lisa',
            'last_name': 'Thompson',
            'profile': {
                'phone': '+1-555-0106',
                'location': 'Denver, CO',
                'bio': 'Product manager with a track record of launching successful products. Strong technical background with MBA.',
                'current_title': 'Senior Product Manager',
                'years_of_experience': 8,
                'linkedin_url': 'https://linkedin.com/in/lisathompson',
            },
            'preferences': {
                'desired_functions': ['Product', 'Management'],
                'work_environments': ['Hybrid', 'Remote'],
                'employment_types': 'full-time',
                'preferred_locations': 'Denver, CO, San Francisco, CA, Remote',
                'willing_to_relocate': True,
                'remote_only': False,
                'minimum_salary': '150k-200k',
                'industries': 'SaaS, FinTech, HealthTech',
                'company_size_preference': 'Mid-size, Enterprise',
                'actively_looking': False,
            }
        },
        {
            'username': 'james.wilson',
            'email': 'james.wilson@example.com',
            'first_name': 'James',
            'last_name': 'Wilson',
            'profile': {
                'phone': '+1-555-0107',
                'location': 'Chicago, IL',
                'bio': 'DevOps engineer specializing in cloud infrastructure and CI/CD. AWS and Kubernetes expert.',
                'current_title': 'DevOps Engineer',
                'years_of_experience': 5,
                'linkedin_url': 'https://linkedin.com/in/jameswilson',
                'github_url': 'https://github.com/jameswilson',
            },
            'preferences': {
                'desired_functions': ['Engineering', 'Operations'],
                'work_environments': ['Remote', 'Hybrid'],
                'employment_types': 'full-time',
                'preferred_locations': 'Chicago, IL, Remote',
                'willing_to_relocate': False,
                'remote_only': True,
                'minimum_salary': '150k-200k',
                'industries': 'Cloud, SaaS, FinTech',
                'company_size_preference': 'Mid-size, Enterprise',
                'actively_looking': True,
            }
        },
        {
            'username': 'amanda.patel',
            'email': 'amanda.patel@example.com',
            'first_name': 'Amanda',
            'last_name': 'Patel',
            'profile': {
                'phone': '+1-555-0108',
                'location': 'Boston, MA',
                'bio': 'UX researcher passionate about understanding user needs. Expertise in qualitative and quantitative research methods.',
                'current_title': 'UX Researcher',
                'years_of_experience': 4,
                'linkedin_url': 'https://linkedin.com/in/amandapatel',
                'portfolio_url': 'https://amandapatel.com',
            },
            'preferences': {
                'desired_functions': ['Design', 'Research'],
                'work_environments': ['Hybrid', 'Remote'],
                'employment_types': 'full-time,contract',
                'preferred_locations': 'Boston, MA, New York, NY',
                'willing_to_relocate': False,
                'remote_only': False,
                'minimum_salary': '100k-150k',
                'industries': 'SaaS, Healthcare, EdTech',
                'company_size_preference': 'Mid-size, Enterprise',
                'actively_looking': True,
            }
        },
    ]

    print("Creating dummy users...")
    
    for user_data in dummy_users:
        # Check if user already exists
        if User.objects.filter(username=user_data['username']).exists():
            print(f"User {user_data['username']} already exists, skipping...")
            continue
        
        # Create user
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='testpass123',  # Same password for all test users
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        # Create profile
        profile_data = user_data['profile']
        UserProfile.objects.create(
            user=user,
            **profile_data
        )
        
        # Create job preferences
        pref_data = user_data['preferences']
        desired_functions = pref_data.pop('desired_functions', [])
        work_environments = pref_data.pop('work_environments', [])
        
        job_pref = JobPreference.objects.create(
            user=user,
            **pref_data
        )
        
        # Add many-to-many relationships
        for func_name in desired_functions:
            func_obj, _ = Function.objects.get_or_create(name=func_name)
            job_pref.desired_functions.add(func_obj)
        
        for env_name in work_environments:
            env_obj, _ = WorkEnvironment.objects.get_or_create(name=env_name)
            job_pref.work_environments.add(env_obj)
        
        print(f"Created user: {user.username} ({user.first_name} {user.last_name})")
    
    print("\nDummy users created successfully!")
    print("All users have password: testpass123")

if __name__ == '__main__':
    create_dummy_users()
