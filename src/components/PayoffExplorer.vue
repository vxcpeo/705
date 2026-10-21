<script setup>
import { computed, ref, watch } from 'vue'
import { ArrowDown, ArrowUp } from 'lucide-vue-next'
import { calculatePayoff } from '../payoff.js'

const props = defineProps({ spot: { type: Number, default: 250 }, asset: { type: String, default: 'SOL' } })
const cap = ref(5)
const settlement = ref(props.spot)
const showTable = ref(false)
watch(() => props.spot, spot => { settlement.value = spot })
const model = computed(() => calculatePayoff({ spot: props.spot, capPercent: cap.value, settlementPrice: settlement.value }))
const money = value => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value)
const change = computed(() => `${model.value.spotChangePercent > 0 ? '+' : ''}${model.value.spotChangePercent.toFixed(1)}%`)
const low = computed(() => props.spot * 0.7)
const high = computed(() => props.spot * 1.3)
const chartMax = computed(() => Math.max(high.value * 1.45, 2))
const gridTicks = computed(() => Array.from({ length: 5 }, (_, index) => chartMax.value * index / 4))
const x = value => 74 + (value - low.value) / (high.value - low.value) * 454
const y = value => 276 - value / chartMax.value * 232
const stockPath = computed(() => `M ${x(low.value)} ${y(low.value)} L ${x(high.value)} ${y(high.value)}`)
const incomePath = computed(() => `M ${x(low.value)} ${y(low.value)} L ${x(model.value.strike)} ${y(model.value.strike)} L ${x(high.value)} ${y(model.value.strike)}`)
const upsidePath = computed(() => `M ${x(low.value)} ${y(0)} L ${x(model.value.strike)} ${y(0)} L ${x(high.value)} ${y(high.value - model.value.strike)}`)
const tableRows = computed(() => [...new Set([low.value, props.spot, model.value.strike, high.value, settlement.value])].sort((a, b) => a - b).map(price => ({
  price,
  income: Math.min(price, model.value.strike),
  upside: Math.max(price - model.value.strike, 0),
})))
const chartDescription = computed(() => `At a settlement price of ${money(settlement.value)}, Income is worth ${money(model.value.incomeSettlement)} and Upside is worth ${money(model.value.upsideSettlement)} per unit. Income follows the stock up to the cap of ${money(model.value.strike)}. Upside receives any amount above the cap.`)
</script>

