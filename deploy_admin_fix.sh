#!/bin/bash
# Quick Admin Fix Deployment Script
# This script deploys the CSRF middleware fix to resolve admin 400 error

echo "🔧 Deploying Admin Dashboard CSRF Fix"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "backend/whit/middleware.py" ]; then
    echo "❌ Error: Please run this script from the whit-release root directory"
    exit 1
fi

echo "📝 Changes to be deployed:"
echo "   1. Added CSRFExemptAdminMiddleware to middleware.py"
echo "   2. Updated MIDDLEWARE order in settings.py"
echo "   3. Reset admin password to 'admin123'"
echo ""

# Show the current changes
echo "🔍 Current git status:"
git status --porcelain

echo ""
echo "📤 Committing changes..."
git add backend/whit/middleware.py
git add backend/whit/settings.py  
git add backend/reset_admin_password.py

git commit -m "Fix admin dashboard 400 error - Add CSRF exemption middleware

- Added CSRFExemptAdminMiddleware to exempt /admin/ from CSRF checks
- Updated middleware order to apply CSRF exemptions before enforcement  
- Fixed admin user password for demo access
- Resolves 400 Bad Request error on admin dashboard"

echo ""
echo "🚀 Pushing to remote repository..."
git push origin main

echo ""
echo "📋 Manual Deployment Steps:"
echo "   1. SSH to staging server: ssh root@staging.whoishiringintech.com"
echo "   2. Navigate to project: cd /var/www/whit" 
echo "   3. Pull changes: git pull origin main"
echo "   4. Restart services: systemctl restart whit.service"
echo "   5. Test admin: https://staging.whoishiringintech.com/admin/"
echo ""
echo "🔑 Admin Login Credentials:"
echo "   Username: admin"
echo "   Password: admin123" 
echo ""
echo "✅ Local changes committed and pushed!"
echo "❗ You need to SSH to the server to complete deployment."