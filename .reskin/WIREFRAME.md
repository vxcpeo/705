# Wireframe — Abyss Console (Pretiola)

Selected automatically: **Abyss Liquidity** (`aave-abyss`, dark-technical) with the
**Terminal Console** (`terminal-console`, linear) skeleton. Original skeleton: `orbital`
(spatial) — a floating pill dock, a sticky mast and full-bleed scenes on a star field.
Source DNA sampled live from <https://aave.com> (3459 ms); only abstract palette, type,
shape, density and motion were taken.

This wireframe is the commitment. Every route uses the console archetype; there is no
fallback shell.

## 1. Shell — `App.vue`

```
<main class="tty-console" id="main">
  <div class="tty-status">            status strip, 30px, sticky
    brand link · Mode/Network/Unit/Records · handle + domain targets
  </div>
  <div class="tty-command">           command line
    prompt + "network market terminal / Preview build"   wallet · Open the board · nav toggle
  </div>
  <div class="tty-deck">              two-track console
    <nav class="tty-nav">             command rail (01-06), current command marked
    <div class="tty-stage">           route content
      <route component>
      <colophon>
    </div>
  </div>
  <div class="tty-hint">              station readout + disclaimer
</main>
```

- Landmarks: `main` then `nav` inside it. No `header`, no floating dock, no `aside`.
- Navigation pattern: a vertical command rail of numbered commands with their notes, inside
  the console. Below 860px the rail becomes a horizontal command strip behind an
  `aria-expanded` toggle in the command line (Escape closes it).
- Mobile: one column; the status cells collapse at 560px; the hint strip stacks.

## 2. Route mapping

| Route | New composition (regions) |
|---|---|
| `/` | command block (kicker, h1, lead, actions, note) → metric strip → **pane deck**: left = board table with its filter/switch toolbar, right = unit-quote form and readout → settlement split → sample tape → briefing → limits |
| `/app/markets` | command block → **pane deck**: left = filters + market table (`Market quotes`, stats band), right = sheet-facts rail → colophon |
| `/app/markets/:symbol` | command block → **pane deck**: left = passport + payoff explorer, right = facts rail |
| `/signal` | command block → **pane deck**: left = step form, right = assumption panel / review record / journal record |
| `/docs` | command block → **document console**: left = in-page index (sticky), right = mechanism, concepts, settlement, prose leaves |
| `/privacy`, `/terms` | command block → legal copy block → actions; same console shell |
| 404 | console error block inside the stage |

## 3. Components

- `App.vue` — rewritten shell (status strip, command line, command rail, stage, hint strip,
  colophon). Script logic kept: `pathname`, `navigate`, `popState`, `scrollToHash`, title
  watch, Escape handling (now closing the command drawer).
- `HomePage.vue` — hero retained as the command block; board and quote moved into a two-track
  deck; settlement split, tape, briefing and limits follow as console blocks.
- `MarketWorkspace.vue` — opening + deck: table left, facts rail right; detail/leaf routes
  keep their own left pane.
- `MarketTable.vue` — data grid restyled (mono headers, tabular numbers, state pills, mobile
  card rail retained).
- `PayoffExplorer.vue` — dial column + instrument card, chart/table toggle retained.
- `DocsPage.vue` — in-page index becomes a sticky left rail; prose becomes the right column.
- `ScenarioLab.vue` — field deck + assumption/record panel, step track retained.
- `SolanaWalletButton.vue` — dialog restyled to a console sheet.

## 4. CSS architecture

- `src/console.css` — the single global layer: tokens (Abyss), reset/base type, console shell,
  deck/rail/pane layout, typography, surface, pills, buttons, switch, fact grid, key/value,
  rails, tables, forms, notices, colophon, responsive rules, reduced-motion guard.
- `src/reskin.css` — deleted (old global layer, no longer imported).
- Component `<style scoped>` blocks remain, renamed to the new token/class names; they carry
  component-specific layout only.
- New namespace: `tty-` (shell/primitives), `pag-` (home), `wrk-` (markets), `tbl-` (table),
  `pfx-` (payoff), `doc-` (docs), `log-` (scenario), `wal-` (wallet). No original class or
  token name survives.
- Breakpoints: 1080px (deck collapses), 900px (docs index becomes a strip), 860px (rail becomes
  a drawer), 560px (status cells collapse).
