from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import json

def health_check(request):
    """
    Health check endpoint for monitoring and load balancer
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check if we can access basic settings
        debug_status = settings.DEBUG
        
        response_data = {
            "status": "healthy",
            "database": "connected",
            "debug": debug_status,
            "version": "1.0.0"
        }
        
        return JsonResponse(response_data, status=200)
    
    except Exception as e:
        response_data = {
            "status": "unhealthy",
            "error": str(e)
        }
        return JsonResponse(response_data, status=500)