# Reskin verification — PASS

Generated: 2026-10-21T13:29:53.311Z

- Project: **librova-website**
- URL: http://127.0.0.1:4317/
- Original skeleton: `terminal-console` (linear)
- New skeleton: `sidebar-workspace` (shell)
- Accent: #ff0000 -> #298dff (148.1 ΔE; min 30)
- Source contract: intact (`3d00ded2cdd4`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.17 | 0.25 | 0 | [desktop](current/home-desktop.png) |
| `/app/markets` | PASS | 0.188 | 0.25 | 0 | [desktop](current/app-markets-desktop.png) |
| `/docs` | PASS | 0.267 | 0.5 | 0 | [desktop](current/docs-desktop.png) |
| `/privacy` | PASS | 0.274 | 0.333 | 0 | [desktop](current/privacy-desktop.png) |
| `/signal` | PASS | 0.277 | 0.333 | 0 | [desktop](current/signal-desktop.png) |
| `/terms` | PASS | 0.274 | 0.333 | 0 | [desktop](current/terms-desktop.png) |

## Blocking issues

- None.

## Warnings

- /: aria attribute changed/removed: aria-label=Build status
- /app/markets: aria attribute changed/removed: aria-label=Build status
- /app/markets: aria attribute added: aria-label=Market facts
- /docs: aria attribute changed/removed: aria-label=Build status
- /privacy: aria attribute changed/removed: aria-label=Build status
- /signal: aria attribute changed/removed: aria-label=Build status
- /terms: aria attribute changed/removed: aria-label=Build status

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
