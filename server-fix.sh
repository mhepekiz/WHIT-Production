#!/bin/bash
echo "=== DJANGO PORT FIX ==="
echo "Checking port 8000..."
netstat -tlnp | grep :8000 || echo "No process found on port 8000"

echo "Killing any Django processes..."
pkill -f "manage.py runserver" || echo "No Django processes found"

echo "Force killing port 8000..."
fuser -k 8000/tcp || echo "No process to kill on port 8000"

echo "Waiting 3 seconds..."
sleep 3

echo "Starting Django server..."
cd /var/www/whit/backend
source ../venv_new/bin/activate
nohup python manage.py runserver 127.0.0.1:8000 > /var/log/whit-backend.log 2>&1 &
DJANGO_PID=$!

echo "Django started with PID: $DJANGO_PID"
echo "Waiting 5 seconds..."
sleep 5

echo "Testing API..."
curl -f http://127.0.0.1:8000/api/companies/ && echo "✅ API Working!" || echo "❌ API Failed"

echo "Checking log..."
tail -5 /var/log/whit-backend.log