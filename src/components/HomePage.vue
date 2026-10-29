<script setup>
import { computed, ref } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import { calculatePayoff } from '../payoff.js'
import { brand } from '../brand.js'

const emit = defineEmits(['navigate'])

const assets = [
  { symbol: 'SOL', name: 'Solana', spot: 182.4, change: 4.82, initials: 'S' },
  { symbol: 'JUP', name: 'Jupiter', spot: 1.12, change: 2.1, initials: 'J' },
  { symbol: 'BONK', name: 'Bonk', spot: 0.000021, change: -1.34, initials: 'B' },
  { symbol: 'USDC', name: 'USD Coin', spot: 1, change: 0.01, initials: '$' },
]

const selected = ref('SOL')
const side = ref('Income')
const units = ref(1)
const cap = ref(5)
const query = ref('')

const asset = computed(() => assets.find(item => item.symbol === selected.value) || assets[0])
const model = computed(() => calculatePayoff({
  spot: asset.value.spot,
  capPercent: cap.value,
  settlementPrice: asset.value.spot,
}))
const unitPrice = computed(() => (side.value === 'Income' ? model.value.incomePrice : model.value.upsidePrice))
const amount = computed(() => {
  const value = Number(units.value)
  return Number.isFinite(value) && value > 0 ? value : 0
})

const money = value => new Intl.NumberFormat('en-US', {
  style: 'currency', currency: 'USD', maximumFractionDigits: 2,
}).format(value)
const spot = value => (value < 0.01 ? `$${value.toFixed(6)}` : money(value))
const pct = value => `${value > 0 ? '+' : ''}${value.toFixed(2)}%`
const signed = value => `${value > 0 ? '+' : ''}${money(value)}`

const tape = computed(() => assets.map(item => ({
  ...item,
  model: calculatePayoff({ spot: item.spot, capPercent: 5, settlementPrice: item.spot }),
})))

