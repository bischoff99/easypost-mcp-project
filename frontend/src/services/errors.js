import { toast } from 'sonner';

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

  console.error(`✗ API Error:`, error.config?.url, status, message);

  if (status >= 500) {
    toast.error('Server Error', { description: message });
  } else if (status >= 400) {
    toast.error('Request Failed', { description: message });
  } else if (error.code === 'ECONNABORTED') {
    toast.error('Request Timeout', { description: 'The request took too long to complete' });
  } else if (error.code === 'ERR_NETWORK') {
    toast.error('Network Error', { description: 'Unable to connect to server' });
  }

  if (import.meta.env.DEV) {
    console.warn('API Error:', error.response?.data || error.message);
  }

  return new ApiError(message, status, error.response?.data);
}
