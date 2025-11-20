import React, { createContext, useState, useContext, useEffect } from 'react';
import {
  isRecruiterAuthenticated,
  getRecruiterUser,
  loginRecruiter as apiLoginRecruiter,
  registerRecruiter as apiRegisterRecruiter,
  logoutRecruiter as apiLogoutRecruiter
} from '../services/recruiterApi';

const RecruiterAuthContext = createContext();

export const useRecruiterAuth = () => {
  const context = useContext(RecruiterAuthContext);
  if (!context) {
    throw new Error('useRecruiterAuth must be used within RecruiterAuthProvider');
  }
  return context;
};

export const RecruiterAuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(isRecruiterAuthenticated());
  const [recruiterUser, setRecruiterUser] = useState(getRecruiterUser());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check authentication status on mount
    setIsAuthenticated(isRecruiterAuthenticated());
    setRecruiterUser(getRecruiterUser());
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiLoginRecruiter(email, password);
      setIsAuthenticated(true);
      setRecruiterUser(data.user);
      return data;
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const register = async (registrationData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiRegisterRecruiter(registrationData);
      setIsAuthenticated(true);
      setRecruiterUser(data.user);
      return data;
    } catch (err) {
      const errorMessage = err.response?.data || 'Registration failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    apiLogoutRecruiter();
    setIsAuthenticated(false);
    setRecruiterUser(null);
    setError(null);
  };

  const value = {
    isAuthenticated,
    recruiterUser,
    loading,
    error,
    login,
    register,
    logout
  };

  return (
    <RecruiterAuthContext.Provider value={value}>
      {children}
    </RecruiterAuthContext.Provider>
  );
};

export default RecruiterAuthContext;
