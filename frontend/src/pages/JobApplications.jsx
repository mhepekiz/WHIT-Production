import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { getJobApplications, updateApplicationStatus } from '../services/recruiterApi';
import './JobApplications.css';

function JobApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedApplication, setSelectedApplication] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const [notes, setNotes] = useState('');
  const [showNotesModal, setShowNotesModal] = useState(false);
  const [pendingStatusUpdate, setPendingStatusUpdate] = useState(null);
  
  // Interview scheduling state
  const [showInterviewModal, setShowInterviewModal] = useState(false);
  const [interviewDate, setInterviewDate] = useState('');
  const [interviewTime, setInterviewTime] = useState('');
  const [selectedApplicationForInterview, setSelectedApplicationForInterview] = useState(null);

  let context = {};
  try {
    context = useOutletContext();
  } catch (e) {
    console.log('No outlet context available');
  }

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      setLoading(true);
      const data = await getJobApplications();
      const apps = data.results || data || [];
      console.log('Fetched applications:', apps);
      setApplications(apps);
    } catch (err) {
      setError('Failed to load applications');
      console.error('Error fetching applications:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (applicationId, newStatus, notesText = '') => {
    try {
      setUpdatingStatus(true);
      await updateApplicationStatus(applicationId, newStatus, notesText);
      await fetchApplications();
      setShowDetailModal(false);
      setShowNotesModal(false);
      setSelectedApplication(null);
      setNotes('');
      setPendingStatusUpdate(null);
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Failed to update application status';
      alert(errorMsg);
      console.error('Error updating status:', err);
      console.error('Error response:', err.response);
    } finally {
      setUpdatingStatus(false);
    }
  };

  const openNotesModal = (applicationId, newStatus) => {
    setPendingStatusUpdate({ applicationId, newStatus });
    setNotes('');
    setShowNotesModal(true);
  };

  const handleNotesSubmit = () => {
    if (pendingStatusUpdate) {
      handleStatusUpdate(pendingStatusUpdate.applicationId, pendingStatusUpdate.newStatus, notes);
    }
  };

  // Interview scheduling functions
  const openInterviewModal = (applicationId) => {
    const application = applications.find(app => app.id === applicationId);
    setSelectedApplicationForInterview(application);
    
    // If there's an existing interview date, populate the form
    if (application.interview_date) {
      const date = new Date(application.interview_date);
      setInterviewDate(date.toISOString().split('T')[0]);
      setInterviewTime(date.toTimeString().slice(0, 5));
    } else {
      setInterviewDate('');
      setInterviewTime('');
    }
    
    setShowInterviewModal(true);
  };

  const handleInterviewSchedule = async () => {
    if (!interviewDate || !interviewTime) {
      alert('Please select both date and time for the interview.');
      return;
    }

    try {
      setUpdatingStatus(true);
      const interviewDateTime = `${interviewDate}T${interviewTime}:00`;
      
      // Update application with interview date and set status to 'interviewed'
      await updateApplicationStatus(
        selectedApplicationForInterview.id, 
        'interviewed', 
        `Interview scheduled for ${new Date(interviewDateTime).toLocaleString()}`,
        interviewDateTime
      );
      
      // Update local state
      setApplications(prev => prev.map(app => 
        app.id === selectedApplicationForInterview.id 
          ? { ...app, status: 'interviewed', interview_date: interviewDateTime }
          : app
      ));
      
      setShowInterviewModal(false);
      setInterviewDate('');
      setInterviewTime('');
      setSelectedApplicationForInterview(null);
      
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Failed to schedule interview';
      alert(errorMsg);
      console.error('Error scheduling interview:', err);
    } finally {
      setUpdatingStatus(false);
    }
  };

  const getStatusBadgeClass = (status) => {
    const statusMap = {
      'pending': 'status-pending',
      'reviewing': 'status-review',
      'shortlisted': 'status-shortlisted',
      'interviewed': 'status-interview',
      'offered': 'status-offered',
      'accepted': 'status-accepted',
      'rejected': 'status-rejected',
      'withdrawn': 'status-withdrawn',
    };
    return statusMap[status] || 'status-pending';
  };

  const getStatusLabel = (status) => {
    const labels = {
      'pending': 'Pending',
      'under_review': 'Under Review',
      'interview': 'Shortlisted',
      'interviewed': 'Interviewed',
      'offered': 'Offered',
      'accepted': 'Accepted',
      'rejected': 'Rejected',
      'withdrawn': 'Withdrawn',
    };
    return labels[status] || status;
  };

  const filteredApplications = filterStatus === 'all'
    ? applications
    : applications.filter(app => app.status === filterStatus);

  const stats = {
    total: applications.length,
    pending: applications.filter(a => a.status === 'pending').length,
    reviewing: applications.filter(a => a.status === 'reviewing').length,
    shortlisted: applications.filter(a => a.status === 'shortlisted').length,
    interviewed: applications.filter(a => a.status === 'interviewed').length,
    offered: applications.filter(a => a.status === 'offered').length,
    accepted: applications.filter(a => a.status === 'accepted').length,
    rejected: applications.filter(a => a.status === 'rejected').length,
  };

  return (
    <div className="applications-container">
      <div className="page-header">
        <div className="header-content">
          <h2>Job Applications</h2>
          <p>Review and manage applications for your job openings</p>
        </div>
        <div className="stats-summary">
          <div className="stat-item">
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Total</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{stats.pending + stats.reviewing}</span>
            <span className="stat-label">To Review</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{stats.interviewed + stats.offered}</span>
            <span className="stat-label">Interview+</span>
          </div>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">{error}</div>
      )}

      {/* Filter Tabs */}
      <div className="filter-tabs">
        <button
          className={`filter-tab ${filterStatus === 'all' ? 'active' : ''}`}
          onClick={() => setFilterStatus('all')}
        >
          All ({stats.total})
        </button>
        <button
          className={`filter-tab ${filterStatus === 'pending' ? 'active' : ''}`}
          onClick={() => setFilterStatus('pending')}
        >
          Pending ({stats.pending})
        </button>
        <button
          className={`filter-tab ${filterStatus === 'reviewing' ? 'active' : ''}`}
          onClick={() => setFilterStatus('reviewing')}
        >
          Reviewing ({stats.reviewing})
        </button>
        <button
          className={`filter-tab ${filterStatus === 'shortlisted' ? 'active' : ''}`}
          onClick={() => setFilterStatus('shortlisted')}
        >
          Shortlisted ({stats.shortlisted})
        </button>
        <button
          className={`filter-tab ${filterStatus === 'interviewed' ? 'active' : ''}`}
          onClick={() => setFilterStatus('interviewed')}
        >
          Interviewed ({stats.interviewed})
        </button>
        <button
          className={`filter-tab ${filterStatus === 'offered' ? 'active' : ''}`}
          onClick={() => setFilterStatus('offered')}
        >
          Offered ({stats.offered})
        </button>
        <button
          className={`filter-tab ${filterStatus === 'rejected' ? 'active' : ''}`}
          onClick={() => setFilterStatus('rejected')}
        >
          Rejected ({stats.rejected})
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading applications...</div>
      ) : filteredApplications.length > 0 ? (
        <div className="applications-grid">
          {filteredApplications.map((application) => (
            <div key={application.id} className="application-card">
              <div className="application-header">
                <div className="applicant-info">
                  <div className="applicant-avatar">
                    {application.candidate_name ? 
                      application.candidate_name.split(' ').map(n => n[0]).join('').toUpperCase() 
                      : 'NA'}
                  </div>
                  <div>
                    <h3>{application.candidate_name || 'Anonymous'}</h3>
                    <p className="applicant-email">{application.candidate_email}</p>
                  </div>
                </div>
                <span className={`status-badge ${getStatusBadgeClass(application.status)}`}>
                  {getStatusLabel(application.status)}
                </span>
              </div>

              <div className="job-title">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <rect x="3" y="4" width="10" height="9" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M6 4V3C6 2.44772 6.44772 2 7 2H9C9.55228 2 10 2.44772 10 3V4" stroke="currentColor" strokeWidth="1.5"/>
                </svg>
                {application.job_title}
              </div>

              {application.cover_letter && (
                <div className="cover-letter-preview">
                  <p>{application.cover_letter.substring(0, 150)}...</p>
                </div>
              )}

              <div className="application-meta">
                <span className="meta-item">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <circle cx="7" cy="7" r="6" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M7 3.5V7L9 9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  Applied: {new Date(application.applied_at).toLocaleDateString()}
                </span>
                {application.interview_date && (
                  <span className="meta-item">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <circle cx="7" cy="7" r="6" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M7 3.5V7L9 9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    Interview: {new Date(application.interview_date).toLocaleString()}
                  </span>
                )}
              </div>

              <div className="application-actions">
                <button 
                  className="btn btn-secondary btn-small"
                  onClick={() => {
                    setSelectedApplication(application);
                    setShowDetailModal(true);
                  }}
                >
                  View Details
                </button>
                
                {application.status === 'pending' && (
                  <>
                    <button 
                      className="btn btn-primary btn-small"
                      onClick={() => openNotesModal(application.id, 'under_review')}
                      disabled={updatingStatus}
                    >
                      Review
                    </button>
                    <button 
                      className="btn btn-success btn-small"
                      onClick={() => openNotesModal(application.id, 'shortlisted')}
                      disabled={updatingStatus}
                    >
                      Shortlist
                    </button>
                  </>
                )}
                
                {application.status === 'under_review' && (
                  <>
                    <button 
                      className="btn btn-success btn-small"
                      onClick={() => openNotesModal(application.id, 'interview')}
                      disabled={updatingStatus}
                    >
                      Shortlist
                    </button>
                    <button 
                      className="btn btn-danger btn-small"
                      onClick={() => openNotesModal(application.id, 'rejected')}
                      disabled={updatingStatus}
                    >
                      Reject
                    </button>
                  </>
                )}
                
                {application.status === 'interview' && (
                  <>
                    <button 
                      className="btn btn-primary btn-small"
                      onClick={() => openInterviewModal(application.id)}
                      disabled={updatingStatus}
                    >
                      {application.interview_date ? 'Reschedule Interview' : 'Schedule Interview'}
                    </button>
                    <button 
                      className="btn btn-success btn-small"
                      onClick={() => openNotesModal(application.id, 'offered')}
                      disabled={updatingStatus}
                    >
                      Make Offer
                    </button>
                    <button 
                      className="btn btn-danger btn-small"
                      onClick={() => openNotesModal(application.id, 'rejected')}
                      disabled={updatingStatus}
                    >
                      Reject
                    </button>
                  </>
                )}                {application.status === 'shortlisted' && (
                  <>
                    <button 
                      className="btn btn-success btn-small"
                      onClick={() => openNotesModal(application.id, 'offered')}
                      disabled={updatingStatus}
                    >
                      Make Offer
                    </button>
                    <button 
                      className="btn btn-danger btn-small"
                      onClick={() => openNotesModal(application.id, 'rejected')}
                      disabled={updatingStatus}
                    >
                      Reject
                    </button>
                  </>
                )}
                
                {application.status === 'offered' && (
                  <button 
                    className="btn btn-success btn-small"
                    onClick={() => handleStatusUpdate(application.id, 'accepted')}
                    disabled={updatingStatus}
                  >
                    Mark Accepted
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
            <rect x="16" y="20" width="32" height="36" rx="2" stroke="currentColor" strokeWidth="3"/>
            <path d="M24 20V16C24 14.8954 24.8954 14 26 14H38C39.1046 14 40 14.8954 40 16V20" stroke="currentColor" strokeWidth="3"/>
            <path d="M24 32H40M24 40H40M24 48H32" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
          </svg>
          <h3>No Applications Yet</h3>
          <p>Applications will appear here once candidates start applying to your jobs</p>
        </div>
      )}

      {/* Detail Modal */}
      {showDetailModal && selectedApplication ? (
        <div className="modal-overlay" onClick={() => setShowDetailModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Application Details</h3>
              <button className="modal-close" onClick={() => setShowDetailModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
            
            <div className="modal-body">
              <div className="applicant-details">
                <div className="applicant-avatar-large">
                  {selectedApplication.candidate_name ? 
                    selectedApplication.candidate_name.split(' ').map(n => n[0]).join('').toUpperCase() 
                    : 'NA'}
                </div>
                <div className="applicant-info-detail">
                  <h2>{selectedApplication.candidate_name}</h2>
                  {selectedApplication.candidate_profile?.current_title && (
                    <p className="current-title">{selectedApplication.candidate_profile.current_title}</p>
                  )}
                  {selectedApplication.candidate_profile?.location && (
                    <p className="location">
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M7 1C4.79 1 3 2.79 3 5C3 7.5 7 13 7 13C7 13 11 7.5 11 5C11 2.79 9.21 1 7 1Z" stroke="currentColor" strokeWidth="1.5"/>
                        <circle cx="7" cy="5" r="1.5" stroke="currentColor" strokeWidth="1.5"/>
                      </svg>
                      {selectedApplication.candidate_profile.location}
                    </p>
                  )}
                  <span className={`status-badge ${getStatusBadgeClass(selectedApplication.status)}`}>
                    {getStatusLabel(selectedApplication.status)}
                  </span>
                </div>
              </div>

              {/* Contact Information */}
              <div className="detail-section">
                <h4>Contact Information</h4>
                {selectedApplication.can_view_contact ? (
                  <div className="contact-info">
                    {selectedApplication.candidate_email && (
                      <div className="contact-item">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <rect x="2" y="4" width="12" height="8" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                          <path d="M2 5L8 9L14 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        <a href={`mailto:${selectedApplication.candidate_email}`}>{selectedApplication.candidate_email}</a>
                      </div>
                    )}
                    {selectedApplication.candidate_phone && (
                      <div className="contact-item">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path d="M3 2H6L7 5L5 6C5 6 6 9 9 10L10 8L13 9V12C13 12 3 14 3 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        <a href={`tel:${selectedApplication.candidate_phone}`}>{selectedApplication.candidate_phone}</a>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="upgrade-notice">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <path d="M10 2L12.5 7L18 8L14 12L15 18L10 15L5 18L6 12L2 8L7.5 7L10 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                    </svg>
                    <p>Upgrade to Premium to view contact details</p>
                  </div>
                )}
              </div>

              <div className="detail-section">
                <h4>Applying For</h4>
                <p className="job-title-large">{selectedApplication.job_title}</p>
                {selectedApplication.job_department && (
                  <p className="job-department">{selectedApplication.job_department}</p>
                )}
              </div>

              {/* Professional Profile */}
              {selectedApplication.candidate_profile && (
                <>
                  {selectedApplication.candidate_profile.bio && (
                    <div className="detail-section">
                      <h4>About</h4>
                      <p className="bio-text">{selectedApplication.candidate_profile.bio}</p>
                    </div>
                  )}

                  <div className="detail-section">
                    <h4>Professional Details</h4>
                    <div className="profile-grid">
                      {selectedApplication.candidate_profile.years_of_experience > 0 && (
                        <div className="profile-item">
                          <span className="profile-label">Experience</span>
                          <span className="profile-value">{selectedApplication.candidate_profile.years_of_experience} years</span>
                        </div>
                      )}
                      {selectedApplication.candidate_profile.employment_type && (
                        <div className="profile-item">
                          <span className="profile-label">Desired Employment</span>
                          <span className="profile-value">{selectedApplication.candidate_profile.employment_type}</span>
                        </div>
                      )}
                      {selectedApplication.candidate_profile.actively_looking !== undefined && (
                        <div className="profile-item">
                          <span className="profile-label">Job Search Status</span>
                          <span className={`profile-value ${selectedApplication.candidate_profile.actively_looking ? 'active-looking' : ''}`}>
                            {selectedApplication.candidate_profile.actively_looking ? '🟢 Actively Looking' : 'Open to Opportunities'}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>

                  {selectedApplication.candidate_profile.desired_roles && selectedApplication.candidate_profile.desired_roles.length > 0 && (
                    <div className="detail-section">
                      <h4>Desired Roles</h4>
                      <div className="roles-list">
                        {selectedApplication.candidate_profile.desired_roles.map((role, index) => (
                          <span key={index} className="role-tag">{role}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {(selectedApplication.candidate_profile.expected_salary_min || selectedApplication.candidate_profile.expected_salary_max) && (
                    <div className="detail-section">
                      <h4>Salary Expectations</h4>
                      <p className="salary-range">
                        ${selectedApplication.candidate_profile.expected_salary_min?.toLocaleString() || '0'} - 
                        ${selectedApplication.candidate_profile.expected_salary_max?.toLocaleString() || '0'}
                      </p>
                    </div>
                  )}

                  {(selectedApplication.candidate_profile.linkedin_url || selectedApplication.candidate_profile.github_url || selectedApplication.candidate_profile.portfolio_url) && (
                    <div className="detail-section">
                      <h4>Links</h4>
                      <div className="social-links">
                        {selectedApplication.candidate_profile.linkedin_url && (
                          <a href={selectedApplication.candidate_profile.linkedin_url} target="_blank" rel="noopener noreferrer" className="social-link">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                              <path d="M14 0H2C0.9 0 0 0.9 0 2V14C0 15.1 0.9 16 2 16H14C15.1 16 16 15.1 16 14V2C16 0.9 15.1 0 14 0ZM5 13H3V6H5V13ZM4 5C3.4 5 3 4.6 3 4C3 3.4 3.4 3 4 3C4.6 3 5 3.4 5 4C5 4.6 4.6 5 4 5ZM13 13H11V9.5C11 8.7 10.3 8 9.5 8C8.7 8 8 8.7 8 9.5V13H6V6H8V7C8.5 6.4 9.2 6 10 6C11.7 6 13 7.3 13 9V13Z"/>
                            </svg>
                            LinkedIn
                          </a>
                        )}
                        {selectedApplication.candidate_profile.github_url && (
                          <a href={selectedApplication.candidate_profile.github_url} target="_blank" rel="noopener noreferrer" className="social-link">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                              <path d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.59C5.87 15.66 6.02 15.42 6.02 15.21C6.02 15.02 6.01 14.39 6.01 13.72C4 14.09 3.48 13.23 3.32 12.78C3.23 12.55 2.84 11.84 2.5 11.65C2.22 11.5 1.82 11.13 2.49 11.12C3.12 11.11 3.57 11.7 3.72 11.94C4.44 13.15 5.59 12.81 6.05 12.6C6.12 12.08 6.33 11.73 6.56 11.53C4.78 11.33 2.92 10.64 2.92 7.58C2.92 6.71 3.23 5.99 3.74 5.43C3.66 5.23 3.38 4.41 3.82 3.31C3.82 3.31 4.49 3.1 6.02 4.13C6.66 3.95 7.34 3.86 8.02 3.86C8.7 3.86 9.38 3.95 10.02 4.13C11.55 3.09 12.22 3.31 12.22 3.31C12.66 4.41 12.38 5.23 12.3 5.43C12.81 5.99 13.12 6.7 13.12 7.58C13.12 10.65 11.25 11.33 9.47 11.53C9.76 11.78 10.01 12.26 10.01 13.01C10.01 14.08 10 14.94 10 15.21C10 15.42 10.15 15.67 10.55 15.59C13.71 14.53 16 11.53 16 8C16 3.58 12.42 0 8 0Z"/>
                            </svg>
                            GitHub
                          </a>
                        )}
                        {selectedApplication.candidate_profile.portfolio_url && (
                          <a href={selectedApplication.candidate_profile.portfolio_url} target="_blank" rel="noopener noreferrer" className="social-link">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                              <rect x="2" y="3" width="12" height="10" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                              <path d="M2 6H14" stroke="currentColor" strokeWidth="1.5"/>
                              <circle cx="4.5" cy="4.5" r="0.5" fill="currentColor"/>
                              <circle cx="6" cy="4.5" r="0.5" fill="currentColor"/>
                            </svg>
                            Portfolio
                          </a>
                        )}
                      </div>
                    </div>
                  )}
                </>
              )}

              {(selectedApplication.resume_file || selectedApplication.profile_resume) && (
                <div className="detail-section">
                  <h4>Resume</h4>
                  {(() => {
                    const resumeUrl = selectedApplication.resume_file || selectedApplication.profile_resume;
                    const fullUrl = resumeUrl?.startsWith('http') ? resumeUrl : `http://localhost:8000${resumeUrl}`;
                    return (
                      <a href={fullUrl} target="_blank" rel="noopener noreferrer" className="resume-link">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path d="M4 2H9L12 5V14H4V2Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                          <path d="M9 2V5H12" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                        </svg>
                        View Resume
                      </a>
                    );
                  })()}
                  {selectedApplication.resume_file && selectedApplication.profile_resume && (
                    <p className="resume-note">Application includes a specific resume</p>
                  )}
                  {!selectedApplication.resume_file && selectedApplication.profile_resume && (
                    <p className="resume-note">From candidate's profile</p>
                  )}
                </div>
              )}

              {selectedApplication.cover_letter && (
                <div className="detail-section">
                  <h4>Cover Letter</h4>
                  <div className="cover-letter-full">
                    {selectedApplication.cover_letter}
                  </div>
                </div>
              )}

              <div className="detail-section">
                <h4>Application Date</h4>
                <p>{new Date(selectedApplication.applied_at).toLocaleString()}</p>
              </div>

              {selectedApplication.recruiter_notes && (
                <div className="detail-section">
                  <h4>Your Notes</h4>
                  <p>{selectedApplication.recruiter_notes}</p>
                </div>
              )}
            </div>

            <div className="modal-footer">
              <div className="status-actions">
                {selectedApplication.status !== 'rejected' && selectedApplication.status !== 'accepted' && (
                  <button 
                    className="btn btn-danger"
                    onClick={() => {
                      setShowDetailModal(false);
                      openNotesModal(selectedApplication.id, 'rejected');
                    }}
                    disabled={updatingStatus}
                  >
                    Reject
                  </button>
                )}
                {selectedApplication.status === 'pending' && (
                  <>
                    <button 
                      className="btn btn-primary"
                      onClick={() => {
                        setShowDetailModal(false);
                        openNotesModal(selectedApplication.id, 'under_review');
                      }}
                      disabled={updatingStatus}
                    >
                      Start Review
                    </button>
                    <button 
                      className="btn btn-success"
                      onClick={() => {
                        setShowDetailModal(false);
                        openNotesModal(selectedApplication.id, 'interview');
                      }}
                      disabled={updatingStatus}
                    >
                      Shortlist
                    </button>
                  </>
                )}
                {selectedApplication.status === 'under_review' && (
                  <button 
                    className="btn btn-success"
                    onClick={() => {
                      setShowDetailModal(false);
                      openNotesModal(selectedApplication.id, 'interview');
                    }}
                    disabled={updatingStatus}
                  >
                    Shortlist
                  </button>
                )}
                {selectedApplication.status === 'interview' && (
                  <button 
                    className="btn btn-primary"
                    onClick={() => {
                      setShowDetailModal(false);
                      openInterviewModal(selectedApplication.id);
                    }}
                    disabled={updatingStatus}
                  >
                    {selectedApplication.interview_date ? 'Reschedule Interview' : 'Schedule Interview'}
                  </button>
                )}
                {selectedApplication.status === 'interview' && (
                  <button 
                    className="btn btn-success"
                    onClick={() => {
                      setShowDetailModal(false);
                      openNotesModal(selectedApplication.id, 'offered');
                    }}
                    disabled={updatingStatus}
                  >
                    Make Offer
                  </button>
                )}
                {selectedApplication.status === 'offered' && (
                  <button 
                    className="btn btn-success"
                    onClick={() => handleStatusUpdate(selectedApplication.id, 'accepted')}
                    disabled={updatingStatus}
                  >
                    Mark Accepted
                  </button>
                )}
              </div>
            </div>
          </div>
                      <button 
                        className="btn btn-success"
                        onClick={() => {
                          setShowDetailModal(false);
                          openNotesModal(selectedApplication.id, 'offered');
                        }}
                        disabled={updatingStatus}
                      >
                        Make Offer
                      </button>
        </div>
      ) : null}

      {/* Notes Modal */}
      {showNotesModal && (
        <div className="modal-overlay" onClick={() => setShowNotesModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add Notes</h3>
              <button className="modal-close" onClick={() => setShowNotesModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
            
            <div className="modal-body">
              <div className="form-group">
                <label htmlFor="notes">Recruiter Notes (Optional)</label>
                <textarea
                  id="notes"
                  className="form-textarea"
                  rows="5"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add any notes about this candidate or decision..."
                />
              </div>
            </div>

            <div className="modal-footer">
              <button 
                className="btn btn-secondary"
                onClick={() => setShowNotesModal(false)}
              >
                Cancel
              </button>
              <button 
                className="btn btn-primary"
                onClick={handleNotesSubmit}
                disabled={updatingStatus}
              >
                {updatingStatus ? 'Updating...' : 'Confirm'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Interview Scheduling Modal */}
      {showInterviewModal && selectedApplicationForInterview && (
        <div className="modal-overlay" onClick={() => setShowInterviewModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                {selectedApplicationForInterview.interview_date ? 'Reschedule Interview' : 'Schedule Interview'}
              </h3>
              <button className="modal-close" onClick={() => setShowInterviewModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
            
            <div className="modal-body">
              <div className="candidate-info" style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
                <h4>{selectedApplicationForInterview.candidate_name}</h4>
                <p>{selectedApplicationForInterview.job_title}</p>
              </div>

              <div className="form-group">
                <label htmlFor="interviewDate">Interview Date</label>
                <input
                  type="date"
                  id="interviewDate"
                  className="form-input"
                  value={interviewDate}
                  onChange={(e) => setInterviewDate(e.target.value)}
                  min={new Date().toISOString().split('T')[0]}
                />
              </div>

              <div className="form-group">
                <label htmlFor="interviewTime">Interview Time</label>
                <input
                  type="time"
                  id="interviewTime"
                  className="form-input"
                  value={interviewTime}
                  onChange={(e) => setInterviewTime(e.target.value)}
                />
              </div>

              {selectedApplicationForInterview.interview_date && (
                <div className="current-interview" style={{ padding: '10px', backgroundColor: '#e7f3ff', borderRadius: '6px', marginBottom: '15px' }}>
                  <strong>Current Interview:</strong> {new Date(selectedApplicationForInterview.interview_date).toLocaleString()}
                </div>
              )}
            </div>

            <div className="modal-footer">
              <button 
                className="btn btn-secondary"
                onClick={() => setShowInterviewModal(false)}
              >
                Cancel
              </button>
              <button 
                className="btn btn-primary"
                onClick={handleInterviewSchedule}
                disabled={updatingStatus || !interviewDate || !interviewTime}
              >
                {updatingStatus ? 'Scheduling...' : selectedApplicationForInterview.interview_date ? 'Reschedule' : 'Schedule'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default JobApplications;
