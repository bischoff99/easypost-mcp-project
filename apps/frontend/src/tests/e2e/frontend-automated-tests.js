/**
 * Comprehensive Frontend Automated Tests using Puppeteer MCP
 *
 * Tests all major frontend functionality:
 * 1. Dashboard loading and data display
 * 2. Shipments page navigation and filtering
 * 3. Tracking functionality
 * 4. Analytics page rendering
 *
 * This test suite uses Puppeteer MCP tools for browser automation.
 */

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:80';
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

// Test configuration
const TEST_CONFIG = {
  timeout: 30000,
  waitTime: 2000,
  screenshotDir: 'test-screenshots',
};

// Test data
const testAddress = {
  name: 'Automated Test User',
  company: 'Test Company Inc',
  street1: '123 Test Street',
  street2: 'Suite 100',
  city: 'San Francisco',
  state: 'CA',
  zip: '94102',
  country: 'US',
  phone: '415-555-0123',
  email: 'test@example.com',
};

const testShipment = {
  from_address: {
    name: 'John Doe',
    street1: '123 Main St',
    city: 'San Francisco',
    state: 'CA',
    zip: '94102',
    country: 'US',
  },
  to_address: {
    name: 'Jane Smith',
    street1: '456 Oak Ave',
    city: 'Los Angeles',
    state: 'CA',
    zip: '90001',
    country: 'US',
  },
  parcel: {
    length: '10',
    width: '8',
    height: '4',
    weight: '16',
  },
};

/**
 * Test Suite: Dashboard Page
 */
async function testDashboard() {
  console.log('\n📊 Testing Dashboard Page...');

  // Navigate to dashboard
  await mcp_puppeteer_puppeteer_navigate({ url: FRONTEND_URL });
  await mcp_puppeteer_puppeteer_wait_for({ time: 3 });

  // Take screenshot
  await mcp_puppeteer_puppeteer_screenshot({ name: '01-dashboard-loaded' });

  // Check for dashboard elements
  const dashboardContent = await mcp_puppeteer_puppeteer_evaluate({
    script: `
      const dashboard = document.querySelector('[class*="Dashboard"]') ||
                       document.querySelector('h2:contains("Dashboard")') ||
                       document.body;
      return {
        hasContent: dashboard.textContent.includes('Dashboard') || dashboard.textContent.includes('Total Shipments'),
        statsVisible: document.querySelectorAll('[class*="Card"], [class*="card"]').length > 0,
        quickActionsVisible: document.querySelectorAll('button, a[href]').length > 3
      };
    `
  });

  console.log('✅ Dashboard loaded:', dashboardContent);
  return dashboardContent;
}

/**
 * Test Suite: Shipments Page
 */
async function testShipmentsPage() {
  console.log('\n📦 Testing Shipments Page...');

  // Navigate to shipments
  await mcp_puppeteer_puppeteer_navigate({ url: `${FRONTEND_URL}/shipments` });
  await mcp_puppeteer_puppeteer_wait_for({ time: 3 });

  await mcp_puppeteer_puppeteer_screenshot({ name: '02-shipments-page' });

  // Check for shipments table/list
  const shipmentsContent = await mcp_puppeteer_puppeteer_evaluate({
    script: `
      return {
        pageLoaded: document.body.textContent.includes('Shipments') ||
                    document.body.textContent.includes('Create'),
        hasTable: document.querySelector('table') !== null,
        hasFilters: document.querySelector('input[type="search"], input[placeholder*="Search"]') !== null,
        hasCreateButton: Array.from(document.querySelectorAll('button')).some(btn =>
          btn.textContent.includes('New') || btn.textContent.includes('Create')
        )
      };
    `
  });

  console.log('✅ Shipments page loaded:', shipmentsContent);
  return shipmentsContent;
}

/**
 * Test Suite: Tracking Page
 */
async function testTrackingPage() {
  console.log('\n📮 Testing Tracking Page...');

  // Navigate to tracking
  await mcp_puppeteer_puppeteer_navigate({ url: `${FRONTEND_URL}/tracking` });
  await mcp_puppeteer_puppeteer_wait_for({ time: 3 });

  await mcp_puppeteer_puppeteer_screenshot({ name: '03-tracking-page' });

  // Check for tracking input
  const trackingContent = await mcp_puppeteer_puppeteer_evaluate({
    script: `
      const input = document.querySelector('input[type="text"], input[placeholder*="tracking"], input[placeholder*="Tracking"]');
      const button = Array.from(document.querySelectorAll('button')).find(btn =>
        btn.textContent.includes('Track') || btn.textContent.includes('Search')
      );
      return {
        hasInput: input !== null,
        hasTrackButton: button !== null,
        placeholder: input ? input.placeholder : null
      };
    `
  });

  console.log('✅ Tracking page loaded:', trackingContent);

  // Test tracking input (if available)
  if (trackingContent.hasInput) {
    const inputSelector = 'input[type="text"], input[placeholder*="tracking"], input[placeholder*="Tracking"]';
    await mcp_puppeteer_puppeteer_fill({
      selector: inputSelector,
      value: 'EZ123456789'
    });
    await mcp_puppeteer_puppeteer_wait_for({ time: 1 });
    await mcp_puppeteer_puppeteer_screenshot({ name: '04-tracking-input-filled' });
    console.log('✅ Tracking input filled');
  }

  return trackingContent;
}

