# Reskin art direction — Bubblegum Exchange

> Selected automatically. Do not ask the user to confirm or choose another direction.

- **Style DNA:** `uniswap-bubblegum` (clean-fintech)
- **Skeleton:** `bento-canvas` (spatial)
- **Seed:** `b464adc11a8dc493fd0bd869ceee31ed52bb109919e7851b70e164a511c70fde`
- **Source DNA:** [https://uniswap.org](https://uniswap.org)
- **Live sampled:** yes — https://uniswap.org (3048 ms)
- **Original:** terminal-console / light / accent #0000d6

## Why this direction

The selector sampled 8/10 blockchain references, scored every direction for perceptual distance from the original accent (#0000d6) and background (#ffffff), added a deterministic seed jitter, and chose Bubblegum Exchange because it is 101 ΔE away from the original accent and pairs with Bento Canvas, a spatial skeleton rather than the original terminal-console.

## Live reference sampling

| Style | URL | Result | Accent sampled | Ground sampled |
|---|---|---|---|---|
| solana-spectrum | https://solana.com | failed: HTTP 429 | — | — |
| base-cobalt | https://www.base.org | ok (1705 ms) | #0000ff | #dde3e9 |
| polygon-agora | https://polygon.technology | ok (1694 ms) | #670de5 | #000000 |
| ethereum-paper | https://ethereum.org | ok (2096 ms) | #0c5681 | #ffffff |
| arbitrum-signal | https://arbitrum.io | failed: HTTP 403 | — | — |
| aave-abyss | https://aave.com | ok (1596 ms) | #ff0000 | #000000 |
| uniswap-bubblegum | https://uniswap.org | ok (3048 ms) | — | #ffffff |
| cosmos-orbit | https://cosmos.network | ok (2441 ms) | #40b3ff | #000000 |
| optimism-poster | https://www.optimism.io | ok (4311 ms) | #ff0421 | #fafaf9 |
| sui-tidal | https://sui.io | ok (2601 ms) | #298dff | #ffffff |

Live sampling is evidence, not a copy target. Never download or reuse a reference site's logo, imagery, copy, or code. Use only the abstract tokens below.

## Candidate ranking

| Candidate | Score | Accent ΔE from original | Layout | Live |
|---|---:|---:|---|---|
| Bubblegum Exchange | 0.8449 | 100.6 | bento-canvas | yes |
| Cosmos Orbit | 0.8297 | 100.4 | orbital | yes |
| Abyss Liquidity | 0.8082 | 164.3 | orbital | yes |
| Poster Optimism | 0.8059 | 156.1 | documentary | yes |
| Tidal Sui | 0.7877 | 63.7 | split-stage | yes |
| Paper Protocol | 0.7835 | 98.3 | split-stage | yes |
| Signal Navy | 0.7564 | 108.3 | bento-canvas | no |
| Spectrum Terminal | 0.7493 | 78.9 | gallery-scroll | no |
| Agora Violet | 0.6553 | 29.6 | orbital | yes |
| Cobalt Blueprint | 0.6256 | 17.6 | bento-canvas | yes |

## Skeleton brief

**Bento Canvas** — no persistent sidebar; 12-column modular tile grid with mixed spans; one oversized anchor tile per page; tiles touch a shared canvas instead of sitting in a content well; navigation is a slim top index, not a full-width app bar.

Navigation: Slim top index with section names; active item is a filled chip; actions live in the hero tile or a floating corner dock.

Structure:
1. slim top index
1. oversized anchor tile (8 columns) + two stacked support tiles (4 columns)
1. three equal data tiles
1. full-bleed data band
1. thin footer line

Content mapping: Put the page's primary number or title in the anchor tile. Distribute secondary metrics into support tiles. Tables become full-bleed bands with sticky column labels. Forms become a two-column tile with the submit action in the tile footer.

Recipe: `display:grid; grid-template-columns:repeat(12,minmax(0,1fr)); gap:clamp(10px,1.2vw,18px); .tile{grid-column:span 4;border:1px solid var(--line);background:var(--surface);border-radius:var(--radius-md)} .tile--anchor{grid-column:span 8;min-height:clamp(280px,38vh,460px)}`

Risks: tiles can become the old cards with new paint; must vary spans and alignment, not just card radius

## Design tokens

```css
:root {
  --bg: #ffffff;
  --surface: #F9F8FA;
  --surface-alt: #F2EEF3;
  --ink: #0D0D0D;
  --muted: #6D6A70;
  --accent: #E6006F;
  --accent-safe: #C2005D;
  --accent-2: #FF4DA6;
  --line: #E9E4EB;
  --success: #0F7B4D;
  --danger: #C42B2B;
  --warning: #8A5A00;

  --font-display: "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --font-body: "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --font-mono: "SFMono-Regular", "Cascadia Mono", ui-monospace, monospace;
  --display-weight: 600;
  --display-tracking: -0.03em;
  --label-tracking: 0.04em;

  --radius-sm: 12px;
  --radius-md: 22px;
  --radius-lg: 32px;
  --border: 1px solid var(--line);
  --shadow: 0 18px 40px rgba(20, 10, 25, 0.06);

  --motion-duration: 200ms;
  --motion-ease: cubic-bezier(.2,.7,.2,1);
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

- Surface: 1px solid var(--line); radius 22px; shadow 0 18px 40px rgba(20, 10, 25, 0.06).
- Type: display **"Avenir Next", "Segoe UI", system-ui, sans-serif** at weight 600, tracking -0.03em; body **"Avenir Next", "Segoe UI", system-ui, sans-serif**; numerals and micro-labels **"SFMono-Regular", "Cascadia Mono", ui-monospace, monospace**.
- Texture: soft bubbles, gradient orbs, fine dividers, compact trade widgets.
- Motion: smooth, 200ms, cubic-bezier(.2,.7,.2,1). Always wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.
- Density: comfortable. Keep body text >= 14px and body contrast >= 4.5:1.
- Use `--accent-safe` for text and icons on `--bg`; use `--accent` for fills and large shapes.

## Originality guard

The replacement must satisfy all of these:

1. The source inventory archetype is `terminal-console`; the new skeleton is `bento-canvas`. Do not fall back to the old shell during implementation.
2. Do not reuse any original class name, CSS selector, design token name, or original accent family.
3. Rewrite templates, not only CSS. Every route must visibly use the new skeleton.
4. Keep every token in `.reskin/content-contract.json`; move it, never rewrite it.
5. Run `node scripts/verify.mjs check` and do not stop until content, structure, accessibility and responsive checks pass.

## Commit statement

Use this sentence in the final report: "The UI was rebuilt around Bubblegum Exchange / Bento Canvas; the original terminal-console shell and palette were removed while the content contract stayed byte-for-byte intact."
