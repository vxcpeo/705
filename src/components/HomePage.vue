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
    <section class="tide-band tide-band--first reef-open">
      <div class="reef-open-copy">
        <p class="tide-kicker">Sheet {{ brand.asset }} / {{ brand.network }} / preview build</p>
        <h1 class="tide-display" tabindex="-1">Read the chain.<br />Price the boundary.<br /><em>Keep the record.</em></h1>
      </div>
      <div class="reef-open-side">
        <p class="tide-lead">{{ brand.supportingLine }}</p>
        <div class="reef-open-actions">
          <a class="tide-btn tide-btn--primary" href="/app/markets" @click.prevent="emit('navigate', '/app/markets')">
            Open the board <ArrowRight :size="15" />
          </a>
          <button class="tide-btn tide-btn--ghost" type="button" @click="toBoundary">Price a boundary</button>
        </div>
        <p class="tide-note">Sample quotes, a user-priced model and a browser-local journal. Nothing here is live and nothing is signed.</p>
      </div>
    </section>

    <!-- annotated gauge -->
    <section class="tide-band reef-gauge-band">
      <dl class="reef-gauge">
        <div><dt>Pairs listed</dt><dd>04</dd></div>
        <div><dt>Cap default</dt><dd>+5%</dd></div>
        <div><dt>Epoch</dt><dd>30d</dd></div>
        <div><dt>Feed</dt><dd>Static</dd></div>
        <div><dt>Records</dt><dd>Local</dd></div>
        <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd></div>
      </dl>
    </section>

    <!-- board + sandbox quote -->
    <section class="tide-band reef-board-band">
      <div class="reef-board">
        <div class="reef-board-main">
          <div class="reef-head">
            <h2 id="tbl-title" class="tide-h2">The board</h2>
            <div class="reef-tools">
              <div class="tide-switch" role="group" aria-label="Position type">
                <button v-for="option in ['All', 'Income', 'Upside']" :key="option" type="button"
                        :class="{ 'is-on': side === option }" :aria-pressed="side === option"
                        @click="side = option">{{ option }}</button>
              </div>
              <label class="reef-search">
                <span class="visually-hidden">Filter the board</span>
                <input v-model="query" type="search" class="tide-input" placeholder="Filter by symbol" />
              </label>
            </div>
          </div>

          <div class="tide-table-wrap">
            <table class="tide-table">
              <caption class="visually-hidden">Illustrative {{ brand.network }} pairs with modelled unit prices</caption>
              <thead>
                <tr>
                  <th scope="col">Pair</th>
                  <th scope="col" class="tide-num">Sample spot</th>
                  <th scope="col" class="tide-num">Move</th>
                  <th scope="col" class="tide-num" :class="{ 'tide-loud': side === 'Income' }">Income / unit</th>
                  <th scope="col" class="tide-num" :class="{ 'tide-loud': side === 'Upside' }">Upside / unit</th>
                  <th scope="col">Open</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in filtered" :key="item.symbol" :class="{ 'is-picked': item.symbol === selected }">
                  <th scope="row">
                    <button class="reef-token" type="button" :aria-pressed="item.symbol === selected" @click="selected = item.symbol">
                      <span class="reef-token-mark" :class="{ 'is-on': item.symbol === selected }" aria-hidden="true">{{ item.initials }}</span>
                      <span class="reef-token-name"><b>{{ item.symbol }}</b><small>{{ item.name }}</small></span>
                    </button>
                  </th>
                  <td class="tide-num">{{ spot(item.spot) }}</td>
                  <td class="tide-num" :class="item.change >= 0 ? 'is-up' : 'is-down'">{{ pct(item.change) }}</td>
                  <td class="tide-num">{{ money(item.model.incomePrice) }}</td>
                  <td class="tide-num">{{ money(item.model.upsidePrice) }}</td>
                  <td><a class="reef-rowlink" :href="`/app/markets/${item.symbol}`"
                         :aria-label="`Open the ${item.symbol} sheet`"
                         @click.prevent="emit('navigate', `/app/markets/${item.symbol}`)">Sheet</a></td>
                </tr>
                <tr v-if="!filtered.length">
                  <td class="reef-empty" colspan="6">
                    Nothing matches “{{ query }}”.
                    <button class="reef-rowlink" type="button" @click="query = ''">Clear filter</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="tide-note reef-foot-note">* {{ brand.asset }} is a proposed symbol. No token has been issued and no contract address exists.</p>
        </div>

        <aside class="reef-quote" aria-labelledby="quote-title">
          <div class="reef-quote-head">
            <h2 id="quote-title" class="tide-h2">Unit quote</h2>
            <span class="tide-pill tide-pill--accent"><i aria-hidden="true"></i>Sandbox</span>
          </div>
          <p class="reef-quote-line">Example arithmetic only. No live quote is read and no order is placed.</p>
          <dl class="reef-readout">
            <div><dt>Sample spot</dt><dd>{{ spot(asset.spot) }}</dd></div>
            <div><dt>Cap price K</dt><dd>{{ money(model.strike) }}</dd></div>
            <div><dt>Model / unit</dt><dd>{{ money(unitPrice) }}</dd></div>
            <div><dt>Leg</dt><dd>{{ side }}</dd></div>
          </dl>
          <div class="reef-quote-body">
            <div class="tide-field">
              <label for="quote-asset">Pair</label>
              <select id="quote-asset" v-model="selected" class="tide-input">
                <option v-for="item in assets" :key="item.symbol" :value="item.symbol">{{ item.symbol }} / {{ item.name }}</option>
              </select>
            </div>

            <div class="tide-field">
              <span class="tide-field-label">Leg</span>
              <div class="tide-switch" role="group" aria-label="Position leg">
                <button v-for="option in ['Income', 'Upside']" :key="option" type="button"
                        :class="{ 'is-on': side === option }" :aria-pressed="side === option"
                        @click="side = option">{{ option }}</button>
              </div>
            </div>

            <div class="tide-field">
              <label for="quote-units">Units</label>
              <span class="reef-combo">
                <input id="quote-units" v-model.number="units" class="tide-input" type="number" inputmode="decimal"
                       min="0.01" max="1000000" step="0.01" />
                <b>{{ selected }}</b>
              </span>
            </div>

            <div class="tide-field">
              <label for="quote-cap">Cap K <output>+{{ cap }}%</output></label>
              <input id="quote-cap" v-model.number="cap" class="tide-range" type="range" min="0" max="10" step="1" />
              <span class="tide-scale"><span>0%</span><span>10%</span></span>
            </div>

            <button class="tide-btn tide-btn--primary tide-btn--wide" type="button" :disabled="!amount" @click="toBoundary">
              See the split <ArrowRight :size="15" />
            </button>
          </div>
          <p class="reef-total"><span>Modelled value</span><strong>{{ money(unitPrice * amount) }}</strong></p>
        </aside>
      </div>
    </section>

    <!-- settlement split -->
    <section id="cap" class="tide-band reef-split-band">
      <div class="reef-head">
        <h2 id="split-title" class="tide-h2">Settlement split</h2>
        <p class="tide-meta">{{ selected }} / cap +{{ cap }}% / settlement at the sample spot</p>
      </div>
      <div class="reef-split">
        <figure class="reef-figure">
          <svg viewBox="0 0 640 300" role="img" :aria-label="`${selected} settlement partition at a ${cap} percent cap`">
            <title>{{ selected }} settlement partition</title>
            <desc>Value below the cap is an income leg priced {{ money(model.incomePrice) }} per unit; value above the cap is an upside leg priced {{ money(model.upsidePrice) }} per unit.</desc>
            <g class="reef-grid-lines">
              <line v-for="t in 5" :key="`g${t}`" :x1="60" :x2="620" :y1="40 + t * 44" :y2="40 + t * 44" />
            </g>
            <rect x="60" :y="40" :width="496 * model.incomeShare" height="220" class="reef-band-a" />
            <rect :x="60 + 496 * model.incomeShare" :y="40" :width="496 * model.upsideShare" height="220" class="reef-band-b" />
            <line x1="60" y1="40" x2="60" y2="260" class="reef-axis" />
            <line x1="60" y1="260" x2="620" y2="260" class="reef-axis" />
            <line :x1="60 + 496 * model.incomeShare" y1="40" :x2="60 + 496 * model.incomeShare" y2="260" class="reef-cap" />
            <text :x="60 + 496 * model.incomeShare + 8" y="58" class="reef-cap-label">CAP K {{ money(model.strike) }}</text>
            <text x="72" y="98" class="reef-band-label">INCOME</text>
            <text :x="620 - 8" y="98" class="reef-band-label is-end" text-anchor="end">UPSIDE</text>
            <text x="72" y="134" class="reef-value">{{ money(model.incomePrice) }} / unit</text>
            <text :x="620 - 8" y="134" class="reef-value is-end" text-anchor="end">{{ money(model.upsidePrice) }} / unit</text>
            <line x1="60" y1="292" x2="620" y2="292" class="reef-axis" />
            <text x="60" y="288" class="reef-tick">0</text>
            <text :x="60 + 496 * model.incomeShare" y="288" class="reef-tick" text-anchor="middle">K</text>
            <text x="620" y="288" class="reef-tick" text-anchor="end">settlement</text>
          </svg>
          <figcaption>{{ model.incomeShare >= model.upsideShare ? 'Most of the sample value sits below the cap.' : 'Most of the sample value sits above the cap.' }} Example arithmetic.</figcaption>
        </figure>
        <dl class="reef-split-readout">
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
    <section class="tide-band reef-tape-band">
      <div class="reef-head">
        <h2 id="tape-title" class="tide-h2">Sample tape</h2>
        <p class="tide-meta">Not a feed</p>
      </div>
      <ul class="reef-tape">
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
    <section class="tide-band reef-brief-band">
      <div class="reef-head">
        <h2 id="brief-title" class="tide-h2">Briefing</h2>
        <p class="tide-meta">Four leaves</p>
      </div>
      <ol class="reef-brief">
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
    <section class="tide-band reef-limits-band">
      <div class="reef-limits">
        <div class="reef-limits-copy">
          <h2 id="disc-title" class="tide-h2">Limits of this preview</h2>
        </div>
        <ul class="reef-limits-list">
          <li>Quotes are illustrative samples, not a market feed.</li>
          <li>The payoff model uses values you enter.</li>
          <li>Journal records stay in this browser's storage.</li>
          <li>No custody, no signing, no trade execution.</li>
          <li>No contract address is published or implied.</li>
        </ul>
        <button class="tide-btn tide-btn--primary" type="button" @click="emit('navigate', '/risk')">Read the limits</button>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ---------------------------------------------------------------- opening */
