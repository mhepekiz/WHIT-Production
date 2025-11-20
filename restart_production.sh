#!/bin/bash

# Quick server restart script for production
# Use this to restart your application after code changes

echo "🔄 Restarting WHIT application services..."

# Restart Django application
echo "Restarting Django application..."
sudo systemctl restart whit

# Reload NGINX
echo "Reloading NGINX..."
sudo systemctl reload nginx

# Check service status
echo "Checking service status..."
sudo systemctl status whit --no-pager -l
sudo systemctl status nginx --no-pager -l

echo "✅ Services restarted!"
echo "📝 Check logs with: sudo journalctl -u whit -f"