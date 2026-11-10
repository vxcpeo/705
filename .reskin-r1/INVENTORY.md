# Reskin inventory — tabuline-website

Generated: 2026-10-22T15:09:37.140Z

## Project

| Field | Value |
|---|---|
| Root | `E:/workspace/chuangye/solana/705/website` |
| Vue | ^3.5.13 |
| Package manager | npm |
| Nuxt | no |
| CSS frameworks | none detected |
| Files scanned | 15 (8 SFCs) |

## Original skeleton

- Archetype: **sidebar-workspace** (shell)
- Traits: sidebar, cards, table, grid, tabs, modal, charts, sticky, terminal
- Max template depth: 11
- Top-level tags: a, div, div, div, section, div, section, section, div

The replacement skeleton must not be `sidebar-workspace` and must not be in the same family (`shell`).

## Routes

- `/`
- `/app/markets`
- `/docs`
- `/privacy`
- `/signal`
- `/terms`

## Palette (most used first)

`#0d71e3` (9) · `#ffffff` (8) · `#298dff` (4) · `#081b2b` (3) · `#e8f3ff` (2) · `#087a55` (1) · `#0a5bc0` (1) · `#0a5c42` (1) · `#24465f` (1) · `#4da2ff` (1)

## Content lock

- Static visible text tokens: **336**
- Binding expressions: **214**
- Event handlers: **46**
- Contract hash: `4812d08e7b124142ed96829d176fc1f1426b0c0bc169ca94907e1c9cefdbeed7`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/705/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/705/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
