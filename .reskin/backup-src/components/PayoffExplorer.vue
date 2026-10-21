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
    <div class="opt-grid">
      <div class="opt-dial">
        <h2 id="cap-heading" class="atlas-h2">A defined level.<br />A clear split.</h2>
        <p class="opt-lead">Choose the cap. K is fixed for the epoch.</p>
        <p class="opt-copy">Set a cap, move the settlement slider, and inspect how the illustrative value splits between Income and Upside. No order or wallet action is created.</p>

        <div class="opt-control">
          <div class="opt-control-label"><label for="cap-range">Cap</label><output for="cap-range">+{{ cap }}%</output></div>
          <div class="opt-range" :style="{ '--range-fill': `${cap * 10}%` }">
            <span class="opt-range-track" aria-hidden="true"><i></i></span>
            <input id="cap-range" v-model.number="cap" class="atlas-range" type="range" min="0" max="10" step="1" :aria-valuetext="`${cap}% cap, strike ${money(model.strike)}`" aria-describedby="cap-model-note" />
          </div>
          <div class="opt-ticks" aria-hidden="true"><span>0%</span><span>2%</span><span :class="{ 'is-lit': cap === 5 }">5%</span><span>10%</span></div>
          <p id="cap-model-note" class="opt-model-note">{{ asset }} example at <span>{{ money(model.spot) }}</span> / cap price (K) <span>{{ money(model.strike) }}</span> / 30 days / model at 25% vol</p>
        </div>
      </div>

      <div class="opt-instrument">
        <div class="atlas-face opt-chart-card">
          <div class="opt-chart-head">
            <div class="opt-chart-titles">
              <h3>{{ asset }} value at settlement</h3>
              <p>Per unit / {{ asset }} example at {{ money(model.spot) }} / cap +{{ cap }}% / K {{ money(model.strike) }}</p>
            </div>
            <button class="atlas-btn opt-toggle" type="button" :aria-pressed="showTable" aria-controls="payoff-display" @click="showTable = !showTable">{{ showTable ? 'Chart' : 'Table' }}</button>
          </div>

          <ul class="opt-legend" aria-label="Chart legend"><li class="opt-legend-stock">{{ asset }} market unit</li><li class="opt-legend-income">Income</li><li class="opt-legend-upside">Upside</li></ul>

          <div id="payoff-display" class="opt-display">
            <div v-if="showTable" class="opt-table-wrap" tabindex="0" role="region" aria-label="Settlement values table">
              <table class="atlas-table opt-table"><caption>Per-unit settlement value, before premium</caption><thead><tr><th scope="col">Stock price</th><th scope="col" class="atlas-num">Income</th><th scope="col" class="atlas-num">Upside</th></tr></thead><tbody><tr v-for="row in tableRows" :key="row.price" :class="{ 'is-chord': row.price === settlement }"><th scope="row">{{ money(row.price) }}<span v-if="row.price === settlement" class="opt-current">Current</span></th><td class="atlas-num">{{ money(row.income) }}</td><td class="atlas-num">{{ money(row.upside) }}</td></tr></tbody></table>
            </div>
            <svg v-else class="opt-chart" viewBox="0 0 650 320" role="img" aria-labelledby="payoff-chart-title payoff-chart-description">
              <title id="payoff-chart-title">Stock, Income and Upside settlement values</title><desc id="payoff-chart-description">{{ chartDescription }}</desc>
              <g class="opt-grid-lines"><template v-for="tick in gridTicks" :key="tick"><line x1="74" x2="528" :y1="y(tick)" :y2="y(tick)"/><text x="63" :y="y(tick) + 5" text-anchor="end">{{ money(tick) }}</text></template></g>
              <g class="opt-axis"><text v-for="tick in [low, model.spot, high]" :key="tick" :x="x(tick)" y="301" text-anchor="middle">{{ money(tick) }}</text></g>
              <line class="opt-strike" :x1="x(model.strike)" :x2="x(model.strike)" y1="44" y2="276"/><text class="opt-cap-label" :x="x(model.strike)" y="34" text-anchor="middle">K {{ money(model.strike) }}</text>
              <text class="opt-cap-label" :x="x(model.spot)" y="14" text-anchor="middle">SPOT {{ money(model.spot) }}</text>
              <path class="opt-line-stock" :d="stockPath"/><path class="opt-line-income" :d="incomePath"/><path class="opt-line-upside" :d="upsidePath"/>
              <line class="opt-settle-line" :x1="x(settlement)" :x2="x(settlement)" y1="44" y2="276"/>
              <text class="opt-settle-label" :x="x(settlement) + (settlement > 285 ? -12 : 12)" y="66" :text-anchor="settlement > 285 ? 'end' : 'start'">S {{ money(settlement) }}</text>
              <circle class="opt-dot-income" :cx="x(settlement)" :cy="y(model.incomeSettlement)" r="7"/><circle class="opt-dot-upside" :cx="x(settlement)" :cy="y(model.upsideSettlement)" r="8"/>
              <g class="opt-endpoint"><circle cx="541" :cy="y(high)" r="3.5"/><text x="550" :y="y(high) + 5">{{ money(high) }}</text></g>
              <g class="opt-endpoint"><circle cx="541" :cy="y(model.strike)" r="3.5"/><text x="550" :y="y(model.strike) + 5">{{ money(model.strike) }}</text></g>
              <g class="opt-endpoint"><circle cx="541" :cy="y(high - model.strike)" r="3.5"/><text x="550" :y="y(high - model.strike) + 5">{{ money(high - model.strike) }}</text></g>
            </svg>
          </div>

          <div class="opt-settle">
            <div class="opt-settle-label"><label for="settlement-range">Settlement price S</label><output for="settlement-range">{{ money(settlement) }} <small>{{ change }} vs spot</small></output></div>
            <div class="opt-range" :style="{ '--range-fill': `${(settlement - low) / (high - low) * 100}%` }">
              <span class="opt-range-track" aria-hidden="true"><i></i></span>
              <input id="settlement-range" v-model.number="settlement" class="atlas-range" type="range" :min="low" :max="high" :step="Math.max(props.spot / 100, 0.000001)" :aria-valuetext="`${money(settlement)}, ${change} versus initial stock price`" aria-describedby="settlement-summary" />
            </div>
          </div>
          <div id="settlement-summary" class="opt-values" aria-live="polite" aria-atomic="true">
            <div class="opt-value-row"><span class="opt-value-label opt-legend-income">Income /<br> min(S, K)</span><div><strong>{{ money(model.incomeSettlement) }}</strong><small> + premium {{ money(model.premium) }} if subscribed (model)<br> = {{ money(model.incomeWithPremium) }}</small></div></div>
            <div class="opt-value-row"><span class="opt-value-label opt-legend-upside">Upside / max(S - K, 0)</span><div><strong>{{ money(model.upsideSettlement) }}</strong><small> breakeven {{ money(model.breakeven) }} (model)</small></div></div>
          </div>
          <p class="opt-disclaimer">Indicative premium <b>{{ money(model.premium) }}</b> per unit / model at 25% vol / 30 days / the auction sets the price. Values per unit; Income is paid in SPL market units worth min(S, K); the premium goes to subscribers only.</p>
        </div>

        <div class="opt-meters">
          <div class="opt-meter opt-meter--income"><div class="opt-meter-label"><span class="opt-meter-mark"><ArrowDown :size="14" /></span><b>INCOME</b><span>(Up to the cap)</span></div><div class="opt-meter-price"><strong>{{ money(model.incomePrice) }}</strong><span>~{{ model.incomeShare.toFixed(1) }}%</span></div><div class="opt-meter-track" aria-hidden="true"><span :style="{ width: `${model.incomeShare}%` }"></span></div></div>
          <div class="opt-meter opt-meter--upside"><div class="opt-meter-label"><span class="opt-meter-mark"><ArrowUp :size="14" /></span><b>UPSIDE</b><span>(Above the cap)</span></div><div class="opt-meter-price"><strong>{{ money(model.upsidePrice) }}</strong><span>~{{ model.upsideShare.toFixed(1) }}%</span></div><div class="opt-meter-track" aria-hidden="true"><span :style="{ width: `${model.upsideShare}%` }"></span></div></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* -------------------------------------------------------------------- grid */
