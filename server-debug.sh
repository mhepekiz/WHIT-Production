#!/bin/bash

echo "🚨 WHIT Staging Server Diagnostic & Fix Script"
echo "=============================================="
echo "Run this on the server: ssh user@45.79.211.144"
echo ""

echo "1. Check if services are running:"
sudo systemctl status nginx
sudo systemctl status whit
echo ""

echo "2. Check if processes are listening on required ports:"
sudo netstat -tulnp | grep :80
sudo netstat -tulnp | grep :443
sudo netstat -tulnp | grep :8000
echo ""

echo "3. Check nginx configuration:"
sudo nginx -t
echo ""

echo "4. Check if deployment files exist in correct location:"
ls -la /var/www/whit/
ls -la /var/www/whit/frontend/
ls -la /var/www/whit/backend/
echo ""

echo "5. Check recent logs:"
echo "--- Nginx Logs ---"
sudo tail -20 /var/log/nginx/error.log
echo "--- WHIT Service Logs ---" 
sudo journalctl -u whit --no-pager -n 20
echo ""

echo "🔧 COMMON FIXES:"
echo ""
echo "If nginx is not running:"
echo "  sudo systemctl start nginx"
echo "  sudo systemctl enable nginx"
echo ""
echo "If whit service is not running:"
echo "  sudo systemctl start whit"
echo "  sudo systemctl enable whit"
echo ""
echo "If SSL certificate issues:"
echo "  sudo certbot --nginx -d staging.whoishiringintech.com"
echo ""
echo "If deployment path issues persist:"
echo "  sudo ln -sf /var/www/whit /var/www/WHIT"
echo ""
echo "Restart all services:"
echo "  sudo systemctl restart nginx"
echo "  sudo systemctl restart whit"