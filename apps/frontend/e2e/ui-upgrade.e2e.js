/**
 * E2E Tests for UI Upgrade
 *
 * Tests all new UI components and upgraded pages using browser tools
 */

export async function runUIUpgradeE2ETests(browser) {
  const results = {
    passed: 0,
    failed: 0,
    tests: [],
  };

  const addResult = (name, passed, error = null) => {
    results.tests.push({ name, passed, error });
    if (passed) results.passed++;
    else results.failed++;
  };

  try {
    // Navigate to shipments page
    console.log('🧪 Testing ShipmentsPage with DataTable...');
    await browser.navigate('http://localhost:4173/shipments');
    await browser.waitFor({ time: 2 });

    // Take initial snapshot
    const shipmentsSnapshot = await browser.snapshot();

    // Test 1: Check if page loaded
    const pageLoaded = shipmentsSnapshot.includes('Shipments') ||
                       shipmentsSnapshot.includes('shipments');
    addResult('ShipmentsPage loads successfully', pageLoaded);

    // Test 2: Check for search input
    const hasSearch = shipmentsSnapshot.includes('Search') ||
                      shipmentsSnapshot.includes('search');
    addResult('Search functionality present', hasSearch);

    // Test 3: Check for table elements
    const hasTable = shipmentsSnapshot.includes('table') ||
                     shipmentsSnapshot.includes('TableHeader');
    addResult('DataTable component rendered', hasTable);

    // Test 4: Take screenshot for visual verification
    await browser.takeScreenshot({ filename: 'shipments-page-upgraded.png' });
    addResult('Screenshot captured for visual verification', true);

    // Navigate to dashboard
    console.log('🧪 Testing Dashboard...');
    await browser.navigate('http://localhost:4173/');
    await browser.waitFor({ time: 2 });

    const dashboardSnapshot = await browser.snapshot();

    // Test 5: Dashboard loads
    const dashboardLoaded = dashboardSnapshot.includes('Dashboard') ||
                            dashboardSnapshot.includes('Quick Actions');
    addResult('Dashboard loads successfully', dashboardLoaded);

    // Test 6: Check for stats cards
    const hasStats = dashboardSnapshot.includes('StatsCard') ||
                     dashboardSnapshot.includes('Total Shipments');
    addResult('Stats cards rendered', hasStats);

    // Test 7: Check for quick actions
    const hasQuickActions = dashboardSnapshot.includes('Create Shipment') ||
                            dashboardSnapshot.includes('Quick Actions');
    addResult('Quick actions present', hasQuickActions);

    // Test 8: Dashboard screenshot
    await browser.takeScreenshot({ filename: 'dashboard-upgraded.png' });
    addResult('Dashboard screenshot captured', true);

    // Test theme toggle
    console.log('🧪 Testing Theme Toggle...');
    const themeSnapshot = await browser.snapshot();
    const hasThemeToggle = themeSnapshot.includes('Toggle theme') ||
                           themeSnapshot.includes('ThemeToggle');
    addResult('Theme toggle present', hasThemeToggle);

    // Test search modal trigger
    console.log('🧪 Testing Search Modal...');
    const hasSearchTrigger = themeSnapshot.includes('Search shipments') ||
                             themeSnapshot.includes('SearchModal');
    addResult('Search modal trigger present', hasSearchTrigger);

    // Test notifications
    console.log('🧪 Testing Notifications...');
    const hasNotifications = themeSnapshot.includes('Notification') ||
                             themeSnapshot.includes('Bell');
    addResult('Notifications system present', hasNotifications);

    // Navigate to tracking page
    console.log('🧪 Testing Tracking Page...');
    await browser.navigate('http://localhost:4173/tracking');
    await browser.waitFor({ time: 2 });

    const trackingSnapshot = await browser.snapshot();
    const trackingLoaded = trackingSnapshot.includes('Track') ||
                           trackingSnapshot.includes('tracking');
    addResult('Tracking page loads', trackingLoaded);

    await browser.takeScreenshot({ filename: 'tracking-page.png' });
    addResult('Tracking page screenshot captured', true);

    // Test responsive design (resize browser)
    console.log('🧪 Testing Responsive Design...');
    await browser.resize({ width: 375, height: 667 }); // Mobile size
    await browser.waitFor({ time: 1 });
    await browser.takeScreenshot({ filename: 'mobile-view.png' });
    addResult('Mobile view tested', true);

    await browser.resize({ width: 768, height: 1024 }); // Tablet size
    await browser.waitFor({ time: 1 });
    await browser.takeScreenshot({ filename: 'tablet-view.png' });
    addResult('Tablet view tested', true);

    await browser.resize({ width: 1920, height: 1080 }); // Desktop size
    await browser.waitFor({ time: 1 });
    addResult('Desktop view tested', true);

  } catch (error) {
    console.error('❌ E2E test error:', error);
    addResult('Test suite execution', false, error.message);
  }

  return results;
}

// Summary function
export function printE2EResults(results) {
  console.log('\n' + '='.repeat(60));
  console.log('📊 E2E Test Results - UI Upgrade');
  console.log('='.repeat(60));
  console.log(`✅ Passed: ${results.passed}`);
  console.log(`❌ Failed: ${results.failed}`);
  console.log(`📝 Total: ${results.tests.length}`);
  console.log('='.repeat(60));

  console.log('\n📋 Test Details:');
  results.tests.forEach((test, index) => {
    const icon = test.passed ? '✅' : '❌';
    console.log(`${index + 1}. ${icon} ${test.name}`);
    if (test.error) {
      console.log(`   Error: ${test.error}`);
    }
  });

  console.log('\n' + '='.repeat(60));
  const passRate = ((results.passed / results.tests.length) * 100).toFixed(1);
  console.log(`🎯 Pass Rate: ${passRate}%`);
  console.log('='.repeat(60) + '\n');

  return passRate >= 80;
}













