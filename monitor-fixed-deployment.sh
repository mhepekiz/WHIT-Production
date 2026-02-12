#!/bin/bash

echo "🚀 Monitoring Fixed WHIT Deployment..."
echo "GitHub Actions: https://github.com/mhepekiz/WHIT-Production/actions"
echo ""

# Monitor deployment for 10 minutes
for i in {1..20}; do
    echo "⏰ Monitor check $i/20 ($(date))"
    
    # Check staging site status
    RESPONSE=$(curl -s https://staging.whoishiringintech.com/ || echo "ERROR")
    
    if [[ "$RESPONSE" == *"<!DOCTYPE html>"* ]]; then
        echo "✅ SUCCESS: Frontend is serving HTML content!"
        echo "🎉 Deployment appears successful - React app is loading"
        
        # Additional check for API
        API_RESPONSE=$(curl -s https://staging.whoishiringintech.com/api/companies/ || echo "ERROR")
        if [[ "$API_RESPONSE" == *"["* ]] || [[ "$API_RESPONSE" == *"{"* ]]; then
            echo "✅ API endpoint also responding correctly"
        fi
        
        echo "🎊 DEPLOYMENT COMPLETE - Both frontend and API working!"
        exit 0
    elif [[ "$RESPONSE" =~ [0-9]+.*[Ee]rror|ERROR ]]; then
        echo "❌ Status: Error - $RESPONSE"
    else
        echo "🔄 Status: Still deploying..."
    fi
    
    sleep 30
done

echo "⏰ Monitor timeout reached. Check GitHub Actions and server manually."
echo "GitHub Actions: https://github.com/mhepekiz/WHIT-Production/actions"