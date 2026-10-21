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
  <div class="deck">
    <!-- opening command block -->
    <section class="tty-scene pag-open">
      <div class="tty-scene-in pag-open-in">
        <div class="pag-open-copy">
          <p class="tty-kicker">Sheet {{ brand.asset }} / {{ brand.network }} / preview build</p>
          <h1 class="tty-display" tabindex="-1">Read the chain.<br />Price the boundary.<br /><em>Keep the record.</em></h1>
        </div>
        <div class="pag-open-side">
          <p class="tty-lead">{{ brand.supportingLine }}</p>
          <div class="pag-open-actions">
            <a class="tty-btn tty-btn--primary" href="/app/markets" @click.prevent="emit('navigate', '/app/markets')">
              Open the board <ArrowRight :size="15" />
            </a>
            <button class="tty-btn tty-btn--ghost" type="button" @click="toBoundary">Price a boundary</button>
          </div>
          <p class="pag-open-note">
            Sample quotes, a user-priced model and a browser-local journal. Nothing here is live and
            nothing is signed.
          </p>
        </div>
      </div>
    </section>

    <!-- metric strip -->
    <section class="tty-scene pag-facts">
      <div class="tty-scene-in">
        <dl class="tty-facts pag-fact-list">
          <div><dt>Pairs listed</dt><dd>04</dd></div>
          <div><dt>Cap default</dt><dd>+5%</dd></div>
          <div><dt>Epoch</dt><dd>30d</dd></div>
          <div><dt>Feed</dt><dd>Static</dd></div>
          <div><dt>Records</dt><dd>Local</dd></div>
          <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd></div>
        </dl>
      </div>
    </section>

    <div class="pag-deck">
      <div class="pag-col pag-col--main">

    <!-- board scene -->
    <section class="tty-scene pag-board">
      <div class="tty-scene-in">
        <div class="pag-head tty-head--row">
          <h2 id="tbl-title" class="tty-h2">The board</h2>
          <div class="pag-tools">
            <div class="tty-switch" role="group" aria-label="Position type">
              <button v-for="option in ['All', 'Income', 'Upside']" :key="option" type="button"
                      :class="{ 'on': side === option }" :aria-pressed="side === option"
                      @click="side = option">{{ option }}</button>
            </div>
            <label class="pag-search">
              <span class="visually-hidden">Filter the board</span>
              <input v-model="query" type="search" placeholder="Filter by symbol" />
            </label>
          </div>
        </div>

        <div class="tty-table-wrap pag-tbl-wrap">
          <table class="tty-table pag-tbl-table">
            <caption class="visually-hidden">Illustrative {{ brand.network }} pairs with modelled unit prices</caption>
            <thead>
              <tr>
                <th scope="col">Pair</th>
                <th scope="col">Sample spot</th>
                <th scope="col">Move</th>
                <th scope="col" :class="{ 'loud': side === 'Income' }">Income / unit</th>
                <th scope="col" :class="{ 'loud': side === 'Upside' }">Upside / unit</th>
                <th scope="col">Open</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filtered" :key="item.symbol" :class="{ 'sel': item.symbol === selected }">
                <th scope="row">
                  <button class="pag-token" type="button" :aria-pressed="item.symbol === selected" @click="selected = item.symbol">
                    <span class="pag-token-mark" :class="{ 'on': item.symbol === selected }" aria-hidden="true">{{ item.initials }}</span>
                    <span class="pag-token-name"><b>{{ item.symbol }}</b><small>{{ item.name }}</small></span>
                  </button>
                </th>
                <td class="tty-num">{{ spot(item.spot) }}</td>
                <td class="tty-num" :class="item.change >= 0 ? 'up' : 'down'">{{ pct(item.change) }}</td>
                <td class="tty-num">{{ money(item.model.incomePrice) }}</td>
                <td class="tty-num">{{ money(item.model.upsidePrice) }}</td>
                <td><a class="pag-rowlink" :href="`/app/markets/${item.symbol}`"
                       :aria-label="`Open the ${item.symbol} sheet`"
                       @click.prevent="emit('navigate', `/app/markets/${item.symbol}`)">Sheet</a></td>
              </tr>
              <tr v-if="!filtered.length">
                <td class="pag-empty" colspan="6">
                  Nothing matches “{{ query }}”.
                  <button class="pag-rowlink" type="button" @click="query = ''">Clear filter</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="tty-note pag-foot-note">* {{ brand.asset }} is a proposed symbol. No token has been issued and no contract address exists.</p>
      </div>
    </section>

    <!-- unit quote scene -->
      </div>

      <div class="pag-col pag-col--rail">
        <section class="tty-scene pag-quote">
      <div class="tty-scene-in pag-quote-in">
        <div class="pag-quote-copy">
          <h2 id="quote-title" class="tty-h2">Unit quote</h2>
          <p class="pag-quote-line">Example arithmetic only. No live quote is read and no order is placed.</p>
          <dl class="tty-pairs pag-readout">
            <div><dt>Sample spot</dt><dd>{{ spot(asset.spot) }}</dd></div>
            <div><dt>Cap price K</dt><dd>{{ money(model.strike) }}</dd></div>
            <div><dt>Model / unit</dt><dd>{{ money(unitPrice) }}</dd></div>
            <div><dt>Leg</dt><dd>{{ side }}</dd></div>
          </dl>
          <p class="pag-total"><span>Modelled value</span><strong>{{ money(unitPrice * amount) }}</strong></p>
        </div>
        <div class="tty-face pag-quote-face" aria-labelledby="quote-title">
          <span class="tty-pill tty-pill--accent pag-quote-tag"><i aria-hidden="true"></i>Sandbox</span>
          <div class="pag-quote-body">
            <div class="tty-field">
              <label for="quote-asset">Pair</label>
              <select id="quote-asset" v-model="selected" class="tty-input">
                <option v-for="item in assets" :key="item.symbol" :value="item.symbol">{{ item.symbol }} / {{ item.name }}</option>
              </select>
            </div>

            <div class="tty-field">
              <span class="tty-field-label">Leg</span>
              <div class="tty-switch" role="group" aria-label="Position leg">
                <button v-for="option in ['Income', 'Upside']" :key="option" type="button"
                        :class="{ 'on': side === option }" :aria-pressed="side === option"
                        @click="side = option">{{ option }}</button>
              </div>
            </div>

            <div class="tty-field">
              <label for="quote-units">Units</label>
              <span class="tty-combo">
                <input id="quote-units" v-model.number="units" type="number" inputmode="decimal"
                       min="0.01" max="1000000" step="0.01" />
                <b>{{ selected }}</b>
              </span>
            </div>

            <div class="tty-field">
              <label for="quote-cap">Cap K <output>+{{ cap }}%</output></label>
              <input id="quote-cap" v-model.number="cap" class="tty-range" type="range" min="0" max="10" step="1" />
              <span class="tty-scale"><span>0%</span><span>10%</span></span>
            </div>

            <button class="tty-btn tty-btn--primary tty-btn--wide" type="button" :disabled="!amount" @click="toBoundary">
              See the split <ArrowRight :size="15" />
            </button>
          </div>
        </div>
      </div>
    </section>
      </div>
    </div>

    <!-- settlement split scene -->
    <section id="cap" class="tty-scene pag-split">
      <div class="tty-scene-in">
        <div class="pag-head tty-head--row">
          <h2 id="split-title" class="tty-h2">Settlement split</h2>
          <p class="tty-meta">{{ selected }} / cap +{{ cap }}% / settlement at the sample spot</p>
        </div>
        <div class="pag-split-grid">
          <figure class="pag-split-figure">
            <svg viewBox="0 0 640 300" role="img" :aria-label="`${selected} settlement partition at a ${cap} percent cap`">
              <title>{{ selected }} settlement partition</title>
              <desc>Value below the cap is an income leg priced {{ money(model.incomePrice) }} per unit; value above the cap is an upside leg priced {{ money(model.upsidePrice) }} per unit.</desc>
              <g class="plot-grid">
                <line v-for="t in 5" :key="`g${t}`" :x1="60" :x2="620" :y1="40 + t * 44" :y2="40 + t * 44" />
              </g>
              <rect x="60" :y="40" :width="496 * model.incomeShare" height="220" class="plot-band-a" />
              <rect :x="60 + 496 * model.incomeShare" :y="40" :width="496 * model.upsideShare" height="220" class="plot-band-b" />
              <line x1="60" y1="40" x2="60" y2="260" class="plot-axis" />
              <line x1="60" y1="260" x2="620" y2="260" class="plot-axis" />
              <line :x1="60 + 496 * model.incomeShare" y1="40" :x2="60 + 496 * model.incomeShare" y2="260" class="plot-cap" />
              <text :x="60 + 496 * model.incomeShare + 8" y="58" class="plot-cap-label">CAP K {{ money(model.strike) }}</text>
              <text x="72" y="98" class="plot-band-label">INCOME</text>
              <text :x="620 - 8" y="98" class="plot-band-label end" text-anchor="end">UPSIDE</text>
              <text x="72" y="134" class="plot-value">{{ money(model.incomePrice) }} / unit</text>
              <text :x="620 - 8" y="134" class="plot-value end" text-anchor="end">{{ money(model.upsidePrice) }} / unit</text>
              <line x1="60" y1="292" x2="620" y2="292" class="plot-axis" />
              <text x="60" y="288" class="plot-tick">0</text>
              <text :x="60 + 496 * model.incomeShare" y="288" class="plot-tick" text-anchor="middle">K</text>
              <text x="620" y="288" class="plot-tick" text-anchor="end">settlement</text>
            </svg>
            <figcaption>{{ model.incomeShare >= model.upsideShare ? 'Most of the sample value sits below the cap.' : 'Most of the sample value sits above the cap.' }} Example arithmetic.</figcaption>
          </figure>
          <dl class="pag-split-readout">
            <div><dt>Income share</dt><dd>{{ (model.incomeShare * 100).toFixed(1) }}%</dd></div>
            <div><dt>Upside share</dt><dd>{{ (model.upsideShare * 100).toFixed(1) }}%</dd></div>
            <div><dt>Income at settlement</dt><dd>{{ money(model.incomeSettlement) }}</dd></div>
            <div><dt>Upside at settlement</dt><dd>{{ money(model.upsideSettlement) }}</dd></div>
            <div><dt>Model premium</dt><dd>{{ money(model.premium) }}</dd></div>
            <div><dt>Breakeven</dt><dd>{{ money(model.breakeven) }}</dd></div>
            <div><dt>Sample move</dt><dd :class="model.spotChangePercent >= 0 ? 'up' : 'down'">{{ signed(model.spotChangePercent) }}</dd></div>
            <div><dt>Cap</dt><dd>+{{ cap }}%</dd></div>
          </dl>
        </div>
      </div>
    </section>

    <!-- sample tape scene -->
    <section class="tty-scene pag-tape-scene">
      <div class="tty-scene-in">
        <div class="pag-head tty-head--row">
          <h2 id="tape-title" class="tty-h2">Sample tape</h2>
          <p class="tty-meta">Not a feed</p>
        </div>
        <ul class="pag-tape">
          <li v-for="item in tape" :key="item.symbol">
            <button type="button" :aria-pressed="item.symbol === selected"
                    :class="{ 'on': item.symbol === selected }" @click="selected = item.symbol">
              <b>{{ item.symbol }}</b>
              <em>{{ spot(item.spot) }}</em>
              <i :class="item.change >= 0 ? 'up' : 'down'">{{ pct(item.change) }}</i>
              <small>K {{ money(item.model.strike) }}</small>
            </button>
          </li>
        </ul>
      </div>
    </section>

    <!-- briefing scene -->
    <section class="tty-scene pag-brief-scene">
      <div class="tty-scene-in">
        <div class="pag-head tty-head--row">
          <h2 id="brief-title" class="tty-h2">Briefing</h2>
          <p class="tty-meta">Four leaves</p>
        </div>
        <ol class="pag-brief">
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
      </div>
    </section>

    <!-- limits scene -->
    <section class="tty-scene pag-limits">
      <div class="tty-scene-in">
        <div class="tty-face tty-face--halo pag-limits-face">
          <div class="tty-face-head">
            <h2 id="disc-title" class="tty-h2">Limits of this preview</h2>
          </div>
          <ul class="pag-limits-list">
            <li>Quotes are illustrative samples, not a market feed.</li>
            <li>The payoff model uses values you enter.</li>
            <li>Journal records stay in this browser's storage.</li>
            <li>No custody, no signing, no trade execution.</li>
            <li>No contract address is published or implied.</li>
          </ul>
          <button class="tty-btn tty-btn--accent tty-btn--wide pag-limits-cta" type="button" @click="emit('navigate', '/risk')">Read the limits</button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ------------------------------------------------------------ opening scene */
