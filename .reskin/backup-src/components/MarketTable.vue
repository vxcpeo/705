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
  <section class="board-block" :class="{ 'board-block--compact': compact }" :aria-label="compact ? 'Market quote table' : undefined" :aria-labelledby="!compact ? 'market-table-title' : undefined">
    <div v-if="!compact" class="board-head">
      <h2 id="market-table-title" class="atlas-h2">Market quotes</h2>
      <p class="atlas-meta board-feed"><span class="board-dot" aria-hidden="true"></span>Example quotes / no live feed</p>
    </div>

    <div class="board-deck">
      <div v-if="!compact" class="board-stats">
      <p class="board-stats-line"><span>On chain stats</span><span class="board-stats-note">Interface preview / no live feed</span></p>
      <dl class="atlas-facts board-stats-grid" aria-label="On chain stats preview">
        <div v-for="stat in stats" :key="stat.label">
          <dt>{{ stat.label }}<span class="atlas-pill atlas-pill--beam board-preview-badge">Preview</span></dt>
          <dd>—</dd>
          <dd>{{ stat.detail }}</dd>
        </div>
      </dl>
    </div>

    <div class="board-toolbar">
      <p class="atlas-label">Cap +5% / 30-day epoch / model values per unit</p>
      <p v-if="props.query.trim()" class="board-search-state" aria-live="polite">{{ rows.length }} result{{ rows.length === 1 ? '' : 's' }} for “{{ props.query.trim() }}”</p>
    </div>

    <div v-if="rows.length" class="atlas-table-wrap board-table-wrap">
      <table class="atlas-table board-grid">
        <caption class="sr-only">Model market values. Quotes are examples and are not live prices.</caption>
        <thead>
          <tr>
            <th scope="col">Asset</th>
            <th scope="col" class="atlas-num">Cap</th>
            <th scope="col" class="atlas-num" :class="{ 'is-loud': activeSide === 'income' }">Income</th>
            <th scope="col" class="atlas-num" :class="{ 'is-loud': activeSide === 'upside' }">Upside</th>
            <th scope="col" class="atlas-num">Epoch</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="asset in rows" :key="asset.symbol">
            <td>
              <a class="board-token" :href="`/app/markets/${asset.symbol}`" :aria-label="`Open ${asset.symbol} market, example quote ${money(asset.spot)}`" @click.prevent="navigate(asset.symbol)">
                <span class="board-token-mark" aria-hidden="true">{{ asset.initials }}</span>
                <span class="board-token-name"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
              </a>
            </td>
            <td class="atlas-num"><span class="board-cap">+5%</span></td>
            <td class="atlas-num" :class="{ 'is-loud': activeSide === 'income' }"><span class="board-value board-value--income">{{ money(asset.payoff.incomePrice) }}</span><small class="board-quote-tag">Model</small></td>
            <td class="atlas-num" :class="{ 'is-loud': activeSide === 'upside' }"><span class="board-value board-value--upside">{{ money(asset.payoff.upsidePrice) }}</span><small class="board-quote-tag">Model</small></td>
            <td class="atlas-num"><span class="board-epoch">30 days</span></td>
            <td><span class="atlas-pill"><i aria-hidden="true"></i>Model</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="rows.length" class="board-rail" aria-label="Market cards">
      <a v-for="asset in rows" :key="`card-${asset.symbol}`" class="board-card" :href="`/app/markets/${asset.symbol}`" @click.prevent="navigate(asset.symbol)">
        <span class="board-token-mark" aria-hidden="true">{{ asset.initials }}</span>
        <span class="board-card-copy"><b>{{ asset.symbol }}</b><small>{{ asset.name }} / Example quote</small></span>
        <span class="board-card-values"><span><small>Income</small><b>{{ money(asset.payoff.incomePrice) }}</b></span><span><small>Upside</small><b>{{ money(asset.payoff.upsidePrice) }}</b></span><ArrowRight :size="14" /></span>
      </a>
    </div>
    <div v-else class="atlas-notice atlas-notice--flag board-empty" role="status" aria-live="polite">
      <p>No model markets match “{{ props.query.trim() }}”.</p>
      <button class="atlas-btn" type="button" @click="resetSearch">Reset search</button>
    </div>

    <div class="board-foot">
      <span>Indicative model values use a 30-day epoch and 25% volatility.</span>
      <span>Example quotes are not live prices.</span>
    </div>
    </div>
  </section>
</template>

<style scoped>
/* ------------------------------------------------------------------ heading */
.board-block { display: grid; gap: 0; min-width: 0; }
.board-deck { display: grid; gap: 0; min-width: 0; }
.board-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-bottom: clamp(18px, 2vw, 28px);
}
.board-feed { display: inline-flex; align-items: center; gap: 9px; }
.board-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--mint);
  box-shadow: 0 0 10px rgba(92, 225, 160, 0.9);
}

