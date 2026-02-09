import { useState, useEffect, useRef } from 'react';
import './CompanyTable.css';
import { getMediaUrl } from '../services/api';
import apiClient from '../services/api';
import sponsoredTracking from '../services/sponsoredTracking';

// Helper function to parse tags - moved outside components to be accessible
const parseTags = (text) => {
  if (!text) return [];
  return text.split(',').map(item => item.trim()).filter(item => item);
};

function CompanyTable({ companies, buttonStyles = { padding: '6px 12px', fontSize: '0.75rem' } }) {
  const [columnWidths, setColumnWidths] = useState({
    functions: 800,
    location: 259,
    workEnvironment: 264
  });

  const [resizing, setResizing] = useState(null);

  if (!companies || companies.length === 0) {
    return (
      <div className="no-results">
        <p>No companies found matching your criteria.</p>
      </div>
    );
  }

  const handleMouseDown = (column) => (e) => {
    e.preventDefault();
    setResizing({ column, startX: e.clientX, startWidth: columnWidths[column] });
  };

  const handleMouseMove = (e) => {
    if (!resizing) return;
    
    const diff = e.clientX - resizing.startX;
    const newWidth = Math.max(150, resizing.startWidth + diff);
    
    setColumnWidths(prev => ({
      ...prev,
      [resizing.column]: newWidth
    }));
  };

  const handleMouseUp = () => {
    setResizing(null);
  };

  useEffect(() => {
    if (resizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [resizing]);

  const handleCareerClick = async (e, company) => {
    try {
      // Don't prevent default - we want the link to open
      // Track the click in the background
      await apiClient.post('companies/track-job-click/', {
        company_id: company.id
      });
    } catch (error) {
      console.error('Error tracking job click:', error);
      // Don't prevent the link from working if tracking fails
    }
  };

  const trackPageView = async (company) => {
    try {
      // Create a unique key for this tracking call
      const trackingKey = `pageview_${company.id}_${Date.now()}`;
      
      // Check if we recently tracked this company (within last 5 seconds)
      const lastTracked = localStorage.getItem(`last_tracked_${company.id}`);
      const now = Date.now();
      
      if (lastTracked && (now - parseInt(lastTracked)) < 5000) {
        console.log(`Skipping duplicate page view for ${company.name}`);
        return;
      }
      
      await apiClient.post('companies/track-page-view/', {
        company_id: company.id
      });
      
      // Store the timestamp to prevent duplicates
      localStorage.setItem(`last_tracked_${company.id}`, now.toString());
      
    } catch (error) {
      console.error('Error tracking page view:', error);
      // Don't prevent display if tracking fails
    }
  };

  return (
    <div className="company-list">
      {companies.map((company) => (
        <SponsoredCompanyCard 
          key={company.id} 
          company={company} 
          buttonStyles={buttonStyles} 
          handleCareerClick={handleCareerClick}
          trackPageView={trackPageView}
        />
      ))}
    </div>
  );
};

// Separate component to handle sponsored tracking for each company
const SponsoredCompanyCard = ({ company, buttonStyles, handleCareerClick, trackPageView }) => {
  const cardRef = useRef(null);
  const trackedRef = useRef(false); // Prevent duplicate tracking

  // Setup tracking for sponsored companies
  useEffect(() => {
    if (company.is_sponsored && company.sponsored_campaign_id && cardRef.current) {
      // Set campaign ID as data attribute for tracking
      cardRef.current.setAttribute('data-campaign-id', company.sponsored_campaign_id);
      
      // Start tracking impressions
      sponsoredTracking.startTracking(cardRef.current);
      
      return () => {
        // Cleanup tracking on unmount
        if (cardRef.current) {
          sponsoredTracking.stopTracking(cardRef.current);
        }
      };
    }
  }, [company.is_sponsored, company.sponsored_campaign_id]);

  // Track page view when component mounts (only once per company)
  useEffect(() => {
    if (!trackedRef.current) {
      trackedRef.current = true;
      trackPageView(company);
    }
  }, []); // Empty dependency array to run only once

  return (
    <div 
      ref={cardRef}
      key={company.id} 
      className={`company-card ${company.is_sponsored ? 'sponsored' : ''}`}
    >
          {company.is_sponsored && (
            <div className="sponsored-badge">
              <span>Sponsored</span>
            </div>
          )}
          <div className="company-header">
            <div className="company-info">
              {company.logo && (
                <img
                  src={getMediaUrl(company.logo)}
                  alt={`${company.name} logo`}
                  className="company-logo"
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              )}
              <div className="company-name-wrapper">
                <span className="company-name">{company.name}</span>
              </div>
            </div>
            <div className="company-actions">
              <a
                href={company.jobs_page_url}
                target="_blank"
                rel="noopener noreferrer"
                className="link-btn careers-btn"
                style={buttonStyles}
                onClick={(e) => handleCareerClick(e, company)}
              >
                Careers
              </a>
              {company.company_reviews && (
                <a
                  href={company.company_reviews}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link-btn reviews-btn"
                  style={buttonStyles}
                >
                  Reviews
                </a>
              )}
            </div>
          </div>
          
          <div className="company-location">
            {company.city && <span>{company.city}, </span>}
            {company.state && <span>{company.state}, </span>}
            <span className="country">{company.country}</span>
          </div>
          
          <div className="company-functions">
            {company.functions && company.functions.slice(0, 4).map((func) => (
              <span 
                key={func.id} 
                className="tag tag-function"
                style={{
                  backgroundColor: func.color,
                  color: func.text_color
                }}
              >
                {func.name}
              </span>
            ))}
            {company.functions && company.functions.length > 4 && (
              <span className="tag tag-overflow">
                +{company.functions.length - 4} more
              </span>
            )}
          </div>
          
          <div className="company-environment">
            {parseTags(company.work_environment).map((env, index) => (
              <span key={index} className="tag tag-environment">
                {env}
              </span>
            ))}
          </div>
        </div>
  );
};

export default CompanyTable;