function toBoundary() {
  document.getElementById('cap')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const filtered = computed(() => {
  const needle = query.value.trim().toLowerCase()
  if (!needle) return tape.value
  return tape.value.filter(item => `${item.symbol} ${item.name}`.toLowerCase().includes(needle))
})

const briefing = [
  ['01', 'Board', 'Every listed pair on one ruled ledger with a stated cap and the two modelled unit prices.', '/app/markets'],
  ['02', 'Boundary', 'Set the cap yourself and read how value splits at settlement, before anything else.', '#cap'],
  ['03', 'Journal', 'Write the thesis and the risk into a record that stays in this browser.', '/signal'],
  ['04', 'Reference', 'How the payoff maths works, what the preview does and where it stops.', '/docs'],
]
</script>

<template>
  <div class="reef">
    <!-- opening shoreline -->
    <section class="bp-band bp-band--first co-open">
      <div class="co-open-copy">
        <p class="bp-kicker">Sheet {{ brand.asset }} / {{ brand.network }} / preview build</p>
        <h1 class="bp-display" tabindex="-1">Read the chain.<br />Price the boundary.<br /><em>Keep the record.</em></h1>
      </div>
      <div class="co-open-side">
        <p class="bp-lead">{{ brand.supportingLine }}</p>
        <div class="co-open-actions">
          <a class="bp-btn bp-btn--primary" href="/app/markets" @click.prevent="emit('navigate', '/app/markets')">
            Open the board <ArrowRight :size="15" />
          </a>
          <button class="bp-btn bp-btn--ghost" type="button" @click="toBoundary">Price a boundary</button>
        </div>
        <p class="bp-note">Sample quotes, a user-priced model and a browser-local journal. Nothing here is live and nothing is signed.</p>
      </div>
    </section>

    <!-- annotated gauge -->
    <section class="bp-band co-gauge-band">
      <dl class="co-gauge">
        <div><dt>Pairs listed</dt><dd>04</dd></div>
        <div><dt>Cap default</dt><dd>+5%</dd></div>
        <div><dt>Epoch</dt><dd>30d</dd></div>
        <div><dt>Feed</dt><dd>Static</dd></div>
        <div><dt>Records</dt><dd>Local</dd></div>
        <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd></div>
      </dl>
    </section>

    <!-- board + sandbox quote -->
    <section class="bp-band co-board-band">
      <div class="co-board">
        <div class="co-board-main">
          <div class="co-head">
            <h2 id="tbl-title" class="bp-h2">The board</h2>
            <div class="co-tools">
              <div class="bp-switch" role="group" aria-label="Position type">
                <button v-for="option in ['All', 'Income', 'Upside']" :key="option" type="button"
                        :class="{ 'is-on': side === option }" :aria-pressed="side === option"
                        @click="side = option">{{ option }}</button>
              </div>
              <label class="co-search">
                <span class="visually-hidden">Filter the board</span>
                <input v-model="query" type="search" class="bp-input" placeholder="Filter by symbol" />
              </label>
            </div>
          </div>

          <div class="bp-table-wrap">
            <table class="bp-table">
              <caption class="visually-hidden">Illustrative {{ brand.network }} pairs with modelled unit prices</caption>
              <thead>
                <tr>
                  <th scope="col">Pair</th>
                  <th scope="col" class="bp-num">Sample spot</th>
                  <th scope="col" class="bp-num">Move</th>
                  <th scope="col" class="bp-num" :class="{ 'bp-loud': side === 'Income' }">Income / unit</th>
                  <th scope="col" class="bp-num" :class="{ 'bp-loud': side === 'Upside' }">Upside / unit</th>
                  <th scope="col">Open</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in filtered" :key="item.symbol" :class="{ 'is-picked': item.symbol === selected }">
                  <th scope="row">
                    <button class="co-token" type="button" :aria-pressed="item.symbol === selected" @click="selected = item.symbol">
                      <span class="co-token-mark" :class="{ 'is-on': item.symbol === selected }" aria-hidden="true">{{ item.initials }}</span>
                      <span class="co-token-name"><b>{{ item.symbol }}</b><small>{{ item.name }}</small></span>
                    </button>
                  </th>
                  <td class="bp-num">{{ spot(item.spot) }}</td>
                  <td class="bp-num" :class="item.change >= 0 ? 'is-up' : 'is-down'">{{ pct(item.change) }}</td>
                  <td class="bp-num">{{ money(item.model.incomePrice) }}</td>
                  <td class="bp-num">{{ money(item.model.upsidePrice) }}</td>
                  <td><a class="co-rowlink" :href="`/app/markets/${item.symbol}`"
                         :aria-label="`Open the ${item.symbol} sheet`"
                         @click.prevent="emit('navigate', `/app/markets/${item.symbol}`)">Sheet</a></td>
                </tr>
                <tr v-if="!filtered.length">
                  <td class="co-empty" colspan="6">
                    Nothing matches “{{ query }}”.
                    <button class="co-rowlink" type="button" @click="query = ''">Clear filter</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="bp-note co-foot-note">* {{ brand.asset }} is a proposed symbol. No token has been issued and no contract address exists.</p>
        </div>

        <section class="co-quote" aria-labelledby="quote-title">
          <div class="co-quote-head">
            <h2 id="quote-title" class="bp-h2">Unit quote</h2>
            <span class="bp-pill bp-pill--bp-cobalt"><i aria-hidden="true"></i>Sandbox</span>
          </div>
          <p class="co-quote-line">Example arithmetic only. No live quote is read and no order is placed.</p>
          <dl class="co-readout">
            <div><dt>Sample spot</dt><dd>{{ spot(asset.spot) }}</dd></div>
            <div><dt>Cap price K</dt><dd>{{ money(model.strike) }}</dd></div>
            <div><dt>Model / unit</dt><dd>{{ money(unitPrice) }}</dd></div>
            <div><dt>Leg</dt><dd>{{ side }}</dd></div>
          </dl>
          <div class="co-quote-body">
            <div class="bp-field">
              <label for="quote-asset">Pair</label>
              <select id="quote-asset" v-model="selected" class="bp-input">
                <option v-for="item in assets" :key="item.symbol" :value="item.symbol">{{ item.symbol }} / {{ item.name }}</option>
              </select>
            </div>

            <div class="bp-field">
              <span class="bp-field-label">Leg</span>
              <div class="bp-switch" role="group" aria-label="Position leg">
                <button v-for="option in ['Income', 'Upside']" :key="option" type="button"
                        :class="{ 'is-on': side === option }" :aria-pressed="side === option"
                        @click="side = option">{{ option }}</button>
              </div>
            </div>

            <div class="bp-field">
              <label for="quote-units">Units</label>
              <span class="co-combo">
                <input id="quote-units" v-model.number="units" class="bp-input" type="number" inputmode="decimal"
                       min="0.01" max="1000000" step="0.01" />
                <b>{{ selected }}</b>
              </span>
            </div>

            <div class="bp-field">
              <label for="quote-cap">Cap K <output>+{{ cap }}%</output></label>
              <input id="quote-cap" v-model.number="cap" class="bp-range" type="range" min="0" max="10" step="1" />
              <span class="bp-scale"><span>0%</span><span>10%</span></span>
            </div>

            <button class="bp-btn bp-btn--primary bp-btn--wide" type="button" :disabled="!amount" @click="toBoundary">
              See the split <ArrowRight :size="15" />
            </button>
          </div>
          <p class="co-total"><span>Modelled value</span><strong>{{ money(unitPrice * amount) }}</strong></p>
        </section>
      </div>
    </section>

    <!-- settlement split -->
    <section id="cap" class="bp-band co-split-band">
      <div class="co-head">
        <h2 id="split-title" class="bp-h2">Settlement split</h2>
        <p class="bp-meta">{{ selected }} / cap +{{ cap }}% / settlement at the sample spot</p>
      </div>
      <div class="co-split">
        <figure class="co-figure">
          <svg viewBox="0 0 640 300" role="img" :aria-label="`${selected} settlement partition at a ${cap} percent cap`">
            <title>{{ selected }} settlement partition</title>
            <desc>Value below the cap is an income leg priced {{ money(model.incomePrice) }} per unit; value above the cap is an upside leg priced {{ money(model.upsidePrice) }} per unit.</desc>
            <g class="co-grid-lines">
              <line v-for="t in 5" :key="`g${t}`" :x1="60" :x2="620" :y1="40 + t * 44" :y2="40 + t * 44" />
            </g>
            <rect x="60" :y="40" :width="496 * model.incomeShare" height="220" class="co-band-a" />
            <rect :x="60 + 496 * model.incomeShare" :y="40" :width="496 * model.upsideShare" height="220" class="co-band-b" />
            <line x1="60" y1="40" x2="60" y2="260" class="co-axis" />
            <line x1="60" y1="260" x2="620" y2="260" class="co-axis" />
            <line :x1="60 + 496 * model.incomeShare" y1="40" :x2="60 + 496 * model.incomeShare" y2="260" class="co-cap" />
            <text :x="60 + 496 * model.incomeShare + 8" y="58" class="co-cap-label">CAP K {{ money(model.strike) }}</text>
            <text x="72" y="98" class="co-band-label">INCOME</text>
            <text :x="620 - 8" y="98" class="co-band-label is-end" text-anchor="end">UPSIDE</text>
            <text x="72" y="134" class="co-value">{{ money(model.incomePrice) }} / unit</text>
            <text :x="620 - 8" y="134" class="co-value is-end" text-anchor="end">{{ money(model.upsidePrice) }} / unit</text>
            <line x1="60" y1="292" x2="620" y2="292" class="co-axis" />
            <text x="60" y="288" class="co-tick">0</text>
            <text :x="60 + 496 * model.incomeShare" y="288" class="co-tick" text-anchor="middle">K</text>
            <text x="620" y="288" class="co-tick" text-anchor="end">settlement</text>
          </svg>
          <figcaption>{{ model.incomeShare >= model.upsideShare ? 'Most of the sample value sits below the cap.' : 'Most of the sample value sits above the cap.' }} Example arithmetic.</figcaption>
        </figure>
        <dl class="co-split-readout">
          <div><dt>Income share</dt><dd>{{ (model.incomeShare * 100).toFixed(1) }}%</dd></div>
          <div><dt>Upside share</dt><dd>{{ (model.upsideShare * 100).toFixed(1) }}%</dd></div>
          <div><dt>Income at settlement</dt><dd>{{ money(model.incomeSettlement) }}</dd></div>
          <div><dt>Upside at settlement</dt><dd>{{ money(model.upsideSettlement) }}</dd></div>
          <div><dt>Model premium</dt><dd>{{ money(model.premium) }}</dd></div>
          <div><dt>Breakeven</dt><dd>{{ money(model.breakeven) }}</dd></div>
          <div><dt>Sample move</dt><dd :class="model.spotChangePercent >= 0 ? 'is-up' : 'is-down'">{{ signed(model.spotChangePercent) }}</dd></div>
          <div><dt>Cap</dt><dd>+{{ cap }}%</dd></div>
        </dl>
      </div>
    </section>

    <!-- sample tape -->
    <section class="bp-band co-tape-band">
      <div class="co-head">
        <h2 id="tape-title" class="bp-h2">Sample tape</h2>
        <p class="bp-meta">Not a feed</p>
      </div>
      <ul class="co-tape">
        <li v-for="item in tape" :key="item.symbol">
          <button type="button" :aria-pressed="item.symbol === selected"
                  :class="{ 'is-on': item.symbol === selected }" @click="selected = item.symbol">
            <b>{{ item.symbol }}</b>
            <em>{{ spot(item.spot) }}</em>
            <i :class="item.change >= 0 ? 'is-up' : 'is-down'">{{ pct(item.change) }}</i>
            <small>K {{ money(item.model.strike) }}</small>
          </button>
        </li>
      </ul>
    </section>

    <!-- briefing -->
    <section class="bp-band co-brief-band">
      <div class="co-head">
        <h2 id="brief-title" class="bp-h2">Briefing</h2>
        <p class="bp-meta">Four leaves</p>
      </div>
      <ol class="co-brief">
        <li v-for="[num, title, body, to] in briefing" :key="num">
          <a :href="to" @click.prevent="to.startsWith('#') ? toBoundary() : emit('navigate', to)">
            <b>{{ num }}</b>
            <span>
              <strong>{{ title }}</strong>
              <em>{{ body }}</em>
            </span>
            <ArrowRight :size="16" aria-hidden="true" />
          </a>
        </li>
      </ol>
    </section>

    <!-- limits proof band -->
    <section class="bp-band co-limits-band">
      <div class="co-limits">
        <div class="co-limits-copy">
          <h2 id="disc-title" class="bp-h2">Limits of this preview</h2>
        </div>
        <ul class="co-limits-list">
          <li>Quotes are illustrative samples, not a market feed.</li>
          <li>The payoff model uses values you enter.</li>
          <li>Journal records stay in this browser's storage.</li>
          <li>No custody, no signing, no trade execution.</li>
          <li>No contract address is published or implied.</li>
        </ul>
        <button class="bp-btn bp-btn--primary" type="button" @click="emit('navigate', '/risk')">Read the limits</button>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Cobalt Blueprint - home stage. Ruled ledger sheets, no ambient gradients. */
.co-page { display: grid; min-width: 0; }
.co-page > * { min-width: 0; }

/* ------------------------------------------------------------------ opening */
.co-open {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(0, 4fr);
  gap: clamp(20px, 3vw, 44px);
  align-items: end;
  padding-block-end: clamp(24px, 3vw, 40px);
  border-block-end: 1px solid var(--bp-line-2);
}
.co-open-copy { display: grid; gap: 14px; align-content: start; min-width: 0; }
.co-open-copy .bp-display { font-size: clamp(40px, 5.2vw, 74px); }
.co-open-side { display: grid; gap: 16px; padding-block-end: 6px; }
.co-open-side .bp-lead { margin-block-start: 0; }
.co-open-actions { display: flex; flex-wrap: wrap; gap: 10px; }

/* ------------------------------------------------------------------- gauge */
.co-gauge-band { padding-block: clamp(18px, 2.2vw, 26px); }
.co-gauge { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); }
.co-gauge > div {
  display: grid;
  gap: 6px;
  padding: 4px 14px;
  border-inline-start: 1px solid var(--bp-line);
}
.co-gauge > div:first-child { border-inline-start: 0; padding-inline-start: 0; }
.co-gauge dt {
  color: var(--bp-muted);
  font: 500 9px/1.4 var(--bp-font-mono);
  letter-spacing: .14em;
  text-transform: uppercase;
}
.co-gauge dd {
  color: var(--bp-ink);
  font: 600 clamp(18px, 1.7vw, 23px)/1 var(--bp-font-display);
  letter-spacing: -.02em;
  font-variant-numeric: tabular-nums;
}

