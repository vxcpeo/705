export const brand = Object.freeze({
  name: 'Filza',
  slug: 'filza',
  asset: 'FILZA',
  network: 'Solana',
  domain: 'filza.xyz',
  handle: '@filza',
  tagline: 'Read the chain. Price the boundary. Keep the record.',
  supportingLine: 'A Solana market terminal for on-chain watchlists, a user-priced payoff boundary and a browser-local research journal.',
})

/* The journal namespace is part of the storage contract. This module previously wrote
   the `Merkova:journal:v1` key, and earlier brands before that; `legacyStorageKeys`
   below lists every retired namespace so ScenarioLab can still migrate from all of
   them. None of those keys may be removed without losing saved user records. */
export const storageKeys = Object.freeze({ journal: 'Filza:journal:v1' })

export const legacyStorageKeys = Object.freeze([
  'Merkova:journal:v1',
  'Tikriva:journal:v1',
  'Orbinza:journal:v1',
  'Kovrane:journal:v1',
  'kinovra:journal:v1',
  'Kinovra:journal:v1',
  'Scenarill:journal:v1',
  'Solenzi:journal:v1',
  'Ivorane:journal:v1',
])
