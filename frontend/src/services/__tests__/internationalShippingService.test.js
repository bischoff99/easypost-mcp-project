import { describe, it, expect } from 'vitest';
import {
  calculateTaxesAndDuties,
  parseDeliveryDays,
} from '../internationalShippingService';

describe('internationalShippingService', () => {
  describe('calculateTaxesAndDuties', () => {
    it('calculates UK VAT correctly', () => {
      const result = calculateTaxesAndDuties({
        country: 'GB',
        itemValue: 200,
        shippingCost: 50,
      });

      expect(result.applicable).toBe(true);
      expect(result.vatRate).toBe(0.20);
      expect(result.vat).toBe(50);
      expect(result.customsDuty).toBe(5);
      expect(result.total).toBe(55);
    });

    it('returns zero under threshold', () => {
      const result = calculateTaxesAndDuties({
        country: 'GB',
        itemValue: 50,
        shippingCost: 10,
      });

      expect(result.applicable).toBe(false);
      expect(result.total).toBe(0);
      expect(result.threshold).toBe(135);
    });
  });

  describe('parseDeliveryDays', () => {
    it('parses single day', () => {
      expect(parseDeliveryDays('Priority 3 days')).toBe(3);
    });

    it('parses day range', () => {
      expect(parseDeliveryDays('Standard 6-10 days')).toBe(8);
    });

    it('defaults for express', () => {
      expect(parseDeliveryDays('Express')).toBe(3);
    });
  });
});