.reef { display: grid; grid-template-columns: minmax(0, 1fr); }
.reef > * { min-width: 0; }
.reef-open {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
  gap: clamp(22px, 3.4vw, 48px);
  align-items: end;
  padding-block-end: clamp(26px, 3.6vw, 46px);
}
.reef-open-copy { min-width: 0; }
.reef-open-side { display: grid; gap: 16px; padding-block-end: 4px; }
.reef-open-side .tide-lead { margin-block-start: 0; }
.reef-open-actions { display: flex; flex-wrap: wrap; gap: 10px; }

/* ------------------------------------------------------------------ gauge */
.reef-gauge-band { padding-block: clamp(22px, 3vw, 34px); }
.reef-gauge {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  border-block: 1px solid var(--line);
}
.reef-gauge > div {
  display: grid;
  gap: 6px;
  padding: 14px 16px;
  border-inline-start: 1px solid var(--line);
}
.reef-gauge > div:first-child { border-inline-start: 0; padding-inline-start: 0; }
.reef-gauge dt {
  color: var(--muted);
  font: 600 9px/1.4 var(--font-mono);
  letter-spacing: .12em;
  text-transform: uppercase;
}
.reef-gauge dd {
  color: var(--ink);
  font: 600 clamp(17px, 1.8vw, 22px)/1 var(--font-display);
  letter-spacing: -.02em;
}

