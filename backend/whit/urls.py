"""
URL configuration for whit project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .health import health_check

@require_GET
def root_handler(request):
    """
    Root endpoint handler - returns API information
    """
    return JsonResponse({
        "message": "Who Is Hiring In Tech API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/api/health/",
            "companies": "/api/companies/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', root_handler, name='root'),
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/', include('companies.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/recruiters/', include('recruiters.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = 'Who Is Hiring In Tech - Admin'
admin.site.site_title = 'WHIT Admin'
admin.site.index_title = 'Manage Companies'
