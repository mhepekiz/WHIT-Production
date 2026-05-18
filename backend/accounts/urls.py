from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    CustomAuthToken,
    UserProfileViewSet,
    JobPreferenceViewSet,
    DashboardView,
    verify_email,
    resend_verification_email,
    password_reset_request,
    password_reset_confirm
)

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'job-preferences', JobPreferenceViewSet, basename='job-preferences')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('verify-email/', verify_email, name='verify-email'),
    path('verify-email/resend/', resend_verification_email, name='resend-verification-email'),
    path('password-reset/request/', password_reset_request, name='password-reset-request'),
    path('password-reset/confirm/', password_reset_confirm, name='password-reset-confirm'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]
