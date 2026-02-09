from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    recruiter_register, recruiter_login,
    RecruiterPackageViewSet, RecruiterProfileViewSet,
    JobOpeningViewSet, JobApplicationViewSet,
    CandidateSearchViewSet, RecruiterMessageViewSet,
    RecruiterDashboardViewSet, export_company_data
)

router = DefaultRouter()
router.register(r'packages', RecruiterPackageViewSet, basename='recruiter-package')
router.register(r'profile', RecruiterProfileViewSet, basename='recruiter-profile')
router.register(r'jobs', JobOpeningViewSet, basename='job-opening')
router.register(r'applications', JobApplicationViewSet, basename='job-application')
router.register(r'candidates', CandidateSearchViewSet, basename='candidate-search')
router.register(r'messages', RecruiterMessageViewSet, basename='recruiter-message')
router.register(r'dashboard', RecruiterDashboardViewSet, basename='recruiter-dashboard')

urlpatterns = [
    path('register/', recruiter_register, name='recruiter-register'),
    path('login/', recruiter_login, name='recruiter-login'),
    path('export/<int:company_id>/', export_company_data, name='export-company-data'),
    path('', include(router.urls)),
]
