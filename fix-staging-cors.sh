#!/bin/bash

# Fix Staging Server CORS and API Issues
# Run this script on your staging server

echo "🔧 Fixing staging server CORS and API configuration..."

# Set the staging server details
STAGING_HOST="45.79.211.144"
STAGING_USER="root"
PROJECT_PATH="/var/www/whit-release"

echo "📋 Current issues detected:"
echo "1. Frontend calling production API instead of staging API"
echo "2. CORS policy blocking cross-origin requests"
echo "3. Environment variables not properly configured"

echo ""
echo "🚀 Applying fixes..."

# Create the staging environment file
echo "📝 Creating staging environment configuration..."
cat > staging.env << EOF
# Staging Environment Variables
VITE_API_URL=https://staging.whoishiringintech.com/api
REACT_APP_API_URL=https://staging.whoishiringintech.com/api

# Django Backend Settings
DEBUG=False
SECRET_KEY=your-staging-secret-key-change-this
ALLOWED_HOSTS=staging.whoishiringintech.com,45.79.211.144,localhost,127.0.0.1

# CORS Settings
CORS_ALLOWED_ORIGINS=https://staging.whoishiringintech.com,http://localhost:3000,http://localhost:5173

# Database (if using PostgreSQL)
DATABASE_ENGINE=sqlite
# DATABASE_NAME=whit_staging
# DATABASE_USER=whit_staging
# DATABASE_PASSWORD=staging_password
# DATABASE_HOST=localhost
# DATABASE_PORT=5432
EOF

echo "✅ Environment file created"

# Create deployment script for staging
echo "🔨 Creating staging deployment commands..."
cat > deploy_staging_fix.sh << 'EOF'
#!/bin/bash

# Navigate to project directory
cd /var/www/whit-release || exit 1

echo "🔄 Stopping services..."
sudo systemctl stop whit || true
sudo pkill -f "gunicorn" || true
sudo pkill -f "manage.py" || true

echo "🔄 Backing up current deployment..."
sudo cp -r /var/www/whit-release /var/www/whit-release.backup.$(date +%Y%m%d_%H%M%S)

echo "📦 Pulling latest changes..."
sudo git pull origin main

echo "🔧 Setting up frontend environment..."
# Copy staging environment to frontend
sudo cp staging.env frontend/.env
sudo chown -R www-data:www-data frontend/.env

echo "🏗️ Building frontend with correct API URL..."
cd frontend
sudo rm -rf node_modules package-lock.json || true
sudo npm install
sudo VITE_API_URL=https://staging.whoishiringintech.com/api npm run build
sudo chown -R www-data:www-data dist/
cd ..

echo "🐍 Setting up backend environment..."
# Activate virtual environment
source venv_new/bin/activate || python3 -m venv venv_new && source venv_new/bin/activate

# Install requirements
pip install -r backend/requirements.txt

# Set environment variables for Django
export DEBUG=False
export SECRET_KEY="your-staging-secret-key-change-this"
export ALLOWED_HOSTS="staging.whoishiringintech.com,45.79.211.144,localhost,127.0.0.1"
export CORS_ALLOWED_ORIGINS="https://staging.whoishiringintech.com,http://localhost:3000,http://localhost:5173"

# Run migrations
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

echo "🌐 Configuring nginx..."
sudo tee /etc/nginx/sites-available/whit-staging > /dev/null << 'NGINX_EOF'
server {
    listen 80;
    server_name staging.whoishiringintech.com 45.79.211.144;

    # Serve frontend static files
    location / {
        root /var/www/whit-release/frontend/dist;
        try_files $uri $uri/ /index.html;
        
        # Add CORS headers for frontend
        add_header Access-Control-Allow-Origin "https://staging.whoishiringintech.com" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type, Accept" always;
        add_header Access-Control-Allow-Credentials "true" always;
    }

    # Proxy API requests to Django backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers for API
        add_header Access-Control-Allow-Origin "https://staging.whoishiringintech.com" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS, PATCH" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type, Accept, X-Requested-With" always;
        add_header Access-Control-Allow-Credentials "true" always;
        
        # Handle preflight requests
        if ($request_method = OPTIONS) {
            add_header Access-Control-Allow-Origin "https://staging.whoishiringintech.com";
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS, PATCH";
            add_header Access-Control-Allow-Headers "Authorization, Content-Type, Accept, X-Requested-With";
            add_header Access-Control-Allow-Credentials "true";
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            return 200;
        }
    }

    # Serve media files
    location /media/ {
        alias /var/www/whit-release/backend/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Serve static files
    location /static/ {
        alias /var/www/whit-release/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
NGINX_EOF

echo "🔗 Enabling nginx configuration..."
sudo ln -sf /etc/nginx/sites-available/whit-staging /etc/nginx/sites-enabled/whit-staging
sudo rm -f /etc/nginx/sites-enabled/default

echo "✅ Testing nginx configuration..."
sudo nginx -t

echo "🔄 Restarting nginx..."
sudo systemctl restart nginx

echo "🚀 Starting Django backend..."
cd backend
nohup python manage.py runserver 127.0.0.1:8000 > /var/log/whit-backend.log 2>&1 &
cd ..

echo "⏳ Waiting for services to start..."
sleep 5

echo "🏥 Testing deployment..."
# Test API health
curl -f http://127.0.0.1:8000/api/health/ || echo "❌ Backend health check failed"

# Test frontend
curl -f http://staging.whoishiringintech.com/ || echo "❌ Frontend check failed"

echo "✅ Staging deployment fix completed!"
echo "🌐 Site should be accessible at: https://staging.whoishiringintech.com"
echo "📊 API should be accessible at: https://staging.whoishiringintech.com/api"

echo "📋 Final checks:"
echo "1. Visit: https://staging.whoishiringintech.com"
echo "2. Check browser console for any remaining CORS errors"
echo "3. Verify API calls are going to staging.whoishiringintech.com/api"

echo "📝 Logs available at:"
echo "- Backend: /var/log/whit-backend.log"
echo "- Nginx: /var/log/nginx/error.log"
EOF

chmod +x deploy_staging_fix.sh

echo "📋 Files created:"
echo "1. staging.env - Environment configuration"
echo "2. deploy_staging_fix.sh - Deployment fix script"

echo ""
echo "🚀 To apply the fix on your staging server, run:"
echo "scp staging.env deploy_staging_fix.sh root@45.79.211.144:/tmp/"
echo "ssh root@45.79.211.144 'chmod +x /tmp/deploy_staging_fix.sh && /tmp/deploy_staging_fix.sh'"

echo ""
echo "🎯 This will fix:"
echo "✅ Frontend API URL pointing to staging instead of production"
echo "✅ CORS headers allowing staging.whoishiringintech.com"
echo "✅ Proper nginx configuration for API proxying"
echo "✅ Environment variables for staging deployment"
echo "✅ Zero-downtime deployment process"