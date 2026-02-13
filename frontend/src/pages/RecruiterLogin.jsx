import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useRecruiterAuth } from '../contexts/RecruiterAuthContext';
import FormPageLayout from '../components/FormPageLayout';
import '../components/Auth.css';

function RecruiterLogin() {
  const navigate = useNavigate();
  const { login, isAuthenticated, error: authError, loading } = useRecruiterAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/recruiter/dashboard');
    }
  }, [isAuthenticated, navigate]);

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

    try {
      await login(formData.email, formData.password);
      navigate('/recruiter/dashboard');
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
    }
  };

  return (
    <FormPageLayout pageName="recruiter_login">
      <div className="auth-card">
        <h2>Recruiter Login</h2>
        <p className="auth-subtitle">Access your recruiter dashboard</p>

        {(error || authError) && (
          <div className="error-message">{error || authError}</div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="your@email.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="auth-footer">
          Don't have a recruiter account? <Link to="/recruiter/register">Register here</Link>
        </p>
        <p className="auth-footer" style={{ marginTop: '0.5rem' }}>
          Looking for a job? <Link to="/login">Login as a candidate</Link>
        </p>
      </div>
    </FormPageLayout>
  );
}

export default RecruiterLogin;
