import { describe, it, expect, beforeEach } from 'vitest';
import {
  getCurrencyFromCountry,
  getCurrencySymbol,
  formatCurrency,
} from '../currencyService';

describe('currencyService', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe('getCurrencyFromCountry', () => {
    it('returns correct currency for US', () => {
      expect(getCurrencyFromCountry('US')).toBe('USD');
    });

    it('returns correct currency for GB', () => {
      expect(getCurrencyFromCountry('GB')).toBe('GBP');
    });

    it('returns correct currency for DE', () => {
      expect(getCurrencyFromCountry('DE')).toBe('EUR');
    });

    it('returns USD for unknown country', () => {
      expect(getCurrencyFromCountry('XX')).toBe('USD');
    });
  });

  describe('getCurrencySymbol', () => {
    it('returns $ for USD', () => {
      expect(getCurrencySymbol('USD')).toBe('$');
    });

    it('returns £ for GBP', () => {
      expect(getCurrencySymbol('GBP')).toBe('£');
    });

    it('returns € for EUR', () => {
      expect(getCurrencySymbol('EUR')).toBe('€');
    });

    it('returns currency code for unknown', () => {
      expect(getCurrencySymbol('XXX')).toBe('XXX');
    });
  });

  describe('formatCurrency', () => {
    it('formats USD correctly', () => {
      expect(formatCurrency(100.50, 'USD')).toBe('$100.50');
    });

    it('formats GBP correctly', () => {
      expect(formatCurrency(75.25, 'GBP')).toBe('£75.25');
    });

    it('formats EUR correctly', () => {
      expect(formatCurrency(90.00, 'EUR')).toBe('90.00€');
    });
  });
});
