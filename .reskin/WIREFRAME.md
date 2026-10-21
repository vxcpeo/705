# Wireframe — Tidal Sui / Split Stage

Project: `website/` (Vue 3.5 + Vite 6). Baseline archetype: `terminal-console` (linear).
New archetype: `split-stage` (spatial). No persistent status strip, no command rail, no
two-track console panes, no hint bar pinned under a console.

## New shell — `src/App.vue` (class namespace `tide-`)

Desktop (>= 1080 px): a single asymmetric split, `grid-template-columns: minmax(320px, 42fr) minmax(0, 58fr)`.

| Region | Holds |
| --- | --- |
| `header.tide-mast` (sticky, 100vh, left column) | brand lockup (`icon.svg` + `{{ brand.name }}`), build line, vertical route index (`nav`), instrument block (Mode / Network / Unit / Records + handle-domain tail), actions (wallet, "Open the board"), colophon + footer links |
| `main.tide-stage` (right column) | the route component, then a full-width proof band carrying the Feed / Unit / Stores / Target facts and the disclaimer |

Mobile (< 1080 px): the mast becomes a compact header (brand + actions + index disclosure
button with `aria-expanded`); the index becomes a horizontally scrollable strip under the
header; the instrument block and colophon move below the stage content. The split is not
preserved. The sticky column is only sticky at >= 1080 px and has its own scroll if short.

Navigation pattern: vertical index in the narrative column, numbered 01–06, each line carrying
the route label and its existing note; the current route is marked with a filled accent bar and
`aria-current`. No horizontal top bar on desktop. On mobile the same index becomes a strip
behind the disclosure.

## Route compositions (`main` content)

| Route | Composition |
| --- | --- |
| `/` HomePage | 8/4 shoreline opening (headline left, supporting copy + actions right), annotated six-cell gauge band, then a 7/5 board band (watchlist ledger left, sandbox unit quote right), a settlement split figure + readout, a horizontal sample tape, a numbered briefing ledger, and a full-bleed limits band |
| `/app/markets` (+ detail, launchpad, auctions, recompose) | opening band with a large page title and back link; filters as a command row; board as a 8/4 split (data table left, annotated facts rail right); asset detail as 5/7 (passport left, payoff instrument right); leaf routes as a single centred sheet |
| `/docs` | opening thesis; then a 3/9 document split: sticky in-page index in the margin, prose column right; concept figures as full-width annotated plates |
| `/signal` ScenarioLab | opening thesis; 7/5 form split (field deck left, assumption panel right); review and journal steps as a single record sheet with the step track |
| `/terms`, `/privacy`, `/risk` | opening thesis; prose column with an actions row, no nested split |
| 404 | single centred sheet |

## Component mapping

- `src/console.css` → **deleted**; replaced by `src/tide.css` (tokens, reset, shell split, type,
  primitives: buttons, inputs, tables, notices, facts, pills, figures, reduced motion).
- New shell: `App.vue` (mast + stage + proof band). Old status strip, command line, command
  rail, hint strip and two-track console deck removed.
- Kept as content-only children (script blocks unchanged): `HomePage.vue`, `MarketWorkspace.vue`,
  `MarketTable.vue`, `PayoffExplorer.vue`, `ScenarioLab.vue`, `DocsPage.vue`,
  `SolanaWalletButton.vue`. Each template is re-laid-out; each scoped stylesheet is replaced.
- `index.html`: `theme-color` and `color-scheme` switch to the light Tidal tokens; title,
  description, icons and social metadata untouched.

## Tokens and breakpoints

`src/tide.css` defines `--tide-*` custom properties from STYLE.md (`--bg`, `--surface`,
`--ink`, `--muted`, `--accent`, `--accent-safe`, `--accent-2`, `--line`, `--radius-*`,
`--shadow`, `--motion-*`), typography from the Sui direction, and the shell grid.

Breakpoints: 1180 px (split ratio tightens), 1080 px (split becomes one column, mast becomes
header, index becomes strip), 760 px (bands stack, tables become labelled rows), 520 px (form
pairs single column, gauges two columns). Every route must render without horizontal overflow
at 390 px.

## Content protection

Every static string, binding, handler, route, source, form signature and link target comes from
the existing templates and is moved verbatim. Script blocks are not edited except for the one
presentational selector in `App.vue` (`onKeydown` focus target), which keeps the same focus
behaviour. No new visible copy.
