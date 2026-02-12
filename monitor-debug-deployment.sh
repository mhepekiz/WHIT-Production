#!/bin/bash

echo "🔍 Monitoring DEBUGGING deployment - this will show detailed logs!"
echo "GitHub Actions: https://github.com/mhepekiz/WHIT-Production/actions"
echo ""
echo "🎯 What the debugging will reveal:"
echo "   • Node.js/npm versions on server"
echo "   • Vite build success/failure details"  
echo "   • Contents of dist/ directory after build"
echo "   • File copy operation results"
echo "   • Before/after states of /var/www/whit/frontend/"
echo ""

check_deployment() {
    local status_code=$(curl -o /dev/null -s -w "%{http_code}" --max-time 15 https://staging.whoishiringintech.com/)
    
    if [ "$status_code" = "200" ]; then
        echo "✅ SUCCESS! Frontend is working - check server to confirm built files"
        return 0
    else
        echo "Status: $status_code - deployment in progress or debugging error"
        return 1
    fi
}

echo "🏗️ Deployment with comprehensive debugging started..."
echo "This will take 3-5 minutes and provide detailed error information."
echo ""

for i in {1..12}; do
    echo "Check $i/12 - $(date)"
    
    if check_deployment; then
        echo ""
        echo "🎉 Deployment successful!"
        echo "Run: sudo ls -la /var/www/whit/frontend/"  
        echo "Should now show: index.html assets/ etc. (not just .env files)"
        break
    fi
    
    if [ $i -eq 12 ]; then
        echo ""
        echo "⚠️ Deployment still running. Check GitHub Actions for detailed debug logs:"
        echo "https://github.com/mhepekiz/WHIT-Production/actions"
        echo ""
        echo "The debug logs will show exactly where the process is failing."
        break
    fi
    
    echo "   Waiting 30s for next check..."
    sleep 30
    echo ""
done