#!/bin/bash

# Zero-downtime deployment script
# This script handles production deployment with Docker containers

set -e

echo "🚀 Starting zero-downtime deployment..."

# Configuration
PROJECT_DIR="/var/www/whit"
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="/var/backups/whit"
LOG_FILE="/var/log/whit/deploy.log"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR
mkdir -p $(dirname $LOG_FILE)

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Main deployment function
deploy() {
    cd $PROJECT_DIR
    
    # Pull latest code
    log "📥 Pulling latest code..."
    git pull origin main
    
    # Pull latest images
    log "📦 Pulling latest Docker images..."
    docker-compose -f $DOCKER_COMPOSE_FILE pull
    
    # Start deployment with zero downtime
    log "🚀 Starting zero-downtime deployment..."
    docker-compose -f $DOCKER_COMPOSE_FILE up -d
    
    # Wait for containers to be ready
    sleep 30
    
    # Run database migrations
    log "🗄️ Running database migrations..."
    docker-compose -f $DOCKER_COMPOSE_FILE exec -T backend python manage.py migrate --noinput
    
    # Collect static files
    log "📁 Collecting static files..."
    docker-compose -f $DOCKER_COMPOSE_FILE exec -T backend python manage.py collectstatic --noinput
    
    # Health check
    log "🔍 Running health check..."
    if curl -f -s "http://localhost:80/api/companies/" > /dev/null; then
        log "✅ Deployment successful!"
    else
        log "❌ Health check failed"
        exit 1
    fi
}

# Execute deployment
deploy