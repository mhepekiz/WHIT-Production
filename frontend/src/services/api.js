import axios from 'axios';

// Force staging API URL to be correctly set during build
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const companyService = {
  // Get all companies with optional filters
  getCompanies: async (params = {}) => {
    const response = await apiClient.get('/companies/', { params });
    return response.data;
  },

  // Get a single company by ID
  getCompany: async (id) => {
    const response = await apiClient.get(`/companies/${id}/`);
    return response.data;
  },

  // Get filter options
  getFilters: async () => {
    const response = await apiClient.get('/companies/filters/');
    return response.data;
  },

  // Get statistics
  getStats: async () => {
    const response = await apiClient.get('/companies/stats/');
    return response.data;
  },

  // Create a new company (admin only)
  createCompany: async (data) => {
    const response = await apiClient.post('/companies/', data);
    return response.data;
  },

  // Update a company (admin only)
  updateCompany: async (id, data) => {
    const response = await apiClient.put(`/companies/${id}/`, data);
    return response.data;
  },

  // Delete a company (admin only)
  deleteCompany: async (id) => {
    await apiClient.delete(`/companies/${id}/`);
  },
};

export default apiClient;
