# Reskin report — Pretiola, Abyss Console

Generated: 2026-10-20 (Asia/Shanghai) · Project: `website/` (Vue 3.5 + Vite 6)
Verification: **PASS** — `node scripts/verify.mjs check` exit 0, 6/6 routes.

## Direction selected automatically

| | |
|---|---|
| Style | **Abyss Liquidity** (`aave-abyss`, dark-technical) |
| Source DNA | <https://aave.com> — live sampled (3459 ms), not copied |
| Bundled catalog | not used (8/10 references sampled live; `arbitrum.io` returned 403, `sui.io` timed out) |
| Accent | `#ff0000` — 144.6 ΔE from the original `#40b3ff` (minimum 30) |
| Ground | `#000000` abyss, `#0d141b` / `#111a24` decks, hairline `#1e2a36` |
| Type | Trebuchet MS display at weight 650 / tracking −0.035em, Segoe UI body, Cascadia Mono labels |
| Shape | 10–16 px corners, flat beats, one accent glow, fine console grid |

Only abstract DNA was used: palette, typography mood, shape language, texture, density and
motion. No reference logo, image, font file, copy or code was taken.

## Skeleton: what replaced what

Original archetype `orbital` / `spatial`: a 252 px floating pill dock at the bottom of the
viewport, a sticky mast with a telemetry ribbon, and routes built as full-bleed scenes on a
star field with orbit rings and a conic halo.

New skeleton — **Terminal Console** (`terminal-console` / `linear`):

- **Navigation** moved from a floating pill dock to a numbered **command rail inside the
  console**, left of the data stage; the current command is marked with a red left rule.
  Below 860 px the rail becomes a horizontal command strip behind an `aria-expanded` toggle
  in the command line (Escape closes it, focus returns to the toggle).
- **Status strip** at the top of the console: brand, Mode/Network/Unit/Records and the
  target-domain readout, 30 px high, sticky.
- **Command line** under it: a prompt, the terminal identity copy, the wallet and board
  actions, and the navigation toggle.
- **Every route is a command line plus a pane deck**: two-track console panes instead of
  full-bleed scenes. The board and unit quote now sit side by side on `/`; `/app/markets`
  puts the table left and a facts rail right; `/docs` puts a sticky in-page index left and
  the prose right; `/signal` keeps the step form and the assumption/record panel as two
  panes.
- **Landmark sequence** collapsed from `header, nav, main, footer` to `main, nav` (the nav
  sits inside the console main, after the status strip), so the landmark similarity is
  0.25–0.40.
- The star field, orbit rings, conic halo, floating dock, mast ribbon and scene chrome were
  deleted from the source.

### Structure measurements (gate ≤ threshold)

| Route | DOM fingerprint (≤0.50) | Landmark LCS (≤0.68) | Class overlap (≤0.10) | Axe serious | Contrast |
|---|---:|---:|---:|---:|---:|
| `/` | 0.113 | 0.25 | 0.056 | 0 | 0/199 |
| `/app/markets` | 0.126 | 0.25 | 0.046 | 0 | 0/132 |
| `/docs` | 0.121 | 0.40 | 0.046 | 0 | 0/148 |
| `/privacy` | 0.118 | 0.25 | 0.067 | 0 | 0/56 |
| `/signal` | 0.131 | 0.25 | 0.058 | 0 | 0/81 |
| `/terms` | 0.118 | 0.25 | 0.067 | 0 | 0/56 |

Baseline screenshots are in `.reskin/baseline/`, reskinned ones in `.reskin/current/`
(`*-desktop.png` 1440×900 full page, `*-mobile.png` 390×844). Plain **viewport** captures at
the top of each route are in `.reskin/views/` (`home-top-desktop`, `home-scrolled-desktop`,
`markets-top-desktop`, `docs-top-desktop`, `signal-top-desktop`, `home-top-mobile`,
`markets-top-mobile`); these show where the sticky strip really sits, because `fullPage`
stitching paints fixed/sticky elements at the scroll position used for the last slice.

## Content contract

`081faeac66dd7468c844126e52f97a3dbe75ceaac7dc1957a980213acc8d2978` — **unchanged**
(336 static text tokens, 214 bindings, 46 handlers; 0 issues, 0 additive warnings).

Every rendered visible word multiset per route is byte-identical to the baseline
(236 / 143 / 321 / 133 / 142 / 121 word tokens at 1440 px), and the numeric token totals are
unchanged (60 / 25 / 36 / 6 / 12 / 6). No copy was added, removed, rewritten, translated or
hidden:

- Only presentation changed. The content was moved between panes, given new landmarks and
  new markup, never retyped.
- Every route, link target, binding, event handler, form field, asset source, meta
  title/description, document language and i18n value is preserved. `document.title` still
  renders `Overview / Pretiola`, `Markets / Pretiola`, … exactly as before.
