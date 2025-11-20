import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useOutletContext } from 'react-router-dom';
import { createJobOpening, updateJobOpening, getJobOpenings } from '../services/recruiterApi';
import './JobOpeningForm.css';

function JobOpeningForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const context = useOutletContext();
  const profile = context?.profile;
  const isEditMode = Boolean(id);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    requirements: '',
    responsibilities: '',
    employment_type: 'full-time',
    experience_level: 'mid',
    salary_min: '',
    salary_max: '',
    salary_currency: 'USD',
    location: '',
    city: '',
    state: '',
    country: '',
    remote_allowed: false,
    skills_required: '',
    department: '',
    status: 'draft',
    application_deadline: '',
    application_method: 'platform', // 'platform' or 'external'
    application_url: '',
    application_email: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEditMode) {
      fetchJobData();
    }
  }, [id]);

  const fetchJobData = async () => {
    try {
      const data = await getJobOpenings();
      // API returns paginated response with results array
      const jobsList = data?.results || data || [];
      const job = jobsList.find(j => j.id === parseInt(id));
      if (job) {
        setFormData({
          ...job,
          skills_required: Array.isArray(job.skills_required) ? job.skills_required.join(', ') : '',
          application_method: job.application_url ? 'external' : 'platform',
          application_deadline: job.application_deadline || '',
        });
      } else {
        setError('Job not found');
      }
    } catch (error) {
      console.error('Error fetching job:', error);
      setError('Failed to load job data');
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Prepare data for submission
      const submitData = {
        ...formData,
        skills_required: formData.skills_required 
          ? formData.skills_required.split(',').map(s => s.trim()).filter(Boolean)
          : [],
        salary_min: formData.salary_min ? parseFloat(formData.salary_min) : null,
        salary_max: formData.salary_max ? parseFloat(formData.salary_max) : null,
        application_url: formData.application_method === 'external' ? formData.application_url : '',
        application_email: formData.application_method === 'platform' ? (formData.application_email || profile?.contact_email) : '',
      };

      if (isEditMode) {
        await updateJobOpening(id, submitData);
      } else {
        await createJobOpening(submitData);
      }

      navigate('/recruiter/dashboard/jobs');
    } catch (error) {
      console.error('Error saving job:', error);
      setError(error.response?.data?.detail || 'Failed to save job opening');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="job-form-container">
      <div className="page-header">
        <h2>{isEditMode ? 'Edit Job Opening' : 'Create New Job Opening'}</h2>
        <p>Fill in the details for your job posting</p>
      </div>

      {error && (
        <div className="alert error">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="job-form">
        {/* Basic Information */}
        <section className="form-section">
          <h3>Basic Information</h3>
          
          <div className="form-group">
            <label htmlFor="title">Job Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="e.g., Senior Frontend Developer"
            />
          </div>

          <div className="form-group">
            <label htmlFor="department">Department</label>
            <input
              type="text"
              id="department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              placeholder="e.g., Engineering, Marketing"
            />
          </div>

          <div className="form-group">
            <label htmlFor="employment_type">Employment Type *</label>
            <select
              id="employment_type"
              name="employment_type"
              value={formData.employment_type}
              onChange={handleChange}
              required
            >
              <option value="full-time">Full Time</option>
              <option value="part-time">Part Time</option>
              <option value="contract">Contract</option>
              <option value="internship">Internship</option>
              <option value="temporary">Temporary</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="experience_level">Experience Level *</label>
            <select
              id="experience_level"
              name="experience_level"
              value={formData.experience_level}
              onChange={handleChange}
              required
            >
              <option value="entry">Entry Level</option>
              <option value="mid">Mid Level</option>
              <option value="senior">Senior Level</option>
              <option value="lead">Lead/Manager</option>
              <option value="executive">Executive</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="status">Status</label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="draft">Draft</option>
              <option value="active">Active</option>
              <option value="paused">Paused</option>
              <option value="closed">Closed</option>
            </select>
          </div>
        </section>

        {/* Job Details */}
        <section className="form-section">
          <h3>Job Details</h3>
          
          <div className="form-group">
            <label htmlFor="description">Job Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="6"
              placeholder="Describe the role, company culture, and what makes this opportunity great..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="requirements">Requirements *</label>
            <textarea
              id="requirements"
              name="requirements"
              value={formData.requirements}
              onChange={handleChange}
              required
              rows="6"
              placeholder="List the required qualifications, skills, and experience..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="responsibilities">Responsibilities</label>
            <textarea
              id="responsibilities"
              name="responsibilities"
              value={formData.responsibilities}
              onChange={handleChange}
              rows="6"
              placeholder="Describe the day-to-day responsibilities and expectations..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="skills_required">Required Skills (comma-separated)</label>
            <input
              type="text"
              id="skills_required"
              name="skills_required"
              value={formData.skills_required}
              onChange={handleChange}
              placeholder="React, TypeScript, Node.js, AWS"
            />
          </div>
        </section>

        {/* Compensation */}
        <section className="form-section">
          <h3>Compensation</h3>
          
          <div className="form-group">
            <label htmlFor="salary_min">Minimum Salary</label>
            <input
              type="number"
              id="salary_min"
              name="salary_min"
              value={formData.salary_min}
              onChange={handleChange}
              placeholder="50000"
              step="1000"
            />
          </div>

          <div className="form-group">
            <label htmlFor="salary_max">Maximum Salary</label>
            <input
              type="number"
              id="salary_max"
              name="salary_max"
              value={formData.salary_max}
              onChange={handleChange}
              placeholder="80000"
              step="1000"
            />
          </div>

          <div className="form-group">
            <label htmlFor="salary_currency">Currency</label>
            <select
              id="salary_currency"
              name="salary_currency"
              value={formData.salary_currency}
              onChange={handleChange}
            >
              <option value="USD">USD - US Dollar</option>
              <option value="EUR">EUR - Euro</option>
              <option value="GBP">GBP - British Pound</option>
              <option value="CAD">CAD - Canadian Dollar</option>
              <option value="AUD">AUD - Australian Dollar</option>
            </select>
          </div>
        </section>

        {/* Location */}
        <section className="form-section">
          <h3>Location</h3>
          
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="remote_allowed"
                checked={formData.remote_allowed}
                onChange={handleChange}
              />
              <span>Remote Work Allowed</span>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="location">Location Description *</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              placeholder="e.g., San Francisco, CA or Remote"
            />
          </div>

          <div className="form-group">
            <label htmlFor="city">City *</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleChange}
              required
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
            <label htmlFor="country">Country *</label>
            <input
              type="text"
              id="country"
              name="country"
              value={formData.country}
              onChange={handleChange}
              required
            />
          </div>
        </section>

        {/* Application Settings */}
        <section className="form-section">
          <h3>Application Settings</h3>
          
          <div className="form-group">
            <label htmlFor="application_deadline">Application Deadline</label>
            <input
              type="date"
              id="application_deadline"
              name="application_deadline"
              value={formData.application_deadline}
              onChange={handleChange}
              min={new Date().toISOString().split('T')[0]}
            />
          </div>

          <div className="form-group">
            <label>Application Method *</label>
            <div className="radio-group">
              <label className="radio-option">
                <input
                  type="radio"
                  name="application_method"
                  value="platform"
                  checked={formData.application_method === 'platform'}
                  onChange={handleChange}
                />
                <span>
                  <strong>Apply on our platform</strong>
                  <small>Candidates apply through WHIT and you receive applications in your dashboard</small>
                </span>
              </label>
              <label className="radio-option">
                <input
                  type="radio"
                  name="application_method"
                  value="external"
                  checked={formData.application_method === 'external'}
                  onChange={handleChange}
                />
                <span>
                  <strong>Apply on company website</strong>
                  <small>Redirect candidates to your company's career page</small>
                </span>
              </label>
            </div>
          </div>

          {formData.application_method === 'external' && (
            <div className="form-group">
              <label htmlFor="application_url">Application URL *</label>
              <input
                type="url"
                id="application_url"
                name="application_url"
                value={formData.application_url}
                onChange={handleChange}
                required={formData.application_method === 'external'}
                placeholder="https://yourcompany.com/careers/apply"
              />
            </div>
          )}

          {formData.application_method === 'platform' && (
            <div className="form-group">
              <label htmlFor="application_email">Application Email</label>
              <input
                type="email"
                id="application_email"
                name="application_email"
                value={formData.application_email}
                onChange={handleChange}
                placeholder={profile?.contact_email || "Email for application notifications"}
              />
              <small className="field-hint">
                Leave blank to use your profile email: {profile?.contact_email}
              </small>
            </div>
          )}
        </section>

        {/* Form Actions */}
        <div className="form-actions">
          <button 
            type="button" 
            onClick={() => navigate('/recruiter/dashboard/jobs')} 
            className="btn-secondary"
          >
            Cancel
          </button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Saving...' : (isEditMode ? 'Update Job' : 'Create Job')}
          </button>
        </div>
      </form>
    </div>
  );
}

export default JobOpeningForm;
