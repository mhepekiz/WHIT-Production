import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import FormPageLayout from '../components/FormPageLayout';
import '../components/Auth.css';

const VerifyEmail = () => {
  const { uid, token } = useParams();
  const [message, setMessage] = useState('Verifying your email...');
  const [error, setError] = useState('');

  useEffect(() => {
    const verify = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/accounts/verify-email/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ uid, token }),
        });
        const data = await response.json();
        if (response.ok) {
          setMessage(data.message || 'Email verified successfully. You can now log in.');
        } else {
          setError(data.error || 'This verification link is invalid or expired.');
        }
      } catch (err) {
        setError('Network error. Please try again.');
      }
    };

    verify();
  }, [uid, token]);

  return (
    <FormPageLayout pageName="login">
      <div className="auth-card">
        <h2>Email Verification</h2>
        {error ? <div className="error-message">{error}</div> : <div className="success-message">{message}</div>}
        <p className="auth-footer">
          <Link to="/login">Login as Job Seeker</Link>
          {' '}or{' '}
          <Link to="/recruiter/login">Login as Recruiter</Link>
        </p>
      </div>
    </FormPageLayout>
  );
};

export default VerifyEmail;
