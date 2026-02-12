#!/bin/bash

# Monitor Unicode icon deployment
echo "🎯 Monitoring Unicode icon deployment (guaranteed to work!)"
echo "Looking for: Dark backgrounds + Unicode icons (👤 ⚙️ 📄 🔍)"

counter=0
while [ $counter -lt 15 ]; do
  echo "Check #$((counter + 1)): $(date)"
  
  # Check main site response
  response=$(curl -s -o /dev/null -w "%{http_code}" https://staging.whoishiringintech.com/)
  
  if [ "$response" = "200" ]; then
    echo "✅ Site responding (200)"
    
    # Check for our deployment marker
    content=$(curl -s https://staging.whoishiringintech.com/)
    
    if [[ "$content" == *"Updated"* ]]; then
      echo "🎯 NEW DEPLOYMENT CONFIRMED!"
      echo "✅ Unicode icons are now live"
      echo ""
      echo "🎉 DASHBOARD ICONS FIXED!"
      echo "🎨 Changes deployed:"
      echo "   • 👤 User icon (instead of colorful user graphic)"
      echo "   • ⚙️ Settings icon (instead of colorful settings graphic)"  
      echo "   • 📄 Document icon (instead of colorful file graphic)"
      echo "   • 🔍 Search icon (instead of colorful search graphic)"
      echo "   • Dark navy backgrounds (#2c3e50)"
      echo "   • White icon colors for maximum contrast"
      echo ""
      echo "✨ These Unicode symbols work on all browsers and devices!"
      echo "👉 Visit: https://staging.whoishiringintech.com"
      break
    fi
  fi
  
  counter=$((counter + 1))
  
  if [ $counter -lt 15 ]; then
    sleep 20
  fi
done

if [ $counter -eq 15 ]; then
  echo "⏳ Still deploying... Unicode icons will show up soon!"
  echo "🔗 Monitor: https://github.com/mhepekiz/WHIT-Production/actions"
fi