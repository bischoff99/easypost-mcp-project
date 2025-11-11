/**
 * API endpoint constants for centralized management.
 *
 * Industry Best Practice: Define all endpoints in one place
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ENDPOINTS = {
  // Core
  ROOT: '/',
  HEALTH: '/health',
  METRICS: '/metrics',

  // Shipments
  RATES: '/rates',
  SHIPMENTS: '/shipments',
  SHIPMENTS_BUY: '/shipments/buy',
  SHIPMENTS_REFUND: (id) => `/shipments/${id}/refund`,

  // Tracking
  TRACKING: (number) => `/tracking/${number}`,

  // Analytics
  ANALYTICS: '/analytics',
  STATS: '/stats',
  CARRIER_PERFORMANCE: '/carrier-performance',

  // Database
  DB_SHIPMENTS: '/db/shipments',
  DB_SHIPMENT_BY_ID: (id) => `/db/shipments/${id}`,
  DB_ADDRESSES: '/db/addresses',
  DB_ANALYTICS: '/db/analytics/dashboard',
  DB_BATCH_OPERATIONS: '/db/batch-operations',
  DB_USER_ACTIVITY: '/db/user-activity',

  // Webhooks
  WEBHOOKS_EASYPOST: '/webhooks/easypost',
};

export const buildUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

export default ENDPOINTS;