/* ------------------------------------------------------------------ board */
.reef-board {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(18px, 2.6vw, 32px);
  align-items: start;
}
.reef-board-main { min-width: 0; display: grid; gap: 14px; }
.reef-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-block-end: 14px;
}
.reef-tools { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.reef-search { display: block; min-width: 200px; }
.reef-search .tide-input { min-height: 38px; padding-block: 8px; font-family: var(--font-body); font-size: 13px; }
.reef-token {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0;
  border: 0;
  background: none;
  text-align: start;
}
.reef-token-mark {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 11px;
  background: var(--surface-alt);
  color: var(--ink-soft);
  font: 600 12px/1 var(--font-mono);
  box-shadow: inset 0 0 0 1px var(--line);
}
.reef-token-mark.is-on {
  background: var(--accent-safe);
  color: #fff;
  box-shadow: 0 6px 16px rgba(13, 113, 227, .3);
}
.reef-token-name { display: grid; gap: 1px; }
.reef-token-name b { font: 600 12px/1.3 var(--font-mono); letter-spacing: .03em; }
.reef-token-name small { color: var(--muted); font: 400 11px/1.3 var(--font-body); }
.tide-table tbody tr.is-picked { background: rgba(41, 141, 255, .07); }
.is-up { color: var(--success); }
.is-down { color: var(--danger); }
.reef-rowlink {
  border: 0;
  border-block-end: 1px solid rgba(13, 113, 227, .35);
  padding: 0 0 2px;
  background: none;
  color: var(--accent-deep);
  font: 600 11px/1.4 var(--font-mono);
  letter-spacing: .06em;
  text-decoration: none;
  text-transform: uppercase;
}
.reef-rowlink:hover { border-block-end-color: var(--accent-safe); }
.reef-empty { padding-block: 22px; color: var(--muted); font: 400 13px/1.7 var(--font-body); }
.reef-empty .reef-rowlink { margin-inline-start: 10px; }
.reef-foot-note { padding-block-start: 4px; }

/* ------------------------------------------------------------------ quote */
.reef-quote {
  display: grid;
  grid-template-columns: minmax(0, 4fr) minmax(0, 6fr);
  gap: 14px clamp(18px, 2.6vw, 30px);
  align-items: start;
  padding: clamp(18px, 2vw, 24px);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background:
    radial-gradient(420px 220px at 100% 0%, rgba(41, 141, 255, .12), transparent 70%),
    var(--surface);
  box-shadow: var(--shadow);
}
.reef-quote-head { grid-column: 1 / -1; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.reef-quote-line { grid-column: 1 / -1; color: var(--muted); font: 400 12px/1.7 var(--font-body); }
.reef-readout { display: grid; border-block-start: 1px solid var(--line); }
.reef-readout > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block: 9px;
  border-block-end: 1px solid var(--line);
}
.reef-readout dt { color: var(--muted); font: 500 10px/1.5 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; }
.reef-readout dd { color: var(--ink); font: 600 13px/1.5 var(--font-mono); }
.reef-quote-body {
  grid-column: 2;
  grid-row: 3 / span 2;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.reef-quote-body > .tide-btn { grid-column: 1 / -1; }
.reef-combo {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
}
.reef-combo b { color: var(--muted); font: 600 11px/1 var(--font-mono); letter-spacing: .08em; }
.reef-total {
  grid-column: 1;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block-start: 12px;
  border-block-start: 1px solid var(--line-strong);
}
.reef-total span { color: var(--muted); font: 500 10px/1.4 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; }
.reef-total strong { color: var(--ink); font: 600 24px/1 var(--font-display); letter-spacing: -.03em; }

/* ------------------------------------------------------------------ split */
.reef-split-band { padding-block-start: clamp(26px, 3.6vw, 44px); }
.reef-split {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
  gap: clamp(18px, 2.6vw, 34px);
  align-items: center;
}
.reef-figure {
  display: grid;
  gap: 12px;
  padding: clamp(14px, 2vw, 22px);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--surface), var(--surface-soft));
}
.reef-figure figcaption { color: var(--muted); font: 400 11px/1.7 var(--font-mono); }
.reef-grid-lines line { stroke: var(--line); stroke-width: 1; }
.reef-band-a { fill: rgba(41, 141, 255, .16); }
.reef-band-b { fill: rgba(41, 141, 255, .42); }
.reef-axis { stroke: var(--line-strong); stroke-width: 1.5; }
.reef-cap { stroke: var(--accent-safe); stroke-width: 2.5; stroke-dasharray: 5 5; }
.reef-cap-label { fill: var(--accent-deep); font: 600 11px/1 var(--font-mono); }
.reef-band-label { fill: var(--ink); font: 600 12px/1 var(--font-mono); letter-spacing: .14em; }
.reef-value { fill: var(--ink-soft); font: 500 13px/1 var(--font-mono); }
.reef-tick { fill: var(--muted); font: 400 10px/1 var(--font-mono); }
.reef-split-readout { display: grid; border-block-start: 1px solid var(--line); }
.reef-split-readout > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block: 9px;
  border-block-end: 1px solid var(--line);
}
.reef-split-readout dt { color: var(--muted); font: 500 10px/1.5 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; }
.reef-split-readout dd { color: var(--ink); font: 600 14px/1.5 var(--font-mono); font-variant-numeric: tabular-nums; }

