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
  <section id="cap" class="bl-explore" aria-labelledby="cap-heading">
    <div class="bl-bento bl-explore-grid">
      <!-- dial -->
      <div class="bl-tile bl-tile--surface bl-span-4 bl-dial">
        <div class="bl-dial-copy">
          <h2 id="cap-heading" class="bl-h2">A defined level.<br />A clear split.</h2>
          <p class="bl-dial-lead">Choose the cap. K is fixed for the epoch.</p>
          <p class="bl-note">Set a cap, move the settlement slider, and inspect how the illustrative value splits between Income and Upside. No order or wallet action is created.</p>
        </div>

        <div class="bl-dial-control">
          <div class="bl-dial-control-label"><label for="cap-range">Cap</label><output for="cap-range">+{{ cap }}%</output></div>
          <div class="bl-dial-range" :style="{ '--range-fill': `${cap * 10}%` }">
            <span class="bl-dial-track" aria-hidden="true"><i></i></span>
            <input id="cap-range" v-model.number="cap" class="bl-range" type="range" min="0" max="10" step="1" :aria-valuetext="`${cap}% cap, strike ${money(model.strike)}`" aria-describedby="cap-model-note" />
          </div>
          <div class="bl-dial-ticks" aria-hidden="true"><span>0%</span><span>2%</span><span :class="{ 'is-live': cap === 5 }">5%</span><span>10%</span></div>
          <p id="cap-model-note" class="bl-dial-note">{{ asset }} example at <span>{{ money(model.spot) }}</span> / cap price (K) <span>{{ money(model.strike) }}</span> / 30 days / model at 25% vol</p>
        </div>
      </div>

      <!-- instrument -->
      <div class="bl-tile bl-span-8 bl-instrument">
        <div class="bl-instrument-head">
          <div class="bl-instrument-titles">
            <h3 class="bl-h3">{{ asset }} value at settlement</h3>
            <p class="bl-meta">Per unit / {{ asset }} example at {{ money(model.spot) }} / cap +{{ cap }}% / K {{ money(model.strike) }}</p>
          </div>
          <button class="bl-btn bl-btn--quiet" type="button" :aria-pressed="showTable" aria-controls="payoff-display" @click="showTable = !showTable">{{ showTable ? 'Chart' : 'Table' }}</button>
        </div>

        <ul class="bl-legend" aria-label="Chart legend"><li class="bl-legend-stock">{{ asset }} market unit</li><li class="bl-legend-income">Income</li><li class="bl-legend-upside">Upside</li></ul>

        <div id="payoff-display" class="bl-display">
          <div v-if="showTable" class="bl-table-wrap bl-payout-wrap" tabindex="0" role="region" aria-label="Settlement values table">
            <table class="bl-table bl-payout"><caption>Per-unit settlement value, before premium</caption><thead><tr><th scope="col">Stock price</th><th scope="col" class="bl-num">Income</th><th scope="col" class="bl-num">Upside</th></tr></thead><tbody><tr v-for="row in tableRows" :key="row.price" :class="{ 'is-marked': row.price === settlement }"><th scope="row">{{ money(row.price) }}<span v-if="row.price === settlement" class="bl-payout-now">Current</span></th><td class="bl-num">{{ money(row.income) }}</td><td class="bl-num">{{ money(row.upside) }}</td></tr></tbody></table>
          </div>
          <svg v-else class="bl-chart" viewBox="0 0 650 320" role="img" aria-labelledby="payoff-chart-title payoff-chart-description">
            <title id="payoff-chart-title">Stock, Income and Upside settlement values</title><desc id="payoff-chart-description">{{ chartDescription }}</desc>
            <g class="bl-chart-grid"><template v-for="tick in gridTicks" :key="tick"><line x1="74" x2="528" :y1="y(tick)" :y2="y(tick)"/><text x="63" :y="y(tick) + 5" text-anchor="end">{{ money(tick) }}</text></template></g>
            <g class="bl-chart-axis"><text v-for="tick in [low, model.spot, high]" :key="tick" :x="x(tick)" y="301" text-anchor="middle">{{ money(tick) }}</text></g>
            <line class="bl-chart-strike" :x1="x(model.strike)" :x2="x(model.strike)" y1="44" y2="276"/><text class="bl-chart-cap" :x="x(model.strike)" y="34" text-anchor="middle">K {{ money(model.strike) }}</text>
            <text class="bl-chart-cap" :x="x(model.spot)" y="14" text-anchor="middle">SPOT {{ money(model.spot) }}</text>
            <path class="bl-chart-stock" :d="stockPath"/><path class="bl-chart-income" :d="incomePath"/><path class="bl-chart-upside" :d="upsidePath"/>
            <line class="bl-chart-settle" :x1="x(settlement)" :x2="x(settlement)" y1="44" y2="276"/>
            <text class="bl-chart-settle-label" :x="x(settlement) + (settlement > 285 ? -12 : 12)" y="66" :text-anchor="settlement > 285 ? 'end' : 'start'">S {{ money(settlement) }}</text>
            <circle class="bl-chart-dot-income" :cx="x(settlement)" :cy="y(model.incomeSettlement)" r="7"/><circle class="bl-chart-dot-upside" :cx="x(settlement)" :cy="y(model.upsideSettlement)" r="8"/>
            <g class="bl-chart-end"><circle cx="541" :cy="y(high)" r="3.5"/><text x="550" :y="y(high) + 5">{{ money(high) }}</text></g>
            <g class="bl-chart-end"><circle cx="541" :cy="y(model.strike)" r="3.5"/><text x="550" :y="y(model.strike) + 5">{{ money(model.strike) }}</text></g>
            <g class="bl-chart-end"><circle cx="541" :cy="y(high - model.strike)" r="3.5"/><text x="550" :y="y(high - model.strike) + 5">{{ money(high - model.strike) }}</text></g>
          </svg>
        </div>

        <div class="bl-settle">
          <div class="bl-settle-label"><label for="settlement-range">Settlement price S</label><output for="settlement-range">{{ money(settlement) }} <small>{{ change }} vs spot</small></output></div>
          <div class="bl-dial-range" :style="{ '--range-fill': `${(settlement - low) / (high - low) * 100}%` }">
            <span class="bl-dial-track" aria-hidden="true"><i></i></span>
            <input id="settlement-range" v-model.number="settlement" class="bl-range" type="range" :min="low" :max="high" :step="Math.max(props.spot / 100, 0.000001)" :aria-valuetext="`${money(settlement)}, ${change} versus initial stock price`" aria-describedby="settlement-summary" />
          </div>
        </div>

        <div id="settlement-summary" class="bl-values" aria-live="polite" aria-atomic="true">
          <div class="bl-value-row"><span class="bl-value-label bl-legend-income">Income /<br> min(S, K)</span><div><strong>{{ money(model.incomeSettlement) }}</strong><small> + premium {{ money(model.premium) }} if subscribed (model)<br> = {{ money(model.incomeWithPremium) }}</small></div></div>
          <div class="bl-value-row"><span class="bl-value-label bl-legend-upside">Upside / max(S - K, 0)</span><div><strong>{{ money(model.upsideSettlement) }}</strong><small> breakeven {{ money(model.breakeven) }} (model)</small></div></div>
        </div>
        <p class="bl-disclaimer">Indicative premium <b>{{ money(model.premium) }}</b> per unit / model at 25% vol / 30 days / the auction sets the price. Values per unit; Income is paid in SPL market units worth min(S, K); the premium goes to subscribers only.</p>
      </div>

      <!-- meters -->
      <div class="bl-tile bl-meter bl-meter--income bl-span-6">
        <div class="bl-meter-label"><span class="bl-meter-mark"><ArrowDown :size="14" /></span><b>INCOME</b><span>(Up to the cap)</span></div>
        <div class="bl-meter-price"><strong>{{ money(model.incomePrice) }}</strong><span>~{{ model.incomeShare.toFixed(1) }}%</span></div>
        <div class="bl-meter-track" aria-hidden="true"><span :style="{ width: `${model.incomeShare}%` }"></span></div>
      </div>
      <div class="bl-tile bl-meter bl-meter--upside bl-span-6">
        <div class="bl-meter-label"><span class="bl-meter-mark"><ArrowUp :size="14" /></span><b>UPSIDE</b><span>(Above the cap)</span></div>
        <div class="bl-meter-price"><strong>{{ money(model.upsidePrice) }}</strong><span>~{{ model.upsideShare.toFixed(1) }}%</span></div>
        <div class="bl-meter-track" aria-hidden="true"><span :style="{ width: `${model.upsideShare}%` }"></span></div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.bl-explore { min-width: 0; }
