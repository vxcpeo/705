/**
 * Viewport screenshots for the visual review.
 *
 * verify.mjs captures full-page images; a sticky status strip is painted at its
 * stitched scroll position there. These are plain viewport captures that show
 * where the strip really sits, at 1440x900 and 390x844.
 */
import { launchChrome, openPage } from 'file:///C:/Users/Administrator/.dsh/skills/rebrand/scripts/lib/chrome.mjs';

const BASE = process.env.SMOKE_URL || 'http://127.0.0.1:4319';
const OUT = 'E:/workspace/chuangye/solana/705/website/.reskin/views';

async function main() {
  const chrome = await launchChrome({ headless: true });
  try {
    const page = await openPage(chrome.cdp, { width: 1440, height: 900 });
    const shots = [
      ['/', 'home-top-desktop', 1440, 900, 0],
      ['/', 'home-scrolled-desktop', 1440, 900, 700],
      ['/app/markets', 'markets-top-desktop', 1440, 900, 0],
      ['/docs', 'docs-top-desktop', 1440, 900, 0],
      ['/signal', 'signal-top-desktop', 1440, 900, 0],
      ['/', 'home-top-mobile', 390, 844, 0],
      ['/app/markets', 'markets-top-mobile', 390, 844, 0],
    ];
    for (const [route, name, width, height, scroll] of shots) {
      await page.navigate(`${BASE}${route}`, { timeoutMs: 30000, delayMs: 700 });
      await page.evaluate(`window.scrollTo(0, ${scroll})`);
      await page.setViewport(width, height, width < 600);
      await new Promise((r) => setTimeout(r, 350));
      await page.screenshot(`${OUT}/${name}.png`, { width, height });
      console.log('captured', name);
    }
    await page.close();
  } finally {
    await chrome.cdp.close();
    await chrome.close().catch(() => {});
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