.pag-open { overflow: hidden; padding-top: clamp(40px, 5vw, 78px); }
.pag-open-in {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.85fr);
  gap: clamp(24px, 4vw, 64px);
  align-items: end;
}
.pag-open-copy { display: grid; gap: clamp(16px, 2vw, 26px); min-width: 0; }
.pag-open-side { display: grid; gap: 18px; align-content: end; padding-bottom: 6px; }
.pag-open-actions { display: flex; flex-wrap: wrap; gap: 10px; }
.pag-open-note {
  margin: 0;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  color: var(--faint);
  font: 400 11px/1.8 var(--font-mono);
}


/* -------------------------------------------------------------- metric band */
.pag-facts { padding-block: clamp(26px, 3vw, 44px); }
.pag-fact-list { border-block: 0; }

/* -------------------------------------------------------------------- board */
.pag-head { margin-bottom: clamp(16px, 2vw, 26px); }
.pag-tools { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.pag-search input {
  min-height: 42px;
  min-width: 210px;
  padding: 0 16px;
  border: 1px solid var(--line-2);
  border-radius: var(--radius-pill);
  background: rgba(10, 14, 20, 0.86);
  color: var(--ink);
  font: 400 11px/1 var(--font-mono);
  letter-spacing: 0.04em;
}
.pag-search input::placeholder { color: var(--faint); }
.pag-tbl-wrap { border-radius: var(--radius-md); }
.pag-tbl-table { min-width: 720px; }
.pag-tbl-table .loud { color: var(--accent-safe); }
.pag-tbl-table .sel { background: rgba(255, 0, 0, 0.08); }
.pag-tbl-table .sel td:first-of-type,
.pag-tbl-table .sel th:first-child { box-shadow: inset 2px 0 0 var(--accent); }

.pag-token {
  display: inline-flex;
  align-items: center;
  gap: 11px;
  width: 100%;
  padding: 6px 12px 6px 6px;
  border: 0;
  border-radius: var(--radius-pill);
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: background-color 160ms var(--ease);
}
.pag-token:hover { background: rgba(255, 0, 0, 0.1); }
.pag-token-mark {
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
.pag-token-mark.on {
  background: var(--accent);
  color: #050608;
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.55);
}
.pag-token-name { display: grid; gap: 2px; min-width: 0; }
.pag-token-name b { font: 500 13px/1.2 var(--font-mono); letter-spacing: 0.04em; }
.pag-token-name small { color: var(--faint); font: 400 10px/1.2 var(--font-body); }

.up { color: var(--mint); }
.down { color: var(--rose); }

.pag-rowlink {
  padding: 0;
  border: 0;
  border-bottom: 1px solid rgba(255, 0, 0, 0.5);
  background: none;
  color: var(--accent-safe);
  font: 500 9px/1.6 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  text-decoration: none;
  cursor: pointer;
}
.pag-rowlink:hover { color: var(--ink); border-bottom-color: var(--ink); }
.pag-empty { padding: 26px 12px; color: var(--muted); font: 400 12px/1.7 var(--font-mono); }
.pag-foot-note { margin-top: 16px; }

/* -------------------------------------------------------------------- quote */
.pag-quote-in {
  display: grid;
  grid-template-columns: minmax(0, 0.82fr) minmax(0, 1fr);
  gap: clamp(22px, 3.4vw, 56px);
  align-items: start;
}
.pag-quote-copy { display: grid; gap: 14px; align-content: start; }
.pag-quote-line { margin: 0; max-width: 38ch; color: var(--muted); font: 400 13px/1.7 var(--font-body); }
.pag-quote-body { display: grid; gap: 16px; }
.pag-quote-tag { margin-bottom: clamp(14px, 1.6vw, 20px); }
.pag-readout { margin-top: 4px; border-top: 1px solid var(--line); }
.pag-total {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  margin: 0;
  padding: 14px 0;
  border-top: 1px solid var(--line);
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.pag-total strong {
  color: var(--ink);
  font: 400 30px/1 var(--font-display);
  letter-spacing: -0.02em;
  text-transform: none;
  text-shadow: 0 0 34px rgba(255, 0, 0, 0.3);
}

/* -------------------------------------------------------------------- split */
.pag-split { scroll-margin-top: 120px; }
.pag-split-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
  gap: clamp(20px, 2.6vw, 40px);
  align-items: start;
}
.pag-split-figure { margin: 0; min-width: 0; }
.pag-split-figure svg {
  width: 100%;
  height: auto;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--surface-2), var(--bg-2));
}
.pag-split-figure figcaption {
  margin-top: 12px;
  color: var(--faint);
  font: 400 11px/1.7 var(--font-mono);
}
.plot-grid line { stroke: var(--line); stroke-width: 1; }
.plot-axis { stroke: var(--line-2); stroke-width: 1.5; }
.plot-cap { stroke: var(--accent); stroke-width: 2; }
.plot-cap-label { fill: var(--accent); font: 500 11px var(--font-mono); }
.plot-band-label { fill: var(--ink); font: 500 12px var(--font-mono); letter-spacing: 0.14em; }
.plot-value { fill: var(--muted); font: 400 11px var(--font-mono); }
.plot-tick { fill: var(--faint); font: 400 10px var(--font-mono); }
.plot-band-a { fill: rgba(92, 225, 160, 0.16); }
.plot-band-b { fill: rgba(255, 0, 200, 0.18); }

