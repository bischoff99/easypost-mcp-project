/**
 * Simplified Frontend Automated Tests using Puppeteer
 *
 * Quick smoke tests to verify frontend pages load correctly
 */

import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdir } from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:80';
const SCREENSHOT_DIR = join(__dirname, '../../../test-screenshots');

await mkdir(SCREENSHOT_DIR, { recursive: true });

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function testPage(page, name, url, expectedText) {
  console.log(`\n📄 Testing ${name}...`);
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await wait(2000);

    const content = await page.evaluate((expected) => {
      return {
        loaded: document.readyState === 'complete',
        hasRoot: document.getElementById('root') !== null,
        hasText: document.body.textContent.includes(expected),
        title: document.title
      };
    }, expectedText);

    await page.screenshot({ path: join(SCREENSHOT_DIR, `${name.toLowerCase().replace(/\s+/g, '-')}.png`) });

    console.log(`✅ ${name}:`, content.hasText ? 'PASS' : 'FAIL');
    return content.hasText;
  } catch (error) {
    console.error(`❌ ${name} failed:`, error.message);
    return false;
  }
}

async function runTests() {
  console.log('🚀 Starting Frontend Automated Tests...');
  console.log(`Frontend URL: ${FRONTEND_URL}`);
  console.log(`Screenshots: ${SCREENSHOT_DIR}\n`);

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      defaultViewport: { width: 1280, height: 720 },
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    });

    const page = await browser.newPage();
    page.setDefaultTimeout(15000);
    page.setDefaultNavigationTimeout(15000);

    const results = {
      dashboard: await testPage(page, 'Dashboard', FRONTEND_URL, 'Dashboard'),
      shipments: await testPage(page, 'Shipments', `${FRONTEND_URL}/shipments`, 'Shipments'),
      tracking: await testPage(page, 'Tracking', `${FRONTEND_URL}/tracking`, 'Tracking'),
      analytics: await testPage(page, 'Analytics', `${FRONTEND_URL}/analytics`, 'Analytics'),
    };

    console.log('\n' + '='.repeat(60));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(60));
    Object.entries(results).forEach(([name, passed]) => {
      console.log(`${passed ? '✅' : '❌'} ${name}: ${passed ? 'PASS' : 'FAIL'}`);
    });
    console.log('='.repeat(60));

    const allPassed = Object.values(results).every(r => r);
    console.log(`\n${allPassed ? '🎉 All tests passed!' : '⚠️  Some tests failed'}`);
    console.log(`📸 Screenshots saved to: ${SCREENSHOT_DIR}`);

    return allPassed ? 0 : 1;
  } catch (error) {
    console.error('\n❌ Test suite failed:', error.message);
    return 1;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// Run with timeout
const timeout = setTimeout(() => {
  console.error('\n❌ Test suite timed out');
  process.exit(1);
}, 60000); // 1 minute timeout

runTests()
  .then(exitCode => {
    clearTimeout(timeout);
    process.exit(exitCode);
  })
  .catch(error => {
    clearTimeout(timeout);
    console.error('Unhandled error:', error);
    process.exit(1);
  });
