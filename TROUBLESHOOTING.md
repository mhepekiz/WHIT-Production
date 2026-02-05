# Gunicorn Service Troubleshooting Guide

## Common Issues and Solutions

### Issue: Service Stops After ~8 Seconds

**Symptoms:**
- `sudo systemctl status whit` shows "inactive (dead)"
- Workers start but quickly terminate with SIGTERM
- Port 8003 not listening
- 502 Bad Gateway errors from nginx

**Root Causes:**
1. **Missing Environment Variables**: Django can't find required settings
2. **Import Errors**: Python modules or Django apps can't be imported
3. **Database Connection Issues**: Can't connect to PostgreSQL or SQLite
4. **Permission Issues**: www-data user can't access files
5. **Missing Dependencies**: Required Python packages not installed

**Solutions:**

#### 1. Check Service Logs
```bash
# View recent logs
sudo journalctl -u whit -n 50 --no-pager

# Follow logs in real-time
sudo journalctl -u whit -f

# Check Gunicorn logs (after service file update)
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log
```

#### 2. Run Health Check
```bash
# Run the health check script
cd /var/www/whit
sudo ./health-check.sh
```

#### 3. Test Django Manually
```bash
cd /var/www/whit/backend

# Test Django check command
sudo -u www-data ./venv/bin/python manage.py check --deploy

# Test WSGI import
sudo -u www-data ./venv/bin/python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
print('WSGI OK')
"

# Test Gunicorn manually (foreground mode)
sudo -u www-data ./venv/bin/gunicorn \
  --bind 127.0.0.1:8003 \
  --timeout 120 \
  whit.wsgi:application
```

#### 4. Check File Permissions
```bash
# Ensure www-data owns the files
sudo chown -R www-data:www-data /var/www/whit
sudo chmod -R 755 /var/www/whit

# Check specific files
ls -la /var/www/whit/backend/
ls -la /var/www/whit/backend/venv/
```

#### 5. Verify Environment File
```bash
# Check if .env exists
ls -la /var/www/whit/backend/.env

# View environment variables (hide secrets)
cat /var/www/whit/backend/.env | grep -v "SECRET\|PASSWORD"
```

#### 6. Check Database
```bash
# For SQLite
ls -la /var/www/whit/backend/db.sqlite3

# For PostgreSQL
sudo -u postgres psql -c "\l" | grep whit
sudo -u postgres psql -c "\du" | grep whit
```

### Issue: Port 8003 Not Listening

**Check:**
```bash
# See what's listening on port 8003
sudo ss -tulnp | grep :8003

# Check if any Python/Gunicorn processes are running
ps aux | grep gunicorn
```

**Fix:**
```bash
# Restart the service
sudo systemctl restart whit

# Check status
sudo systemctl status whit

# Wait a few seconds and check port again
sleep 5
sudo ss -tulnp | grep :8003
```

### Issue: 502 Bad Gateway Errors

**Cause:** Nginx can't connect to Gunicorn backend

**Check:**
```bash
# Verify Gunicorn is running and listening
sudo systemctl status whit
sudo ss -tulnp | grep :8003

# Check nginx configuration
sudo nginx -t

# Check nginx error logs
sudo tail -50 /var/log/nginx/error.log
```

**Fix:**
```bash
# Restart both services in order
sudo systemctl restart whit
sleep 5
sudo systemctl reload nginx
```

### Issue: 400 Bad Request Errors

**Cause:** Usually related to ALLOWED_HOSTS or CORS settings

**Check:**
```bash
# View current Django settings
cd /var/www/whit/backend
sudo -u www-data ./venv/bin/python manage.py shell -c "
from django.conf import settings
print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
print('DEBUG:', settings.DEBUG)
print('CORS_ALLOWED_ORIGINS:', settings.CORS_ALLOWED_ORIGINS)
"
```

**Fix:**
Update `/var/www/whit/backend/.env`:
```env
ALLOWED_HOSTS=nahhat.com,www.nahhat.com,your.server.ip,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://nahhat.com,https://www.nahhat.com
```

Then restart:
```bash
sudo systemctl restart whit
```

### Issue: 404 Not Found Errors

**Cause:** Missing data or URL routing issues

**Check:**
```bash
cd /var/www/whit/backend

# Check if required data exists
sudo -u www-data ./venv/bin/python manage.py shell -c "
from companies.models import Company, HowItWorksSection
print('Companies:', Company.objects.count())
print('HowItWorksSection:', HowItWorksSection.objects.count())
"

# List all URLs
sudo -u www-data ./venv/bin/python manage.py show_urls || \
sudo -u www-data ./venv/bin/python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
import django
django.setup()
from django.urls import get_resolver
resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(pattern)
"
```

**Fix:**
```bash
# Run the homepage sections creation command
cd /var/www/whit/backend
sudo -u www-data ./venv/bin/python manage.py force_create_homepage_sections
```

## Service Management Commands

### Check Status
```bash
sudo systemctl status whit
sudo systemctl status nginx
```

### Start/Stop/Restart
```bash
# Django/Gunicorn
sudo systemctl start whit
sudo systemctl stop whit
sudo systemctl restart whit

# Nginx
sudo systemctl reload nginx
sudo systemctl restart nginx
```

### Enable/Disable Auto-start
```bash
sudo systemctl enable whit
sudo systemctl disable whit
```

### View Logs
```bash
# Django/Gunicorn systemd logs
sudo journalctl -u whit -f

# Gunicorn application logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Quick Recovery Steps

If the service is completely broken:

```bash
# 1. Stop everything
sudo systemctl stop whit
sudo systemctl stop nginx

# 2. Run health check
cd /var/www/whit
sudo ./health-check.sh

# 3. If health check passes, setup logs and restart
sudo ./setup-gunicorn-logs.sh
sudo systemctl daemon-reload
sudo systemctl start whit
sleep 5

# 4. Check if service is running
sudo systemctl status whit --no-pager
sudo ss -tulnp | grep :8003

# 5. If running, start nginx
sudo systemctl start nginx

# 6. Test the site
curl -I http://localhost
curl -I http://localhost/api/
```

## Prevention Tips

1. **Always run health checks before restarting the service**
2. **Monitor logs regularly**
3. **Keep backups of working configurations**
4. **Test changes in staging before production**
5. **Use the deployment workflows which include health checks**
6. **Set up log rotation to prevent disk space issues**

## Getting Help

If issues persist:

1. Collect diagnostic information:
```bash
cd /var/www/whit
./health-check.sh > diagnostic.log 2>&1
sudo journalctl -u whit --no-pager -n 100 >> diagnostic.log
sudo tail -100 /var/log/gunicorn/error.log >> diagnostic.log
```

2. Review the diagnostic.log file
3. Check for specific error messages in the logs
4. Verify all prerequisites are met (see DEPLOYMENT_GUIDE.md)
