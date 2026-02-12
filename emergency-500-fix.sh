#!/bin/bash

echo "🚨 URGENT: Fixing 500 Error - Staging Deployment Fix"
echo "===================================================="

# The issue is likely that nginx is serving files correctly to /var/www/whit-frontend
# but when it falls back to Django (@django location), Django is returning 500
# Since our API endpoints work (companies=200, api root=200), Django is running
# but seems to fail for frontend fallback routes

echo "📊 Current Status:"
echo "- Frontend files deployed to: /var/www/whit-frontend (likely correct)"
echo "- API endpoints working (companies=200, api/=200)" 
echo "- Frontend route fallback to Django = 500 error"

echo -e "\n🔧 Attempting remote fixes..."

# Test if we can trigger a service restart through the health check endpoint
echo "1. Attempting to wake up Django service..."
curl -v https://staging.whoishiringintech.com/api/companies/ >/dev/null 2>&1

# Test if static files exist by trying to access known files
echo "2. Testing if frontend files were deployed..."
echo -n "   - Testing index.html: "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/index.html

echo -n "   - Testing favicon: "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/favicon.ico

# Test if Django can handle root requests
echo "3. Testing Django's ability to handle root requests..."
echo -n "   - Django API root: "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/api/

echo -n "   - Django admin panel: "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/admin/

echo -e "\n💡 Root Cause Analysis:"
echo "The 500 error happens when:"
echo "1. Someone visits https://staging.whoishiringintech.com/"
echo "2. Nginx tries to serve from /var/www/whit-frontend/index.html"
echo "3. If that fails, it falls back to @django location (proxy to Django)"
echo "4. Django at port 8003 returns 500 for frontend routes"

echo -e "\n🚑 Emergency Fix Suggestions:"
echo "A) Frontend files missing: Build didn't deploy correctly"
echo "B) Django 500 on root: Django app needs ALLOWED_HOSTS or URL config fix"
echo "C) Permission issue: Files exist but nginx can't read them"

# Try one more diagnostic - check if we can bypass nginx completely
echo -e "\n🧪 Testing direct Django connection (bypassing nginx):"
echo "If Django is on port 8003 like nginx config suggests:"

# This won't work externally but shows the command
echo "   Command to test locally: curl http://localhost:8003/"

echo -e "\n⚡ IMMEDIATE ACTION ITEMS:"
echo "1. SSH to server and run: systemctl restart whit"  
echo "2. Check: ls -la /var/www/whit-frontend/"
echo "3. Check: systemctl status whit"
echo "4. If Django down: sudo -u www-data /var/www/whit/backend/venv/bin/gunicorn --check-config"
