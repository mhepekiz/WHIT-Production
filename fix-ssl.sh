#!/bin/bash

echo "🔧 Fixing SSL and nginx configuration issues..."
echo "================================================="

# Step 1: Handle the conflicting site configuration
echo "1. Checking for conflicting nginx sites..."
if [ -f "/etc/nginx/sites-enabled/staging.realfood.tips" ]; then
    echo "⚠️  Found conflicting site: staging.realfood.tips"
    echo "Disabling conflicting site..."
    sudo rm /etc/nginx/sites-enabled/staging.realfood.tips
    echo "✅ Conflicting site disabled"
fi

# Step 2: Update the nginx configuration from the repository
echo ""
echo "2. Updating nginx configuration..."
cd /var/www/whit
sudo cp nginx.conf /etc/nginx/sites-available/whit
sudo ln -sf /etc/nginx/sites-available/whit /etc/nginx/sites-enabled/whit

# Step 3: Test the nginx configuration
echo ""
echo "3. Testing nginx configuration..."
sudo nginx -t
if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration still has errors"
    echo "Showing recent nginx error logs:"
    sudo tail -10 /var/log/nginx/error.log
    exit 1
fi

# Step 4: Reload nginx
echo ""
echo "4. Reloading nginx..."
sudo systemctl reload nginx
if [ $? -eq 0 ]; then
    echo "✅ Nginx reloaded successfully"
else
    echo "❌ Failed to reload nginx"
    sudo systemctl status nginx --no-pager
    exit 1
fi

# Step 5: Check nginx status
echo ""
echo "5. Checking nginx status..."
sudo systemctl status nginx --no-pager

# Step 6: Test the SSL connection
echo ""
echo "6. Testing connections..."
echo "Testing HTTPS connection to staging domain:"
curl -I https://staging.whoishiringintech.com 2>&1 | head -5

echo ""
echo "Testing API endpoint:"
curl -I https://staging.whoishiringintech.com/api/ 2>&1 | head -5

# Step 7: Check certificate validity
echo ""
echo "7. Checking SSL certificate:"
echo "Certificate details:"
openssl x509 -in /etc/letsencrypt/live/staging.whoishiringintech.com/fullchain.pem -subject -dates -noout

echo ""
echo "🎉 SSL fix completed!"
echo ""
echo "Your staging site should now be accessible at:"
echo "https://staging.whoishiringintech.com"
echo ""
echo "If you still have issues, run:"
echo "sudo systemctl status nginx"
echo "sudo tail -f /var/log/nginx/error.log"