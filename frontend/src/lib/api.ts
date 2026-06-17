import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Auto-attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        try {
          const { data } = await axios.post(`${BASE_URL}/auth/refresh`, { refresh_token: refresh });
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('refresh_token', data.refresh_token);
          error.config.headers.Authorization = `Bearer ${data.access_token}`;
          return api(error.config);
        } catch {
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth
export const authApi = {
  register: (data: any) => api.post('/auth/register', data).then(r => r.data),
  login: (data: any) => api.post('/auth/login', data).then(r => r.data),
  me: () => api.get('/auth/me').then(r => r.data),
  updateMe: (data: any) => api.patch('/auth/me', data).then(r => r.data),
  listApiKeys: () => api.get('/auth/me/api-keys').then(r => r.data),
  createApiKey: (data: any) => api.post('/auth/me/api-keys', data).then(r => r.data),
  revokeApiKey: (id: string) => api.delete(`/auth/me/api-keys/${id}`),
};

// Models
export const modelsApi = {
  list: (params?: any) => api.get('/models', { params }).then(r => r.data),
  listMy: () => api.get('/models/my').then(r => r.data),
  get: (id: string) => api.get(`/models/${id}`).then(r => r.data),
  create: (data: any) => api.post('/models', data).then(r => r.data),
  update: (id: string, data: any) => api.patch(`/models/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/models/${id}`),
  createVersion: (id: string, data: any) => api.post(`/models/${id}/versions`, data).then(r => r.data),
  uploadFile: (modelId: string, versionId: string, file: File) => {
    const form = new FormData();
    form.append('file', file);
    return api.post(`/models/${modelId}/versions/${versionId}/upload`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(r => r.data);
  },
  predict: (id: string, payload: any) => api.post(`/inference/${id}/predict`, payload).then(r => r.data),
};

// Datasets
export const datasetsApi = {
  list: (params?: any) => api.get('/datasets', { params }).then(r => r.data),
  listMy: () => api.get('/datasets/my').then(r => r.data),
  get: (id: string) => api.get(`/datasets/${id}`).then(r => r.data),
  create: (data: any) => api.post('/datasets', data).then(r => r.data),
  delete: (id: string) => api.delete(`/datasets/${id}`),
  upload: (id: string, file: File) => {
    const form = new FormData();
    form.append('file', file);
    return api.post(`/datasets/${id}/upload`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(r => r.data);
  },
};

// Training
export const trainingApi = {
  list: (params?: any) => api.get('/training', { params }).then(r => r.data),
  get: (id: string) => api.get(`/training/${id}`).then(r => r.data),
  create: (data: any) => api.post('/training', data).then(r => r.data),
  cancel: (id: string) => api.post(`/training/${id}/cancel`).then(r => r.data),
  logs: (id: string) => api.get(`/training/${id}/logs`).then(r => r.data),
};
