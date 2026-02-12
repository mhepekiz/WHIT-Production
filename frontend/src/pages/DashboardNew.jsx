import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getApiUrl } from '../services/api';
import './DashboardNew.css';

const DashboardNew = () => {
  const navigate = useNavigate();
  const { user, token } = useAuth();
  const [profile, setProfile] = useState(null);
  const [jobPreferences, setJobPreferences] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchDashboardData();
  }, [token, navigate]);

  const fetchDashboardData = async () => {
    try {
      const [profileRes, prefsRes] = await Promise.all([
        fetch(getApiUrl('accounts/profile/me/'), {
          headers: { 'Authorization': `Token ${token}` },
        }),
        fetch(getApiUrl('accounts/job-preferences/me/'), {
          headers: { 'Authorization': `Token ${token}` },
        }),
      ]);

      if (profileRes.ok) {
        const profileData = await profileRes.json();
        setProfile(profileData);
      }
      if (prefsRes.ok) {
        const prefsData = await prefsRes.json();
        setJobPreferences(prefsData);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateProfileCompletion = () => {
    if (!profile) return 0;
    
    let completed = 0;
    let total = 0;
    
    // Profile fields (7 fields)
    const profileFields = [
      { name: 'phone', value: profile.phone, check: (v) => v && v.trim() !== '' },
      { name: 'location', value: profile.location, check: (v) => v && v.trim() !== '' },
      { name: 'bio', value: profile.bio, check: (v) => v && v.trim() !== '' },
      { name: 'current_title', value: profile.current_title, check: (v) => v && v.trim() !== '' },
      { name: 'years_of_experience', value: profile.years_of_experience, check: (v) => v !== null && v !== undefined && v !== '' },
      { name: 'linkedin_url', value: profile.linkedin_url, check: (v) => v && v.trim() !== '' },
      { name: 'resume', value: profile.resume, check: (v) => v && v.trim() !== '' },
    ];
    
    profileFields.forEach(field => {
      total++;
      const isComplete = field.check(field.value);
      if (isComplete) completed++;
      console.log(`${field.name}: ${isComplete ? '✓' : '✗'} (value: ${JSON.stringify(field.value)})`);
    });
    
    // Job preferences fields (3 fields - excluding employment_types as it's not in UI)
    if (jobPreferences) {
      const prefsFields = [
        { name: 'desired_functions', value: jobPreferences.desired_functions, check: (v) => Array.isArray(v) && v.length > 0 },
        { name: 'work_environments', value: jobPreferences.work_environments, check: (v) => Array.isArray(v) && v.length > 0 },
        { name: 'preferred_locations', value: jobPreferences.preferred_locations, check: (v) => v && typeof v === 'string' && v.trim() !== '' },
      ];
      
      prefsFields.forEach(field => {
        total++;
        const isComplete = field.check(field.value);
        if (isComplete) completed++;
        console.log(`${field.name}: ${isComplete ? '✓' : '✗'} (value: ${JSON.stringify(field.value)})`);
      });
    } else {
      total += 3; // Add 3 for uncompleted preference fields
    }
    
    console.log(`Profile Completion: ${completed}/${total} = ${Math.round((completed / total) * 100)}%`);
    return Math.round((completed / total) * 100);
  };

  if (loading) {
    return <div className="dashboard-loading">Loading...</div>;
  }

  const completionPercentage = calculateProfileCompletion();
  
  // Get user info from profile or user context
  const userInfo = profile?.user || user;
  const fullName = userInfo?.first_name && userInfo?.last_name 
    ? `${userInfo.first_name} ${userInfo.last_name}` 
    : userInfo?.first_name || userInfo?.username || 'there';

  return (
    <div className="dashboard-new">
      <div className="dashboard-container">
        {/* Welcome Header */}
        <div className="welcome-header">
          <h1>Welcome back, {fullName}! 👋</h1>
          <p className="subtitle">Manage your profile and job search preferences - Updated</p>
        </div>

        {/* Profile Completion Card */}
        <div className="completion-card">
          <h2>Profile Completion</h2>
          <div className="progress-bar-container">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${completionPercentage}%` }}
              >
                <span className="progress-percentage">{completionPercentage}%</span>
              </div>
            </div>
          </div>
          <p className="completion-message">
            Complete your profile to get better job matches!
          </p>
        </div>

        {/* Quick Actions Grid */}
        <div className="actions-grid">
          {/* Personal Info Card */}
          <Link to="/dashboard/profile" className="action-card">
            <div className="card-icon">
              <span className="icon-symbol">👤</span>
            </div>
            <div className="card-content">
              <h3>Personal Info</h3>
              <p>Update your name, location, and contact details</p>
            </div>
            <div className="card-arrow">→</div>
          </Link>

          {/* Job Preferences Card */}
          <Link to="/dashboard/preferences" className="action-card">
            <div className="card-icon">
              <span className="icon-symbol">⚙️</span>
            </div>
            <div className="card-content">
              <h3>Job Preferences</h3>
              <p>Set your preferred job functions and work environment</p>
            </div>
            <div className="card-arrow">→</div>
          </Link>

          {/* Resume Card */}
          <Link to="/dashboard/resume" className="action-card">
            <div className="card-icon">
              <span className="icon-symbol">📄</span>
            </div>
            <div className="card-content">
              <h3>Resume</h3>
              <p>Upload and manage your resume</p>
            </div>
            <div className="card-arrow">→</div>
          </Link>

          {/* Browse Companies Card */}
          <Link to="/companies" className="action-card">
            <div className="card-icon">
              <span className="icon-symbol">🔍</span>
            </div>
            <div className="card-content">
              <h3>Browse Companies</h3>
              <p>Explore tech companies that are hiring</p>
            </div>
            <div className="card-arrow">→</div>
          </Link>
        </div>

        {/* Account Information */}
        <div className="account-info-card">
          <h2>Account Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>EMAIL:</label>
              <p>{userInfo?.email || 'Not provided'}</p>
            </div>
            <div className="info-item">
              <label>NAME:</label>
              <p>{fullName || 'Not set'}</p>
            </div>
            <div className="info-item">
              <label>LOCATION:</label>
              <p>{profile?.location ? 
                  profile.location.split(';').map(part => {
                    const [key, value] = part.split(':');
                    return value;
                  }).filter(Boolean).join(', ') 
                  : 'Not set'}</p>
            </div>
            <div className="info-item">
              <label>CURRENT TITLE:</label>
              <p>{profile?.current_title || 'Not set'}</p>
            </div>
            <div className="info-item">
              <label>EXPERIENCE:</label>
              <p>{profile?.years_of_experience ? `${profile.years_of_experience} years` : 'Not set'}</p>
            </div>
            <div className="info-item">
              <label>RESUME:</label>
              <p>{profile?.resume ? '✓ Uploaded' : 'Not uploaded'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardNew;