/* -------------------------------------------------------------------- stats */
.board-stats { display: grid; gap: 12px; margin-bottom: clamp(18px, 2vw, 26px); }
.board-stats-line {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  margin: 0;
  color: var(--star);
  font: 500 10px/1.3 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.board-stats-note { color: var(--star-faint); font-weight: 400; letter-spacing: 0.1em; }
.board-stats-grid { --cols: 4; margin: 0; }
.board-stats-grid dt { display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
.board-stats-grid dd + dd { color: var(--star-faint); }
.board-preview-badge { padding: 3px 8px; }

/* ------------------------------------------------------------------ toolbar */
.board-toolbar {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.board-search-state { margin: 0; color: var(--beam); font: 500 10px/1.6 var(--font-mono); letter-spacing: 0.06em; }

/* -------------------------------------------------------------------- table */
.board-table-wrap { border-radius: var(--r-md); }
.board-grid { min-width: 700px; }
.board-grid thead th.is-loud { color: var(--beam); border-bottom-color: rgba(64, 179, 255, 0.5); }
.board-grid tbody td.is-loud { background: rgba(64, 179, 255, 0.07); }
.board-grid tbody td.is-loud .board-value { color: var(--beam); }
.board-token { display: inline-flex; align-items: center; gap: 11px; text-decoration: none; }
.board-token-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--deck-3);
  color: var(--star-2);
  font: 500 11px/1 var(--font-mono);
  box-shadow: inset 0 0 0 1px var(--hair-2);
}
.board-token-name { display: grid; gap: 2px; min-width: 0; }
.board-token-name b { font: 500 13px/1.2 var(--font-mono); letter-spacing: 0.04em; }
.board-token-name small { color: var(--star-faint); font: 400 10px/1.2 var(--font-body); }
.board-cap { color: var(--beam-2); font: 500 12px/1.4 var(--font-mono); }
.board-value { display: block; font: 500 13px/1.4 var(--font-mono); font-variant-numeric: tabular-nums; }
.board-value--income { color: var(--mint); }
.board-value--upside { color: var(--beam-2); }
.board-quote-tag {
  display: block;
  margin-top: 3px;
  color: var(--star-faint);
  font: 400 9px/1.2 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.board-epoch { color: var(--star-mute); font: 400 11px/1.4 var(--font-mono); }

/* --------------------------------------------------------------- card rail */
.board-rail { display: none; }
.board-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  background: var(--void-2);
  color: inherit;
  text-decoration: none;
}
.board-card-copy { display: grid; gap: 2px; min-width: 0; }
.board-card-copy b { font: 500 13px/1.2 var(--font-mono); }
.board-card-copy small { overflow: hidden; color: var(--star-faint); font: 400 10px/1.2 var(--font-body); text-overflow: ellipsis; white-space: nowrap; }
.board-card-values { display: flex; align-items: center; gap: 14px; margin-left: auto; }
.board-card-values > span { display: grid; gap: 2px; text-align: right; }
.board-card-values small { color: var(--star-faint); font: 400 9px/1.2 var(--font-mono); letter-spacing: 0.16em; text-transform: uppercase; }
.board-card-values b { font: 500 12px/1.2 var(--font-mono); font-variant-numeric: tabular-nums; }
.board-card-values > span:first-child b { color: var(--mint); }
.board-card-values > span:nth-child(2) b { color: var(--beam-2); }
.board-card-values svg { color: var(--star-faint); }

/* -------------------------------------------------------------- empty + foot */
.board-empty { justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; margin-top: 8px; }
.board-empty p { margin: 0; }
.board-foot {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid var(--hair);
  color: var(--star-faint);
  font: 400 10px/1.7 var(--font-mono);
}

/* ------------------------------------------------------------------ compact */
.board-block--compact .board-grid { min-width: 0; table-layout: fixed; }
.board-block--compact .board-grid th:nth-child(5), .board-block--compact .board-grid td:nth-child(5),
.board-block--compact .board-grid th:nth-child(6), .board-block--compact .board-grid td:nth-child(6) { display: none; }
.board-block--compact .board-grid th, .board-block--compact .board-grid td { padding-inline: 8px; }
.board-block--compact .board-grid th:first-child, .board-block--compact .board-grid td:first-child { width: 42%; }

/* --------------------------------------------------------------- responsive */
@media (max-width: 780px) {
  .board-head { align-items: flex-start; flex-direction: column; gap: 8px; }
  .board-stats-line { align-items: flex-start; flex-direction: column; gap: 6px; }
  .board-toolbar { flex-direction: column; gap: 6px; }
}
@media (max-width: 580px) {
  .board-table-wrap { display: none; }
  .board-rail { display: grid; gap: 10px; }
  .board-foot { flex-direction: column; gap: 4px; }
}
</style>
