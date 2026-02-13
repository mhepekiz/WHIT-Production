"""
Management command to create dummy job openings for testing.
Assigns jobs to existing recruiters, or creates a test recruiter if none exist.
"""
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from recruiters.models import Recruiter, RecruiterPackage, JobOpening


DUMMY_JOBS = [
    {
        "title": "Senior Frontend Engineer",
        "description": "We're looking for an experienced frontend engineer to build modern, responsive web applications using React and TypeScript. You'll work closely with our design and backend teams to deliver polished user experiences.",
        "requirements": "5+ years of experience with JavaScript/TypeScript. Strong proficiency in React and state management libraries. Experience with CSS-in-JS or Tailwind CSS. Familiarity with testing frameworks (Jest, Cypress).",
        "responsibilities": "Build and maintain frontend features. Collaborate with designers on UI/UX improvements. Write unit and integration tests. Mentor junior developers. Participate in code reviews.",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 140000,
        "salary_max": 185000,
        "location": "San Francisco, CA",
        "city": "San Francisco",
        "state": "California",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["React", "TypeScript", "CSS", "JavaScript", "GraphQL"],
        "department": "Engineering",
    },
    {
        "title": "Backend Software Engineer",
        "description": "Join our backend team to design and build scalable APIs and microservices. You'll work with Python and Django to power our platform serving millions of users.",
        "requirements": "3+ years of backend development experience. Proficiency in Python and Django or Flask. Experience with PostgreSQL and Redis. Understanding of RESTful API design.",
        "responsibilities": "Design and implement APIs. Optimize database queries and performance. Maintain CI/CD pipelines. Write documentation for internal and external APIs.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 120000,
        "salary_max": 160000,
        "location": "New York, NY",
        "city": "New York",
        "state": "New York",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["Python", "Django", "PostgreSQL", "REST APIs", "Docker"],
        "department": "Engineering",
    },
    {
        "title": "DevOps Engineer",
        "description": "We need a DevOps engineer to manage our cloud infrastructure, improve deployment pipelines, and ensure system reliability at scale.",
        "requirements": "3+ years of DevOps or SRE experience. Strong knowledge of AWS or GCP. Proficiency with Terraform, Docker, and Kubernetes. Experience with monitoring tools (Datadog, Prometheus).",
        "responsibilities": "Manage and optimize cloud infrastructure. Automate deployment and provisioning. Monitor system health and respond to incidents. Implement security best practices.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 130000,
        "salary_max": 170000,
        "location": "Austin, TX",
        "city": "Austin",
        "state": "Texas",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["AWS", "Terraform", "Docker", "Kubernetes", "Linux", "CI/CD"],
        "department": "Infrastructure",
    },
    {
        "title": "Product Designer",
        "description": "We're hiring a product designer to shape the user experience of our platform. You'll conduct research, create prototypes, and collaborate with engineering to deliver delightful products.",
        "requirements": "4+ years of product design experience. Expert in Figma or Sketch. Portfolio demonstrating strong interaction and visual design skills. Experience with user research and usability testing.",
        "responsibilities": "Conduct user research and synthesize findings. Design wireframes, prototypes, and high-fidelity mockups. Work closely with product managers and engineers. Maintain and evolve our design system.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 110000,
        "salary_max": 150000,
        "location": "Seattle, WA",
        "city": "Seattle",
        "state": "Washington",
        "country": "United States",
        "remote_allowed": False,
        "skills_required": ["Figma", "UI/UX Design", "Prototyping", "User Research", "Design Systems"],
        "department": "Design",
    },
    {
        "title": "Data Scientist",
        "description": "Join our data team to build predictive models and derive actionable insights from large datasets. You'll work on recommendation systems, fraud detection, and business analytics.",
        "requirements": "3+ years of data science experience. Strong proficiency in Python (pandas, scikit-learn, TensorFlow or PyTorch). Experience with SQL and data warehousing. Master's degree in a quantitative field preferred.",
        "responsibilities": "Build and deploy machine learning models. Analyze large datasets to identify trends. Present findings to stakeholders. Collaborate with engineering to productionize models.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 135000,
        "salary_max": 175000,
        "location": "Boston, MA",
        "city": "Boston",
        "state": "Massachusetts",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["Python", "Machine Learning", "SQL", "TensorFlow", "Statistics"],
        "department": "Data",
    },
    {
        "title": "Engineering Manager",
        "description": "Lead a team of 8-10 engineers building our core platform. You'll balance technical leadership with people management to deliver high-quality software on time.",
        "requirements": "7+ years of software engineering experience. 2+ years managing engineering teams. Strong communication and project planning skills. Technical depth in at least one major language/framework.",
        "responsibilities": "Manage and mentor a team of engineers. Set technical direction and priorities. Run sprint planning and retrospectives. Partner with product on roadmap planning. Conduct 1:1s and performance reviews.",
        "employment_type": "full-time",
        "experience_level": "lead",
        "salary_min": 180000,
        "salary_max": 230000,
        "location": "San Francisco, CA",
        "city": "San Francisco",
        "state": "California",
        "country": "United States",
        "remote_allowed": False,
        "skills_required": ["Leadership", "Agile", "System Design", "Python", "JavaScript"],
        "department": "Engineering",
    },
    {
        "title": "Junior Web Developer",
        "description": "Great opportunity for a motivated junior developer to grow their skills. You'll work on real features from day one with mentorship from senior engineers.",
        "requirements": "0-2 years of experience. Familiarity with HTML, CSS, and JavaScript. Willingness to learn modern frameworks (React, Vue). Computer science degree or bootcamp graduate.",
        "responsibilities": "Implement frontend features under guidance. Fix bugs and improve existing code. Write unit tests. Participate in code reviews and team meetings.",
        "employment_type": "full-time",
        "experience_level": "entry",
        "salary_min": 65000,
        "salary_max": 85000,
        "location": "Chicago, IL",
        "city": "Chicago",
        "state": "Illinois",
        "country": "United States",
        "remote_allowed": False,
        "skills_required": ["HTML", "CSS", "JavaScript", "Git"],
        "department": "Engineering",
    },
    {
        "title": "Mobile Developer (iOS)",
        "description": "Build beautiful and performant iOS applications with Swift and SwiftUI. Join a small, focused team shipping features weekly to millions of users.",
        "requirements": "3+ years of iOS development. Proficiency in Swift and SwiftUI. Experience with Core Data, Combine, and networking. Published apps on the App Store.",
        "responsibilities": "Develop new iOS features. Optimize app performance and battery usage. Integrate with backend APIs. Review pull requests and maintain code quality.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 125000,
        "salary_max": 165000,
        "location": "Los Angeles, CA",
        "city": "Los Angeles",
        "state": "California",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["Swift", "SwiftUI", "iOS", "Xcode", "Core Data"],
        "department": "Mobile",
    },
    {
        "title": "QA Automation Engineer",
        "description": "Own the quality of our product by building and maintaining automated test suites. Work across web and API testing to ensure rock-solid releases.",
        "requirements": "3+ years of QA experience. Strong automation skills with Selenium, Playwright, or Cypress. Experience with API testing (Postman, REST Assured). Familiarity with CI/CD integration.",
        "responsibilities": "Design and implement automated test plans. Maintain CI/CD test pipelines. Report and track defects. Collaborate with developers on testability improvements.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 100000,
        "salary_max": 140000,
        "location": "Denver, CO",
        "city": "Denver",
        "state": "Colorado",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["Selenium", "Playwright", "Python", "CI/CD", "API Testing"],
        "department": "Quality",
    },
    {
        "title": "Cloud Solutions Architect",
        "description": "Design and implement cloud-native architectures for enterprise clients. You'll evaluate requirements, propose solutions, and guide teams through implementation.",
        "requirements": "7+ years of software/infrastructure experience. AWS Solutions Architect certification preferred. Deep knowledge of microservices, serverless, and containerization. Excellent communication skills.",
        "responsibilities": "Design scalable cloud architectures. Advise clients on best practices. Create architecture documentation and diagrams. Lead proof-of-concept implementations.",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 160000,
        "salary_max": 210000,
        "location": "Remote",
        "city": "Remote",
        "state": "",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["AWS", "Azure", "Microservices", "Serverless", "Architecture"],
        "department": "Engineering",
    },
    {
        "title": "Technical Writer",
        "description": "Create clear, concise documentation for our developer platform. You'll write API references, tutorials, and guides that help developers integrate our products.",
        "requirements": "2+ years of technical writing experience. Ability to understand and document APIs. Familiarity with Markdown, Git, and docs-as-code workflows. Strong written English.",
        "responsibilities": "Write and maintain API documentation. Create getting-started guides and tutorials. Review and edit content from engineering teams. Manage documentation site updates.",
        "employment_type": "contract",
        "experience_level": "mid",
        "salary_min": 80000,
        "salary_max": 110000,
        "location": "Portland, OR",
        "city": "Portland",
        "state": "Oregon",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["Technical Writing", "API Documentation", "Markdown", "Git"],
        "department": "Developer Relations",
    },
    {
        "title": "Machine Learning Engineer",
        "description": "Build production ML pipelines that power our recommendation engine. You'll bridge the gap between data science experiments and scalable production systems.",
        "requirements": "4+ years of ML engineering experience. Strong Python skills. Experience with MLOps tools (MLflow, Kubeflow, SageMaker). Knowledge of distributed computing (Spark, Dask).",
        "responsibilities": "Build and maintain ML training and serving pipelines. Optimize model inference latency. Implement A/B testing frameworks. Monitor model performance in production.",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 155000,
        "salary_max": 200000,
        "location": "San Jose, CA",
        "city": "San Jose",
        "state": "California",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["Python", "MLOps", "TensorFlow", "Kubernetes", "Spark"],
        "department": "AI/ML",
    },
    {
        "title": "Security Engineer",
        "description": "Protect our platform and users by identifying vulnerabilities, implementing security controls, and responding to threats. Join a fast-growing security team.",
        "requirements": "3+ years of security engineering experience. Knowledge of OWASP Top 10 and common attack vectors. Experience with security tools (Burp Suite, Nessus). Familiarity with cloud security (AWS/GCP).",
        "responsibilities": "Conduct security assessments and penetration tests. Implement security monitoring and alerting. Review code for security vulnerabilities. Develop security policies and procedures.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 130000,
        "salary_max": 170000,
        "location": "Washington, DC",
        "city": "Washington",
        "state": "District of Columbia",
        "country": "United States",
        "remote_allowed": False,
        "skills_required": ["Security", "Penetration Testing", "OWASP", "AWS Security", "Python"],
        "department": "Security",
    },
    {
        "title": "Full Stack Developer",
        "description": "Work across the entire stack to build features end-to-end. Our tech stack includes React, Node.js, and PostgreSQL running on AWS.",
        "requirements": "3+ years of full stack experience. Proficiency in React and Node.js. Experience with SQL databases. Understanding of cloud deployment.",
        "responsibilities": "Build full-stack features from design to deployment. Write clean, tested code. Participate in architecture discussions. On-call rotation for production issues.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 115000,
        "salary_max": 155000,
        "location": "Miami, FL",
        "city": "Miami",
        "state": "Florida",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["React", "Node.js", "PostgreSQL", "AWS", "TypeScript"],
        "department": "Engineering",
    },
    {
        "title": "VP of Engineering",
        "description": "Lead our engineering organization of 40+ engineers across multiple teams. Set technical strategy, build culture, and drive execution for our next phase of growth.",
        "requirements": "12+ years of engineering experience. 5+ years in engineering leadership. Experience scaling teams from 20 to 100+. Track record of delivering complex projects. MBA or advanced technical degree preferred.",
        "responsibilities": "Set engineering vision and strategy. Hire and develop engineering leaders. Manage engineering budget and resource allocation. Report to CTO on team performance and roadmap.",
        "employment_type": "full-time",
        "experience_level": "executive",
        "salary_min": 250000,
        "salary_max": 350000,
        "location": "San Francisco, CA",
        "city": "San Francisco",
        "state": "California",
        "country": "United States",
        "remote_allowed": False,
        "skills_required": ["Leadership", "Strategy", "Team Building", "System Design", "Agile"],
        "department": "Engineering",
    },
    {
        "title": "Part-Time React Developer",
        "description": "Looking for a React developer to work 20 hours/week on our customer-facing dashboard. Flexible schedule, async-first culture.",
        "requirements": "2+ years of React experience. Comfortable working independently. Good communication skills for async collaboration.",
        "responsibilities": "Build dashboard components. Fix UI bugs. Improve performance. Weekly check-in with the team lead.",
        "employment_type": "part-time",
        "experience_level": "mid",
        "salary_min": 50000,
        "salary_max": 70000,
        "location": "Remote",
        "city": "Remote",
        "state": "",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["React", "JavaScript", "CSS", "REST APIs"],
        "department": "Engineering",
    },
    {
        "title": "Software Engineering Intern",
        "description": "12-week summer internship program. Work on a real project with mentorship from senior engineers. Potential for full-time offer at the end.",
        "requirements": "Currently pursuing a CS degree (junior or senior). Basic knowledge of at least one programming language. Passion for building software.",
        "responsibilities": "Work on an intern project with real impact. Attend tech talks and lunch-and-learns. Present your project to the company at the end of the internship.",
        "employment_type": "internship",
        "experience_level": "entry",
        "salary_min": 35000,
        "salary_max": 45000,
        "location": "New York, NY",
        "city": "New York",
        "state": "New York",
        "country": "United States",
        "remote_allowed": False,
        "skills_required": ["Python", "JavaScript", "Git", "Problem Solving"],
        "department": "Engineering",
    },
    {
        "title": "Platform Engineer",
        "description": "Build the internal developer platform that powers our engineering teams. Focus on developer experience, CI/CD, and infrastructure abstraction.",
        "requirements": "4+ years of platform or infrastructure engineering. Experience with Kubernetes, Helm, and ArgoCD. Strong Go or Python skills. Understanding of developer workflows.",
        "responsibilities": "Build and maintain internal developer tools. Improve CI/CD pipeline performance. Create self-service infrastructure for developers. Document platform capabilities.",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 150000,
        "salary_max": 190000,
        "location": "Seattle, WA",
        "city": "Seattle",
        "state": "Washington",
        "country": "United States",
        "remote_allowed": True,
        "skills_required": ["Kubernetes", "Go", "Python", "ArgoCD", "Terraform"],
        "department": "Platform",
    },
    {
        "title": "Frontend Developer (Vue.js)",
        "description": "Join our team building a next-generation analytics dashboard using Vue 3 and TypeScript. Great opportunity to work on data visualization and real-time features.",
        "requirements": "2+ years with Vue.js. Experience with TypeScript. Familiarity with charting libraries (D3, Chart.js, ECharts). Understanding of WebSocket and real-time data.",
        "responsibilities": "Build interactive data visualizations. Implement real-time dashboard features. Optimize rendering performance. Collaborate on component library.",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 110000,
        "salary_max": 145000,
        "location": "Toronto, ON",
        "city": "Toronto",
        "state": "Ontario",
        "country": "Canada",
        "remote_allowed": True,
        "skills_required": ["Vue.js", "TypeScript", "D3.js", "WebSocket", "CSS"],
        "department": "Engineering",
    },
    {
        "title": "Site Reliability Engineer",
        "description": "Ensure 99.99% uptime for our platform. Build resilient systems, automate operations, and improve observability across our microservices architecture.",
        "requirements": "4+ years of SRE or DevOps experience. Deep Linux and networking knowledge. Experience with observability tools (Grafana, Prometheus, ELK). Strong scripting (Bash, Python).",
        "responsibilities": "Manage production infrastructure. Define and track SLOs/SLIs. Build runbooks and automate incident response. Participate in on-call rotation.",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 145000,
        "salary_max": 190000,
        "location": "London",
        "city": "London",
        "state": "",
        "country": "United Kingdom",
        "remote_allowed": False,
        "skills_required": ["Linux", "Prometheus", "Grafana", "Python", "Kubernetes"],
        "department": "Infrastructure",
    },
]


