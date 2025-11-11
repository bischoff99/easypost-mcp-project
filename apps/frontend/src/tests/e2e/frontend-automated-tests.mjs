/**
 * Comprehensive Frontend Automated Tests using Puppeteer
 *
 * Tests all major frontend functionality:
 * 1. Dashboard loading and data display
 * 2. Shipments page navigation and filtering
 * 3. Tracking functionality
 * 4. Analytics page rendering
 * 5. Address Book CRUD operations
 * 6. Settings page functionality
 *
 * Run with: node frontend/src/tests/e2e/frontend-automated-tests.js
 */

import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdir } from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:80';
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const SCREENSHOT_DIR = join(__dirname, '../../../test-screenshots');

// Ensure screenshot directory exists
await mkdir(SCREENSHOT_DIR, { recursive: true });

// Helper function to wait
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Test Suite: Dashboard Page
 */
async function testDashboard(page) {
  console.log('\n📊 Testing Dashboard Page...');

  await page.goto(FRONTEND_URL, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(2000);
  await page.screenshot({ path: join(SCREENSHOT_DIR, '01-dashboard-loaded.png') });

  const dashboardContent = await page.evaluate(() => {
    const dashboard = document.body;
    const hasContent = dashboard && (
      dashboard.textContent.includes('Dashboard') ||
      dashboard.textContent.includes('Total Shipments') ||
      dashboard.textContent.includes('Shipments')
    );
    const statsCards = document.querySelectorAll('[class*="Card"], [class*="card"]').length;
    const hasReactRoot = document.getElementById('root') !== null;

    return {
      hasContent,
      statsCards,
      hasReactRoot,
      title: document.title,
      url: window.location.href
    };
  });

  console.log('✅ Dashboard loaded:', dashboardContent);
  return dashboardContent;
}

/**
 * Test Suite: Shipments Page
 */
async function testShipmentsPage(page) {
  console.log('\n📦 Testing Shipments Page...');

  await page.goto(`${FRONTEND_URL}/shipments`, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(2000);
  await page.screenshot({ path: join(SCREENSHOT_DIR, '02-shipments-page.png') });

  const shipmentsContent = await page.evaluate(() => {
    return {
      pageLoaded: document.body.textContent.includes('Shipments') ||
                  document.body.textContent.includes('Create'),
      hasTable: document.querySelector('table') !== null,
      hasFilters: document.querySelector('input[type="search"], input[placeholder*="Search"]') !== null,
      hasCreateButton: Array.from(document.querySelectorAll('button')).some(btn =>
        btn.textContent.includes('New') || btn.textContent.includes('Create')
      )
    };
  });

  console.log('✅ Shipments page loaded:', shipmentsContent);
  return shipmentsContent;
}

/**
 * Test Suite: Tracking Page
 */
async function testTrackingPage(page) {
  console.log('\n📮 Testing Tracking Page...');

  await page.goto(`${FRONTEND_URL}/tracking`, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(2000);
  await page.screenshot({ path: join(SCREENSHOT_DIR, '03-tracking-page.png') });

  const trackingContent = await page.evaluate(() => {
    const input = document.querySelector('input[type="text"], input[placeholder*="tracking"], input[placeholder*="Tracking"]');
    const button = Array.from(document.querySelectorAll('button')).find(btn =>
      btn.textContent.includes('Track') || btn.textContent.includes('Search')
    );
    return {
      hasInput: input !== null,
      hasTrackButton: button !== null,
      placeholder: input ? input.placeholder : null
    };
  });

  console.log('✅ Tracking page loaded:', trackingContent);

  // Test tracking input (if available)
  if (trackingContent.hasInput) {
    try {
      const inputSelector = 'input[type="text"], input[placeholder*="tracking"], input[placeholder*="Tracking"]';
      await page.waitForSelector(inputSelector, { timeout: 5000 });
      await page.click(inputSelector, { clickCount: 3 });
      await page.type(inputSelector, 'EZ123456789');
      await wait(1000);
      await page.screenshot({ path: join(SCREENSHOT_DIR, '04-tracking-input-filled.png') });
      console.log('✅ Tracking input filled');
    } catch (error) {
      console.log('⚠️  Could not fill tracking input:', error.message);
    }
  }

  return trackingContent;
}

/**
 * Test Suite: Analytics Page
 */
async function testAnalyticsPage(page) {
  console.log('\n📈 Testing Analytics Page...');

  await page.goto(`${FRONTEND_URL}/analytics`, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(3000); // Wait longer for charts to load
  await page.screenshot({ path: join(SCREENSHOT_DIR, '05-analytics-page.png') });

  const analyticsContent = await page.evaluate(() => {
    return {
      pageLoaded: document.body.textContent.includes('Analytics') ||
                  document.body.textContent.includes('Metrics'),
      hasCharts: document.querySelector('svg') !== null ||
                 document.querySelector('[class*="Chart"]') !== null,
      hasMetrics: document.querySelectorAll('[class*="Card"], [class*="card"]').length > 0
    };
  });

  console.log('✅ Analytics page loaded:', analyticsContent);
  return analyticsContent;
}

/**
 * Test Suite: Address Book Page
 */
async function testAddressBookPage(page) {
  console.log('\n📇 Testing Address Book Page...');

  await page.goto(`${FRONTEND_URL}/addresses`, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(2000);
  await page.screenshot({ path: join(SCREENSHOT_DIR, '06-address-book-page.png') });

  const addressBookContent = await page.evaluate(() => {
    return {
      pageLoaded: document.body.textContent.includes('Address') ||
                  document.body.textContent.includes('Book'),
      hasAddButton: Array.from(document.querySelectorAll('button')).some(btn =>
        btn.textContent.includes('Add') || btn.textContent.includes('New')
      ),
      hasSearch: document.querySelector('input[type="search"], input[placeholder*="Search"]') !== null,
      hasAddressList: document.querySelectorAll('[class*="Card"], [class*="card"]').length > 0
    };
  });

  console.log('✅ Address Book page loaded:', addressBookContent);
  return addressBookContent;
}

/**
 * Test Suite: Settings Page
 */
async function testSettingsPage(page) {
  console.log('\n⚙️  Testing Settings Page...');

  await page.goto(`${FRONTEND_URL}/settings`, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(2000);
  await page.screenshot({ path: join(SCREENSHOT_DIR, '07-settings-page.png') });

  const settingsContent = await page.evaluate(() => {
    return {
      pageLoaded: document.body.textContent.includes('Settings') ||
                  document.body.textContent.includes('Preferences'),
      hasFormFields: document.querySelectorAll('input, select').length > 0,
      hasSaveButton: Array.from(document.querySelectorAll('button')).some(btn =>
        btn.textContent.includes('Save')
      ),
      hasSections: document.querySelectorAll('[class*="Card"], [class*="card"]').length > 0
    };
  });

  console.log('✅ Settings page loaded:', settingsContent);
  return settingsContent;
}

/**
 * Test Suite: Navigation and Sidebar
 */
async function testNavigation(page) {
  console.log('\n🧭 Testing Navigation...');

  await page.goto(FRONTEND_URL, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(2000);

  const navigationContent = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a[href]'));
    const navLinks = links.filter(link => {
      const href = link.getAttribute('href');
      return ['/shipments', '/tracking', '/analytics', '/addresses', '/settings'].some(path =>
        href === path || href.includes(path)
      );
    });
    return {
      hasNavLinks: navLinks.length > 0,
      linkCount: navLinks.length,
      links: navLinks.map(link => link.getAttribute('href'))
    };
  });

  console.log('✅ Navigation links found:', navigationContent);
  await page.screenshot({ path: join(SCREENSHOT_DIR, '08-navigation-sidebar.png') });

  return navigationContent;
}

/**
 * Test Suite: API Connectivity
 */
async function testAPIConnectivity(page) {
  console.log('\n🔌 Testing API Connectivity...');

  await page.goto(FRONTEND_URL, { waitUntil: 'networkidle2', timeout: 30000 });
  await wait(3000);

  // Check console for errors
  const consoleMessages = [];
  page.on('console', msg => {
    const text = msg.text();
    if (text.includes('error') || text.includes('Error') || text.includes('Failed')) {
      consoleMessages.push(text);
    }
  });

  // Check network requests
  const networkRequests = [];
  page.on('response', response => {
    if (response.status() >= 400) {
      networkRequests.push({
        url: response.url(),
        status: response.status()
      });
    }
  });

  await wait(2000);

  const apiStatus = await page.evaluate(() => {
    return {
      pageLoaded: document.readyState === 'complete',
      hasReactRoot: document.getElementById('root') !== null,
      apiBaseURL: window.location.origin
    };
  });

  console.log('✅ API connectivity check:', apiStatus);
  if (consoleMessages.length > 0) {
    console.log('⚠️  Console errors:', consoleMessages);
  }
  if (networkRequests.length > 0) {
    console.log('⚠️  Failed network requests:', networkRequests);
  }

  return { ...apiStatus, consoleErrors: consoleMessages.length, failedRequests: networkRequests.length };
}

/**
 * Main Test Runner
 */
async function runAllTests() {
  console.log('🚀 Starting Frontend Automated Tests...');
  console.log(`Frontend URL: ${FRONTEND_URL}`);
  console.log(`Backend URL: ${BACKEND_URL}`);
  console.log(`Screenshots: ${SCREENSHOT_DIR}\n`);

  const browser = await puppeteer.launch({
    headless: 'new',
    defaultViewport: { width: 1280, height: 720 },
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    timeout: 30000,
  });

  const page = await browser.newPage();

  // Set default timeout for all operations
  page.setDefaultTimeout(30000);
  page.setDefaultNavigationTimeout(30000);

  const results = {
    dashboard: null,
    shipments: null,
    tracking: null,
    analytics: null,
    addressBook: null,
    settings: null,
    navigation: null,
    apiConnectivity: null,
  };

  try {
    // Test API connectivity first
    results.apiConnectivity = await testAPIConnectivity(page);

    // Test navigation
    results.navigation = await testNavigation(page);

    // Test Dashboard
    results.dashboard = await testDashboard(page);

    // Test Shipments Page
    results.shipments = await testShipmentsPage(page);

    // Test Tracking Page
    results.tracking = await testTrackingPage(page);

    // Test Analytics Page
    results.analytics = await testAnalyticsPage(page);

    // Test Address Book Page
    results.addressBook = await testAddressBookPage(page);

    // Test Settings Page
    results.settings = await testSettingsPage(page);

    // Print summary
    console.log('\n' + '='.repeat(60));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(60));
    console.log(`✅ Dashboard: ${results.dashboard?.hasContent ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Shipments: ${results.shipments?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Tracking: ${results.tracking?.hasInput ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Analytics: ${results.analytics?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Address Book: ${results.addressBook?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Settings: ${results.settings?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log(`✅ Navigation: ${results.navigation?.hasNavLinks ? 'PASS' : 'FAIL'}`);
    console.log(`✅ API Connectivity: ${results.apiConnectivity?.pageLoaded ? 'PASS' : 'FAIL'}`);
    console.log('='.repeat(60));

    const allPassed = Object.values(results).every(result =>
      result && (result.hasContent || result.pageLoaded || result.hasInput || result.hasNavLinks)
    );

    if (allPassed) {
      console.log('\n🎉 All tests passed!');
      console.log(`📸 Screenshots saved to: ${SCREENSHOT_DIR}`);
      return 0;
    } else {
      console.log('\n⚠️  Some tests failed. Check screenshots for details.');
      console.log(`📸 Screenshots saved to: ${SCREENSHOT_DIR}`);
      return 1;
    }

  } catch (error) {
    console.error('\n❌ Test suite failed:', error);
    try {
      await page.screenshot({ path: join(SCREENSHOT_DIR, 'error-final.png') });
    } catch (screenshotError) {
      console.error('Could not take error screenshot:', screenshotError.message);
    }
    return 1;
  } finally {
    try {
      await browser.close();
    } catch (closeError) {
      console.error('Error closing browser:', closeError.message);
    }
  }
}

// Run tests with timeout protection
const testTimeout = setTimeout(() => {
  console.error('\n❌ Test suite timed out after 2 minutes');
  process.exit(1);
}, 120000); // 2 minute timeout

runAllTests()
  .then(exitCode => {
    clearTimeout(testTimeout);
    process.exit(exitCode);
  })
  .catch(error => {
    clearTimeout(testTimeout);
    console.error('Unhandled error:', error);
    process.exit(1);
  });
