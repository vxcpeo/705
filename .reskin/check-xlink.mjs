#!/usr/bin/env node
/** Verify the footer's outbound X link, the head metadata and the absence of stale targets. */
import path from 'node:path'
import fs from 'node:fs/promises'
import { createRequire } from 'node:module'

const require = createRequire(path.resolve('.reskin/tools/package.json'))
const { chromium } = require('playwright-core')

const BASE = process.argv[2] || 'http://127.0.0.1:4501'
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
const OUT = '.reskin/xlink'
const ROUTES = ['/', '/app/markets', '/signal', '/docs', '/risk']
const EXPECTED = {
  href: 'https://x.com/tallyria_top',
  text: '@tallyria_top',
  domain: 'tallyria.top',
  site: '@tallyria_top',
}

const browser = await chromium.launch({
  headless: true,
  executablePath: CHROME,
  args: ['--no-sandbox', '--hide-scrollbars'],
})
await fs.mkdir(OUT, { recursive: true })
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } })
const page = await context.newPage()
const errors = []
page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()) })
page.on('pageerror', (error) => errors.push(error.message))

const results = []
for (const route of ROUTES) {
  await page.goto(BASE + route, { waitUntil: 'networkidle', timeout: 30000 })
  await page.evaluate(() => document.fonts?.ready)
  const found = await page.locator('footer a[href^="https://x.com/"]').evaluateAll((links) =>
    links.map((link) => ({
      href: link.href,
      text: link.textContent.replace(/\s+/g, ' ').trim(),
      target: link.target,
      rel: link.rel,
      aria: link.getAttribute('aria-label'),
      visible: Boolean(link.offsetWidth || link.offsetHeight),
    })))
  const stale = await page.evaluate(() => {
    const body = document.body.innerText
    const head = document.head.innerHTML
    return {
      body: body.match(/tallyria\.xyz|@tallyria(?!_top)/gi) || [],
      head: head.match(/tallyria\.xyz|@tallyria(?!_top)/gi) || [],
    }
  })
  results.push({ route, found, stale })
}

await page.goto(BASE + '/', { waitUntil: 'networkidle' })
const meta = await page.evaluate(() => ({
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  relMe: document.querySelector('link[rel="me"]')?.href,
  ogUrl: document.querySelector('meta[property="og:url"]')?.content,
  ogImage: document.querySelector('meta[property="og:image"]')?.content,
  twitterSite: document.querySelector('meta[name="twitter:site"]')?.content,
  twitterCreator: document.querySelector('meta[name="twitter:creator"]')?.content,
  twitterImage: document.querySelector('meta[name="twitter:image"]')?.content,
}))
const footerCopy = await page.locator('.bl-colophon-copy').innerText()
const targetsCopy = await page.locator('.bl-targets').innerText()

await page.locator('footer').scrollIntoViewIfNeeded()
await page.waitForTimeout(400)
await page.locator('footer').screenshot({ path: `${OUT}/footer-1440.png` })

await page.setViewportSize({ width: 390, height: 844 })
await page.waitForTimeout(300)
await page.locator('footer').scrollIntoViewIfNeeded()
await page.waitForTimeout(400)
await page.locator('footer').screenshot({ path: `${OUT}/footer-390.png` })

await browser.close()

let failures = 0
const check = (ok, label) => {
  if (!ok) failures += 1
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${label}`)
}

for (const { route, found, stale } of results) {
  const link = found[0]
  check(found.length === 1, `${route}: exactly one outbound X link (found ${found.length})`)
  check(link?.href === EXPECTED.href, `${route}: href ${link?.href}`)
  check(link?.text.includes(EXPECTED.text), `${route}: visible label "${link?.text}"`)
  check(link?.target === '_blank', `${route}: opens in a new tab`)
  check(/noopener/.test(link?.rel || '') && /noreferrer/.test(link?.rel || ''), `${route}: rel ${link?.rel}`)
  check(link?.visible === true, `${route}: link is rendered`)
  check(link?.aria?.includes(EXPECTED.text), `${route}: aria-label "${link?.aria}"`)
  check(stale.body.length === 0, `${route}: no stale targets in body ${stale.body.join(', ')}`)
  check(stale.head.length === 0, `${route}: no stale targets in head ${stale.head.join(', ')}`)
}
check(meta.canonical === 'https://tallyria.top/', `canonical ${meta.canonical}`)
check(meta.relMe === EXPECTED.href, `rel=me ${meta.relMe}`)
check(meta.ogUrl === 'https://tallyria.top/', `og:url ${meta.ogUrl}`)
check(meta.ogImage === 'https://tallyria.top/og-image.jpg', `og:image ${meta.ogImage}`)
check(meta.twitterSite === EXPECTED.site, `twitter:site ${meta.twitterSite}`)
check(meta.twitterCreator === EXPECTED.site, `twitter:creator ${meta.twitterCreator}`)
check(meta.twitterImage === 'https://tallyria.top/og-image.jpg', `twitter:image ${meta.twitterImage}`)
check(footerCopy.includes(EXPECTED.domain) && footerCopy.includes(EXPECTED.text), `colophon "${footerCopy}"`)
check(targetsCopy === EXPECTED.domain, `footer domain "${targetsCopy}"`)
check(errors.length === 0, `no console/page errors ${errors.join(' | ')}`)

console.log(`\n${failures === 0 ? 'ALL CHECKS PASS' : `${failures} CHECK(S) FAILED`}`)
process.exit(failures === 0 ? 0 : 1)
