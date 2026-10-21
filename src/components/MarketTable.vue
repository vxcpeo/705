<script setup>
import { computed } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import { calculatePayoff } from '../payoff.js'

const props = defineProps({
  compact: { type: Boolean, default: false },
  query: { type: String, default: '' },
  side: { type: String, default: 'All' },
})

const emit = defineEmits(['navigate', 'reset'])

const money = value => new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
}).format(value)

const assets = Object.freeze([
  { symbol: 'SOL', name: 'Solana', spot: 182, initials: 'S' },
  { symbol: 'JUP', name: 'Jupiter', spot: 1.12, initials: 'J' },
  { symbol: 'BONK', name: 'Bonk', spot: 0.000021, initials: 'B' },
  { symbol: 'USDC', name: 'USD Coin', spot: 1, initials: '$' },
])

const allRows = assets.map(asset => ({
  ...asset,
  payoff: calculatePayoff({ spot: asset.spot, capPercent: 5, settlementPrice: asset.spot }),
}))

const rows = computed(() => {
  const needle = props.query.trim().toLocaleLowerCase()
  const source = allRows
  if (!needle) return source
  return source.filter(asset => `${asset.symbol} ${asset.name}`.toLocaleLowerCase().includes(needle))
})

const activeSide = computed(() => {
  const value = props.side.trim().toLocaleLowerCase()
  return value === 'income' || value === 'upside' ? value : ''
})

const stats = Object.freeze([
  { label: 'Premium received', detail: 'Model epoch' },
  { label: 'Open series', detail: 'Current epoch' },
  { label: 'Active income', detail: 'Indicative' },
  { label: 'Total volume', detail: 'Model ledger' },
])

function navigate(symbol) {
  emit('navigate', `/app/markets/${symbol}`)
}

function resetSearch() {
  emit('reset')
}
</script>

<template>
  <section class="shoal-ledger" :class="{ 'shoal-ledger--compact': compact }" :aria-label="compact ? 'Market quote table' : undefined" :aria-labelledby="!compact ? 'market-table-title' : undefined">
    <div v-if="!compact" class="shoal-ledger-head">
      <h2 id="market-table-title" class="tide-h2">Market quotes</h2>
      <p class="tide-meta shoal-feed"><span class="shoal-feed-dot" aria-hidden="true"></span>Example quotes / no live feed</p>
    </div>

    <div v-if="!compact" class="shoal-stats">
      <p class="shoal-stats-line"><span>On chain stats</span><span class="shoal-stats-note">Interface preview / no live feed</span></p>
      <dl class="shoal-stats-grid" aria-label="On chain stats preview">
        <div v-for="stat in stats" :key="stat.label">
          <dt>{{ stat.label }}<span class="tide-pill tide-pill--accent shoal-badge">Preview</span></dt>
          <dd>—</dd>
          <dd>{{ stat.detail }}</dd>
        </div>
      </dl>
    </div>

    <div class="shoal-toolbar">
      <p class="tide-label">Cap +5% / 30-day epoch / model values per unit</p>
      <p v-if="props.query.trim()" class="shoal-search-state" aria-live="polite">{{ rows.length }} result{{ rows.length === 1 ? '' : 's' }} for “{{ props.query.trim() }}”</p>
    </div>

    <div v-if="rows.length" class="tide-table-wrap shoal-table-wrap">
      <table class="tide-table shoal-grid">
        <caption class="visually-hidden">Model market values. Quotes are examples and are not live prices.</caption>
        <thead>
          <tr>
            <th scope="col">Asset</th>
            <th scope="col" class="tide-num">Cap</th>
            <th scope="col" class="tide-num" :class="{ 'tide-loud': activeSide === 'income' }">Income</th>
            <th scope="col" class="tide-num" :class="{ 'tide-loud': activeSide === 'upside' }">Upside</th>
            <th scope="col" class="tide-num">Epoch</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="asset in rows" :key="asset.symbol">
            <td>
              <a class="shoal-token" :href="`/app/markets/${asset.symbol}`" :aria-label="`Open ${asset.symbol} market, example quote ${money(asset.spot)}`" @click.prevent="navigate(asset.symbol)">
                <span class="shoal-token-mark" aria-hidden="true">{{ asset.initials }}</span>
                <span class="shoal-token-name"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
              </a>
            </td>
            <td class="tide-num"><span class="shoal-cap">+5%</span></td>
            <td class="tide-num" :class="{ 'tide-loud': activeSide === 'income' }"><span class="shoal-value shoal-value--income">{{ money(asset.payoff.incomePrice) }}</span><small class="shoal-tag">Model</small></td>
            <td class="tide-num" :class="{ 'tide-loud': activeSide === 'upside' }"><span class="shoal-value shoal-value--upside">{{ money(asset.payoff.upsidePrice) }}</span><small class="shoal-tag">Model</small></td>
            <td class="tide-num"><span class="shoal-epoch">30 days</span></td>
            <td><span class="tide-pill"><i aria-hidden="true"></i>Model</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="rows.length" class="shoal-rail" aria-label="Market cards">
      <a v-for="asset in rows" :key="`card-${asset.symbol}`" class="shoal-card" :href="`/app/markets/${asset.symbol}`" @click.prevent="navigate(asset.symbol)">
        <span class="shoal-token-mark" aria-hidden="true">{{ asset.initials }}</span>
        <span class="shoal-card-copy"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
        <span class="shoal-card-values"><span><small>Income</small><b>{{ money(asset.payoff.incomePrice) }}</b></span><span><small>Upside</small><b>{{ money(asset.payoff.upsidePrice) }}</b></span><ArrowRight :size="14" /></span>
      </a>
    </div>
    <div v-else class="tide-notice tide-notice--flag shoal-empty" role="status" aria-live="polite">
      <p>No model markets match “{{ props.query.trim() }}”.</p>
      <button class="tide-btn tide-btn--quiet" type="button" @click="resetSearch">Reset search</button>
    </div>

    <div class="shoal-foot">
      <span>Indicative model values use a 30-day epoch and 25% volatility.</span>
      <span>Example quotes are not live prices.</span>
    </div>
  </section>
