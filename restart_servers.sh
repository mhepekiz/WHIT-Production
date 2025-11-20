#!/bin/bash

# Kill existing servers
echo "Stopping existing servers..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Clear log files
echo "" > /tmp/django.log
echo "" > /tmp/vite.log

# Wait a moment
sleep 2

# Start Django
echo "Starting Django..."
cd /Users/mustafahepekiz/Desktop/whit/backend
nohup python manage.py runserver 8000 > /tmp/django.log 2>&1 &
DJANGO_PID=$!
echo "Django started with PID: $DJANGO_PID"

# Wait for Django to start
sleep 3

# Start Vite
echo "Starting Vite..."
cd /Users/mustafahepekiz/Desktop/whit/frontend
nohup npm run dev > /tmp/vite.log 2>&1 &
VITE_PID=$!
echo "Vite started with PID: $VITE_PID"

# Wait for Vite to start
sleep 3

echo "Servers started!"
echo "Django: http://localhost:8000 (PID: $DJANGO_PID)"
echo "Vite: http://localhost:5173 (PID: $VITE_PID)"
echo "Django logs: tail -f /tmp/django.log"
echo "Vite logs: tail -f /tmp/vite.log"
