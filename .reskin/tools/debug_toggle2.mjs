import { launchChrome, openPage } from 'file:///C:/Users/Administrator/.dsh/skills/rebrand/scripts/lib/chrome.mjs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const chrome = await launchChrome({ headless: true });
const page = await openPage(chrome.cdp, { width: 1440, height: 900 });
try {
  await page.navigate('http://127.0.0.1:4319/app/markets/SOL', { timeoutMs: 30000, delayMs: 1200 });
  await page.evaluate(`(() => { const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='Table'); b?.click(); return true; })()`);
  await sleep(500);
  console.log(await page.evaluate("document.querySelector('table') ? document.querySelector('table').innerText.slice(0,200) : 'no table'"));
  console.log('bodyText length:', (await page.bodyText()).length);
  console.log('contains Income:', (await page.bodyText()).includes('Income'));
} finally { await chrome.cdp.close(); await chrome.close().catch(()=>{}); }
