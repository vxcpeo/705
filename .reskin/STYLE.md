# Reskin art direction — Cosmos Orbit

> Selected automatically. Do not ask the user to confirm or choose another direction.

- **Style DNA:** `cosmos-orbit` (spatial-futurist)
- **Skeleton:** `gallery-scroll` (spatial)
- **Seed:** `a31479cb05406a384e482c52f20f948b703e77df221cf9903b785586a52a13a6`
- **Source DNA:** [https://cosmos.network](https://cosmos.network)
- **Live sampled:** yes — https://cosmos.network (2350 ms)
- **Original:** sidebar-workspace / light / accent #b26a00

## Why this direction

The selector sampled 9/10 blockchain references, scored every direction for perceptual distance from the original accent (#b26a00) and background (#ffffff), added a deterministic seed jitter, and chose Cosmos Orbit because it is 112 ΔE away from the original accent and pairs with Gallery Scroll, a spatial skeleton rather than the original sidebar-workspace.

## Live reference sampling

| Style | URL | Result | Accent sampled | Ground sampled |
|---|---|---|---|---|
| ethereum-paper | https://ethereum.org | ok (863 ms) | #0c5681 | #ffffff |
| polygon-agora | https://polygon.technology | ok (1461 ms) | #670de5 | #000000 |
| base-cobalt | https://www.base.org | ok (2497 ms) | #0000ff | #dde3e9 |
| solana-spectrum | https://solana.com | ok (2721 ms) | #9945ff | #000000 |
| arbitrum-signal | https://arbitrum.io | failed: HTTP 403 | — | — |
| optimism-poster | https://www.optimism.io | ok (2237 ms) | #ff0421 | #fafaf9 |
| aave-abyss | https://aave.com | ok (1621 ms) | #ff0000 | #000000 |
| uniswap-bubblegum | https://uniswap.org | ok (2576 ms) | — | #ffffff |
| cosmos-orbit | https://cosmos.network | ok (2350 ms) | #40b3ff | #000000 |
| sui-tidal | https://sui.io | ok (2360 ms) | #298dff | #ffffff |

Live sampling is evidence, not a copy target. Never download or reuse a reference site's logo, imagery, copy, or code. Use only the abstract tokens below.

## Candidate ranking

| Candidate | Score | Accent ΔE from original | Layout | Live |
|---|---:|---:|---|---|
| Cosmos Orbit | 0.9976 | 111.5 | gallery-scroll | yes |
| Agora Violet | 0.9757 | 144.5 | orbital | yes |
| Signal Navy | 0.9543 | 102.5 | bento-canvas | no |
| Tidal Sui | 0.9099 | 124.1 | gallery-scroll | yes |
| Abyss Liquidity | 0.9069 | 58.1 | orbital | yes |
| Spectrum Terminal | 0.8301 | 145.3 | terminal-console | yes |
| Bubblegum Exchange | 0.8294 | 71.7 | orbital | yes |
| Cobalt Blueprint | 0.7809 | 177.3 | bento-canvas | yes |
| Paper Protocol | 0.7522 | 94.6 | gallery-scroll | yes |
| Poster Optimism | 0.688 | 51 | ticker-stage | yes |

## Skeleton brief

**Gallery Scroll** — full-viewport panels with generous negative space; horizontal scroll-snap for related panels; minimal floating dock navigation; each route is a sequence of framed scenes; large imagery/typography and very few borders.

Navigation: Floating dock at the bottom (icons + accessible names) and a vertical dot index for sections; no conventional header.

Structure:
1. opening panel with brand and route count
1. scene panels with snap points
1. horizontal data rail
1. closing panel with form/action
1. floating dock

Content mapping: Group each route's content into 2-4 scenes. Keep metrics as large typographic facts. Tables become horizontal snap rails with one record per panel on mobile. Forms become the closing scene.

Recipe: `.scene{min-height:100svh;display:grid;place-content:center;padding:clamp(24px,6vw,96px);scroll-snap-align:start}.rail{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:16px}.rail>*{scroll-snap-align:start;flex:0 0 min(86vw,520px)}.dock{position:fixed;bottom:18px;left:50%;translate:-50% 0;display:flex;gap:6px;border-radius:999px}`

Risks: full-viewport panels can hide content below the fold; provide visible scroll cues; horizontal rails need keyboard and touch support

## Design tokens

```css
:root {
  --bg: #000000;
  --surface: #12121E;
  --surface-alt: #191927;
  --ink: #F5F4FA;
  --muted: #9A98AD;
  --accent: #40b3ff;
  --accent-safe: #40b3ff;
  --accent-2: #A78BFA;
  --line: #262536;
  --success: #5CE1A0;
  --danger: #FF8A8A;
  --warning: #F2C94C;

  --font-display: "Century Gothic", "Futura", "Segoe UI", sans-serif;
  --font-body: "Segoe UI", "Helvetica Neue", sans-serif;
  --font-mono: "Cascadia Mono", ui-monospace, monospace;
  --display-weight: 400;
  --display-tracking: 0.02em;
  --label-tracking: 0.24em;

  --radius-sm: 999px;
  --radius-md: 999px;
  --radius-lg: 28px;
  --border: 1px solid var(--line);
  --shadow: 0 0 60px rgba(110, 123, 255, 0.16);

  --motion-duration: 420ms;
  --motion-ease: cubic-bezier(.16,1,.3,1);
  --space-1: clamp(4px, .35vw, 6px);
  --space-2: clamp(8px, .7vw, 12px);
  --space-3: clamp(14px, 1.2vw, 20px);
  --space-4: clamp(22px, 2vw, 32px);
  --space-5: clamp(36px, 3.4vw, 56px);
  --space-6: clamp(56px, 5vw, 88px);
  --page-pad: clamp(18px, 4vw, 64px);
  --max-width: 1440px;
}
```

## Component grammar

- Surface: 1px solid var(--line); radius 999px; shadow 0 0 60px rgba(110, 123, 255, 0.16).
- Type: display **"Century Gothic", "Futura", "Segoe UI", sans-serif** at weight 400, tracking 0.02em; body **"Segoe UI", "Helvetica Neue", sans-serif**; numerals and micro-labels **"Cascadia Mono", ui-monospace, monospace**.
- Texture: orbital rings, star fields, thin constellation lines, radial glows.
- Motion: slow-orbit, 420ms, cubic-bezier(.16,1,.3,1). Always wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.
- Density: airy. Keep body text >= 14px and body contrast >= 4.5:1.
- Use `--accent-safe` for text and icons on `--bg`; use `--accent` for fills and large shapes.

## Originality guard

The replacement must satisfy all of these:

1. The source inventory archetype is `sidebar-workspace`; the new skeleton is `gallery-scroll`. Do not fall back to the old shell during implementation.
2. Do not reuse any original class name, CSS selector, design token name, or original accent family.
3. Rewrite templates, not only CSS. Every route must visibly use the new skeleton.
4. Keep every token in `.reskin/content-contract.json`; move it, never rewrite it.
5. Run `node scripts/verify.mjs check` and do not stop until content, structure, accessibility and responsive checks pass.

## Commit statement

Use this sentence in the final report: "The UI was rebuilt around Cosmos Orbit / Gallery Scroll; the original sidebar-workspace shell and palette were removed while the content contract stayed byte-for-byte intact."
