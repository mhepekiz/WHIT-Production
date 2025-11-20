import React, { useState, useEffect } from 'react';
import './FormPageLayout.css';

const FormPageLayout = ({ children, pageName }) => {
  const [layout, setLayout] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLayout = async () => {
      try {
        console.log('Fetching layout for page:', pageName);
        const response = await fetch(
          `http://localhost:8000/api/form-layouts/by_page/?page=${pageName}`
        );
        console.log('Response status:', response.status);
        if (response.ok) {
          const data = await response.json();
          console.log('Layout data received:', data);
          setLayout(data);
        } else {
          console.error('Failed to fetch layout, status:', response.status);
          setLayout({ form_position: 'center' });
        }
      } catch (error) {
        console.error('Error fetching form layout:', error);
        // Set default center layout on error
        setLayout({ form_position: 'center' });
      } finally {
        setLoading(false);
      }
    };

    fetchLayout();
  }, [pageName]);

  if (loading) {
    return <div className="form-page-loading">Loading...</div>;
  }

  const formPosition = layout?.form_position || 'center';

  // Center layout - original style
  if (formPosition === 'center') {
    return <div className="form-page-container form-center">{children}</div>;
  }

  // Left or Right layout with side panel
  return (
    <div className={`form-page-container form-split form-${formPosition}`}>
      {/* Form Section */}
      <div className="form-section">
        <div className="form-wrapper">{children}</div>
      </div>

      {/* Side Panel Section */}
      <div
        className="side-panel"
        style={{
          backgroundColor: layout.background_color,
          color: layout.text_color,
        }}
      >
        <div className="side-panel-content">
          {layout.side_image_url && (
            <div className="side-image">
              <img src={layout.side_image_url} alt={layout.side_heading} />
            </div>
          )}

          {/* Text overlay on image */}
          {(layout.side_heading || layout.side_subheading || layout.side_text) && (
            <div className={`text-overlay ${layout.text_overlay_position || 'center-center'}`}>
              {layout.side_heading && 
                React.createElement(
                  layout.side_heading_tag || 'h1',
                  { className: 'side-heading' },
                  layout.side_heading
                )
              }

              {layout.side_subheading && 
                React.createElement(
                  layout.side_subheading_tag || 'h2',
                  { className: 'side-subheading' },
                  layout.side_subheading
                )
              }

              {layout.side_text && 
                React.createElement(
                  layout.side_text_tag || 'p',
                  { className: 'side-text' },
                  layout.side_text
                )
              }
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FormPageLayout;
