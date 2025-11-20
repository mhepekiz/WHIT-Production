import django_filters
from .models import Company


class CompanyFilter(django_filters.FilterSet):
    """Custom filter for Company model."""
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='iexact')
    state = django_filters.CharFilter(lookup_expr='iexact')
    city = django_filters.CharFilter(lookup_expr='icontains')
    functions = django_filters.CharFilter(method='filter_functions')
    work_environment = django_filters.CharFilter(method='filter_work_environment')
    status = django_filters.CharFilter(lookup_expr='iexact')
    
    class Meta:
        model = Company
        fields = ['name', 'country', 'state', 'city', 'functions', 'work_environment', 'status']
    
    def filter_functions(self, queryset, name, value):
        """Filter companies by function (case-insensitive, partial match)."""
        return queryset.filter(functions__name__icontains=value)
    
    def filter_work_environment(self, queryset, name, value):
        """Filter companies by work environment (case-insensitive, partial match)."""
        return queryset.filter(work_environment__icontains=value)
