# Reskin inventory — librova-website

Generated: 2026-10-21T12:39:10.074Z

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
- Max template depth: 12
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

`#ff0000` (20) · `#050608` (13) · `#0a0e14` (7) · `#000000` (5) · `#0d141b` (5) · `#5ce1a0` (4) · `#ff00c8` (4) · `#ff6b6b` (3) · `#121a24` (2) · `#182533` (2)

## Content lock

- Static visible text tokens: **336**
- Binding expressions: **214**
- Event handlers: **46**
- Contract hash: `3d00ded2cdd47802617906eea285edc387a2bb8d4e6c483f87aba609740953d5`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/705/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/705/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
