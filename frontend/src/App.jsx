import { lazy, Suspense, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'sonner';
import { initializeTheme } from './stores/useThemeStore';
import AppShell from './components/layout/AppShell';
import DashboardPage from './pages/DashboardPage';
import ErrorBoundary from './components/ui/ErrorBoundary';
import NavigationLoader from './components/ui/SuspenseBoundary';

// Lazy load pages for better performance
const ShipmentsPage = lazy(() => import('./pages/ShipmentsPage'));
const TrackingPage = lazy(() => import('./pages/TrackingPage'));
const AnalyticsPage = lazy(() => import('./pages/AnalyticsPage'));
const AddressBookPage = lazy(() => import('./pages/AddressBookPage'));
const SettingsPage = lazy(() => import('./pages/SettingsPage'));
const CreateShipmentPage = lazy(() => import('./pages/CreateShipmentPage'));
const InternationalShippingPage = lazy(() => import('./pages/InternationalShippingPage'));

// Loading fallback component
const PageLoader = () => (
  <div className="flex items-center justify-center h-[50vh]">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
  </div>
);

function App() {
  // Initialize theme on app start
  useEffect(() => {
    initializeTheme();
  }, []);

  return (
    <ErrorBoundary>
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <NavigationLoader />
        <Toaster position="top-right" richColors closeButton />
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<AppShell />}>
              <Route index element={<DashboardPage />} />
              <Route path="shipments" element={<ShipmentsPage />} />
              <Route path="shipments/new" element={<CreateShipmentPage />} />
              <Route path="shipments/international" element={<InternationalShippingPage />} />
              <Route path="tracking" element={<TrackingPage />} />
              <Route path="analytics" element={<AnalyticsPage />} />
              <Route path="addresses" element={<AddressBookPage />} />
              <Route path="settings" element={<SettingsPage />} />
            </Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
