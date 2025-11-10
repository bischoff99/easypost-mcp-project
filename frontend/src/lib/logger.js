/* eslint-disable no-console */
/**
 * Logger utility for frontend application
 *
 * Provides structured logging with environment-aware levels.
 * In production, only errors are logged. In development, all logs are shown.
 */

const isDevelopment = import.meta.env.DEV;

class Logger {
  log(...args) {
    if (isDevelopment) {
      console.log('[LOG]', ...args);
    }
  }

  info(...args) {
    if (isDevelopment) {
      console.info('[INFO]', ...args);
    }
  }

  warn(...args) {
    if (isDevelopment) {
      console.warn('[WARN]', ...args);
    }
  }

  error(...args) {
    // Always log errors, even in production
    console.error('[ERROR]', ...args);
  }

  debug(...args) {
    if (isDevelopment) {
      console.debug('[DEBUG]', ...args);
    }
  }

  api(method, url, status) {
    if (isDevelopment) {
      console.log(`✓ API ${method.toUpperCase()} ${url}: ${status}`);
    }
  }
}

export const logger = new Logger();
export default logger;