<template>
  <section id="cap" class="buoy" aria-labelledby="cap-heading">
    <div class="buoy-grid">
      <div class="buoy-dial">
        <h2 id="cap-heading" class="tide-h2">A defined level.<br />A clear split.</h2>
        <p class="buoy-lead">Choose the cap. K is fixed for the epoch.</p>
        <p class="buoy-copy">Set a cap, move the settlement slider, and inspect how the illustrative value splits between Income and Upside. No order or wallet action is created.</p>

        <div class="buoy-control">
          <div class="buoy-control-label"><label for="cap-range">Cap</label><output for="cap-range">+{{ cap }}%</output></div>
          <div class="buoy-range" :style="{ '--range-fill': `${cap * 10}%` }">
            <span class="buoy-range-track" aria-hidden="true"><i></i></span>
            <input id="cap-range" v-model.number="cap" class="tide-range" type="range" min="0" max="10" step="1" :aria-valuetext="`${cap}% cap, strike ${money(model.strike)}`" aria-describedby="cap-model-note" />
          </div>
          <div class="buoy-ticks" aria-hidden="true"><span>0%</span><span>2%</span><span :class="{ 'is-on': cap === 5 }">5%</span><span>10%</span></div>
          <p id="cap-model-note" class="buoy-model-note">{{ asset }} example at <span>{{ money(model.spot) }}</span> / cap price (K) <span>{{ money(model.strike) }}</span> / 30 days / model at 25% vol</p>
        </div>
      </div>

      <div class="buoy-instrument">
        <div class="buoy-chart-card">
          <div class="buoy-chart-head">
            <div class="buoy-chart-titles">
              <h3 class="tide-h3">{{ asset }} value at settlement</h3>
              <p>Per unit / {{ asset }} example at {{ money(model.spot) }} / cap +{{ cap }}% / K {{ money(model.strike) }}</p>
            </div>
            <button class="tide-btn tide-btn--quiet buoy-toggle" type="button" :aria-pressed="showTable" aria-controls="payoff-display" @click="showTable = !showTable">{{ showTable ? 'Chart' : 'Table' }}</button>
          </div>

          <ul class="buoy-legend" aria-label="Chart legend"><li class="buoy-legend-stock">{{ asset }} market unit</li><li class="buoy-legend-income">Income</li><li class="buoy-legend-upside">Upside</li></ul>

          <div id="payoff-display" class="buoy-display">
            <div v-if="showTable" class="buoy-table-wrap" tabindex="0" role="region" aria-label="Settlement values table">
              <table class="tide-table buoy-table"><caption>Per-unit settlement value, before premium</caption><thead><tr><th scope="col">Stock price</th><th scope="col" class="tide-num">Income</th><th scope="col" class="tide-num">Upside</th></tr></thead><tbody><tr v-for="row in tableRows" :key="row.price" :class="{ 'is-sel': row.price === settlement }"><th scope="row">{{ money(row.price) }}<span v-if="row.price === settlement" class="buoy-current">Current</span></th><td class="tide-num">{{ money(row.income) }}</td><td class="tide-num">{{ money(row.upside) }}</td></tr></tbody></table>
            </div>
            <svg v-else class="buoy-chart" viewBox="0 0 650 320" role="img" aria-labelledby="payoff-chart-title payoff-chart-description">
              <title id="payoff-chart-title">Stock, Income and Upside settlement values</title><desc id="payoff-chart-description">{{ chartDescription }}</desc>
              <g class="buoy-grid-lines"><template v-for="tick in gridTicks" :key="tick"><line x1="74" x2="528" :y1="y(tick)" :y2="y(tick)"/><text x="63" :y="y(tick) + 5" text-anchor="end">{{ money(tick) }}</text></template></g>
              <g class="buoy-axis"><text v-for="tick in [low, model.spot, high]" :key="tick" :x="x(tick)" y="301" text-anchor="middle">{{ money(tick) }}</text></g>
              <line class="buoy-strike" :x1="x(model.strike)" :x2="x(model.strike)" y1="44" y2="276"/><text class="buoy-cap-label" :x="x(model.strike)" y="34" text-anchor="middle">K {{ money(model.strike) }}</text>
              <text class="buoy-cap-label" :x="x(model.spot)" y="14" text-anchor="middle">SPOT {{ money(model.spot) }}</text>
              <path class="buoy-line-stock" :d="stockPath"/><path class="buoy-line-income" :d="incomePath"/><path class="buoy-line-upside" :d="upsidePath"/>
              <line class="buoy-settle-line" :x1="x(settlement)" :x2="x(settlement)" y1="44" y2="276"/>
              <text class="buoy-settle-label" :x="x(settlement) + (settlement > 285 ? -12 : 12)" y="66" :text-anchor="settlement > 285 ? 'end' : 'start'">S {{ money(settlement) }}</text>
              <circle class="buoy-dot-income" :cx="x(settlement)" :cy="y(model.incomeSettlement)" r="7"/><circle class="buoy-dot-upside" :cx="x(settlement)" :cy="y(model.upsideSettlement)" r="8"/>
              <g class="buoy-endpoint"><circle cx="541" :cy="y(high)" r="3.5"/><text x="550" :y="y(high) + 5">{{ money(high) }}</text></g>
              <g class="buoy-endpoint"><circle cx="541" :cy="y(model.strike)" r="3.5"/><text x="550" :y="y(model.strike) + 5">{{ money(model.strike) }}</text></g>
              <g class="buoy-endpoint"><circle cx="541" :cy="y(high - model.strike)" r="3.5"/><text x="550" :y="y(high - model.strike) + 5">{{ money(high - model.strike) }}</text></g>
            </svg>
          </div>

          <div class="buoy-settle">
            <div class="buoy-settle-label"><label for="settlement-range">Settlement price S</label><output for="settlement-range">{{ money(settlement) }} <small>{{ change }} vs spot</small></output></div>
            <div class="buoy-range" :style="{ '--range-fill': `${(settlement - low) / (high - low) * 100}%` }">
              <span class="buoy-range-track" aria-hidden="true"><i></i></span>
              <input id="settlement-range" v-model.number="settlement" class="tide-range" type="range" :min="low" :max="high" :step="Math.max(props.spot / 100, 0.000001)" :aria-valuetext="`${money(settlement)}, ${change} versus initial stock price`" aria-describedby="settlement-summary" />
            </div>
          </div>
          <div id="settlement-summary" class="buoy-values" aria-live="polite" aria-atomic="true">
            <div class="buoy-value-row"><span class="buoy-value-label buoy-legend-income">Income /<br> min(S, K)</span><div><strong>{{ money(model.incomeSettlement) }}</strong><small> + premium {{ money(model.premium) }} if subscribed (model)<br> = {{ money(model.incomeWithPremium) }}</small></div></div>
            <div class="buoy-value-row"><span class="buoy-value-label buoy-legend-upside">Upside / max(S - K, 0)</span><div><strong>{{ money(model.upsideSettlement) }}</strong><small> breakeven {{ money(model.breakeven) }} (model)</small></div></div>
          </div>
          <p class="buoy-disclaimer">Indicative premium <b>{{ money(model.premium) }}</b> per unit / model at 25% vol / 30 days / the auction sets the price. Values per unit; Income is paid in SPL market units worth min(S, K); the premium goes to subscribers only.</p>
        </div>

        <div class="buoy-meters">
          <div class="buoy-meter buoy-meter--income"><div class="buoy-meter-label"><span class="buoy-meter-mark"><ArrowDown :size="14" /></span><b>INCOME</b><span>(Up to the cap)</span></div><div class="buoy-meter-price"><strong>{{ money(model.incomePrice) }}</strong><span>~{{ model.incomeShare.toFixed(1) }}%</span></div><div class="buoy-meter-track" aria-hidden="true"><span :style="{ width: `${model.incomeShare}%` }"></span></div></div>
          <div class="buoy-meter buoy-meter--upside"><div class="buoy-meter-label"><span class="buoy-meter-mark"><ArrowUp :size="14" /></span><b>UPSIDE</b><span>(Above the cap)</span></div><div class="buoy-meter-price"><strong>{{ money(model.upsidePrice) }}</strong><span>~{{ model.upsideShare.toFixed(1) }}%</span></div><div class="buoy-meter-track" aria-hidden="true"><span :style="{ width: `${model.upsideShare}%` }"></span></div></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.buoy { min-width: 0; }
