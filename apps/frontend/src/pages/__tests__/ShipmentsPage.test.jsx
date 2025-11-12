import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ShipmentsPage from '../ShipmentsPage';
import { shipmentAPI } from '@/services/api';

// Mock the API
vi.mock('@/services/api', () => ({
  shipmentAPI: {
    getRecentShipments: vi.fn(),
  },
}));

// Mock router navigation
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('ShipmentsPage', () => {
  let queryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });
    vi.clearAllMocks();
  });

  const renderWithProviders = (component) => {
    return render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          {component}
        </BrowserRouter>
      </QueryClientProvider>
    );
  };

  it('renders page title and description', async () => {
    shipmentAPI.getRecentShipments.mockResolvedValue({
      status: 'success',
      data: [],
    });

    renderWithProviders(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText('Shipments')).toBeInTheDocument();
      expect(screen.getByText('View and manage all your shipments')).toBeInTheDocument();
    });
  });

  it('renders New Shipment button', async () => {
    shipmentAPI.getRecentShipments.mockResolvedValue({
      status: 'success',
      data: [],
    });

    renderWithProviders(<ShipmentsPage />);

    await waitFor(() => {
      const newButton = screen.getByText('New Shipment');
      expect(newButton).toBeInTheDocument();
    });
  });

  it('displays empty state when no shipments', async () => {
    shipmentAPI.getRecentShipments.mockResolvedValue({
      status: 'success',
      data: [],
    });

    renderWithProviders(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText('No shipments yet')).toBeInTheDocument();
    });
  });

  it('displays shipments when data is loaded', async () => {
    const mockShipments = [
      {
        id: '1',
        tracking_number: 'EZ1234567890',
        status: 'in_transit',
        carrier: 'USPS',
        service: 'Priority Mail',
        from: 'San Francisco, CA',
        to: 'New York, NY',
        rate: '12.50',
        created_at: new Date().toISOString(),
      },
    ];

    shipmentAPI.getRecentShipments.mockResolvedValue({
      status: 'success',
      data: mockShipments,
    });

    renderWithProviders(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText('EZ1234567890')).toBeInTheDocument();
      expect(screen.getByText('USPS')).toBeInTheDocument();
    });
  });

  it('shows filters card', async () => {
    shipmentAPI.getRecentShipments.mockResolvedValue({
      status: 'success',
      data: [],
    });

    renderWithProviders(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText('Search & Filter')).toBeInTheDocument();
    });
  });
});





















