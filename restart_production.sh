#!/bin/bash

# Quick server restart script for production
# Use this to restart your application after code changes

echo "🔄 Restarting WHIT application services..."

# Run health check first
if [ -f "./health-check.sh" ]; then
    echo "Running health checks..."
    if ./health-check.sh; then
        echo "✅ Health checks passed"
    else
        echo "❌ Health checks failed - aborting restart"
        exit 1
    fi
else
    echo "⚠️  Health check script not found, skipping..."
fi

# Restart Django application
echo "Restarting Django application..."
sudo systemctl restart whit

# Wait for service to stabilize
sleep 5

# Reload NGINX
echo "Reloading NGINX..."
sudo systemctl reload nginx

# Check service status
echo "Checking service status..."
if sudo systemctl is-active --quiet whit; then
    echo "✅ Django service is running"
    sudo systemctl status whit --no-pager -l
else
    echo "❌ Django service failed to start!"
    echo "Recent logs:"
    sudo journalctl -u whit --no-pager -n 20
    exit 1
fi

if sudo systemctl is-active --quiet nginx; then
    echo "✅ Nginx service is running"
    sudo systemctl status nginx --no-pager -l
else
    echo "❌ Nginx service is not running!"
    exit 1
fi

# Check if port is listening
if sudo ss -tulnp | grep -q :8003; then
    echo "✅ Port 8003 is listening"
else
    echo "❌ Port 8003 is NOT listening!"
    exit 1
fi

echo "✅ Services restarted successfully!"
echo "📝 Check logs with: sudo journalctl -u whit -f"