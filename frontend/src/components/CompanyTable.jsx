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
    <div className="table-container">
      <table className="company-table">
        <thead>
          <tr>
            <th>Company</th>
            <th>Jobs Page</th>
            <th>Reviews</th>
            <th className="resizable-header" style={{ width: `${columnWidths.functions}px` }}>
              <div className="header-content">
                <span>Functions</span>
                <div className="resize-handle" onMouseDown={handleMouseDown('functions')} />
              </div>
            </th>
            <th className="resizable-header" style={{ width: `${columnWidths.location}px` }}>
              <div className="header-content">
                <span>Location</span>
                <div className="resize-handle" onMouseDown={handleMouseDown('location')} />
              </div>
            </th>
            <th className="resizable-header" style={{ width: `${columnWidths.workEnvironment}px` }}>
              <div className="header-content">
                <span>Work Environment</span>
                <div className="resize-handle" onMouseDown={handleMouseDown('workEnvironment')} />
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          {companies.map((company) => (
            <tr key={company.id}>
              <td className="company-name-cell">
                <div className="company-name-wrapper">
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
                  <span className="company-name">{company.name}</span>
                </div>
              </td>

              <td>
                <a
                  href={company.jobs_page_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link-btn careers-btn"
                  style={buttonStyles}
                >
                  Careers
                </a>
              </td>

              <td>
                {company.company_reviews ? (
                  <a
                    href={company.company_reviews}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="link-btn reviews-btn"
                    style={buttonStyles}
                  >
                    Reviews
                  </a>
                ) : (
                  <span className="text-muted">—</span>
                )}
              </td>

              <td style={{ width: `${columnWidths.functions}px` }}>
                <div className="tags-container">
                  {company.functions && company.functions.map((func) => (
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
                </div>
              </td>

              <td className="location-cell" style={{ width: `${columnWidths.location}px` }}>
                <div className="location-text">
                  {company.city && <span>{company.city}, </span>}
                  {company.state && <span>{company.state}, </span>}
                  <span className="country">{company.country}</span>
                </div>
              </td>

              <td className="work-environment-cell" style={{ width: `${columnWidths.workEnvironment}px` }}>
                <div className="tags-container">
                  {parseTags(company.work_environment).map((env, index) => (
                    <span key={index} className="tag tag-environment">
                      {env}
                    </span>
                  ))}
                </div>
              </td>

            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CompanyTable;