/* ------------------------------------------------------------------- tape */
.reef-tape { display: flex; gap: 10px; overflow-x: auto; padding-block-end: 4px; scrollbar-width: thin; }
.reef-tape li { flex: 0 0 auto; }
.reef-tape button {
  display: grid;
  grid-template-columns: auto minmax(64px, auto) auto;
  align-items: baseline;
  gap: 4px 12px;
  min-width: 178px;
  padding: 12px 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: var(--surface);
  text-align: start;
  transition: border-color var(--motion-duration) var(--motion-ease), background-color var(--motion-duration) var(--motion-ease);
}
.reef-tape button:hover { border-color: var(--accent-2); }
.reef-tape button.is-on { border-color: var(--accent-safe); background: rgba(41, 141, 255, .08); }
.reef-tape b { color: var(--ink); font: 600 13px/1.3 var(--font-mono); letter-spacing: .05em; }
.reef-tape em { color: var(--ink-soft); font: 500 13px/1.3 var(--font-mono); font-style: normal; text-align: end; }
.reef-tape i { font: 500 11px/1.3 var(--font-mono); font-style: normal; text-align: end; }
.reef-tape small { grid-column: 1 / -1; color: var(--muted); font: 400 10px/1.4 var(--font-mono); }

/* ---------------------------------------------------------------- briefing */
.reef-brief { display: grid; border-block-start: 1px solid var(--line); }
.reef-brief li { border-block-end: 1px solid var(--line); }
.reef-brief a {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr) auto;
  align-items: start;
  gap: 16px;
  padding: 16px 4px;
  color: inherit;
  text-decoration: none;
  transition: background-color var(--motion-duration) var(--motion-ease);
}
.reef-brief a:hover { background: rgba(41, 141, 255, .05); }
.reef-brief b { color: var(--accent-safe); font: 600 12px/1.6 var(--font-mono); letter-spacing: .1em; }
.reef-brief span { display: grid; gap: 3px; }
.reef-brief strong { font: 600 17px/1.35 var(--font-display); letter-spacing: -.02em; }
.reef-brief em { color: var(--muted); font: 400 13px/1.65 var(--font-body); font-style: normal; }
.reef-brief svg { color: var(--accent-safe); margin-block-start: 3px; }

