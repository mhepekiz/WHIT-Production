from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Company, Function, WorkEnvironment, AdSlot, SiteSettings, FormLayout
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    FunctionSerializer,
    WorkEnvironmentSerializer
)
from .filters import CompanyFilter


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Company CRUD operations.
    
    Provides list, retrieve, create, update, and delete operations.
    Supports filtering, searching, and ordering.
    """
    
    queryset = Company.objects.all().prefetch_related('functions')
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ['name', 'city', 'functions__name', 'country']
    ordering_fields = ['name', 'country', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return CompanyListSerializer
        return CompanySerializer
    
    @action(detail=False, methods=['get'])
    def filters(self, request):
        """
        Get available filter options.
        Returns unique values for countries, states, cities, functions, and work environments.
        """
        # Get unique countries
        countries = Company.objects.values_list('country', flat=True).distinct().order_by('country')
        
        # Get unique states (non-null)
        states = Company.objects.exclude(state__isnull=True).exclude(state='').values_list('state', flat=True).distinct().order_by('state')
        
        # Get unique cities (non-null)
        cities = Company.objects.exclude(city__isnull=True).exclude(city='').values_list('city', flat=True).distinct().order_by('city')
        
        # Get unique functions
        functions = Function.objects.all().values('id', 'name', 'color', 'text_color').order_by('name')
        
        # Get unique work environments
        all_work_envs = set()
        for company in Company.objects.all():
            all_work_envs.update(company.get_work_environment_list())
        
        return Response({
            'countries': list(countries),
            'states': list(states),
            'cities': list(cities),
            'functions': list(functions),
            'work_environments': sorted(list(all_work_envs)),
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics about companies."""
        total_companies = Company.objects.count()
        active_companies = Company.objects.filter(status='Active').count()
        engineering_positions = Company.objects.filter(engineering_positions=True).count()
        countries_count = Company.objects.values('country').distinct().count()
        
        return Response({
            'total_companies': total_companies,
            'active_companies': active_companies,
            'engineering_positions': engineering_positions,
            'countries_count': countries_count,
        })


class FunctionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Function model (read-only)."""
    
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer


class WorkEnvironmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for WorkEnvironment model (read-only)."""
    
    queryset = WorkEnvironment.objects.all()
    serializer_class = WorkEnvironmentSerializer


class AdSlotViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving ad slots (admin can manage via Django admin)."""
    
    queryset = AdSlot.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active ad slots with support for both code and image banners."""
        ad_slots = AdSlot.objects.filter(is_active=True)
        data = {}
        for ad in ad_slots:
            # Check if banner image exists (prioritize image over code)
            if ad.banner_image:
                # Build absolute URL for banner image
                image_url = request.build_absolute_uri(ad.banner_image.url)
                data[ad.slot_name] = {
                    'type': 'image',
                    'image_url': image_url,
                    'link': ad.banner_link or '#',
                    'alt_text': ad.banner_alt_text or 'Advertisement',
                    'open_in_new_tab': ad.open_in_new_tab
                }
            elif ad.ad_code:
                data[ad.slot_name] = {
                    'type': 'code',
                    'code': ad.ad_code
                }
            else:
                data[ad.slot_name] = None
        return Response(data)


class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving site settings."""
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current site settings."""
        settings = SiteSettings.load()
        return Response({
            'companies_per_page': settings.companies_per_page,
            'companies_per_group': settings.companies_per_group,
            'label_size': settings.label_size,
        })


class FormLayoutViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving form layout configurations."""
    
    queryset = FormLayout.objects.all()
    
    @action(detail=False, methods=['get'])
    def by_page(self, request):
        """Get form layout by page name."""
        page_name = request.query_params.get('page', None)
        if not page_name:
            return Response({'error': 'page parameter is required'}, status=400)
        
        try:
            layout = FormLayout.objects.get(page_name=page_name)
            
            # Build full URL for image
            image_url = layout.get_image_url()
            if image_url and not image_url.startswith('http'):
                # Build absolute URL
                image_url = request.build_absolute_uri(image_url)
            
            data = {
                'page_name': layout.page_name,
                'form_position': layout.form_position,
                'side_heading': layout.side_heading,
                'side_heading_tag': layout.side_heading_tag,
                'side_subheading': layout.side_subheading,
                'side_subheading_tag': layout.side_subheading_tag,
                'side_text': layout.side_text,
                'side_text_tag': layout.side_text_tag,
                'side_image_url': image_url,
                'text_overlay_position': layout.text_overlay_position,
                'background_color': layout.background_color,
                'text_color': layout.text_color,
            }
            return Response(data)
        except FormLayout.DoesNotExist:
            # Return default center layout if not configured
            return Response({
                'page_name': page_name,
                'form_position': 'center',
                'side_heading': '',
                'side_heading_tag': 'h1',
                'side_subheading': '',
                'side_subheading_tag': 'h2',
                'side_text': '',
                'side_text_tag': 'p',
                'side_image_url': None,
                'text_overlay_position': 'center-center',
                'background_color': '#ffffff',
                'text_color': '#000000',
            })
