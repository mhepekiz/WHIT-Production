import { useNavigate } from 'react-router-dom';
import { getMediaUrl } from '../services/api';
import './JobCard.css';

/** Only allow http/https URLs to prevent javascript: injection */
const getSafeUrl = (url) => {
  if (!url) return null;
  try {
    const parsed = new URL(url, window.location.origin);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') return url;
  } catch { /* invalid URL */ }
  return null;
};

const getEmploymentTypeClass = (type) => {
  switch (type) {
    case 'full-time': return 'chip-engineering';
    case 'part-time': return 'chip-product';
    case 'contract': return 'chip-data';
    case 'internship': return 'chip-internship';
    case 'temporary': return 'chip-marketing';
    default: return 'chip-neutral';
  }
};

const getExperienceLevelClass = (level) => {
  switch (level) {
    case 'entry': return 'chip-internship';
    case 'mid': return 'chip-engineering';
    case 'senior': return 'chip-data';
    case 'lead': return 'chip-product';
    case 'executive': return 'chip-design';
    default: return 'chip-neutral';
  }
};

const getExperienceLabel = (level) => {
  const labels = {
    'entry': 'Entry Level',
    'mid': 'Mid Level',
    'senior': 'Senior',
    'lead': 'Lead/Manager',
    'executive': 'Executive',
  };
  return labels[level] || level;
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

const formatSalary = (min, max, currency = 'USD') => {
  const fmt = (val) => {
    const num = Number(val);
    if (num >= 1000) return `${Math.round(num / 1000)}k`;
    return num.toString();
  };

  if (min && max) return `$${fmt(min)} - $${fmt(max)}`;
  if (min) return `From $${fmt(min)}`;
  if (max) return `Up to $${fmt(max)}`;
  return null;
};

const timeAgo = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays}d ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}mo ago`;
  return `${Math.floor(diffDays / 365)}y ago`;
};

function JobCard({ job }) {
  const navigate = useNavigate();
  if (!job) return null;

  const salary = formatSalary(job.salary_min, job.salary_max, job.salary_currency);
  const skills = job.skills_required || [];
  const visibleSkills = skills.slice(0, 4);
  const hiddenSkillCount = skills.length - 4;

  const locationParts = [job.city, job.state, job.country].filter(Boolean);
  const locationStr = locationParts.join(', ');

  const handleCardClick = (e) => {
    // Don't navigate if clicking a link or button
    if (e.target.closest('a') || e.target.closest('button')) return;
    navigate(`/jobs/${job.id}`);
  };

  return (
    <div className={`job-card ${job.is_featured ? 'featured' : ''}`} onClick={handleCardClick} style={{ cursor: 'pointer' }}>
      {job.is_featured && (
        <div className="job-card-featured-badge">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
            <path d="M8 2L10 6H14L11 9L12 14L8 11.5L4 14L5 9L2 6H6L8 2Z" 
                  fill="currentColor" />
          </svg>
          Featured
        </div>
      )}

      {/* Header */}
      <div className="job-card-header">
        <div className="job-card-company-info">
          {job.company_logo ? (
            <img
              src={getMediaUrl(job.company_logo)}
              alt={`${job.recruiter_company} logo`}
              className="job-card-logo"
              onError={(e) => { e.target.style.display = 'none'; }}
            />
          ) : (
            <div className="job-card-logo-placeholder">
              {job.recruiter_company?.charAt(0) || '?'}
            </div>
          )}
          <div>
            <h3 className="job-card-title">{job.title}</h3>
            <p className="job-card-company">{job.recruiter_company}</p>
          </div>
        </div>
        <span className="job-card-posted">{timeAgo(job.published_at || job.created_at)}</span>
      </div>

      {/* Meta chips */}
      <div className="job-card-meta">
        <span className={`chip ${getEmploymentTypeClass(job.employment_type)}`}>
          {getEmploymentLabel(job.employment_type)}
        </span>
        <span className={`chip ${getExperienceLevelClass(job.experience_level)}`}>
          {getExperienceLabel(job.experience_level)}
        </span>
        {job.remote_allowed && (
          <span className="chip chip-remote">Remote</span>
        )}
      </div>

      {/* Location & Salary */}
      <div className="job-card-details">
        {locationStr && (
          <div className="job-card-detail">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <path d="M8 1C5.24 1 3 3.24 3 6C3 9.75 8 15 8 15C8 15 13 9.75 13 6C13 3.24 10.76 1 8 1ZM8 8C6.9 8 6 7.1 6 6C6 4.9 6.9 4 8 4C9.1 4 10 4.9 10 6C10 7.1 9.1 8 8 8Z" 
                    fill="currentColor" opacity="0.6"/>
            </svg>
            <span>{locationStr}</span>
          </div>
        )}
        {salary && (
          <div className="job-card-detail">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" opacity="0.6"/>
              <path d="M8 4V12M10 6.5C10 5.67 9.33 5 8 5C6.67 5 6 5.67 6 6.5C6 7.33 6.67 8 8 8C9.33 8 10 8.67 10 9.5C10 10.33 9.33 11 8 11C6.67 11 6 10.33 6 9.5" 
                    stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.6"/>
            </svg>
            <span>{salary}</span>
          </div>
        )}
        {job.department && (
          <div className="job-card-detail">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <rect x="2" y="4" width="12" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.5" opacity="0.6"/>
              <path d="M5 4V3C5 2.45 5.45 2 6 2H10C10.55 2 11 2.45 11 3V4" stroke="currentColor" strokeWidth="1.5" opacity="0.6"/>
            </svg>
            <span>{job.department}</span>
          </div>
        )}
      </div>

      {/* Skills */}
      {visibleSkills.length > 0 && (
        <div className="job-card-skills">
          {visibleSkills.map((skill, i) => (
            <span key={i} className="job-card-skill">{skill}</span>
          ))}
          {hiddenSkillCount > 0 && (
            <span className="job-card-skill job-card-skill-more">+{hiddenSkillCount}</span>
          )}
        </div>
      )}

      {/* Description excerpt */}
      <p className="job-card-description">
        {job.description?.length > 160
          ? job.description.substring(0, 160) + '...'
          : job.description}
      </p>

      {/* Actions */}
      <div className="job-card-actions">
        {getSafeUrl(job.application_url) && (
          <a
            href={getSafeUrl(job.application_url)}
            target="_blank"
            rel="noopener noreferrer"
            className="job-card-btn primary"
          >
            Apply Now
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <path d="M3 8H13M10 5L13 8L10 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
        )}

        {job.application_deadline && (
          <span className="job-card-deadline">
            Deadline: {new Date(job.application_deadline).toLocaleDateString()}
          </span>
        )}
      </div>
    </div>
  );
}

export default JobCard;