/* ----------------------------------------------------------------- limits */
.reef-limits-band { padding-block-end: clamp(30px, 4vw, 52px); }
.reef-limits {
  display: grid;
  grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
  gap: clamp(18px, 2.6vw, 34px);
  align-items: start;
  padding: clamp(20px, 2.6vw, 30px);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  background:
    radial-gradient(560px 260px at 100% 0%, rgba(41, 141, 255, .13), transparent 70%),
    var(--surface-soft);
}
.reef-limits-copy { display: grid; gap: 8px; }
.reef-limits-list { display: grid; gap: 10px; }
.reef-limits-list li {
  position: relative;
  padding-inline-start: 20px;
  color: var(--ink-soft);
  font: 400 13px/1.6 var(--font-body);
}
.reef-limits-list li::before {
  content: "";
  position: absolute;
  inset-inline-start: 0;
  inset-block-start: .55em;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 2px solid var(--accent);
}
.reef-limits .tide-btn { grid-column: 1 / -1; justify-self: start; }

/* ------------------------------------------------------------ responsive */
@media (max-width: 1180px) {
  .reef-quote { grid-template-columns: minmax(0, 1fr); }
  .reef-quote-body { grid-column: 1; grid-row: auto; }
  .reef-gauge { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .reef-gauge > div:nth-child(4) { border-inline-start: 0; padding-inline-start: 0; }
  .reef-gauge > div:nth-child(-n+3) { border-block-end: 1px solid var(--line); }
}
@media (max-width: 900px) {
  .reef-open { grid-template-columns: minmax(0, 1fr); align-items: start; }
  .reef-split { grid-template-columns: minmax(0, 1fr); }
  .reef-limits { grid-template-columns: minmax(0, 1fr); }
  .reef-limits .tide-btn { justify-self: stretch; }
}
@media (max-width: 620px) {
  .reef-gauge { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .reef-gauge > div:nth-child(4) { border-inline-start: 1px solid var(--line); padding-inline-start: 16px; }
  .reef-gauge > div:nth-child(odd) { border-inline-start: 0; padding-inline-start: 0; }
  .reef-gauge > div:nth-child(even) { border-block-end: 1px solid var(--line); }
  .reef-gauge > div:nth-child(-n+4) { border-block-end: 1px solid var(--line); }
  .reef-brief a { grid-template-columns: 34px minmax(0, 1fr); }
  .reef-brief svg { display: none; }
  .reef-search { width: 100%; }
  .reef-tools { width: 100%; }
  .reef-tools .tide-switch { flex: 1 1 auto; }
  .reef-tools .tide-switch button { flex: 1 1 auto; }
}
</style>
