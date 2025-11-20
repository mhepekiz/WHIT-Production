import React, { useState, useEffect } from 'react';
import { useRecruiterAuth } from '../contexts/RecruiterAuthContext';
import './RecruiterProfile.css';

const RecruiterProfile = () => {
  const { recruiterUser } = useRecruiterAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    company_name: '',
    company_website: '',
    company_description: '',
    contact_email: '',
    phone_number: '',
    address: '',
    city: '',
    state: '',
    country: '',
    postal_code: '',
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('recruiterToken');
      if (!token) {
        setError('Not authenticated. Please log in.');
        setLoading(false);
        return;
      }

      const response = await fetch('http://localhost:8000/api/recruiters/profile/me/', {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setProfile(data);
        setFormData({
          first_name: data.first_name || '',
          last_name: data.last_name || '',
          company_name: data.company_name || '',
          company_website: data.company_website || '',
          company_description: data.company_description || '',
          contact_email: data.contact_email || '',
          phone_number: data.phone_number || '',
          address: data.address || '',
          city: data.city || '',
          state: data.state || '',
          country: data.country || '',
          postal_code: data.postal_code || '',
        });
      } else {
        setError('Failed to load profile');
      }
    } catch (err) {
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setSaving(true);

    try {
      const token = localStorage.getItem('recruiterToken');
      const response = await fetch('http://localhost:8000/api/recruiters/profile/me/', {
        method: 'PATCH',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        setProfile(data);
        setSuccess('Profile updated successfully!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Failed to update profile');
      }
    } catch (err) {
      setError('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="profile-loading">Loading profile...</div>;
  }

  return (
    <div className="profile-container">
      <h1>Recruiter Profile</h1>
      <p className="profile-subtitle">Manage your company information and contact details</p>

      {error && <div className="alert error">{error}</div>}
      {success && <div className="alert success">{success}</div>}

      <form onSubmit={handleSubmit} className="profile-form">
        <section className="form-section">
          <h3>Personal Information</h3>
          <div className="form-group">
            <label htmlFor="first_name">First Name *</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="last_name">Last Name *</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>
        </section>

        <section className="form-section">
          <h3>Company Information</h3>
          <div className="form-group">
            <label htmlFor="company_name">Company Name *</label>
            <input
              type="text"
              id="company_name"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="company_website">Company Website</label>
            <input
              type="url"
              id="company_website"
              name="company_website"
              value={formData.company_website}
              onChange={handleChange}
              placeholder="https://example.com"
            />
          </div>
          <div className="form-group">
            <label htmlFor="company_description">Company Description</label>
            <textarea
              id="company_description"
              name="company_description"
              value={formData.company_description}
              onChange={handleChange}
              rows="4"
            />
          </div>
        </section>

        <section className="form-section">
          <h3>Contact Information</h3>
          <div className="form-group">
            <label htmlFor="contact_email">Contact Email *</label>
            <input
              type="email"
              id="contact_email"
              name="contact_email"
              value={formData.contact_email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="phone_number">Phone Number</label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
            />
          </div>
        </section>

        <section className="form-section">
          <h3>Address</h3>
          <div className="form-group">
            <label htmlFor="address">Street Address</label>
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="country">Country</label>
            <input
              type="text"
              id="country"
              name="country"
              value={formData.country}
              onChange={handleChange}
            />
          </div>
          <div className="form-row form-row-three">
            <div className="form-group">
              <label htmlFor="city">City</label>
              <input
                type="text"
                id="city"
                name="city"
                value={formData.city}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="state">State/Province</label>
              <input
                type="text"
                id="state"
                name="state"
                value={formData.state}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="postal_code">Postal Code</label>
              <input
                type="text"
                id="postal_code"
                name="postal_code"
                value={formData.postal_code}
                onChange={handleChange}
              />
            </div>
          </div>
        </section>

        {profile && profile.package && (
          <section className="form-section package-section">
            <h3>Current Package</h3>
            <div className="package-grid">
              <div className="package-item">
                <span>Package:</span>
                <strong>{profile.package.name}</strong>
              </div>
              <div className="package-item">
                <span>Price:</span>
                <strong>${profile.package.price}/month</strong>
              </div>
              <div className="package-item">
                <span>Job Openings:</span>
                <strong>
                  {profile.package.monthly_job_openings === 0 
                    ? 'Unlimited' 
                    : `${profile.package.monthly_job_openings}/month`}
                </strong>
              </div>
              <div className="package-item">
                <span>Searches:</span>
                <strong>
                  {profile.package.monthly_candidate_searches === 0 
                    ? 'Unlimited' 
                    : `${profile.package.monthly_candidate_searches}/month`}
                </strong>
              </div>
            </div>
          </section>
        )}

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default RecruiterProfile;
