import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://staging.whoishiringintech.com/api';
const API_URL = `${API_BASE_URL.replace('/api', '')}/api/recruiters`;

// Create axios instance with auth header
const getAuthHeader = () => {
  const token = localStorage.getItem('recruiterToken');
  return token ? { Authorization: `Token ${token}` } : {};
};

// Package APIs
export const getPackages = async () => {
  const response = await axios.get(`${API_URL}/packages/`);
  return response.data;
};

// Authentication APIs
export const registerRecruiter = async (data) => {
  const response = await axios.post(`${API_URL}/register/`, data);
  if (response.data.token) {
    localStorage.setItem('recruiterToken', response.data.token);
    localStorage.setItem('recruiterUser', JSON.stringify(response.data.user));
  }
  return response.data;
};

export const loginRecruiter = async (email, password) => {
  console.log('DEBUG: API_URL:', API_URL);
  console.log('DEBUG: Full login URL:', `${API_URL}/login/`);
  console.log('DEBUG: Login request data:', { email, password });
  
  try {
    const response = await axios.post(`${API_URL}/login/`, 
      { email, password },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    console.log('DEBUG: Login response status:', response.status);
    console.log('DEBUG: Login response data:', response.data);
    
    if (response.data.token) {
      localStorage.setItem('recruiterToken', response.data.token);
      localStorage.setItem('recruiterUser', JSON.stringify(response.data.user));
    }
    return response.data;
  } catch (error) {
    console.error('DEBUG: Login request failed:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers,
      url: error.config?.url,
      method: error.config?.method
    });
    throw error;
  }
};

export const logoutRecruiter = () => {
  localStorage.removeItem('recruiterToken');
  localStorage.removeItem('recruiterUser');
};

export const isRecruiterAuthenticated = () => {
  return !!localStorage.getItem('recruiterToken');
};

export const getRecruiterUser = () => {
  const user = localStorage.getItem('recruiterUser');
  return user ? JSON.parse(user) : null;
};

// Profile APIs
export const getRecruiterProfile = async () => {
  const response = await axios.get(`${API_URL}/profile/me/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const updateRecruiterProfile = async (id, data) => {
  const response = await axios.patch(`${API_URL}/profile/${id}/`, data, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const getRecruiterUsage = async () => {
  const response = await axios.get(`${API_URL}/profile/usage/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

// Job Opening APIs
export const getJobOpenings = async () => {
  const response = await axios.get(`${API_URL}/jobs/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const createJobOpening = async (data) => {
  const response = await axios.post(`${API_URL}/jobs/`, data, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const updateJobOpening = async (id, data) => {
  const response = await axios.patch(`${API_URL}/jobs/${id}/`, data, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const deleteJobOpening = async (id) => {
  await axios.delete(`${API_URL}/jobs/${id}/`, {
    headers: getAuthHeader()
  });
};

export const publishJobOpening = async (id) => {
  const response = await axios.post(`${API_URL}/jobs/${id}/publish/`, {}, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const getJobAnalytics = async () => {
  const response = await axios.get(`${API_URL}/jobs/analytics/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

// Job Application APIs
export const getJobApplications = async () => {
  const response = await axios.get(`${API_URL}/applications/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const updateApplicationStatus = async (id, status, notes = '', interviewDate = null) => {
  const requestData = { status, recruiter_notes: notes };
  if (interviewDate) {
    requestData.interview_date = interviewDate;
  }
  
  const response = await axios.patch(
    `${API_URL}/applications/${id}/update_status/`,
    requestData,
    { headers: getAuthHeader() }
  );
  return response.data;
};

// Candidate Search APIs
export const searchCandidates = async (searchParams) => {
  const response = await axios.post(
    `${API_URL}/candidates/search_candidates/`,
    searchParams,
    { headers: getAuthHeader() }
  );
  return response.data;
};

export const getCandidateSearches = async () => {
  const response = await axios.get(`${API_URL}/candidates/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const getSavedCandidates = async () => {
  const response = await axios.get(`${API_URL}/candidates/saved/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const saveCandidateSearch = async (id, data) => {
  const response = await axios.patch(`${API_URL}/candidates/${id}/`, data, {
    headers: getAuthHeader()
  });
  return response.data;
};

// Messaging APIs
export const getMessages = async () => {
  const response = await axios.get(`${API_URL}/messages/`, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const sendMessage = async (data) => {
  const response = await axios.post(`${API_URL}/messages/`, data, {
    headers: getAuthHeader()
  });
  return response.data;
};

export const markMessageRead = async (id) => {
  const response = await axios.post(`${API_URL}/messages/${id}/mark_read/`, {}, {
    headers: getAuthHeader()
  });
  return response.data;
};
