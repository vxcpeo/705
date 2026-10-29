# Reskin report — Cobalt Blueprint / Split Stage

- Project: `E:\workspace\chuangye\solana\705\website` (`tabuline-website`, Vue 3 + Vite)
- Date: 2026-10-22
- Verdict: **PASS** — `node scripts/verify.mjs check` exits 0 for all six static routes.

> The UI was rebuilt around **[Cobalt Blueprint]** / **[Split Stage]**; the original
> **[sidebar-workspace]** shell and palette were removed while the content contract stayed
> byte-for-byte intact.

## 1. Selected direction

| Field | Value |
| --- | --- |
| Style DNA | `base-cobalt` — Cobalt Blueprint (optimistic-modern) |
| Source DNA | https://www.base.org (live sample, 5980 ms) |
| Skeleton | `split-stage` (spatial) → implementation reads as `terminal-console` / `linear` |
| Original | `sidebar-workspace` / `shell`, light, accent `#298dff` |
| Accent distance | 72.06 ΔE measured (`#298dff` → `#0000d6`; threshold 30) |
| Live sampling | 9 of 10 blockchain references sampled; only arbitrum.io failed (HTTP 403), catalog fallback used for it |

No reference logo, image, copy or code was reused. Only palette, typography mood, shape language,
texture and layout grammar were taken from the DNA.

## 2. Skeleton, and how it differs

The old site was a light left sidebar (brand, numbered index, instrument rows) beside a scrolling
stage, with rounded white cards and sky-blue gradients. The new site inverts that relationship:

- **Right-hand instrument spine, dark ink** (`#0a0b0d`) with a blueprint grid, cobalt ticks and a
  cobalt active route block. The data leaf is on the left. The pointer and the eye enter the
  content first.
- **No `header`/`aside` landmark shell.** The spine is `div[role=complementary]`, the nav and the
  footer sit inside it, and the leaf carries its own slim `.bp-dock`. The source classifier moved
  from `sidebar-workspace` (shell) to `terminal-console` (linear).
- **Different per-route composition.** Home is a ruled ledger (`co-page`): opening article,
  gauge row, board article, quote sheet, settlement figure article, tape rail, briefing list,
  limits sheet — flat sheets with cobalt rules instead of rounded shadowed cards. Markets, journal
  and documentation each re-lay their content in the new stage grammar; legal routes use a ruled
  clause sheet.
- **Mobile is a genuine linear adaptation**, not the collapsed sidebar: leaf first, then the dark
  spine, with the numbered index expanding behind the existing `aria-expanded` toggle.

Evidence is in `.reskin/current/` (screenshots), `.reskin/baseline/` (the captured pre-reskin
state) and `.reskin/VERIFICATION.md` (gate table).

| Route | DOM similarity | Landmark similarity | Axe serious/critical | Result |
| --- | ---: | ---: | ---: | --- |
| `/` | 0.307 | 0.25 | 0 | PASS |
| `/app/markets` | 0.271 | 0.20 | 0 | PASS |
| `/docs` | 0.364 | 0.40 | 0 | PASS |
| `/privacy` | 0.500 | 0.333 | 0 | PASS |
| `/signal` | 0.400 | 0.25 | 0 | PASS |
| `/terms` | 0.500 | 0.333 | 0 | PASS |

Thresholds: DOM fingerprint ≤ 0.50, landmark sequence ≤ 0.68, CSS class overlap ≤ 0.10, accent
ΔE ≥ 30, contrast failures 0, axe serious/critical 0.

## 3. Content contract

- Frozen contract hash from inventory: `4812d08e7b124142ed96829d176fc1f1426b0c0bc169ca94907e1c9cefdbeed7`
  (336 text tokens, 214 bindings, 46 handlers).
- Verification reports the source contract **intact** with six additive-only warnings (no token
  removed or rewritten).
- Rendered word multisets match the baseline exactly on every route (`/` 236 words, `/app/markets`
  143, `/docs` 321, `/privacy` 133, `/signal` 142, `/terms` 121).
- Attribute, form-field, link and document-title parity hold. Remaining warnings are the
  accessibility-name additions described below, one extra icon link target (`/` in the dock) and
  the two extra numeric tokens on the legal sheets (decorative clause numbers are `aria-hidden`;
  they are digits, not copy).

## 4. Files changed

| File | Change |
| --- | --- |
| `src/App.vue` | rewritten shell (`BpFrame`): leaf + dock + dark spine, new route index, new footer, same navigation handlers and focus behaviour |
| `src/blueprint.css` | **new** global token/reset/shell/primitives layer (replaces `tide.css`) |
| `src/tide.css` | removed from the render path and deleted |
| `src/main.js` | imports `blueprint.css` |
| `src/components/HomePage.vue` | template re-laid out into `co-page`; scoped styles fully rewritten (ruled ledger, flat sheets) |
| `src/components/MarketWorkspace.vue` | aside → complementary `div`, stage renames, dock/ledger restyle |
| `src/components/MarketTable.vue` | renamed `gr-*` table/rail; hairline table system |
| `src/components/PayoffExplorer.vue` | renamed `dy-*` explorer; blueprint chart strokes |
| `src/components/ScenarioLab.vue` | renamed `jn-*` docket; flat form sheet |
| `src/components/DocsPage.vue` | legal routes rebuilt as a ruled clause sheet; docs stage renamed `dc-*` |
| `src/components/SolanaWalletButton.vue` | renamed `wl-*` dialog; flat sheet, cobalt accents |

A pre-edit copy of `src/` is kept in `.reskin/original-src/`; baseline screenshots and page
metrics are in `.reskin/baseline/`.

## 5. Accessibility and responsive results

- axe WCAG 2.x: **0 serious/critical** on every route, desktop and mobile.
- Contrast: **0 failures** across 578 checked text nodes (cobalt, ink, muted, success and danger
  tokens were tuned until the tinted-row and picked-row cases passed 4.5:1).
- One `h1` per route, labelled controls, alt text present, keyboard focus visible
  (`:focus-visible` cobalt outline), skip link preserved.
- No horizontal overflow at 390×844 on any route (the market table scrolls inside its own wrap).
- `prefers-reduced-motion` guard disables scroll smoothing and transitions.
- Mobile navigation target check: PASS (index toggle, `aria-expanded`, pinned focus on Escape).

## 6. Known limitations

- `/app/markets/SOL`-style asset routes are rendered from the same workspace component and were
  captured for the X art, but the gate list only covers the six static routes the router exposes.
- Fonts are system stacks (Inter Tight/Inter/Geist Mono are not bundled); the visual system falls
  back to Segoe UI and Cascadia Mono on this machine.
- The reskin was performed after the identity replacement; visible words therefore carry the
  Tabuline name frozen from the rebrand checkpoint.
