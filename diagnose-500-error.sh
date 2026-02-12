#!/bin/bash

echo "🚨 Diagnosing 500 Internal Server Error"
echo "======================================="

echo "1. Testing main staging site:"
echo -n "Frontend (https://staging.whoishiringintech.com): "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/

echo -e "\n2. Testing API endpoints:"
echo -n "Health endpoint: "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/api/health/

echo -n "Companies API: "  
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/api/companies/

echo -n "API root: "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/api/

echo -e "\n3. Getting actual error content:"
echo "Main site response:"
curl -s https://staging.whoishiringintech.com/ | head -20

echo -e "\n4. Checking static files:"
echo -n "CSS files: "
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://staging.whoishiringintech.com/static/

echo -e "\n5. Testing without SSL to isolate issues:"
echo -n "HTTP (port 80): "
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://staging.whoishiringintech.com/ 2>/dev/null || echo "Failed"

echo -e "\n6. DNS and Connection Test:"
echo "Server IP: $(dig +short staging.whoishiringintech.com)"
echo "Port 443 connectivity:"
nc -zv staging.whoishiringintech.com 443 2>&1 | head -1

echo "Port 80 connectivity:"  
nc -zv staging.whoishiringintech.com 80 2>&1 | head -1

echo -e "\n=== DIAGNOSIS SUMMARY ==="
echo "If main site is 500 but API endpoints are 404, likely Django isn't running"
echo "If all endpoints are 500, likely nginx configuration issue"
echo "If connection fails, DNS or firewall issue"