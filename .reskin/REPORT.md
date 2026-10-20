# Reskin report — Filza, Orbit Atlas

Generated: 2026-10-20 (Asia/Shanghai) · Project: `website/` (Vue 3.5 + Vite 6)
Verification: **PASS** — `node scripts/verify.mjs check` exit 0, 6/6 routes.

## Direction selected automatically

| | |
|---|---|
| Style | **Cosmos Orbit** (`cosmos-orbit`, spatial-futurist) |
| Source DNA | <https://cosmos.network> — live sampled (2350 ms), not copied |
| Bundled catalog | not used (9/10 references sampled live; `arbitrum.io` returned 403) |
| Accent | `#40b3ff` — 111.5 ΔE from the original `#b26a00` (minimum 30) |
| Ground | `#000000` void, `#12121e` decks, hairline `#262536` |
| Type | geometric display (Century Gothic / Futura stack), Segoe UI body, Cascadia Mono micro-labels |
| Shape | pill controls, 28 px plates, orbit rings, conic-gradient halo, star dust |

Only abstract DNA was used: palette, typography mood, shape language, texture and
motion. No reference logo, image, font file, copy or code was taken.

## Skeleton: what replaced what

Original archetype `sidebar-workspace` / `shell`: a 252 px fixed left rail with the
route list, a dark 44 px telemetry strip, then a 12-column ruled sheet on paper.

New skeleton — Gallery Scroll scenes on a spatial stage (detector: `orbital`, family
`spatial`, because the Cosmos direction contributes the concentric core):

- **Navigation** moved from a permanent left rail to a floating pill dock fixed at the
  bottom of the viewport: six numbered links with label and note, horizontally
  scrollable below 900 px. A sticky mast now carries identity, telemetry and the
  wallet / board actions only.
- **Every route is a vertical sequence of full-bleed scenes** separated by a single
  hairline instead of a 12-column ruled grid; the opening scene is a display-type
  panel with orbit rings and a soft conic halo.
- **Metrics became typographic facts** (the 6-cell ribbon, the 2×4 split readout, the
  4-cell sheet facts) rather than table cells.
- **Rails**: the sample tape and the on-page index are horizontal snap rails.
- **Footer** absorbed the old rail readout (Feed / Unit / Stores / Target) and the
  tiny disclaimer as a station readout.
- Landmark sequence collapsed from `aside, nav, main, header, aside, footer, nav`
  to `header, nav, main, footer` (`/docs` keeps its on-page index as a second nav).

### Structure measurements (gate ≤ threshold)

| Route | DOM fingerprint | Landmark LCS | Class overlap | Axe serious | Contrast |
|---|---:|---:|---:|---:|---:|
| `/` | 0.392 (≤0.50) | 0.429 (≤0.68) | 0.028 (≤0.10) | 0 | 0/199 |
| `/app/markets` | 0.309 | 0.500 | 0.043 | 0 | 0/132 |
| `/docs` | 0.224 | 0.571 | 0.036 | 0 | 0/148 |
| `/privacy` | 0.343 | 0.500 | 0.049 | 0 | 0/56 |
| `/signal` | 0.383 | 0.429 | 0.048 | 0 | 0/81 |
| `/terms` | 0.343 | 0.500 | 0.049 | 0 | 0/56 |

Baseline screenshots are in `.reskin/baseline/`, reskinned ones in `.reskin/current/`
(`*-desktop.png` 1440×900 full page, `*-mobile.png` 390×844). Extra viewport-level
evidence captured during review: `.reskin/views/` (top / mid / end at 1440 and 390)
and `.reskin/flows/` (review and journal steps, wallet dialog, filtered board, table
toggle, phone telemetry drawer, uncaptured routes).

## Content contract

`3a7f596d88bae2d33fff020c22e6632666384f80cf177291f9a322ccca481ba5` — **unchanged**.

Every visible word multiset per route is byte-identical to the baseline (236 / 143 /
321 / 133 / 142 / 121 word tokens at 1440 px). No copy was added, removed, rewritten,
reordered in a way that changes tokens, translated or hidden:

- Only presentation changed. No `text-transform` trick was needed because the audit
  reads authored text nodes; case is unchanged anyway.
- The only 12 warnings are two aria-labels that describe obsolete navigation
  (`Filza navigation` → the dock is labelled `Primary`; `Site links` → the colophon
  links are now a plain list). Both are accessibility names, not visible copy.
