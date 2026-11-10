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
  <section class="bl-quotes" :class="{ 'bl-quotes--compact': compact }" :aria-label="compact ? 'Market quote table' : undefined" :aria-labelledby="!compact ? 'market-table-title' : undefined">
    <div v-if="!compact" class="bl-quotes-head">
      <h2 id="market-table-title" class="bl-h2">Market quotes</h2>
      <p class="bl-meta bl-quotes-feed"><span class="bl-feed-dot" aria-hidden="true"></span>Example quotes / no live feed</p>
    </div>

    <div v-if="!compact" class="bl-quotes-stats">
      <p class="bl-stats-line"><span>On chain stats</span><span class="bl-stats-note">Interface preview / no live feed</span></p>
      <dl class="bl-stats-grid" aria-label="On chain stats preview">
        <div v-for="stat in stats" :key="stat.label" class="bl-stat-tile">
          <dt>{{ stat.label }}<span class="bl-chip bl-chip--accent bl-stat-badge">Preview</span></dt>
          <dd>—</dd>
          <dd>{{ stat.detail }}</dd>
        </div>
      </dl>
    </div>

    <p v-if="props.query.trim()" class="bl-quotes-state" aria-live="polite">{{ rows.length }} result{{ rows.length === 1 ? '' : 's' }} for “{{ props.query.trim() }}”</p>

    <p class="bl-quotes-cap bl-label">Cap +5% / 30-day epoch / model values per unit</p>

    <div v-if="rows.length" class="bl-table-wrap bl-quotes-wrap">
      <table class="bl-table bl-quotes-grid">
        <caption class="visually-hidden">Model market values. Quotes are examples and are not live prices.</caption>
        <thead>
          <tr>
            <th scope="col">Asset</th>
            <th scope="col" class="bl-num">Cap</th>
            <th scope="col" class="bl-num" :class="{ 'bl-loud': activeSide === 'income' }">Income</th>
            <th scope="col" class="bl-num" :class="{ 'bl-loud': activeSide === 'upside' }">Upside</th>
            <th scope="col" class="bl-num">Epoch</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="asset in rows" :key="asset.symbol" :class="{ 'is-chosen': activeSide }">
            <td>
              <a class="bl-asset" :href="`/app/markets/${asset.symbol}`" :aria-label="`Open ${asset.symbol} market, example quote ${money(asset.spot)}`" @click.prevent="navigate(asset.symbol)">
                <span class="bl-asset-mark" aria-hidden="true">{{ asset.initials }}</span>
                <span class="bl-asset-name"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
              </a>
            </td>
            <td class="bl-num"><span class="bl-cap">+5%</span></td>
            <td class="bl-num" :class="{ 'bl-loud': activeSide === 'income' }"><span class="bl-value bl-value--income">{{ money(asset.payoff.incomePrice) }}</span><small class="bl-tag">Model</small></td>
            <td class="bl-num" :class="{ 'bl-loud': activeSide === 'upside' }"><span class="bl-value bl-value--upside">{{ money(asset.payoff.upsidePrice) }}</span><small class="bl-tag">Model</small></td>
            <td class="bl-num"><span class="bl-epoch">30 days</span></td>
            <td><span class="bl-chip"><i aria-hidden="true"></i>Model</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="rows.length" class="bl-cardrail" aria-label="Market cards">
      <a v-for="asset in rows" :key="`card-${asset.symbol}`" class="bl-card" :href="`/app/markets/${asset.symbol}`" @click.prevent="navigate(asset.symbol)">
        <span class="bl-asset-mark" aria-hidden="true">{{ asset.initials }}</span>
        <span class="bl-asset-name"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
        <span class="bl-card-values"><span><small>Income</small><b>{{ money(asset.payoff.incomePrice) }}</b></span><span><small>Upside</small><b>{{ money(asset.payoff.upsidePrice) }}</b></span><ArrowRight :size="14" /></span>
      </a>
    </div>
    <div v-else class="bl-notice bl-notice--flag bl-quotes-empty" role="status" aria-live="polite">
      <p>No model markets match “{{ props.query.trim() }}”.</p>
      <button class="bl-btn bl-btn--quiet" type="button" @click="resetSearch">Reset search</button>
    </div>

    <div class="bl-quotes-foot">
      <span>Indicative model values use a 30-day epoch and 25% volatility.</span>
      <span>Example quotes are not live prices.</span>
    </div>
  </section>
</template>

<style scoped>
.bl-quotes { display: grid; gap: 0; min-width: 0; }
.bl-quotes-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-block-end: 14px;
}
.bl-quotes-feed { display: inline-flex; align-items: center; gap: 8px; }
.bl-feed-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--bl-good);
  box-shadow: 0 0 0 4px rgba(15, 123, 77, .12);
}