.opt { min-width: 0; scroll-margin-top: 120px; }
.opt-grid {
  display: grid;
  grid-template-columns: minmax(0, 240px) minmax(0, 1fr);
  gap: clamp(18px, 2.4vw, 32px);
  align-items: start;
}
.opt-dial { display: grid; gap: 12px; align-content: start; min-width: 0; }
.opt-lead {
  margin: 0;
  color: var(--beam);
  font: 500 10px/1.5 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.opt-copy { margin: 0; color: var(--star-mute); font: 400 13px/1.7 var(--font-body); }
.opt-control { margin-top: 6px; display: grid; gap: 6px; }
.opt-control-label,
.opt-settle-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  color: var(--star-faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.opt-control-label output,
.opt-settle-label output { color: var(--star); font-size: 12px; letter-spacing: 0.02em; }
.opt-settle-label output small { color: var(--star-faint); font-size: 9px; }
.opt-ticks { display: flex; justify-content: space-between; color: var(--star-faint); font: 400 10px/1 var(--font-mono); }
.opt-ticks .is-lit { color: var(--beam); font-weight: 500; }
.opt-model-note { margin: 6px 0 0; color: var(--star-faint); font: 400 10px/1.7 var(--font-mono); }
.opt-model-note span { color: var(--star-2); }

/* ------------------------------------------------------------------ range */
.opt-range { position: relative; display: grid; align-items: center; }
.opt-range-track {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 6px;
  transform: translateY(-50%);
  border-radius: var(--r-pill);
  background: var(--deck-3);
  overflow: hidden;
  pointer-events: none;
}
.opt-range-track i {
  display: block;
  width: var(--range-fill, 0%);
  height: 100%;
  border-radius: var(--r-pill);
  background: linear-gradient(90deg, var(--beam), var(--beam-2));
}
.opt-range .atlas-range {
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
.opt-range .atlas-range::-webkit-slider-runnable-track { height: 26px; border: 0; background: transparent; }
.opt-range .atlas-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  margin-top: 5px;
  border: 2px solid #04060d;
  border-radius: 50%;
  background: var(--beam);
  box-shadow: 0 0 18px rgba(64, 179, 255, 0.7);
}
.opt-range .atlas-range::-moz-range-track { height: 26px; border: 0; background: transparent; }
.opt-range .atlas-range::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border: 2px solid #04060d;
  border-radius: 50%;
  background: var(--beam);
}

/* -------------------------------------------------------------- instrument */
.opt-instrument { display: grid; gap: 16px; min-width: 0; }
.opt-chart-card { display: grid; gap: 14px; }
.opt-chart-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.opt-chart-titles h3 { margin: 0; font: 500 15px/1.3 var(--font-body); }
.opt-chart-titles p { margin: 5px 0 0; color: var(--star-faint); font: 400 10px/1.7 var(--font-mono); }
.opt-toggle { min-height: 34px; padding: 0 14px; flex: none; }
.opt-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--star-faint);
  font: 400 9px/1 var(--font-mono);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.opt-legend li { position: relative; padding-left: 15px; }
