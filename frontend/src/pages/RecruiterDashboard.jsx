import React, { useState, useEffect } from 'react';
import { useNavigate, Outlet, NavLink } from 'react-router-dom';
import { useRecruiterAuth } from '../contexts/RecruiterAuthContext';
import { getRecruiterProfile, getRecruiterUsage } from '../services/recruiterApi';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faChartLine, 
  faUser, 
  faBriefcase, 
  faChartBar, 
  faSearch, 
  faClipboardList, 
  faEnvelope, 
  faSignOutAlt,
  faTachometerAlt
} from '@fortawesome/free-solid-svg-icons';
import './RecruiterDashboard.css';

function RecruiterDashboard() {
  const navigate = useNavigate();
  const { isAuthenticated, recruiterUser, logout } = useRecruiterAuth();
  const [profile, setProfile] = useState(null);
  const [usage, setUsage] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/recruiter/login');
    } else {
      fetchData();
    }
  }, [isAuthenticated, navigate]);

  const fetchData = async () => {
    try {
      const [profileData, usageData] = await Promise.all([
        getRecruiterProfile(),
        getRecruiterUsage()
      ]);
      setProfile(profileData);
      setUsage(usageData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/recruiter/login');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="recruiter-dashboard">
      {/* Sidebar Navigation */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <h2>WHIT Recruiter</h2>
          {profile && (
            <div className="company-info">
              <h3>{profile.company_name}</h3>
              <p className="package-badge">{profile.package?.name}</p>
            </div>
          )}
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/recruiter/dashboard" end className="nav-item">
            <span className="nav-icon">
              <FontAwesomeIcon icon={faTachometerAlt} />
            </span>
            <span>Overview</span>
          </NavLink>
          <NavLink to="/recruiter/dashboard/profile" className="nav-item">
            <span className="nav-icon">
              <FontAwesomeIcon icon={faUser} />
            </span>
            <span>Profile</span>
          </NavLink>
          <NavLink to="/recruiter/dashboard/jobs" className="nav-item">
            <span className="nav-icon">
              <FontAwesomeIcon icon={faBriefcase} />
            </span>
            <span>Job Openings</span>
          </NavLink>
          <NavLink to="/recruiter/dashboard/analytics" className="nav-item">
            <span className="nav-icon">
              <FontAwesomeIcon icon={faChartLine} />
            </span>
            <span>Analytics</span>
          </NavLink>
          <NavLink to="/recruiter/dashboard/candidates" className="nav-item">
            <span className="nav-icon">
              <FontAwesomeIcon icon={faSearch} />
            </span>
            <span>Search Candidates</span>
          </NavLink>
          <NavLink to="/recruiter/dashboard/applications" className="nav-item">
            <span className="nav-icon">
              <FontAwesomeIcon icon={faClipboardList} />
            </span>
            <span>Applications</span>
          </NavLink>
          {profile?.package?.messaging_enabled && (
            <NavLink to="/recruiter/dashboard/messages" className="nav-item">
              <span className="nav-icon">
                <FontAwesomeIcon icon={faEnvelope} />
              </span>
              <span>Messages</span>
            </NavLink>
          )}
        </nav>

        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-btn">
            <span className="nav-icon">
              <FontAwesomeIcon icon={faSignOutAlt} />
            </span>
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="dashboard-header">
          <div className="user-welcome">
            <h1>Welcome back, {recruiterUser?.first_name}!</h1>
            <p>{new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
          </div>

          {usage && (
            <div className="usage-summary">
              <div className="usage-item">
                <span className="usage-label">Job Openings</span>
                <span className="usage-value">
                  {usage.job_openings_created} / {usage.package_limits.monthly_job_openings === 0 ? '∞' : usage.package_limits.monthly_job_openings}
                </span>
              </div>
              <div className="usage-item">
                <span className="usage-label">Searches</span>
                <span className="usage-value">
                  {usage.candidates_searched} / {usage.package_limits.monthly_candidate_searches === 0 ? '∞' : usage.package_limits.monthly_candidate_searches}
                </span>
              </div>
              {profile?.package?.messaging_enabled && (
                <div className="usage-item">
                  <span className="usage-label">Messages</span>
                  <span className="usage-value">
                    {usage.messages_sent} / {usage.package_limits.monthly_messages === 0 ? '∞' : usage.package_limits.monthly_messages}
                  </span>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="dashboard-content">
          <Outlet context={{ profile, usage, refreshData: fetchData }} />
        </div>
      </main>
    </div>
  );
}

export default RecruiterDashboard;
