#!/bin/bash

# Post-deployment verification script
# Run this after deployment to verify everything is working correctly

set -e

echo "🔍 Running post-deployment verification..."
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SUCCESS=0
WARNINGS=0
FAILURES=0

# Function to print status
print_check() {
    local status=$1
    local message=$2
    
    if [ "$status" = "pass" ]; then
        echo -e "${GREEN}✓${NC} $message"
        SUCCESS=$((SUCCESS + 1))
    elif [ "$status" = "warn" ]; then
        echo -e "${YELLOW}⚠${NC} $message"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${RED}✗${NC} $message"
        FAILURES=$((FAILURES + 1))
    fi
}

# Check 1: Django service status
echo "Checking Django service..."
if sudo systemctl is-active --quiet whit; then
    print_check "pass" "Django service is running"
else
    print_check "fail" "Django service is NOT running"
fi

# Check 2: Nginx service status
echo "Checking Nginx service..."
if sudo systemctl is-active --quiet nginx; then
    print_check "pass" "Nginx service is running"
else
    print_check "fail" "Nginx service is NOT running"
fi

# Check 3: Port 8003 listening
echo "Checking if port 8003 is listening..."
if sudo ss -tulnp | grep -q :8003; then
    print_check "pass" "Port 8003 is listening"
else
    print_check "fail" "Port 8003 is NOT listening"
fi

# Check 4: Gunicorn logs exist
echo "Checking Gunicorn logs..."
if [ -f "/var/log/gunicorn/access.log" ] && [ -f "/var/log/gunicorn/error.log" ]; then
    print_check "pass" "Gunicorn log files exist"
else
    print_check "warn" "Gunicorn log files not found (may not be created yet)"
fi

# Check 5: Recent log entries
echo "Checking for recent log activity..."
if sudo journalctl -u whit --since "5 minutes ago" | grep -q "Booting worker"; then
    print_check "pass" "Gunicorn workers are booting"
elif sudo journalctl -u whit --since "5 minutes ago" | grep -q "Listening at"; then
    print_check "pass" "Gunicorn is listening"
else
    print_check "warn" "No recent Gunicorn activity in logs"
fi

# Check 6: No recent errors
echo "Checking for recent errors..."
if sudo journalctl -u whit --since "5 minutes ago" --priority=err | grep -q .; then
    print_check "warn" "Errors found in recent logs"
    echo "  Run: sudo journalctl -u whit --since '5 minutes ago' --priority=err"
else
    print_check "pass" "No errors in recent logs"
fi

# Check 7: Nginx configuration
echo "Checking Nginx configuration..."
if sudo nginx -t > /dev/null 2>&1; then
    print_check "pass" "Nginx configuration is valid"
else
    print_check "fail" "Nginx configuration has errors"
fi

# Check 8: Test HTTP connection to localhost
echo "Testing HTTP connection to localhost..."
if curl -f -s -o /dev/null http://localhost; then
    print_check "pass" "HTTP connection successful"
else
    print_check "warn" "HTTP connection failed (may be SSL-only)"
fi

# Check 9: Test API endpoint
echo "Testing API endpoint..."
if curl -f -s -o /dev/null http://localhost/api/; then
    print_check "pass" "API endpoint responding"
else
    print_check "warn" "API endpoint not responding via HTTP"
fi

# Check 10: Database connection
echo "Testing database connection..."
cd /var/www/whit/backend
if sudo -u www-data ./venv/bin/python manage.py showmigrations --list > /dev/null 2>&1; then
    print_check "pass" "Database connection working"
else
    print_check "fail" "Database connection failed"
fi

# Check 11: Static files
echo "Checking static files..."
if [ -d "/var/www/whit/backend/staticfiles" ]; then
    print_check "pass" "Static files directory exists"
else
    print_check "warn" "Static files directory not found"
fi

# Check 12: Media files directory
echo "Checking media files..."
if [ -d "/var/www/whit/backend/media" ]; then
    print_check "pass" "Media files directory exists"
else
    print_check "warn" "Media files directory not found"
fi

# Summary
echo ""
echo "========================================="
echo "Verification Summary"
echo "========================================="
echo -e "${GREEN}Passed:${NC} $SUCCESS"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "${RED}Failed:${NC} $FAILURES"
echo ""

if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}✓ Deployment verification successful!${NC}"
    echo ""
    echo "Next steps:"
    echo "  • Monitor logs: sudo journalctl -u whit -f"
    echo "  • Check Gunicorn logs: sudo tail -f /var/log/gunicorn/error.log"
    echo "  • Test the application in your browser"
    exit 0
else
    echo -e "${RED}✗ Deployment verification failed!${NC}"
    echo ""
    echo "Please review the failures above and:"
    echo "  • Check service logs: sudo journalctl -u whit --no-pager -n 50"
    echo "  • Run health check: sudo /var/www/whit/health-check.sh"
    echo "  • See TROUBLESHOOTING.md for help"
    exit 1
fi
