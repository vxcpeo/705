# Reskin report - Librova, Tidal Split Stage

Generated: 2026-10-21 (Asia/Shanghai) - Project: `website/` (Vue 3.5 + Vite 6)
Verification: **PASS** - `node scripts/verify.mjs check` exit 0, 6/6 routes.

## Direction selected automatically

| | |
|---|---|
| Style | **Tidal Sui** (`sui-tidal`, clean-fintech) |
| Source DNA | <https://sui.io> - live sampled (3545 ms), not copied |
| Live samples | 4/10 references reachable; solana.com, ethereum.org, optimism.io, uniswap.org and aave.com timed out, arbitrum.io returned 403 |
| Accent | `#298dff` - 148.1 dE from the original `#ff0000` (minimum 30) |
| Ground | `#ffffff` page, `#e8f3ff` sky wash, hairline `#d8e7f5` |
| Type | Segoe UI Variable Display / Segoe UI at weight 600, tracking -0.04em; Cascadia Mono labels; tabular numerals |
| Shape | 12 / 22 / 36 px radii, soft blue shadows, hairline rules, tidal arcs, no hard borders |

Only abstract DNA was used: palette, typography mood, shape language, texture, density and
motion. No reference logo, image, font file, copy or code was taken.

## Skeleton: what replaced what

Original archetype `terminal-console` (linear): a 30 px status strip, a command line, a
numbered command rail inside a console, a two-track pane deck, a bottom hint strip and a
dark red-on-black palette.

New skeleton - **Split Stage** (`split-stage`, spatial):

> The verifier's DOM classifier reads the persistent sticky narrative column as
> `sidebar-workspace` (shell family) rather than the selector's `split-stage` label. Either way
> the original `terminal-console` / linear archetype is gone, and the structure gate passes on
> the measured similarity rather than on the label.

- **Navigation** moved from a command rail inside a console to a numbered **vertical index in
  a sticky 42% narrative column**; the current route is marked with an accent left rule and
  `aria-current`. Below 1080 px the narrative column collapses to a header and the index
  becomes a disclosure drawer opened by an icon button; Escape closes it and returns focus to
  the toggle.
- **The status strip, command line, hint strip and console panes were removed.** Their facts
  moved into an instrument block in the narrative column and a proof band at the foot of the
  stage.
- **Every route is now a stage of bands, not a pane deck.** `/` is a 7/5 shoreline opening, a
  six-cell gauge, a full-width watchlist ledger with the sandbox quote below it, a 7/5
  settlement split, a horizontal sample tape, a numbered briefing ledger and a full-width
  limits band. `/app/markets` is a title band, a command row, a four-cell facts strip and the
  full-width market ledger; `/app/markets/:symbol` stacks a passport sheet and a full-width
  payoff instrument. `/docs` is a 3/9 document split with a sticky in-page index in the
  margin. `/signal` is a 7/5 form split and a record sheet. Legal routes are a single prose
  column.
- **Landmark sequence** changed from `main, nav` to `header, nav, main, footer`-style bands
  inside a two-column shell; the measured landmark similarity is 0.25-0.50.
- The dark console, the red accent, the hard borders, the pane gutters and every `tty-`,
  `pag-`, `wrk-`, `tbl-`, `pfx-`, `log-`, `wal-` class were deleted from the render path.

### Structure measurements (gate in brackets)

| Route | DOM fingerprint (<=0.50) | Landmark similarity (<=0.68) | Class overlap (<=0.10) | Axe serious | Contrast |
|---|---:|---:|---:|---:|---:|
| `/` | 0.170 | 0.25 | 0.018 | 0 | 0/200 |
| `/app/markets` | 0.188 | 0.25 | 0.035 | 0 | 0/133 |
| `/docs` | 0.267 | 0.50 | 0.028 | 0 | 0/149 |
| `/privacy` | 0.274 | 0.333 | 0.035 | 0 | 0/57 |
| `/signal` | 0.277 | 0.333 | 0.039 | 0 | 0/82 |
| `/terms` | 0.274 | 0.333 | 0.035 | 0 | 0/57 |

## Content contract

`3d00ded2cdd4` - **unchanged** (336 static text tokens, 214 bindings, 46 handlers; 0 issues,
0 additive warnings). Every rendered visible word multiset per route is byte-identical to the
baseline (236 / 143 / 321 / 133 / 142 / 121 word tokens at 1440 px), and the numeric token
totals are unchanged. No copy was added, removed, rewritten, translated or hidden.

- Only presentation changed. Content was moved between bands and given new markup, never
  retyped.
- Routes, link targets, bindings, handlers, form fields, asset sources, meta title and
  description, document language and i18n values are preserved.