/* ------------------------------------------------------------------- board */
.co-board-band { padding-block-start: clamp(24px, 3vw, 38px); }
.co-board { display: grid; gap: clamp(16px, 2vw, 24px); min-width: 0; }
.co-board > * { min-width: 0; }
.co-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-block-end: 12px;
  padding-block-end: 10px;
  border-block-end: 1px solid var(--bp-line-2);
}
.co-head .bp-h2 { font-size: clamp(22px, 2.4vw, 30px); }
.co-tools { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.co-search { display: block; min-width: 200px; }
.co-search .bp-input { min-height: 34px; padding-block: 6px; font-size: 13px; }
.co-token {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0;
  border: 0;
  background: none;
  text-align: start;
}
.co-token-mark {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border-radius: 3px;
  background: var(--bp-paper-2);
  color: var(--bp-ink-2);
  font: 600 11px/1 var(--bp-font-mono);
  box-shadow: inset 0 0 0 1px var(--bp-line-2);
}
.co-token-mark.is-on { background: var(--bp-cobalt); color: #fff; box-shadow: inset 0 0 0 1px var(--bp-cobalt); }
.co-token-name { display: grid; gap: 1px; }
.co-token-name b { font: 600 12px/1.3 var(--bp-font-mono); letter-spacing: .03em; }
.co-token-name small { color: var(--bp-muted); font: 400 11px/1.3 var(--bp-font-body); }
.bp-table tbody tr.is-picked { background: rgba(117, 117, 255, .1); }
.is-up { color: var(--bp-success); }
.is-down { color: var(--bp-danger); }
.co-rowlink {
  border: 0;
  border-block-end: 1px solid rgba(0, 0, 214, .4);
  padding: 0 0 2px;
  background: none;
  color: var(--bp-cobalt-safe);
  font: 600 10px/1.4 var(--bp-font-mono);
  letter-spacing: .08em;
  text-decoration: none;
  text-transform: uppercase;
}
.co-rowlink:hover { border-block-end-color: var(--bp-cobalt); }
.co-empty { padding-block: 22px; color: var(--bp-muted); font: 400 13px/1.7 var(--bp-font-body); }
.co-empty .co-rowlink { margin-inline-start: 10px; }
.co-foot-note { padding-block-start: 2px; }

/* ------------------------------------------------------------------- quote */
.co-quote {
  display: grid;
  grid-template-columns: minmax(0, 4fr) minmax(0, 6fr);
  gap: 14px clamp(18px, 2.4vw, 30px);
  align-items: start;
  padding: clamp(18px, 2vw, 24px);
  border: 1px solid var(--bp-line-2);
  border-block-start: 3px solid var(--bp-cobalt);
  border-radius: 0;
  background: var(--bp-paper);
}
.co-quote-head { grid-column: 1 / -1; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.co-quote-line { grid-column: 1 / -1; color: var(--bp-muted); font: 400 12px/1.7 var(--bp-font-body); }
.co-readout { display: grid; border-block-start: 1px solid var(--bp-line); }
.co-readout > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block: 9px;
  border-block-end: 1px solid var(--bp-line);
}
.co-readout dt { color: var(--bp-muted); font: 500 10px/1.5 var(--bp-font-mono); letter-spacing: .08em; text-transform: uppercase; }
.co-readout dd { color: var(--bp-ink); font: 600 13px/1.5 var(--bp-font-mono); font-variant-numeric: tabular-nums; }
.co-quote-body {
  grid-column: 2;
  grid-row: 3 / span 2;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.co-quote-body > .bp-btn { grid-column: 1 / -1; }
.co-combo { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 10px; }
.co-combo b { color: var(--bp-muted); font: 600 11px/1 var(--bp-font-mono); letter-spacing: .08em; }
.co-total {
  grid-column: 1;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block-start: 12px;
  border-block-start: 2px solid var(--bp-ink);
}
.co-total span { color: var(--bp-muted); font: 500 10px/1.4 var(--bp-font-mono); letter-spacing: .12em; text-transform: uppercase; }
.co-total strong { color: var(--bp-ink); font: 600 24px/1 var(--bp-font-display); letter-spacing: -.03em; font-variant-numeric: tabular-nums; }

/* ------------------------------------------------------------------- split */
.co-split-band { padding-block-start: clamp(24px, 3vw, 38px); }
.co-split > * { min-width: 0; }
.co-split {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
  gap: clamp(18px, 2.4vw, 32px);
  align-items: start;
}
.co-figure {
  display: grid;
  gap: 12px;
  padding: clamp(14px, 1.8vw, 20px);
  border: 1px solid var(--bp-line-2);
  border-radius: 0;
  background:
    linear-gradient(90deg, rgba(0, 0, 255, .04) 1px, transparent 1px),
    linear-gradient(180deg, rgba(0, 0, 255, .04) 1px, transparent 1px),
    var(--bp-paper);
  background-size: 32px 32px, 32px 32px, auto;
}
.co-figure figcaption { color: var(--bp-muted); font: 400 11px/1.7 var(--bp-font-mono); }
.co-grid-lines line { stroke: var(--bp-line); stroke-width: 1; }
.co-band-a { fill: rgba(0, 0, 255, .12); }
.co-band-b { fill: rgba(0, 0, 255, .34); }
.co-axis { stroke: var(--bp-line-2); stroke-width: 1.5; }
.co-cap { stroke: var(--bp-cobalt); stroke-width: 2.5; stroke-dasharray: 5 5; }
.co-cap-label { fill: var(--bp-cobalt-safe); font: 600 11px/1 var(--bp-font-mono); }
.co-band-label { fill: var(--bp-ink); font: 600 12px/1 var(--bp-font-mono); letter-spacing: .14em; }
.co-value { fill: var(--bp-ink-2); font: 500 13px/1 var(--bp-font-mono); }
.co-tick { fill: var(--bp-muted); font: 400 10px/1 var(--bp-font-mono); }
.co-split-readout { display: grid; border-block-start: 2px solid var(--bp-ink); }
.co-split-readout > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block: 8px;
  border-block-end: 1px solid var(--bp-line);
}
.co-split-readout dt { color: var(--bp-muted); font: 500 10px/1.5 var(--bp-font-mono); letter-spacing: .08em; text-transform: uppercase; }
.co-split-readout dd { color: var(--bp-ink); font: 600 14px/1.5 var(--bp-font-mono); font-variant-numeric: tabular-nums; }

/* -------------------------------------------------------------------- tape */
.co-tape { display: flex; gap: 8px; overflow-x: auto; padding-block-end: 4px; scrollbar-width: thin; }
.co-tape li { flex: 0 0 auto; }
.co-tape button {
  display: grid;
  grid-template-columns: auto minmax(64px, auto) auto;
  align-items: baseline;
  gap: 3px 12px;
  min-width: 172px;
  padding: 11px 14px;
  border: 1px solid var(--bp-line-2);
  border-radius: 3px;
  background: var(--bp-paper);
  text-align: start;
  transition: border-color var(--bp-motion-duration) var(--bp-motion-ease), background-color var(--bp-motion-duration) var(--bp-motion-ease);
}
.co-tape button:hover { border-color: var(--bp-cobalt); }
.co-tape button.is-on { border-color: var(--bp-cobalt); background: rgba(117, 117, 255, .1); }
.co-tape b { color: var(--bp-ink); font: 600 12px/1.3 var(--bp-font-mono); letter-spacing: .05em; }
.co-tape em { color: var(--bp-ink-2); font: 500 12px/1.3 var(--bp-font-mono); font-style: normal; text-align: end; }
.co-tape i { font: 500 11px/1.3 var(--bp-font-mono); font-style: normal; text-align: end; }
.co-tape small { grid-column: 1 / -1; color: var(--bp-muted); font: 400 10px/1.4 var(--bp-font-mono); }

/* ---------------------------------------------------------------- briefing */
.co-brief { display: grid; border-block-start: 1px solid var(--bp-line-2); }
.co-brief li { border-block-end: 1px solid var(--bp-line); }
.co-brief a {
  display: grid;
  grid-template-columns: 54px minmax(0, 1fr) auto;
  align-items: start;
  gap: 16px;
  padding: 16px 6px;
  color: inherit;
  text-decoration: none;
  transition: background-color var(--bp-motion-duration) var(--bp-motion-ease);
}
.co-brief a:hover { background: rgba(117, 117, 255, .08); }
.co-brief b { color: var(--bp-cobalt-safe); font: 500 12px/1.6 var(--bp-font-mono); letter-spacing: .1em; }
.co-brief span { display: grid; gap: 3px; }
.co-brief strong { font: 600 17px/1.35 var(--bp-font-display); letter-spacing: -.02em; }
.co-brief em { color: var(--bp-muted); font: 400 13px/1.65 var(--bp-font-body); font-style: normal; }
.co-brief svg { color: var(--bp-cobalt-safe); margin-block-start: 3px; }

/* ----------------------------------------------------------------- limits */
.co-limits-band { padding-block-end: clamp(24px, 3vw, 40px); }
.co-limits {
  display: grid;
  grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
  gap: clamp(18px, 2.4vw, 32px);
  align-items: start;
  padding: clamp(20px, 2.4vw, 30px);
  border: 1px solid var(--bp-line-2);
  border-inline-start: 3px solid var(--bp-cobalt);
  border-radius: 0;
  background: var(--bp-paper);
}
.co-limits-copy { display: grid; gap: 8px; }
.co-limits-list { display: grid; gap: 9px; }
.co-limits-list li {
  position: relative;
  padding-inline-start: 20px;
  color: var(--bp-ink-2);
  font: 400 13px/1.6 var(--bp-font-body);
}
.co-limits-list li::before {
  content: "";
  position: absolute;
  inset-inline-start: 0;
  inset-block-start: .58em;
  width: 7px;
  height: 7px;
  border: 1px solid var(--bp-cobalt);
  background: var(--bp-paper);
}
.co-limits .bp-btn { grid-column: 1 / -1; justify-self: start; }

/* ------------------------------------------------------------- responsive */
@media (max-width: 1180px) {
  .co-quote { grid-template-columns: minmax(0, 1fr); }
  .co-quote-body { grid-column: 1; grid-row: auto; }
  .co-gauge { grid-template-columns: repeat(3, minmax(0, 1fr)); row-gap: 14px; }
  .co-gauge > div:nth-child(4) { border-inline-start: 0; padding-inline-start: 0; }
}
@media (max-width: 900px) {
  .co-open { grid-template-columns: minmax(0, 1fr); align-items: start; }
  .co-split > * { min-width: 0; }
.co-split { grid-template-columns: minmax(0, 1fr); }
  .co-limits { grid-template-columns: minmax(0, 1fr); }
  .co-limits .bp-btn { justify-self: stretch; }
}
@media (max-width: 620px) {
  .co-gauge { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .co-gauge > div:nth-child(3) { border-inline-start: 0; padding-inline-start: 0; }
  .co-gauge > div:nth-child(even) { border-inline-start: 0; }
  .co-brief a { grid-template-columns: 34px minmax(0, 1fr); }
  .co-brief svg { display: none; }
  .co-search { width: 100%; }
  .co-tools { width: 100%; }
  .co-tools .bp-switch { flex: 1 1 auto; }
  .co-tools .bp-switch button { flex: 1 1 auto; }
}
</style>