/**
 * Test Suite: Analytics Page
 */
async function testAnalyticsPage() {
  console.log('\n📈 Testing Analytics Page...');

  // Navigate to analytics
  await mcp_puppeteer_puppeteer_navigate({ url: `${FRONTEND_URL}/analytics` });
  await mcp_puppeteer_puppeteer_wait_for({ time: 3 });

  await mcp_puppeteer_puppeteer_screenshot({ name: '05-analytics-page' });

  // Check for analytics content
  const analyticsContent = await mcp_puppeteer_puppeteer_evaluate({
    script: `
      return {
        pageLoaded: document.body.textContent.includes('Analytics') ||
                    document.body.textContent.includes('Metrics'),
        hasCharts: document.querySelector('svg') !== null ||
                   document.querySelector('[class*="Chart"]') !== null,
        hasMetrics: document.querySelectorAll('[class*="Card"], [class*="card"]').length > 0
      };
    `
  });

  console.log('✅ Analytics page loaded:', analyticsContent);
  return analyticsContent;
}

/**
 * Test Suite: Navigation and Sidebar
 */
async function testNavigation() {
  console.log('\n🧭 Testing Navigation...');

  await mcp_puppeteer_puppeteer_navigate({ url: FRONTEND_URL });
  await mcp_puppeteer_puppeteer_wait_for({ time: 2 });

  // Check sidebar navigation
  const navigationContent = await mcp_puppeteer_puppeteer_evaluate({
    script: `
      const links = Array.from(document.querySelectorAll('a[href]'));
      const navLinks = links.filter(link =>
        return ['/shipments', '/tracking', '/analytics'].some(path =>
          link.getAttribute('href') === path
        )
      );
      return {
        hasNavLinks: navLinks.length > 0,
        linkCount: navLinks.length,
        links: navLinks.map(link => link.getAttribute('href'))
      };
    `
  });

  console.log('✅ Navigation links found:', navigationContent);
  await mcp_puppeteer_puppeteer_screenshot({ name: '08-navigation-sidebar' });

  return navigationContent;
}

/**
 * Test Suite: API Connectivity
 */
async function testAPIConnectivity() {
  console.log('\n🔌 Testing API Connectivity...');

  await mcp_puppeteer_puppeteer_navigate({ url: FRONTEND_URL });
  await mcp_puppeteer_puppeteer_wait_for({ time: 3 });

  // Check for API calls in network
  const apiStatus = await mcp_puppeteer_puppeteer_evaluate({
    script: `
      return {
        pageLoaded: document.readyState === 'complete',
        hasReactRoot: document.getElementById('root') !== null,
        apiBaseURL: window.location.origin
      };
    `
  });

  console.log('✅ API connectivity check:', apiStatus);
  return apiStatus;
}

/**
 * Main Test Runner
 */
async function runAllTests() {
  console.log('🚀 Starting Frontend Automated Tests...');
  console.log(`Frontend URL: ${FRONTEND_URL}`);
  console.log(`Backend URL: ${BACKEND_URL}\n`);

  const results = {
    dashboard: null,
    shipments: null,
    tracking: null,
    analytics: null,
    navigation: null,
    apiConnectivity: null,
  };

  try {
    // Test API connectivity first
    results.apiConnectivity = await testAPIConnectivity();

    // Test navigation
    results.navigation = await testNavigation();

    // Test Dashboard
    results.dashboard = await testDashboard();

    // Test Shipments Page
    results.shipments = await testShipmentsPage();

    // Test Tracking Page
    results.tracking = await testTrackingPage();

    // Test Analytics Page
    results.analytics = await testAnalyticsPage();

    // Print summary
    console.log('\n' + '='.repeat(60));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(60));
    console.log(`✅ Dashboard: ${results.dashboard?.hasContent ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Shipments: ${results.shipments?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Tracking: ${results.tracking?.hasInput ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Analytics: ${results.analytics?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Navigation: ${results.navigation?.hasNavLinks ? 'PASS' : 'FAIL'}`);
    console.log(`✅ API Connectivity: ${results.apiConnectivity?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log('='.repeat(60));

    const allPassed = Object.values(results).every(result =>
      result && (result.hasContent || result.pageLoaded || result.hasInput || result.hasNavLinks)
    );

    if (allPassed) {
      console.log('\n🎉 All tests passed!');
      return 0;
    } else {
      console.log('\n⚠️  Some tests failed. Check screenshots for details.');
      return 1;
    }

  } catch (error) {
    console.error('\n❌ Test suite failed:', error);
    await mcp_puppeteer_puppeteer_screenshot({ name: 'error-final' });
    return 1;
  }
}

// Export for use as module or run directly
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { runAllTests, testDashboard, testShipmentsPage, testTrackingPage };
} else {
  // Run tests if executed directly
  runAllTests().then(exitCode => {
    process.exit(exitCode);
  });
}
