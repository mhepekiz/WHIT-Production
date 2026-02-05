#!/bin/bash

# Setup script for Gunicorn log directory
# This should be run on the production server during initial setup or deployment

echo "Setting up Gunicorn log directory..."

# Create log directory if it doesn't exist
sudo mkdir -p /var/log/gunicorn

# Set proper ownership
sudo chown -R www-data:www-data /var/log/gunicorn

# Set proper permissions
sudo chmod 755 /var/log/gunicorn

echo "✅ Gunicorn log directory setup complete"
echo "Logs will be written to:"
echo "  - Access log: /var/log/gunicorn/access.log"
echo "  - Error log: /var/log/gunicorn/error.log"
