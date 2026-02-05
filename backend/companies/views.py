from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Company, Function, WorkEnvironment, AdSlot, SiteSettings, FormLayout, SponsorCampaign, HowItWorksSection, RecruiterSection
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    FunctionSerializer,
    WorkEnvironmentSerializer,
    HowItWorksSectionSerializer,
    RecruiterSectionSerializer
)
from .filters import CompanyFilter
from .services.sponsor_service import SponsorSelector


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
    ordering_fields = ['name', 'country', 'created_at', 'updated_at', 'is_sponsored', 'sponsor_order']
    ordering = ['-is_sponsored', 'sponsor_order', 'name']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return CompanyListSerializer
        return CompanySerializer
    
    def list(self, request, *args, **kwargs):
        """Override list to implement production sponsor placement algorithm."""
        # Get user hash for tracking and anti-fatigue
        user_hash = SponsorSelector.get_user_hash(request)
        
        # Get current filters from request
        filters = {}
        if hasattr(request, 'query_params'):
            filters.update({
                'country': request.query_params.get('country'),
                'function': request.query_params.get('functions'),
                'work_environment': request.query_params.get('work_environments'),
                'search': request.query_params.get('search'),
            })
            # Remove None values
            filters = {k: v for k, v in filters.items() if v}
        
        # Get all companies matching filters (organic only for main results)
        queryset = self.filter_queryset(self.get_queryset())
        organic_companies = queryset.filter(is_sponsored=False)
        
        # Get pagination info
        page = self.paginate_queryset(organic_companies)
        if page is not None:
            # Paginated response
            page_number = getattr(self.paginator.page, 'number', 1)
            page_key = SponsorSelector.build_page_key(request, filters, page_number)
            
            # Select sponsored campaign using production algorithm
            sponsored_campaign = SponsorSelector.pick_sponsored_campaign(
                filters=filters,
                user_hash=user_hash,
                page_number=page_number,
                request_path=request.path
            )
            
            # Build final results: [1 sponsored company] + [organic results]
            final_results = []
            if sponsored_campaign:
                final_results.append(sponsored_campaign.company)
                
                # Record impression (will be confirmed by frontend)
                # For now just log the selection, actual impression recorded via API
                
            final_results.extend(page)
            
            # Serialize with sponsored context
            serializer = self.get_serializer(final_results, many=True)
            response_data = serializer.data
            
            # Add sponsored campaign info to response
            if sponsored_campaign:
                response_data[0]['sponsored_campaign_id'] = sponsored_campaign.id
                
            return self.get_paginated_response(response_data)
        
        # Non-paginated fallback (e.g., homepage preview)
        page_key = SponsorSelector.build_page_key(request, filters, 1)
        
        # Select sponsored campaign for homepage
        sponsored_campaign = SponsorSelector.pick_sponsored_campaign(
            filters=filters,
            user_hash=user_hash,
            page_number=1,
            request_path=request.path
        )
        
        # Build results: [1 sponsored] + [organic results]
        final_results = []
        if sponsored_campaign:
            final_results.append(sponsored_campaign.company)
        
        # Get organic results (limit based on context)
        organic_limit = 12 if 'homepage' in request.get_full_path() else 30
        remaining_limit = organic_limit - len(final_results)
        final_results.extend(organic_companies[:remaining_limit])
        
        # Serialize with sponsored context
        serializer = self.get_serializer(final_results, many=True)
        response_data = serializer.data
        
        # Add sponsored campaign info to first result if present
        if sponsored_campaign and response_data:
            response_data[0]['sponsored_campaign_id'] = sponsored_campaign.id
            
        return Response(response_data)
    
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
    
    @action(detail=False, methods=['post'], url_path='sponsored/impression')
    def record_sponsored_impression(self, request):
        """Record impression for sponsored campaign."""
        try:
            campaign_id = request.data.get('campaign_id')
            page_url = request.data.get('page_url', '')
            
            if not campaign_id:
                return Response(
                    {'error': 'campaign_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get campaign
            try:
                campaign = SponsorCampaign.objects.get(id=campaign_id, status='active')
            except SponsorCampaign.DoesNotExist:
                return Response(
                    {'error': 'Invalid campaign_id'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get user hash and build page key
            user_hash = SponsorSelector.get_user_hash(request)
            filters = request.data.get('filters', {})
            page_number = request.data.get('page_number', 1)
            page_key = SponsorSelector.build_page_key(request, filters, page_number)
            
            # Record impression
            SponsorSelector.record_impression(
                campaign=campaign,
                user_hash=user_hash,
                page_key=page_key,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=SponsorSelector._get_client_ip(request),
                referrer=request.META.get('HTTP_REFERER', '')
            )
            
            return Response({'success': True})
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='sponsored/click')
    def record_sponsored_click(self, request):
        """Record click for sponsored campaign."""
        try:
            campaign_id = request.data.get('campaign_id')
            page_url = request.data.get('page_url', '')
            
            if not campaign_id:
                return Response(
                    {'error': 'campaign_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get campaign
            try:
                campaign = SponsorCampaign.objects.get(id=campaign_id, status='active')
            except SponsorCampaign.DoesNotExist:
                return Response(
                    {'error': 'Invalid campaign_id'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get user hash and build page key
            user_hash = SponsorSelector.get_user_hash(request)
            filters = request.data.get('filters', {})
            page_number = request.data.get('page_number', 1)
            page_key = SponsorSelector.build_page_key(request, filters, page_number)
            
            # Record click
            SponsorSelector.record_click(
                campaign=campaign,
                user_hash=user_hash,
                page_key=page_key,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=SponsorSelector._get_client_ip(request),
                referrer=request.META.get('HTTP_REFERER', '')
            )
            
            return Response({'success': True})
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        
        # Get user agent from request headers to detect mobile
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        is_mobile = any(keyword in user_agent for keyword in [
            'mobile', 'android', 'iphone', 'ipad', 'windows phone', 'blackberry'
        ])
        
        for ad in ad_slots:
            # Check if banner image exists (prioritize image over code)
            if ad.banner_image or ad.mobile_banner_image:
                # Choose appropriate banner based on device type
                banner_image = None
                if is_mobile and ad.mobile_banner_image:
                    banner_image = ad.mobile_banner_image
                elif ad.banner_image:
                    banner_image = ad.banner_image
                
                if banner_image:
                    # Build absolute URL for banner image
                    image_url = request.build_absolute_uri(banner_image.url)
                    data[ad.slot_name] = {
                        'type': 'image',
                        'image_url': image_url,
                        'mobile_image_url': request.build_absolute_uri(ad.mobile_banner_image.url) if ad.mobile_banner_image else None,
                        'desktop_image_url': request.build_absolute_uri(ad.banner_image.url) if ad.banner_image else None,
                        'link': ad.banner_link or '#',
                        'alt_text': ad.banner_alt_text or 'Advertisement',
                        'open_in_new_tab': ad.open_in_new_tab,
                        'is_mobile_optimized': bool(ad.mobile_banner_image)
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


@action(detail=False, methods=['get'])
def homepage_sections(request):
    """Get all active homepage sections."""
    from rest_framework.response import Response
    from rest_framework.decorators import api_view
    
    # Get How It Works sections
    how_it_works_sections = HowItWorksSection.objects.filter(is_active=True).order_by('order')
    how_it_works_data = HowItWorksSectionSerializer(how_it_works_sections, many=True).data
    
    # Get Recruiter sections
    recruiter_sections = RecruiterSection.objects.filter(is_active=True).order_by('order')
    recruiter_data = RecruiterSectionSerializer(recruiter_sections, many=True).data
    
    return Response({
        'how_it_works_sections': how_it_works_data,
        'recruiter_sections': recruiter_data
    })


@api_view(['GET'])
def homepage_sections_api(request):
    """Standalone API endpoint for homepage sections."""
    from rest_framework.response import Response
    
    try:
        # Get How It Works sections
        how_it_works_sections = HowItWorksSection.objects.filter(is_active=True).order_by('order')
        how_it_works_data = HowItWorksSectionSerializer(how_it_works_sections, many=True).data
        
        # Get Recruiter sections
        recruiter_sections = RecruiterSection.objects.filter(is_active=True).order_by('order')
        recruiter_data = RecruiterSectionSerializer(recruiter_sections, many=True).data
        
        return Response({
            'how_it_works_sections': how_it_works_data,
            'recruiter_sections': recruiter_data
        })
    except Exception as e:
        # If models don't exist or there's a DB error, return empty sections
        return Response({
            'how_it_works_sections': [],
            'recruiter_sections': []
        })
