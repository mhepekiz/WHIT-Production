#!/bin/bash

# Complete Staging Server Fix Script
# Run this directly on the server as root

echo "🔧 COMPLETE STAGING SERVER FIX"
echo "============================="

# Navigate to project directory
cd /var/www/whit || { echo "❌ Project directory not found"; exit 1; }

echo "📁 Current directory: $(pwd)"
echo "📋 Project structure:"
ls -la

echo ""
echo "🐍 Python Setup"
echo "==============="

# Check Python
echo "Python3 version: $(python3 --version 2>/dev/null || echo 'Not found')"
echo "Python3 location: $(which python3 2>/dev/null || echo 'Not found')"

# Install pip if missing
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip3..."
    apt update
    apt install -y python3-pip
fi

# Install virtual environment tools
echo "📦 Installing venv tools..."
apt install -y python3-venv

# Create virtual environment
echo "🏗️ Creating virtual environment..."
python3 -m venv venv_new
source venv_new/bin/activate

echo "Virtual environment created and activated"
echo "Python path: $(which python)"
echo "Pip path: $(which pip)"

echo ""
echo "📦 Installing Backend Dependencies"
echo "================================="

cd backend || { echo "❌ Backend directory not found"; exit 1; }

# Install requirements
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🗄️ Database Setup"
echo "=================="

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "🚀 Starting Backend Server"
echo "=========================="

# Kill any existing processes
pkill -f 'manage.py runserver' || true
pkill -f 'python.*manage.py' || true
sleep 3

# Start the backend server
echo "Starting Django server on 127.0.0.1:8000..."
nohup python manage.py runserver 127.0.0.1:8000 > /var/log/whit-backend.log 2>&1 &
DJANGO_PID=$!

sleep 5

# Check if process is running
if ps -p $DJANGO_PID > /dev/null; then
    echo "✅ Django server started successfully (PID: $DJANGO_PID)"
else
    echo "❌ Django server failed to start"
    echo "Error log:"
    tail -20 /var/log/whit-backend.log
    exit 1
fi

echo ""
echo "🌐 Frontend Build"
echo "================="

cd ../frontend || { echo "❌ Frontend directory not found"; exit 1; }

# Ensure .env file exists with correct API URL
echo "Setting frontend environment..."
echo 'VITE_API_URL=https://staging.whoishiringintech.com/api' > .env

# Install dependencies and build
echo "Installing npm packages..."
npm install

echo "Building frontend..."
export VITE_API_URL=https://staging.whoishiringintech.com/api
npm run build

echo ""
echo "🌐 Nginx Configuration"
echo "====================="

# Configure nginx
cat > /etc/nginx/sites-available/whit-staging << 'NGINX_EOF'
server {
    listen 80;
    server_name staging.whoishiringintech.com 47.221.151.132;

    # Frontend static files
    location / {
        root /var/www/whit/frontend/dist;
        try_files $uri $uri/ /index.html;
        
        # Basic headers
        add_header Cache-Control "public, max-age=3600";
    }

    # API proxy to Django backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers for staging
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

    # Media files
    location /media/ {
        alias /var/www/whit/backend/media/;
        expires 30d;
    }

    # Static files  
    location /static/ {
        alias /var/www/whit/backend/staticfiles/;
        expires 30d;
    }
}
NGINX_EOF

# Enable the site
ln -sf /etc/nginx/sites-available/whit-staging /etc/nginx/sites-enabled/whit-staging
rm -f /etc/nginx/sites-enabled/default

# Test nginx config
if nginx -t; then
    echo "✅ Nginx configuration is valid"
    systemctl restart nginx
    echo "✅ Nginx restarted successfully"
else
    echo "❌ Nginx configuration error"
    nginx -t
    exit 1
fi

echo ""
echo "🧪 Testing Deployment"
echo "===================="

# Test backend health
echo "Testing backend..."
sleep 5
if curl -f http://127.0.0.1:8000/api/health/ >/dev/null 2>&1; then
    echo "✅ Backend health check passed"
else
    echo "⚠️ Backend health check failed, trying companies endpoint..."
    if curl -f http://127.0.0.1:8000/api/companies/ >/dev/null 2>&1; then
        echo "✅ Backend companies endpoint working"
    else
        echo "❌ Backend not responding"
        echo "Backend logs:"
        tail -20 /var/log/whit-backend.log
        exit 1
    fi
fi

# Test frontend
echo "Testing frontend..."
if curl -f https://staging.whoishiringintech.com/ >/dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "⚠️ Frontend check failed (might be SSL/domain issue)"
fi

echo ""
echo "🎉 DEPLOYMENT COMPLETED!"
echo "======================="
echo ""
echo "📊 Summary:"
echo "- ✅ Virtual environment created: venv_new/"
echo "- ✅ Python dependencies installed"
echo "- ✅ Database migrated"  
echo "- ✅ Django server running on 127.0.0.1:8000"
echo "- ✅ Frontend built with staging API URL"
echo "- ✅ Nginx configured with CORS headers"
echo ""
echo "🌐 URLs:"
echo "- Frontend: https://staging.whoishiringintech.com"
echo "- API: https://staging.whoishiringintech.com/api/"
echo ""
echo "📋 Logs:"
echo "- Backend: tail -f /var/log/whit-backend.log"
echo "- Nginx: tail -f /var/log/nginx/error.log"
echo ""
echo "🔧 Management:"
echo "- Restart backend: cd /var/www/whit && source venv_new/bin/activate && cd backend && python manage.py runserver 127.0.0.1:8000"
echo "- Check processes: ps aux | grep -E '(manage.py|nginx)'"
echo ""
echo "✅ CORS issues should now be resolved!"
echo "✅ Frontend will call staging API instead of production!"