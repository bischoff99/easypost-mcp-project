import axios from 'axios';
import { toast } from 'sonner';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Error interceptor with toast notifications
api.interceptors.response.use(
  response => response,
  error => {
    const message = error.response?.data?.message || error.message || 'An error occurred';
    
    // Show toast notification for errors
    if (error.response?.status >= 500) {
      toast.error('Server Error', { description: message });
    } else if (error.response?.status >= 400) {
      toast.error('Request Failed', { description: message });
    } else if (error.code === 'ECONNABORTED') {
      toast.error('Request Timeout', { description: 'The request took too long to complete' });
    } else if (error.code === 'ERR_NETWORK') {
      toast.error('Network Error', { description: 'Unable to connect to server' });
    }
    
    // Log to console in dev mode
    if (import.meta.env.DEV) {
      console.warn('API Error:', error.response?.data || error.message);
    }
    
    return Promise.reject(error);
  }
);

export const shipmentAPI = {
  createShipment: async data => {
    try {
      const response = await api.post('/shipments', data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create shipment');
    }
  },

  getTracking: async trackingNumber => {
    try {
      const response = await api.get(`/tracking/${trackingNumber}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get tracking');
    }
  },

  getRates: async data => {
    try {
      const response = await api.post('/rates', data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get rates');
    }
  },

  getRecentShipments: async (limit = 10) => {
    try {
      const response = await api.get(`/shipments?page_size=${limit}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get recent shipments');
    }
  },

  getStats: async () => {
    try {
      const response = await api.get('/analytics');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get statistics');
    }
  },

  getShipment: async shipmentId => {
    try {
      const response = await api.get(`/shipments/${shipmentId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get shipment details');
    }
  },

  healthCheck: async () => {
    try {
      const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${baseURL}/health`, { timeout: 5000 });
      return response.data;
    } catch {
      throw new Error('Backend server is not running');
    }
  },
};

export default api;
