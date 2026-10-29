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
  <section class="gr-ledger" :class="{ 'gr-ledger--compact': compact }" :aria-label="compact ? 'Market quote table' : undefined" :aria-labelledby="!compact ? 'market-table-title' : undefined">
    <div v-if="!compact" class="gr-ledger-head">
      <h2 id="market-table-title" class="bp-h2">Market quotes</h2>
      <p class="bp-meta gr-feed"><span class="gr-feed-dot" aria-hidden="true"></span>Example quotes / no live feed</p>
    </div>

    <div v-if="!compact" class="gr-stats">
      <p class="gr-stats-line"><span>On chain stats</span><span class="gr-stats-note">Interface preview / no live feed</span></p>
      <dl class="gr-stats-grid" aria-label="On chain stats preview">
        <div v-for="stat in stats" :key="stat.label">
          <dt>{{ stat.label }}<span class="bp-pill bp-pill--bp-cobalt gr-badge">Preview</span></dt>
          <dd>—</dd>
          <dd>{{ stat.detail }}</dd>
        </div>
      </dl>
    </div>

    <div class="gr-toolbar">
      <p class="bp-label">Cap +5% / 30-day epoch / model values per unit</p>
      <p v-if="props.query.trim()" class="gr-search-state" aria-live="polite">{{ rows.length }} result{{ rows.length === 1 ? '' : 's' }} for “{{ props.query.trim() }}”</p>
    </div>

    <div v-if="rows.length" class="bp-table-wrap gr-table-wrap">
      <table class="bp-table gr-grid">
        <caption class="visually-hidden">Model market values. Quotes are examples and are not live prices.</caption>
        <thead>
          <tr>
            <th scope="col">Asset</th>
            <th scope="col" class="bp-num">Cap</th>
            <th scope="col" class="bp-num" :class="{ 'bp-loud': activeSide === 'income' }">Income</th>
            <th scope="col" class="bp-num" :class="{ 'bp-loud': activeSide === 'upside' }">Upside</th>
            <th scope="col" class="bp-num">Epoch</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="asset in rows" :key="asset.symbol">
            <td>
              <a class="gr-token" :href="`/app/markets/${asset.symbol}`" :aria-label="`Open ${asset.symbol} market, example quote ${money(asset.spot)}`" @click.prevent="navigate(asset.symbol)">
                <span class="gr-token-mark" aria-hidden="true">{{ asset.initials }}</span>
                <span class="gr-token-name"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
              </a>
            </td>
            <td class="bp-num"><span class="gr-cap">+5%</span></td>
            <td class="bp-num" :class="{ 'bp-loud': activeSide === 'income' }"><span class="gr-value gr-value--income">{{ money(asset.payoff.incomePrice) }}</span><small class="gr-tag">Model</small></td>
            <td class="bp-num" :class="{ 'bp-loud': activeSide === 'upside' }"><span class="gr-value gr-value--upside">{{ money(asset.payoff.upsidePrice) }}</span><small class="gr-tag">Model</small></td>
            <td class="bp-num"><span class="gr-epoch">30 days</span></td>
            <td><span class="bp-pill"><i aria-hidden="true"></i>Model</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="rows.length" class="gr-rail" aria-label="Market cards">
      <a v-for="asset in rows" :key="`card-${asset.symbol}`" class="gr-card" :href="`/app/markets/${asset.symbol}`" @click.prevent="navigate(asset.symbol)">
        <span class="gr-token-mark" aria-hidden="true">{{ asset.initials }}</span>
        <span class="gr-card-copy"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
        <span class="gr-card-values"><span><small>Income</small><b>{{ money(asset.payoff.incomePrice) }}</b></span><span><small>Upside</small><b>{{ money(asset.payoff.upsidePrice) }}</b></span><ArrowRight :size="14" /></span>
      </a>
    </div>
    <div v-else class="bp-notice bp-notice--flag gr-empty" role="status" aria-live="polite">
      <p>No model markets match “{{ props.query.trim() }}”.</p>
      <button class="bp-btn bp-btn--quiet" type="button" @click="resetSearch">Reset search</button>
    </div>

    <div class="gr-foot">
      <span>Indicative model values use a 30-day epoch and 25% volatility.</span>
      <span>Example quotes are not live prices.</span>
    </div>
  </section>
</template>

<style scoped>
.gr-ledger { display: grid; gap: 0; min-width: 0; }
.gr-ledger-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-block-end: clamp(16px, 2vw, 24px);
}
.gr-feed { display: inline-flex; align-items: center; gap: 9px; }
.gr-feed-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--bp-success);
  box-shadow: 0 0 0 4px rgba(0, 135, 90, .14);
}

/* -------------------------------------------------------------- stat strip */
.gr-stats { display: grid; gap: 12px; margin-block-end: clamp(18px, 2vw, 26px); }
.gr-stats-line {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  color: var(--bp-ink);
  font: 600 10px/1.3 var(--bp-font-mono);
  letter-spacing: .16em;
  text-transform: uppercase;
}
.gr-stats-note { color: var(--bp-muted); font-weight: 400; letter-spacing: .08em; }
.gr-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border-block: 1px solid var(--bp-line);
}
.gr-stats-grid > div { display: grid; gap: 5px; padding: 14px 16px; border-inline-start: 1px solid var(--bp-line); }
.gr-stats-grid > div:first-child { border-inline-start: 0; padding-inline-start: 0; }
.gr-stats-grid dt {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  color: var(--bp-muted);
  font: 600 9px/1.4 var(--bp-font-mono);
  letter-spacing: .1em;
  text-transform: uppercase;
}
.gr-stats-grid dd { color: var(--bp-ink); font: 600 20px/1.1 var(--bp-font-display); letter-spacing: -.02em; }
.gr-stats-grid dd + dd { color: var(--bp-muted); font: 400 10px/1.5 var(--bp-font-mono); }
.gr-badge { padding: 3px 8px; }