</template>

<style scoped>
.shoal-ledger { display: grid; gap: 0; min-width: 0; }
.shoal-ledger-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-block-end: clamp(16px, 2vw, 24px);
}
.shoal-feed { display: inline-flex; align-items: center; gap: 9px; }
.shoal-feed-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 0 4px rgba(8, 122, 85, .14);
}

/* -------------------------------------------------------------- stat strip */
.shoal-stats { display: grid; gap: 12px; margin-block-end: clamp(18px, 2vw, 26px); }
.shoal-stats-line {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  color: var(--ink);
  font: 600 10px/1.3 var(--font-mono);
  letter-spacing: .16em;
  text-transform: uppercase;
}
.shoal-stats-note { color: var(--muted); font-weight: 400; letter-spacing: .08em; }
.shoal-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border-block: 1px solid var(--line);
}
.shoal-stats-grid > div { display: grid; gap: 5px; padding: 14px 16px; border-inline-start: 1px solid var(--line); }
.shoal-stats-grid > div:first-child { border-inline-start: 0; padding-inline-start: 0; }
.shoal-stats-grid dt {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  color: var(--muted);
  font: 600 9px/1.4 var(--font-mono);
  letter-spacing: .1em;
  text-transform: uppercase;
}
.shoal-stats-grid dd { color: var(--ink); font: 600 20px/1.1 var(--font-display); letter-spacing: -.02em; }
.shoal-stats-grid dd + dd { color: var(--muted); font: 400 10px/1.5 var(--font-mono); }
.shoal-badge { padding: 3px 8px; }

/* ---------------------------------------------------------------- toolbar */
.shoal-toolbar {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-block-end: 8px;
}
.shoal-search-state { color: var(--accent-deep); font: 500 10px/1.6 var(--font-mono); letter-spacing: .06em; }

