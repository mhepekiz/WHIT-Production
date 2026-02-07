import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/HomepageSections.css';

const JobSeekerCard = ({ section }) => {
  const steps = section.steps
    .filter(step => step.is_active)
    .sort((a, b) => a.order - b.order)
    .slice(0, 4); // Enforce 4 bullets max

  return (
    <div className="role-navigation-card job-seeker-card">
      <div className="card-header">
        <div className="card-icon">🔍</div>
        <h3 className="card-title">For Job Seekers</h3>
      </div>
      
      <div className="card-content">
        <p className="card-description">
          Discover tech companies actively hiring and track your applications
        </p>
        
        <ul className="card-bullets">
          {steps.map(step => (
            <li key={step.id} className="bullet-item">
              <span className="bullet-icon">{step.icon}</span>
              <span className="bullet-text">{step.title}</span>
            </li>
          ))}
          {/* Fill remaining bullets if less than 4 */}
          {steps.length < 4 && Array.from({ length: 4 - steps.length }, (_, index) => (
            <li key={`filler-${index}`} className="bullet-item">
              <span className="bullet-icon">✓</span>
              <span className="bullet-text">Track application status</span>
            </li>
          ))}
        </ul>
      </div>
      
      <div className="card-actions">
        <Link to="/companies" className="card-button primary">
          Browse Companies
        </Link>
        <Link to="/register" className="card-link">
          Create Account →
        </Link>
      </div>
    </div>
  );
};

const RecruiterCard = ({ section }) => {
  const isExternalLink = section.button_link.startsWith('http');

  return (
    <div className="role-navigation-card recruiter-card">
      <div className="card-header">
        <div className="card-icon">💼</div>
        <h3 className="card-title">For Recruiters</h3>
      </div>
      
      <div className="card-content">
        <p className="card-description">
          Add your company and get discovered by candidates tracking active hiring signals
        </p>
        
        <ul className="card-bullets">
          <li className="bullet-item">
            <span className="bullet-icon">🎯</span>
            <span className="bullet-text">Target active job seekers</span>
          </li>
          <li className="bullet-item">
            <span className="bullet-icon">📈</span>
            <span className="bullet-text">Track company visibility</span>
          </li>
          <li className="bullet-item">
            <span className="bullet-icon">⚡</span>
            <span className="bullet-text">Post jobs instantly</span>
          </li>
          <li className="bullet-item">
            <span className="bullet-icon">🔍</span>
            <span className="bullet-text">Browse candidate profiles</span>
          </li>
        </ul>
      </div>
      
      <div className="card-actions">
        {isExternalLink ? (
          <a
            href={section.button_link}
            className="card-button outline"
            target="_blank"
            rel="noopener noreferrer"
          >
            {section.button_text}
          </a>
        ) : (
          <Link to={section.button_link} className="card-button outline">
            {section.button_text}
          </Link>
        )}
        <Link to="/recruiter/register" className="card-link">
          Sign Up →
        </Link>
      </div>
    </div>
  );
};

const HomepageSections = ({ sections }) => {
  if (!sections) return null;

  const { how_it_works_sections = [], recruiter_sections = [] } = sections;

  // Get the first active section of each type
  const jobSeekerSection = how_it_works_sections.find(section => section.is_active);
  const recruiterSection = recruiter_sections.find(section => section.is_active);

  // Only render if we have at least one section
  if (!jobSeekerSection && !recruiterSection) return null;

  return (
    <div className="homepage-sections">
      <div className="role-navigation-container">
        {jobSeekerSection && <JobSeekerCard section={jobSeekerSection} />}
        {recruiterSection && <RecruiterCard section={recruiterSection} />}
      </div>
    </div>
  );
};

export default HomepageSections;