.buoy-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(18px, 2.6vw, 30px);
  align-items: start;
}
.buoy-dial {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(260px, .9fr);
  gap: 10px clamp(18px, 2.6vw, 34px);
  align-content: start;
  align-items: start;
}
.buoy-dial > h2, .buoy-dial > .buoy-lead, .buoy-dial > .buoy-copy { grid-column: 1; }
.buoy-dial > .buoy-control { grid-column: 2; grid-row: 1 / span 3; margin-block-start: 0; }
.buoy-lead { color: var(--ink); font: 600 15px/1.5 var(--font-body); }
.buoy-copy { max-width: 46ch; color: var(--muted); font: 400 13px/1.7 var(--font-body); }
.buoy-control {
  display: grid;
  gap: 10px;
  margin-block-start: 8px;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface-soft);
}
.buoy-control-label { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; }
.buoy-control-label label { font: 600 13px/1.4 var(--font-body); }
.buoy-control-label output { color: var(--accent-safe); font: 600 18px/1 var(--font-mono); }
.buoy-range { position: relative; display: grid; align-items: center; min-height: 30px; }
.buoy-range-track {
  position: absolute;
  inset-inline: 0;
  height: 8px;
  border-radius: 999px;
  background: var(--line);
  overflow: hidden;
}
.buoy-range-track i {
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: var(--range-fill, 50%);
  background: linear-gradient(90deg, var(--accent), var(--accent-safe));
}
.buoy-range .tide-range { position: relative; z-index: 1; }
.buoy-ticks { display: flex; justify-content: space-between; color: var(--muted); font: 400 10px/1.4 var(--font-mono); }
.buoy-ticks .is-on { color: var(--accent-safe); font-weight: 600; }
.buoy-model-note { color: var(--muted); font: 400 10px/1.7 var(--font-mono); }
.buoy-model-note span { color: var(--ink-soft); }

