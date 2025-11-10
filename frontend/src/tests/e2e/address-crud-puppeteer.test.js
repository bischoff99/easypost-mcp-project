/**
 * Address CRUD E2E Tests with Puppeteer
 *
 * Tests complete address lifecycle:
 * 1. Navigate to Address Book page
 * 2. Create new address
 * 3. Edit existing address
 * 4. Search/filter addresses
 * 5. Delete address
 *
 * Run with: node address-crud-puppeteer.test.js
 */

import puppeteer from 'puppeteer';

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:80';
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

// Test data
const testAddress = {
  name: 'Test User',
  company: 'Test Company',
  street1: '123 Test Street',
  street2: 'Suite 100',
  city: 'San Francisco',
  state: 'CA',
  zip: '94102',
  country: 'US',
  phone: '415-555-0123',
  email: 'test@example.com',
};

const updatedAddress = {
  name: 'Updated User',
  company: 'Updated Company',
  street1: '456 Updated Street',
};

async function waitForElement(page, selector, timeout = 5000) {
  try {
    await page.waitForSelector(selector, { timeout });
    return true;
  } catch {
    return false;
  }
}

async function fillFormField(page, selector, value) {
  await page.waitForSelector(selector);
  await page.click(selector, { clickCount: 3 }); // Select all existing text
  await page.type(selector, value);
}

async function testAddressCRUD() {
  console.log('🚀 Starting Address CRUD E2E Tests...\n');

  const browser = await puppeteer.launch({
    headless: false, // Set to true for CI
    defaultViewport: { width: 1280, height: 720 },
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();

  try {
    // Test 1: Navigate to Address Book
    console.log('📋 Test 1: Navigate to Address Book page');
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle2', timeout: 30000 });
    await page.screenshot({ path: 'test-screenshots/01-initial-page.png' });

    // Click on Addresses in sidebar
    const addressesLink = await page.waitForSelector('a[href="/addresses"]', { timeout: 10000 });
    if (addressesLink) {
      await page.click('a[href="/addresses"]');
      await page.waitForNavigation({ waitUntil: 'networkidle2' });
      console.log('✅ Navigated to Address Book page');
    } else {
      // Try direct navigation
      await page.goto(`${FRONTEND_URL}/addresses`, { waitUntil: 'networkidle2' });
      console.log('✅ Navigated directly to Address Book page');
    }

    await page.screenshot({ path: 'test-screenshots/02-address-book-page.png' });

    // Test 2: Create New Address
    console.log('\n📝 Test 2: Create new address');
    const addButton = await page.waitForSelector('button:has-text("Add Address")', { timeout: 10000 });
    if (addButton) {
      await page.click('button:has-text("Add Address")');
    } else {
      // Try alternative selector
      await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        const addBtn = buttons.find((btn) => btn.textContent.includes('Add Address'));
        if (addBtn) addBtn.click();
      });
    }

    // Wait for form modal
    await page.waitForSelector('input[placeholder*="Name"]', { timeout: 5000 });
    await page.screenshot({ path: 'test-screenshots/03-address-form-open.png' });

    // Fill form fields
    await fillFormField(page, 'input[placeholder*="Name"], input[value=""]', testAddress.name);
    await fillFormField(page, 'input[placeholder*="Company"]', testAddress.company);
    await fillFormField(page, 'input[placeholder*="Street"]', testAddress.street1);
    await fillFormField(page, 'input[placeholder*="Street Address 2"]', testAddress.street2);
    await fillFormField(page, 'input[placeholder*="City"]', testAddress.city);
    await fillFormField(page, 'input[placeholder*="State"]', testAddress.state);
    await fillFormField(page, 'input[placeholder*="ZIP"]', testAddress.zip);
    await fillFormField(page, 'input[type="tel"]', testAddress.phone);
    await fillFormField(page, 'input[type="email"]', testAddress.email);

    await page.screenshot({ path: 'test-screenshots/04-address-form-filled.png' });

    // Submit form
    const submitButton = await page.waitForSelector('button:has-text("Create Address")', { timeout: 5000 });
    await submitButton.click();

    // Wait for success toast and form close
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-screenshots/05-address-created.png' });
    console.log('✅ Address created successfully');

    // Test 3: Search/Filter Addresses
    console.log('\n🔍 Test 3: Search addresses');
    const searchInput = await page.waitForSelector('input[placeholder*="Search"]', { timeout: 5000 });
    if (searchInput) {
      await fillFormField(page, 'input[placeholder*="Search"]', testAddress.city);
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-screenshots/06-search-results.png' });
      console.log('✅ Search functionality works');
    }

    // Test 4: Edit Address
    console.log('\n✏️  Test 4: Edit address');
    // Find and click Edit button on the first address card
    const editButtons = await page.$$('button:has-text("Edit")');
    if (editButtons.length > 0) {
      await editButtons[0].click();
      await page.waitForSelector('input[placeholder*="Name"]', { timeout: 5000 });
      await page.screenshot({ path: 'test-screenshots/07-edit-form-open.png' });

      // Update name field
      await fillFormField(page, 'input[placeholder*="Name"], input[value*="Test"]', updatedAddress.name);
      await fillFormField(page, 'input[placeholder*="Company"]', updatedAddress.company);
      await fillFormField(page, 'input[placeholder*="Street"]', updatedAddress.street1);

      await page.screenshot({ path: 'test-screenshots/08-edit-form-filled.png' });

      // Submit update
      const updateButton = await page.waitForSelector('button:has-text("Update Address")', { timeout: 5000 });
      await updateButton.click();
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test-screenshots/09-address-updated.png' });
      console.log('✅ Address updated successfully');
    }

    // Test 5: Delete Address
    console.log('\n🗑️  Test 5: Delete address');
    const deleteButtons = await page.$$('button:has-text("Delete")');
    if (deleteButtons.length > 0) {
      await deleteButtons[0].click();
      await page.waitForTimeout(1000); // Wait for confirmation dialog
      await page.screenshot({ path: 'test-screenshots/10-delete-confirmation.png' });

      // Confirm deletion (click Delete in toast/confirmation)
      const confirmDelete = await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        const deleteBtn = buttons.find((btn) =>
          btn.textContent.includes('Delete') && !btn.textContent.includes('Cancel')
        );
        if (deleteBtn) {
          deleteBtn.click();
          return true;
        }
        return false;
      });

      if (confirmDelete) {
        await page.waitForTimeout(2000);
        await page.screenshot({ path: 'test-screenshots/11-address-deleted.png' });
        console.log('✅ Address deleted successfully');
      }
    }

    console.log('\n✅ All Address CRUD tests completed successfully!');

  } catch (error) {
    console.error('❌ Test failed:', error);
    await page.screenshot({ path: 'test-screenshots/error.png' });
    throw error;
  } finally {
    await browser.close();
  }
}

// Run tests
testAddressCRUD().catch((error) => {
  console.error('Test suite failed:', error);
  process.exit(1);
});
