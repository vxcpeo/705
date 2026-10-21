# Reskin art direction — Tidal Sui

> Selected automatically. Do not ask the user to confirm or choose another direction.

- **Style DNA:** `sui-tidal` (clean-fintech)
- **Skeleton:** `split-stage` (spatial)
- **Seed:** `65b75ce24ae00e3f2abc73152a5f8e467036bc8b3667fab2f7df6950ca1b701d`
- **Source DNA:** [https://sui.io](https://sui.io)
- **Live sampled:** yes — https://sui.io (3545 ms)
- **Original:** terminal-console / light / accent #ff0000

## Why this direction

The selector sampled 4/10 blockchain references, scored every direction for perceptual distance from the original accent (#ff0000) and background (#000000), added a deterministic seed jitter, and chose Tidal Sui because it is 146 ΔE away from the original accent and pairs with Split Stage, a spatial skeleton rather than the original terminal-console.

## Live reference sampling

| Style | URL | Result | Accent sampled | Ground sampled |
|---|---|---|---|---|
| base-cobalt | https://www.base.org | ok (1351 ms) | #0000ff | #dde3e9 |
| polygon-agora | https://polygon.technology | ok (6173 ms) | #670de5 | #000000 |
| solana-spectrum | https://solana.com | failed: timeout | — | — |
| ethereum-paper | https://ethereum.org | failed: timeout | — | — |
| optimism-poster | https://www.optimism.io | failed: timeout | — | — |
| arbitrum-signal | https://arbitrum.io | failed: HTTP 403 | — | — |
| cosmos-orbit | https://cosmos.network | ok (4175 ms) | #40b3ff | #000000 |
| uniswap-bubblegum | https://uniswap.org | failed: timeout | — | — |
| aave-abyss | https://aave.com | failed: timeout | — | — |
| sui-tidal | https://sui.io | ok (3545 ms) | #298dff | #ffffff |

Live sampling is evidence, not a copy target. Never download or reuse a reference site's logo, imagery, copy, or code. Use only the abstract tokens below.

## Candidate ranking

| Candidate | Score | Accent ΔE from original | Layout | Live |
|---|---:|---:|---|---|
| Tidal Sui | 0.9655 | 146.2 | split-stage | yes |
| Paper Protocol | 0.9448 | 136.1 | documentary | no |
| Bubblegum Exchange | 0.8905 | 64.4 | bento-canvas | no |
| Cobalt Blueprint | 0.8742 | 176.3 | bento-canvas | yes |
| Agora Violet | 0.8656 | 145 | orbital | yes |
| Abyss Liquidity | 0.8612 | 100.5 | orbital | no |
| Spectrum Terminal | 0.8585 | 121.2 | gallery-scroll | no |
| Cosmos Orbit | 0.8429 | 144.6 | orbital | yes |
| Signal Navy | 0.8266 | 136.8 | bento-canvas | no |
| Poster Optimism | 0.6317 | 38.9 | gallery-scroll | no |

## Skeleton brief

**Split Stage** — asymmetric 5/7 or 4/8 split with a sticky narrative column; one side scrolls independently; no top navigation bar; a vertical index sits in the sticky column; headline and primary action share the left stage; data is presented as an annotated ledger, not a card grid.

Navigation: Vertical index in the sticky column; on mobile it becomes a horizontally scrollable index strip above the content.

Structure:
1. sticky 42% narrative column with brand, route index and page thesis
1. scrolling 58% data stage
1. full-width proof band below the split
1. footer set inside the narrative column

Content mapping: The sticky column carries brand, route index, page title and the primary action. The scrolling stage carries the table/list/form. Secondary metrics become annotated rows rather than cards.

Recipe: `.split{display:grid;grid-template-columns:minmax(300px,42fr) minmax(0,58fr);min-height:100vh}.narrative{position:sticky;top:0;height:100vh;display:flex;flex-direction:column;justify-content:space-between;padding:clamp(24px,4vw,64px)}.stage{min-height:100vh;padding:clamp(24px,5vw,80px) clamp(20px,5vw,90px)}`

Risks: sticky column must not hide content on short screens; mobile must not preserve the split

## Design tokens

```css
:root {
  --bg: #ffffff;
  --surface: #FFFFFF;
  --surface-alt: #E8F3FF;
  --ink: #081B2B;
  --muted: #5B7185;
  --accent: #298dff;
  --accent-safe: #0d71e3;
  --accent-2: #4DA2FF;
  --line: #D8E7F5;
  --success: #087A55;
  --danger: #B42318;
  --warning: #8A5A00;

  --font-display: "Segoe UI Variable Display", "Segoe UI", "Helvetica Neue", sans-serif;
  --font-body: "Segoe UI", "Helvetica Neue", sans-serif;
  --font-mono: "Cascadia Mono", ui-monospace, monospace;
  --display-weight: 600;
  --display-tracking: -0.04em;
  --label-tracking: 0.06em;

  --radius-sm: 12px;
  --radius-md: 22px;
  --radius-lg: 36px;
  --border: 1px solid var(--line);
  --shadow: 0 24px 60px rgba(30, 111, 217, 0.1);

  --motion-duration: 260ms;
  --motion-ease: cubic-bezier(.22,1,.36,1);
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

- Surface: 1px solid var(--line); radius 22px; shadow 0 24px 60px rgba(30, 111, 217, 0.1).
- Type: display **"Segoe UI Variable Display", "Segoe UI", "Helvetica Neue", sans-serif** at weight 600, tracking -0.04em; body **"Segoe UI", "Helvetica Neue", sans-serif**; numerals and micro-labels **"Cascadia Mono", ui-monospace, monospace**.
- Texture: tidal curves, soft caustics, aqua gradients, floating rounded panels.
- Motion: fluid, 260ms, cubic-bezier(.22,1,.36,1). Always wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.
- Density: airy. Keep body text >= 14px and body contrast >= 4.5:1.
- Use `--accent-safe` for text and icons on `--bg`; use `--accent` for fills and large shapes.

## Originality guard

The replacement must satisfy all of these:

1. The source inventory archetype is `terminal-console`; the new skeleton is `split-stage`. Do not fall back to the old shell during implementation.
2. Do not reuse any original class name, CSS selector, design token name, or original accent family.
3. Rewrite templates, not only CSS. Every route must visibly use the new skeleton.
4. Keep every token in `.reskin/content-contract.json`; move it, never rewrite it.
5. Run `node scripts/verify.mjs check` and do not stop until content, structure, accessibility and responsive checks pass.

## Commit statement

Use this sentence in the final report: "The UI was rebuilt around Tidal Sui / Split Stage; the original terminal-console shell and palette were removed while the content contract stayed byte-for-byte intact."
