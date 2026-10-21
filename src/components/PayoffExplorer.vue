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
  <section id="cap" class="opt" aria-labelledby="cap-heading">
    <div class="pfx-grid">
      <div class="pfx-dial">
        <h2 id="cap-heading" class="tty-h2">A defined level.<br />A clear split.</h2>
        <p class="pfx-lead">Choose the cap. K is fixed for the epoch.</p>
        <p class="pfx-copy">Set a cap, move the settlement slider, and inspect how the illustrative value splits between Income and Upside. No order or wallet action is created.</p>

        <div class="pfx-control">
          <div class="pfx-control-label"><label for="cap-range">Cap</label><output for="cap-range">+{{ cap }}%</output></div>
          <div class="pfx-range" :style="{ '--range-fill': `${cap * 10}%` }">
            <span class="pfx-range-track" aria-hidden="true"><i></i></span>
            <input id="cap-range" v-model.number="cap" class="tty-range" type="range" min="0" max="10" step="1" :aria-valuetext="`${cap}% cap, strike ${money(model.strike)}`" aria-describedby="cap-model-note" />
          </div>
          <div class="pfx-ticks" aria-hidden="true"><span>0%</span><span>2%</span><span :class="{ 'on': cap === 5 }">5%</span><span>10%</span></div>
          <p id="cap-model-note" class="pfx-model-note">{{ asset }} example at <span>{{ money(model.spot) }}</span> / cap price (K) <span>{{ money(model.strike) }}</span> / 30 days / model at 25% vol</p>
        </div>
      </div>

      <div class="pfx-instrument">
        <div class="tty-face pfx-chart-card">
          <div class="pfx-chart-head">
            <div class="pfx-chart-titles">
              <h3>{{ asset }} value at settlement</h3>
              <p>Per unit / {{ asset }} example at {{ money(model.spot) }} / cap +{{ cap }}% / K {{ money(model.strike) }}</p>
            </div>
            <button class="tty-btn pfx-toggle" type="button" :aria-pressed="showTable" aria-controls="payoff-display" @click="showTable = !showTable">{{ showTable ? 'Chart' : 'Table' }}</button>
          </div>

          <ul class="pfx-legend" aria-label="Chart legend"><li class="pfx-legend-stock">{{ asset }} market unit</li><li class="pfx-legend-income">Income</li><li class="pfx-legend-upside">Upside</li></ul>

          <div id="payoff-display" class="pfx-display">
            <div v-if="showTable" class="pfx-table-wrap" tabindex="0" role="region" aria-label="Settlement values table">
              <table class="tty-table pfx-table"><caption>Per-unit settlement value, before premium</caption><thead><tr><th scope="col">Stock price</th><th scope="col" class="tty-num">Income</th><th scope="col" class="tty-num">Upside</th></tr></thead><tbody><tr v-for="row in tableRows" :key="row.price" :class="{ 'sel': row.price === settlement }"><th scope="row">{{ money(row.price) }}<span v-if="row.price === settlement" class="pfx-current">Current</span></th><td class="tty-num">{{ money(row.income) }}</td><td class="tty-num">{{ money(row.upside) }}</td></tr></tbody></table>
            </div>
            <svg v-else class="pfx-chart" viewBox="0 0 650 320" role="img" aria-labelledby="payoff-chart-title payoff-chart-description">
              <title id="payoff-chart-title">Stock, Income and Upside settlement values</title><desc id="payoff-chart-description">{{ chartDescription }}</desc>
              <g class="pfx-grid-lines"><template v-for="tick in gridTicks" :key="tick"><line x1="74" x2="528" :y1="y(tick)" :y2="y(tick)"/><text x="63" :y="y(tick) + 5" text-anchor="end">{{ money(tick) }}</text></template></g>
              <g class="pfx-axis"><text v-for="tick in [low, model.spot, high]" :key="tick" :x="x(tick)" y="301" text-anchor="middle">{{ money(tick) }}</text></g>
              <line class="pfx-strike" :x1="x(model.strike)" :x2="x(model.strike)" y1="44" y2="276"/><text class="pfx-cap-label" :x="x(model.strike)" y="34" text-anchor="middle">K {{ money(model.strike) }}</text>
              <text class="pfx-cap-label" :x="x(model.spot)" y="14" text-anchor="middle">SPOT {{ money(model.spot) }}</text>
              <path class="pfx-line-stock" :d="stockPath"/><path class="pfx-line-income" :d="incomePath"/><path class="pfx-line-upside" :d="upsidePath"/>
              <line class="pfx-settle-line" :x1="x(settlement)" :x2="x(settlement)" y1="44" y2="276"/>
              <text class="pfx-settle-label" :x="x(settlement) + (settlement > 285 ? -12 : 12)" y="66" :text-anchor="settlement > 285 ? 'end' : 'start'">S {{ money(settlement) }}</text>
              <circle class="pfx-dot-income" :cx="x(settlement)" :cy="y(model.incomeSettlement)" r="7"/><circle class="pfx-dot-upside" :cx="x(settlement)" :cy="y(model.upsideSettlement)" r="8"/>
              <g class="pfx-endpoint"><circle cx="541" :cy="y(high)" r="3.5"/><text x="550" :y="y(high) + 5">{{ money(high) }}</text></g>
              <g class="pfx-endpoint"><circle cx="541" :cy="y(model.strike)" r="3.5"/><text x="550" :y="y(model.strike) + 5">{{ money(model.strike) }}</text></g>
              <g class="pfx-endpoint"><circle cx="541" :cy="y(high - model.strike)" r="3.5"/><text x="550" :y="y(high - model.strike) + 5">{{ money(high - model.strike) }}</text></g>
            </svg>
          </div>

          <div class="pfx-settle">
            <div class="pfx-settle-label"><label for="settlement-range">Settlement price S</label><output for="settlement-range">{{ money(settlement) }} <small>{{ change }} vs spot</small></output></div>
            <div class="pfx-range" :style="{ '--range-fill': `${(settlement - low) / (high - low) * 100}%` }">
              <span class="pfx-range-track" aria-hidden="true"><i></i></span>
              <input id="settlement-range" v-model.number="settlement" class="tty-range" type="range" :min="low" :max="high" :step="Math.max(props.spot / 100, 0.000001)" :aria-valuetext="`${money(settlement)}, ${change} versus initial stock price`" aria-describedby="settlement-summary" />
            </div>
          </div>
          <div id="settlement-summary" class="pfx-values" aria-live="polite" aria-atomic="true">
            <div class="pfx-value-row"><span class="pfx-value-label pfx-legend-income">Income /<br> min(S, K)</span><div><strong>{{ money(model.incomeSettlement) }}</strong><small> + premium {{ money(model.premium) }} if subscribed (model)<br> = {{ money(model.incomeWithPremium) }}</small></div></div>
            <div class="pfx-value-row"><span class="pfx-value-label pfx-legend-upside">Upside / max(S - K, 0)</span><div><strong>{{ money(model.upsideSettlement) }}</strong><small> breakeven {{ money(model.breakeven) }} (model)</small></div></div>
          </div>
          <p class="pfx-disclaimer">Indicative premium <b>{{ money(model.premium) }}</b> per unit / model at 25% vol / 30 days / the auction sets the price. Values per unit; Income is paid in SPL market units worth min(S, K); the premium goes to subscribers only.</p>
        </div>

        <div class="pfx-meters">
          <div class="pfx-meter pfx-meter--income"><div class="pfx-meter-label"><span class="pfx-meter-mark"><ArrowDown :size="14" /></span><b>INCOME</b><span>(Up to the cap)</span></div><div class="pfx-meter-price"><strong>{{ money(model.incomePrice) }}</strong><span>~{{ model.incomeShare.toFixed(1) }}%</span></div><div class="pfx-meter-track" aria-hidden="true"><span :style="{ width: `${model.incomeShare}%` }"></span></div></div>
          <div class="pfx-meter pfx-meter--upside"><div class="pfx-meter-label"><span class="pfx-meter-mark"><ArrowUp :size="14" /></span><b>UPSIDE</b><span>(Above the cap)</span></div><div class="pfx-meter-price"><strong>{{ money(model.upsidePrice) }}</strong><span>~{{ model.upsideShare.toFixed(1) }}%</span></div><div class="pfx-meter-track" aria-hidden="true"><span :style="{ width: `${model.upsideShare}%` }"></span></div></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* -------------------------------------------------------------------- grid */
