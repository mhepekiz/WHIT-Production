import React, { useState, useEffect } from 'react';
import { Link, useOutletContext } from 'react-router-dom';
import { getJobOpenings, getJobAnalytics, getJobApplications } from '../services/recruiterApi';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBriefcase, faEye, faFileAlt, faCheckCircle, faPlus, faSearch, faClipboardList, faChartBar } from '@fortawesome/free-solid-svg-icons';
import './DashboardOverview.css';

function DashboardOverview() {
  const { profile, usage } = useOutletContext();
  const [analytics, setAnalytics] = useState(null);
  const [recentJobs, setRecentJobs] = useState([]);
  const [recentApplications, setRecentApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOverviewData();
  }, []);

  const fetchOverviewData = async () => {
    try {
      const [analyticsData, jobsData, applicationsData] = await Promise.all([
        getJobAnalytics(),
        getJobOpenings(),
        getJobApplications()
      ]);
      
      setAnalytics(analyticsData);
      setRecentJobs(jobsData.slice(0, 5));
      setRecentApplications(applicationsData.slice(0, 5));
    } catch (error) {
      console.error('Error fetching overview data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading overview...</div>;
  }

  return (
    <div className="dashboard-overview">
      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon"><FontAwesomeIcon icon={faBriefcase} /></div>
          <div className="stat-content">
            <h3>{analytics?.total_jobs || 0}</h3>
            <p>Total Job Postings</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon"><FontAwesomeIcon icon={faEye} /></div>
          <div className="stat-content">
            <h3>{analytics?.total_views || 0}</h3>
            <p>Total Views</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon"><FontAwesomeIcon icon={faFileAlt} /></div>
          <div className="stat-content">
            <h3>{analytics?.total_applications || 0}</h3>
            <p>Total Applications</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon"><FontAwesomeIcon icon={faCheckCircle} /></div>
          <div className="stat-content">
            <h3>{analytics?.active_jobs || 0}</h3>
            <p>Active Jobs</p>
          </div>
        </div>
      </div>

      {/* Package Info */}
      <div className="package-info-card">
        <h3>Your Package: {profile?.package?.name}</h3>
        <div className="package-limits">
          <div className="limit-item">
            <span>Job Openings</span>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ 
                  width: `${usage?.package_limits.monthly_job_openings === 0 ? 0 : 
                    (usage?.job_openings_created / usage?.package_limits.monthly_job_openings * 100)}%` 
                }}
              />
            </div>
            <span className="limit-text">
              {usage?.job_openings_created} / {usage?.package_limits.monthly_job_openings === 0 ? 'Unlimited' : usage?.package_limits.monthly_job_openings}
            </span>
          </div>

          <div className="limit-item">
            <span>Candidate Searches</span>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ 
                  width: `${usage?.package_limits.monthly_candidate_searches === 0 ? 0 : 
                    (usage?.candidates_searched / usage?.package_limits.monthly_candidate_searches * 100)}%` 
                }}
              />
            </div>
            <span className="limit-text">
              {usage?.candidates_searched} / {usage?.package_limits.monthly_candidate_searches === 0 ? 'Unlimited' : usage?.package_limits.monthly_candidate_searches}
            </span>
          </div>

          {profile?.package?.messaging_enabled && (
            <div className="limit-item">
              <span>Messages</span>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ 
                    width: `${usage?.package_limits.monthly_messages === 0 ? 0 : 
                      (usage?.messages_sent / usage?.package_limits.monthly_messages * 100)}%` 
                  }}
                />
              </div>
              <span className="limit-text">
                {usage?.messages_sent} / {usage?.package_limits.monthly_messages === 0 ? 'Unlimited' : usage?.package_limits.monthly_messages}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <div className="actions-grid">
          <Link to="/recruiter/dashboard/jobs/new" className="action-card action-post">
            <span className="action-icon"><FontAwesomeIcon icon={faPlus} /></span>
            <span>Post New Job</span>
          </Link>
          <Link to="/recruiter/dashboard/candidates" className="action-card action-search">
            <span className="action-icon"><FontAwesomeIcon icon={faSearch} /></span>
            <span>Search Candidates</span>
          </Link>
          <Link to="/recruiter/dashboard/applications" className="action-card action-apps">
            <span className="action-icon"><FontAwesomeIcon icon={faClipboardList} /></span>
            <span>View Applications</span>
          </Link>
          <Link to="/recruiter/dashboard/analytics" className="action-card action-analytics">
            <span className="action-icon"><FontAwesomeIcon icon={faChartBar} /></span>
            <span>View Analytics</span>
          </Link>
        </div>
      </div>

      {/* Recent Jobs */}
      <div className="recent-section">
        <div className="section-header">
          <h3>Recent Job Postings</h3>
          <Link to="/recruiter/dashboard/jobs" className="view-all-link">View All</Link>
        </div>
        {recentJobs.length > 0 ? (
          <div className="jobs-list">
            {recentJobs.map(job => (
              <div key={job.id} className="job-item">
                <div className="job-info">
                  <h4>{job.title}</h4>
                  <p>{job.location} • {job.employment_type}</p>
                </div>
                <div className="job-stats">
                  <span className={`status-badge ${job.status}`}>{job.status}</span>
                  <span className="stat">{job.views_count} views</span>
                  <span className="stat">{job.applications_count} applications</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No job postings yet</p>
            <Link to="/recruiter/dashboard/jobs/new" className="btn-primary">Post Your First Job</Link>
          </div>
        )}
      </div>

      {/* Recent Applications */}
      <div className="recent-section">
        <div className="section-header">
          <h3>Recent Applications</h3>
          <Link to="/recruiter/dashboard/applications" className="view-all-link">View All</Link>
        </div>
        {recentApplications.length > 0 ? (
          <div className="applications-list">
            {recentApplications.map(app => (
              <div key={app.id} className="application-item">
                <div className="applicant-info">
                  <h4>{app.candidate_name}</h4>
                  <p>{app.job_title}</p>
                </div>
                <div className="application-meta">
                  <span className={`status-badge ${app.status}`}>{app.status}</span>
                  <span className="date">{new Date(app.applied_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No applications yet</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default DashboardOverview;
