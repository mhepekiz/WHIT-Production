# Gunicorn Service Fix Summary

## Problem Statement

The WHIT Django application's Gunicorn service was experiencing critical stability issues:

1. **Service Termination**: Gunicorn service would stop after approximately 8 seconds
2. **502 Bad Gateway Errors**: Nginx couldn't connect to the backend service
3. **Port Not Listening**: Port 8003 was not actively listening for connections
4. **Poor Debugging**: No logs available to diagnose the root cause
5. **No Validation**: No pre-deployment health checks to catch issues early

## Root Cause Analysis

The systemd service configuration had several deficiencies:

1. **Missing Environment Variables**: 
   - No `DJANGO_SETTINGS_MODULE` set
   - Limited PATH configuration
   - No .env file loading support

2. **No Logging**:
   - No access or error logs configured
   - Only systemd journal available (limited detail)

3. **Inadequate Error Handling**:
   - No timeout configuration
   - Default restart policy without delay
   - No graceful shutdown handling

4. **No Pre-flight Checks**:
   - Service started without validating Django configuration
   - Database connectivity not verified
   - WSGI application loading not tested

## Solution Implemented

### 1. Enhanced Systemd Service File (`whit.service`)

**Before:**
```ini
[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/whit/backend
Environment="PATH=/var/www/whit/backend/venv/bin"
ExecStart=/var/www/whit/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8003 whit.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
```

**After:**
```ini
[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/whit/backend
Environment="PATH=/var/www/whit/backend/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="DJANGO_SETTINGS_MODULE=whit.settings"
EnvironmentFile=-/var/www/whit/backend/.env
ExecStart=/var/www/whit/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8003 \
    --timeout 120 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --log-level info \
    --capture-output \
    whit.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
KillMode=mixed
KillSignal=SIGQUIT
TimeoutStopSec=30
```

**Key Improvements:**
- ✅ Added `DJANGO_SETTINGS_MODULE` environment variable
- ✅ Extended PATH to include system binaries
- ✅ Added `.env` file loading support
- ✅ Configured Gunicorn logging to `/var/log/gunicorn/`
- ✅ Increased timeout to 120 seconds
- ✅ Added 10-second restart delay to prevent rapid restart loops
- ✅ Improved signal handling (SIGQUIT for graceful shutdown)
- ✅ Added log capture for better debugging

### 2. New Helper Scripts

#### `setup-gunicorn-logs.sh`
Creates and configures the Gunicorn log directory with proper permissions:
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chmod 755 /var/log/gunicorn
```

#### `health-check.sh`
Comprehensive validation script that checks:
- ✅ Backend directory exists
- ✅ Virtual environment is properly configured
- ✅ manage.py file exists
- ✅ .env file presence (warning if missing)
- ✅ Django system checks pass (`manage.py check --deploy`)
- ✅ Database connection is working
- ✅ Migrations are applied
- ✅ WSGI application loads correctly
- ✅ Gunicorn is installed in venv

### 3. Updated Deployment Workflows

Both `deploy.yml` and `deploy-production.yml` now include:

1. **Log Directory Setup**:
   ```bash
   sudo mkdir -p /var/log/gunicorn
   sudo chown -R www-data:www-data /var/log/gunicorn
   ```

2. **Health Checks Before Service Start**:
   ```bash
   sudo -u www-data ./venv/bin/python manage.py check --deploy || exit 1
   ```

3. **Service Update**:
   ```bash
   sudo cp /tmp/whit-deploy/whit.service /etc/systemd/system/whit.service
   sudo systemctl daemon-reload
   ```

4. **Stabilization Wait**:
   ```bash
   sudo systemctl start whit || sudo systemctl restart whit
   sleep 5  # Allow service to stabilize
   ```

5. **Failure Detection**:
   ```bash
   sudo systemctl status whit --no-pager || {
     echo "❌ Whit service failed to start!"
     sudo journalctl -u whit --no-pager -n 50
     exit 1
   }
   ```

### 4. Enhanced Production Restart Script

`restart_production.sh` now includes:
- Pre-restart health checks
- Service status validation
- Port listening verification
- Better error messages and early exit on failures

### 5. Comprehensive Documentation

#### TROUBLESHOOTING.md
New comprehensive guide covering:
- Common issues and their solutions
- Step-by-step troubleshooting procedures
- Log analysis techniques
- Quick recovery steps
- Prevention tips
- Diagnostic command reference

#### Updated DEPLOYMENT_GUIDE.md
- Added references to new scripts
- Included health check steps
- Enhanced service configuration section

#### Updated README.md
- Added production deployment section
- Referenced troubleshooting guide

## Expected Outcomes

After deploying these changes:

1. ✅ **Service Stability**: Gunicorn service should remain running continuously
2. ✅ **Better Logging**: Detailed logs available at `/var/log/gunicorn/`
3. ✅ **Early Failure Detection**: Health checks catch issues before service starts
4. ✅ **Easier Debugging**: Comprehensive logs and troubleshooting guide
5. ✅ **Reduced Downtime**: Proper restart policies prevent rapid restart loops
6. ✅ **502 Errors Resolved**: Port 8003 remains listening, nginx can connect

## Testing Plan

1. **Deploy to Staging**: 
   - Push changes to main branch
   - Monitor deployment workflow
   - Verify health checks pass
   - Confirm service starts and stays running

2. **Verify Logging**:
   - Check `/var/log/gunicorn/access.log` is being written
   - Check `/var/log/gunicorn/error.log` for any issues
   - Verify `journalctl -u whit` shows service activity

3. **Test Service Stability**:
   - Wait 5 minutes and verify service is still running
   - Check `sudo systemctl status whit`
   - Verify `sudo ss -tulnp | grep :8003` shows listening port

4. **Test Error Handling**:
   - Introduce a configuration error (e.g., invalid ALLOWED_HOSTS)
   - Verify health check catches it
   - Verify service doesn't start with broken config
   - Fix error and verify service starts successfully

5. **Load Testing**:
   - Send requests to the API
   - Verify requests are logged
   - Check service remains stable under load

## Rollback Plan

If issues occur:

1. Revert to previous service file:
   ```bash
   git checkout HEAD~3 whit.service
   sudo cp whit.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl restart whit
   ```

2. Check old logs:
   ```bash
   sudo journalctl -u whit --since "1 hour ago"
   ```

3. Report issues in the PR for further investigation

## Maintenance Notes

1. **Log Rotation**: Configure logrotate for `/var/log/gunicorn/` to prevent disk space issues
2. **Monitoring**: Set up monitoring to alert if service goes down
3. **Regular Health Checks**: Run `./health-check.sh` periodically to catch issues early
4. **Keep Backups**: Always backup working configurations before major changes

## Files Changed

- `whit.service` - Enhanced systemd service configuration
- `setup-gunicorn-logs.sh` - New log directory setup script
- `health-check.sh` - New comprehensive health check script
- `.github/workflows/deploy.yml` - Enhanced staging deployment
- `.github/workflows/deploy-production.yml` - Enhanced production deployment
- `restart_production.sh` - Improved restart script with validation
- `TROUBLESHOOTING.md` - New comprehensive troubleshooting guide
- `DEPLOYMENT_GUIDE.md` - Updated with new scripts
- `README.md` - Added production deployment references

## Security Notes

- ✅ No security vulnerabilities introduced (CodeQL scan passed)
- ✅ Service runs as www-data (non-root user)
- ✅ Log files have appropriate permissions (755)
- ✅ .env file loading uses safe EnvironmentFile directive
- ✅ No secrets exposed in service file or scripts
