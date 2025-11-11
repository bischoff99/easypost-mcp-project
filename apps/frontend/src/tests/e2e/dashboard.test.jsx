import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Toaster } from 'sonner';

// Import pages
import DashboardPage from '../../pages/DashboardPage';
import ShipmentsPage from '../../pages/ShipmentsPage';
import TrackingPage from '../../pages/TrackingPage';
import AnalyticsPage from '../../pages/AnalyticsPage';

/**
 * E2E Dashboard Tests
 *
 * Tests complete dashboard functionality including:
 * - Page navigation and rendering
 * - Interactive elements (buttons, forms)
 * - Data display and updates
 * - Error handling
 *
 * M3 Max Optimized: Run with vitest --threads=20
 */

// Test wrapper with router
const renderWithRouter = (Component) => {
  return render(
    <BrowserRouter>
      <Component />
      <Toaster />
    </BrowserRouter>
  );
};

// E2E tests require running backend - skip in CI/unit tests
describe.skip('Dashboard E2E Tests', () => {
  describe('DashboardPage', () => {
    it('renders dashboard with all sections', async () => {
      renderWithRouter(DashboardPage);

      // Check main heading
      expect(screen.getByText('Dashboard Overview')).toBeInTheDocument();

      // Check stats cards are present
      await waitFor(() => {
        expect(screen.getByText('Total Shipments')).toBeInTheDocument();
        expect(screen.getByText('This Week')).toBeInTheDocument();
        expect(screen.getByText('Success Rate')).toBeInTheDocument();
      });

      // Check quick actions
      expect(screen.getByText('Create Shipment')).toBeInTheDocument();
      expect(screen.getByText('Track Package')).toBeInTheDocument();
      expect(screen.getByText('View Rates')).toBeInTheDocument();
    });

    it('displays recent activity section', () => {
      renderWithRouter(DashboardPage);

      expect(screen.getByText('Recent Activity')).toBeInTheDocument();
      expect(screen.getByText('Latest shipping updates and events')).toBeInTheDocument();
    });
  });

  describe('ShipmentsPage', () => {
    it('renders shipments list page', () => {
      renderWithRouter(ShipmentsPage);

      expect(screen.getByText('Shipments')).toBeInTheDocument();
      expect(screen.getByText('View and manage all your shipments')).toBeInTheDocument();
      expect(screen.getByText('New Shipment')).toBeInTheDocument();
    });

    it('displays search and filter section', () => {
      renderWithRouter(ShipmentsPage);

      expect(screen.getByText('Search & Filter')).toBeInTheDocument();
      expect(
        screen.getByPlaceholderText('Search by tracking number, address...')
      ).toBeInTheDocument();
      expect(screen.getByText('Filters')).toBeInTheDocument();
    });
  });

  describe('TrackingPage', () => {
    it('renders tracking page with input', () => {
      renderWithRouter(TrackingPage);

      expect(screen.getByText('Track Package')).toBeInTheDocument();
      expect(screen.getByText('Track your shipments in real-time')).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/Enter tracking number/i)).toBeInTheDocument();
    });

    it('shows empty state initially', () => {
      renderWithRouter(TrackingPage);

      expect(screen.getByText('No tracking data')).toBeInTheDocument();
      expect(screen.getByText('Enter a tracking number to get started')).toBeInTheDocument();
    });
  });

  describe('AnalyticsPage', () => {
    it('renders analytics page with all metrics', () => {
      renderWithRouter(AnalyticsPage);

      expect(screen.getByText('Analytics')).toBeInTheDocument();
      expect(
        screen.getByText('Insights and analytics for your shipping operations')
      ).toBeInTheDocument();
    });

    it('displays all metric cards with trends', () => {
      renderWithRouter(AnalyticsPage);

      // Check all 4 metrics are present
      expect(screen.getByText('Total Shipments')).toBeInTheDocument();
      expect(screen.getByText('Total Spending')).toBeInTheDocument();
      expect(screen.getByText('Average Cost')).toBeInTheDocument();
      expect(screen.getByText('Success Rate')).toBeInTheDocument();

      // Check metric values
      expect(screen.getByText('2,612')).toBeInTheDocument();
      expect(screen.getByText('$43,025')).toBeInTheDocument();
      expect(screen.getByText('$16.47')).toBeInTheDocument();
      expect(screen.getByText('94.3%')).toBeInTheDocument();

      // Check trends are displayed
      expect(screen.getByText('+12.5%')).toBeInTheDocument();
      expect(screen.getByText('+8.2%')).toBeInTheDocument();
      expect(screen.getByText('-3.1%')).toBeInTheDocument();
      expect(screen.getByText('+2.4%')).toBeInTheDocument();
    });

    it('displays all charts', () => {
      renderWithRouter(AnalyticsPage);

      expect(screen.getByText('Shipment Volume')).toBeInTheDocument();
      expect(screen.getByText('Carrier Distribution')).toBeInTheDocument();
      expect(screen.getByText('Cost Breakdown')).toBeInTheDocument();
      expect(screen.getByText('Top Destinations')).toBeInTheDocument();
    });

    it('displays time period filters', () => {
      renderWithRouter(AnalyticsPage);

      expect(screen.getByText('Last 7 Days')).toBeInTheDocument();
      expect(screen.getByText('Last 30 Days')).toBeInTheDocument();
      expect(screen.getByText('Last 90 Days')).toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    it('all pages are accessible without errors', () => {
      const pages = [
        DashboardPage,
        ShipmentsPage,
        TrackingPage,
        AnalyticsPage,
      ];

      pages.forEach((Page) => {
        const { unmount } = renderWithRouter(Page);
        expect(document.body).toBeTruthy();
        unmount();
      });
    });
  });
});
