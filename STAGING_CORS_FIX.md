# 🚨 URGENT: Staging Server CORS Fix

## Problem Diagnosed
Your staging server at `staging.whoishiringintech.com` has CORS errors because:
1. **Frontend is calling PRODUCTION API** (`whoishiringintech.com/api`) instead of staging API
2. **Missing environment variable** `VITE_API_URL` on staging server
3. **CORS policy** blocking cross-origin requests

## 🚀 IMMEDIATE FIX

### Option 1: Automated Fix (Recommended)
Run this single command from your local machine:
```bash
ssh root@45.79.211.144 "cd /var/www/whit-release && echo 'VITE_API_URL=https://staging.whoishiringintech.com/api' > frontend/.env && cd frontend && npm run build && cd ../backend && pkill -f 'manage.py' || true && nohup python manage.py runserver 127.0.0.1:8000 > /var/log/django.log 2>&1 &"
```

### Option 2: Manual Fix (If SSH has issues)
SSH to your server and run these commands:

```bash
# 1. Connect to staging server
ssh root@45.79.211.144

# 2. Navigate to project
cd /var/www/whit-release

# 3. Fix frontend API URL
echo 'VITE_API_URL=https://staging.whoishiringintech.com/api' > frontend/.env

# 4. Rebuild frontend with correct API URL
cd frontend
export VITE_API_URL=https://staging.whoishiringintech.com/api
npm run build

# 5. Restart backend with CORS fix
cd ../backend
pkill -f 'manage.py runserver' || true
nohup python manage.py runserver 127.0.0.1:8000 > /var/log/django.log 2>&1 &

# 6. Verify fix
curl -I https://staging.whoishiringintech.com/api/health/
```

## 🎯 Expected Results After Fix

✅ **Before Fix (Current Issue):**
- Frontend calls: `whoishiringintech.com/api` ❌
- CORS Error: "Access blocked by CORS policy" ❌  
- Error: "Failed to load companies. Please try again later." ❌

✅ **After Fix:**
- Frontend calls: `staging.whoishiringintech.com/api` ✅
- CORS: No errors ✅
- Companies: Load successfully ✅

## 🔍 How to Verify Fix Works

1. Open https://staging.whoishiringintech.com
2. Check browser console (F12 → Console)
3. Look for API calls - should go to `staging.whoishiringintech.com/api`
4. No CORS errors should appear
5. Companies should load without "Failed to load" error

## 🛠️ Root Cause Analysis

The issue happened because:
1. **CI/CD Pipeline** deployed code without setting `VITE_API_URL`
2. **Frontend defaults** to production API when env var is missing
3. **Cross-origin requests** from staging → production are blocked by CORS

## 🔄 Prevention for Future Deployments

To prevent this in the future, update your GitHub Actions workflow to include:

```yaml
- name: Set Environment Variables
  run: |
    echo "VITE_API_URL=https://staging.whoishiringintech.com/api" > frontend/.env
```

## 📊 Technical Details

**Current (Broken) Flow:**
```
staging.whoishiringintech.com (Frontend) 
    ↓ API Call
whoishiringintech.com/api (Production API) ❌ CORS Block
```

**Fixed Flow:**
```
staging.whoishiringintech.com (Frontend)
    ↓ API Call  
staging.whoishiringintech.com/api (Staging API) ✅ Same Origin
```

## 🚨 Priority Level: CRITICAL
This fix should be applied immediately as it's blocking all API functionality on staging.

---
**Status:** Ready to deploy
**Time to fix:** 2-3 minutes
**Impact:** Resolves all CORS errors and API loading issues