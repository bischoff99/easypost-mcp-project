import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Error interceptor
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
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
      const response = await api.get(`/shipments/recent?limit=${limit}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get recent shipments');
    }
  },

  getStats: async () => {
    try {
      const response = await api.get('/stats/overview');
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
    } catch (error) {
      throw new Error('Backend server is not running');
    }
  },
};

export default api;
