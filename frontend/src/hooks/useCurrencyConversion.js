import { useQuery } from '@tanstack/react-query';
import { fetchExchangeRates, convertCurrency } from '@/services/currencyService';
import { logger } from '@/lib/logger';
import { useState, useCallback } from 'react';

/**
 * useCurrencyConversion Hook
 *
 * Manages currency conversion with caching
 */
export const useCurrencyConversion = () => {
  const [targetCurrency, setTargetCurrency] = useState('USD');

  // Fetch exchange rates with 1-hour cache
  const { data: rates, isLoading, error } = useQuery({
    queryKey: ['exchange-rates'],
    queryFn: fetchExchangeRates,
    staleTime: 60 * 60 * 1000, // 1 hour
    cacheTime: 60 * 60 * 1000, // 1 hour
    refetchOnWindowFocus: false,
    onSuccess: (data) => {
      logger.debug('Exchange rates fetched:', data);
    },
    onError: (error) => {
      logger.error('Failed to fetch exchange rates:', error);
    },
  });

  // Convert amount to target currency
  const convert = useCallback(
    async (amount, currency = targetCurrency) => {
      try {
        return await convertCurrency(amount, currency);
      } catch (error) {
        logger.error('Currency conversion failed:', error);
        return amount; // Fallback to original amount
      }
    },
    [targetCurrency]
  );

  return {
    rates,
    isLoading,
    error,
    targetCurrency,
    setTargetCurrency,
    convert,
  };
};

export default useCurrencyConversion;
