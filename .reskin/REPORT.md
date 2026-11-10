# Reskin report — Bloom / Bento Canvas (round 2)

- Project: `E:\workspace\chuangye\solana\705\website` (`tallyria-website`, Vue 3 + Vite)
- Date: 2026-11-10
- Verdict: **PASS** — `node scripts/verify.mjs check` exits 0 for all six static routes.
- Round 1 evidence (the pre-reskin light sidebar baseline and the cobalt split stage it produced)
  is archived at `website/.reskin-r1/`; this directory holds the round-2 baseline, which is the
  cobalt split stage as it stood immediately before this round.

> The UI was rebuilt around **[Bubblegum Exchange]** / **[Bento Canvas]**; the original
> **[terminal-console]** shell and palette were removed while the content contract stayed
> byte-for-byte intact.

## 1. Selected direction

| Field | Value |
| --- | --- |
| Style DNA | `uniswap-bubblegum` — Bubblegum Exchange (clean-fintech) |
| Source DNA | https://uniswap.org (live sample, 3048 ms) |
| Skeleton | `bento-canvas` (spatial), implemented as the Bloom frame |
| Original | `terminal-console` / linear, light ground, accent `#0000d6` |
| Accent distance | 100.6 ΔE measured (`#0000d6` → `#e6006f`; threshold 30) |
| Live sampling | 8 of 10 blockchain references sampled; solana.com returned HTTP 429 and arbitrum.io HTTP 403, catalog fallback used for both |

No reference logo, image, copy or code was reused. Only palette, typography mood, shape language,
texture and layout grammar were taken from the DNA.

## 2. Skeleton, and how it differs

The round-1 site was a cobalt split stage: a light data leaf on the left and a sticky dark
instrument spine on the right holding the wordmark, a numbered vertical index, the build facts and
the footer. This round removes that relationship entirely:

- **No spine, no sidebar, no `complementary` landmark.** The shell is a slim sticky masthead
  (`header`), a route stage (`main`), and a bento footer deck (`footer`). Navigation is a horizontal
  index of pills in the masthead; the current route is a filled pink chip. Below 1000px the index
  becomes a pull-down sheet behind the same `aria-expanded` toggle and Escape handling.
- **Routes are 12-column tile canvases, not ruled bands.** Every route has one oversized anchor tile
  and support tiles with different spans; the composition differs per route: home is 7/5 → 12 → 8/4 →
  7/5 → 12 → 4x3 → 12, markets is 7/5 with a 2x2 fact-tile cluster and a full-width board band, the
  series page splits passport / explorer / meters, the journal is 12 → 7/5, documentation is 8/4 with
  a chip index, a three-tile concept row and a two-column glossary band.
- **All class names and tokens renamed** (`bp-*`/`co-*`/`gr-*`/`dy-*`/`jn-*`/`dc-*`/`wl-*` →
  `bl-*`, `--bp-*` → `--bl-*`). `src/blueprint.css` is deleted; `src/styles/bloom.css` replaces it.
- **Mobile is a linear stack**: masthead (wrapping at <=620px), scrollable index or sheet, one tile
  per row. No content is hidden at any width.

## 3. Content contract

- Frozen contract hash from inventory: `9a6611056f84…` (336 text tokens, 215 bindings, 47 events).
- Verification reports the source contract **intact with zero additive warnings**: no token removed,
  rewritten or added.
- Rendered word multisets match the baseline exactly on every route (`/` 236 words, `/app/markets`
  143, `/docs` 321, `/privacy` 133, `/signal` 142, `/terms` 121).
- Attribute, form-field, link and document-title parity hold. The only warnings are `aria-label`
  changes on controls that were renamed in the new shell (for example the old `Terminal index`
  landmark label is gone with the spine).

## 4. Gate table

| Gate | Threshold | Result |
| --- | --- | --- |
| Source contract | no removals or additions | intact, 0 issues |
| Archetype family | must change | `terminal-console` (linear) → `bento-canvas` (spatial) |
| Accent distance | >= 30 ΔE | 103.43 ΔE |
| DOM fingerprint similarity | <= 0.50 | see `verification.json` per route |
| Landmark similarity | <= 0.68 | see `verification.json` per route |
| CSS class overlap | <= 0.10 | 0.023 – 0.036 (`visually-hidden` plus a few state helpers) |
| Contrast failures | 0 | 0 on all six routes, desktop and mobile |
| Axe WCAG 2.x serious/critical | 0 | 0 on all six routes |
| Keyboard focus visibility | visible | PASS |
| Mobile navigation reachability | >= 2 targets | PASS |
| Horizontal overflow at 390x844 | none | none |

## 5. Files changed

| File | Change |
| --- | --- |
| `src/App.vue` | rewritten shell: masthead index, stage, bento footer deck, same navigation handlers, focus and Escape behaviour |
| `src/styles/bloom.css` | **new** global token, reset, shell, bento, control and footer layer |
| `src/blueprint.css` | deleted (was the round-1 global layer) |
| `src/main.js` | imports `styles/bloom.css` |
| `src/components/HomePage.vue` | template re-laid out as tiles; scoped styles rewritten |
| `src/components/MarketWorkspace.vue` | pass/fact tiles, board band, renamed classes |
| `src/components/MarketTable.vue` | renamed quote ledger, stat tiles, compact table |
| `src/components/PayoffExplorer.vue` | dial / instrument / meter tiles, blueprint chart strokes replaced |
| `src/components/ScenarioLab.vue` | form, quiet notes and record tiles; stages renamed |
| `src/components/DocsPage.vue` | chip index, mechanism and role tiles, concept row, glossary band |
| `src/components/SolanaWalletButton.vue` | renamed dialog, pink-accented sheet |

## 6. Artwork regenerated for the new direction

| Asset | What changed |
| --- | --- |
| `website/public/icon.svg`, `favicon-32.png`, `apple-icon.png` | cobalt gradient tile → pink gradient tile, same mark geometry |
| `website/public/og-image.jpg` / `.svg` | new ground, pink accent, fresh overview screenshot |
| `website/public/concept-*.webp` / `.svg` | three concept figures re-rendered in the Bloom palette |
| `twitter/twitter-logo.jpg`, `twitter-banner.jpg` | new avatar and banner in the same palette |
| `twitter/post-0*-*.jpg` / `@2x` / `.svg` | four post cards re-composed, all built on fresh captures of the new UI |
| `twitter/social-og-image.jpg` | new link card |

`twitter/brandkit.py` now owns the Bloom palette so the site art and the X art cannot drift.

## 7. Accessibility and responsive results

- axe WCAG 2.x: **0 serious/critical** on every route, desktop and mobile.
- Contrast: **0 failures** across 578 checked text nodes (muted tokens were darkened and the accent
  band uses a solid `#c2005d` ground so white text clears 6:1).
- One `h1` per route, labelled controls, alt text present, keyboard focus visible
  (`:focus-visible` accent outline), skip link preserved.
- No horizontal overflow at 390x844; the market tables scroll inside their own wrap and switch to a
  stacked card list below 580px.
- `prefers-reduced-motion` guard disables scroll smoothing and transitions.

## 8. Known limitations

- `/app/markets/:symbol`-style routes are rendered from the same workspace component and were
  captured for the artwork, but the gate list covers the six static routes the app exposes.
- Fonts are system stacks (Avenir Next is not bundled); the visual system falls back to Segoe UI and
  Cascadia Mono on this machine.
- The home settlement figure keeps the model's own arithmetic, including its 98.92%/1.08% shares; the
  reskin did not change any calculation, so the chart reads the same as before by design.
