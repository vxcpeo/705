# Reskin verification — PASS

Generated: 2026-10-19T19:09:13.956Z

- Project: **filza-website**
- URL: http://127.0.0.1:4318/
- Original skeleton: `sidebar-workspace` (shell)
- New skeleton: `orbital` (spatial)
- Accent: #b26a00 -> #40b3ff (111.47 ΔE; min 30)
- Source contract: intact (`3a7f596d88ba`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.392 | 0.429 | 0 | [desktop](current/home-desktop.png) |
| `/app/markets` | PASS | 0.309 | 0.5 | 0 | [desktop](current/app-markets-desktop.png) |
| `/docs` | PASS | 0.224 | 0.571 | 0 | [desktop](current/docs-desktop.png) |
| `/privacy` | PASS | 0.343 | 0.5 | 0 | [desktop](current/privacy-desktop.png) |
| `/signal` | PASS | 0.383 | 0.429 | 0 | [desktop](current/signal-desktop.png) |
| `/terms` | PASS | 0.343 | 0.5 | 0 | [desktop](current/terms-desktop.png) |

## Blocking issues

- None.

## Warnings

- /: aria attribute changed/removed: aria-label=Filza navigation
- /: aria attribute changed/removed: aria-label=Site links
- /app/markets: aria attribute changed/removed: aria-label=Filza navigation
- /app/markets: aria attribute changed/removed: aria-label=Site links
- /docs: aria attribute changed/removed: aria-label=Filza navigation
- /docs: aria attribute changed/removed: aria-label=Site links
- /privacy: aria attribute changed/removed: aria-label=Filza navigation
- /privacy: aria attribute changed/removed: aria-label=Site links
- /signal: aria attribute changed/removed: aria-label=Filza navigation
- /signal: aria attribute changed/removed: aria-label=Site links
- /terms: aria attribute changed/removed: aria-label=Filza navigation
- /terms: aria attribute changed/removed: aria-label=Site links

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
