## Manual Staging Server Fix Instructions

### Step 1: Upload the fix script to your server
Run this on your local machine:
```bash
scp complete-staging-fix.sh root@47.221.151.132:/tmp/fix.sh
```

### Step 2: Connect to server and run the fix
```bash
ssh root@47.221.151.132
chmod +x /tmp/fix.sh
/tmp/fix.sh
```

### Alternative: Direct execution (copy-paste this entire block into server terminal)
```bash
#!/bin/bash

echo "🔧 COMPLETE STAGING SERVER FIX"
echo "============================="

# Navigate to project directory
cd /var/www/whit || { echo "❌ Project directory not found"; exit 1; }

echo "📁 Current directory: $(pwd)"

echo "🐍 Python Setup"
echo "==============="

# Install tools
apt update
apt install -y python3-pip python3-venv

# Create virtual environment
python3 -m venv venv_new
source venv_new/bin/activate

echo "📦 Installing Backend Dependencies"
cd backend
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Database Setup"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "🚀 Starting Backend Server"
pkill -f 'manage.py runserver' || true
sleep 3
nohup python manage.py runserver 127.0.0.1:8000 > /var/log/whit-backend.log 2>&1 &

echo "🌐 Frontend Build"
cd ../frontend
echo 'VITE_API_URL=https://staging.whoishiringintech.com/api' > .env
npm install
export VITE_API_URL=https://staging.whoishiringintech.com/api
npm run build

echo "✅ DEPLOYMENT COMPLETED!"
echo "Test: curl http://127.0.0.1:8000/api/companies/"
```

### Quick Test Commands
After running the fix:
```bash
# Check if backend is running
curl http://127.0.0.1:8000/api/companies/

# Check processes
ps aux | grep manage.py

# Check logs
tail -f /var/log/whit-backend.log
```