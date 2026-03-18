// src/services/api.js
// Centralised Axios instance — reads token from localStorage automatically

import axios from 'axios';

// In dev, Vite proxies /auth, /upload etc. to Flask — so base is ''.
// In production, set VITE_API_URL=https://your-backend.render.com
const BASE_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({ baseURL: BASE_URL });

// ── Request interceptor: attach JWT ──────────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Response interceptor: auto-logout on 401 ────────────────────────
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;
