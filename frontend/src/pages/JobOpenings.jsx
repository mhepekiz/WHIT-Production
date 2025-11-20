import React, { useState, useEffect } from 'react';
import { Link, useOutletContext } from 'react-router-dom';
import { getJobOpenings, deleteJobOpening, createJobOpening } from '../services/recruiterApi';
import './JobOpenings.css';

function JobOpenings() {
  let context, usage;
  try {
    context = useOutletContext();
    usage = context?.usage;
  } catch (error) {
    console.log('Context not available:', error);
    context = {};
    usage = null;
  }
  
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, active, draft, closed

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const data = await getJobOpenings();
      console.log('Fetched jobs:', data);
      // API returns paginated response with results array
      const jobsList = data?.results || data || [];
      setJobs(Array.isArray(jobsList) ? jobsList : []);
    } catch (error) {
      console.error('Error fetching jobs:', error);
      setJobs([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this job opening?')) {
      try {
        await deleteJobOpening(id);
        setJobs(jobs.filter(job => job.id !== id));
      } catch (error) {
        console.error('Error deleting job:', error);
        alert('Failed to delete job opening');
      }
    }
  };

  const handleDuplicate = async (job) => {
    if (!canCreateJob()) {
      alert("You've reached your monthly job posting limit. Please upgrade your package to post more jobs.");
      return;
    }

    try {
      // Create a copy of the job without the ID and reset some fields
      const duplicatedJob = {
        ...job,
        title: `${job.title} (Copy)`,
        status: 'draft',
        views_count: undefined,
        applications_count: undefined,
        published_at: undefined,
        created_at: undefined,
        updated_at: undefined,
        id: undefined,
      };

      const newJob = await createJobOpening(duplicatedJob);
      
      // Refresh the jobs list
      fetchJobs();
      alert('Job duplicated successfully!');
    } catch (error) {
      console.error('Error duplicating job:', error);
      alert('Failed to duplicate job opening');
    }
  };

  const filteredJobs = filter === 'all' 
    ? (jobs || [])
    : (jobs || []).filter(job => job.status === filter);

  const canCreateJob = () => {
    if (!usage) return false;
    const limit = usage.package_limits.monthly_job_openings;
    if (limit === 0) return true; // Unlimited
    return usage.job_openings_created < limit;
  };

  console.log('JobOpenings render - loading:', loading, 'jobs:', jobs);

  if (loading) {
    return (
      <div className="job-openings-container">
        <div className="loading">Loading job openings...</div>
      </div>
    );
  }

  return (
    <div className="job-openings-container">
      <div className="page-header">
        <div className="header-content">
          <h2>Job Openings</h2>
          <p>Manage your job postings</p>
        </div>
        <div className="header-actions">
          {usage && (
            <div className="usage-badge">
              {usage.job_openings_created} / {usage.package_limits.monthly_job_openings === 0 ? '∞' : usage.package_limits.monthly_job_openings} jobs this month
            </div>
          )}
          {canCreateJob() ? (
            <Link to="/recruiter/dashboard/jobs/new" className="btn-primary">
              + New Job Opening
            </Link>
          ) : (
            <button className="btn-primary" disabled title="You've reached your monthly job posting limit">
              + New Job Opening
            </button>
          )}
        </div>
      </div>

      <div className="filter-tabs">
        <button 
          className={filter === 'all' ? 'active' : ''} 
          onClick={() => setFilter('all')}
        >
          All ({(jobs || []).length})
        </button>
        <button 
          className={filter === 'active' ? 'active' : ''} 
          onClick={() => setFilter('active')}
        >
          Active ({(jobs || []).filter(j => j.status === 'active').length})
        </button>
        <button 
          className={filter === 'draft' ? 'active' : ''} 
          onClick={() => setFilter('draft')}
        >
          Draft ({(jobs || []).filter(j => j.status === 'draft').length})
        </button>
        <button 
          className={filter === 'closed' ? 'active' : ''} 
          onClick={() => setFilter('closed')}
        >
          Closed ({(jobs || []).filter(j => j.status === 'closed').length})
        </button>
      </div>

      {filteredJobs.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">💼</div>
          <h3>No job openings found</h3>
          <p>
            {filter === 'all' 
              ? "You haven't created any job openings yet. Start by posting your first job!"
              : `No ${filter} job openings.`
            }
          </p>
          {filter === 'all' && canCreateJob() && (
            <Link to="/recruiter/dashboard/jobs/new" className="btn-primary">
              Create Your First Job
            </Link>
          )}
        </div>
      ) : (
        <div className="jobs-list">
          {filteredJobs.map(job => (
            <div key={job.id} className="job-card">
              <div className="job-card-header">
                <div className="job-title-section">
                  <h3>{job.title}</h3>
                  <div className="job-meta">
                    <span className="meta-item">📍 {job.location}</span>
                    <span className="meta-item">💼 {job.employment_type}</span>
                    <span className="meta-item">📅 Posted {new Date(job.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <div className="job-status">
                  <span className={`status-badge ${job.status}`}>
                    {job.status}
                  </span>
                  {job.is_featured && (
                    <span className="featured-badge">⭐ Featured</span>
                  )}
                </div>
              </div>

              <div className="job-card-body">
                <div className="job-stats">
                  <div className="stat-item">
                    <span className="stat-icon">👁️</span>
                    <div className="stat-details">
                      <span className="stat-value">{job.views_count}</span>
                      <span className="stat-label">Views</span>
                    </div>
                  </div>
                  <div className="stat-item">
                    <span className="stat-icon">📨</span>
                    <div className="stat-details">
                      <span className="stat-value">{job.applications_count}</span>
                      <span className="stat-label">Applications</span>
                    </div>
                  </div>
                  {job.application_deadline && (
                    <div className="stat-item">
                      <span className="stat-icon">⏰</span>
                      <div className="stat-details">
                        <span className="stat-value">
                          {new Date(job.application_deadline).toLocaleDateString()}
                        </span>
                        <span className="stat-label">Deadline</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="job-description">
                  <p>{job.description.substring(0, 150)}...</p>
                </div>

                {job.application_url && (
                  <div className="application-info">
                    <span className="info-label">Apply via:</span>
                    <a href={job.application_url} target="_blank" rel="noopener noreferrer" className="external-link">
                      {job.application_url}
                    </a>
                  </div>
                )}
              </div>

              <div className="job-card-footer">
                <Link to={`/recruiter/dashboard/jobs/${job.id}/edit`} className="btn-secondary">
                  Edit
                </Link>
                <button 
                  onClick={() => handleDuplicate(job)} 
                  className="btn-secondary"
                  disabled={!canCreateJob()}
                  title={canCreateJob() ? "Create a copy of this job opening" : "You've reached your monthly job posting limit"}
                >
                  Duplicate
                </button>
                <Link to={`/recruiter/dashboard/jobs/${job.id}/applications`} className="btn-secondary">
                  View Applications ({job.applications_count})
                </Link>
                <button 
                  onClick={() => handleDelete(job.id)} 
                  className="btn-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default JobOpenings;
