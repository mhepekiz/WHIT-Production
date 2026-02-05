# Quick Reference: Gunicorn Service Management

## Quick Start Commands

### Check Service Status
```bash
sudo systemctl status whit
sudo ss -tulnp | grep :8003
```

### Restart Service
```bash
cd /var/www/whit
sudo ./restart_production.sh
```

### Run Health Check
```bash
cd /var/www/whit
sudo ./health-check.sh
```

### View Logs
```bash
# Systemd logs
sudo journalctl -u whit -f

# Gunicorn logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log
```

## Common Issues

### Service Won't Start
1. Run health check: `sudo ./health-check.sh`
2. Check logs: `sudo journalctl -u whit --no-pager -n 50`
3. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### 502 Bad Gateway
1. Check if port 8003 is listening: `sudo ss -tulnp | grep :8003`
2. Restart service: `sudo ./restart_production.sh`
3. Check nginx: `sudo nginx -t && sudo systemctl reload nginx`

### View Recent Errors
```bash
sudo journalctl -u whit --since "10 minutes ago" --priority=err
```

## Files and Locations

| Item | Location |
|------|----------|
| Service file | `/etc/systemd/system/whit.service` |
| Application | `/var/www/whit/backend/` |
| Access logs | `/var/log/gunicorn/access.log` |
| Error logs | `/var/log/gunicorn/error.log` |
| Systemd logs | `journalctl -u whit` |
| Health check | `/var/www/whit/health-check.sh` |
| Verify deployment | `/var/www/whit/verify-deployment.sh` |

## Documentation

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Comprehensive troubleshooting guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Full deployment instructions
- **[GUNICORN_FIX_SUMMARY.md](GUNICORN_FIX_SUMMARY.md)** - Details of fixes implemented

## After Deployment

Run the verification script:
```bash
cd /var/www/whit
sudo ./verify-deployment.sh
```

This checks:
- ✅ Service status
- ✅ Port listening
- ✅ Logs exist
- ✅ No recent errors
- ✅ Database connection
- ✅ API endpoint responding
