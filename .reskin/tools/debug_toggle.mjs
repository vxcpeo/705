import { launchChrome, openPage } from 'file:///C:/Users/Administrator/.dsh/skills/rebrand/scripts/lib/chrome.mjs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const chrome = await launchChrome({ headless: true });
const page = await openPage(chrome.cdp, { width: 1440, height: 900 });
try {
  await page.navigate('http://127.0.0.1:4319/app/markets/SOL', { timeoutMs: 30000, delayMs: 1200 });
  console.log('buttons:', await page.evaluate("[...document.querySelectorAll('button')].map(b => b.textContent.trim()).slice(0,20)"));
  console.log('has payoff section:', await page.evaluate("Boolean(document.querySelector('#cap'))"));
  console.log('tables before:', await page.evaluate("document.querySelectorAll('table').length"));
  const clicked = await page.evaluate(`(() => {
    const b = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === 'Table');
    if (!b) return 'no-table-button';
    b.click();
    return 'clicked';
  })()`);
  await sleep(600);
  console.log('click result:', clicked);
  console.log('tables after:', await page.evaluate("document.querySelectorAll('table').length"));
  console.log('body has Stock price:', (await page.bodyText()).includes('Stock price'));
} finally { await chrome.cdp.close(); await chrome.close().catch(()=>{}); }
