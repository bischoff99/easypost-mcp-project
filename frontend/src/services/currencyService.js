import { logger } from '@/lib/logger';

/**
 * Currency Service
 *
 * Handles currency conversion using exchangerate-api.com
 * Implements caching with 1-hour TTL
 */

const CACHE_KEY = 'exchange_rates';
const CACHE_TTL = 60 * 60 * 1000; // 1 hour in milliseconds
const API_URL = import.meta.env.VITE_EXCHANGE_RATE_API_URL || 'https://api.exchangerate-api.com/v4/latest/USD';

/**
 * Get cached exchange rates
 */
const getCachedRates = () => {
  try {
    const cached = localStorage.getItem(CACHE_KEY);
    if (!cached) return null;

    const { rates, timestamp } = JSON.parse(cached);
    const now = Date.now();

    // Check if cache is still valid
    if (now - timestamp < CACHE_TTL) {
      return rates;
    }

    // Cache expired
    localStorage.removeItem(CACHE_KEY);
    return null;
  } catch (error) {
    logger.error('Failed to get cached rates:', error);
    return null;
  }
};

/**
 * Set cached exchange rates
 */
const setCachedRates = (rates) => {
  try {
    localStorage.setItem(
      CACHE_KEY,
      JSON.stringify({
        rates,
        timestamp: Date.now(),
      })
    );
  } catch (error) {
    logger.error('Failed to cache rates:', error);
  }
};

/**
 * Fetch exchange rates from API
 */
export const fetchExchangeRates = async () => {
  // Check cache first
  const cached = getCachedRates();
  if (cached) {
    logger.debug('Using cached exchange rates');
    return cached;
  }

  try {
    logger.debug('Fetching exchange rates from API');
    const response = await fetch(API_URL);

    if (!response.ok) {
      throw new Error(`Failed to fetch rates: ${response.statusText}`);
    }

    const data = await response.json();
    const rates = data.rates;

    // Cache the rates
    setCachedRates(rates);

    return rates;
  } catch (error) {
    logger.error('Failed to fetch exchange rates:', error);
    throw error;
  }
};

/**
 * Convert amount from USD to target currency
 */
export const convertCurrency = async (amount, targetCurrency) => {
  if (targetCurrency === 'USD') {
    return amount;
  }

  try {
    const rates = await fetchExchangeRates();
    const rate = rates[targetCurrency];

    if (!rate) {
      throw new Error(`Exchange rate not found for ${targetCurrency}`);
    }

    return amount * rate;
  } catch (error) {
    logger.error('Currency conversion failed:', error);
    throw error;
  }
};

/**
 * Get currency symbol for country code
 */
export const getCurrencySymbol = (currencyCode) => {
  const symbols = {
    USD: '$',
    EUR: '€',
    GBP: '£',
    JPY: '¥',
    CAD: 'CA$',
    AUD: 'A$',
    CHF: 'CHF',
    CNY: '¥',
    INR: '₹',
    SEK: 'kr',
    NOK: 'kr',
    DKK: 'kr',
    PLN: 'zł',
  };

  return symbols[currencyCode] || currencyCode;
};

/**
 * Get currency code from country code
 */
export const getCurrencyFromCountry = (countryCode) => {
  const currencyMap = {
    US: 'USD',
    GB: 'GBP',
    DE: 'EUR',
    FR: 'EUR',
    ES: 'EUR',
    IT: 'EUR',
    CA: 'CAD',
    AU: 'AUD',
    JP: 'JPY',
    CN: 'CNY',
    IN: 'INR',
    CH: 'CHF',
  };

  return currencyMap[countryCode] || 'USD';
};

/**
 * Format currency for display
 */
export const formatCurrency = (amount, currencyCode) => {
  const symbol = getCurrencySymbol(currencyCode);
  const formatted = amount.toFixed(2);

  // Place symbol before or after based on currency
  const symbolAfter = ['EUR', 'SEK', 'NOK', 'DKK', 'PLN'];

  if (symbolAfter.includes(currencyCode)) {
    return `${formatted}${symbol}`;
  }

  return `${symbol}${formatted}`;
};

export default {
  fetchExchangeRates,
  convertCurrency,
  getCurrencySymbol,
  getCurrencyFromCountry,
  formatCurrency,
};