.bl-explore-grid { gap: var(--bl-gap); }

/* -------------------------------------------------------------------- dial */
.bl-dial { gap: 18px; align-content: start; }
.bl-dial-copy { display: grid; gap: 10px; }
.bl-dial-lead { color: var(--bl-ink); font: 600 15px/1.5 var(--bl-font-body); }
.bl-dial-control {
  display: grid;
  gap: 10px;
  padding: 16px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-paper);
}
.bl-dial-control-label { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; }
.bl-dial-control-label label { font: 600 13px/1.4 var(--bl-font-body); }
.bl-dial-control-label output { color: var(--bl-accent-safe); font: 600 18px/1 var(--bl-font-mono); }
.bl-dial-range { position: relative; display: grid; align-items: center; min-height: 30px; }
.bl-dial-track {
  position: absolute;
  inset-inline: 0;
  height: 8px;
  border-radius: var(--bl-radius-pill);
  background: var(--bl-surface-2);
  overflow: hidden;
}
.bl-dial-track i {
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: var(--range-fill, 50%);
  background: linear-gradient(90deg, var(--bl-accent-soft), var(--bl-accent));
}
.bl-dial-range .bl-range { position: relative; z-index: 1; }
.bl-dial-ticks { display: flex; justify-content: space-between; color: var(--bl-muted-2); font: 400 10px/1.4 var(--bl-font-mono); }
.bl-dial-ticks .is-live { color: var(--bl-accent-safe); font-weight: 600; }
.bl-dial-note { color: var(--bl-muted); font: 400 10px/1.7 var(--bl-font-mono); }
.bl-dial-note span { color: var(--bl-ink-soft); }

