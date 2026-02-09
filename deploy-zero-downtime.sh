#!/bin/bash

# Zero-Downtime Deployment Script
# This script handles rolling deployment without downtime

set -e

# Configuration
PROJECT_NAME="whit"
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="/var/backups/whit"
DEPLOY_USER="deploy"
DEPLOY_KEY_PATH="~/.ssh/deploy_key"

echo "🚀 Starting zero-downtime deployment..."

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create database backup before deployment
echo "📦 Creating database backup..."
docker-compose -f $DOCKER_COMPOSE_FILE exec -T db pg_dump -U whit_user whit_db > "$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"

# Build new images
echo "🔨 Building new Docker images..."
docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache

# Start rolling deployment
echo "🔄 Starting rolling deployment..."

# Update backend with zero downtime
echo "⚙️  Updating backend services..."
docker-compose -f $DOCKER_COMPOSE_FILE up -d --scale web=2
sleep 10  # Wait for new container to be ready
docker-compose -f $DOCKER_COMPOSE_FILE up -d --scale web=1 --remove-orphans

# Update frontend
echo "🌐 Updating frontend..."
docker-compose -f $DOCKER_COMPOSE_FILE up -d frontend

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose -f $DOCKER_COMPOSE_FILE exec web python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f $DOCKER_COMPOSE_FILE exec web python manage.py collectstatic --noinput

# Health check
echo "🏥 Running health checks..."
MAX_ATTEMPTS=30
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    if curl -f -s http://localhost/api/health/ > /dev/null; then
        echo "✅ Health check passed!"
        break
    else
        echo "⏳ Health check attempt $ATTEMPT/$MAX_ATTEMPTS failed, retrying..."
        sleep 5
        ATTEMPT=$((ATTEMPT + 1))
    fi
done

if [ $ATTEMPT -gt $MAX_ATTEMPTS ]; then
    echo "❌ Health check failed after $MAX_ATTEMPTS attempts!"
    echo "🔙 Rolling back..."
    
    # Rollback logic
    docker-compose -f $DOCKER_COMPOSE_FILE down
    # Restore from backup if needed
    exit 1
fi

# Clean up old Docker images
echo "🧹 Cleaning up old Docker images..."
docker system prune -f

echo "✅ Deployment completed successfully!"
echo "🌐 Application is running at: http://localhost"
echo "📊 Monitor logs with: docker-compose -f $DOCKER_COMPOSE_FILE logs -f"