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
    <!-- opening scene -->
    <section class="atlas-scene deck-open">
      <div class="deck-orbit" aria-hidden="true">
        <span class="deck-ring deck-ring--a"></span>
        <span class="deck-ring deck-ring--b"></span>
        <span class="deck-ring deck-ring--c"></span>
        <i class="deck-core"></i>
      </div>
      <div class="atlas-scene-in deck-open-in">
        <div class="deck-open-copy">
          <p class="atlas-kicker">Sheet {{ brand.asset }} / {{ brand.network }} / preview build</p>
          <h1 class="atlas-display" tabindex="-1">Read the chain.<br />Price the boundary.<br /><em>Keep the record.</em></h1>
        </div>
        <div class="deck-open-side">
          <p class="atlas-lead">{{ brand.supportingLine }}</p>
          <div class="deck-open-actions">
            <a class="atlas-btn atlas-btn--primary" href="/app/markets" @click.prevent="emit('navigate', '/app/markets')">
              Open the board <ArrowRight :size="15" />
            </a>
            <button class="atlas-btn atlas-btn--ghost" type="button" @click="toBoundary">Price a boundary</button>
          </div>
          <p class="deck-open-note">
            Sample quotes, a user-priced model and a browser-local journal. Nothing here is live and
            nothing is signed.
          </p>
        </div>
      </div>
    </section>

    <!-- metric ribbon -->
    <section class="atlas-scene deck-facts">
      <div class="atlas-scene-in">
        <dl class="atlas-facts deck-fact-list">
          <div><dt>Pairs listed</dt><dd>04</dd></div>
          <div><dt>Cap default</dt><dd>+5%</dd></div>
          <div><dt>Epoch</dt><dd>30d</dd></div>
          <div><dt>Feed</dt><dd>Static</dd></div>
          <div><dt>Records</dt><dd>Local</dd></div>
          <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd></div>
        </dl>
      </div>
    </section>

    <!-- board scene -->
    <section class="atlas-scene deck-board">
      <div class="atlas-scene-in">
        <div class="deck-head atlas-head--row">
          <h2 id="board-title" class="atlas-h2">The board</h2>
          <div class="deck-tools">
            <div class="atlas-switch" role="group" aria-label="Position type">
              <button v-for="option in ['All', 'Income', 'Upside']" :key="option" type="button"
                      :class="{ 'is-lit': side === option }" :aria-pressed="side === option"
                      @click="side = option">{{ option }}</button>
            </div>
            <label class="deck-search">
              <span class="sr-only">Filter the board</span>
              <input v-model="query" type="search" placeholder="Filter by symbol" />
            </label>
          </div>
        </div>

        <div class="atlas-table-wrap deck-board-wrap">
          <table class="atlas-table deck-board-table">
            <caption class="sr-only">Illustrative {{ brand.network }} pairs with modelled unit prices</caption>
            <thead>
              <tr>
                <th scope="col">Pair</th>
                <th scope="col">Sample spot</th>
                <th scope="col">Move</th>
                <th scope="col" :class="{ 'is-loud': side === 'Income' }">Income / unit</th>
                <th scope="col" :class="{ 'is-loud': side === 'Upside' }">Upside / unit</th>
                <th scope="col">Open</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filtered" :key="item.symbol" :class="{ 'is-chord': item.symbol === selected }">
                <th scope="row">
                  <button class="deck-token" type="button" :aria-pressed="item.symbol === selected" @click="selected = item.symbol">
                    <span class="deck-token-mark" :class="{ 'is-lit': item.symbol === selected }" aria-hidden="true">{{ item.initials }}</span>
                    <span class="deck-token-name"><b>{{ item.symbol }}</b><small>{{ item.name }}</small></span>
                  </button>
                </th>
                <td class="atlas-num">{{ spot(item.spot) }}</td>
                <td class="atlas-num" :class="item.change >= 0 ? 'is-rise' : 'is-fall'">{{ pct(item.change) }}</td>
                <td class="atlas-num">{{ money(item.model.incomePrice) }}</td>
                <td class="atlas-num">{{ money(item.model.upsidePrice) }}</td>
                <td><a class="deck-rowlink" :href="`/app/markets/${item.symbol}`"
                       :aria-label="`Open the ${item.symbol} sheet`"
                       @click.prevent="emit('navigate', `/app/markets/${item.symbol}`)">Sheet</a></td>
              </tr>
              <tr v-if="!filtered.length">
                <td class="deck-empty" colspan="6">
                  Nothing matches “{{ query }}”.
                  <button class="deck-rowlink" type="button" @click="query = ''">Clear filter</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="atlas-note deck-foot-note">* {{ brand.asset }} is a proposed symbol. No token has been issued and no contract address exists.</p>
      </div>
    </section>

    <!-- unit quote scene -->
    <section class="atlas-scene deck-quote">
      <div class="atlas-scene-in deck-quote-in">
        <div class="deck-quote-copy">
          <h2 id="quote-title" class="atlas-h2">Unit quote</h2>
          <p class="deck-quote-line">Example arithmetic only. No live quote is read and no order is placed.</p>
          <dl class="atlas-pairs deck-readout">
            <div><dt>Sample spot</dt><dd>{{ spot(asset.spot) }}</dd></div>
            <div><dt>Cap price K</dt><dd>{{ money(model.strike) }}</dd></div>
            <div><dt>Model / unit</dt><dd>{{ money(unitPrice) }}</dd></div>
            <div><dt>Leg</dt><dd>{{ side }}</dd></div>
          </dl>
          <p class="deck-total"><span>Modelled value</span><strong>{{ money(unitPrice * amount) }}</strong></p>
        </div>
        <div class="atlas-face deck-quote-face" aria-labelledby="quote-title">
          <span class="atlas-pill atlas-pill--beam deck-quote-tag"><i aria-hidden="true"></i>Sandbox</span>
          <div class="deck-quote-body">
            <div class="atlas-field">
              <label for="quote-asset">Pair</label>
              <select id="quote-asset" v-model="selected" class="atlas-input">
                <option v-for="item in assets" :key="item.symbol" :value="item.symbol">{{ item.symbol }} / {{ item.name }}</option>
              </select>
            </div>

            <div class="atlas-field">
              <span class="atlas-field-label">Leg</span>
              <div class="atlas-switch" role="group" aria-label="Position leg">
                <button v-for="option in ['Income', 'Upside']" :key="option" type="button"
                        :class="{ 'is-lit': side === option }" :aria-pressed="side === option"
                        @click="side = option">{{ option }}</button>
              </div>
            </div>

            <div class="atlas-field">
              <label for="quote-units">Units</label>
              <span class="atlas-combo">
                <input id="quote-units" v-model.number="units" type="number" inputmode="decimal"
                       min="0.01" max="1000000" step="0.01" />
                <b>{{ selected }}</b>
              </span>
            </div>

            <div class="atlas-field">
              <label for="quote-cap">Cap K <output>+{{ cap }}%</output></label>
              <input id="quote-cap" v-model.number="cap" class="atlas-range" type="range" min="0" max="10" step="1" />
              <span class="atlas-scale"><span>0%</span><span>10%</span></span>
            </div>

            <button class="atlas-btn atlas-btn--primary atlas-btn--wide" type="button" :disabled="!amount" @click="toBoundary">
              See the split <ArrowRight :size="15" />
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- settlement split scene -->
    <section id="cap" class="atlas-scene deck-split">
      <div class="atlas-scene-in">
        <div class="deck-head atlas-head--row">
          <h2 id="split-title" class="atlas-h2">Settlement split</h2>
          <p class="atlas-meta">{{ selected }} / cap +{{ cap }}% / settlement at the sample spot</p>
        </div>
        <div class="deck-split-grid">
          <figure class="deck-split-figure">
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
              <text :x="620 - 8" y="98" class="plot-band-label is-anchor-end" text-anchor="end">UPSIDE</text>
              <text x="72" y="134" class="plot-value">{{ money(model.incomePrice) }} / unit</text>
              <text :x="620 - 8" y="134" class="plot-value is-anchor-end" text-anchor="end">{{ money(model.upsidePrice) }} / unit</text>
              <line x1="60" y1="292" x2="620" y2="292" class="plot-axis" />
              <text x="60" y="288" class="plot-tick">0</text>
              <text :x="60 + 496 * model.incomeShare" y="288" class="plot-tick" text-anchor="middle">K</text>
              <text x="620" y="288" class="plot-tick" text-anchor="end">settlement</text>
            </svg>
            <figcaption>{{ model.incomeShare >= model.upsideShare ? 'Most of the sample value sits below the cap.' : 'Most of the sample value sits above the cap.' }} Example arithmetic.</figcaption>
          </figure>
          <dl class="deck-split-readout">
            <div><dt>Income share</dt><dd>{{ (model.incomeShare * 100).toFixed(1) }}%</dd></div>
            <div><dt>Upside share</dt><dd>{{ (model.upsideShare * 100).toFixed(1) }}%</dd></div>
            <div><dt>Income at settlement</dt><dd>{{ money(model.incomeSettlement) }}</dd></div>
            <div><dt>Upside at settlement</dt><dd>{{ money(model.upsideSettlement) }}</dd></div>
            <div><dt>Model premium</dt><dd>{{ money(model.premium) }}</dd></div>
            <div><dt>Breakeven</dt><dd>{{ money(model.breakeven) }}</dd></div>
            <div><dt>Sample move</dt><dd :class="model.spotChangePercent >= 0 ? 'is-rise' : 'is-fall'">{{ signed(model.spotChangePercent) }}</dd></div>
            <div><dt>Cap</dt><dd>+{{ cap }}%</dd></div>
          </dl>
        </div>
      </div>
    </section>

    <!-- sample tape scene -->
    <section class="atlas-scene deck-tape-scene">
      <div class="atlas-scene-in">
        <div class="deck-head atlas-head--row">
          <h2 id="tape-title" class="atlas-h2">Sample tape</h2>
          <p class="atlas-meta">Not a feed</p>
        </div>
        <ul class="deck-tape">
          <li v-for="item in tape" :key="item.symbol">
            <button type="button" :aria-pressed="item.symbol === selected"
                    :class="{ 'is-lit': item.symbol === selected }" @click="selected = item.symbol">
              <b>{{ item.symbol }}</b>
              <em>{{ spot(item.spot) }}</em>
              <i :class="item.change >= 0 ? 'is-rise' : 'is-fall'">{{ pct(item.change) }}</i>
              <small>K {{ money(item.model.strike) }}</small>
            </button>
          </li>
        </ul>
      </div>
    </section>

    <!-- briefing scene -->
    <section class="atlas-scene deck-brief-scene">
      <div class="atlas-scene-in">
        <div class="deck-head atlas-head--row">
          <h2 id="brief-title" class="atlas-h2">Briefing</h2>
          <p class="atlas-meta">Four leaves</p>
        </div>
        <ol class="deck-brief">
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
    <section class="atlas-scene deck-limits">
      <div class="atlas-scene-in">
        <div class="atlas-face atlas-face--halo deck-limits-face">
          <div class="atlas-face-head">
            <h2 id="disc-title" class="atlas-h2">Limits of this preview</h2>
          </div>
          <ul class="deck-limits-list">
            <li>Quotes are illustrative samples, not a market feed.</li>
            <li>The payoff model uses values you enter.</li>
            <li>Journal records stay in this browser's storage.</li>
            <li>No custody, no signing, no trade execution.</li>
            <li>No contract address is published or implied.</li>
          </ul>
          <button class="atlas-btn atlas-btn--accent atlas-btn--wide deck-limits-cta" type="button" @click="emit('navigate', '/risk')">Read the limits</button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ------------------------------------------------------------ opening scene */
