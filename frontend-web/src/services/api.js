import axios from 'axios';

const API_BASE_URL = 'https://chemical-equipment-backend-bjfj.onrender.com/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  getCurrentUser: () => api.get('/auth/user/'),
};

// Dataset APIs
export const datasetAPI = {
  upload: (formData) => {
    return api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  list: () => api.get('/datasets/'),
  get: (id) => api.get(`/datasets/${id}/`),
  delete: (id) => api.delete(`/datasets/${id}/delete/`),
  generateReport: (id) => {
    return api.get(`/datasets/${id}/report/`, {
      responseType: 'blob',
    });
  },
};

// Statistics API
export const statisticsAPI = {
  get: () => api.get('/statistics/'),
};

export default api;
