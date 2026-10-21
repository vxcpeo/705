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
  <section class="tbl-block" :class="{ 'tbl-block--compact': compact }" :aria-label="compact ? 'Market quote table' : undefined" :aria-labelledby="!compact ? 'market-table-title' : undefined">
    <div v-if="!compact" class="tbl-head">
      <h2 id="market-table-title" class="tty-h2">Market quotes</h2>
      <p class="tty-meta tbl-feed"><span class="tbl-dot" aria-hidden="true"></span>Example quotes / no live feed</p>
    </div>

    <div class="tbl-deck">
      <div v-if="!compact" class="tbl-stats">
      <p class="tbl-stats-line"><span>On chain stats</span><span class="tbl-stats-note">Interface preview / no live feed</span></p>
      <dl class="tty-facts tbl-stats-grid" aria-label="On chain stats preview">
        <div v-for="stat in stats" :key="stat.label">
          <dt>{{ stat.label }}<span class="tty-pill tty-pill--accent tbl-preview-badge">Preview</span></dt>
          <dd>—</dd>
          <dd>{{ stat.detail }}</dd>
        </div>
      </dl>
    </div>

    <div class="tbl-toolbar">
      <p class="tty-label">Cap +5% / 30-day epoch / model values per unit</p>
      <p v-if="props.query.trim()" class="tbl-search-state" aria-live="polite">{{ rows.length }} result{{ rows.length === 1 ? '' : 's' }} for “{{ props.query.trim() }}”</p>
    </div>

    <div v-if="rows.length" class="tty-table-wrap tbl-table-wrap">
      <table class="tty-table tbl-grid">
        <caption class="visually-hidden">Model market values. Quotes are examples and are not live prices.</caption>
        <thead>
          <tr>
            <th scope="col">Asset</th>
            <th scope="col" class="tty-num">Cap</th>
            <th scope="col" class="tty-num" :class="{ 'loud': activeSide === 'income' }">Income</th>
            <th scope="col" class="tty-num" :class="{ 'loud': activeSide === 'upside' }">Upside</th>
            <th scope="col" class="tty-num">Epoch</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="asset in rows" :key="asset.symbol">
            <td>
              <a class="tbl-token" :href="`/app/markets/${asset.symbol}`" :aria-label="`Open ${asset.symbol} market, example quote ${money(asset.spot)}`" @click.prevent="navigate(asset.symbol)">
                <span class="tbl-token-mark" aria-hidden="true">{{ asset.initials }}</span>
                <span class="tbl-token-name"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
              </a>
            </td>
            <td class="tty-num"><span class="tbl-cap">+5%</span></td>
            <td class="tty-num" :class="{ 'loud': activeSide === 'income' }"><span class="tbl-value tbl-value--income">{{ money(asset.payoff.incomePrice) }}</span><small class="tbl-quote-tag">Model</small></td>
            <td class="tty-num" :class="{ 'loud': activeSide === 'upside' }"><span class="tbl-value tbl-value--upside">{{ money(asset.payoff.upsidePrice) }}</span><small class="tbl-quote-tag">Model</small></td>
            <td class="tty-num"><span class="tbl-epoch">30 days</span></td>
            <td><span class="tty-pill"><i aria-hidden="true"></i>Model</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="rows.length" class="tbl-rail" aria-label="Market cards">
      <a v-for="asset in rows" :key="`card-${asset.symbol}`" class="tbl-card" :href="`/app/markets/${asset.symbol}`" @click.prevent="navigate(asset.symbol)">
        <span class="tbl-token-mark" aria-hidden="true">{{ asset.initials }}</span>
        <span class="tbl-card-copy"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
        <span class="tbl-card-values"><span><small>Income</small><b>{{ money(asset.payoff.incomePrice) }}</b></span><span><small>Upside</small><b>{{ money(asset.payoff.upsidePrice) }}</b></span><ArrowRight :size="14" /></span>
      </a>
    </div>
    <div v-else class="tty-notice tty-notice--flag tbl-empty" role="status" aria-live="polite">
      <p>No model markets match “{{ props.query.trim() }}”.</p>
      <button class="tty-btn" type="button" @click="resetSearch">Reset search</button>
    </div>

    <div class="tbl-foot">
      <span>Indicative model values use a 30-day epoch and 25% volatility.</span>
      <span>Example quotes are not live prices.</span>
    </div>
    </div>
  </section>
</template>

<style scoped>
/* ------------------------------------------------------------------ heading */
.tbl-block { display: grid; gap: 0; min-width: 0; }
.tbl-deck { display: grid; gap: 0; min-width: 0; }
.tbl-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-bottom: clamp(18px, 2vw, 28px);
}
.tbl-feed { display: inline-flex; align-items: center; gap: 9px; }
.tbl-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--mint);
  box-shadow: 0 0 10px rgba(92, 225, 160, 0.9);
}

