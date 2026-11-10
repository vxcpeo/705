# Reskin verification — PASS

Generated: 2026-11-09T18:27:34.770Z

- Project: **tallyria-website**
- URL: http://127.0.0.1:4317/
- Original skeleton: `terminal-console` (linear)
- New skeleton: `bento-canvas` (spatial)
- Accent: #0000d6 -> #e6006f (103.43 ΔE; min 30)
- Source contract: intact (`9a6611056f84`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.19 | 0.5 | 0 | [desktop](current/home-desktop.png) |
| `/app/markets` | PASS | 0.283 | 0.4 | 0 | [desktop](current/app-markets-desktop.png) |
| `/docs` | PASS | 0.222 | 0.6 | 0 | [desktop](current/docs-desktop.png) |
| `/privacy` | PASS | 0.213 | 0.5 | 0 | [desktop](current/privacy-desktop.png) |
| `/signal` | PASS | 0.176 | 0.5 | 0 | [desktop](current/signal-desktop.png) |
| `/terms` | PASS | 0.213 | 0.5 | 0 | [desktop](current/terms-desktop.png) |

## Blocking issues

- None.

## Warnings

- /: aria attribute changed/removed: aria-label=Tallyria overview
- /: aria attribute changed/removed: aria-label=Terminal index
- /app/markets: aria attribute changed/removed: aria-label=Tallyria overview
- /app/markets: aria attribute changed/removed: aria-label=Terminal index
- /docs: aria attribute changed/removed: aria-label=Legacy journal anchor
- /docs: aria attribute changed/removed: aria-label=Legacy limits anchor
- /docs: aria attribute changed/removed: aria-label=Legacy overview anchor
- /docs: aria attribute changed/removed: aria-label=Legacy scenario anchor
- /docs: aria attribute changed/removed: aria-label=Tallyria overview
- /docs: aria attribute changed/removed: aria-label=Terminal index
- /privacy: aria attribute changed/removed: aria-label=Tallyria overview
- /privacy: aria attribute changed/removed: aria-label=Terminal index
- /signal: aria attribute changed/removed: aria-label=Tallyria overview
- /signal: aria attribute changed/removed: aria-label=Terminal index
- /terms: aria attribute changed/removed: aria-label=Tallyria overview
- /terms: aria attribute changed/removed: aria-label=Terminal index

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
