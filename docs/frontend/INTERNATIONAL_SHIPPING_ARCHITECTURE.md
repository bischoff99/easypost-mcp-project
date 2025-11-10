# International Shipping - Architecture & Data Flow

**Date**: 2025-11-09
**Branch**: `feature/international-shipping`
**Status**: Planning Phase

---

## Overview

Extend the modernized React + Vite frontend to support fully functional international shipments with:
- Country selection
- Real-time shipping rates
- Currency conversion
- Tax/duty calculation
- Multi-language support (i18n)

---

## Architecture

### Component Structure

```
src/
├── components/
│   ├── shipping/
│   │   ├── CountrySelector.jsx       # Country dropdown with flags
│   │   ├── ShippingOptions.jsx       # Display shipping methods
│   │   ├── PriceBreakdown.jsx        # Itemized costs with taxes
│   │   └── AddressValidator.jsx      # International address validation
│   └── i18n/
│       └── LanguageSelector.jsx      # Language switcher
├── services/
│   ├── shippingAPI.js                # Shipping rate API client
│   ├── currencyAPI.js                # Exchange rate service
│   ├── taxCalculator.js              # Tax/duty calculator
│   └── addressValidator.js           # Address validation service
├── locales/
│   ├── en/
│   │   └── translation.json          # English translations
│   ├── es/
│   │   └── translation.json          # Spanish translations
│   ├── fr/
│   │   └── translation.json          # French translations
│   └── de/
│       └── translation.json          # German translations
└── hooks/
    ├── useShippingRates.js           # Hook for fetching rates
    ├── useCurrencyConversion.js      # Hook for currency conversion
    └── useI18n.js                    # i18n helper hook
```

---

## Data Flow

### 1. Shipping Rate Calculation

```
User Input (Country, Address, Package)
    ↓
Frontend validates address format
    ↓
API call to backend with:
- Origin address
- Destination address
- Package dimensions/weight
- Selected currency
    ↓
Backend calls EasyPost API
    ↓
Returns shipping options:
- Carrier name
- Service level
- Base cost
- Estimated delivery
    ↓
Frontend applies currency conversion
    ↓
Frontend calculates taxes/duties
    ↓
Display total with breakdown
```

### 2. Currency Conversion Flow

```
User selects destination country
    ↓
Determine currency from country code
    ↓
Check cache for exchange rate
    ↓
If not cached or expired:
  - Call exchangerate-api.com
  - Cache for 1 hour
    ↓
Convert shipping cost to local currency
    ↓
Display with currency symbol
```

### 3. Tax/Duty Calculation

```
Shipping destination country
    ↓
Look up tax rules:
- VAT rate (EU countries)
- GST rate (Canada, Australia, etc.)
- Customs duty threshold
- Import fees
    ↓
Calculate based on:
- Item value
- Shipping cost
- Country rules
    ↓
Display itemized breakdown
```

---

## API Integration

### Shipping API (EasyPost)

**Endpoint**: `/api/shipping/rates`

**Request**:
```json
{
  "origin": {
    "country": "US",
    "zip": "94107",
    "city": "San Francisco",
    "state": "CA"
  },
  "destination": {
    "country": "GB",
    "zip": "SW1A 1AA",
    "city": "London"
  },
  "package": {
    "length": 10,
    "width": 8,
    "height": 6,
    "weight": 16,
    "unit": "oz"
  }
}
```

**Response**:
```json
{
  "rates": [
    {
      "carrier": "USPS",
      "service": "Priority Mail International",
      "cost": 45.50,
      "currency": "USD",
      "delivery_days": "6-10",
      "delivery_date": "2025-11-19"
    }
  ]
}
```

### Currency API (exchangerate-api.com)

**Endpoint**: `https://api.exchangerate-api.com/v4/latest/USD`

**Response**:
```json
{
  "base": "USD",
  "date": "2025-11-09",
  "rates": {
    "GBP": 0.79,
    "EUR": 0.92,
    "JPY": 149.50
  }
}
```

