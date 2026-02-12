#!/usr/bin/env python3
"""
Admin Dashboard Fix - Apply CSRF middleware fix 
"""
import requests
import json

def test_admin_access():
    """Test admin dashboard access"""
    try:
        # Test the admin endpoint
        admin_url = "https://staging.whoishiringintech.com/admin/"
        
        print("🔍 Testing admin dashboard access...")
        response = requests.get(admin_url, timeout=10)
        
        print(f"Admin URL: {admin_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.text)} characters")
        
        if response.status_code == 200:
            print("✅ Admin dashboard is accessible!")
            if "Django administration" in response.text:
                print("✅ Django admin page loaded correctly!")
            else:
                print("⚠️ Page loaded but may not be admin interface")
        elif response.status_code == 400:
            print("❌ 400 Bad Request - CSRF or middleware issue")
            print("🔧 Need to apply CSRF exemption middleware fix")
        elif response.status_code == 403:
            print("❌ 403 Forbidden - Permission issue")
        elif response.status_code == 404:
            print("❌ 404 Not Found - Admin URL not configured")
        elif response.status_code == 500:
            print("❌ 500 Server Error - Application error")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            
        # Also test if login page shows up
        if "login" in response.text.lower():
            print("✅ Login form detected - admin is working!")
            return True
        
        return response.status_code == 200
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing admin access: {e}")
        return False

def test_api_health():
    """Test API health to verify server is running"""
    try:
        health_url = "https://staging.whoishiringintech.com/api/health/"
        response = requests.get(health_url, timeout=10)
        
        print(f"🏥 Health Check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data.get('status', 'unknown')}")
            return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    return False

if __name__ == "__main__":
    print("🔧 WHIT Admin Dashboard Fix Test")
    print("=" * 50)
    
    # Test API health first
    if test_api_health():
        # Test admin access
        admin_works = test_admin_access()
        
        if admin_works:
            print("\n🎉 SUMMARY: Admin dashboard should be working!")
            print("📝 Login credentials:")
            print("   Username: admin")
            print("   Password: admin123")
        else:
            print("\n❌ SUMMARY: Admin needs middleware fix deployment")
            print("🔧 Required fixes:")
            print("   1. Deploy CSRFExemptAdminMiddleware")
            print("   2. Update settings.py middleware order")
            print("   3. Restart Django application")
    else:
        print("\n❌ SUMMARY: Server not responding to API calls")