import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import FormPageLayout from './FormPageLayout';
import './Auth.css';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error for this field
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: null,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    console.log('Submitting registration with data:', formData);
    const result = await register(formData);
    console.log('Registration result:', result);

    if (result.success) {
      navigate('/dashboard');
    } else {
      console.error('Registration errors:', result.error);
      setErrors(result.error);
    }
    setLoading(false);
  };

  return (
    <FormPageLayout pageName="register">
      <div className="auth-card">
        <h2>Create Account</h2>
        <p className="auth-subtitle">Join Who Is Hiring In Tech</p>

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">First Name</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
              />
              {errors.first_name && (
                <span className="error-text">{errors.first_name[0]}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="last_name">Last Name</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
              />
              {errors.last_name && (
                <span className="error-text">{errors.last_name[0]}</span>
              )}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
            {errors.username && (
              <span className="error-text">{errors.username[0]}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            {errors.email && (
              <span className="error-text">{errors.email[0]}</span>
            )}
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
            />
            <small style={{ color: '#666', fontSize: '0.85em' }}>
              Password must be at least 8 characters and not entirely numeric
            </small>
            {errors.password && (
              <div className="error-text">
                {Array.isArray(errors.password) 
                  ? errors.password.map((err, idx) => <div key={idx}>{err}</div>)
                  : errors.password
                }
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="password2">Confirm Password</label>
            <input
              type="password"
              id="password2"
              name="password2"
              value={formData.password2}
              onChange={handleChange}
              required
            />
            {errors.password2 && (
              <span className="error-text">
                {Array.isArray(errors.password2) ? errors.password2[0] : errors.password2}
              </span>
            )}
          </div>

          {errors.detail && (
            <div className="error-message">{errors.detail}</div>
          )}
          
          {errors.non_field_errors && (
            <div className="error-message">
              {Array.isArray(errors.non_field_errors) 
                ? errors.non_field_errors[0] 
                : errors.non_field_errors
              }
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </FormPageLayout>
  );
};

export default Register;
