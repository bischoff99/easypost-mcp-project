import { toast } from 'sonner';
import { logger } from '@/lib/logger';

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

export function handleApiError(error) {
  const message = error.response?.data?.message || error.message || 'An error occurred';
  const status = error.response?.status;
  const url = error.config?.url || 'unknown endpoint';

  logger.error(`API Error: ${url}`, { status, message, code: error.code });

  // Handle connection errors (backend not running)
  if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED') {
    logger.warn('Backend server is unreachable. Make sure it is running on http://localhost:8000');
    // Only toast once per session to avoid spam
    if (!window.__apiOfflineToasted) {
      toast.error('Backend Offline', {
        description: 'Unable to connect to the API server. Please ensure the backend is running.',
      });
      window.__apiOfflineToasted = true;
    }
  } else if (error.code === 'ECONNABORTED' || status === 408) {
    toast.error('Request Timeout', { description: 'The request took too long to complete' });
  } else if (status >= 500) {
    toast.error('Server Error', { description: message });
  } else if (status >= 400) {
    toast.error('Request Failed', { description: message });
  }

  if (import.meta.env.DEV) {
    logger.warn('API Error details:', error.response?.data || error.message);
  }

  return new ApiError(message, status, error.response?.data);
}
