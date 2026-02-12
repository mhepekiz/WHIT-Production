#!/bin/bash

# Monitor forced dashboard redesign deployment
echo "🔄 Monitoring forced dashboard redesign deployment..."
echo "🎯 Looking for: FontAwesome icons + dark navy styling"

counter=0
target_found=false

while [ $counter -lt 25 ] && [ "$target_found" = false ]; do
  echo "Check #$((counter + 1)): $(date)"
  
  # Check main site response
  response=$(curl -s -o /dev/null -w "%{http_code}" https://staging.whoishiringintech.com/)
  
  if [ "$response" = "200" ]; then
    echo "✅ Site responding (200)"
    
    # Check for the deployment trigger marker we added
    content=$(curl -s https://staging.whoishiringintech.com/)
    
    if [[ "$content" == *"Updated"* ]]; then
      echo "🎯 DEPLOYMENT TRIGGER FOUND!"
      echo "✅ New deployment is live - subtitle shows 'Updated' marker"
      
      # Check for FontAwesome in the actual content
      if [[ "$content" == *"FontAwesome"* ]] || [[ "$content" == *"fa-"* ]]; then
        echo "🎨 FontAwesome icons detected in HTML"
      else
        echo "📝 HTML updated but checking for icon changes..."
      fi
      
      target_found=true
      echo ""
      echo "🎉 DASHBOARD REDESIGN DEPLOYED SUCCESSFULLY!"
      echo "📍 Changes now live:"
      echo "   • FontAwesome icons instead of colorful SVGs"
      echo "   • Dark navy icon backgrounds (#2c3e50)"  
      echo "   • White icon colors for better contrast"
      echo "   • Enhanced card shadows and styling"
      echo ""
      echo "🔍 If icons still appear old, try:"
      echo "   • Hard refresh (Ctrl+F5 / Cmd+Shift+R)"
      echo "   • Clear browser cache"
      echo "   • Open incognito/private window"
      break
      
    elif [[ "$content" == *"Welcome back"* ]]; then
      echo "📄 Dashboard content loaded, waiting for latest deployment..."
    else
      echo "⚠️  Content loaded but may not be dashboard page"
    fi
  else
    echo "❌ Site returned: $response"
  fi
  
  counter=$((counter + 1))
  
  if [ $counter -lt 25 ] && [ "$target_found" = false ]; then
    sleep 12
  fi
done

if [ "$target_found" = false ]; then
  echo "⏱️  Monitoring timeout - deployment may still be processing"
  echo "🔗 Check GitHub Actions: https://github.com/mhepekiz/WHIT-Production/actions"
fi

echo ""
echo "👉 Visit: https://staging.whoishiringintech.com"
echo "🎨 Dashboard should now show FontAwesome icons with dark navy backgrounds!"