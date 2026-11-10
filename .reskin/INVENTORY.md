# Reskin inventory — tallyria-website

Generated: 2026-11-09T18:05:19.119Z

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

- Archetype: **terminal-console** (linear)
- Traits: cards, table, grid, tabs, modal, charts, sticky, terminal
- Max template depth: 11
- Top-level tags: a, div, div, div, section, div, section, section, div

The replacement skeleton must not be `terminal-console` and must not be in the same family (`linear`).

## Routes

- `/`
- `/app/markets`
- `/docs`
- `/privacy`
- `/signal`
- `/terms`

## Palette (most used first)

`#ffffff` (11) · `#0000d6` (4) · `#0000cc` (3) · `#0a0b0d` (3) · `#0000ff` (2) · `#081b2b` (2) · `#0000b3` (1) · `#005f3f` (1) · `#14161a` (1) · `#2a2c31` (1)

## Content lock

- Static visible text tokens: **336**
- Binding expressions: **215**
- Event handlers: **47**
- Contract hash: `9a6611056f8484ff8d2b274e27d7e61586c165f050998d5ac33619eaeaeaeea3`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/705/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/705/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
