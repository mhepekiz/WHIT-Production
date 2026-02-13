import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useRecruiterAuth } from '../contexts/RecruiterAuthContext';
import { getPackages } from '../services/recruiterApi';
import FormPageLayout from '../components/FormPageLayout';
import '../components/Auth.css';
import './RecruiterRegister.css';

function RecruiterRegister() {
  const navigate = useNavigate();
  const { register, isAuthenticated, error: authError } = useRecruiterAuth();
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1); // 1: Package Selection, 2: Company Info, 3: Personal Info
  
  const [formData, setFormData] = useState({
    // Personal Info
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    password2: '',
    
    // Company Info
    company_name: '',
    company_website: '',
    company_description: '',
    contact_email: '',
    phone_number: '',
    
    // Address
    address: '',
    city: '',
    state: '',
    country: '',
    postal_code: '',
    
    // Package
    package_id: null
  });

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/recruiter/dashboard');
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    fetchPackages();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchPackages = async () => {
    try {
      const data = await getPackages();
      console.log('Packages API response:', data);
      setPackages(data.results || data);
    } catch (err) {
      console.error('Failed to fetch packages:', err);
      setError('Failed to load packages. Please try again.');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const selectPackage = (packageId) => {
    setFormData(prev => ({
      ...prev,
      package_id: packageId
    }));
    setStep(2);
  };

  const validateCompanyEmail = (email) => {
    if (!email) return true; // Allow empty for optional fields
    
    const genericDomains = [
      'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
      'aol.com', 'icloud.com', 'mail.com', 'protonmail.com',
      'zoho.com', 'yandex.com', 'gmx.com', 'inbox.com',
      'live.com', 'msn.com', 'me.com', 'mac.com'
    ];
    
    const genericPatterns = [
      /.*gmail\..*/i,
      /.*yahoo\..*/i,
      /.*hotmail\..*/i,
      /.*outlook\..*/i,
      /.*aol\..*/i,
      /.*icloud\..*/i,
      /.*mail\.com.*/i,
      /.*proton.*mail\..*/i,
      /.*live\..*/i,
      /.*msn\..*/i
    ];
    
    const domain = email.split('@')[1]?.toLowerCase();
    if (!domain) return false;
    
    // Check exact matches
    if (genericDomains.includes(domain)) {
      return false;
    }
    
    // Check patterns
    for (const pattern of genericPatterns) {
      if (pattern.test(domain)) {
        return false;
      }
    }
    
    return true;
  };

  const handleStep2Submit = (e) => {
    e.preventDefault();
    setError('');
    
    // Validate contact email
    if (formData.contact_email && !validateCompanyEmail(formData.contact_email)) {
      setError('Please use a company email address for contact information. Generic email providers (Gmail, Yahoo, etc.) are not allowed.');
      return;
    }
    
    setStep(3);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted with data:', formData);
    setError('');
    setLoading(true);

    // Validation
    if (formData.password !== formData.password2) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (!formData.package_id) {
      setError('Please select a package');
      setLoading(false);
      return;
    }

    // Validate email addresses
    if (!validateCompanyEmail(formData.email)) {
      setError('Please use a company email address. Generic email providers (Gmail, Yahoo, etc.) are not allowed for recruiter registration.');
      setLoading(false);
      return;
    }

    if (formData.contact_email && !validateCompanyEmail(formData.contact_email)) {
      setError('Please use a company email address for contact information. Generic email providers (Gmail, Yahoo, etc.) are not allowed.');
      setLoading(false);
      return;
    }

    try {
      await register(formData);
      navigate('/recruiter/dashboard');
    } catch (err) {
      console.error('Registration error:', err);
      console.error('Error response:', err.response?.data);
      
      // Handle field-specific errors
      if (err.response?.data) {
        const errorData = err.response.data;
        if (typeof errorData === 'object' && !errorData.error && !errorData.message) {
          // Format field errors - extract just the messages
          const errorMessages = Object.entries(errorData)
            .map(([field, messages]) => {
              const msgArray = Array.isArray(messages) ? messages : [messages];
              // Extract string from error objects or use as-is if string
              const messageStrings = msgArray.map(msg => {
                if (typeof msg === 'string') return msg;
                if (typeof msg === 'object' && msg !== null) {
                  return msg.string || msg.message || JSON.stringify(msg);
                }
                return String(msg);
              });
              return messageStrings.join(', ');
            })
            .filter(msg => msg) // Remove empty messages
            .join(' ');
          setError(errorMessages || 'Registration failed. Please check your information.');
        } else {
          // Handle simple error messages
          const errorMsg = errorData.error || errorData.message || 
                          (typeof errorData === 'string' ? errorData : 'Registration failed. Please try again.');
          setError(errorMsg);
        }
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormPageLayout pageName="recruiter_register">
    <div className="auth-card recruiter-register-card">
        <h2>Recruiter Registration</h2>
        <p className="subtitle">Join WHIT to find the best tech talent</p>

        {/* Progress Steps */}
        <div className="progress-steps">
          <div className={`step ${step >= 1 ? 'active' : ''}`}>
            <span className="step-number">1</span>
            <span className="step-label">Package</span>
          </div>
          <div className={`step ${step >= 2 ? 'active' : ''}`}>
            <span className="step-number">2</span>
            <span className="step-label">Company</span>
          </div>
          <div className={`step ${step >= 3 ? 'active' : ''}`}>
            <span className="step-number">3</span>
            <span className="step-label">Personal</span>
          </div>
        </div>

        {error && <div className="error-message" style={{ whiteSpace: 'pre-wrap' }}>{error}</div>}
        {authError && typeof authError === 'string' && (
          <div className="error-message" style={{ whiteSpace: 'pre-wrap' }}>{authError}</div>
        )}

        {/* Step 1: Package Selection */}
        {step === 1 && (
          <div className="packages-grid">
            {packages.map(pkg => (
              <div key={pkg.id} className="package-card" onClick={() => selectPackage(pkg.id)}>
                <h3>{pkg.name}</h3>
                <div className="package-price">${pkg.price}/month</div>
                <p className="package-description">{pkg.description}</p>
                <ul className="package-features">
                  <li>
                    {pkg.monthly_job_openings === 0 ? 'Unlimited' : pkg.monthly_job_openings} job openings/month
                  </li>
                  <li>
                    {pkg.monthly_candidate_searches === 0 ? 'Unlimited' : pkg.monthly_candidate_searches} candidate searches/month
                  </li>
                  <li>{pkg.analytics_level} analytics</li>
                  {pkg.messaging_enabled && (
                    <li>
                      {pkg.monthly_messages === 0 ? 'Unlimited' : pkg.monthly_messages} messages/month
                    </li>
                  )}
                  {pkg.featured_job_posts > 0 && (
                    <li>{pkg.featured_job_posts} featured job posts</li>
                  )}
                  {pkg.priority_support && <li>Priority support</li>}
                  {pkg.can_export_data && <li>Data export</li>}
                </ul>
                <button className="select-package-btn">Select Package</button>
              </div>
            ))}
          </div>
        )}

        {/* Step 2: Company Information */}
        {step === 2 && (
          <form onSubmit={handleStep2Submit}>
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
                placeholder="Tell us about your company..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="contact_email">Contact Email (Company Email) *</label>
                <input
                  type="email"
                  id="contact_email"
                  name="contact_email"
                  value={formData.contact_email}
                  onChange={handleChange}
                  required
                />
                <small className="form-hint">Must be a company email address</small>
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
            </div>

            <div className="form-group">
              <label htmlFor="address">Address</label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
              />
            </div>

            <div className="form-row">
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
            </div>

            <div className="form-row">
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

            <div className="form-actions">
              <button type="button" className="btn-secondary" onClick={() => setStep(1)}>
                Back
              </button>
              <button type="submit" className="btn-primary">
                Continue
              </button>
            </div>
          </form>
        )}

        {/* Step 3: Personal Information */}
        {step === 3 && (
          <form onSubmit={handleSubmit}>
            <h3>Personal Information</h3>
            
            <div className="form-row">
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
            </div>

            <div className="form-group">
              <label htmlFor="email">Email Address (Company Email) *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <small className="form-hint">Please use your company email address. Generic providers (Gmail, Yahoo, etc.) are not allowed.</small>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password *</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                minLength="8"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password2">Confirm Password *</label>
              <input
                type="password"
                id="password2"
                name="password2"
                value={formData.password2}
                onChange={handleChange}
                required
                minLength="8"
              />
            </div>

            <div className="form-actions">
              <button type="button" className="btn-secondary" onClick={() => setStep(2)}>
                Back
              </button>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Registering...' : 'Complete Registration'}
              </button>
            </div>
          </form>
        )}

        <div className="auth-footer">
          <p>Already have a recruiter account? <Link to="/recruiter/login">Login here</Link></p>
          <p>Looking for a job? <Link to="/register">Register as a candidate</Link></p>
        </div>
      </div>
    </FormPageLayout>
  );
}

export default RecruiterRegister;
