#!/bin/bash

echo "🔍 Checking what's using port 8000..."
lsof -i :8000 || echo "No process found on port 8000"

echo ""
echo "🛑 Killing any Django processes..."
pkill -f 'manage.py runserver' || echo "No Django runserver processes found"
pkill -f 'python.*manage.py' || echo "No Python Django processes found"

echo ""
echo "🔫 Force killing port 8000..."
lsof -ti :8000 | xargs kill -9 2>/dev/null || echo "No processes to kill on port 8000"

echo ""
echo "⏳ Waiting for port to be freed..."
sleep 3

echo ""
echo "🚀 Starting Django server..."
cd /var/www/whit/backend
source ../venv_new/bin/activate
nohup python manage.py runserver 127.0.0.1:8000 > /var/log/whit-backend.log 2>&1 &
DJANGO_PID=$!

echo "Django server started with PID: $DJANGO_PID"

sleep 5

echo ""
echo "✅ Checking if server is running..."
if ps -p $DJANGO_PID > /dev/null; then
    echo "✅ Django server is running (PID: $DJANGO_PID)"
    echo "Testing health endpoint..."
    curl -f http://127.0.0.1:8000/api/companies/ && echo "" && echo "✅ Backend is working!" || echo "⚠️ Backend might be starting up..."
else
    echo "❌ Django server failed to start"
    echo "Error log:"
    tail -10 /var/log/whit-backend.log
fi