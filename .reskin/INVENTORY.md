# Reskin inventory — filza-website

Generated: 2026-10-19T18:46:57.213Z

## Project

| Field | Value |
|---|---|
| Root | `E:/workspace/chuangye/solana/705/website` |
| Vue | ^3.5.13 |
| Package manager | npm |
| Nuxt | no |
| CSS frameworks | none detected |
| Files scanned | 26 (16 SFCs) |

## Original skeleton

- Archetype: **sidebar-workspace** (shell)
- Traits: sidebar, cards, hero, table, grid, tabs, modal, charts, sticky, terminal
- Max template depth: 11
- Top-level tags: a, div, section, section, div, section, section, section, section, div, a, div, section, section, div, section, section, section, section, div

The replacement skeleton must not be `sidebar-workspace` and must not be in the same family (`shell`).

## Routes

- `/`
- `/app/markets`
- `/docs`
- `/privacy`
- `/signal`
- `/terms`

## Palette (most used first)

`#ffffff` (16) · `#0d0d10` (8) · `#3a3a44` (6) · `#f2eee6` (4) · `#0f8a63` (2) · `#1f4fe0` (2) · `#2b2b33` (2) · `#33333c` (2) · `#4a4a55` (2) · `#6f6a60` (2)

## Content lock

- Static visible text tokens: **672**
- Binding expressions: **428**
- Event handlers: **92**
- Contract hash: `3a7f596d88bae2d33fff020c22e6632666384f80cf177291f9a322ccca481ba5`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/705/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/705/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
