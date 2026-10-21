/**
 * Interactive smoke test for the reskinned console.
 *
 * Drives the production preview through the rebrand skill's zero-dependency CDP
 * driver: route navigation, the scenario form -> review -> journal flow, the
 * wallet dialog open/close, and the board filter. Prints a JSON verdict.
 */
import { launchChrome, openPage } from 'file:///C:/Users/Administrator/.dsh/skills/rebrand/scripts/lib/chrome.mjs';

const BASE = process.env.SMOKE_URL || 'http://127.0.0.1:4319';
const results = [];
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function record(name, ok, detail = '') {
  results.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ` 鈥?${detail}` : ''}`);
}

async function main() {
  const chrome = await launchChrome({ headless: true });
  const cdp = chrome.cdp;
  try {
    const page = await openPage(cdp, { width: 1440, height: 900 });

    await page.navigate(`${BASE}/signal`, { timeoutMs: 30000, delayMs: 900 });
    record('signal route loads', (await page.title()).includes('Journal'));

    const filled = await page.evaluate(`(() => {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      const amount = document.querySelector('#amount');
      const price = document.querySelector('#base-price');
      const note = document.querySelector('#note');
      if (!amount || !price || !note) return false;
      setter.call(amount, '2500');
      amount.dispatchEvent(new Event('input', { bubbles: true }));
      setter.call(price, '1.25');
      price.dispatchEvent(new Event('input', { bubbles: true }));
      const noteSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
      noteSetter.call(note, 'Smoke test assumption.');
      note.dispatchEvent(new Event('input', { bubbles: true }));
      return true;
    })()`);
    record('scenario inputs accept values', filled);

    const submitted = await page.evaluate(`(() => {
      const button = document.querySelector('form button[type="submit"]');
      if (!button) return false;
      button.click();
      return true;
    })()`);
    await sleep(700);
    const reviewText = await page.bodyText();
    record('review step renders', submitted && reviewText.includes('Check the numbers.'));

    await page.evaluate(`(() => {
      const button = [...document.querySelectorAll('button')].find((b) => b.textContent.includes('Save to journal'));
      button?.click();
      return Boolean(button);
    })()`);
    await sleep(700);
    const journalText = await page.bodyText();
    record('journal step renders', journalText.includes('Your local record.'));

    await page.navigate(`${BASE}/`, { timeoutMs: 30000, delayMs: 700 });
    const homeText = await page.bodyText();
    record('home renders the console shell', homeText.includes('The board') && homeText.includes('Unit quote'));

    await page.evaluate(`(() => {
      const link = [...document.querySelectorAll('nav a')].find((a) => a.getAttribute('href') === '/app/markets');
      link?.click();
      return Boolean(link);
    })()`);
    await sleep(900);
    const pathname = await page.evaluate('location.pathname');
    const boardText = await page.bodyText();
    record('rail navigation reaches the board', pathname === '/app/markets' && boardText.includes('Market quotes'));

    await page.evaluate(`(() => {
      const input = document.querySelector('input[placeholder="Search token or market"]');
      if (!input) return false;
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(input, 'zzz');
      input.dispatchEvent(new Event('input', { bubbles: true }));
      return true;
    })()`);
    await sleep(600);
    const emptyText = await page.bodyText();
    record('board search shows the empty state', emptyText.includes('No model markets match'));

    await page.evaluate(`(() => {
      const reset = [...document.querySelectorAll('button')].find((b) => b.textContent.includes('Reset search'));
      reset?.click();
      return Boolean(reset);
    })()`);
    await sleep(500);

    await page.evaluate(`(() => {
      const trigger = [...document.querySelectorAll('button')].find((b) => /Connect wallet|Choose a wallet/.test(b.textContent));
      trigger?.click();
      return Boolean(trigger);
    })()`);
    await sleep(700);
    const dialogOpen = await page.evaluate("Boolean(document.querySelector('[role=\"dialog\"][aria-modal=\"true\"]'))");
    record('wallet dialog opens', dialogOpen);

    await page.evaluate(`(() => {
      const close = document.querySelector('button[aria-label="Close wallet dialog"]');
      close?.click();
      return Boolean(close);
    })()`);
    await sleep(600);
    const dialogClosed = await page.evaluate("!document.querySelector('[role=\"dialog\"][aria-modal=\"true\"]')");
    record('wallet dialog closes', dialogClosed);

    // Filter toggle + chart/table toggle on the detail route.
    await page.navigate(`${BASE}/app/markets/SOL`, { timeoutMs: 30000, delayMs: 900 });
    const detailText = await page.bodyText();
    record('asset detail route renders', detailText.includes('SOL / Solana') && detailText.includes('A defined level.'));

    const toggled = await page.evaluate(`(() => {
      const toggle = [...document.querySelectorAll('button')].find((b) => b.textContent.trim() === 'Table');
      toggle?.click();
      return Boolean(toggle);
    })()`);
    await sleep(500);
    const tableShown = await page.bodyText();
    record('payoff chart/table toggle works', toggled && tableShown.toLowerCase().includes('stock price'));

    await page.close();
  } finally {
    await cdp.close();
    await chrome.close().catch(() => {});
  }
  const failed = results.filter((r) => !r.ok);
  console.log(JSON.stringify({ ok: failed.length === 0, results }, null, 2));
  process.exit(failed.length === 0 ? 0 : 1);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

