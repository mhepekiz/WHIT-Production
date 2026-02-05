from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, FunctionViewSet, WorkEnvironmentViewSet, AdSlotViewSet, SiteSettingsViewSet, FormLayoutViewSet, homepage_sections_api
from .debug_views import debug_status

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'functions', FunctionViewSet, basename='function')
router.register(r'work-environments', WorkEnvironmentViewSet, basename='work-environment')
router.register(r'ad-slots', AdSlotViewSet, basename='ad-slot')
router.register(r'site-settings', SiteSettingsViewSet, basename='site-settings')
router.register(r'form-layouts', FormLayoutViewSet, basename='form-layout')

urlpatterns = [
    path('', include(router.urls)),
    path('homepage-sections/', homepage_sections_api, name='homepage-sections'),
    path('debug-status/', debug_status, name='debug-status'),
]