- Every route, link target, binding, event handler, form field, asset source, meta
  title/description, document language and i18n value is preserved. `document.title`
  still renders `Overview / Filza`, `Markets / Filza`, … exactly as before.

## Files changed

| File | Change |
|---|---|
| `src/reskin.css` | **new** global system: tokens, reset, mast, dock, scenes, plates, tables, forms, notices, colophon, breakpoints, reduced-motion guard |
| `src/styles.css` | **deleted** (paper-and-rule ledger system, 646 lines) |
| `src/mobile.css` | **deleted** (empty placeholder) |
| `src/main.js` | imports `reskin.css` only |
| `src/App.vue` | new shell: mast + telemetry ribbon + floating dock + stage + station footer; drawer state replaces the rail toggle |
| `src/components/HomePage.vue` | eight scenes, orbit rings, quote readout column, tape rail, 2×2 briefing |
| `src/components/MarketWorkspace.vue` | opening scene, fact ribbon, passport plate, leaf plates, filter rail |
| `src/components/MarketTable.vue` | `atlas-table` deck, stats grid, mobile card rail, footnote |
| `src/components/PayoffExplorer.vue` | dial column, instrument card, chart/table toggle, position meters |
| `src/components/DocsPage.vue` | pill index rail, mechanism steps, inverted concept plates, prose constellation |
| `src/components/ScenarioLab.vue` | field deck, aside plate, record plate with stage track |
| `src/components/SolanaWalletButton.vue` | hatch dialog with pill wallet options |
| `index.html` | `theme-color` → `#05060d`, added `color-scheme: dark` (title, description, icons untouched) |

Script logic was not changed except presentational wiring: the dock replaced the
rail so `App.vue` keeps `pathname`, `navigate`, `popState`, `scrollToHash`, the title
watch, and the Escape-to-close behaviour (now closing the telemetry drawer); the
wallet dialog's focus selector follows the renamed close button.

## Accessibility and responsiveness

- axe WCAG 2.0/2.1/2.2 A+AA: **0 serious/critical and 0 moderate** on all six routes.
- Contrast: 0 failures on 199 / 132 / 148 / 56 / 81 / 56 measured text/background pairs
  (the old build had 38 failures on `/` alone). Body text ≥ 12 px, most ≥ 13 px.
- Keyboard: 8 sampled tab stops all show a 2 px `#40b3ff` focus ring; skip link first,
  then brand, wallet, board, dock links; `:focus-visible` never removed.
- One `h1` per route, headings unchanged in level; all inputs keep their labels
  (0 labelled-field issues), every image has `alt` (0 issues), every control has an
  accessible name (0 issues).
- Mobile navigation: all six route targets are reachable at 390 px in the dock
  (no hamburger required); the telemetry drawer is an `aria-expanded` disclosure.
- No horizontal document overflow at 390 px on any route (`scrollWidth == clientWidth`).
- `prefers-reduced-motion` disables transitions, animations and smooth scrolling.

Interaction checks run in the real browser (`.reskin/flows/`): scenario form →
review → journal with `Filza:journal:v1` persistence, wallet dialog open/Escape-close
with focus returned, board search + empty state + reset, chart/table toggle, dock
navigation with browser back, phone telemetry drawer. No console or page errors.

## Notes and limitations

- The project contains a stale duplicate of the whole site in `website/a705/`. The
  inventory scans it, so it still contributes `sidebar`/`terminal` signals to the
  archetype classifier (hence `orbital`, not `gallery-scroll`). It was left untouched;
  the shipped UI in `src/` renders no `<aside>` and no left rail.
- Dynamic routes `/app/markets/:symbol`, plus `/risk`, `/stats` and the 404 leaf, are
  not part of the six captured routes (they have no static `href`). They were built
  with the same system and checked manually: correct titles/h1, no overflow, no
  console errors (`.reskin/flows/extra-*.png`).
- The three `/concept-*.webp` plates are supplied brand art and stay byte-identical in
  the DOM; they are inverted with a CSS filter so the paper-drawn plates read as night
  charts inside the dark deck. The site icon `/icon.svg` is likewise an existing asset
  and was not redrawn.
- `verify.mjs` screenshots use `fullPage`, which paints the fixed dock at the position
  it had during stitching; `.reskin/views/*-top.png` shows where the dock really sits.

> The UI was rebuilt around **Cosmos Orbit** / **Gallery Scroll**; the original **sidebar-workspace** shell and palette were removed while the content contract stayed byte-for-byte intact.
