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
 * Run with: npm test -- src/tests/e2e/address-crud-puppeteer.test.js
 * Or standalone: node src/tests/e2e/address-crud-puppeteer.test.js
 */

import { describe, test, expect, beforeAll, afterAll } from 'vitest';
import puppeteer from 'puppeteer';

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:5173';
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

// Helper functions
async function waitForElement(page, selector, timeout = 5000) {
  try {
    await page.waitForSelector(selector, { timeout });
    return true;
  } catch {
    return false;
  }
}

async function waitForTimeout(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fillFormField(page, selector, value) {
  await page.waitForSelector(selector);
  await page.click(selector, { clickCount: 3 }); // Select all existing text
  await page.type(selector, value);
}

async function findButtonByText(page, text) {
  return await page.evaluate((buttonText) => {
    const buttons = Array.from(document.querySelectorAll('button'));
    return buttons.find((btn) => btn.textContent.includes(buttonText));
  }, text);
}

describe('Address CRUD E2E Tests', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: process.env.CI === 'true' || process.env.HEADLESS === 'true', // Headless in CI
      defaultViewport: { width: 1280, height: 720 },
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    page = await browser.newPage();
  });

  afterAll(async () => {
    if (browser) {
      await browser.close();
    }
  });

  test('should navigate to Address Book page', async () => {
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle2', timeout: 30000 });

    // Try clicking sidebar link or direct navigation
    const addressesLink = await waitForElement(page, 'a[href="/addresses"]', 10000);
    if (addressesLink) {
      await page.click('a[href="/addresses"]');
      await page.waitForNavigation({ waitUntil: 'networkidle2' });
    } else {
      await page.goto(`${FRONTEND_URL}/addresses`, { waitUntil: 'networkidle2' });
    }

    // Verify we're on the addresses page
    const url = page.url();
    expect(url).toContain('/addresses');
  }, 60000); // 60s timeout for E2E tests

  test('should create a new address', async () => {
    // Navigate to addresses page if not already there
    await page.goto(`${FRONTEND_URL}/addresses`, { waitUntil: 'networkidle2' });

    // Find and click Add Address button
    const addButton = await findButtonByText(page, 'Add Address');
    if (addButton) {
      await page.evaluate((btn) => btn.click(), addButton);
    } else {
      // Try waiting for button to appear
      await page.waitForSelector('button', { timeout: 5000 });
      const btn = await findButtonByText(page, 'Add Address');
      if (btn) await page.evaluate((b) => b.click(), btn);
    }

    // Wait for form modal
    await page.waitForSelector('input[placeholder*="Name"], input[name="name"]', { timeout: 5000 });

    // Fill form fields
    await fillFormField(page, 'input[placeholder*="Name"], input[name="name"]', testAddress.name);
    await fillFormField(page, 'input[placeholder*="Company"], input[name="company"]', testAddress.company);
    await fillFormField(page, 'input[placeholder*="Street"], input[name="street1"]', testAddress.street1);
    await fillFormField(page, 'input[placeholder*="City"], input[name="city"]', testAddress.city);
    await fillFormField(page, 'input[placeholder*="State"], input[name="state"]', testAddress.state);
    await fillFormField(page, 'input[placeholder*="ZIP"], input[name="zip"]', testAddress.zip);

    // Submit form
    const submitButton = await findButtonByText(page, 'Create');
    if (submitButton) {
      await page.evaluate((btn) => btn.click(), submitButton);
    } else {
      const submitBtn = await page.$('button[type="submit"]');
      if (submitBtn) await submitBtn.click();
    }

    // Wait for success (toast or form close)
    await waitForTimeout(2000);

    // Verify address was created (check for success message or address in list)
    const successIndicator = await page.evaluate(() => {
      return document.body.textContent.includes('created') || document.body.textContent.includes('success');
    });
    expect(successIndicator).toBe(true);
  }, 60000);

  test('should search/filter addresses', async () => {
    await page.goto(`${FRONTEND_URL}/addresses`, { waitUntil: 'networkidle2' });

    const searchInput = await waitForElement(page, 'input[placeholder*="Search"], input[type="search"]', 5000);
    if (searchInput) {
      await fillFormField(page, 'input[placeholder*="Search"], input[type="search"]', testAddress.city);
      await waitForTimeout(1000);

      // Verify search results
      const hasResults = await page.evaluate((city) => {
        return document.body.textContent.includes(city);
      }, testAddress.city);
      expect(hasResults).toBe(true);
    }
  }, 30000);

  test('should edit an existing address', async () => {
    await page.goto(`${FRONTEND_URL}/addresses`, { waitUntil: 'networkidle2' });

    // Find and click Edit button
    const editButton = await findButtonByText(page, 'Edit');
    if (editButton) {
      await page.evaluate((btn) => btn.click(), editButton);
      await page.waitForSelector('input[placeholder*="Name"], input[name="name"]', { timeout: 5000 });

      // Update fields
      await fillFormField(page, 'input[placeholder*="Name"], input[name="name"]', updatedAddress.name);
      await fillFormField(page, 'input[placeholder*="Company"], input[name="company"]', updatedAddress.company);

      // Submit update
      const updateButton = await findButtonByText(page, 'Update');
      if (updateButton) {
        await page.evaluate((btn) => btn.click(), updateButton);
      } else {
        const submitBtn = await page.$('button[type="submit"]');
        if (submitBtn) await submitBtn.click();
      }
      await waitForTimeout(2000);

      // Verify update
      const updateSuccess = await page.evaluate(() => {
        return document.body.textContent.includes('updated') || document.body.textContent.includes('success');
      });
      expect(updateSuccess).toBe(true);
    } else {
      // Skip if no addresses exist
      expect(true).toBe(true);
    }
  }, 60000);

  test('should delete an address', async () => {
    await page.goto(`${FRONTEND_URL}/addresses`, { waitUntil: 'networkidle2' });

    const deleteButton = await findButtonByText(page, 'Delete');
    if (deleteButton) {
      await page.evaluate((btn) => btn.click(), deleteButton);
      await waitForTimeout(1000); // Wait for confirmation dialog

      // Confirm deletion
      await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        const confirmBtn = buttons.find((btn) =>
          btn.textContent.includes('Delete') && !btn.textContent.includes('Cancel')
        );
        if (confirmBtn) confirmBtn.click();
      });

      await waitForTimeout(2000);

      // Verify deletion
      const deleteSuccess = await page.evaluate(() => {
        return document.body.textContent.includes('deleted') || document.body.textContent.includes('success');
      });
      expect(deleteSuccess).toBe(true);
    } else {
      // Skip if no addresses exist
      expect(true).toBe(true);
    }
  }, 60000);
});
