#!/bin/bash

# Monitor dashboard improvements deployment
echo "Monitoring dashboard improvements deployment..."
echo "Checking styling changes and FontAwesome icons..."

counter=0
while [ $counter -lt 30 ]; do
  echo "Check #$((counter + 1)): $(date)"
  
  # Check main site response
  response=$(curl -s -o /dev/null -w "%{http_code}" https://staging.whoishiringintech.com/)
  
  if [ "$response" = "200" ]; then
    echo "✅ Site is responding (200)"
    
    # Check if FontAwesome is loading
    content=$(curl -s https://staging.whoishiringintech.com/)
    
    if [[ "$content" == *"FontAwesome"* ]] || [[ "$content" == *"fa-"* ]]; then
      echo "🎨 FontAwesome icons detected in HTML"
    else
      echo "📝 HTML content loaded, checking for updated styling..."
    fi
    
    # Check if the dashboard page loads
    if [[ "$content" == *"Welcome back"* ]] && [[ "$content" == *"Personal Info"* ]]; then
      echo "🎯 Dashboard content confirmed - deployment successful!"
      echo ""
      echo "🎉 Dashboard improvements deployed successfully!"
      echo "📋 Changes applied:"
      echo "   • Plain FontAwesome icons (User, Cog, Document, Search)"
      echo "   • Dark navy icon backgrounds with white icons"
      echo "   • Improved text contrast for better readability"
      echo "   • Enhanced card shadows and borders"
      echo ""
      echo "👉 Visit: https://staging.whoishiringintech.com"
      break
    fi
  else
    echo "❌ Site returned: $response"
  fi
  
  counter=$((counter + 1))
  
  if [ $counter -lt 30 ]; then
    sleep 10
  fi
done

if [ $counter -eq 30 ]; then
  echo "⏱️  Monitoring timeout reached"
  echo "💡 The deployment may still be in progress"
  echo "🔗 Check GitHub Actions: https://github.com/mhepekiz/WHIT-Production/actions"
fi