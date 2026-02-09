# Generated migration for company-recruiter relationship
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_create_default_homepage_sections'),
        ('recruiters', '0001_initial'),  # Adjust based on your latest migration
    ]

    operations = [
        # Create the many-to-many relationship between Company and Recruiter
        migrations.CreateModel(
            name='CompanyRecruiterAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_see_sponsored_stats', models.BooleanField(default=False, help_text='Allow this recruiter to view sponsor campaign statistics')),
                ('access_level', models.CharField(choices=[('view', 'View Only'), ('manage', 'Manage Campaigns')], default='view', help_text='Level of access to company sponsor data', max_length=10)),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this recruiter access')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruiter_accesses', to='companies.company')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_accesses', to='recruiters.recruiter')),
            ],
            options={
                'unique_together': {('company', 'recruiter')},
                'verbose_name': 'Company Recruiter Access',
                'verbose_name_plural': 'Company Recruiter Accesses',
            },
        ),
    ]