import axios from 'axios';
import { handleApiError, ApiError } from './errors';
import { logger } from '@/lib/logger';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Error interceptor with toast notifications
api.interceptors.response.use(
  (response) => {
    logger.api(response.config.method, response.config.url, response.status);
    return response;
  },
  (error) => {
    const apiError = handleApiError(error);
    return Promise.reject(apiError);
  }
);

export const shipmentAPI = {
  createShipment: async (data) => {
    const response = await api.post('/shipments', data);
    return response.data;
  },

  getTracking: async (trackingNumber) => {
    const response = await api.get(`/tracking/${trackingNumber}`);
    return response.data;
  },

  getRates: async (data) => {
    const response = await api.post('/rates', data);
    return response.data;
  },

  getRecentShipments: async (limit = 10) => {
    const response = await api.get('/shipments', { params: { page_size: limit } });
    return response.data;
  },

  getAnalytics: async () => {
    const response = await api.get('/analytics');
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/analytics');
    if (response.data.status === 'success' && response.data.data) {
      const { summary, by_carrier } = response.data.data;
      const totalShipments = summary?.total_shipments || 0;
      const totalCost = summary?.total_cost || 0;
      const deliveredCount = by_carrier?.reduce((sum, c) => sum + (c.shipment_count * c.success_rate / 100), 0) || 0;
      const deliveryRate = totalShipments > 0 ? deliveredCount / totalShipments : 0;

      return {
        status: 'success',
        data: {
          total_shipments: {
            label: 'Total Shipments',
            value: totalShipments,
            note: 'Last 100 from API',
          },
          in_transit: {
            label: 'In Transit',
            value: Math.max(0, totalShipments - Math.floor(deliveredCount)),
            note: 'Currently shipping',
          },
          total_cost: {
            label: 'Total Spent',
            value: totalCost,
            note: 'From shipment rates',
          },
          delivery_rate: {
            label: 'Delivery Rate',
            value: deliveryRate,
            note: 'Delivered / Total',
          },
        },
      };
    }
    throw new Error(response.data.message || 'Failed to fetch stats');
  },

  getCarrierPerformance: async () => {
    const response = await api.get('/analytics');
    if (response.data.status === 'success' && response.data.data) {
      const { by_carrier } = response.data.data;
      return {
        status: 'success',
        data: (by_carrier || []).map((carrier) => ({
          carrier: carrier.carrier,
          shipments: carrier.shipment_count,
          delivered: Math.floor(carrier.shipment_count * carrier.success_rate / 100),
          rate: carrier.success_rate,
        })),
      };
    }
    throw new Error(response.data.message || 'Failed to fetch carrier performance');
  },

  getShipment: async (shipmentId) => {
    const response = await api.get(`/shipments/${shipmentId}`);
    return response.data;
  },

  buyShipment: async (data) => {
    const response = await api.post('/shipments/buy', data);
    return response.data;
  },

  healthCheck: async () => {
    try {
      const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${baseURL}/health`, { timeout: 5000 });
      return response.data;
    } catch {
      throw new ApiError('Backend server is not running', 503, null);
    }
  },

  // Bulk Operations
  createBulkShipments: async (shipments, onProgress) => {
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
  },
};

export default api;
