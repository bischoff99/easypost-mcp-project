/**
 * Country Data
 *
 * List of countries with codes, currencies, and shipping support
 */

export const COUNTRIES = [
  // North America
  { code: 'US', name: 'United States', currency: 'USD', region: 'North America' },
  { code: 'CA', name: 'Canada', currency: 'CAD', region: 'North America' },
  { code: 'MX', name: 'Mexico', currency: 'MXN', region: 'North America' },

  // Europe
  { code: 'GB', name: 'United Kingdom', currency: 'GBP', region: 'Europe' },
  { code: 'DE', name: 'Germany', currency: 'EUR', region: 'Europe' },
  { code: 'FR', name: 'France', currency: 'EUR', region: 'Europe' },
  { code: 'ES', name: 'Spain', currency: 'EUR', region: 'Europe' },
  { code: 'IT', name: 'Italy', currency: 'EUR', region: 'Europe' },
  { code: 'NL', name: 'Netherlands', currency: 'EUR', region: 'Europe' },
  { code: 'BE', name: 'Belgium', currency: 'EUR', region: 'Europe' },
  { code: 'CH', name: 'Switzerland', currency: 'CHF', region: 'Europe' },
  { code: 'AT', name: 'Austria', currency: 'EUR', region: 'Europe' },
  { code: 'SE', name: 'Sweden', currency: 'SEK', region: 'Europe' },
  { code: 'NO', name: 'Norway', currency: 'NOK', region: 'Europe' },
  { code: 'DK', name: 'Denmark', currency: 'DKK', region: 'Europe' },
  { code: 'FI', name: 'Finland', currency: 'EUR', region: 'Europe' },
  { code: 'PL', name: 'Poland', currency: 'PLN', region: 'Europe' },

  // Asia Pacific
  { code: 'AU', name: 'Australia', currency: 'AUD', region: 'Asia Pacific' },
  { code: 'NZ', name: 'New Zealand', currency: 'NZD', region: 'Asia Pacific' },
  { code: 'JP', name: 'Japan', currency: 'JPY', region: 'Asia Pacific' },
  { code: 'CN', name: 'China', currency: 'CNY', region: 'Asia Pacific' },
  { code: 'IN', name: 'India', currency: 'INR', region: 'Asia Pacific' },
  { code: 'SG', name: 'Singapore', currency: 'SGD', region: 'Asia Pacific' },
  { code: 'HK', name: 'Hong Kong', currency: 'HKD', region: 'Asia Pacific' },
  { code: 'KR', name: 'South Korea', currency: 'KRW', region: 'Asia Pacific' },

  // South America
  { code: 'BR', name: 'Brazil', currency: 'BRL', region: 'South America' },
  { code: 'AR', name: 'Argentina', currency: 'ARS', region: 'South America' },
  { code: 'CL', name: 'Chile', currency: 'CLP', region: 'South America' },

  // Middle East
  { code: 'AE', name: 'United Arab Emirates', currency: 'AED', region: 'Middle East' },
  { code: 'SA', name: 'Saudi Arabia', currency: 'SAR', region: 'Middle East' },
  { code: 'IL', name: 'Israel', currency: 'ILS', region: 'Middle East' },
];

export const getCountryByCode = (code) => {
  return COUNTRIES.find((country) => country.code === code);
};

export const getCountriesByRegion = (region) => {
  return COUNTRIES.filter((country) => country.region === region);
};

export const REGIONS = [...new Set(COUNTRIES.map((c) => c.region))];

export default COUNTRIES;
