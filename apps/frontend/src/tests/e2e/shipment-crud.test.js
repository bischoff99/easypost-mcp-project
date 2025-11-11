import { describe, it, expect } from 'vitest';
import api from '../../services/api';

/**
 * Shipment CRUD E2E Tests
 *
 * Tests complete shipment lifecycle:
 * 1. Create shipment with addresses
 * 2. Get rates from multiple carriers
 * 3. Buy label with selected rate
 * 4. Track shipment status
 * 5. Retrieve label image
 *
 * M3 Max Optimized: Run with vitest --threads=20
 */

// E2E tests require running backend - skip in CI/unit tests
describe.skip('Shipment CRUD Operations', () => {
  const mockShipmentData = {
    from_address: {
      name: 'John Sender',
      street1: '123 Main St',
      city: 'San Francisco',
      state: 'CA',
      zip: '94102',
      country: 'US',
      phone: '415-555-0123',
    },
    to_address: {
      name: 'Jane Receiver',
      street1: '456 Market St',
      city: 'New York',
      state: 'NY',
      zip: '10001',
      country: 'US',
      phone: '212-555-0456',
    },
    parcel: {
      length: 10,
      width: 8,
      height: 4,
      weight: 16,
    },
  };

  describe('Create Shipment', () => {
    it('creates shipment with valid addresses', async () => {
      const response = await api.post('/shipments', mockShipmentData);

      expect(response.data.status).toBe('success');
      expect(response.data.data).toHaveProperty('id');
      expect(response.data.data).toHaveProperty('rates');
      expect(Array.isArray(response.data.data.rates)).toBe(true);
    });

    it('returns error for invalid address', async () => {
      const invalidData = {
        ...mockShipmentData,
        from_address: {
          ...mockShipmentData.from_address,
          zip: 'INVALID',
        },
      };

      try {
        await api.post('/shipments', invalidData);
      } catch (error) {
        expect(error.response.status).toBeGreaterThanOrEqual(400);
      }
    });
  });

  describe('Get Rates', () => {
    it('retrieves rates for shipment', async () => {
      const ratesData = {
        from_address: mockShipmentData.from_address,
        to_address: mockShipmentData.to_address,
        parcel: mockShipmentData.parcel,
      };

      const response = await api.post('/rates', ratesData);

      expect(response.data.status).toBe('success');
      expect(response.data.data).toHaveProperty('rates');
      expect(response.data.data.rates.length).toBeGreaterThan(0);

      // Check rate structure
      const rate = response.data.data.rates[0];
      expect(rate).toHaveProperty('id');
      expect(rate).toHaveProperty('carrier');
      expect(rate).toHaveProperty('service');
      expect(rate).toHaveProperty('rate');
      expect(rate).toHaveProperty('delivery_days');
    });

    it('compares rates across carriers', async () => {
      const ratesData = {
        from_address: mockShipmentData.from_address,
        to_address: mockShipmentData.to_address,
        parcel: mockShipmentData.parcel,
      };

      const response = await api.post('/rates', ratesData);
      const rates = response.data.data.rates;

      // Should have rates from multiple carriers
      const carriers = new Set(rates.map((r) => r.carrier));
      expect(carriers.size).toBeGreaterThan(1);

      // Rates should be sortable by price
      const sortedByPrice = [...rates].sort((a, b) => parseFloat(a.rate) - parseFloat(b.rate));
      expect(sortedByPrice[0].rate).toBeLessThanOrEqual(sortedByPrice[1].rate);
    });
  });

  describe('Buy Label', () => {
    it('purchases label with selected rate', async () => {
      // First create shipment and get rates
      const createResponse = await api.post('/shipments', mockShipmentData);
      const shipmentId = createResponse.data.data.id;
      const rateId = createResponse.data.data.rates[0].id;

      // Buy label
      const buyResponse = await api.post('/shipments/buy', {
        shipment_id: shipmentId,
        rate_id: rateId,
      });

      expect(buyResponse.data.status).toBe('success');
      expect(buyResponse.data.data).toHaveProperty('tracking_number');
      expect(buyResponse.data.data).toHaveProperty('label_url');
      expect(buyResponse.data.data).toHaveProperty('postage_label');
    });

    it('validates rate ID before purchase', async () => {
      try {
        await api.post('/shipments/buy', {
          shipment_id: 'invalid',
          rate_id: 'invalid',
        });
      } catch (error) {
        expect(error.response.status).toBeGreaterThanOrEqual(400);
      }
    });
  });

  describe('Track Shipment', () => {
    it('tracks shipment by tracking number', async () => {
      // Use a real tracking number from test data
      const trackingNumber = '1Z09E1D36727775421';

      const response = await api.get(`/tracking/${trackingNumber}`);

      expect(response.data.status).toBe('success');
      expect(response.data.data).toHaveProperty('tracking_number');
      expect(response.data.data).toHaveProperty('status_detail');
      expect(response.data.data).toHaveProperty('events');
      expect(Array.isArray(response.data.data.events)).toBe(true);
    });

    it('returns tracking history events', async () => {
      const trackingNumber = '1Z09E1D36727775421';
      const response = await api.get(`/tracking/${trackingNumber}`);

      const events = response.data.data.events;
      expect(events.length).toBeGreaterThan(0);

      // Check event structure
      const event = events[0];
      expect(event).toHaveProperty('timestamp');
      expect(event).toHaveProperty('status');
      expect(event).toHaveProperty('message');
    });

    it('handles invalid tracking number', async () => {
      try {
        await api.get('/tracking/INVALID123');
      } catch (error) {
        expect(error.response.status).toBeGreaterThanOrEqual(400);
      }
    });
  });

  describe('List Shipments', () => {
    it('retrieves shipment list', async () => {
      const response = await api.get('/db/shipments?limit=10');

      expect(response.data.status).toBe('success');
      expect(Array.isArray(response.data.data)).toBe(true);
      expect(response.data.data.length).toBeGreaterThan(0);
    });

    it('supports pagination', async () => {
      const page1 = await api.get('/db/shipments?limit=5');
      const page2 = await api.get('/shipments?limit=5&after_id=' + page1.data.data[4].id);

      expect(page1.data.data.length).toBe(5);
      expect(page2.data.data.length).toBeGreaterThan(0);

      // Pages should not overlap
      const page1Ids = page1.data.data.map((s) => s.id);
      const page2Ids = page2.data.data.map((s) => s.id);
      const overlap = page1Ids.filter((id) => page2Ids.includes(id));
      expect(overlap.length).toBe(0);
    });
  });

  describe('Complete Workflow', () => {
    it('completes full shipment lifecycle', async () => {
      // Step 1: Create shipment
      const createResponse = await api.post('/shipments', mockShipmentData);
      expect(createResponse.data.status).toBe('success');

      const shipmentId = createResponse.data.data.id;
      const rates = createResponse.data.data.rates;
      expect(rates.length).toBeGreaterThan(0);

      // Step 2: Select cheapest rate
      const cheapestRate = rates.reduce((min, rate) =>
        parseFloat(rate.rate) < parseFloat(min.rate) ? rate : min
      );
      expect(cheapestRate).toHaveProperty('id');

      // Step 3: Buy label
      const buyResponse = await api.post('/shipments/buy', {
        shipment_id: shipmentId,
        rate_id: cheapestRate.id,
      });
      expect(buyResponse.data.status).toBe('success');

      const trackingNumber = buyResponse.data.data.tracking_number;
      expect(trackingNumber).toBeTruthy();

      // Step 4: Track shipment
      const trackResponse = await api.get(`/tracking/${trackingNumber}`);
      expect(trackResponse.data.status).toBe('success');
      expect(trackResponse.data.data.tracking_number).toBe(trackingNumber);

      // Step 5: Verify in shipment list
      const listResponse = await api.get('/db/shipments?limit=100');
      const shipmentInList = listResponse.data.data.find(
        (s) => s.tracking_number === trackingNumber
      );
      expect(shipmentInList).toBeTruthy();
    }, 30000); // 30 second timeout for full workflow
  });
});