/* -------------------------------------------------------------- instrument */
.bl-instrument { gap: 12px; }
.bl-instrument-head { display: flex; align-items: start; justify-content: space-between; gap: 16px; }
.bl-instrument-titles { display: grid; gap: 4px; }
.bl-instrument-titles p { color: var(--bl-muted); font: 400 10px/1.6 var(--bl-font-mono); }
.bl-legend { display: flex; flex-wrap: wrap; gap: 6px 18px; padding-block-end: 8px; border-block-end: 1px solid var(--bl-line); }
.bl-legend li {
  position: relative;
  padding-inline-start: 14px;
  color: var(--bl-ink-soft);
  font: 500 10px/1.5 var(--bl-font-mono);
  letter-spacing: .04em;
}
.bl-legend li::before {
  content: "";
  position: absolute;
  inset-inline-start: 0;
  inset-block-start: .45em;
  width: 8px;
  height: 8px;
  border-radius: 3px;
}
.bl-legend-stock::before { background: var(--bl-ink); }
.bl-legend-income::before { background: var(--bl-good); }
.bl-legend-upside::before { background: var(--bl-accent); }

.bl-display { min-height: 0; }
.bl-chart { width: 100%; height: auto; }
.bl-chart-grid line { stroke: var(--bl-line); stroke-width: 1; }
.bl-chart-grid text { fill: var(--bl-muted); font: 400 9px/1 var(--bl-font-mono); }
.bl-chart-axis text { fill: var(--bl-muted); font: 400 9px/1 var(--bl-font-mono); }
.bl-chart-strike { stroke: var(--bl-accent-safe); stroke-width: 1.5; stroke-dasharray: 4 4; }
.bl-chart-cap { fill: var(--bl-accent-deep); font: 600 10px/1 var(--bl-font-mono); }
.bl-chart-stock { fill: none; stroke: var(--bl-ink); stroke-width: 2.5; }
.bl-chart-income { fill: none; stroke: var(--bl-good); stroke-width: 2.5; }
.bl-chart-upside { fill: none; stroke: var(--bl-accent); stroke-width: 2.5; }
.bl-chart-settle { stroke: var(--bl-ink-soft); stroke-width: 1; stroke-dasharray: 2 4; }
.bl-chart-settle-label { fill: var(--bl-ink); font: 600 10px/1 var(--bl-font-mono); }
.bl-chart-dot-income { fill: var(--bl-good); }
.bl-chart-dot-upside { fill: var(--bl-accent); }
.bl-chart-end circle { fill: var(--bl-line-2); }
.bl-chart-end text { fill: var(--bl-muted); font: 400 9px/1 var(--bl-font-mono); }

