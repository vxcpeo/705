# Reskin verification — PASS

Generated: 2026-10-22T15:40:28.643Z

- Project: **tabuline-website**
- URL: http://127.0.0.1:4317/
- Original skeleton: `sidebar-workspace` (shell)
- New skeleton: `terminal-console` (linear)
- Accent: #298dff -> #0000d6 (72.06 ΔE; min 30)
- Source contract: intact (`9889e37ce44b`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.307 | 0.25 | 0 | [desktop](current/home-desktop.png) |
| `/app/markets` | PASS | 0.271 | 0.2 | 0 | [desktop](current/app-markets-desktop.png) |
| `/docs` | PASS | 0.364 | 0.4 | 0 | [desktop](current/docs-desktop.png) |
| `/privacy` | PASS | 0.5 | 0.333 | 0 | [desktop](current/privacy-desktop.png) |
| `/signal` | PASS | 0.4 | 0.25 | 0 | [desktop](current/signal-desktop.png) |
| `/terms` | PASS | 0.5 | 0.333 | 0 | [desktop](current/terms-desktop.png) |

## Blocking issues

- None.

## Warnings

- attributes: "href=/" count increased 4 -> 5
- attributes: "src=/icon.svg" count increased 2 -> 3
- bindings: "interpolation:String(index + 1).padStart(2, '0')" count increased 2 -> 3
- events: "click:navigate('/')" count increased 2 -> 3
- links: "href:/" count increased 4 -> 5
- assets: "src:/icon.svg" count increased 2 -> 3
- /: aria attribute added: aria-label=Tabuline overview
- /: aria attribute added: aria-label=Terminal index
- /: link target added: /
- /app/markets: aria attribute added: aria-label=Tabuline overview
- /app/markets: aria attribute added: aria-label=Terminal index
- /app/markets: link target added: /
- /docs: aria attribute added: aria-label=Tabuline overview
- /docs: aria attribute added: aria-label=Terminal index
- /docs: link target added: /
- /privacy: numeric token count changed: 6 -> 8 (dynamic values may differ)
- /privacy: aria attribute added: aria-label=Tabuline overview
- /privacy: aria attribute added: aria-label=Terminal index
- /privacy: link target added: /
- /signal: aria attribute added: aria-label=Tabuline overview
- /signal: aria attribute added: aria-label=Terminal index
- /signal: link target added: /
- /terms: numeric token count changed: 6 -> 8 (dynamic values may differ)
- /terms: aria attribute added: aria-label=Tabuline overview
- /terms: aria attribute added: aria-label=Terminal index
- /terms: link target added: /

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