- The two aria-label adjustments are recorded as warnings: the old status strip's
  `aria-label="Build status"` no longer exists because that strip is gone, and the market facts
  rail gained `aria-label="Market facts"` so the new aside has an accessible name.

## Files changed

| File | Change |
|---|---|
| `src/tide.css` | **new** global system: tokens, reset, type, split shell, mast, index, instrument, bands, proof band, buttons, fields, switches, pills, notices, facts, tables, motion, responsive |
| `src/console.css` | **deleted** (the previous console layer) |
| `src/main.js` | imports `tide.css` only |
| `src/App.vue` | new shell: sticky narrative column (brand, route index, instrument, actions, colophon) + stage + proof band; drawer state for the mobile index; Escape returns focus to the toggle |
| `src/components/HomePage.vue` | shoreline opening, gauge band, full-width watchlist ledger, sandbox unit quote, settlement split, sample tape, briefing ledger, limits band |
| `src/components/MarketWorkspace.vue` | title band, command row, facts strip, full-width ledger, stacked detail with a full-width payoff instrument, centred leaf sheets |
| `src/components/MarketTable.vue` | full-width data ledger with a stat strip and a mobile card rail |
| `src/components/PayoffExplorer.vue` | dial band + full-width instrument sheet; chart/table toggle retained |
| `src/components/DocsPage.vue` | document split: sticky in-page index + prose column; concept plates; legal prose |
| `src/components/ScenarioLab.vue` | field deck + assumption panel, record sheet and stage track |
| `src/components/SolanaWalletButton.vue` | light dialog sheet with a scrim and focus trap |
| `index.html` | `theme-color` to `#ffffff`, `color-scheme` to `light` (title, description, icons untouched) |

All old design-token names were replaced by the `--tide-*` layer; the new class namespaces are
`tide-`, `reef-`, `shoal-`, `strand-`, `lagoon-`, `buoy-` and `dock-`.

## Accessibility and responsiveness

- axe WCAG 2.0/2.1/2.2 A+AA: **0 serious or critical** on all six routes.
- Contrast: 0 failures on 200 / 133 / 149 / 57 / 82 / 57 measured text/background pairs.
  Accent text on tinted surfaces uses `--accent-deep` (`#0a5bc0`); `--accent` is reserved for
  fills, bars and decorative arcs.
- Keyboard: skip link first; visible 2 px focus ring on every control; one `h1` per route;
  every input labelled; every image has `alt`; every control has an accessible name.
- Mobile navigation: the index is a disclosure behind an `aria-expanded` toggle; Escape
  closes it and focus returns to the toggle; all six route targets are in the drawer.
- No horizontal document overflow at 1440 px or 390 px on any route
  (`scrollWidth == clientWidth`). Wide data tables scroll inside their own wrapper; the home
  board becomes a card rail below 580 px.
- `prefers-reduced-motion` disables transitions, animations and smooth scrolling.

## Interaction checks (real browser)

`.reskin/tools/smoke.mjs` drives the production preview through the Chrome DevTools protocol;
8/8 checks pass:

- `/signal` loads; the scenario form accepts values; **Review scenario** renders
  "Check the numbers."; **Save to journal** renders "Your local record." with Export JSON.
- The wallet dialog opens and closes from the mast; `/` board search shows its empty state and
  **Clear filter** restores the ledger.
- The rail link reaches `/app/markets`; the payoff **Table/Chart** toggle renders the
  settlement table with the current row marked.
- No console errors on the checked routes.

## Screenshots

Baseline: `.reskin/baseline/` (`*-desktop.png` 1440x900 full page, `*-mobile.png` 390x844).
Current: `.reskin/current/` with the same names. Plain viewport captures of the first fold are
in `.reskin/views/` (`home-top-1440.png`, `markets-top-1440.png`, `docs-top-1440.png`,
`signal-top-1440.png`, `home-top-390.png`, `markets-top-390.png`, `signal-top-390.png`),
because full-page stitching paints sticky elements at the last scroll slice.

## Notes and limitations

- Dynamic routes `/app/markets/:symbol`, `/risk`, `/stats` and the 404 leaf are not part of the
  six captured routes. The detail route was captured and smoke-tested; the 404 block renders
  in the same stage shell.
- The home board table keeps an internal horizontal scroll at 390 px (seven columns); the page
  itself never overflows.
- Pre-existing model output is unchanged and visible as before: the settlement readout prints
  `incomeShare * 100` (9891.6 %), and the home settlement SVG bands use the same percentage
  value. Changing those bindings would be a content change; they are recorded here instead.
- The X kit and the concept figures were regenerated in this art direction after the UI passed
  verification; they show real screenshots of the result.

> The UI was rebuilt around **Tidal Sui** / **Split Stage**; the original **terminal-console**
> shell and palette were removed while the content contract stayed byte-for-byte intact.