.bl-payout-wrap { max-height: 320px; overflow: auto; border: 1px solid var(--bl-line); border-radius: var(--bl-r-sm); }
.bl-payout { min-width: 420px; }
.bl-payout th { padding: 9px 12px; font-size: 11px; }
.bl-payout td { padding: 9px 12px; font: 500 12px/1.4 var(--bl-font-mono); }
.bl-payout tbody tr.is-marked { background: var(--bl-tint); }
.bl-payout-now {
  margin-inline-start: 8px;
  padding: 2px 7px;
  border-radius: var(--bl-radius-pill);
  background: var(--bl-surface-2);
  color: var(--bl-accent-deep);
  font: 600 9px/1.4 var(--bl-font-mono);
  letter-spacing: .06em;
  text-transform: uppercase;
}

.bl-settle { display: grid; gap: 10px; padding-block-start: 12px; border-block-start: 1px solid var(--bl-line); }
.bl-settle-label { display: flex; align-items: baseline; justify-content: space-between; gap: 14px; flex-wrap: wrap; }
.bl-settle-label label { font: 600 13px/1.4 var(--bl-font-body); }
.bl-settle-label output { color: var(--bl-ink); font: 600 15px/1 var(--bl-font-mono); }
.bl-settle-label small { color: var(--bl-muted); font: 500 10px/1 var(--bl-font-mono); }

.bl-values { display: grid; gap: 8px; }
.bl-value-row {
  display: grid;
  grid-template-columns: minmax(120px, 4fr) minmax(0, 8fr);
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-surface);
}
.bl-value-label { color: var(--bl-accent-safe); font: 600 10px/1.5 var(--bl-font-mono); letter-spacing: .04em; }
.bl-value-row strong { color: var(--bl-ink); font: var(--bl-display-weight) 20px/1.1 var(--bl-font-display); letter-spacing: -.02em; }
.bl-value-row small { color: var(--bl-muted); font: 400 10px/1.6 var(--bl-font-mono); }
.bl-disclaimer { color: var(--bl-muted); font: 400 10px/1.7 var(--bl-font-mono); }
.bl-disclaimer b { color: var(--bl-ink-soft); }

/* ------------------------------------------------------------------ meters */
.bl-meter { gap: 10px; }
.bl-meter-label { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.bl-meter-mark {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border-radius: 9px;
  background: var(--bl-tint);
}
.bl-meter--income .bl-meter-mark { color: var(--bl-good); background: rgba(15, 123, 77, .1); }
.bl-meter--upside .bl-meter-mark { color: var(--bl-accent-safe); }
.bl-meter-label b { font: 600 11px/1.3 var(--bl-font-mono); letter-spacing: .08em; }
.bl-meter-label span:last-child { color: var(--bl-muted); font: 400 10px/1.4 var(--bl-font-mono); }
.bl-meter-price { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
.bl-meter-price strong { font: var(--bl-display-weight) 24px/1 var(--bl-font-display); letter-spacing: -.02em; }
.bl-meter-price span { color: var(--bl-muted); font: 500 11px/1 var(--bl-font-mono); }
.bl-meter-track { height: 8px; border-radius: var(--bl-radius-pill); background: var(--bl-surface-2); overflow: hidden; }
.bl-meter-track span { display: block; height: 100%; border-radius: var(--bl-radius-pill); }
.bl-meter--income .bl-meter-track span { background: var(--bl-good); }
.bl-meter--upside .bl-meter-track span { background: linear-gradient(90deg, var(--bl-accent-soft), var(--bl-accent)); }

@media (max-width: 720px) {
  .bl-value-row { grid-template-columns: minmax(0, 1fr); }
  .bl-instrument-head { flex-direction: column; }
}
</style>