.opt { min-width: 0; scroll-margin-top: 120px; }
.pfx-grid {
  display: grid;
  grid-template-columns: minmax(0, 240px) minmax(0, 1fr);
  gap: clamp(18px, 2.4vw, 32px);
  align-items: start;
}
.pfx-dial { display: grid; gap: 12px; align-content: start; min-width: 0; }
.pfx-lead {
  margin: 0;
  color: var(--accent-safe);
  font: 500 10px/1.5 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.pfx-copy { margin: 0; color: var(--muted); font: 400 13px/1.7 var(--font-body); }
.pfx-control { margin-top: 6px; display: grid; gap: 6px; }
.pfx-control-label,
.pfx-settle-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.pfx-control-label output,
.pfx-settle-label output { color: var(--ink); font-size: 12px; letter-spacing: 0.02em; }
.pfx-settle-label output small { color: var(--faint); font-size: 9px; }
.pfx-ticks { display: flex; justify-content: space-between; color: var(--faint); font: 400 10px/1 var(--font-mono); }
.pfx-ticks .on { color: var(--accent-safe); font-weight: 500; }
.pfx-model-note { margin: 6px 0 0; color: var(--faint); font: 400 10px/1.7 var(--font-mono); }
.pfx-model-note span { color: var(--ink-2); }

/* ------------------------------------------------------------------ range */
.pfx-range { position: relative; display: grid; align-items: center; }
.pfx-range-track {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 6px;
  transform: translateY(-50%);
  border-radius: var(--radius-pill);
  background: var(--surface-3);
  overflow: hidden;
  pointer-events: none;
}
.pfx-range-track i {
  display: block;
  width: var(--range-fill, 0%);
  height: 100%;
  border-radius: var(--radius-pill);
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
}
.pfx-range .tty-range {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 26px;
  margin: 0;
  appearance: none;
  -webkit-appearance: none;
  background: transparent;
  cursor: ew-resize;
}
.pfx-range .tty-range::-webkit-slider-runnable-track { height: 26px; border: 0; background: transparent; }
.pfx-range .tty-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  margin-top: 5px;
  border: 2px solid #050608;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 18px rgba(255, 0, 0, 0.7);
}
.pfx-range .tty-range::-moz-range-track { height: 26px; border: 0; background: transparent; }
.pfx-range .tty-range::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border: 2px solid #050608;
  border-radius: 50%;
  background: var(--accent);
}

