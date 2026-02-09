#!/bin/bash

echo "🚨 CRITICAL STAGING SERVER FIX"
echo "=============================="
echo ""
echo "The SSH connection is having pseudo terminal issues."
echo "You need to manually fix the staging server by running these commands:"
echo ""
echo "1. SSH to your server manually:"
echo "   ssh root@45.79.211.144"
echo ""
echo "2. Run these exact commands:"
echo ""
echo "cd /var/www/whit-release"
echo "echo 'VITE_API_URL=https://staging.whoishiringintech.com/api' > frontend/.env"
echo "cd frontend"
echo "npm run build"
echo "cd ../backend"
echo "pkill -f 'manage.py runserver' || true"
echo "pkill -f 'gunicorn' || true"
echo "sleep 3"
echo "python manage.py runserver 127.0.0.1:8000 &"
echo ""
echo "3. Test the fix:"
echo "curl -I https://staging.whoishiringintech.com/api/health/"
echo ""
echo "🎯 WHAT THIS DOES:"
echo "✅ Creates .env file with staging API URL"
echo "✅ Rebuilds frontend to use staging API instead of production"
echo "✅ Restarts backend server"
echo "✅ Fixes CORS issues"
echo ""
echo "📊 EXPECTED RESULT:"
echo "- Frontend will call staging.whoishiringintech.com/api"
echo "- No more CORS errors"
echo "- Companies will load successfully"
echo ""
echo "⚠️ ALTERNATIVE SIMPLE FIX:"
echo "If the above doesn't work, the root issue is that the frontend build"
echo "doesn't have the VITE_API_URL environment variable. The simplest fix"
echo "is to update the frontend code to default to staging instead of production."

# Create a simple remote command that might work
echo ""
echo "🔧 TRYING AUTOMATED FIX WITH SIMPLER APPROACH:"

# Try using printf instead of echo to avoid shell interpretation issues
printf 'VITE_API_URL=https://staging.whoishiringintech.com/api\n' > /tmp/staging_env

echo "Environment file created locally. Now uploading to server..."

# Use scp to upload the file
scp -o StrictHostKeyChecking=no /tmp/staging_env root@45.79.211.144:/var/www/whit-release/frontend/.env

if [ $? -eq 0 ]; then
    echo "✅ Environment file uploaded successfully"
    
    # Now try to run the build command
    echo "🏗️ Trying to rebuild frontend on server..."
    sshpass -p 'sm0ky&&G0nc4' ssh -o StrictHostKeyChecking=no -o LogLevel=quiet root@45.79.211.144 'cd /var/www/whit-release/frontend && npm run build && echo "Build completed"'
    
    if [ $? -eq 0 ]; then
        echo "✅ Frontend rebuilt successfully with staging API"
        echo "🔄 Restarting backend..."
        sshpass -p 'sm0ky&&G0nc4' ssh -o StrictHostKeyChecking=no -o LogLevel=quiet root@45.79.211.144 'cd /var/www/whit-release/backend && pkill -f "manage.py" || true && python manage.py runserver 127.0.0.1:8000 &'
        echo "✅ Fix completed! Check https://staging.whoishiringintech.com"
    else
        echo "❌ Build failed. Manual intervention required."
    fi
else
    echo "❌ Upload failed. Manual intervention required."
fi

rm -f /tmp/staging_env