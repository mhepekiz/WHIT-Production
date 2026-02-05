# WHIT Deployment Guide for nahhat.com

## 📋 Pre-requisites
- Linode server with Ubuntu 20.04+ 
- Domain name `nahhat.com` pointing to your server IP
- SSH access to your server
- Basic familiarity with Linux commands

## 🚀 Deployment Steps

### 1. Initial Server Setup
Upload your project files to your Linode server:
```bash
# From your local machine
rsync -avz --exclude='node_modules' --exclude='venv*' --exclude='*.pyc' . user@your-server-ip:/var/www/whit/
```

### 2. Run the deployment script
```bash
# On your server
cd /var/www/whit
sudo ./deploy.sh
```

### 3. Configure Environment Variables
Edit the production environment file:
```bash
cd /var/www/whit/backend
cp ../.env.production .env
nano .env
```

**Important**: Update these values in `.env`:
- `SECRET_KEY`: Generate a new Django secret key
- `DATABASE_PASSWORD`: Set a strong password
- `ALLOWED_HOSTS`: Include your server IP
- `CORS_ALLOWED_ORIGINS`: Set to your domain

### 4. Setup Backend
```bash
# In /var/www/whit/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Django setup
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 5. Build Frontend
```bash
# In /var/www/whit/frontend
npm install
npm run build
```

### 6. Configure Services
```bash
# Setup Gunicorn log directory
cd /var/www/whit
sudo ./setup-gunicorn-logs.sh

# Run health checks
sudo ./health-check.sh

# Setup systemd service
sudo cp /var/www/whit/whit.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable whit
sudo systemctl start whit

# Verify service is running
sleep 5
sudo systemctl status whit

# Setup NGINX
sudo cp /var/www/whit/nginx.conf /etc/nginx/sites-available/nahhat.com
sudo ln -s /etc/nginx/sites-available/nahhat.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. SSL Certificate
```bash
sudo certbot --nginx -d nahhat.com -d www.nahhat.com
```

### 8. Firewall Configuration
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

## 🔧 Production Management

### Check Service Status
```bash
sudo systemctl status whit
sudo systemctl status nginx
```

### View Logs
```bash
# Django application logs
sudo journalctl -u whit -f

# NGINX logs
sudo tail -f /var/log/nginx/nahhat.com.access.log
sudo tail -f /var/log/nginx/nahhat.com.error.log
```

### Restart Services
```bash
# Use the provided script
./restart_production.sh

# Or manually
sudo systemctl restart whit
sudo systemctl reload nginx
```

### Database Backup
```bash
# Create backup
sudo -u postgres pg_dump whit_production > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
sudo -u postgres psql whit_production < backup_file.sql
```

## 📁 File Structure on Server
```
/var/www/whit/
├── backend/               # Django application
│   ├── venv/             # Python virtual environment
│   ├── staticfiles/      # Collected static files
│   ├── media/            # User uploads
│   ├── .env              # Production environment variables
│   └── manage.py
├── frontend/
│   ├── dist/             # Built React application
│   └── package.json
├── nginx.conf            # NGINX configuration
├── whit.service          # Systemd service file
└── deploy.sh             # Deployment script
```

## 🔐 Security Checklist
- [ ] Strong database password set
- [ ] Django SECRET_KEY changed
- [ ] DEBUG=False in production
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Regular backups configured
- [ ] Server security updates enabled

## 🌐 DNS Configuration
Make sure your domain DNS records point to your Linode server:
```
A Record: nahhat.com → YOUR_SERVER_IP
A Record: www.nahhat.com → YOUR_SERVER_IP
```

## 📞 Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Run health checks
cd /var/www/whit
sudo ./health-check.sh

# View detailed logs
sudo journalctl -u whit --no-pager -l
```

For detailed troubleshooting steps, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

**NGINX errors:**
```bash
sudo nginx -t
```

**Database connection issues:**
```bash
sudo -u postgres psql -c "\l"  # List databases
sudo -u postgres psql -c "\du" # List users
```

**SSL certificate issues:**
```bash
sudo certbot certificates
sudo certbot renew --dry-run
```

## 📈 Monitoring & Maintenance

### Log Rotation
Logs are automatically rotated by systemd, but you can check:
```bash
sudo journalctl --disk-usage
```

### Performance Monitoring
```bash
# Check system resources
htop
df -h
free -m

# Check application performance
sudo systemctl status whit
```

### Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Python packages (in virtual environment)
source /var/www/whit/backend/venv/bin/activate
pip list --outdated
```

## 🎯 Success Verification
After deployment, verify everything works:
1. Visit `https://nahhat.com` - should load your React frontend
2. Visit `https://nahhat.com/api/` - should show Django REST API
3. Visit `https://nahhat.com/admin/` - should load Django admin
4. Test user registration and login
5. Test file uploads (if applicable)

Your WHIT application should now be successfully deployed on nahhat.com! 🎉