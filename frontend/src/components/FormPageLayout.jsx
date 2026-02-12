import React, { useState, useEffect } from 'react';
import './FormPageLayout.css';

const FormPageLayout = ({ children, pageName }) => {
  const [layout, setLayout] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLayout = async () => {
      try {
        console.log('Fetching layout for page:', pageName);
        const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://staging.whoishiringintech.com/api';
        const response = await fetch(
          `${API_BASE_URL}/form-layouts/by_page/?page=${pageName}`
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
  const imageWidthPct = layout?.image_width_percentage || 50;
  const formWidthPct = 100 - imageWidthPct;

  // Center layout - original style
  if (formPosition === 'center') {
    return <div className="form-page-container form-center">{children}</div>;
  }

  // Left or Right layout with side panel
  return (
    <div className={`form-page-container form-split form-${formPosition}`}>
      {/* Form Section */}
      <div className="form-section" style={{ flex: `0 0 ${formWidthPct}%`, maxWidth: `${formWidthPct}%` }}>
        <div className="form-wrapper">{children}</div>
      </div>

      {/* Side Panel Section */}
      <div
        className="side-panel"
        style={{
          flex: `0 0 ${imageWidthPct}%`,
          maxWidth: `${imageWidthPct}%`,
          backgroundColor: layout.background_color,
          color: layout.text_color,
          ...(layout.side_image_url ? {
            backgroundImage: `url(${layout.side_image_url})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
          } : {}),
        }}
      >
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
  );
};

export default FormPageLayout;