/* ------------------------------------------------------------- stat tiles */
.bl-quotes-stats { display: grid; gap: 10px; margin-block-end: 16px; }
.bl-stats-line {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  color: var(--bl-ink-soft);
  font: 600 10px/1.3 var(--bl-font-mono);
  letter-spacing: .12em;
  text-transform: uppercase;
}
.bl-stats-note { color: var(--bl-muted); font-weight: 400; letter-spacing: .04em; }
.bl-stats-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--bl-gap); }
.bl-stat-tile {
  display: grid;
  gap: 4px;
  align-content: start;
  padding: 13px 15px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-surface);
}
.bl-stat-tile dt {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  color: var(--bl-muted);
  font: 600 9.5px/1.4 var(--bl-font-mono);
  letter-spacing: .08em;
  text-transform: uppercase;
}
.bl-stat-tile dd { color: var(--bl-ink); font: var(--bl-display-weight) 20px/1.1 var(--bl-font-display); letter-spacing: -.02em; }
.bl-stat-tile dd + dd { color: var(--bl-muted); font: 400 10.5px/1.5 var(--bl-font-mono); }
.bl-stat-badge { padding: 3px 8px; }

/* ----------------------------------------------------------------- table */
.bl-quotes-state { margin-block-end: 8px; color: var(--bl-accent-safe); font: 600 10.5px/1.6 var(--bl-font-mono); letter-spacing: .04em; }
.bl-quotes-cap { margin-block-end: 6px; }
.bl-quotes-wrap { border: 1px solid var(--bl-line); border-radius: var(--bl-r-sm); background: var(--bl-paper); }
.bl-quotes-grid { min-width: 640px; }
.bl-quotes-grid thead th.bl-loud { color: var(--bl-accent-deep); }
.bl-quotes-grid tbody td.bl-loud { background: var(--bl-tint); }
.bl-asset { display: inline-flex; align-items: center; gap: 11px; text-decoration: none; }
.bl-asset-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 30px;
  height: 30px;
  border-radius: 10px;
  background: var(--bl-surface-2);
  color: var(--bl-ink-soft);
  font: 600 11px/1 var(--bl-font-mono);
}
.bl-asset-name { display: grid; gap: 1px; min-width: 0; }
.bl-asset-name b { font: 600 12px/1.25 var(--bl-font-mono); letter-spacing: .04em; }
.bl-asset-name small { color: var(--bl-muted); font: 400 10px/1.3 var(--bl-font-body); }
.bl-cap { color: var(--bl-accent-deep); font: 600 12px/1.4 var(--bl-font-mono); }
.bl-value { display: block; font: 600 13px/1.4 var(--bl-font-mono); font-variant-numeric: tabular-nums; }
.bl-value--income { color: var(--bl-good); }
.bl-value--upside { color: var(--bl-accent-safe); }
.bl-tag {
  display: block;
  margin-block-start: 2px;
  color: var(--bl-muted);
  font: 400 9px/1.2 var(--bl-font-mono);
  letter-spacing: .14em;
  text-transform: uppercase;
}
.bl-epoch { color: var(--bl-ink-soft); font: 400 11px/1.4 var(--bl-font-mono); }

/* -------------------------------------------------------------- card rail */
.bl-cardrail { display: none; }
.bl-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 15px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-paper);
  color: inherit;
  text-decoration: none;
}
.bl-card-values { display: flex; align-items: center; gap: 14px; margin-inline-start: auto; }
.bl-card-values > span { display: grid; gap: 2px; text-align: end; }
.bl-card-values small { color: var(--bl-muted); font: 400 9px/1.2 var(--bl-font-mono); letter-spacing: .12em; text-transform: uppercase; }
.bl-card-values b { font: 600 12px/1.2 var(--bl-font-mono); font-variant-numeric: tabular-nums; }
.bl-card-values > span:first-child b { color: var(--bl-good); }
.bl-card-values > span:nth-child(2) b { color: var(--bl-accent-safe); }
.bl-card-values svg { color: var(--bl-muted); }

/* --------------------------------------------------------- empty + footer */
.bl-quotes-empty { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
.bl-quotes-foot {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-block-start: 12px;
  padding-block-start: 10px;
  border-block-start: 1px solid var(--bl-line);
  color: var(--bl-muted);
  font: 400 10px/1.7 var(--bl-font-mono);
}

/* ---------------------------------------------------------------- compact */
.bl-quotes--compact .bl-quotes-grid { min-width: 0; table-layout: fixed; }
.bl-quotes--compact .bl-quotes-grid th:nth-child(5), .bl-quotes--compact .bl-quotes-grid td:nth-child(5),
.bl-quotes--compact .bl-quotes-grid th:nth-child(6), .bl-quotes--compact .bl-quotes-grid td:nth-child(6) { display: none; }
.bl-quotes--compact .bl-quotes-grid th, .bl-quotes--compact .bl-quotes-grid td { padding-inline: 8px; }
.bl-quotes--compact .bl-quotes-grid th:first-child, .bl-quotes--compact .bl-quotes-grid td:first-child { width: 42%; }

@media (max-width: 900px) {
  .bl-stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .bl-quotes-head { align-items: flex-start; flex-direction: column; gap: 8px; }
}
@media (max-width: 580px) {
  .bl-quotes-wrap { display: none; }
  .bl-cardrail { display: grid; gap: 10px; }
  .bl-quotes-foot { flex-direction: column; gap: 4px; }
}
</style>
