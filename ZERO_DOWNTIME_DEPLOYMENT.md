# Zero-Downtime CI/CD Deployment Guide

This guide sets up a production-ready CI/CD pipeline with **zero downtime deployment** using Docker containers and automated GitHub Actions.

## 🚀 Key Features

- **Zero Downtime**: Rolling deployments with health checks
- **Automated CI/CD**: GitHub Actions pipeline triggered on push
- **Containerized**: Docker containers for consistent environments
- **Scalable**: Load balancing with nginx
- **Secure**: PostgreSQL database, Redis caching, SSL ready
- **Monitoring**: Health checks and logging
- **Rollback**: Automatic rollback on failed deployments

## 📋 Prerequisites

1. **Server Requirements**:
   - Ubuntu 20.04+ or similar Linux distribution
   - Docker and Docker Compose installed
   - At least 2GB RAM
   - Port 80 and 443 available

2. **Domain Setup**:
   - Domain pointing to your server IP
   - SSL certificate (Let's Encrypt recommended)

3. **GitHub Repository**:
   - Repository with code
   - GitHub Actions enabled

## 🛠️ Installation Steps

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login to apply group changes
```

### 2. Project Setup

```bash
# Clone repository
git clone https://github.com/yourusername/whit-release.git
cd whit-release

# Copy environment file
cp .env.production.example .env.production

# Edit environment variables
nano .env.production
```

### 3. Environment Configuration

Edit `.env.production` with your settings:

```env
# Update these values
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (will be created automatically)
DATABASE_URL=postgresql://whit_user:secure_password_here@db:5432/whit_db

# Email settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 4. GitHub Secrets Setup

In your GitHub repository, go to Settings → Secrets and Variables → Actions, and add:

```
STAGING_HOST: your-server-ip-or-domain
STAGING_USER: your-server-username
STAGING_PASSWORD: your-server-password-or-key
DOCKER_HUB_USERNAME: your-dockerhub-username (optional)
DOCKER_HUB_ACCESS_TOKEN: your-dockerhub-token (optional)
```

### 5. Initial Deployment

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Run database migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 6. Verify Deployment

```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Test health check
curl http://localhost/api/health/

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔄 How Zero-Downtime Deployment Works

### Traditional Deployment (OLD - Causes Downtime):
1. Stop existing services ❌
2. Replace files ❌
3. Start services ❌
4. **Result: 2-5 minutes downtime** ❌

### New Zero-Downtime Deployment:
1. Build new Docker images ✅
2. Start new containers alongside existing ones ✅
3. Health check new containers ✅
4. Route traffic to new containers ✅
5. Stop old containers ✅
6. **Result: 0 seconds downtime** ✅

## 🚀 Automated Deployment Process

### Trigger Deployment:
```bash
# Simply push to main branch
git add .
git commit -m "Your changes"
git push origin main
```

### What Happens Automatically:
1. **GitHub Actions** detects the push
2. **Runs tests** to ensure code quality
3. **Builds Docker images** with new code
4. **Deploys to server** using zero-downtime strategy
5. **Runs health checks** to verify deployment
6. **Sends notifications** about deployment status

## 📊 Monitoring and Maintenance

### Check Service Status:
```bash
# View all services
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Health check
curl http://yourdomain.com/api/health/
```

### Database Backup:
```bash
# Manual backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U whit_user whit_db > backup_$(date +%Y%m%d).sql

# Restore from backup
cat backup_20240101.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U whit_user whit_db
```

### Scaling Services:
```bash
# Scale backend for high traffic
docker-compose -f docker-compose.prod.yml up -d --scale web=3

# Scale back down
docker-compose -f docker-compose.prod.yml up -d --scale web=1
```

## 🔧 Troubleshooting

### Deployment Failed:
```bash
# Check GitHub Actions logs in repository
# Check server logs:
docker-compose -f docker-compose.prod.yml logs

# Manual deployment:
./deploy-zero-downtime.sh
```

### Service Issues:
```bash
# Restart specific service
docker-compose -f docker-compose.prod.yml restart web

# Restart all services
docker-compose -f docker-compose.prod.yml restart
```

### Database Issues:
```bash
# Access database
docker-compose -f docker-compose.prod.yml exec db psql -U whit_user whit_db

# Check database connection
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

## 🔄 Rollback Strategy

If something goes wrong:

### Automatic Rollback:
- Health checks fail → Automatic rollback
- Database issues → Restore from backup

### Manual Rollback:
```bash
# Get previous image
docker images

# Use previous image tag
docker-compose -f docker-compose.prod.yml down
# Edit docker-compose.prod.yml to use previous image
docker-compose -f docker-compose.prod.yml up -d
```

## 🎯 Benefits of This Setup

1. **Zero Downtime**: Users never experience service interruption
2. **Automated**: No manual file copying or service restarting
3. **Reliable**: Health checks ensure deployment success
4. **Scalable**: Easy to add more servers or scale services
5. **Secure**: Containerized environment with proper separation
6. **Maintainable**: Clear logs and monitoring
7. **Fast**: Deployments complete in under 2 minutes
8. **Safe**: Automatic rollback on failures

## 📈 Performance Improvements

- **Database**: PostgreSQL instead of SQLite
- **Caching**: Redis for session and query caching  
- **Load Balancing**: nginx distributes traffic
- **Static Files**: Optimized serving of CSS/JS/images
- **Compression**: Gzip compression enabled
- **Security**: HTTPS ready with proper headers

## 🔐 Security Features

- **Environment Variables**: Secrets not in code
- **Database Security**: Isolated PostgreSQL container
- **Network Security**: Internal Docker network
- **SSL Ready**: HTTPS configuration included
- **CORS Protection**: Proper cross-origin policies
- **Admin Security**: Django admin protection

This setup transforms your manual deployment process into a professional, enterprise-grade CI/CD pipeline with zero downtime! 🚀