#!/bin/bash

# Navigate to backend directory
cd /Users/mustafahepekiz/Desktop/whit-release/backend

# Activate virtual environment
source ../.venv/bin/activate

# Run the management command
python manage.py create_test_user

echo "Test user creation complete!"
echo "Now try logging in with:"
echo "Email: analytics@test.com"
echo "Password: testpass123"