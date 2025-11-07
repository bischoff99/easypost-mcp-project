import axios from 'axios';
import axiosRetry from 'axios-retry';
import { handleApiError, ApiError } from './errors';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Retry failed requests
axiosRetry(api, {
  retries: 3,
  retryDelay: (retryCount) => {
    return retryCount * 1000;
  },
  retryCondition: (error) => {
    return error.code === 'ERR_NETWORK' || error.response?.status >= 500;
  },
});

// Error interceptor with toast notifications
api.interceptors.response.use(
  (response) => {
    console.log(`✓ API ${response.config.method.toUpperCase()} ${response.config.url}: ${response.status}`);
    return response;
  },
  (error) => {
    const apiError = handleApiError(error);
    return Promise.reject(apiError);
  }
);

export const shipmentAPI = {
  createShipment: async (data) => {
    try {
      const response = await api.post('/shipments', data);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getTracking: async (trackingNumber) => {
    try {
      const response = await api.get(`/tracking/${trackingNumber}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getRates: async (data) => {
    try {
      const response = await api.post('/rates', data);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getRecentShipments: async (limit = 10) => {
    try {
      const response = await api.get(`/shipments?page_size=${limit}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getAnalytics: async () => {
    try {
      const response = await api.get('/analytics');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getStats: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getCarrierPerformance: async () => {
    try {
      const response = await api.get('/carrier-performance');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getShipment: async (shipmentId) => {
    try {
      const response = await api.get(`/shipments/${shipmentId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  buyShipment: async (data) => {
    try {
      const response = await api.post('/shipments/buy', data);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  healthCheck: async () => {
    try {
      const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${baseURL}/health`, { timeout: 5000 });
      return response.data;
    } catch (error) {
      throw new ApiError('Backend server is not running', 503, null);
    }
  },

  // Bulk Operations
  createBulkShipments: async (shipments, onProgress) => {
    try {
      const response = await api.post('/bulk-shipments', { shipments });

      // Simulate progress updates (in production, use WebSocket or SSE)
      if (onProgress) {
        const total = shipments.length;
        let current = 0;
        const interval = setInterval(() => {
          current += Math.min(10, total - current);
          onProgress(Math.round((current / total) * 100));
          if (current >= total) {
            clearInterval(interval);
          }
        }, 500);
      }

      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default api;