.opt-legend li::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  width: 8px;
  height: 3px;
  border-radius: 2px;
  background: currentColor;
}
.opt-legend-stock { color: var(--star); }
.opt-legend-income { color: var(--mint); }
.opt-legend-upside { color: var(--beam-2); }

.opt-display {
  min-width: 0;
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  background: linear-gradient(180deg, var(--deck-2), var(--void-2));
  overflow: hidden;
}
.opt-chart { display: block; width: 100%; height: auto; }
.opt-grid-lines line { stroke: var(--hair); stroke-width: 1; }
.opt-grid-lines text { fill: var(--star-faint); font-family: var(--font-mono); font-size: 11px; font-variant-numeric: tabular-nums; }
.opt-axis text { fill: var(--star-mute); font-family: var(--font-mono); font-size: 11px; font-variant-numeric: tabular-nums; }
.opt-strike { stroke: var(--beam); stroke-width: 2; }
.opt-cap-label { fill: var(--beam); font-family: var(--font-mono); font-size: 11px; font-weight: 500; letter-spacing: 0.02em; }
.opt-line-stock { fill: none; stroke: var(--star); stroke-width: 2; }
.opt-line-income { fill: none; stroke: var(--mint); stroke-width: 2.5; }
.opt-line-upside { fill: none; stroke: var(--beam-2); stroke-width: 2.5; }
.opt-settle-line { stroke: var(--star-mute); stroke-width: 1; stroke-dasharray: 5 4; }
.opt-settle-label { fill: var(--star); font-family: var(--font-mono); font-size: 11px; font-weight: 500; }
.opt-dot-income { fill: var(--mint); stroke: #04060d; stroke-width: 2; }
.opt-dot-upside { fill: var(--beam-2); stroke: #04060d; stroke-width: 2; }
.opt-endpoint circle { fill: var(--star-mute); }
.opt-endpoint text { fill: var(--star-mute); font-family: var(--font-mono); font-size: 11px; font-variant-numeric: tabular-nums; }

.opt-table-wrap { overflow-x: auto; }
.opt-table caption {
  padding: 12px 14px;
  border-bottom: 1px solid var(--hair);
  color: var(--star-faint);
  font: 400 10px/1.5 var(--font-mono);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.opt-table th[scope='row'] {
  padding-inline: 14px;
  font: 500 13px/1.4 var(--font-mono);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.opt-current {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  border-radius: var(--r-pill);
  background: rgba(64, 179, 255, 0.16);
  color: var(--beam);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  vertical-align: 2px;
}

/* ---------------------------------------------------------------- settlement */
.opt-settle { display: grid; gap: 6px; }
.opt-values {
  display: grid;
  gap: 0;
  border-top: 1px solid var(--hair);
}
.opt-value-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--hair);
}
.opt-value-label { font: 500 9px/1.6 var(--font-mono); letter-spacing: 0.14em; text-transform: uppercase; }
.opt-value-row > div { text-align: right; }
.opt-value-row strong { font: 500 20px/1.2 var(--font-mono); font-variant-numeric: tabular-nums; color: var(--star); }
.opt-value-row small { display: block; margin-top: 4px; color: var(--star-faint); font: 400 10px/1.6 var(--font-mono); }
.opt-disclaimer {
  margin: 0;
  padding-top: 12px;
  border-top: 1px solid var(--hair);
  color: var(--star-faint);
  font: 400 10px/1.8 var(--font-mono);
}
.opt-disclaimer b { color: var(--star); }

/* ------------------------------------------------------------------ meters */
.opt-meters {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.opt-meter {
  display: grid;
  gap: 12px;
  min-width: 0;
  padding: 16px 18px;
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  background: var(--void-2);
}
.opt-meter--income { background: linear-gradient(160deg, rgba(92, 225, 160, 0.08), var(--void-2)); }
.opt-meter--upside { background: linear-gradient(160deg, rgba(167, 139, 250, 0.1), var(--void-2)); }
.opt-meter-label { display: flex; align-items: center; gap: 9px; }
.opt-meter-label b { font: 500 10px/1 var(--font-mono); letter-spacing: 0.18em; }
.opt-meter-label > span:last-child { color: var(--star-faint); font: 400 10px/1.3 var(--font-mono); }
.opt-meter-mark {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  color: #04060d;
}
.opt-meter--income .opt-meter-mark { background: var(--mint); box-shadow: 0 0 18px rgba(92, 225, 160, 0.45); }
.opt-meter--upside .opt-meter-mark { background: var(--beam-2); box-shadow: 0 0 18px rgba(167, 139, 250, 0.45); }
.opt-meter-price { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
.opt-meter-price strong { font: 400 22px/1.1 var(--font-display); font-variant-numeric: tabular-nums; }
.opt-meter-price span { color: var(--star-mute); font: 400 11px/1.3 var(--font-mono); font-variant-numeric: tabular-nums; }
.opt-meter-track { height: 4px; border-radius: var(--r-pill); background: var(--deck-3); overflow: hidden; }
.opt-meter-track span { display: block; height: 100%; border-radius: var(--r-pill); }
.opt-meter--income .opt-meter-track span { background: var(--mint); }
.opt-meter--upside .opt-meter-track span { background: var(--beam-2); }

/* --------------------------------------------------------------- responsive */
@media (max-width: 1100px) {
  .opt-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 520px) {
  .opt-meters { grid-template-columns: minmax(0, 1fr); }
  .opt-value-row { grid-template-columns: minmax(0, 1fr); }
  .opt-value-row > div { text-align: left; }
}
</style>
