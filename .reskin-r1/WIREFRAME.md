# Wiring plan — Cobalt Blueprint / Split Stage

The reskin selector chose **Cobalt Blueprint** (`base-cobalt`, sampled from base.org) with the
**Split Stage** skeleton. The original DOM archetype was `sidebar-workspace` (family `shell`).
This plan was written before the presentation layer was rebuilt and is the commitment the
implementation follows.

## 1. New shell

- `src/App.vue` becomes `BpFrame`: a two-column frame with the **data leaf on the left** and the
  **instrument spine on the right**. The spine is the sticky column; it is dark ink with a
  blueprint grid, not a light sidebar.
- Landmarks: `main` (leaf) → `div[role=complementary]` (spine) → `nav` → `footer`. No `header`
  landmark and no `<aside>` element, so the source classifier no longer sees a sidebar shell.
- Top actions live in a slim `.bp-dock` inside the leaf (icon-only home link, wallet, primary
  action, mobile index toggle). The wordmark and the numbered index live in the spine.
- Mobile: single column. The leaf comes first; the spine follows as a dark block; the index is
  collapsed behind the existing `aria-expanded` toggle and expands in place.

## 2. Route → composition

| Route | Composition |
| --- | --- |
| `/` | `co-page`: opening article (h1 + supporting column) → gauge row → board article (heading row, filter rail, ruled table) → quote sheet → settlement figure article → tape rail → briefing list → limits sheet. |
| `/app/markets` | `gr` stage: title block → fact strip → ledger table → market facts; asset route: passport sheet beside the payoff explorer. |
| `/signal` | `jn` docket: heading, numbered form steps, side assumption sheet. |
| `/docs` | `dc` document: title block → sticky on-page index → article sections; legal routes use a ruled clause sheet with numbered clauses. |
| 404 | `nf-sheet` inside `.bp-void`. |

## 3. Components

- Kept as content-only children with rewritten templates and renamed classes: `HomePage`,
  `MarketWorkspace`, `MarketTable`, `PayoffExplorer`, `ScenarioLab`, `DocsPage`,
  `SolanaWalletButton`.
- Deleted from the render path: `src/tide.css` (the previous global system). Replaced by
  `src/blueprint.css`, which owns tokens, reset, shell and shared primitives.
- Every original class token was renamed (`tide-→bp-`, `reef-→co-`, `shoal-→gr-`, `buoy-→dy-`,
  `dock-→wl-`, `lagoon-→jn-`, `strand-→dc-`, `wave-→nf-`) and every design variable moved to a
  `--bp-*` name.

## 4. Tokens and breakpoints

- Ground `#dde3e9`, paper `#ffffff`, ink `#0a0b0d`, cobalt `#0000ff` (safe text `#0000d6`),
  secondary `#7575ff`, hairline `#d7d9d3`, panel `#0a0b0d`.
- Type: Inter Tight / Segoe UI display at weight 640 and -0.038em, Inter / Segoe UI body,
  Geist Mono / Cascadia Mono for labels and numerals.
- Shape: 4/8/14/22 px radii, 1 px rules, flat sheets; shadows only on overlay money surfaces.
- Breakpoints: 1180 px (frame proportions), 980 px (split collapses, spine follows the leaf),
  680/620 px (dense single column).

## 5. Content lock

Every token in `.reskin/content-contract.json` is moved, never rewritten. New visible copy is
forbidden, so route-index headers, decorative numbers and shell headings use only existing words
or `aria-label`/`aria-hidden` support.