/* -------------------------------------------------------------------- stats */
.tbl-stats { display: grid; gap: 12px; margin-bottom: clamp(18px, 2vw, 26px); }
.tbl-stats-line {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  margin: 0;
  color: var(--ink);
  font: 500 10px/1.3 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.tbl-stats-note { color: var(--faint); font-weight: 400; letter-spacing: 0.1em; }
.tbl-stats-grid { --cols: 4; margin: 0; }
.tbl-stats-grid dt { display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
.tbl-stats-grid dd + dd { color: var(--faint); }
.tbl-preview-badge { padding: 3px 8px; }

/* ------------------------------------------------------------------ toolbar */
.tbl-toolbar {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.tbl-search-state { margin: 0; color: var(--accent-safe); font: 500 10px/1.6 var(--font-mono); letter-spacing: 0.06em; }

/* -------------------------------------------------------------------- table */
.tbl-table-wrap { border-radius: var(--radius-md); }
.tbl-grid { min-width: 700px; }
.tbl-grid thead th.loud { color: var(--accent-safe); border-bottom-color: rgba(255, 0, 0, 0.5); }
.tbl-grid tbody td.loud { background: rgba(255, 0, 0, 0.07); }
.tbl-grid tbody td.loud .tbl-value { color: var(--accent-safe); }
.tbl-token { display: inline-flex; align-items: center; gap: 11px; text-decoration: none; }
.tbl-token-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--surface-3);
  color: var(--ink-2);
  font: 500 11px/1 var(--font-mono);
  box-shadow: inset 0 0 0 1px var(--line-2);
}
.tbl-token-name { display: grid; gap: 2px; min-width: 0; }
.tbl-token-name b { font: 500 13px/1.2 var(--font-mono); letter-spacing: 0.04em; }
.tbl-token-name small { color: var(--faint); font: 400 10px/1.2 var(--font-body); }
.tbl-cap { color: var(--accent-2); font: 500 12px/1.4 var(--font-mono); }
.tbl-value { display: block; font: 500 13px/1.4 var(--font-mono); font-variant-numeric: tabular-nums; }
.tbl-value--income { color: var(--mint); }
.tbl-value--upside { color: var(--accent-2); }
.tbl-quote-tag {
  display: block;
  margin-top: 3px;
  color: var(--faint);
  font: 400 9px/1.2 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.tbl-epoch { color: var(--muted); font: 400 11px/1.4 var(--font-mono); }

/* --------------------------------------------------------------- card rail */
.tbl-rail { display: none; }
.tbl-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--bg-2);
  color: inherit;
  text-decoration: none;
}
.tbl-card-copy { display: grid; gap: 2px; min-width: 0; }
.tbl-card-copy b { font: 500 13px/1.2 var(--font-mono); }
.tbl-card-copy small { overflow: hidden; color: var(--faint); font: 400 10px/1.2 var(--font-body); text-overflow: ellipsis; white-space: nowrap; }
.tbl-card-values { display: flex; align-items: center; gap: 14px; margin-left: auto; }
.tbl-card-values > span { display: grid; gap: 2px; text-align: right; }
.tbl-card-values small { color: var(--faint); font: 400 9px/1.2 var(--font-mono); letter-spacing: 0.16em; text-transform: uppercase; }
.tbl-card-values b { font: 500 12px/1.2 var(--font-mono); font-variant-numeric: tabular-nums; }
.tbl-card-values > span:first-child b { color: var(--mint); }
.tbl-card-values > span:nth-child(2) b { color: var(--accent-2); }
.tbl-card-values svg { color: var(--faint); }

/* -------------------------------------------------------------- empty + foot */
.tbl-empty { justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; margin-top: 8px; }
.tbl-empty p { margin: 0; }
.tbl-foot {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  color: var(--faint);
  font: 400 10px/1.7 var(--font-mono);
}

/* ------------------------------------------------------------------ compact */
.tbl-block--compact .tbl-grid { min-width: 0; table-layout: fixed; }
.tbl-block--compact .tbl-grid th:nth-child(5), .tbl-block--compact .tbl-grid td:nth-child(5),
.tbl-block--compact .tbl-grid th:nth-child(6), .tbl-block--compact .tbl-grid td:nth-child(6) { display: none; }
.tbl-block--compact .tbl-grid th, .tbl-block--compact .tbl-grid td { padding-inline: 8px; }
.tbl-block--compact .tbl-grid th:first-child, .tbl-block--compact .tbl-grid td:first-child { width: 42%; }

/* --------------------------------------------------------------- responsive */
@media (max-width: 780px) {
  .tbl-head { align-items: flex-start; flex-direction: column; gap: 8px; }
  .tbl-stats-line { align-items: flex-start; flex-direction: column; gap: 6px; }
  .tbl-toolbar { flex-direction: column; gap: 6px; }
}
@media (max-width: 580px) {
  .tbl-table-wrap { display: none; }
  .tbl-rail { display: grid; gap: 10px; }
  .tbl-foot { flex-direction: column; gap: 4px; }
}
</style>
