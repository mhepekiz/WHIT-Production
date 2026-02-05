import hashlib
import random
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache

from ..models import SponsorCampaign, SponsorDeliveryLog, SponsorStatsDaily


class SponsorSelector:
    """
    Production-ready sponsored content selection system.
    Handles targeting, rotation, fatigue, and tracking.
    """
    
    # Anti-fatigue settings
    FATIGUE_MINUTES = 45  # Don't show same sponsor within 45 minutes
    FATIGUE_PAGE_VIEWS = 3  # Or within last 3 page views
    
    @classmethod
    def pick_sponsored_campaign(
        cls, 
        filters: Dict[str, Any], 
        user_hash: str,
        page_number: int = 1,
        request_path: str = "",
        now: Optional[datetime] = None
    ) -> Optional['SponsorCampaign']:
        """
        Select a sponsored campaign using production algorithm.
        
        Args:
            filters: Current page filters (country, function, work_env, etc.)
            user_hash: Anonymized user identifier 
            page_number: Current page number for rotation
            request_path: Current request path for context
            now: Current timestamp (for testing)
            
        Returns:
            Selected SponsorCampaign or None
        """
        if now is None:
            now = timezone.now()
        
        # Step 1: Build eligible set (hard filters)
        eligible = cls._get_eligible_campaigns(filters, now)
        if not eligible:
            return None
            
        # Step 2: Apply user-level fatigue rules (soft filters)
        eligible = cls._apply_fatigue_rules(eligible, user_hash, now)
        if not eligible:
            return None
            
        # Step 3: Choose one using weighted "least delivered" rotation
        selected = cls._weighted_selection(eligible, filters, user_hash, page_number, now)
        
        return selected
    
    @classmethod
    def _get_eligible_campaigns(cls, filters: Dict[str, Any], now: datetime) -> List['SponsorCampaign']:
        """Get campaigns that meet basic eligibility criteria"""
        # Import here to avoid circular imports
        from ..models import SponsorCampaign
        
        # Active campaigns within date range
        eligible = SponsorCampaign.objects.filter(
            status='active',
            start_at__lte=now,
            end_at__gte=now
        ).select_related('company')
        
        # Filter by targeting and daily caps
        matching_campaigns = []
        for campaign in eligible:
            # Check targeting match
            if not campaign.matches_targeting(filters):
                continue
                
            # Check daily caps
            if not campaign.under_daily_caps(now.date()):
                continue
                
            matching_campaigns.append(campaign)
            
        return matching_campaigns
    
    @classmethod
    def _apply_fatigue_rules(cls, eligible: List['SponsorCampaign'], user_hash: str, now: datetime) -> List['SponsorCampaign']:
        """Apply user-level anti-fatigue rules"""
        if not eligible:
            return eligible
            
        # Get recently shown campaigns for this user
        fatigue_cutoff = now - timedelta(minutes=cls.FATIGUE_MINUTES)
        
        recent_campaign_ids = SponsorDeliveryLog.objects.filter(
            user_hash=user_hash,
            action='impression',
            shown_at__gte=fatigue_cutoff
        ).values_list('campaign_id', flat=True).distinct()
        
        # Remove recently shown campaigns
        filtered = [c for c in eligible if c.id not in recent_campaign_ids]
        
        # If that eliminates all campaigns, relax the rule (use last hour only)
        if not filtered:
            relaxed_cutoff = now - timedelta(hours=1)
            recent_hour_ids = SponsorDeliveryLog.objects.filter(
                user_hash=user_hash,
                action='impression', 
                shown_at__gte=relaxed_cutoff
            ).values_list('campaign_id', flat=True).distinct()
            
            filtered = [c for c in eligible if c.id not in recent_hour_ids]
            
        # If still empty, return original eligible set
        return filtered if filtered else eligible
    
    @classmethod
    def _weighted_selection(
        cls, 
        eligible: List['SponsorCampaign'], 
        filters: Dict[str, Any],
        user_hash: str, 
        page_number: int, 
        now: datetime
    ) -> Optional['SponsorCampaign']:
        """Select campaign using weighted random based on under-delivery"""
        if not eligible:
            return None
            
        # Create deterministic seed for stable selection per user/page/time period
        # For homepage (page 1), use much shorter time periods for frequent rotation
        # For paginated browse, use longer periods for stability
        if page_number == 1:
            # Homepage: rotate every 30 seconds for frequent changes
            time_component = now.strftime('%Y%m%d%H%M') + str(now.second // 30)
        else:
            # Browse pages: rotate every hour for stability during pagination
            time_component = now.strftime('%Y%m%d%H')
            
        seed_data = f"{time_component}-{user_hash}-{page_number}-{hash(str(sorted(filters.items())))}"
        seed = int(hashlib.md5(seed_data.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Calculate selection scores
        scored_campaigns = []
        today = now.date()
        
        for campaign in eligible:
            impressions_today = campaign.impressions_today(today)
            
            # Score formula: (priority * weight) / (1 + impressions_today)
            # Higher priority and lower delivery = higher score
            score = (campaign.priority * campaign.weight) / (1 + impressions_today)
            scored_campaigns.append((campaign, score))
        
        # Weighted random selection
        total_score = sum(score for _, score in scored_campaigns)
        if total_score <= 0:
            return random.choice(eligible)  # Fallback to uniform random
            
        # Select based on weighted probability
        target = random.uniform(0, total_score)
        current_sum = 0
        
        for campaign, score in scored_campaigns:
            current_sum += score
            if current_sum >= target:
                return campaign
                
        # Fallback (shouldn't happen)
        return scored_campaigns[0][0] if scored_campaigns else None
    
    @classmethod
    def record_impression(
        cls, 
        campaign: 'SponsorCampaign',
        user_hash: str,
        page_key: str,
        user_agent: str = "",
        ip_address: str = "",
        referrer: str = ""
    ) -> None:
        """Record an impression for tracking and anti-fatigue"""
        now = timezone.now()
        
        with transaction.atomic():
            # Log the delivery
            SponsorDeliveryLog.objects.create(
                campaign=campaign,
                user_hash=user_hash,
                action='impression',
                page_key=page_key,
                user_agent=user_agent,
                ip_address=ip_address,
                referrer=referrer
            )
            
            # Update daily stats
            stats, created = SponsorStatsDaily.objects.get_or_create(
                campaign=campaign,
                date=now.date(),
                defaults={'impressions': 0, 'clicks': 0}
            )
            stats.impressions += 1
            stats.save()
    
    @classmethod
    def record_click(
        cls,
        campaign: 'SponsorCampaign', 
        user_hash: str,
        page_key: str,
        user_agent: str = "",
        ip_address: str = "",
        referrer: str = ""
    ) -> None:
        """Record a click for tracking"""
        now = timezone.now()
        
        with transaction.atomic():
            # Log the click
            SponsorDeliveryLog.objects.create(
                campaign=campaign,
                user_hash=user_hash,
                action='click',
                page_key=page_key,
                user_agent=user_agent,
                ip_address=ip_address,
                referrer=referrer
            )
            
            # Update daily stats
            stats, created = SponsorStatsDaily.objects.get_or_create(
                campaign=campaign,
                date=now.date(),
                defaults={'impressions': 0, 'clicks': 0}
            )
            stats.clicks += 1
            stats.save()
    
    @classmethod
    def get_user_hash(cls, request) -> str:
        """Generate consistent user hash for tracking"""
        # Use session key + user agent + IP for anonymous users
        # For logged-in users, could use user.id
        if hasattr(request, 'user') and request.user.is_authenticated:
            base_string = f"user-{request.user.id}"
        else:
            session_key = request.session.session_key or ""
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:200]
            ip = cls._get_client_ip(request)
            base_string = f"{session_key}-{user_agent}-{ip}"
            
        return hashlib.sha256(base_string.encode()).hexdigest()
    
    @classmethod
    def _get_client_ip(cls, request) -> str:
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
    
    @classmethod
    def build_page_key(cls, request, filters: Dict[str, Any], page_number: int) -> str:
        """Build consistent page key for tracking"""
        filter_hash = hashlib.md5(str(sorted(filters.items())).encode()).hexdigest()[:8]
        path = request.path.replace('/api/', '').replace('/', '')
        return f"{path}:page={page_number}:filters={filter_hash}"