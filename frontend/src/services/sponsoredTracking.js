// Service for tracking sponsored content impressions and clicks
class SponsoredTrackingService {
  constructor() {
    this.viewportObserver = null;
    this.trackedCampaigns = new Set();
    this.setupViewportObserver();
  }

  setupViewportObserver() {
    // Create intersection observer for viewport tracking
    this.viewportObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
            const campaignId = entry.target.getAttribute('data-campaign-id');
            if (campaignId && !this.trackedCampaigns.has(campaignId)) {
              this.recordImpression(campaignId, entry.target);
              this.trackedCampaigns.add(campaignId);
            }
          }
        });
      },
      {
        threshold: [0.5], // Track when 50% visible
        rootMargin: '0px'
      }
    );
  }

  async recordImpression(campaignId, element) {
    try {
      // Get current page context
      const urlParams = new URLSearchParams(window.location.search);
      const filters = {
        country: urlParams.get('country'),
        functions: urlParams.get('functions'),
        work_environments: urlParams.get('work_environments'),
        search: urlParams.get('search')
      };

      // Remove null/empty values
      Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
      });

      const pageNumber = parseInt(urlParams.get('page')) || 1;

      const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/companies/sponsored/impression/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: JSON.stringify({
          campaign_id: campaignId,
          page_url: window.location.href,
          filters: filters,
          page_number: pageNumber,
          is_above_fold: element.getBoundingClientRect().top < window.innerHeight
        })
      });

      if (!response.ok) {
        console.warn('Failed to record sponsored impression:', response.status);
      }
    } catch (error) {
      console.warn('Error recording sponsored impression:', error);
    }
  }

  async recordClick(campaignId) {
    try {
      // Get current page context  
      const urlParams = new URLSearchParams(window.location.search);
      const filters = {
        country: urlParams.get('country'),
        functions: urlParams.get('functions'), 
        work_environments: urlParams.get('work_environments'),
        search: urlParams.get('search')
      };

      // Remove null/empty values
      Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
      });

      const pageNumber = parseInt(urlParams.get('page')) || 1;

      const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/companies/sponsored/click/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: JSON.stringify({
          campaign_id: campaignId,
          page_url: window.location.href,
          filters: filters,
          page_number: pageNumber
        })
      });

      if (!response.ok) {
        console.warn('Failed to record sponsored click:', response.status);
      }
    } catch (error) {
      console.warn('Error recording sponsored click:', error);
    }
  }

  startTracking(element) {
    // Start tracking impressions for sponsored elements
    if (this.viewportObserver && element) {
      this.viewportObserver.observe(element);
    }
  }

  stopTracking(element) {
    // Stop tracking impressions for elements
    if (this.viewportObserver && element) {
      this.viewportObserver.unobserve(element);
    }
  }

  getCSRFToken() {
    // Get CSRF token from cookies or meta tag
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return value;
      }
    }
    
    // Fallback: check meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    return csrfMeta ? csrfMeta.getAttribute('content') : '';
  }

  cleanup() {
    // Cleanup observers
    if (this.viewportObserver) {
      this.viewportObserver.disconnect();
    }
    this.trackedCampaigns.clear();
  }
}

// Create global instance
const sponsoredTracking = new SponsoredTrackingService();

export default sponsoredTracking;