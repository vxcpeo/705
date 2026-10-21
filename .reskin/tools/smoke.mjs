import { launchChrome, openPage, sleep } from 'file:///C:/Users/Administrator/.dsh/skills/rebrand/scripts/lib/chrome.mjs';

const base = process.env.PREVIEW || 'http://127.0.0.1:4322';
const results = [];
const check = (name, ok, detail = '') => results.push({ name, ok, detail });

const browser = await launchChrome({ headless: true });
const page = await openPage(browser.cdp, { width: 1440, height: 900 });
const run = (js) => page.evaluate(`(() => { ${js} })()`);

try {
  // 1. scenario lab: fill, review, save
  await page.navigate(base + '/signal', { timeoutMs: 30000, delayMs: 800 });
  await run(`
    const set = (id, v) => { const el = document.querySelector(id); const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set; s.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); };
    set('#amount', '1000'); set('#base-price', '1.00'); set('#move-text', '-15');
    return true;
  `);
  await run(`
    const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim().startsWith('Review scenario'));
    if (btn) btn.click(); return Boolean(btn);
  `);
  await sleep(400);
  const reviewText = await page.bodyText();
  check('/signal review', reviewText.includes('Check the numbers.'));

  await run(`
    const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim().startsWith('Save to journal'));
    if (btn) btn.click(); return Boolean(btn);
  `);
  await sleep(400);
  const journalText = await page.bodyText();
  check('/signal save', journalText.includes('Your local record.') && journalText.includes('Export JSON'));

  // 2. wallet dialog opens and closes
  await page.navigate(base + '/', { timeoutMs: 30000, delayMs: 800 });
  await run(`
    const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim().startsWith('Connect wallet'));
    if (btn) btn.click(); return Boolean(btn);
  `);
  await sleep(500);
  const dialogOpen = await run(`return Boolean(document.querySelector('[role="dialog"]'));`);
  check('wallet dialog opens', dialogOpen === true);
  await run(`
    const btn = document.querySelector('[aria-label="Close wallet dialog"]');
    if (btn) btn.click(); return Boolean(btn);
  `);
  await sleep(300);
  const dialogClosed = await run(`return !document.querySelector('[role="dialog"]');`);
  check('wallet dialog closes', dialogClosed === true);

  // 3. home board search empty state and reset
  await run(`
    const el = document.querySelector('input[type="search"]');
    const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
    s.call(el, 'zzzz'); el.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  `);
  await sleep(300);
  const emptyText = await page.bodyText();
  const homeSearch = await run(`const el = document.querySelector('input[type="search"]'); return el ? el.value : 'MISSING';`);
  check('board empty state', emptyText.includes('zzzz') && /clear filter/i.test(emptyText), JSON.stringify({ homeSearch, snippet: emptyText.split('\n').filter((l) => l.includes('Nothing') || l.includes('zzzz')).slice(0, 2) }));
  await run(`
    const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Clear filter');
    if (btn) btn.click(); return Boolean(btn);
  `);
  await sleep(300);
  const resetText = await page.bodyText();
  check('board reset', resetText.includes('USDC') && !resetText.includes('No model markets'));

  // 4. rail navigation reaches the market desk
  await run(`
    const link = [...document.querySelectorAll('nav a')].find(a => a.textContent.includes('Board'));
    if (link) link.click(); return Boolean(link);
  `);
  await sleep(500);
  const marketText = await page.bodyText();
  const marketPath = await page.evaluate('location.pathname');
  check('rail navigation', marketText.includes('Market quotes') && marketPath === '/app/markets', marketPath);

  // 5. payoff table toggle on the detail route
  await page.navigate(base + '/app/markets/SOL', { timeoutMs: 30000, delayMs: 800 });
  await run(`
    const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Table');
    if (btn) btn.click(); return Boolean(btn);
  `);
  await sleep(400);
  const tableText = await page.bodyText();
  const toggleState = await run(`
    const btn = [...document.querySelectorAll('button')].find(b => ['Table','Chart'].includes(b.textContent.trim()));
    return JSON.stringify({ path: location.pathname, btn: btn ? btn.textContent.trim() : null, pressed: btn ? btn.getAttribute('aria-pressed') : null, tables: document.querySelectorAll('table').length, hasStock: document.body.innerText.includes('Stock price'), tableText: document.querySelector('table') ? document.querySelector('table').textContent.slice(0,120) : null });
  `);
  check('payoff table toggle', /stock price/i.test(tableText) && /current/i.test(tableText), toggleState);

  // 6. no console errors on the checked routes
  const errors = page.consoleErrors || [];
  check('no console errors', errors.length === 0, JSON.stringify(errors.slice(0, 2)));
} finally {
  await page.close();
  await browser.close();
}

for (const item of results) console.log(`${item.ok ? 'PASS' : 'FAIL'}  ${item.name}${item.detail ? '  ' + item.detail : ''}`);
console.log(results.every((r) => r.ok) ? 'SMOKE PASS' : 'SMOKE FAIL');
process.exitCode = results.every((r) => r.ok) ? 0 : 1;
