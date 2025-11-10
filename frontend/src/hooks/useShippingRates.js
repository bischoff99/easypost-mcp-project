import { useMutation } from '@tanstack/react-query';
import { getInternationalRates } from '@/services/internationalShippingService';
import { logger } from '@/lib/logger';

/**
 * useShippingRates Hook
 *
 * Fetches and manages international shipping rates
 */
export const useShippingRates = () => {
  const fetchRatesMutation = useMutation({
    mutationFn: async (shipmentData) => {
      return await getInternationalRates(shipmentData);
    },
    onSuccess: (data) => {
      logger.debug('Shipping rates fetched:', data);
    },
    onError: (error) => {
      logger.error('Failed to fetch shipping rates:', error);
    },
  });

  return {
    getRates: fetchRatesMutation.mutate,
    rates: fetchRatesMutation.data,
    isLoading: fetchRatesMutation.isPending,
    error: fetchRatesMutation.error,
    reset: fetchRatesMutation.reset,
  };
};

export default useShippingRates;
