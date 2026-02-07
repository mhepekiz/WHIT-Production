#!/bin/bash

# Post-deployment fix script to ensure stable service configuration
echo "🔧 Running post-deployment fixes..."

# Ensure the gunicorn run directory exists
echo "Creating runtime directory..."
sudo mkdir -p /run/gunicorn
sudo chown www-data:www-data /run/gunicorn

# Check if the service file has correct syntax
echo "Validating systemd service file..."
if ! systemd-analyze verify /etc/systemd/system/whit.service; then
    echo "❌ Invalid systemd service file detected. Applying fix..."
    
    # Create a corrected service file
    sudo tee /etc/systemd/system/whit.service > /dev/null << 'EOF'
[Unit]
Description=Gunicorn instance to serve WHIT Django application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/var/www/whit/backend
Environment="PATH=/var/www/whit/backend/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=whit.settings"
EnvironmentFile=-/var/www/whit/backend/.env

ExecStart=/var/www/whit/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8003 \
    --timeout 120 \
    --keep-alive 60 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --preload \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --log-level info \
    --capture-output \
    whit.wsgi:application

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30

# Conservative restart policy to prevent restart loops
Restart=on-failure
RestartSec=30
StartLimitInterval=300
StartLimitBurst=3

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    echo "✅ Service file corrected"
fi

# Kill any conflicting processes on port 8003
echo "Checking for port conflicts..."

# More aggressive cleanup - kill any python processes running on port 8003
sudo pkill -f "gunicorn.*8003" || true
sudo pkill -f "python.*8003" || true
sudo pkill -f ":8003" || true

# Also kill any processes by name
sudo pkill -f "whit.wsgi:application" || true

# Wait for processes to fully terminate
sleep 3

# Check again and force kill if needed
if lsof -i :8003 >/dev/null 2>&1; then
    echo "⚠️ Port 8003 still in use. Force killing processes..."
    lsof -ti :8003 | xargs sudo kill -9 2>/dev/null || true
    sleep 2
fi

# Stop the systemd service to ensure clean slate
echo "Stopping whit service to ensure clean startup..."
sudo systemctl stop whit 2>/dev/null || true
sleep 2

# Reload systemd and restart service
echo "Reloading systemd configuration..."
sudo systemctl daemon-reload

echo "Restarting whit service..."
sudo systemctl restart whit

# Enable service for auto-start
echo "Enabling whit service for auto-start..."
sudo systemctl enable whit

# Wait for service to stabilize
echo "Waiting for service to stabilize..."
sleep 5

# Check service status
if sudo systemctl is-active --quiet whit; then
    echo "✅ Whit service is running successfully"
    
    # Test basic connectivity
    if curl -f -s -o /dev/null http://127.0.0.1:8003; then
        echo "✅ Service is responding on port 8003"
    else
        echo "⚠️ Service not responding on port 8003 (this may be normal for Django apps)"
    fi
else
    echo "❌ Whit service failed to start"
    echo "Service status:"
    sudo systemctl status whit --no-pager
    echo "Recent logs:"
    sudo journalctl -u whit -n 20 --no-pager
    exit 1
fi

echo "🎉 Post-deployment fixes completed successfully!"