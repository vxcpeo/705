# Reskin wireframe — Bubblegum Exchange / Bento Canvas

Round 2 of the reskin record. The baseline frozen in `.reskin/baseline/` is the **Cobalt Blueprint
split stage** (right-hand dark instrument spine, scrolling data leaf, ruled sheets, `#0000d6` accent).
Round 1 evidence is archived at `website/.reskin-r1/`.

## Shell

New shell: **Bloom frame** (`bl-` namespace, `src/styles/bloom.css`).

| Old | New |
| --- | --- |
| `.bp-frame` two-column grid: data leaf + sticky dark spine | `.bl-shell` single canvas: slim sticky masthead, route stage, bento footer deck |
| Navigation inside the right spine, numbered vertical index, `complementary` landmark | Navigation in the masthead: horizontal index chips, filled chip for the current route, collapsing into a pull-down sheet below 1000px |
| Route content in `.bp-leaf-body` with `.bp-band` ruled bands | Route content in a 12-column bento grid (`.bl-bento`) of tiles with mixed spans |
| Facts split between spine (`bp-instrument`) and leaf footer (`bp-proof`) | Facts merged into one three-tile footer deck (`about` / `mode` / `proof`) |
| `main` + `div[role=complementary]` + nav + footer | `header` + `nav` + `main` + `footer` landmarks |

No `<aside>`, no sidebar, no dark spine: the DOM depth profile and landmark sequence both change.

## Route → composition

| Route | Anchor tile (span 7–8) | Support tiles | Full-bleed bands |
| --- | --- | --- | --- |
| `/` | Opening: kicker, three-line `h1`, actions, limits note | lead + gauge | board 8 / quote 4, split figure 7 / readout 5, tape 12, four briefing tiles span 3, limits 8 + accent tile 4 |
| `/app/markets` | Page title + summary | board toolbar, market table 8, four fact tiles 4 | table band |
| `/app/markets/:symbol` | Series passport 4 | payoff explorer 8 | meters |
| `/signal` | Lab title + notices | form 7 / workspace notes 5 | review + journal record |
| `/docs` | Doc title 8 | on-page index 4 (2-col chip grid) | steps, roles, three concept tiles span 4, settlement, eight leaf tiles span 4 |
| `/risk`, `/terms`, `/privacy` | Notice title 8 + accent tile 4 | numbered clause rows 12 | actions |

Mobile (<1000px) is a linear stack: masthead row, scrollable index rail (or pull-down sheet),
single-column tiles. No content is hidden at any width.

## Content mapping rule

Tiles only add wrappers. Every text node, interpolation, `@` handler, `v-model`, form field, link
target and asset path is moved verbatim from `.reskin/baseline/content-contract.json`; the
`visually-hidden` utility name is kept so the frozen `hiddenText` tokens stay hidden text.

## Token / breakpoint files

- `src/styles/bloom.css` — tokens, reset, base type, shell, bento grid, primitives.
- Component scoped styles use the same tokens; breakpoints 1280 / 1000 / 720 / 460.
- `src/blueprint.css` is deleted from the render path.
