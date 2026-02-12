#!/bin/bash

echo "🚑 EMERGENCY SERVER FIXES - Staging 500 Error Recovery"
echo "==============================================="
echo ""

# Kill the background monitoring first 
pkill -f monitor-deployment.sh 2>/dev/null || true

echo "1️⃣ Checking GitHub Actions deployment status..."
echo "   Manual check: https://github.com/mhepekiz/WHIT-Production/actions"
echo ""

echo "2️⃣ Testing current API status..."
API_STATUS=$(curl -o /dev/null -s -w "%{http_code}" --max-time 10 https://staging.whoishiringintech.com/api/companies/)
echo "   API Status: $API_STATUS"

if [ "$API_STATUS" = "200" ]; then
    echo "   ✅ API is working - issue is likely frontend serving"
else
    echo "   ❌ API also failing - broader server issue"
fi
echo ""

echo "3️⃣ If deployment completed but still 500, run these commands on your server:"
echo "   SSH to staging server, then execute:"
echo ""
echo "   # Check if frontend files were deployed to correct location:"
echo "   sudo ls -la /var/www/whit/frontend/"
echo "   # Check overall whit directory structure:"
echo "   sudo ls -la /var/www/whit/"
echo ""
echo "   # Restart services:"
echo "   sudo systemctl restart whit"
echo "   sudo systemctl reload nginx"
echo ""
echo "   # Check service status:"
echo "   sudo systemctl status whit"
echo "   sudo systemctl status nginx"
echo ""
echo "   # Check nginx error logs:"
echo "   sudo tail -20 /var/log/nginx/staging.whoishiringintech.com.error.log"
echo ""

echo "4️⃣ MOST LIKELY FIXES:"
echo "   Option A) GitHub deployment still in progress (wait 2-5 more minutes)"
echo "   Option B) Services need manual restart after config change"  
echo "   Option C) Permission issues with new directory structure"
echo ""

# Try a comprehensive status check
echo "5️⃣ Quick diagnosis from here:"
echo ""
curl -s -I https://staging.whoishiringintech.com/ 2>&1 | head -5
echo ""
curl -s -I https://staging.whoishiringintech.com/api/companies/ 2>&1 | head -5  
echo ""

echo "🔧 Next steps:"
echo "   1. Check GitHub Actions progress"
echo "   2. If deployment completed, manually restart services"
echo "   3. Check server directory structure and permissions"