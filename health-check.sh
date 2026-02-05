#!/bin/bash

# Health check script for WHIT Django application
# This script verifies that Django can start properly before Gunicorn runs

set -e

BACKEND_DIR="/var/www/whit/backend"
VENV_PYTHON="$BACKEND_DIR/venv/bin/python"
MANAGE_PY="$BACKEND_DIR/manage.py"

echo "🔍 Running WHIT Django health checks..."

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found: $BACKEND_DIR"
    exit 1
fi

echo "✅ Backend directory exists"

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment Python not found: $VENV_PYTHON"
    exit 1
fi

echo "✅ Virtual environment exists"

# Check if manage.py exists
if [ ! -f "$MANAGE_PY" ]; then
    echo "❌ manage.py not found: $MANAGE_PY"
    exit 1
fi

echo "✅ manage.py exists"

# Navigate to backend directory
cd "$BACKEND_DIR" || exit 1

# Check if .env file exists (optional but recommended for production)
if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not found (will use default settings)"
fi

# Test Django check command
echo "Running Django system checks..."
if sudo -u www-data "$VENV_PYTHON" "$MANAGE_PY" check --deploy 2>&1 | tee /tmp/django-check.log; then
    echo "✅ Django system checks passed"
else
    echo "❌ Django system checks failed"
    cat /tmp/django-check.log
    exit 1
fi

# Test database connection
echo "Testing database connection..."
if sudo -u www-data "$VENV_PYTHON" "$MANAGE_PY" showmigrations --list > /dev/null 2>&1; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed"
    exit 1
fi

# Check if migrations are applied
echo "Checking migration status..."
UNAPPLIED=$(sudo -u www-data "$VENV_PYTHON" "$MANAGE_PY" showmigrations --plan | grep -c "\[ \]" || true)
if [ "$UNAPPLIED" -gt 0 ]; then
    echo "⚠️  Warning: $UNAPPLIED unapplied migrations found"
    echo "Run: python manage.py migrate"
else
    echo "✅ All migrations applied"
fi

# Test WSGI application
echo "Testing WSGI application..."
if sudo -u www-data "$VENV_PYTHON" -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
print('WSGI application loaded successfully')
" 2>&1; then
    echo "✅ WSGI application loads correctly"
else
    echo "❌ WSGI application failed to load"
    exit 1
fi

# Check if Gunicorn is installed
echo "Checking Gunicorn installation..."
if sudo -u www-data "$BACKEND_DIR/venv/bin/gunicorn" --version > /dev/null 2>&1; then
    GUNICORN_VERSION=$(sudo -u www-data "$BACKEND_DIR/venv/bin/gunicorn" --version)
    echo "✅ Gunicorn installed: $GUNICORN_VERSION"
else
    echo "❌ Gunicorn not found in virtual environment"
    exit 1
fi

echo ""
echo "✅ All health checks passed!"
echo "Django application is ready to be served by Gunicorn"
exit 0
