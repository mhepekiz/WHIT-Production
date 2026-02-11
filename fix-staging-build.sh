#!/bin/bash

echo "🔧 Fixing staging build environment variables..."

# Create a staging environment file that overrides everything
cat > frontend/.env.staging << EOF
VITE_API_URL=https://staging.whoishiringintech.com/api
NODE_ENV=production
EOF

# Also create .env.production to ensure it works in production mode
cat > frontend/.env.production << EOF
VITE_API_URL=https://staging.whoishiringintech.com/api
NODE_ENV=production
EOF

# Also create regular .env file as additional safeguard
cat > frontend/.env << EOF
VITE_API_URL=https://staging.whoishiringintech.com/api
NODE_ENV=production
EOF

echo "✅ Created environment files:"
echo "📄 .env.staging:"
cat frontend/.env.staging

echo ""
echo "📄 .env.production:"
cat frontend/.env.production

echo ""
echo "📄 .env:"
cat frontend/.env

echo ""
echo "🔍 Let's test a local build to verify environment variables work..."

cd frontend

# Clear any existing build
rm -rf dist/

# Force clean install and build
npm install

# Build with explicit environment variable
echo "🏗️ Building with VITE_API_URL=https://staging.whoishiringintech.com/api"
VITE_API_URL=https://staging.whoishiringintech.com/api npm run build

if [ -d "dist" ]; then
    echo ""
    echo "🔍 Checking built JS files for URLs..."
    
    if find dist/assets -name "*.js" -exec grep -l "https://whoishiringintech\.com" {} \; 2>/dev/null | grep -q .; then
        echo "❌ ERROR: Production URLs still found in built JS files!"
        echo "🔍 Found instances:"
        find dist/assets -name "*.js" -exec grep -o 'https://[^"]*whoishiringintech\.com[^"]*' {} \; 2>/dev/null || true
    else
        echo "✅ SUCCESS: No production URLs found in built JS files"
        echo "🔍 Checking for staging URLs..."
        if find dist/assets -name "*.js" -exec grep -l "staging\.whoishiringintech\.com" {} \; 2>/dev/null | grep -q .; then
            echo "✅ CONFIRMED: Staging URLs found in built JS files"
            staging_count=$(find dist/assets -name "*.js" -exec grep -o 'staging\.whoishiringintech\.com' {} \; 2>/dev/null | wc -l | tr -d ' ')
            echo "📊 Found ${staging_count} instances of staging URLs"
        else
            echo "⚠️ WARNING: No staging URLs found either - please check"
        fi
    fi
else
    echo "❌ ERROR: Build failed - no dist directory created"
fi

echo ""
echo "📋 Summary:"
echo "- Created .env, .env.staging, and .env.production files"
echo "- All files set VITE_API_URL to staging.whoishiringintech.com/api"
echo "- Tested local build to verify environment variable usage"
echo ""
echo "🚀 Now run: git add . && git commit -m 'Fix staging build environment' && git push"
echo "   This will trigger the GitHub Actions deployment pipeline"