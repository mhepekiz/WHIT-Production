# Generated manually for admin-managed static pages.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0022_add_jobs_per_page_to_sitesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, help_text='URL slug. Leave blank to generate from title.', max_length=220, unique=True)),
                ('content', models.TextField(help_text='Page body. Basic HTML is supported.')),
                ('excerpt', models.CharField(blank=True, help_text='Optional short summary for internal reference or future previews.', max_length=300)),
                ('show_in_top_nav', models.BooleanField(default=False, help_text='Show this page in the top navigation.')),
                ('show_in_footer_nav', models.BooleanField(default=False, help_text='Show this page in the footer navigation.')),
                ('is_published', models.BooleanField(default=True, help_text='Only published pages are visible on the public site.')),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower numbers appear first in navigation.')),
                ('meta_title', models.CharField(blank=True, max_length=200)),
                ('meta_description', models.CharField(blank=True, max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Static Page',
                'verbose_name_plural': 'Static Pages',
                'ordering': ['order', 'title'],
            },
        ),
        migrations.AddIndex(
            model_name='staticpage',
            index=models.Index(fields=['slug'], name='companies_s_slug_a5c103_idx'),
        ),
        migrations.AddIndex(
            model_name='staticpage',
            index=models.Index(fields=['is_published', 'show_in_top_nav', 'order'], name='companies_s_is_publ_3b9aeb_idx'),
        ),
        migrations.AddIndex(
            model_name='staticpage',
            index=models.Index(fields=['is_published', 'show_in_footer_nav', 'order'], name='companies_s_is_publ_c08b1b_idx'),
        ),
    ]