/* ------------------------------------------------------------------ table */
.shoal-table-wrap { border-radius: var(--radius-md); }
.shoal-grid th, .shoal-grid td { padding: 11px 10px; }
.shoal-grid { min-width: 640px; }
.shoal-grid thead th.tide-loud { color: var(--accent-deep); border-block-end-color: rgba(13, 113, 227, .4); }
.shoal-grid tbody td.tide-loud { background: rgba(41, 141, 255, .07); }
.shoal-grid tbody td.tide-loud .shoal-value { color: var(--accent-deep); }
.shoal-token { display: inline-flex; align-items: center; gap: 11px; text-decoration: none; }
.shoal-token-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 30px;
  height: 30px;
  border-radius: 10px;
  background: var(--surface-alt);
  color: var(--ink-soft);
  font: 600 11px/1 var(--font-mono);
  box-shadow: inset 0 0 0 1px var(--line);
}
.shoal-token-name { display: grid; gap: 1px; min-width: 0; }
.shoal-token-name b { font: 600 12px/1.25 var(--font-mono); letter-spacing: .04em; }
.shoal-token-name small { color: var(--muted); font: 400 10px/1.3 var(--font-body); }
.shoal-cap { color: var(--accent-deep); font: 600 12px/1.4 var(--font-mono); }
.shoal-value { display: block; font: 600 13px/1.4 var(--font-mono); font-variant-numeric: tabular-nums; }
.shoal-value--income { color: var(--success); }
.shoal-value--upside { color: var(--accent-deep); }
.shoal-tag {
  display: block;
  margin-block-start: 2px;
  color: var(--muted);
  font: 400 9px/1.2 var(--font-mono);
  letter-spacing: .18em;
  text-transform: uppercase;
}
.shoal-epoch { color: var(--ink-soft); font: 400 11px/1.4 var(--font-mono); }

/* --------------------------------------------------------------- card rail */
.shoal-rail { display: none; }
.shoal-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 15px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: inherit;
  text-decoration: none;
}
.shoal-card-copy { display: grid; gap: 2px; min-width: 0; }
.shoal-card-copy b { font: 600 12px/1.2 var(--font-mono); }
.shoal-card-copy small { overflow: hidden; color: var(--muted); font: 400 10px/1.2 var(--font-body); text-overflow: ellipsis; white-space: nowrap; }
.shoal-card-values { display: flex; align-items: center; gap: 14px; margin-inline-start: auto; }
.shoal-card-values > span { display: grid; gap: 2px; text-align: end; }
.shoal-card-values small { color: var(--muted); font: 400 9px/1.2 var(--font-mono); letter-spacing: .14em; text-transform: uppercase; }
.shoal-card-values b { font: 600 12px/1.2 var(--font-mono); font-variant-numeric: tabular-nums; }
.shoal-card-values > span:first-child b { color: var(--success); }
.shoal-card-values > span:nth-child(2) b { color: var(--accent-safe); }
.shoal-card-values svg { color: var(--muted); }

/* -------------------------------------------------------------- empty + foot */
.shoal-empty { justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; margin-block-start: 8px; }
.shoal-foot {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-block-start: 14px;
  padding-block-start: 12px;
  border-block-start: 1px solid var(--line);
  color: var(--muted);
  font: 400 10px/1.7 var(--font-mono);
}

/* ------------------------------------------------------------------ compact */
.shoal-ledger--compact .shoal-grid { min-width: 0; table-layout: fixed; }
.shoal-ledger--compact .shoal-grid th:nth-child(5), .shoal-ledger--compact .shoal-grid td:nth-child(5),
.shoal-ledger--compact .shoal-grid th:nth-child(6), .shoal-ledger--compact .shoal-grid td:nth-child(6) { display: none; }
.shoal-ledger--compact .shoal-grid th, .shoal-ledger--compact .shoal-grid td { padding-inline: 8px; }
.shoal-ledger--compact .shoal-grid th:first-child, .shoal-ledger--compact .shoal-grid td:first-child { width: 42%; }

/* --------------------------------------------------------------- responsive */
@media (max-width: 780px) {
  .shoal-ledger-head { align-items: flex-start; flex-direction: column; gap: 8px; }
  .shoal-stats-line { align-items: flex-start; flex-direction: column; gap: 6px; }
  .shoal-toolbar { flex-direction: column; gap: 6px; }
  .shoal-stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .shoal-stats-grid > div:nth-child(3) { border-inline-start: 0; padding-inline-start: 0; }
  .shoal-stats-grid > div:nth-child(-n+2) { border-block-end: 1px solid var(--line); }
}
@media (max-width: 580px) {
  .shoal-table-wrap { display: none; }
  .shoal-rail { display: grid; gap: 10px; }
  .shoal-foot { flex-direction: column; gap: 4px; }
}
</style>
