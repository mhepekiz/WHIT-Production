#!/bin/bash

echo "🔄 Monitoring staging deployment and health..."
echo "GitHub Actions should be deploying with corrected directory paths now"
echo ""

# Function to check staging status
check_staging() {
    local status_code=$(curl -o /dev/null -s -w "%{http_code}" --max-time 15 https://staging.whoishiringintech.com/)
    echo "Frontend Status: $status_code"
    
    if [ "$status_code" = "200" ]; then
        echo "✅ SUCCESS: Staging frontend is working!"
        return 0
    elif [ "$status_code" = "500" ]; then
        echo "❌ Still getting 500 error"
        return 1
    else
        echo "⚠️ Got status: $status_code"
        return 1
    fi
}

echo "Waiting for deployment to complete (typically takes 3-5 minutes)..."
echo ""

# Check every 30 seconds for up to 10 minutes
for i in {1..20}; do
    echo "Check $i of 20 - $(date)"
    
    if check_staging; then
        echo ""
        echo "🎉 Deployment successful! The directory path fix resolved the 500 error."
        echo ""
        echo "✅ Final verification:"
        curl -I https://staging.whoishiringintech.com/api/companies/ 2>/dev/null | head -1
        echo ""
        break
    fi
    
    if [ $i -eq 20 ]; then
        echo ""
        echo "⏰ Timeout reached. Check GitHub Actions for deployment status:"
        echo "https://github.com/mhepekiz/WHIT-Production/actions"
        break
    fi
    
    echo "   Waiting 30 seconds before next check..."
    sleep 30
    echo ""
done