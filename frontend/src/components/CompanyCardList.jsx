import { useState } from 'react';
import './CompanyCardList.css';

// Premium neutral chip styling
const getFunctionChipClass = (functionName) => {
  return 'chip-neutral'; // All functions use neutral style
};

const getWorkEnvironmentChipClass = (environment) => {
  const env = environment?.toLowerCase();
  if (env === 'remote') return 'chip-env-remote';
  if (env === 'hybrid') return 'chip-env-hybrid';
  if (env === 'on-site' || env === 'onsite') return 'chip-env-onsite';
  return 'chip-env-remote';
};

function CompanyCardList({ companies, buttonStyles }) {
  const [expandedCompanies, setExpandedCompanies] = useState(new Set());

  const toggleExpanded = (companyId) => {
    setExpandedCompanies(prev => {
      const newSet = new Set(prev);
      if (newSet.has(companyId)) {
        newSet.delete(companyId);
      } else {
        newSet.add(companyId);
      }
      return newSet;
    });
  };

  if (!companies || companies.length === 0) {
    return (
      <div className="no-results">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <h3>No companies found</h3>
        <p>Try adjusting your filters or search terms.</p>
      </div>
    );
  }

  return (
    <div className="company-card-list">
      {companies.map((company) => {
        const isExpanded = expandedCompanies.has(company.id);
        const maxVisibleFunctions = 3;
        const visibleFunctions = company.functions?.slice(0, maxVisibleFunctions) || [];
        const hiddenCount = Math.max(0, (company.functions?.length || 0) - maxVisibleFunctions);

        return (
          <div key={company.id} className="company-card-item">
            {/* Top Row: Company Name + Work Environment */}
            <div className="card-top-row">
              <div className="company-name-section">
                <h3 className="company-name">{company.name}</h3>
                {company.website && (
                  <a 
                    href={company.website.startsWith('http') ? company.website : `https://${company.website}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="company-website"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                      <polyline points="15,3 21,3 21,9"/>
                      <line x1="10" y1="14" x2="21" y2="3"/>
                    </svg>
                  </a>
                )}
              </div>
              
              <div className="work-env-badges">
                {company.work_environments?.map((env, index) => (
                  <span
                    key={index}
                    className={`chip ${getWorkEnvironmentChipClass(env.name)}`}
                  >
                    {env.name}
                  </span>
                ))}
              </div>
            </div>

            {/* Second Row: Location */}
            <div className="card-location-row">
              <div className="location-info">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <span className="location-text">
                  {[company.city, company.state, company.country].filter(Boolean).join(', ')}
                </span>
              </div>
            </div>

            {/* Third Row: Functions */}
            <div className="card-functions-row">
              <div className="functions-container">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <line x1="9" y1="9" x2="15" y2="9"/>
                  <line x1="9" y1="15" x2="15" y2="15"/>
                </svg>
                <div className="functions-chips">
                  {visibleFunctions.map((func, index) => (
                    <span
                      key={index}
                      className={`chip ${getFunctionChipClass(func.name)}`}
                    >
                      {func.name}
                    </span>
                  ))}
                  {hiddenCount > 0 && (
                    <button
                      className="expand-functions-btn"
                      onClick={() => toggleExpanded(company.id)}
                    >
                      {isExpanded ? `Show less` : `+${hiddenCount}`}
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Expanded Functions */}
            {isExpanded && hiddenCount > 0 && (
              <div className="card-expanded-functions">
                <div className="expanded-functions-chips">
                  {company.functions.slice(maxVisibleFunctions).map((func, index) => (
                    <span
                      key={index}
                      className={`chip ${getFunctionChipClass(func.name)}`}
                    >
                      {func.name}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Bottom Row: Action Buttons */}
            <div className="card-bottom-row">
              <div className="action-buttons">
                <a
                  href={company.jobs_page || company.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-primary jobs-btn"
                  style={buttonStyles}
                >
                  Jobs
                </a>
                <a
                  href={company.reviews_link || '#'}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-secondary reviews-btn"
                  style={buttonStyles}
                >
                  Reviews
                </a>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default CompanyCardList;