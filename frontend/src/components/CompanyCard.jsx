import { useState, useEffect, useRef } from 'react';
import './CompanyCard.css';
import sponsoredTracking from '../services/sponsoredTracking';

// Function to get semantic class names based on function type
const getFunctionChipClass = (functionName) => {
  const name = functionName.toLowerCase();
  
  if (name.includes('engineer') || name.includes('developer') || name.includes('software') || name.includes('technical')) {
    return 'chip-engineering';
  } else if (name.includes('data') || name.includes('analytics') || name.includes('science')) {
    return 'chip-data';
  } else if (name.includes('product') || name.includes('pm')) {
    return 'chip-product';
  } else if (name.includes('design') || name.includes('ux') || name.includes('ui')) {
    return 'chip-design';
  } else if (name.includes('marketing') || name.includes('growth') || name.includes('content')) {
    return 'chip-marketing';
  } else if (name.includes('sales') || name.includes('business') || name.includes('account')) {
    return 'chip-sales';
  } else if (name.includes('support') || name.includes('customer') || name.includes('success')) {
    return 'chip-support';
  } else if (name.includes('finance') || name.includes('accounting') || name.includes('finance')) {
    return 'chip-finance';
  } else if (name.includes('hr') || name.includes('people') || name.includes('talent')) {
    return 'chip-hr';
  } else if (name.includes('intern') || name.includes('trainee') || name.includes('entry')) {
    return 'chip-internship';
  }
  
  return 'chip-support'; // Default fallback
};

// Function to get work environment chip class
const getWorkEnvironmentChipClass = (env) => {
  const environment = env.toLowerCase();
  
  if (environment.includes('remote')) {
    return 'chip-remote';
  } else if (environment.includes('hybrid')) {
    return 'chip-hybrid';
  } else if (environment.includes('office') || environment.includes('on-site') || environment.includes('onsite')) {
    return 'chip-onsite';
  }
  
  return 'chip-onsite'; // Default fallback
};

function CompanyCard({ company, buttonStyles = { padding: '6px 12px', fontSize: '0.75rem' } }) {
  const [functionsExpanded, setFunctionsExpanded] = useState(false);
  const cardRef = useRef(null);

  if (!company) return null;

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

  const handleSponsoredClick = (e) => {
    // Record click when user interacts with sponsored content
    if (company.is_sponsored && company.sponsored_campaign_id) {
      sponsoredTracking.recordClick(company.sponsored_campaign_id);
    }
  };

  const parseTags = (text) => {
    if (!text) return [];
    return text.split(',').map(item => item.trim()).filter(item => item);
  };

  const functionTags = company.functions || [];
  const workEnvironmentTags = parseTags(company.work_environment);
  
  // Limit visible function chips
  const maxVisibleFunctions = 3;
  const visibleFunctions = functionsExpanded 
    ? functionTags 
    : functionTags.slice(0, maxVisibleFunctions);
  const hiddenFunctionsCount = functionTags.length - maxVisibleFunctions;

  return (
    <div 
      ref={cardRef}
      className={`company-card ${company.is_sponsored ? 'sponsored' : ''}`}
      onClick={handleSponsoredClick}
    >
      {company.is_sponsored && (
        <div className="sponsored-badge">
          <span>Sponsored</span>
        </div>
      )}
      {/* Card Header */}
      <div className="company-card-header">
        <div className="company-info">
          {company.logo && (
            <img
              src={company.logo}
              alt={`${company.name} logo`}
              className="company-card-logo"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          )}
          <div className="company-details">
            <h3 className="company-card-name">{company.name}</h3>
            <div className="company-card-location">
              {company.city && <span>{company.city}, </span>}
              {company.state && <span>{company.state}, </span>}
              <span className="company-card-country">{company.country}</span>
            </div>
          </div>
        </div>
        
        {/* Status Badge */}
        {company.status && (
          <div className={`status-badge ${company.status.toLowerCase()}`}>
            {company.status}
          </div>
        )}
      </div>

      {/* Card Body */}
      <div className="company-card-body">
        {/* Work Environment Chips */}
        {workEnvironmentTags.length > 0 && (
          <div className="card-section">
            <div className="card-section-title">Work Environment</div>
            <div className="tags-container">
              {workEnvironmentTags.map((env, index) => (
                <span key={index} className={`chip ${getWorkEnvironmentChipClass(env)}`}>
                  {env}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Functions Chips */}
        {functionTags.length > 0 && (
          <div className="card-section">
            <div className="card-section-title">Functions</div>
            <div className="tags-container">
              {visibleFunctions.map((func) => (
                <span 
                  key={func.id} 
                  className={`chip ${getFunctionChipClass(func.name)}`}
                >
                  {func.name}
                </span>
              ))}
              
              {/* Show more/less button */}
              {hiddenFunctionsCount > 0 && !functionsExpanded && (
                <button 
                  className="tag tag-expand"
                  onClick={() => setFunctionsExpanded(true)}
                >
                  +{hiddenFunctionsCount} more
                </button>
              )}
              
              {functionsExpanded && functionTags.length > maxVisibleFunctions && (
                <button 
                  className="tag tag-expand"
                  onClick={() => setFunctionsExpanded(false)}
                >
                  Show less
                </button>
              )}
            </div>
          </div>
        )}

        {/* Engineering Positions Badge */}
        {company.engineering_positions && (
          <div className="card-section">
            <div className="engineering-badge">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M8 2L10.5 6H13L10 9L11 14L8 12L5 14L6 9L3 6H5.5L8 2Z" 
                      fill="currentColor" stroke="currentColor" strokeWidth="1" strokeLinejoin="round"/>
              </svg>
              Engineering Positions Available
            </div>
          </div>
        )}
      </div>

      {/* Card Actions */}
      <div className="company-card-actions">
        <a
          href={company.jobs_page_url}
          target="_blank"
          rel="noopener noreferrer"
          className="card-action-btn primary"
          style={buttonStyles}
        >
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <rect x="2" y="4" width="14" height="11" rx="2" stroke="currentColor" strokeWidth="1.5"/>
            <path d="M6 2V6M12 2V6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          View Jobs
        </a>
        
        {company.company_reviews ? (
          <a
            href={company.company_reviews}
            target="_blank"
            rel="noopener noreferrer"
            className="card-action-btn secondary"
            style={buttonStyles}
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M9 1L11.5 6H17L13 9.5L14.5 15L9 12L3.5 15L5 9.5L1 6H6.5L9 1Z" 
                    stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
            </svg>
            Reviews
          </a>
        ) : (
          <div className="card-action-btn disabled">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M9 1L11.5 6H17L13 9.5L14.5 15L9 12L3.5 15L5 9.5L1 6H6.5L9 1Z" 
                    stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
            </svg>
            No Reviews
          </div>
        )}
      </div>
    </div>
  );
}

export default CompanyCard;