.pag-split-readout {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin: 0;
  background: var(--line);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.pag-split-readout > div { padding: 16px 18px; background: var(--bg-2); min-width: 0; }
.pag-split-readout dt {
  margin: 0;
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.pag-split-readout dd {
  margin: 8px 0 0;
  color: var(--ink);
  font: 400 20px/1.15 var(--font-display);
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
}
.pag-split-readout dd.up { color: var(--mint); }
.pag-split-readout dd.down { color: var(--rose); }

/* --------------------------------------------------------------------- tape */
.pag-tape {
  display: flex;
  gap: 12px;
  margin: 0;
  padding: 0 0 8px;
  list-style: none;
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--line-2) transparent;
}
.pag-tape > li { flex: 1 1 0; min-width: 176px; }
.pag-tape button {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  gap: 2px 10px;
  width: 100%;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--bg-2);
  text-align: left;
  cursor: pointer;
  transition: border-color 180ms var(--ease), background-color 180ms var(--ease);
}
.pag-tape button:hover { border-color: rgba(255, 0, 0, 0.45); background: var(--surface-2); }
.pag-tape button.on {
  border-color: rgba(255, 0, 0, 0.6);
  background: linear-gradient(160deg, rgba(255, 0, 0, 0.14), var(--bg-2));
  box-shadow: 0 0 30px rgba(255, 0, 0, 0.16);
}
.pag-tape b { grid-column: 1; font: 500 12px/1.3 var(--font-mono); letter-spacing: 0.12em; }
.pag-tape em {
  grid-column: 1;
  grid-row: 2;
  color: var(--ink);
  font: 400 22px/1.2 var(--font-display);
  font-style: normal;
  font-variant-numeric: tabular-nums;
}
.pag-tape i {
  grid-column: 2;
  grid-row: 1;
  font: 500 11px/1.3 var(--font-mono);
  font-style: normal;
  text-align: right;
}
.pag-tape small {
  grid-column: 2;
  grid-row: 2;
  justify-self: end;
  color: var(--faint);
  font: 400 10px/1.3 var(--font-mono);
}

