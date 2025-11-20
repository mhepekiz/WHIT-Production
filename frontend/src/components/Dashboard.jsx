import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import PhoneInput from './PhoneInput';
import LocationInput from './LocationInput';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, token, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Profile state
  const [profile, setProfile] = useState({
    phone: '',
    location: '',
    bio: '',
    current_title: '',
    years_of_experience: '',
    linkedin_url: '',
    portfolio_url: '',
    github_url: '',
  });

  // Job preferences state
  const [jobPreferences, setJobPreferences] = useState({
    desired_functions: [],
    work_environments: [],
    employment_types: '',
    preferred_locations: '',
    willing_to_relocate: false,
    remote_only: false,
    minimum_salary: '',
    industries: '',
    company_size_preference: '',
    email_notifications: true,
    job_alerts: true,
  });

  // Available functions and work environments
  const [functions, setFunctions] = useState([]);
  const [workEnvironments, setWorkEnvironments] = useState([]);

  // Resume state
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeUrl, setResumeUrl] = useState('');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchDashboardData();
    fetchFunctions();
    fetchWorkEnvironments();
  }, [token, navigate]);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/accounts/dashboard/', {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setProfile(data.profile);
        setJobPreferences(data.job_preference);
        setResumeUrl(data.profile.resume_url || '');
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const fetchFunctions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/functions/');
      if (response.ok) {
        const data = await response.json();
        setFunctions(data);
      }
    } catch (error) {
      console.error('Error fetching functions:', error);
    }
  };

  const fetchWorkEnvironments = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/work-environments/');
      if (response.ok) {
        const data = await response.json();
        setWorkEnvironments(data);
      }
    } catch (error) {
      console.error('Error fetching work environments:', error);
    }
  };

  const handleProfileChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value,
    });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/accounts/profile/me/', {
        method: 'PATCH',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profile),
      });

      if (response.ok) {
        setMessage('Profile updated successfully!');
      } else {
        setMessage('Error updating profile');
      }
    } catch (error) {
      setMessage('Network error');
    }
    setLoading(false);
  };

  const handleJobPreferencesChange = (e) => {
    const { name, value, type, checked } = e.target;
    setJobPreferences({
      ...jobPreferences,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleFunctionToggle = (functionId) => {
    const current = jobPreferences.desired_functions || [];
    const updated = current.includes(functionId)
      ? current.filter(id => id !== functionId)
      : [...current, functionId];
    
    setJobPreferences({
      ...jobPreferences,
      desired_functions: updated,
    });
  };

  const handleWorkEnvironmentToggle = (workEnvId) => {
    const current = jobPreferences.work_environments || [];
    const updated = current.includes(workEnvId)
      ? current.filter(id => id !== workEnvId)
      : [...current, workEnvId];
    
    setJobPreferences({
      ...jobPreferences,
      work_environments: updated,
    });
  };

  const handleJobPreferencesSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/accounts/job-preferences/me/', {
        method: 'PATCH',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jobPreferences),
      });

      if (response.ok) {
        setMessage('Job preferences updated successfully!');
      } else {
        setMessage('Error updating job preferences');
      }
    } catch (error) {
      setMessage('Network error');
    }
    setLoading(false);
  };

  const handleResumeUpload = async (e) => {
    e.preventDefault();
    if (!resumeFile) return;

    setLoading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('resume', resumeFile);

    try {
      const response = await fetch('http://localhost:8000/api/accounts/profile/upload_resume/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResumeUrl(data.resume_url);
        setMessage('Resume uploaded successfully!');
        setResumeFile(null);
      } else {
        setMessage('Error uploading resume');
      }
    } catch (error) {
      setMessage('Network error');
    }
    setLoading(false);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <button onClick={handleLogout} className="btn-logout">Logout</button>
      </div>

      <div className="dashboard-tabs">
        <button
          className={activeTab === 'profile' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </button>
        <button
          className={activeTab === 'preferences' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('preferences')}
        >
          Job Preferences
        </button>
        <button
          className={activeTab === 'resume' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('resume')}
        >
          Resume
        </button>
      </div>

      <div className="dashboard-content">
        {message && <div className="message-box">{message}</div>}

        {activeTab === 'profile' && (
          <form onSubmit={handleProfileSubmit} className="dashboard-form">
            <h2>Personal Information</h2>
            
            <div className="form-row">
              <div className="form-group">
                <label>Phone</label>
                <PhoneInput
                  value={profile.phone || ''}
                  onChange={(value) => setProfile({ ...profile, phone: value })}
                />
              </div>

            </div>

            <div className="form-group full-width">
              <label>Location</label>
              <LocationInput
                value={profile.location || ''}
                onChange={(value) => setProfile({ ...profile, location: value })}
              />
            </div>

            <div className="form-group">
              <label>Bio</label>
              <textarea
                name="bio"
                value={profile.bio || ''}
                onChange={handleProfileChange}
                rows="4"
              />
            </div>

            <h2>Professional Information</h2>

            <div className="form-row">
              <div className="form-group">
                <label>Current Title</label>
                <input
                  type="text"
                  name="current_title"
                  value={profile.current_title || ''}
                  onChange={handleProfileChange}
                />
              </div>

              <div className="form-group">
                <label>Years of Experience</label>
                <input
                  type="number"
                  name="years_of_experience"
                  value={profile.years_of_experience || ''}
                  onChange={handleProfileChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label>LinkedIn URL</label>
              <input
                type="url"
                name="linkedin_url"
                value={profile.linkedin_url || ''}
                onChange={handleProfileChange}
              />
            </div>

            <div className="form-group">
              <label>Portfolio URL</label>
              <input
                type="url"
                name="portfolio_url"
                value={profile.portfolio_url || ''}
                onChange={handleProfileChange}
              />
            </div>

            <div className="form-group">
              <label>GitHub URL</label>
              <input
                type="url"
                name="github_url"
                value={profile.github_url || ''}
                onChange={handleProfileChange}
              />
            </div>

            <button type="submit" className="btn-save" disabled={loading}>
              {loading ? 'Saving...' : 'Save Profile'}
            </button>
          </form>
        )}

        {activeTab === 'preferences' && (
          <form onSubmit={handleJobPreferencesSubmit} className="dashboard-form">
            <h2>Desired Functions</h2>
            <div className="checkbox-grid">
              {functions.map(func => (
                <label key={func.id} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={jobPreferences.desired_functions?.includes(func.id)}
                    onChange={() => handleFunctionToggle(func.id)}
                  />
                  <span>{func.name}</span>
                </label>
              ))}
            </div>

            <h2>Work Environments</h2>
            <div className="checkbox-grid">
              {workEnvironments.map(env => (
                <label key={env.id} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={jobPreferences.work_environments?.includes(env.id)}
                    onChange={() => handleWorkEnvironmentToggle(env.id)}
                  />
                  <span>{env.name}</span>
                </label>
              ))}
            </div>

            <h2>Employment & Location</h2>

            <div className="form-group">
              <label>Employment Types (comma-separated)</label>
              <input
                type="text"
                name="employment_types"
                value={jobPreferences.employment_types || ''}
                onChange={handleJobPreferencesChange}
                placeholder="Full-time, Part-time, Contract"
              />
            </div>

            <div className="form-group">
              <label>Preferred Locations (comma-separated)</label>
              <input
                type="text"
                name="preferred_locations"
                value={jobPreferences.preferred_locations || ''}
                onChange={handleJobPreferencesChange}
                placeholder="San Francisco, New York, Remote"
              />
            </div>

            <div className="checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="willing_to_relocate"
                  checked={jobPreferences.willing_to_relocate}
                  onChange={handleJobPreferencesChange}
                />
                <span>Willing to relocate</span>
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="remote_only"
                  checked={jobPreferences.remote_only}
                  onChange={handleJobPreferencesChange}
                />
                <span>Remote only</span>
              </label>
            </div>

            <h2>Salary & Company</h2>

            <div className="form-group">
              <label>Minimum Salary</label>
              <select
                name="minimum_salary"
                value={jobPreferences.minimum_salary || ''}
                onChange={handleJobPreferencesChange}
              >
                <option value="">Select range</option>
                <option value="0-50k">$0 - $50,000</option>
                <option value="50k-75k">$50,000 - $75,000</option>
                <option value="75k-100k">$75,000 - $100,000</option>
                <option value="100k-150k">$100,000 - $150,000</option>
                <option value="150k-200k">$150,000 - $200,000</option>
                <option value="200k+">$200,000+</option>
              </select>
            </div>

            <div className="form-group">
              <label>Industries (comma-separated)</label>
              <input
                type="text"
                name="industries"
                value={jobPreferences.industries || ''}
                onChange={handleJobPreferencesChange}
                placeholder="Tech, Healthcare, Finance"
              />
            </div>

            <div className="form-group">
              <label>Company Size Preference</label>
              <input
                type="text"
                name="company_size_preference"
                value={jobPreferences.company_size_preference || ''}
                onChange={handleJobPreferencesChange}
                placeholder="Startup, Mid-size, Enterprise"
              />
            </div>

            <h2>Notifications</h2>

            <div className="checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="email_notifications"
                  checked={jobPreferences.email_notifications}
                  onChange={handleJobPreferencesChange}
                />
                <span>Email notifications</span>
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="job_alerts"
                  checked={jobPreferences.job_alerts}
                  onChange={handleJobPreferencesChange}
                />
                <span>Job alerts</span>
              </label>
            </div>

            <button type="submit" className="btn-save" disabled={loading}>
              {loading ? 'Saving...' : 'Save Preferences'}
            </button>
          </form>
        )}

        {activeTab === 'resume' && (
          <div className="dashboard-form">
            <h2>Resume Management</h2>

            {resumeUrl && (
              <div className="current-resume">
                <p>Current Resume:</p>
                <a href={resumeUrl} target="_blank" rel="noopener noreferrer" className="resume-link">
                  View Resume
                </a>
              </div>
            )}

            <form onSubmit={handleResumeUpload}>
              <div className="form-group">
                <label>Upload New Resume</label>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={(e) => setResumeFile(e.target.files[0])}
                />
                {resumeFile && (
                  <p className="file-name">Selected: {resumeFile.name}</p>
                )}
              </div>

              <button type="submit" className="btn-save" disabled={loading || !resumeFile}>
                {loading ? 'Uploading...' : 'Upload Resume'}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
