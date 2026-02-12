#!/bin/bash
echo "🔍 Finding Staging Nginx Configuration"
echo "====================================="

echo "1. Checking for site-specific files:"
ls -la /etc/nginx/sites-available/

echo ""
echo "2. Checking for any files containing 'staging.whoishiringintech.com':"
grep -r "staging.whoishiringintech.com" /etc/nginx/ 2>/dev/null

echo ""
echo "3. Checking main nginx.conf:"
grep -n "server_name" /etc/nginx/nginx.conf

echo ""
echo "4. Looking for files with /Users/mustafahepekiz paths:"
grep -r "/Users/mustafahepekiz" /etc/nginx/ 2>/dev/null

echo ""
echo "5. Checking enabled sites:"
ls -la /etc/nginx/sites-enabled/

echo ""
echo "6. Checking for any .conf files:"
find /etc/nginx/ -name "*.conf" -type f

echo ""
echo "🔧 Once you find the correct file, look for these lines to fix:"
echo "   alias /Users/mustafahepekiz/Desktop/whit-release/backend/staticfiles/;"
echo "   alias /Users/mustafahepekiz/Desktop/whit-release/backend/media/;"
echo ""
echo "   And change them to:"
echo "   alias /var/www/whit/backend/staticfiles/;"
echo "   alias /var/www/whit/backend/media/;"