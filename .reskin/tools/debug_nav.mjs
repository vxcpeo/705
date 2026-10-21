import { launchChrome, openPage } from 'file:///C:/Users/Administrator/.dsh/skills/rebrand/scripts/lib/chrome.mjs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const chrome = await launchChrome({ headless: true });
const page = await openPage(chrome.cdp, { width: 390, height: 844 });
try {
  await page.navigate('http://127.0.0.1:4319/', { timeoutMs: 30000, delayMs: 900 });
  const opened = await page.evaluate(`(() => { const b=document.querySelector('.tty-command-more'); b?.click(); return Boolean(b); })()`);
  await sleep(500);
  console.log('toggle found:', opened);
  console.log('nav visible:', await page.evaluate("(() => { const n=document.querySelector('.tty-nav'); if(!n) return false; const r=n.getBoundingClientRect(); return r.width>0 && r.height>0; })()"));
  await page.screenshot('E:/workspace/chuangye/solana/705/website/.reskin/views/home-mobile-nav-open.png', { width: 390, height: 844, mobile: true });
  await page.evaluate(`document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))`);
  await sleep(300);
  console.log('nav closed after Escape:', await page.evaluate("(() => { const n=document.querySelector('.tty-nav'); const r=n?.getBoundingClientRect(); return !r || r.height===0; })()"));
} finally { await chrome.cdp.close(); await chrome.close().catch(()=>{}); }
