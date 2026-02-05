import { useState, useEffect } from 'react';
import './CompanyTable.css';

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

  const parseTags = (text) => {
    if (!text) return [];
    return text.split(',').map(item => item.trim()).filter(item => item);
  };

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

  return (
    <div className="company-list">
      {companies.map((company) => (
        <div key={company.id} className={`company-card ${company.is_sponsored ? 'sponsored' : ''}`}>
          {company.is_sponsored && (
            <div className="sponsored-badge">
              <span>Sponsored</span>
            </div>
          )}
          <div className="company-header">
            <div className="company-info">
              {company.logo && (
                <img
                  src={company.logo}
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
      ))}
    </div>
  );
}

export default CompanyTable;