- The screen-reader-only strings (`Filter the board`, `Search markets`, `Illustrative`,
  the caption fragments) stay in the same visibility class; the source contract confirms
  they are still `hiddenText`, not visible copy.

## Files changed

| File | Change |
|---|---|
| `src/console.css` | **new** global system: Abyss tokens, reset, status strip, command line, command rail, deck, panes, hint strip, colophon, typography, surfaces, pills, buttons, switch, fact grid, key-value, tables, forms, notices, responsive, reduced-motion |
| `src/reskin.css` | **deleted** (the previous Orbit Atlas global layer) |
| `src/main.js` | imports `console.css` only |
| `src/App.vue` | new shell: status strip + command line + command rail + stage + hint strip + colophon; drawer state replaces the dock; Escape closes the drawer and returns focus to the toggle |
| `src/components/HomePage.vue` | command block + pane deck (board | unit quote), then split, tape, briefing, limits as console blocks |
| `src/components/MarketWorkspace.vue` | opening + pane deck: filters/table | facts rail; detail and leaf routes keep a left pane |
| `src/components/MarketTable.vue` | console data grid: mono headers, tabular numbers, state pills, mobile card rail retained |
| `src/components/PayoffExplorer.vue` | dial column + instrument sheet; chart/table toggle retained |
| `src/components/DocsPage.vue` | document console: sticky in-page index rail + prose column |
| `src/components/ScenarioLab.vue` | field deck + assumption/record pane; step track retained |
| `src/components/SolanaWalletButton.vue` | console sheet dialog |
| `index.html` | `theme-color` → `#000000` (title, description, icons untouched) |

All old class namespaces (`atlas-`, `deck-`, `quay-`, `board-`, `opt-`, `leaf-`, `lab-`,
`port-`) and design-token names (`--void`, `--deck`, `--star`, `--beam`, `--hair`, `--r-*`, …)
are gone; the new namespaces are `tty-`, `pag-`, `wrk-`, `tbl-`, `pfx-`, `doc-`, `log-`,
`wal-` with `--bg`, `--surface`, `--ink`, `--accent`, `--line`, `--radius-*`.

## Accessibility and responsiveness

- axe WCAG 2.0/2.1/2.2 A+AA: **0 serious/critical and 0 moderate** on all six routes.
- Contrast: 0 failures on 199 / 132 / 148 / 56 / 81 / 56 measured text/background pairs.
  Text accents use `--accent-safe` (`#ff5f5f`) on dark surfaces; `--accent` is reserved for
  fills, rules and large shapes.
- Keyboard: 8/8 sampled tab stops on `/` show a visible 2 px focus ring; skip link first.
- One `h1` per route, heading order unchanged, every input labelled, every image has `alt`,
  every control has an accessible name.
- Mobile navigation: all six route targets are reachable at 390 px through the command
  drawer; no horizontal document overflow on any route (`scrollWidth == clientWidth`).
- `prefers-reduced-motion` disables transitions, animations and smooth scrolling.

## Interaction checks (real browser)

`.reskin/tools/smoke.mjs` drives the production preview through the Chrome DevTools
protocol; all 11 checks pass:

- `/signal` loads; the scenario form accepts values; **Review scenario** renders
  "Check the numbers."; **Save to journal** renders "Your local record.".
- `/` renders the console shell; the rail link reaches `/app/markets`; the board search shows
  its empty state and **Reset search** restores the table.
- The wallet dialog opens and closes; `/app/markets/SOL` renders the detail pane; the payoff
  **Table/Chart** toggle shows the settlement table.

## Notes and limitations

- Dynamic routes `/app/markets/:symbol`, `/risk`, `/stats` and the 404 leaf are not part of
  the six captured routes (no static `href` for the 404, and `/risk` is a nav command).
  The detail route and the 404 block were checked in the smoke run and with viewport capture;
  no console errors.
- The home board table keeps its internal horizontal scroll at 390 px (it has seven columns).
  The page itself never overflows; the dedicated `/app/markets` board renders the mobile card
  rail instead.
- The concept figures and the site icon are brand assets from the rebrand and were not
  redrawn; they are displayed as-is inside the new sheets.
- Two pre-existing model outputs are unchanged by the reskin (and by the content lock):
  the settlement readout prints `incomeShare * 100` (9891.6 %) exactly as the baseline did.
  Changing the binding would be a content change; it is recorded here instead.
- `verify.mjs` full-page screenshots paint the sticky status strip at the stitch position;
  `.reskin/views/*-top.png` are the plain viewport captures that show the real layout.

> The UI was rebuilt around **Abyss Liquidity** / **Terminal Console**; the original **orbital**
> shell and palette were removed while the content contract stayed byte-for-byte intact.
