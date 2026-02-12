#!/bin/bash

echo "🔄 Monitoring deployment with FIXED file copying..."
echo "GitHub Actions should now copy BUILT files instead of source files"
echo ""

check_staging() {
    local status_code=$(curl -o /dev/null -s -w "%{http_code}" --max-time 15 https://staging.whoishiringintech.com/)
    echo "Frontend Status: $status_code"
    
    if [ "$status_code" = "200" ]; then
        echo "✅ SUCCESS: Frontend working! The fix resolved the issue."
        return 0
    else
        echo "⚠️ Status: $status_code (still deploying...)"
        return 1
    fi
}

echo "Waiting for GitHub Actions deployment (3-5 minutes)..."
echo "Check progress: https://github.com/mhepekiz/WHIT-Production/actions"
echo ""

for i in {1..15}; do
    echo "Check $i of 15 - $(date)"
    
    if check_staging; then
        echo ""
        echo "🎉 DEPLOYMENT SUCCESSFUL!"
        echo "The server should now have proper React build files with index.html"
        echo ""
        break
    fi
    
    if [ $i -eq 15 ]; then
        echo ""
        echo "⏰ Still deploying. Check GitHub Actions for detailed logs."
        break
    fi
    
    echo "   Next check in 30 seconds..."
    sleep 30
    echo ""
done