/* ------------------------------------------------------------------ briefing */
.pag-brief {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin: 0;
  padding: 0;
  list-style: none;
  background: var(--line);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.pag-brief li { min-width: 0; background: var(--bg-2); }
.pag-brief a {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: start;
  gap: 18px;
  height: 100%;
  padding: clamp(20px, 2.4vw, 32px);
  text-decoration: none;
  transition: background-color 180ms var(--ease);
}
.pag-brief a:hover { background: rgba(255, 0, 0, 0.07); }
.pag-brief a:hover strong { color: var(--accent-safe); }
.pag-brief b {
  color: var(--faint);
  font: 500 10px/1.9 var(--font-mono);
  letter-spacing: 0.18em;
}
.pag-brief span { display: grid; gap: 8px; min-width: 0; }
.pag-brief strong {
  font: 400 clamp(19px, 1.8vw, 24px)/1.15 var(--font-display);
  letter-spacing: -0.01em;
  transition: color 180ms var(--ease);
}
.pag-brief em {
  color: var(--muted);
  font: 400 12px/1.7 var(--font-body);
  font-style: normal;
}
.pag-brief svg { color: var(--faint); margin-top: 3px; }

/* -------------------------------------------------------------------- limits */
.pag-limits-face {
  display: grid;
  gap: clamp(18px, 2vw, 26px);
  max-width: 780px;
  margin-inline: auto;
}
.pag-limits-list {
  display: grid;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}
.pag-limits-list li {
  position: relative;
  padding: 12px 0 12px 24px;
  border-bottom: 1px solid var(--line);
  color: var(--ink-2);
  font: 400 13px/1.6 var(--font-mono);
}
.pag-limits-list li::before {
  content: '';
  position: absolute;
  top: 22px;
  left: 4px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 12px rgba(255, 0, 0, 0.8);
}
.pag-limits-cta { margin-top: 4px; }

/* ---------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .pag-open-in { grid-template-columns: minmax(0, 1fr); align-items: start; }
  .pag-quote-in { grid-template-columns: minmax(0, 1fr); }
  .pag-split-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 860px) {
  .pag-brief { grid-template-columns: minmax(0, 1fr); }
  .pag-tools { width: 100%; }
  .pag-search { flex: 1 1 100%; }
  .pag-search input { width: 100%; min-width: 0; }
}
@media (max-width: 620px) {
  .pag-split-readout { grid-template-columns: minmax(0, 1fr); }
  .pag-open-actions { display: grid; }
  .pag-tape > li { flex: 0 0 min(78vw, 240px); }
}

/* ------------------------------------------------------------ console deck */
.pag-deck {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 366px);
  align-items: stretch;
  border-bottom: 1px solid var(--line);
}
.pag-col { min-width: 0; display: flex; flex-direction: column; }
.pag-col + .pag-col {
  border-left: 1px solid var(--line);
  background: rgba(13, 20, 27, 0.35);
}
.pag-col .tty-scene { border-bottom: 0; }
.pag-col .tty-scene + .tty-scene { border-top: 1px solid var(--line); }

.pag-col--rail .pag-quote-in { grid-template-columns: minmax(0, 1fr); }
.pag-col--rail .pag-split-grid { grid-template-columns: minmax(0, 1fr); }
.pag-col--rail .pag-split-readout { grid-template-columns: minmax(0, 1fr); }

@media (max-width: 1080px) {
  .pag-deck { grid-template-columns: minmax(0, 1fr); }
  .pag-col + .pag-col { border-left: 0; border-top: 1px solid var(--line); }
}
</style>
