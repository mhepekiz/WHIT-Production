#!/bin/bash

# Start script for Who Is Hiring In Tech
# This script starts both backend and frontend servers

echo "🚀 Starting Who Is Hiring In Tech..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Start backend
echo "Starting Django backend..."
cd backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 2

# Start frontend
echo "Starting React frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✨ Application is starting..."
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for processes
wait
