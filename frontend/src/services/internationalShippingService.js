import api from './api';
import { logger } from '@/lib/logger';
import { convertCurrency, getCurrencyFromCountry } from './currencyService';

/**
 * International Shipping Service
 *
 * Integrates with EasyPost backend API for:
 * - Address validation
 * - International shipping rates
 * - Customs information
 * - Tax/duty calculation
 */

/**
 * Validate international address using EasyPost
 *
 * @param {Object} address - Address object
 * @returns {Promise<Object>} - Validated address
 */
export const validateAddress = async (address) => {
  try {
    logger.debug('Validating address:', address);

    const response = await api.post('/addresses/validate', {
      street1: address.street1,
      street2: address.street2,
      city: address.city,
      state: address.state,
      zip: address.zip,
      country: address.country,
    });

    if (response.data.status === 'success') {
      return response.data.data;
    }

    throw new Error(response.data.message || 'Address validation failed');
  } catch (error) {
    logger.error('Address validation error:', error);
    throw error;
  }
};

/**
 * Get international shipping rates
 *
 * @param {Object} shipment - Shipment details
 * @returns {Promise<Array>} - Array of shipping rates
 */
export const getInternationalRates = async (shipment) => {
  try {
    logger.debug('Fetching international rates:', shipment);

    const response = await api.post('/shipments/rates', {
      from_address: shipment.from_address,
      to_address: shipment.to_address,
      parcel: shipment.parcel,
    });

    if (response.data.status === 'success') {
      const rates = response.data.data;

      // Convert rates to destination currency
      const targetCurrency = getCurrencyFromCountry(shipment.to_address.country);

      if (targetCurrency !== 'USD') {
        const convertedRates = await Promise.all(
          rates.map(async (rate) => {
            const convertedRate = await convertCurrency(rate.rate, targetCurrency);
            return {
              ...rate,
              original_rate: rate.rate,
              rate: convertedRate,
              currency: targetCurrency,
            };
          })
        );
        return convertedRates;
      }

      return rates.map((rate) => ({ ...rate, currency: 'USD' }));
    }

    throw new Error(response.data.message || 'Failed to fetch rates');
  } catch (error) {
    logger.error('Failed to fetch shipping rates:', error);
    throw error;
  }
};

/**
 * Calculate taxes and duties for international shipment
 *
 * @param {Object} params - Calculation parameters
 * @returns {Object} - Tax breakdown
 */
export const calculateTaxesAndDuties = (params) => {
  const { country, itemValue, shippingCost } = params;

  // Tax rules by country
  const taxRules = {
    GB: { vat: 0.20, threshold: 135, customsDuty: 0.025 }, // UK
    DE: { vat: 0.19, threshold: 22, customsDuty: 0.030 }, // Germany
    FR: { vat: 0.20, threshold: 22, customsDuty: 0.030 }, // France
    ES: { vat: 0.21, threshold: 22, customsDuty: 0.030 }, // Spain
    IT: { vat: 0.22, threshold: 22, customsDuty: 0.030 }, // Italy
    CA: { gst: 0.05, threshold: 20, customsDuty: 0.035 }, // Canada
    AU: { gst: 0.10, threshold: 1000, customsDuty: 0.050 }, // Australia
    JP: { vat: 0.10, threshold: 130, customsDuty: 0.040 }, // Japan
    CN: { vat: 0.13, threshold: 50, customsDuty: 0.070 }, // China
    IN: { gst: 0.18, threshold: 100, customsDuty: 0.100 }, // India
  };

  const rules = taxRules[country];

  if (!rules) {
    // Default: no additional taxes for countries not in the list
    return {
      vat: 0,
      customsDuty: 0,
      total: 0,
      threshold: 0,
      applicable: false,
    };
  }

  const totalValue = itemValue + shippingCost;
  const applicable = totalValue >= rules.threshold;

  if (!applicable) {
    return {
      vat: 0,
      customsDuty: 0,
      total: 0,
      threshold: rules.threshold,
      applicable: false,
    };
  }

  // Calculate VAT/GST
  const vatRate = rules.vat || rules.gst || 0;
  const vat = totalValue * vatRate;

  // Calculate customs duty
  const customsDuty = itemValue * rules.customsDuty;

  return {
    vat: parseFloat(vat.toFixed(2)),
    customsDuty: parseFloat(customsDuty.toFixed(2)),
    total: parseFloat((vat + customsDuty).toFixed(2)),
    threshold: rules.threshold,
    applicable: true,
    vatRate,
    customsDutyRate: rules.customsDuty,
  };
};

/**
 * Get estimated delivery date
 *
 * @param {number} days - Number of days
 * @returns {string} - Formatted date
 */
export const getEstimatedDeliveryDate = (days) => {
  const date = new Date();
  date.setDate(date.getDate() + days);

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

/**
 * Parse delivery days from service description
 *
 * @param {string} service - Service description
 * @returns {number} - Estimated days
 */
export const parseDeliveryDays = (service) => {
  // Extract days from service description (e.g., "Priority Mail International 6-10 Days")
  const match = service.match(/(\d+)-?(\d+)?\s*days?/i);

  if (match) {
    const min = parseInt(match[1], 10);
    const max = match[2] ? parseInt(match[2], 10) : min;
    return Math.ceil((min + max) / 2); // Return average
  }

  // Default estimates based on common service types
  if (service.toLowerCase().includes('express')) return 3;
  if (service.toLowerCase().includes('priority')) return 7;
  if (service.toLowerCase().includes('economy')) return 14;

  return 10; // Default
};

export default {
  validateAddress,
  getInternationalRates,
  calculateTaxesAndDuties,
  getEstimatedDeliveryDate,
  parseDeliveryDays,
};
