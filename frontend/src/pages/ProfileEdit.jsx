import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import PhoneInput from '../components/PhoneInput';
import LocationInput from '../components/LocationInput';
import './ProfileEdit.css';

const ProfileEdit = () => {
  const navigate = useNavigate();
  const { token } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

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

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchProfile();
  }, [token, navigate]);

  const fetchProfile = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/accounts/profile/me/', {
        headers: { 'Authorization': `Token ${token}` },
      });

      if (response.ok) {
        const data = await response.json();
        setProfile({
          phone: data.phone || '',
          location: data.location || '',
          bio: data.bio || '',
          current_title: data.current_title || '',
          years_of_experience: data.years_of_experience || '',
          linkedin_url: data.linkedin_url || '',
          portfolio_url: data.portfolio_url || '',
          github_url: data.github_url || '',
        });
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
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
        setMessage('Profile saved successfully!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        const error = await response.json();
        setMessage(error.phone?.[0] || 'Failed to save profile. Please try again.');
      }
    } catch (error) {
      console.error('Error saving profile:', error);
      setMessage('Network error. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="profile-edit-page">
      <div className="profile-container">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>

        <h1>Personal Information</h1>
        <p className="subtitle">Update your personal and professional details</p>

        {/* Contact Information */}
        <div className="profile-section">
          <h2 className="section-label">Contact Information</h2>
          
          <div className="form-field">
            <label>Phone</label>
            <PhoneInput
              value={profile.phone}
              onChange={(value) => setProfile({ ...profile, phone: value })}
            />
          </div>

          <div className="form-field">
            <label>Location</label>
            <LocationInput
              value={profile.location}
              onChange={(value) => setProfile({ ...profile, location: value })}
            />
          </div>
        </div>

        {/* Professional Information */}
        <div className="profile-section">
          <h2 className="section-label">Professional Information</h2>
          
          <div className="form-field">
            <label>Current Title</label>
            <input
              type="text"
              value={profile.current_title}
              onChange={(e) => setProfile({ ...profile, current_title: e.target.value })}
              placeholder="e.g., Senior Software Engineer"
              className="profile-input"
            />
          </div>

          <div className="form-field">
            <label>Years of Experience</label>
            <input
              type="number"
              value={profile.years_of_experience}
              onChange={(e) => setProfile({ ...profile, years_of_experience: e.target.value })}
              placeholder="e.g., 5"
              className="profile-input"
              min="0"
            />
          </div>

          <div className="form-field">
            <label>Bio</label>
            <textarea
              value={profile.bio}
              onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
              placeholder="Tell us about yourself..."
              className="profile-textarea"
              rows="4"
            />
          </div>
        </div>

        {/* Links */}
        <div className="profile-section">
          <h2 className="section-label">Professional Links</h2>
          
          <div className="form-field">
            <label>LinkedIn URL</label>
            <input
              type="url"
              value={profile.linkedin_url}
              onChange={(e) => setProfile({ ...profile, linkedin_url: e.target.value })}
              placeholder="https://linkedin.com/in/yourprofile"
              className="profile-input"
            />
          </div>

          <div className="form-field">
            <label>Portfolio URL</label>
            <input
              type="url"
              value={profile.portfolio_url}
              onChange={(e) => setProfile({ ...profile, portfolio_url: e.target.value })}
              placeholder="https://yourportfolio.com"
              className="profile-input"
            />
          </div>

          <div className="form-field">
            <label>GitHub URL</label>
            <input
              type="url"
              value={profile.github_url}
              onChange={(e) => setProfile({ ...profile, github_url: e.target.value })}
              placeholder="https://github.com/yourusername"
              className="profile-input"
            />
          </div>
        </div>

        {/* Save Button */}
        <div className="actions">
          {message && (
            <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}
          <button 
            onClick={handleSave}
            disabled={saving}
            className="save-button"
          >
            {saving ? 'Saving...' : 'Save Profile'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfileEdit;
