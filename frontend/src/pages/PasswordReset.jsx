import React, { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import FormPageLayout from '../components/FormPageLayout';
import '../components/Auth.css';

const PasswordReset = () => {
  const { uid, token } = useParams();
  const [formData, setFormData] = useState({ password: '', password2: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
    setError('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/accounts/password-reset/confirm/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid, token, ...formData }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
      } else {
        setError(data.error || data.password?.[0] || data.password2?.[0] || 'Unable to reset password.');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormPageLayout pageName="login">
      <div className="auth-card">
        <h2>Choose New Password</h2>
        {message && <div className="success-message">{message}</div>}
        {error && <div className="error-message">{error}</div>}
        {!message && (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="password">New Password</label>
              <input id="password" name="password" type="password" value={formData.password} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label htmlFor="password2">Confirm New Password</label>
              <input id="password2" name="password2" type="password" value={formData.password2} onChange={handleChange} required />
            </div>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        )}
        <p className="auth-footer"><Link to="/login">Back to login</Link></p>
      </div>
    </FormPageLayout>
  );
};

export default PasswordReset;
