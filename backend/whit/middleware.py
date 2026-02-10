from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForAPIMiddleware(MiddlewareMixin):
    """
    Disable CSRF protection for API endpoints
    """
    def process_request(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None


class CSRFExemptAdminMiddleware(MiddlewareMixin):
    """
    Exempt admin from CSRF checks to prevent 400 errors
    """
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Allow admin access without CSRF checks
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None