/* ------------------------------------------------------------- instrument */
.buoy-instrument { display: grid; gap: 14px; min-width: 0; }
.buoy-chart-card {
  display: grid;
  gap: 12px;
  padding: clamp(16px, 2vw, 22px);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface);
  box-shadow: var(--shadow-soft);
}
.buoy-chart-head { display: flex; align-items: start; justify-content: space-between; gap: 16px; }
.buoy-chart-titles { display: grid; gap: 4px; }
.buoy-chart-titles p { color: var(--muted); font: 400 10px/1.6 var(--font-mono); }
.buoy-toggle { flex: none; }
.buoy-legend { display: flex; flex-wrap: wrap; gap: 6px 18px; padding-block-end: 8px; border-block-end: 1px solid var(--line); }
.buoy-legend li {
  position: relative;
  padding-inline-start: 14px;
  color: var(--ink-soft);
  font: 500 10px/1.5 var(--font-mono);
  letter-spacing: .04em;
}
.buoy-legend li::before {
  content: "";
  position: absolute;
  inset-inline-start: 0;
  inset-block-start: .45em;
  width: 8px;
  height: 8px;
  border-radius: 2px;
}
.buoy-legend-stock::before { background: var(--ink); }
.buoy-legend-income::before { background: var(--success); }
.buoy-legend-upside::before { background: var(--accent); }

.buoy-display { min-height: 0; }
.buoy-chart { width: 100%; height: auto; }
.buoy-grid-lines line { stroke: var(--line); stroke-width: 1; }
.buoy-grid-lines text { fill: var(--muted); font: 400 9px/1 var(--font-mono); }
.buoy-axis text { fill: var(--muted); font: 400 9px/1 var(--font-mono); }
.buoy-strike { stroke: var(--accent-safe); stroke-width: 1.5; stroke-dasharray: 4 4; }
.buoy-cap-label { fill: var(--accent-deep); font: 600 10px/1 var(--font-mono); }
.buoy-line-stock { fill: none; stroke: var(--ink); stroke-width: 2.5; }
.buoy-line-income { fill: none; stroke: var(--success); stroke-width: 2.5; }
.buoy-line-upside { fill: none; stroke: var(--accent); stroke-width: 2.5; }
.buoy-settle-line { stroke: var(--ink-soft); stroke-width: 1; stroke-dasharray: 2 4; }
.buoy-settle-label { fill: var(--ink); font: 600 10px/1 var(--font-mono); }
.buoy-dot-income { fill: var(--success); }
.buoy-dot-upside { fill: var(--accent); }
.buoy-endpoint circle { fill: var(--line-strong); }
.buoy-endpoint text { fill: var(--muted); font: 400 9px/1 var(--font-mono); }