class Command(BaseCommand):
    help = 'Create dummy job openings for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing job openings before creating new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = JobOpening.objects.count()
            JobOpening.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing job openings'))

        # Get or create a recruiter to own the jobs
        recruiters = list(Recruiter.objects.filter(is_active=True))

        if not recruiters:
            self.stdout.write('No recruiters found. Creating a test recruiter...')
            user, _ = User.objects.get_or_create(
                username='test_recruiter',
                defaults={
                    'email': 'recruiter@test.com',
                    'first_name': 'Test',
                    'last_name': 'Recruiter',
                }
            )
            user.set_password('testpass123')
            user.save()

            package = RecruiterPackage.objects.first()
            if not package:
                package = RecruiterPackage.objects.create(
                    name='Basic',
                    monthly_job_openings=50,
                    monthly_candidate_searches=100,
                    monthly_messages=50,
                    messaging_enabled=True,
                    price=0,
                )

            recruiter, _ = Recruiter.objects.get_or_create(
                user=user,
                defaults={
                    'package': package,
                    'company_name': 'TechCorp Inc.',
                    'company_website': 'https://techcorp.example.com',
                    'contact_email': 'recruiter@test.com',
                    'city': 'San Francisco',
                    'state': 'California',
                    'country': 'United States',
                    'is_verified': True,
                }
            )
            recruiters = [recruiter]

        now = timezone.now()
        created_count = 0
        statuses = ['active', 'active', 'active', 'active', 'draft']  # 80% active, 20% draft

        for job_data in DUMMY_JOBS:
            recruiter = random.choice(recruiters)
            status = random.choice(statuses)
            days_ago = random.randint(1, 60)
            created_date = now - timedelta(days=days_ago)
            deadline = now + timedelta(days=random.randint(14, 90))

            job = JobOpening.objects.create(
                recruiter=recruiter,
                title=job_data['title'],
                description=job_data['description'],
                requirements=job_data['requirements'],
                responsibilities=job_data.get('responsibilities', ''),
                employment_type=job_data['employment_type'],
                experience_level=job_data['experience_level'],
                salary_min=job_data.get('salary_min'),
                salary_max=job_data.get('salary_max'),
                salary_currency='USD',
                location=job_data['location'],
                city=job_data['city'],
                state=job_data.get('state', ''),
                country=job_data['country'],
                remote_allowed=job_data.get('remote_allowed', False),
                skills_required=job_data.get('skills_required', []),
                department=job_data.get('department', ''),
                status=status,
                application_deadline=deadline.date(),
                application_email=recruiter.contact_email,
                views_count=random.randint(10, 500),
                applications_count=random.randint(0, 30),
            )

            # Backdate created_at
            JobOpening.objects.filter(pk=job.pk).update(
                created_at=created_date,
                published_at=created_date if status == 'active' else None,
            )

            created_count += 1
            self.stdout.write(f'  Created: {job.title} ({status}) → {recruiter.company_name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully created {created_count} dummy job openings'
        ))
