import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getApiUrl, getMediaUrl } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './JobDetail.css';

/** Only allow http/https URLs to prevent javascript: injection */
const getSafeUrl = (url) => {
  if (!url) return null;
  try {
    const parsed = new URL(url, window.location.origin);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') return url;
  } catch { /* invalid URL */ }
  return null;
};

/** Validate an email address format */
const isValidEmail = (email) => {
  if (!email) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

const getEmploymentLabel = (type) => {
  const labels = {
    'full-time': 'Full Time',
    'part-time': 'Part Time',
    'contract': 'Contract',
    'internship': 'Internship',
    'temporary': 'Temporary',
  };
  return labels[type] || type;
};

const getExperienceLabel = (level) => {
  const labels = {
    'entry': 'Entry Level',
    'mid': 'Mid Level',
    'senior': 'Senior',
    'lead': 'Lead / Manager',
    'executive': 'Executive',
  };
  return labels[level] || level;
};

const formatSalary = (min, max, currency = 'USD') => {
  const fmt = (val) => {
    const num = Number(val);
    return num.toLocaleString('en-US');
  };
  if (min && max) return `$${fmt(min)} – $${fmt(max)}`;
  if (min) return `From $${fmt(min)}`;
  if (max) return `Up to $${fmt(max)}`;
  return null;
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const timeAgo = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
  return `${Math.floor(diffDays / 365)} years ago`;
};

function JobDetail() {
  const { id } = useParams();
  const { token } = useAuth();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchJob = async () => {
      // Validate ID is a positive integer
      if (!/^\d+$/.test(id)) {
        setError('Invalid job ID');
        setLoading(false);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(getApiUrl(`recruiters/job-board/${id}/`), {
          headers: { 'Authorization': `Token ${token}` },
        });
        if (!res.ok) throw new Error('Job not found');
        const data = await res.json();
        setJob(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchJob();
  }, [id, token]);

  if (loading) {
    return (
      <div className="job-detail">
        <div className="job-detail-loading">
          <div className="job-detail-spinner" />
          <p>Loading job details...</p>
        </div>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="job-detail">
        <div className="job-detail-error">
          <h2>Job Not Found</h2>
          <p>The job you're looking for doesn't exist or has been removed.</p>
          <button className="job-detail-back-btn" onClick={() => navigate('/jobs')}>
            ← Back to Jobs
          </button>
        </div>
      </div>
    );
  }

  const salary = formatSalary(job.salary_min, job.salary_max, job.salary_currency);
  const locationParts = [job.city, job.state, job.country].filter(Boolean);
  const locationStr = locationParts.join(', ');
  const skills = job.skills_required || [];

  return (
    <div className="job-detail">
      {/* Back link */}
      <div className="job-detail-breadcrumb">
        <Link to="/jobs" className="job-detail-back-link">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M10 12L6 8L10 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Back to Jobs
        </Link>
      </div>

      <div className="job-detail-layout">
        {/* Main content */}
        <div className="job-detail-main">
          {/* Header card */}
          <div className="job-detail-header-card">
            {job.is_featured && (
              <div className="job-detail-featured-badge">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <path d="M8 2L10 6H14L11 9L12 14L8 11.5L4 14L5 9L2 6H6L8 2Z" fill="currentColor"/>
                </svg>
                Featured Position
              </div>
            )}

            <div className="job-detail-header">
              <div className="job-detail-company-info">
                {job.company_logo ? (
                  <img
                    src={getMediaUrl(job.company_logo)}
                    alt={`${job.recruiter_company} logo`}
                    className="job-detail-logo"
                    onError={(e) => { e.target.style.display = 'none'; }}
                  />
                ) : (
                  <div className="job-detail-logo-placeholder">
                    {job.recruiter_company?.charAt(0) || '?'}
                  </div>
                )}
                <div>
                  <h1 className="job-detail-title">{job.title}</h1>
                  <p className="job-detail-company">{job.recruiter_company}</p>
                </div>
              </div>
            </div>

            {/* Quick info chips */}
            <div className="job-detail-chips">
              <span className="job-detail-chip chip-type">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <rect x="2" y="4" width="12" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M5 4V3C5 2.45 5.45 2 6 2H10C10.55 2 11 2.45 11 3V4" stroke="currentColor" strokeWidth="1.5"/>
                </svg>
                {getEmploymentLabel(job.employment_type)}
              </span>
              <span className="job-detail-chip chip-level">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <path d="M2 14V10M6 14V7M10 14V4M14 14V2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                {getExperienceLabel(job.experience_level)}
              </span>
              {locationStr && (
                <span className="job-detail-chip chip-location">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1C5.24 1 3 3.24 3 6C3 9.75 8 15 8 15C8 15 13 9.75 13 6C13 3.24 10.76 1 8 1ZM8 8C6.9 8 6 7.1 6 6C6 4.9 6.9 4 8 4C9.1 4 10 4.9 10 6C10 7.1 9.1 8 8 8Z" fill="currentColor"/>
                  </svg>
                  {locationStr}
                </span>
              )}
              {job.remote_allowed && (
                <span className="job-detail-chip chip-remote">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                    <rect x="1" y="3" width="14" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M5 14H11M8 12V14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  Remote
                </span>
              )}
              {job.department && (
                <span className="job-detail-chip chip-dept">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="5" r="3" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M2 14C2 11.24 4.69 9 8 9C11.31 9 14 11.24 14 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  {job.department}
                </span>
              )}
            </div>

            {/* Salary & posted */}
            <div className="job-detail-meta-row">
              {salary && (
                <div className="job-detail-salary">
                  <svg width="18" height="18" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M8 4V12M10 6.5C10 5.67 9.33 5 8 5C6.67 5 6 5.67 6 6.5C6 7.33 6.67 8 8 8C9.33 8 10 8.67 10 9.5C10 10.33 9.33 11 8 11C6.67 11 6 10.33 6 9.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  <span>{salary} <small>/ year</small></span>
                </div>
              )}
              <div className="job-detail-posted">
                Posted {timeAgo(job.published_at || job.created_at)}
                {job.published_at && (
                  <span className="job-detail-date"> · {formatDate(job.published_at)}</span>
                )}
              </div>
            </div>
          </div>

          {/* Description */}
          <div className="job-detail-section">
            <h2 className="job-detail-section-title">About This Role</h2>
            <div className="job-detail-text">{job.description}</div>
          </div>

          {/* Requirements */}
          {job.requirements && (
            <div className="job-detail-section">
              <h2 className="job-detail-section-title">Requirements</h2>
              <div className="job-detail-text">{job.requirements}</div>
            </div>
          )}

          {/* Responsibilities */}
          {job.responsibilities && (
            <div className="job-detail-section">
              <h2 className="job-detail-section-title">Responsibilities</h2>
              <div className="job-detail-text">{job.responsibilities}</div>
            </div>
          )}

          {/* Skills */}
          {skills.length > 0 && (
            <div className="job-detail-section">
              <h2 className="job-detail-section-title">Skills Required</h2>
              <div className="job-detail-skills">
                {skills.map((skill, i) => (
                  <span key={i} className="job-detail-skill-tag">{skill}</span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <aside className="job-detail-sidebar">
          {/* Apply card */}
          <div className="job-detail-apply-card">
            <h3>Interested in this role?</h3>
            {getSafeUrl(job.application_url) ? (
              <a
                href={getSafeUrl(job.application_url)}
                target="_blank"
                rel="noopener noreferrer"
                className="job-detail-apply-btn"
              >
                Apply Now
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M3 8H13M10 5L13 8L10 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </a>
            ) : isValidEmail(job.application_email) ? (
              <a
                href={`mailto:${encodeURI(job.application_email)}`}
                className="job-detail-apply-btn"
              >
                Apply via Email
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M2 4H14V12H2V4Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                  <path d="M2 4L8 9L14 4" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                </svg>
              </a>
            ) : (
              <p className="job-detail-no-apply">Contact the company directly to apply.</p>
            )}

            {job.application_deadline && (
              <p className="job-detail-deadline">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M8 4V8L11 10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                Apply by {formatDate(job.application_deadline)}
              </p>
            )}
          </div>

          {/* Job details card */}
          <div className="job-detail-info-card">
            <h3>Job Details</h3>
            <ul className="job-detail-info-list">
              <li>
                <span className="job-detail-info-label">Employment Type</span>
                <span className="job-detail-info-value">{getEmploymentLabel(job.employment_type)}</span>
              </li>
              <li>
                <span className="job-detail-info-label">Experience Level</span>
                <span className="job-detail-info-value">{getExperienceLabel(job.experience_level)}</span>
              </li>
              {locationStr && (
                <li>
                  <span className="job-detail-info-label">Location</span>
                  <span className="job-detail-info-value">{locationStr}</span>
                </li>
              )}
              {job.remote_allowed && (
                <li>
                  <span className="job-detail-info-label">Remote</span>
                  <span className="job-detail-info-value">Yes</span>
                </li>
              )}
              {salary && (
                <li>
                  <span className="job-detail-info-label">Salary Range</span>
                  <span className="job-detail-info-value">{salary}</span>
                </li>
              )}
              {job.department && (
                <li>
                  <span className="job-detail-info-label">Department</span>
                  <span className="job-detail-info-value">{job.department}</span>
                </li>
              )}
              <li>
                <span className="job-detail-info-label">Posted</span>
                <span className="job-detail-info-value">{formatDate(job.published_at || job.created_at)}</span>
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default JobDetail;
