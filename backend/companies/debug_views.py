from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os
import sys
from django.conf import settings


@csrf_exempt
@require_http_methods(["GET"])
def debug_status(request):
    """Simple debug endpoint to check server status - staff only"""
    if not settings.DEBUG and not (request.user.is_authenticated and request.user.is_staff):
        return JsonResponse({"error": "Not authorized"}, status=403)
    try:
        from companies.models import Company, HowItWorksSection
        from django.db import connection
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "OK"
    except Exception as e:
        db_status = f"ERROR: {str(e)}"
    
    # Check if models exist
    try:
        company_count = Company.objects.count()
        model_status = "OK"
    except Exception as e:
        company_count = 0
        model_status = f"ERROR: {str(e)}"
    
    # Check homepage sections
    try:
        sections_count = HowItWorksSection.objects.count()
        sections_status = "OK" 
    except Exception as e:
        sections_count = 0
        sections_status = f"ERROR: {str(e)}"
    
    return JsonResponse({
        "status": "debug_endpoint_working",
        "python_version": sys.version,
        "django_debug": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "database_status": db_status,
        "company_count": company_count,
        "model_status": model_status,
        "sections_count": sections_count,
        "sections_status": sections_status,
        "working_directory": os.getcwd(),
        "database_path": os.path.join(settings.BASE_DIR, "db.sqlite3") if hasattr(settings, 'BASE_DIR') else "unknown"
    })