/* -------------------------------------------------------------- instrument */
.pfx-instrument { display: grid; gap: 16px; min-width: 0; }
.pfx-chart-card { display: grid; gap: 14px; }
.pfx-chart-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.pfx-chart-titles h3 { margin: 0; font: 500 15px/1.3 var(--font-body); }
.pfx-chart-titles p { margin: 5px 0 0; color: var(--faint); font: 400 10px/1.7 var(--font-mono); }
.pfx-toggle { min-height: 34px; padding: 0 14px; flex: none; }
.pfx-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--faint);
  font: 400 9px/1 var(--font-mono);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.pfx-legend li { position: relative; padding-left: 15px; }
.pfx-legend li::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  width: 8px;
  height: 3px;
  border-radius: 2px;
  background: currentColor;
}
.pfx-legend-stock { color: var(--ink); }
.pfx-legend-income { color: var(--mint); }
.pfx-legend-upside { color: var(--accent-2); }

.pfx-display {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--surface-2), var(--bg-2));
  overflow: hidden;
}
.pfx-chart { display: block; width: 100%; height: auto; }
.pfx-grid-lines line { stroke: var(--line); stroke-width: 1; }
.pfx-grid-lines text { fill: var(--faint); font-family: var(--font-mono); font-size: 11px; font-variant-numeric: tabular-nums; }
.pfx-axis text { fill: var(--muted); font-family: var(--font-mono); font-size: 11px; font-variant-numeric: tabular-nums; }
.pfx-strike { stroke: var(--accent); stroke-width: 2; }
.pfx-cap-label { fill: var(--accent); font-family: var(--font-mono); font-size: 11px; font-weight: 500; letter-spacing: 0.02em; }
.pfx-line-stock { fill: none; stroke: var(--ink); stroke-width: 2; }
.pfx-line-income { fill: none; stroke: var(--mint); stroke-width: 2.5; }
.pfx-line-upside { fill: none; stroke: var(--accent-2); stroke-width: 2.5; }
.pfx-settle-line { stroke: var(--muted); stroke-width: 1; stroke-dasharray: 5 4; }
.pfx-settle-label { fill: var(--ink); font-family: var(--font-mono); font-size: 11px; font-weight: 500; }
.pfx-dot-income { fill: var(--mint); stroke: #050608; stroke-width: 2; }
.pfx-dot-upside { fill: var(--accent-2); stroke: #050608; stroke-width: 2; }
.pfx-endpoint circle { fill: var(--muted); }
.pfx-endpoint text { fill: var(--muted); font-family: var(--font-mono); font-size: 11px; font-variant-numeric: tabular-nums; }

.pfx-table-wrap { overflow-x: auto; }
.pfx-table caption {
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
  color: var(--faint);
  font: 400 10px/1.5 var(--font-mono);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.pfx-table th[scope='row'] {
  padding-inline: 14px;
  font: 500 13px/1.4 var(--font-mono);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.pfx-current {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  background: rgba(255, 0, 0, 0.16);
  color: var(--accent-safe);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  vertical-align: 2px;
}

/* ---------------------------------------------------------------- settlement */
.pfx-settle { display: grid; gap: 6px; }
.pfx-values {
  display: grid;
  gap: 0;
  border-top: 1px solid var(--line);
}
.pfx-value-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--line);
}
.pfx-value-label { font: 500 9px/1.6 var(--font-mono); letter-spacing: 0.14em; text-transform: uppercase; }
.pfx-value-row > div { text-align: right; }
.pfx-value-row strong { font: 500 20px/1.2 var(--font-mono); font-variant-numeric: tabular-nums; color: var(--ink); }
.pfx-value-row small { display: block; margin-top: 4px; color: var(--faint); font: 400 10px/1.6 var(--font-mono); }
.pfx-disclaimer {
  margin: 0;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  color: var(--faint);
  font: 400 10px/1.8 var(--font-mono);
}
.pfx-disclaimer b { color: var(--ink); }

/* ------------------------------------------------------------------ meters */
.pfx-meters {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.pfx-meter {
  display: grid;
  gap: 12px;
  min-width: 0;
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--bg-2);
}
.pfx-meter--income { background: linear-gradient(160deg, rgba(92, 225, 160, 0.08), var(--bg-2)); }
.pfx-meter--upside { background: linear-gradient(160deg, rgba(255, 0, 200, 0.1), var(--bg-2)); }
.pfx-meter-label { display: flex; align-items: center; gap: 9px; }
.pfx-meter-label b { font: 500 10px/1 var(--font-mono); letter-spacing: 0.18em; }
.pfx-meter-label > span:last-child { color: var(--faint); font: 400 10px/1.3 var(--font-mono); }
.pfx-meter-mark {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  color: #050608;
}
.pfx-meter--income .pfx-meter-mark { background: var(--mint); box-shadow: 0 0 18px rgba(92, 225, 160, 0.45); }
.pfx-meter--upside .pfx-meter-mark { background: var(--accent-2); box-shadow: 0 0 18px rgba(255, 0, 200, 0.45); }
.pfx-meter-price { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
.pfx-meter-price strong { font: 400 22px/1.1 var(--font-display); font-variant-numeric: tabular-nums; }
.pfx-meter-price span { color: var(--muted); font: 400 11px/1.3 var(--font-mono); font-variant-numeric: tabular-nums; }
.pfx-meter-track { height: 4px; border-radius: var(--radius-pill); background: var(--surface-3); overflow: hidden; }
.pfx-meter-track span { display: block; height: 100%; border-radius: var(--radius-pill); }
.pfx-meter--income .pfx-meter-track span { background: var(--mint); }
.pfx-meter--upside .pfx-meter-track span { background: var(--accent-2); }

/* --------------------------------------------------------------- responsive */
@media (max-width: 1100px) {
  .pfx-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 520px) {
  .pfx-meters { grid-template-columns: minmax(0, 1fr); }
  .pfx-value-row { grid-template-columns: minmax(0, 1fr); }
  .pfx-value-row > div { text-align: left; }
}
</style>
