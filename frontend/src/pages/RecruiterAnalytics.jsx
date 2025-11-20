import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { getJobOpenings, getJobAnalytics } from '../services/recruiterApi';
import './RecruiterAnalytics.css';

function RecruiterAnalytics() {
  const context = useOutletContext();
  const profile = context?.profile;
  
  const [analytics, setAnalytics] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('all'); // all, month, week

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      const [analyticsData, jobsData] = await Promise.all([
        getJobAnalytics(),
        getJobOpenings()
      ]);
      
      setAnalytics(analyticsData);
      setJobs(jobsData?.results || []);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateAverages = () => {
    if (!jobs || jobs.length === 0) return { avgViews: 0, avgApplications: 0, conversionRate: 0 };
    
    const totalViews = jobs.reduce((sum, job) => sum + (job.views_count || 0), 0);
    const totalApplications = jobs.reduce((sum, job) => sum + (job.applications_count || 0), 0);
    
    const avgViews = Math.round(totalViews / jobs.length);
    const avgApplications = Math.round(totalApplications / jobs.length);
    const conversionRate = totalViews > 0 ? ((totalApplications / totalViews) * 100).toFixed(1) : 0;
    
    return { avgViews, avgApplications, conversionRate, totalViews, totalApplications };
  };

  const getTopPerformingJobs = () => {
    return [...jobs]
      .sort((a, b) => (b.applications_count || 0) - (a.applications_count || 0))
      .slice(0, 5);
  };

  const getJobsByStatus = () => {
    const statusCounts = {
      active: jobs.filter(j => j.status === 'active').length,
      draft: jobs.filter(j => j.status === 'draft').length,
      paused: jobs.filter(j => j.status === 'paused').length,
      closed: jobs.filter(j => j.status === 'closed').length,
    };
    return statusCounts;
  };

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading">Loading analytics...</div>
      </div>
    );
  }

  const stats = calculateAverages();
  const topJobs = getTopPerformingJobs();
  const statusCounts = getJobsByStatus();

  return (
    <div className="analytics-container">
      <div className="page-header">
        <div className="header-content">
          <h2>Analytics Dashboard</h2>
          <p>Track your job postings performance and recruitment metrics</p>
        </div>
        <div className="time-range-selector">
          <button 
            className={timeRange === 'week' ? 'active' : ''} 
            onClick={() => setTimeRange('week')}
          >
            Last 7 Days
          </button>
          <button 
            className={timeRange === 'month' ? 'active' : ''} 
            onClick={() => setTimeRange('month')}
          >
            Last 30 Days
          </button>
          <button 
            className={timeRange === 'all' ? 'active' : ''} 
            onClick={() => setTimeRange('all')}
          >
            All Time
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon">💼</div>
          <div className="metric-content">
            <h3>Total Job Postings</h3>
            <p className="metric-value">{jobs.length}</p>
            <span className="metric-label">Active: {statusCounts.active}</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">👁️</div>
          <div className="metric-content">
            <h3>Total Views</h3>
            <p className="metric-value">{stats.totalViews.toLocaleString()}</p>
            <span className="metric-label">Avg: {stats.avgViews} per job</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">📨</div>
          <div className="metric-content">
            <h3>Total Applications</h3>
            <p className="metric-value">{stats.totalApplications.toLocaleString()}</p>
            <span className="metric-label">Avg: {stats.avgApplications} per job</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">📊</div>
          <div className="metric-content">
            <h3>Conversion Rate</h3>
            <p className="metric-value">{stats.conversionRate}%</p>
            <span className="metric-label">Views to applications</span>
          </div>
        </div>
      </div>

      {/* Job Status Distribution */}
      <div className="analytics-section">
        <h3>Job Status Distribution</h3>
        <div className="status-grid">
          <div className="status-card active-card">
            <div className="status-count">{statusCounts.active}</div>
            <div className="status-label">Active</div>
            <div className="status-percentage">
              {jobs.length > 0 ? ((statusCounts.active / jobs.length) * 100).toFixed(0) : 0}%
            </div>
          </div>
          <div className="status-card draft-card">
            <div className="status-count">{statusCounts.draft}</div>
            <div className="status-label">Draft</div>
            <div className="status-percentage">
              {jobs.length > 0 ? ((statusCounts.draft / jobs.length) * 100).toFixed(0) : 0}%
            </div>
          </div>
          <div className="status-card paused-card">
            <div className="status-count">{statusCounts.paused}</div>
            <div className="status-label">Paused</div>
            <div className="status-percentage">
              {jobs.length > 0 ? ((statusCounts.paused / jobs.length) * 100).toFixed(0) : 0}%
            </div>
          </div>
          <div className="status-card closed-card">
            <div className="status-count">{statusCounts.closed}</div>
            <div className="status-label">Closed</div>
            <div className="status-percentage">
              {jobs.length > 0 ? ((statusCounts.closed / jobs.length) * 100).toFixed(0) : 0}%
            </div>
          </div>
        </div>
      </div>

      {/* Top Performing Jobs */}
      <div className="analytics-section">
        <h3>Top Performing Job Postings</h3>
        {topJobs.length > 0 ? (
          <div className="top-jobs-list">
            {topJobs.map((job, index) => (
              <div key={job.id} className="top-job-item">
                <div className="job-rank">#{index + 1}</div>
                <div className="job-details">
                  <h4>{job.title}</h4>
                  <p>{job.location} • {job.employment_type}</p>
                </div>
                <div className="job-metrics">
                  <div className="metric-small">
                    <span className="metric-icon-small">👁️</span>
                    <span>{job.views_count}</span>
                  </div>
                  <div className="metric-small">
                    <span className="metric-icon-small">📨</span>
                    <span>{job.applications_count}</span>
                  </div>
                  <div className="metric-small">
                    <span className="metric-icon-small">📊</span>
                    <span>
                      {job.views_count > 0 
                        ? ((job.applications_count / job.views_count) * 100).toFixed(1) 
                        : 0}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state-small">
            <p>No job postings available yet</p>
          </div>
        )}
      </div>

      {/* All Jobs Performance */}
      <div className="analytics-section">
        <h3>All Jobs Performance</h3>
        {jobs.length > 0 ? (
          <div className="performance-table">
            <table>
              <thead>
                <tr>
                  <th>Job Title</th>
                  <th>Status</th>
                  <th>Location</th>
                  <th>Views</th>
                  <th>Applications</th>
                  <th>Conversion</th>
                  <th>Posted</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map(job => (
                  <tr key={job.id}>
                    <td className="job-title-cell">
                      <strong>{job.title}</strong>
                      {job.is_featured && <span className="featured-tag">⭐ Featured</span>}
                    </td>
                    <td>
                      <span className={`status-badge ${job.status}`}>
                        {job.status}
                      </span>
                    </td>
                    <td>{job.location}</td>
                    <td className="number-cell">{job.views_count}</td>
                    <td className="number-cell">{job.applications_count}</td>
                    <td className="number-cell">
                      {job.views_count > 0 
                        ? ((job.applications_count / job.views_count) * 100).toFixed(1) 
                        : 0}%
                    </td>
                    <td>{new Date(job.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state-small">
            <p>No job postings to analyze</p>
          </div>
        )}
      </div>

      {/* Package Information */}
      {profile && (
        <div className="analytics-section package-info-section">
          <h3>Your Package: {profile.package?.name}</h3>
          <div className="package-features">
            <div className="feature-item">
              <span className="feature-label">Analytics Level:</span>
              <span className="feature-value">{profile.package?.analytics_level || 'Basic'}</span>
            </div>
            <div className="feature-item">
              <span className="feature-label">Monthly Job Postings:</span>
              <span className="feature-value">
                {profile.package?.monthly_job_openings === 0 
                  ? 'Unlimited' 
                  : profile.package?.monthly_job_openings}
              </span>
            </div>
            <div className="feature-item">
              <span className="feature-label">Data Export:</span>
              <span className="feature-value">
                {profile.package?.can_export_data ? 'Enabled' : 'Not Available'}
              </span>
            </div>
          </div>
          {profile.package?.analytics_level === 'basic' && (
            <div className="upgrade-prompt">
              <p>📈 Upgrade to get advanced analytics including trend analysis, candidate insights, and custom reports!</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default RecruiterAnalytics;