.deck-open { overflow: hidden; padding-top: clamp(40px, 5vw, 78px); }
.deck-open-in {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.85fr);
  gap: clamp(24px, 4vw, 64px);
  align-items: end;
}
.deck-open-copy { display: grid; gap: clamp(16px, 2vw, 26px); min-width: 0; }
.deck-open-side { display: grid; gap: 18px; align-content: end; padding-bottom: 6px; }
.deck-open-actions { display: flex; flex-wrap: wrap; gap: 10px; }
.deck-open-note {
  margin: 0;
  padding-top: 14px;
  border-top: 1px solid var(--hair);
  color: var(--star-faint);
  font: 400 11px/1.8 var(--font-mono);
}

.deck-orbit {
  position: absolute;
  top: -30%;
  right: -8%;
  width: min(58vw, 680px);
  aspect-ratio: 1;
  pointer-events: none;
}
.deck-ring {
  position: absolute;
  border: 1px solid rgba(64, 179, 255, 0.16);
  border-radius: 50%;
}
.deck-ring--a { inset: 0; border-color: rgba(167, 139, 250, 0.18); }
.deck-ring--b { inset: 12%; border-color: rgba(64, 179, 255, 0.2); }
.deck-ring--c { inset: 26%; border-color: rgba(64, 179, 255, 0.12); }
.deck-core {
  position: absolute;
  inset: 20%;
  border-radius: 50%;
  background:
    conic-gradient(from 150deg, rgba(64, 179, 255, 0.26), rgba(167, 139, 250, 0.14) 42%, rgba(64, 179, 255, 0.26) 80%, rgba(167, 139, 250, 0.14));
  filter: blur(48px);
  opacity: 0.5;
}