---

## Tax/Duty Rules

### Country-specific Rules

| Country | VAT/GST | Threshold | Customs Duty |
|---------|---------|-----------|--------------|
| UK | 20% | £135 | Varies by product |
| Germany | 19% | €22 | Varies by product |
| France | 20% | €22 | Varies by product |
| Canada | 5% GST | CAD $20 | Varies by product |
| Australia | 10% GST | AUD $1000 | Varies by product |

**Implementation**: Create tax calculator with country-specific rules

---

## i18n Configuration

### Translation Keys

```json
{
  "shipping": {
    "selectCountry": "Select destination country",
    "shippingOptions": "Shipping options",
    "standard": "Standard",
    "express": "Express",
    "economy": "Economy",
    "estimatedDelivery": "Estimated delivery",
    "priceBreakdown": "Price breakdown",
    "subtotal": "Subtotal",
    "shipping": "Shipping",
    "taxes": "Taxes & Duties",
    "total": "Total"
  }
}
```

### Supported Languages
- English (en)
- Spanish (es)
- French (fr)
- German (de)

**Future**: Add Japanese, Chinese, Arabic (RTL support)

---

## State Management

### Shipping Store (Zustand)

```javascript
const useShippingStore = create((set) => ({
  selectedCountry: null,
  selectedCurrency: 'USD',
  exchangeRates: {},
  shippingRates: [],
  selectedRate: null,
  taxes: 0,
  total: 0,

  setCountry: (country) => set({ selectedCountry: country }),
  setCurrency: (currency) => set({ selectedCurrency: currency }),
  setRates: (rates) => set({ shippingRates: rates }),
  selectRate: (rate) => set({ selectedRate: rate }),
  calculateTotal: () => { /* calculation logic */ }
}));
```

---

## Performance Optimizations

### Code Splitting
- Lazy load country data (flags, names)
- Dynamic import for shipping API client
- Separate i18n bundles per language

### Caching Strategy
- Exchange rates: 1 hour TTL
- Country data: Session storage
- Shipping rates: 15 minutes TTL

### Bundle Size
- Use react-country-flag (lightweight)
- Tree-shake unused translations
- Compress flag images

---

## Security Considerations

1. **API Keys**
   - Store in `.env.local`
   - Never commit to git
   - Use environment-specific values

2. **Input Validation**
   - Sanitize all address inputs
   - Validate country codes against ISO list
   - Rate limit API calls

3. **Data Privacy**
   - Don't log sensitive address data
   - Encrypt API payloads
   - GDPR compliant data handling

---

## Testing Strategy

### Unit Tests
- Currency conversion accuracy
- Tax calculation for each country
- Address validation rules

### Integration Tests
- API error handling
- Rate limiting behavior
- Cache invalidation

### E2E Tests (Puppeteer)
- Complete checkout flow
- Country selection
- Currency switching
- Tax display
- Visual regression

---

## Dependencies to Add

```json
{
  "dependencies": {
    "react-i18next": "^13.5.0",
    "i18next": "^23.7.6",
    "react-country-flag": "^3.1.0",
    "country-list": "^2.3.0",
    "currency-symbol-map": "^5.1.0",
    "validator": "^13.11.0"
  },
  "devDependencies": {
    "@types/validator": "^13.11.6"
  }
}
```

---

## Implementation Timeline

1. **Phase 1**: Dependencies & Setup (30 min)
2. **Phase 2**: API Layer (1 hour)
3. **Phase 3**: UI Components (1.5 hours)
4. **Phase 4**: i18n Integration (1 hour)
5. **Phase 5**: Testing (1 hour)
6. **Phase 6**: Documentation (30 min)

**Total Estimate**: ~5.5 hours

---

## Next Steps

1. Install dependencies
2. Create API service layer
3. Build country selector UI
4. Implement currency conversion
5. Add tax calculation
6. Setup i18n
7. Write tests
8. Update documentation

---

**Architecture Defined**: Ready for implementation
