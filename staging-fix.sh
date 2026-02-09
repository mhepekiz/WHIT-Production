#!/bin/bash
cd /var/www/whit
echo 'VITE_API_URL=https://staging.whoishiringintech.com/api' > frontend/.env
cd frontend
export VITE_API_URL=https://staging.whoishiringintech.com/api
npm run build
cd ../backend
pkill -f 'manage.py runserver' || true
sleep 2
export CORS_ALLOWED_ORIGINS='https://staging.whoishiringintech.com,http://localhost:3000'
export ALLOWED_HOSTS='staging.whoishiringintech.com,45.79.211.144,localhost,127.0.0.1'
nohup python manage.py runserver 127.0.0.1:8000 > /var/log/whit-backend.log 2>&1 &
echo '✅ Staging server fixes applied!'