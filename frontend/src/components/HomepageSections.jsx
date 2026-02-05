import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/HomepageSections.css';

const HowItWorksSection = ({ section }) => {
  return (
    <div className="how-it-works-section">
      <h2 className="section-title">{section.title}</h2>
      <p className="section-subtitle">{section.subtitle}</p>
      <h3 className="section-header">{section.section_header}</h3>
      <p className="section-description">{section.description}</p>
      
      <div className="how-it-works-steps">
        {section.steps
          .filter(step => step.is_active)
          .sort((a, b) => a.order - b.order)
          .map(step => (
            <div key={step.id} className="how-it-works-step">
              <div className="step-icon">{step.icon}</div>
              <div className="step-content">
                <h4 className="step-title">{step.title}</h4>
                <p className="step-description">{step.description}</p>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};

const RecruiterSection = ({ section }) => {
  const isExternalLink = section.button_link.startsWith('http');
  
  const buttonStyle = {
    backgroundColor: section.button_color,
    color: '#ffffff',
  };
  
  const sectionStyle = {
    backgroundColor: section.background_color,
    color: section.text_color,
  };

  return (
    <div className="recruiter-section" style={sectionStyle}>
      <h2 className="recruiter-title" style={{ color: section.text_color }}>
        {section.title}
      </h2>
      <p className="recruiter-description" style={{ color: section.text_color }}>
        {section.description}
      </p>
      
      {isExternalLink ? (
        <a
          href={section.button_link}
          className="recruiter-button"
          style={buttonStyle}
          target="_blank"
          rel="noopener noreferrer"
        >
          {section.button_text}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M7 17L17 7" />
            <path d="M7 7h10v10" />
          </svg>
        </a>
      ) : (
        <Link
          to={section.button_link}
          className="recruiter-button"
          style={buttonStyle}
        >
          {section.button_text}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </Link>
      )}
    </div>
  );
};

const HomepageSections = ({ sections }) => {
  if (!sections) return null;

  const { how_it_works_sections = [], recruiter_sections = [] } = sections;

  // Combine and sort all sections by order
  const allSections = [
    ...how_it_works_sections.filter(section => section.is_active).map(section => ({
      ...section,
      type: 'how_it_works'
    })),
    ...recruiter_sections.filter(section => section.is_active).map(section => ({
      ...section,
      type: 'recruiter'
    }))
  ].sort((a, b) => a.order - b.order);

  return (
    <div className="homepage-sections">
      {allSections.map(section => (
        <div key={`${section.type}-${section.id}`}>
          {section.type === 'how_it_works' ? (
            <HowItWorksSection section={section} />
          ) : (
            <RecruiterSection section={section} />
          )}
        </div>
      ))}
    </div>
  );
};

export default HomepageSections;