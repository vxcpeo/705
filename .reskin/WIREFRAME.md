# Wiring plan — Orbit Atlas (committed before implementation)

Style: **Cosmos Orbit** (`cosmos-orbit`), skeleton target: **Gallery Scroll / spatial**.
Original: `sidebar-workspace` / `shell` — a fixed left rail plus a ruled paper sheet.

## New shell

| Region | Element | Replaces |
|---|---|---|
| Identity | `header.atlas-mast` (sticky): brand lockup, 2-line build line, telemetry ribbon, wallet + open-board actions | `.rail` head, `.rail-foot`, `.strip` |
| Navigation | `nav.atlas-dock`: floating pill dock, fixed bottom centre, 6 route links with number, label and note; horizontally scrollable on phones | `.rail-nav` |
| Stage | `main.atlas-stage`: sequence of `.atlas-scene` blocks separated by one hairline | `.sheet` + 12-column `.editorial` grid |
| Station data | `footer.atlas-colophon`: brand, figure list, station readout `dl`, tiny disclaimer | `.rail-readout`, `.rail-tiny`, `.colophon` |
| Mobile drawer | `button.atlas-mast-more` reveals the telemetry ribbon; `.atlas-mast-scrim` closes it | `.railtoggle` + `.rail-scrim` |

Landmarks go from `aside > nav > main > header > aside > footer > nav` to
`header > nav > main > footer` (`/docs` adds the on-page index as a second `nav`).

## Route → composition

| Route | Scenes |
|---|---|
| `/` | 01 opening (display headline + orbit rings + CTA column) · 02 metric ribbon (6 facts) · 03 board (switch + search + table) · 04 unit quote (readout column + control card) · 05 settlement split (`#cap`: figure + 2×4 readout) · 06 sample tape (snap rail) · 07 briefing (2×2 link plates) · 08 limits (halo panel) |
| `/app/markets` | opening + back link · sheet facts (4) · board branch: filters rail + `MarketTable` (head, stats, table, card rail, footnote) · leaf branch for launchpad/recompose · passport + payoff branch for an asset |
| `/docs` | opening · on-page index as a horizontal pill rail · mechanism (steps + two role plates) · concepts (three inverted plates) · settlement (copy + formula) · eight prose leaves in a 2-column constellation · legacy anchors |
| `/risk`, `/terms`, `/privacy` | opening + quoted prose column + two actions |
| `/signal` | opening · form scene (field column + `atlas-face` form, aside plate) · record scenes for review and journal |

## Component decisions

| Old | New |
|---|---|
| `App.vue` shell (rail + strip) | rewritten: mast, dock, stage, colophon |
| `HomePage` mast + 12-col editorial | rewritten as eight scenes |
| `MarketWorkspace` header + `cells` + `panel` cards | rewritten as scenes + passports |
| `MarketTable` `ledger`, `market-cards`, `cells` | rewritten: `atlas-table` + card rail, stats grid |
| `PayoffExplorer` `panel` + `chart-*` | rewritten: dial column + instrument card + meters |
| `DocsPage` sticky TOC + ruled sheet | rewritten: pill index + leaves |
| `ScenarioLab` `sl-*` two-column | rewritten: field deck + aside plate + record plate |
| `SolanaWalletButton` ink sheet dialog | rewritten: rounded hatch dialog with pill options |
| `src/styles.css`, `src/mobile.css` | deleted; replaced by `src/reskin.css` |

Content-only children (SVG payoff figure, concept plates, all form fields, all
copy) are kept verbatim; only wrappers, class names and layout change.

## Tokens and breakpoints

- `src/reskin.css` defines `--void / --deck / --star / --beam / --hair / --glow`,
  `--r-pill / --r-lg / --r-md / --r-sm`, `--font-display / --font-body / --font-mono`,
  `--pad`, `--fit`, `--dock-h`, `--ease`.
- Breakpoints: 1180 (fact grid → 3), 1080–1100 (split scenes stack), 1000 (form stacks),
  900 (mast compacts, ribbon → drawer, dock notes hidden, 2-col → 1-col),
  780/640/620 (tables and pairs stack), 580 (market cards replace the table),
  520–480 (meters and dialog go full width).
- Motion: 180–420 ms with `cubic-bezier(.16, 1, .3, 1)`, all non-essential motion
  guarded by `prefers-reduced-motion`.
