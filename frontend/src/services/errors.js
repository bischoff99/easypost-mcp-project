/**
 * Centralized error handling for API requests.
 *
 * Industry Best Practice: Consistent error messages and logging
 */

export class APIError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Extract error message from various error formats.
 */
export const getErrorMessage = (error) => {
  // Axios error
  if (error.response) {
    const data = error.response.data;

    // FastAPI error format
    if (data.detail) {
      return typeof data.detail === 'string'
        ? data.detail
        : JSON.stringify(data.detail);
    }

    // Custom API error format
    if (data.message) {
      return data.message;
    }

    return `Request failed with status ${error.response.status}`;
  }

  // Network error
  if (error.request) {
    return 'Network error - server may be down';
  }

  // Other errors
  return error.message || 'An unexpected error occurred';
};

/**
 * Handle API errors consistently across the application.
 */
export const handleAPIError = (error, context = '') => {
  const message = getErrorMessage(error);
  console.error(`API Error ${context}:`, message, error);

  // Return user-friendly error
  return {
    success: false,
    message: message,
    error: error,
  };
};

/**
 * Log error for debugging (can be extended to send to monitoring service).
 */
export const logError = (error, context = {}) => {
  console.error('Error:', {
    message: error.message,
    stack: error.stack,
    ...context,
  });

  // TODO: Send to monitoring service (e.g., Sentry, LogRocket)
  // if (window.Sentry) {
  //   window.Sentry.captureException(error, { contexts: { custom: context } });
  // }
};