.buoy-table-wrap { max-height: 320px; overflow: auto; border: 1px solid var(--line); border-radius: var(--radius-sm); }
.buoy-table { min-width: 420px; }
.buoy-table th { padding: 9px 12px; font-size: 11px; }
.buoy-table td { padding: 9px 12px; font: 500 12px/1.4 var(--font-mono); }
.buoy-table tbody tr.is-sel { background: rgba(41, 141, 255, .08); }
.buoy-current {
  margin-inline-start: 8px;
  padding: 2px 7px;
  border-radius: 999px;
  background: var(--surface-alt);
  color: var(--accent-deep);
  font: 600 9px/1.4 var(--font-mono);
  letter-spacing: .06em;
  text-transform: uppercase;
}

.buoy-settle { display: grid; gap: 10px; padding-block-start: 12px; border-block-start: 1px solid var(--line); }
.buoy-settle-label { display: flex; align-items: baseline; justify-content: space-between; gap: 14px; flex-wrap: wrap; }
.buoy-settle-label label { font: 600 13px/1.4 var(--font-body); }
.buoy-settle-label output { color: var(--ink); font: 600 15px/1 var(--font-mono); }
.buoy-settle-label small { color: var(--muted); font: 500 10px/1 var(--font-mono); }

.buoy-values { display: grid; gap: 1px; background: var(--line); border: 1px solid var(--line); border-radius: var(--radius-sm); overflow: hidden; }
.buoy-value-row {
  display: grid;
  grid-template-columns: minmax(120px, 4fr) minmax(0, 8fr);
  gap: 12px;
  padding: 12px 14px;
  background: var(--surface);
}
.buoy-value-label { color: var(--accent-safe); font: 600 10px/1.5 var(--font-mono); letter-spacing: .04em; }
.buoy-value-row strong { color: var(--ink); font: 600 20px/1.1 var(--font-display); letter-spacing: -.02em; }
.buoy-value-row small { color: var(--muted); font: 400 10px/1.6 var(--font-mono); }
.buoy-disclaimer { color: var(--muted); font: 400 10px/1.7 var(--font-mono); }
.buoy-disclaimer b { color: var(--ink-soft); }

/* ---------------------------------------------------------------- meters */
.buoy-meters { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.buoy-meter {
  display: grid;
  gap: 10px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: var(--surface-soft);
}
.buoy-meter-label { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.buoy-meter-mark {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border-radius: 9px;
  background: var(--surface);
  box-shadow: inset 0 0 0 1px var(--line);
}
.buoy-meter--income .buoy-meter-mark { color: var(--success); }
.buoy-meter--upside .buoy-meter-mark { color: var(--accent-safe); }
.buoy-meter-label b { font: 600 11px/1.3 var(--font-mono); letter-spacing: .12em; }
.buoy-meter-label span:last-child { color: var(--muted); font: 400 10px/1.4 var(--font-mono); }
.buoy-meter-price { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
.buoy-meter-price strong { font: 600 22px/1 var(--font-display); letter-spacing: -.02em; }
.buoy-meter-price span { color: var(--muted); font: 500 11px/1 var(--font-mono); }
.buoy-meter-track { height: 7px; border-radius: 999px; background: var(--line); overflow: hidden; }
.buoy-meter-track span { display: block; height: 100%; border-radius: 999px; }
.buoy-meter--income .buoy-meter-track span { background: var(--success); }
.buoy-meter--upside .buoy-meter-track span { background: var(--accent); }

@media (max-width: 1000px) {
  .buoy-dial { grid-template-columns: minmax(0, 1fr); }
  .buoy-dial > .buoy-control { grid-column: 1; grid-row: auto; }
}
@media (max-width: 640px) {
  .buoy-meters { grid-template-columns: minmax(0, 1fr); }
  .buoy-value-row { grid-template-columns: minmax(0, 1fr); }
  .buoy-chart-head { flex-direction: column; }
}
</style>