/* ---------------------------------------------------------------- toolbar */
.gr-toolbar {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-block-end: 8px;
}
.gr-search-state { color: var(--bp-cobalt-deep); font: 500 10px/1.6 var(--bp-font-mono); letter-spacing: .06em; }

/* ------------------------------------------------------------------ table */
.gr-table-wrap { border-radius: var(--bp-r-md); }
.gr-grid th, .gr-grid td { padding: 11px 10px; }
.gr-grid { min-width: 640px; }
.gr-grid thead th.bp-loud { color: var(--bp-cobalt-deep); border-block-end-color: rgba(0, 0, 204, .4); }
.gr-grid tbody td.bp-loud { background: rgba(0, 0, 255, .07); }
.gr-grid tbody td.bp-loud .gr-value { color: var(--bp-cobalt-deep); }
.gr-token { display: inline-flex; align-items: center; gap: 11px; text-decoration: none; }
.gr-token-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 30px;
  height: 30px;
  border-radius: 10px;
  background: var(--bp-paper-2);
  color: var(--bp-ink-2);
  font: 600 11px/1 var(--bp-font-mono);
  box-shadow: inset 0 0 0 1px var(--bp-line);
}
.gr-token-name { display: grid; gap: 1px; min-width: 0; }
.gr-token-name b { font: 600 12px/1.25 var(--bp-font-mono); letter-spacing: .04em; }
.gr-token-name small { color: var(--bp-muted); font: 400 10px/1.3 var(--bp-font-body); }
.gr-cap { color: var(--bp-cobalt-deep); font: 600 12px/1.4 var(--bp-font-mono); }
.gr-value { display: block; font: 600 13px/1.4 var(--bp-font-mono); font-variant-numeric: tabular-nums; }
.gr-value--income { color: var(--bp-success); }
.gr-value--upside { color: var(--bp-cobalt-deep); }
.gr-tag {
  display: block;
  margin-block-start: 2px;
  color: var(--bp-muted);
  font: 400 9px/1.2 var(--bp-font-mono);
  letter-spacing: .18em;
  text-transform: uppercase;
}
.gr-epoch { color: var(--bp-ink-2); font: 400 11px/1.4 var(--bp-font-mono); }

/* --------------------------------------------------------------- card rail */
.gr-rail { display: none; }
.gr-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 15px;
  border: 1px solid var(--bp-line);
  border-radius: var(--bp-r-sm);
  background: var(--bp-paper);
  color: inherit;
  text-decoration: none;
}
.gr-card-copy { display: grid; gap: 2px; min-width: 0; }
.gr-card-copy b { font: 600 12px/1.2 var(--bp-font-mono); }
.gr-card-copy small { overflow: hidden; color: var(--bp-muted); font: 400 10px/1.2 var(--bp-font-body); text-overflow: ellipsis; white-space: nowrap; }
.gr-card-values { display: flex; align-items: center; gap: 14px; margin-inline-start: auto; }
.gr-card-values > span { display: grid; gap: 2px; text-align: end; }
.gr-card-values small { color: var(--bp-muted); font: 400 9px/1.2 var(--bp-font-mono); letter-spacing: .14em; text-transform: uppercase; }
.gr-card-values b { font: 600 12px/1.2 var(--bp-font-mono); font-variant-numeric: tabular-nums; }
.gr-card-values > span:first-child b { color: var(--bp-success); }
.gr-card-values > span:nth-child(2) b { color: var(--bp-cobalt-safe); }
.gr-card-values svg { color: var(--bp-muted); }

/* -------------------------------------------------------------- empty + foot */
.gr-empty { justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; margin-block-start: 8px; }
.gr-foot {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-block-start: 14px;
  padding-block-start: 12px;
  border-block-start: 1px solid var(--bp-line);
  color: var(--bp-muted);
  font: 400 10px/1.7 var(--bp-font-mono);
}

/* ------------------------------------------------------------------ compact */
.gr-ledger--compact .gr-grid { min-width: 0; table-layout: fixed; }
.gr-ledger--compact .gr-grid th:nth-child(5), .gr-ledger--compact .gr-grid td:nth-child(5),
.gr-ledger--compact .gr-grid th:nth-child(6), .gr-ledger--compact .gr-grid td:nth-child(6) { display: none; }
.gr-ledger--compact .gr-grid th, .gr-ledger--compact .gr-grid td { padding-inline: 8px; }
.gr-ledger--compact .gr-grid th:first-child, .gr-ledger--compact .gr-grid td:first-child { width: 42%; }

/* --------------------------------------------------------------- responsive */
@media (max-width: 780px) {
  .gr-ledger-head { align-items: flex-start; flex-direction: column; gap: 8px; }
  .gr-stats-line { align-items: flex-start; flex-direction: column; gap: 6px; }
  .gr-toolbar { flex-direction: column; gap: 6px; }
  .gr-stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .gr-stats-grid > div:nth-child(3) { border-inline-start: 0; padding-inline-start: 0; }
  .gr-stats-grid > div:nth-child(-n+2) { border-block-end: 1px solid var(--bp-line); }
}
@media (max-width: 580px) {
  .gr-table-wrap { display: none; }
  .gr-rail { display: grid; gap: 10px; }
  .gr-foot { flex-direction: column; gap: 4px; }
}
</style>
