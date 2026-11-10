#!/usr/bin/env node
/** Capture fresh UI screenshots (page + named element crops) for the X / OG artwork. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(path.resolve('.reskin/tools/package.json'));
const { chromium } = require('playwright-core');

const BASE = process.argv[2] || 'http://127.0.0.1:4321';
const OUT = path.resolve('../twitter/ui');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

const routes = [
  ['home', '/'],
  ['markets', '/app/markets'],
  ['signal', '/signal'],
  ['docs', '/docs'],
  ['sol', '/app/markets/SOL'],
];

const crops = [
  ['home', 'home-cap', '#cap'],
  ['home', 'home-board', '.bl-board'],
  ['sol', 'sol-explorer', '#cap'],
  ['sol', 'sol-passport', '.bl-mkt-passport'],
  ['signal', 'signal-form', '.bl-lab-form'],
  ['markets', 'markets-board', '.bl-mkt-board'],
];

await fs.mkdir(OUT, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath: CHROME, args: ['--no-sandbox', '--hide-scrollbars'] });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();

for (const [slug, route] of routes) {
  await page.goto(BASE + route, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(700);
  await page.evaluate(async () => {
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    for (let y = 0; y < document.documentElement.scrollHeight; y += 700) { window.scrollTo(0, y); await sleep(60); }
    window.scrollTo(0, 0);
    await sleep(200);
    if (document.fonts?.ready) await document.fonts.ready;
  });
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.screenshot({ path: path.join(OUT, `${slug}-top-1440.png`) });
  await page.screenshot({ path: path.join(OUT, `${slug}-full.png`), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(OUT, `${slug}-top-390.png`) });
  await page.setViewportSize({ width: 1440, height: 900 });
  console.log(`${slug}: captured`);
}

for (const [routeSlug, name, selector] of crops) {
  const route = routes.find(([s]) => s === routeSlug)[1];
  await page.goto(BASE + route, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(600);
  const el = page.locator(selector).first();
  if (await el.count()) {
    await el.screenshot({ path: path.join(OUT, `${name}.png`) });
    const box = await el.boundingBox();
    console.log(`${name}: ${Math.round(box.width)}x${Math.round(box.height)}`);
  } else {
    console.log(`${name}: selector not found`);
  }
}

await browser.close();
console.log(`screenshots -> ${OUT}`);
