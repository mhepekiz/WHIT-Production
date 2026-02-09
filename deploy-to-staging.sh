#!/bin/bash

# Deploy WHIT to staging server
# This script updates the staging server with latest code

SERVER="root@45.79.211.144"
REMOTE_DIR="/var/www/whit"
LOCAL_DIR="/Users/mustafahepekiz/Desktop/whit-release"

echo "🚀 Deploying WHIT to staging server..."

# Build frontend locally first
echo "📦 Building frontend locally..."
cd $LOCAL_DIR/frontend
npm run build

# Copy backend files
echo "📂 Copying backend files..."
sshpass -p 'sm0ky&&G0nc4' rsync -avz --delete \
  --exclude='venv*' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.git' \
  --exclude='db.sqlite3' \
  --exclude='media' \
  --exclude='logs' \
  --exclude='.env' \
  $LOCAL_DIR/backend/ $SERVER:$REMOTE_DIR/backend/

# Copy frontend dist files
echo "🌐 Copying frontend dist files..."
sshpass -p 'sm0ky&&G0nc4' rsync -avz --delete \
  $LOCAL_DIR/frontend/dist/ $SERVER:$REMOTE_DIR/frontend/dist/

# Run migrations
echo "🗄️ Running migrations..."
sshpass -p 'sm0ky&&G0nc4' ssh -o StrictHostKeyChecking=no $SERVER \
  "cd $REMOTE_DIR/backend && source venv/bin/activate && python manage.py migrate"

# Collect static files
echo "📁 Collecting static files..."
sshpass -p 'sm0ky&&G0nc4' ssh -o StrictHostKeyChecking=no $SERVER \
  "cd $REMOTE_DIR/backend && source venv/bin/activate && python manage.py collectstatic --noinput"

# Restart services
echo "🔄 Restarting services..."
sshpass -p 'sm0ky&&G0nc4' ssh -o StrictHostKeyChecking=no $SERVER \
  "systemctl restart whit.service && systemctl restart nginx"

echo "✅ Deployment complete!"
echo "🌟 Visit: https://staging.whoishiringintech.com"