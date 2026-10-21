# Reskin verification — PASS

Generated: 2026-10-20T15:52:57.056Z

- Project: **pretiola-website**
- URL: http://127.0.0.1:4318/
- Original skeleton: `orbital` (spatial)
- New skeleton: `terminal-console` (linear)
- Accent: #40b3ff -> #ff0000 (144.6 ΔE; min 30)
- Source contract: intact (`081faeac66dd`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.113 | 0.25 | 0 | [desktop](current/home-desktop.png) |
| `/app/markets` | PASS | 0.126 | 0.25 | 0 | [desktop](current/app-markets-desktop.png) |
| `/docs` | PASS | 0.121 | 0.4 | 0 | [desktop](current/docs-desktop.png) |
| `/privacy` | PASS | 0.118 | 0.25 | 0 | [desktop](current/privacy-desktop.png) |
| `/signal` | PASS | 0.131 | 0.25 | 0 | [desktop](current/signal-desktop.png) |
| `/terms` | PASS | 0.118 | 0.25 | 0 | [desktop](current/terms-desktop.png) |

## Blocking issues

- None.

## Warnings

- None.

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
