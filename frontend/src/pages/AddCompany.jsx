import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './AddCompany.css';

function AddCompany() {
  const { isAuthenticated, token } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    jobs_page_url: '',
    company_reviews: '',
    country: '',
    state: '',
    city: '',
    work_environment: 'Remote',
    functions_text: '',
    engineering_positions: true,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/companies/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSubmitStatus({ type: 'success', message: 'Company submitted successfully! It will be reviewed before going live.' });
        setFormData({
          name: '',
          jobs_page_url: '',
          company_reviews: '',
          country: '',
          state: '',
          city: '',
          work_environment: 'Remote',
          functions_text: '',
          engineering_positions: true,
        });
      } else {
        const errorData = await response.json();
        setSubmitStatus({ type: 'error', message: errorData.message || 'Failed to submit company. Please try again.' });
      }
    } catch (error) {
      setSubmitStatus({ type: 'error', message: 'Network error. Please check your connection and try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="add-company-page">
      <div className="add-company-container">
        <div className="page-header">
          <h1>Add Your Company</h1>
          <p>Share your company with talented job seekers in tech.</p>
        </div>

        {submitStatus && (
          <div className={`status-message ${submitStatus.type}`}>
            {submitStatus.message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="add-company-form">
          <div className="form-section">
            <h2>Company Information</h2>
            
            <div className="form-group">
              <label htmlFor="name">Company Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                placeholder="Enter your company name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="jobs_page_url">Jobs/Careers Page URL *</label>
              <input
                type="url"
                id="jobs_page_url"
                name="jobs_page_url"
                value={formData.jobs_page_url}
                onChange={handleInputChange}
                required
                placeholder="https://yourcompany.com/careers"
              />
              <small>Link to where people can view and apply for jobs</small>
            </div>

            <div className="form-group">
              <label htmlFor="company_reviews">Company Reviews URL (Optional)</label>
              <input
                type="url"
                id="company_reviews"
                name="company_reviews"
                value={formData.company_reviews}
                onChange={handleInputChange}
                placeholder="https://glassdoor.com/Overview/..."
              />
              <small>Link to Glassdoor, Indeed, or other review site</small>
            </div>
          </div>

          <div className="form-section">
            <h2>Location</h2>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="country">Country *</label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleInputChange}
                  required
                  placeholder="USA, Canada, UK, etc."
                />
              </div>

              <div className="form-group">
                <label htmlFor="state">State/Province</label>
                <input
                  type="text"
                  id="state"
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  placeholder="California, Ontario, etc."
                />
              </div>

              <div className="form-group">
                <label htmlFor="city">City</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleInputChange}
                  placeholder="San Francisco, Toronto, etc."
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h2>Work Details</h2>
            
            <div className="form-group">
              <label htmlFor="work_environment">Work Environment *</label>
              <select
                id="work_environment"
                name="work_environment"
                value={formData.work_environment}
                onChange={handleInputChange}
                required
              >
                <option value="Remote">Remote</option>
                <option value="On-Site">On-Site</option>
                <option value="Hybrid">Hybrid</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="functions_text">Company Functions/Industry</label>
              <input
                type="text"
                id="functions_text"
                name="functions_text"
                value={formData.functions_text}
                onChange={handleInputChange}
                placeholder="e.g. Software Development, AI/ML, Fintech, Healthcare"
              />
              <small>Describe what your company does or what industry you're in</small>
            </div>

            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="engineering_positions"
                  checked={formData.engineering_positions}
                  onChange={handleInputChange}
                />
                <span className="checkmark"></span>
                We have engineering/technical positions available
              </label>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" disabled={isSubmitting} className="btn btn-primary">
              {isSubmitting ? 'Submitting...' : 'Submit Company'}
            </button>
            <button type="button" onClick={() => navigate('/')} className="btn btn-secondary">
              Cancel
            </button>
          </div>
        </form>

        <div className="form-footer">
          <p><small>* Required fields</small></p>
          <p><small>
            By submitting your company, you agree that the information provided is accurate. 
            All submissions are reviewed before being published.
          </small></p>
        </div>
      </div>
    </div>
  );
}

export default AddCompany;