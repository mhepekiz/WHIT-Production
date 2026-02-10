#!/bin/bash

echo "🔍 DJANGO SERVER DIAGNOSTIC"
echo "==========================="

echo "📋 Checking backend log..."
if [ -f /var/log/whit-backend.log ]; then
    echo "Last 20 lines of error log:"
    tail -20 /var/log/whit-backend.log
else
    echo "❌ Log file not found at /var/log/whit-backend.log"
fi

echo ""
echo "🐍 Python Environment Check"
echo "==========================="

cd /var/www/whit/backend
source ../venv_new/bin/activate

echo "Python version: $(python --version 2>/dev/null || echo 'Not found')"
echo "Python3 version: $(python3 --version 2>/dev/null || echo 'Not found')" 
echo "Which python: $(which python 2>/dev/null || echo 'Not found')"
echo "Which python3: $(which python3 2>/dev/null || echo 'Not found')"

echo ""
echo "📦 Django Environment Check"
echo "=========================="

echo "Django version:"
python -c "import django; print(django.get_version())" 2>/dev/null || echo "❌ Django not found"

echo ""
echo "📁 File Permissions"
echo "=================="
ls -la manage.py
echo "Current directory: $(pwd)"

echo ""
echo "🗄️ Database Check"  
echo "================"
ls -la db.sqlite3 2>/dev/null || echo "❌ Database file not found"

echo ""
echo "⚙️ Django Settings Check"
echo "========================"
python manage.py check --deploy 2>/dev/null || python manage.py check 2>/dev/null || echo "❌ Django check failed"

echo ""
echo "🔧 Manual Start Attempt"
echo "======================"
echo "Trying to start Django manually to see error..."
timeout 10s python manage.py runserver 127.0.0.1:8000 || echo "Manual start failed or timed out"