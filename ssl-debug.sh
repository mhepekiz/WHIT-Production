#!/bin/bash

echo "🔍 SSL Troubleshooting for staging.whoishiringintech.com"
echo "=================================================="

# Check if the domain resolves correctly
echo "1. Checking DNS resolution..."
nslookup staging.whoishiringintech.com
echo ""

# Check if SSL certificate exists
echo "2. Checking SSL certificates..."
if [ -d "/etc/letsencrypt/live/staging.whoishiringintech.com" ]; then
    echo "✅ SSL certificate directory exists"
    ls -la /etc/letsencrypt/live/staging.whoishiringintech.com/
    echo ""
    echo "Certificate details:"
    openssl x509 -in /etc/letsencrypt/live/staging.whoishiringintech.com/fullchain.pem -text -noout | grep -A 2 "Subject:"
    echo ""
    echo "Certificate expiry:"
    openssl x509 -in /etc/letsencrypt/live/staging.whoishiringintech.com/fullchain.pem -enddate -noout
else
    echo "❌ SSL certificate directory does not exist"
fi
echo ""

# Check nginx configuration
echo "3. Testing nginx configuration..."
nginx -t
echo ""

# Check what's listening on port 443
echo "4. Checking what's listening on SSL port 443..."
netstat -tulnp | grep :443 || echo "Nothing listening on port 443"
echo ""

# Check nginx sites
echo "5. Checking nginx sites configuration..."
echo "Available sites:"
ls -la /etc/nginx/sites-available/
echo ""
echo "Enabled sites:"
ls -la /etc/nginx/sites-enabled/
echo ""

# Check nginx status
echo "6. Checking nginx status..."
systemctl status nginx --no-pager
echo ""

# Test SSL connection
echo "7. Testing SSL connection..."
echo "Testing HTTPS connection to staging domain..."
curl -I -k https://staging.whoishiringintech.com 2>&1 | head -10
echo ""

# Check recent nginx error logs
echo "8. Recent nginx error logs..."
tail -20 /var/log/nginx/error.log | grep -i staging || echo "No staging-related errors in recent logs"
echo ""

echo "🔧 Suggested fixes:"
echo "==================="

if [ ! -d "/etc/letsencrypt/live/staging.whoishiringintech.com" ]; then
    echo "SSL certificate missing. Run these commands:"
    echo "1. Install certbot:"
    echo "   sudo apt update && sudo apt install snapd"
    echo "   sudo snap install --classic certbot"
    echo "   sudo ln -sf /snap/bin/certbot /usr/bin/certbot"
    echo ""
    echo "2. Get SSL certificate:"
    echo "   sudo certbot --nginx -d staging.whoishiringintech.com --email admin@whoishiringintech.com"
    echo ""
    echo "OR temporarily run on HTTP only:"
    echo "   sudo systemctl stop nginx"
    echo "   # Edit /etc/nginx/sites-available/whit to remove SSL config for staging"
    echo "   sudo systemctl start nginx"
fi

echo ""
echo "Run this script on your server to diagnose the issue!"