/* -------------------------------------------------------------- metric band */
.deck-facts { padding-block: clamp(26px, 3vw, 44px); }
.deck-fact-list { border-block: 0; }

/* -------------------------------------------------------------------- board */
.deck-head { margin-bottom: clamp(16px, 2vw, 26px); }
.deck-tools { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.deck-search input {
  min-height: 42px;
  min-width: 210px;
  padding: 0 16px;
  border: 1px solid var(--hair-2);
  border-radius: var(--r-pill);
  background: rgba(11, 12, 21, 0.86);
  color: var(--star);
  font: 400 11px/1 var(--font-mono);
  letter-spacing: 0.04em;
}
.deck-search input::placeholder { color: var(--star-faint); }
.deck-board-wrap { border-radius: var(--r-md); }
.deck-board-table { min-width: 720px; }
.deck-board-table .is-loud { color: var(--beam); }
.deck-board-table .is-chord { background: rgba(64, 179, 255, 0.08); }
.deck-board-table .is-chord td:first-of-type,
.deck-board-table .is-chord th:first-child { box-shadow: inset 2px 0 0 var(--beam); }

.deck-token {
  display: inline-flex;
  align-items: center;
  gap: 11px;
  width: 100%;
  padding: 6px 12px 6px 6px;
  border: 0;
  border-radius: var(--r-pill);
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: background-color 160ms var(--ease);
}
.deck-token:hover { background: rgba(64, 179, 255, 0.1); }
.deck-token-mark {
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
.deck-token-mark.is-lit {
  background: var(--beam);
  color: #04060d;
  box-shadow: 0 0 20px rgba(64, 179, 255, 0.55);
}
.deck-token-name { display: grid; gap: 2px; min-width: 0; }
.deck-token-name b { font: 500 13px/1.2 var(--font-mono); letter-spacing: 0.04em; }
.deck-token-name small { color: var(--star-faint); font: 400 10px/1.2 var(--font-body); }

.is-rise { color: var(--mint); }
.is-fall { color: var(--rose); }

.deck-rowlink {
  padding: 0;
  border: 0;
  border-bottom: 1px solid rgba(64, 179, 255, 0.5);
  background: none;
  color: var(--beam);
  font: 500 9px/1.6 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  text-decoration: none;
  cursor: pointer;
}
.deck-rowlink:hover { color: var(--star); border-bottom-color: var(--star); }
.deck-empty { padding: 26px 12px; color: var(--star-mute); font: 400 12px/1.7 var(--font-mono); }
.deck-foot-note { margin-top: 16px; }

/* -------------------------------------------------------------------- quote */
.deck-quote-in {
  display: grid;
  grid-template-columns: minmax(0, 0.82fr) minmax(0, 1fr);
  gap: clamp(22px, 3.4vw, 56px);
  align-items: start;
}
.deck-quote-copy { display: grid; gap: 14px; align-content: start; }
.deck-quote-line { margin: 0; max-width: 38ch; color: var(--star-mute); font: 400 13px/1.7 var(--font-body); }
.deck-quote-body { display: grid; gap: 16px; }
.deck-quote-tag { margin-bottom: clamp(14px, 1.6vw, 20px); }
.deck-readout { margin-top: 4px; border-top: 1px solid var(--hair); }
.deck-total {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  margin: 0;
  padding: 14px 0;
  border-top: 1px solid var(--hair);
  color: var(--star-faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.deck-total strong {
  color: var(--star);
  font: 400 30px/1 var(--font-display);
  letter-spacing: -0.02em;
  text-transform: none;
  text-shadow: 0 0 34px rgba(64, 179, 255, 0.3);
}

/* -------------------------------------------------------------------- split */
.deck-split { scroll-margin-top: 120px; }
.deck-split-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
  gap: clamp(20px, 2.6vw, 40px);
  align-items: start;
}
.deck-split-figure { margin: 0; min-width: 0; }
.deck-split-figure svg {
  width: 100%;
  height: auto;
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  background: linear-gradient(180deg, var(--deck-2), var(--void-2));
}
.deck-split-figure figcaption {
  margin-top: 12px;
  color: var(--star-faint);
  font: 400 11px/1.7 var(--font-mono);
}
.plot-grid line { stroke: var(--hair); stroke-width: 1; }
.plot-axis { stroke: var(--hair-2); stroke-width: 1.5; }
.plot-cap { stroke: var(--beam); stroke-width: 2; }
.plot-cap-label { fill: var(--beam); font: 500 11px var(--font-mono); }
.plot-band-label { fill: var(--star); font: 500 12px var(--font-mono); letter-spacing: 0.14em; }
.plot-value { fill: var(--star-mute); font: 400 11px var(--font-mono); }
.plot-tick { fill: var(--star-faint); font: 400 10px var(--font-mono); }
.plot-band-a { fill: rgba(92, 225, 160, 0.16); }
.plot-band-b { fill: rgba(167, 139, 250, 0.18); }

.deck-split-readout {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin: 0;
  background: var(--hair);
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  overflow: hidden;
}
.deck-split-readout > div { padding: 16px 18px; background: var(--void-2); min-width: 0; }
.deck-split-readout dt {
  margin: 0;
  color: var(--star-faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.deck-split-readout dd {
  margin: 8px 0 0;
  color: var(--star);
  font: 400 20px/1.15 var(--font-display);
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
}
.deck-split-readout dd.is-rise { color: var(--mint); }
.deck-split-readout dd.is-fall { color: var(--rose); }

/* --------------------------------------------------------------------- tape */
.deck-tape {
  display: flex;
  gap: 12px;
  margin: 0;
  padding: 0 0 8px;
  list-style: none;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin;
  scrollbar-color: var(--hair-2) transparent;
}
.deck-tape > li { flex: 1 1 0; min-width: 176px; scroll-snap-align: start; }
.deck-tape button {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  gap: 2px 10px;
  width: 100%;
  padding: 16px;
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  background: var(--void-2);
  text-align: left;
  cursor: pointer;
  transition: border-color 180ms var(--ease), background-color 180ms var(--ease);
}
.deck-tape button:hover { border-color: rgba(64, 179, 255, 0.45); background: var(--deck-2); }
.deck-tape button.is-lit {
  border-color: rgba(64, 179, 255, 0.6);
  background: linear-gradient(160deg, rgba(64, 179, 255, 0.14), var(--void-2));
  box-shadow: 0 0 30px rgba(64, 179, 255, 0.16);
}
.deck-tape b { grid-column: 1; font: 500 12px/1.3 var(--font-mono); letter-spacing: 0.12em; }
.deck-tape em {
  grid-column: 1;
  grid-row: 2;
  color: var(--star);
  font: 400 22px/1.2 var(--font-display);
  font-style: normal;
  font-variant-numeric: tabular-nums;
}
.deck-tape i {
  grid-column: 2;
  grid-row: 1;
  font: 500 11px/1.3 var(--font-mono);
  font-style: normal;
  text-align: right;
}
.deck-tape small {
  grid-column: 2;
  grid-row: 2;
  justify-self: end;
  color: var(--star-faint);
  font: 400 10px/1.3 var(--font-mono);
}

/* ------------------------------------------------------------------ briefing */
.deck-brief {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin: 0;
  padding: 0;
  list-style: none;
  background: var(--hair);
  border: 1px solid var(--hair);
  border-radius: var(--r-lg);
  overflow: hidden;
}
.deck-brief li { min-width: 0; background: var(--void-2); }
.deck-brief a {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: start;
  gap: 18px;
  height: 100%;
  padding: clamp(20px, 2.4vw, 32px);
  text-decoration: none;
  transition: background-color 180ms var(--ease);
}
.deck-brief a:hover { background: rgba(64, 179, 255, 0.07); }
.deck-brief a:hover strong { color: var(--beam); }
.deck-brief b {
  color: var(--star-faint);
  font: 500 10px/1.9 var(--font-mono);
  letter-spacing: 0.18em;
}
.deck-brief span { display: grid; gap: 8px; min-width: 0; }
.deck-brief strong {
  font: 400 clamp(19px, 1.8vw, 24px)/1.15 var(--font-display);
  letter-spacing: -0.01em;
  transition: color 180ms var(--ease);
}
.deck-brief em {
  color: var(--star-mute);
  font: 400 12px/1.7 var(--font-body);
  font-style: normal;
}
.deck-brief svg { color: var(--star-faint); margin-top: 3px; }

/* -------------------------------------------------------------------- limits */
.deck-limits-face {
  display: grid;
  gap: clamp(18px, 2vw, 26px);
  max-width: 780px;
  margin-inline: auto;
}
.deck-limits-list {
  display: grid;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}
.deck-limits-list li {
  position: relative;
  padding: 12px 0 12px 24px;
  border-bottom: 1px solid var(--hair);
  color: var(--star-2);
  font: 400 13px/1.6 var(--font-mono);
}
.deck-limits-list li::before {
  content: '';
  position: absolute;
  top: 22px;
  left: 4px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--beam);
  box-shadow: 0 0 12px rgba(64, 179, 255, 0.8);
}
.deck-limits-cta { margin-top: 4px; }

/* ---------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .deck-open-in { grid-template-columns: minmax(0, 1fr); align-items: start; }
  .deck-quote-in { grid-template-columns: minmax(0, 1fr); }
  .deck-split-grid { grid-template-columns: minmax(0, 1fr); }
  .deck-orbit { top: -8%; right: -18%; width: min(78vw, 560px); opacity: 0.75; }
}
@media (max-width: 860px) {
  .deck-brief { grid-template-columns: minmax(0, 1fr); }
  .deck-tools { width: 100%; }
  .deck-search { flex: 1 1 100%; }
  .deck-search input { width: 100%; min-width: 0; }
}
@media (max-width: 620px) {
  .deck-split-readout { grid-template-columns: minmax(0, 1fr); }
  .deck-open-actions { display: grid; }
  .deck-tape > li { flex: 0 0 min(78vw, 240px); }
}
</style>
