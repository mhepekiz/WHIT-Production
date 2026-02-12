#!/bin/bash

# Deploy Frontend to Staging Server
# Run this on the staging server at 45.79.211.144

echo "🚀 Deploying frontend to staging server..."

# Navigate to the project directory
cd /var/www/whit

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Build frontend with staging environment
echo "🔨 Building frontend..."
cd frontend
npm run build

# Copy built files to nginx directory  
echo "📂 Updating served files..."
sudo cp -r dist/* /var/www/whit/frontend/dist/

# Fix nginx configuration paths (if needed)
echo "🔧 Checking nginx configuration..."
if grep -q "/Users/mustafahepekiz" /etc/nginx/sites-available/default 2>/dev/null || grep -q "/Users/mustafahepekiz" /etc/nginx/nginx.conf 2>/dev/null; then
    echo "⚠️  Found incorrect local paths in nginx config. Please update manually:"
    echo "   /static/ should point to: /var/www/whit/backend/staticfiles/"
    echo "   /media/ should point to: /var/www/whit/backend/media/"
fi

# Restart nginx to ensure fresh files are served
echo "🔄 Restarting nginx..."
sudo systemctl restart nginx

# Verify the deployment
echo "✅ Checking if staging site is accessible..."
curl -I https://staging.whoishiringintech.com/

echo "🎉 Frontend deployment complete!"
echo "Please check https://staging.whoishiringintech.com/ in your browser"
echo "Clear browser cache if you still see old content"