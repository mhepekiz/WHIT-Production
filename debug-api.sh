#!/bin/bash

echo "🔍 Django API Debug Script"
echo "========================="

echo "1. Checking Django service status:"
systemctl status whit --no-pager

echo -e "\n2. Checking what ports Django is running on:"
ps aux | grep gunicorn | grep -v grep
netstat -tulnp | grep :800

echo -e "\n3. Testing local API endpoints:"
echo "Testing port 8000:"
curl -s -o /dev/null -w "HTTP %{http_code} - %{url_effective}\n" http://localhost:8000/api/companies/ || echo "Port 8000 failed"

echo "Testing port 8003:"
curl -s -o /dev/null -w "HTTP %{http_code} - %{url_effective}\n" http://localhost:8003/api/companies/ || echo "Port 8003 failed"

echo -e "\n4. Checking Django logs:"
journalctl -u whit --no-pager -n 10

echo -e "\n5. Testing database connection:"
cd /var/www/whit/backend
sudo -u www-data ./venv/bin/python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whit.settings')
django.setup()
from companies.models import Company
print(f'Companies in database: {Company.objects.count()}')
if Company.objects.exists():
    for company in Company.objects.all()[:3]:
        print(f'- {company.name if hasattr(company, \"name\") else company}')
"

echo -e "\n6. Checking nginx proxy configuration:"
grep -n "proxy_pass.*8000" /etc/nginx/sites-enabled/whit || echo "No port 8000 proxy found"
grep -n "proxy_pass.*8003" /etc/nginx/sites-enabled/whit || echo "No port 8003 proxy found"

echo -e "\n7. Testing external API access:"
curl -s -I https://staging.whoishiringintech.com/api/companies/ | head -3

echo -e "\n=== Debug Summary ==="
echo "If Django is running on port 8003 but nginx proxies to 8000, that's the problem!"
echo "If companies count is 0, we need to load sample data."
echo "Check the HTTP status codes above for specific issues."