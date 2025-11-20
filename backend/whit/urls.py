"""
URL configuration for whit project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
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
