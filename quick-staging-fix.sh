#!/bin/bash

echo "🚀 Quick Staging Fix - Alternative Deployment Methods"
echo "======================================================"
echo ""

# Method 1: Upload the corrected dist folder directly
echo "Method 1: Upload local build to server"
echo "--------------------------------------"
echo "From your local machine, run:"
echo "  scp -r frontend/dist/* root@45.79.211.144:/var/www/whit/frontend/dist/"
echo ""

# Method 2: Check what's on the server first
echo "Method 2: Check current server setup"
echo "------------------------------------"
echo "On the server, run these commands to investigate:"
echo "  ls -la /var/www/whit/"
echo "  ls -la /var/www/whit/frontend/"
echo "  ls -la /var/www/whit/frontend/dist/"
echo ""

# Method 3: Initialize git repository on server
echo "Method 3: Initialize git on server (if you want git-based deployments)"
echo "----------------------------------------------------------------------"
echo "On the server:"
echo "  cd /var/www/whit"
echo "  git init"
echo "  git remote add origin YOUR_GIT_REPO_URL"
echo "  git pull origin main"
echo ""

# Method 4: Direct frontend rebuild on server
echo "Method 4: Build frontend directly on server (if npm/node available)"
echo "--------------------------------------------------------------------"
echo "On the server:"
echo "  cd /var/www/whit/frontend"
echo "  npm install  # if not already done"
echo "  npm run build"
echo ""

echo "Fix nginx paths and restart:"
echo "  sudo nano /etc/nginx/sites-available/default"
echo "  # Change /Users/mustafahepekiz/... paths to /var/www/whit/..."
echo "  sudo systemctl restart nginx"
echo ""

echo "🔍 Recommended: Start with Method 2 to see what's currently there"