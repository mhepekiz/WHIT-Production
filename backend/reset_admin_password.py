#!/usr/bin/env python3
"""
Reset admin password for staging server access
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()

from django.contrib.auth.models import User

def reset_admin_password():
    """Reset admin user password"""
    try:
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@whoishiringintech.com',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if created:
            print("Created new admin user")
        else:
            print("Found existing admin user")
        
        # Set password to "admin123" for demo
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True 
        admin_user.is_active = True
        admin_user.save()
        
        print(f"Admin user: {admin_user.username}")
        print(f"Password: admin123")
        print(f"Is superuser: {admin_user.is_superuser}")
        print(f"Is staff: {admin_user.is_staff}")
        print(f"Is active: {admin_user.is_active}")
        print("\nAdmin password reset successfully!")
        print("You can now login at /admin/ with username: admin, password: admin123")
        
    except Exception as e:
        print(f"Error resetting admin password: {e}")

if __name__ == "__main__":
    reset_admin_password()