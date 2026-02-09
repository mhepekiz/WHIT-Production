// Centralized API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://staging.whoishiringintech.com/api';
const BASE_URL = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('/api', '') : 'https://staging.whoishiringintech.com';

export const getApiUrl = (endpoint) => {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${API_BASE_URL}/${cleanEndpoint}`;
};

export const getBaseUrl = () => BASE_URL;
export const getMediaUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http')) return path;
  return `${BASE_URL}${path.startsWith('/') ? path : '/' + path}`;
};

export { API_BASE_URL };