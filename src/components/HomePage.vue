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
  <div class="bl-page bl-home">
    <div class="bl-bento">
      <!-- anchor tile: the opening -->
      <section class="bl-tile bl-tile--tint bl-span-7 bl-home-open">
        <div class="bl-home-open-copy">
          <p class="bl-kicker">Sheet {{ brand.asset }} / {{ brand.network }} / preview build</p>
          <h1 class="bl-display bl-home-title" tabindex="-1">Read the chain.<br />Price the boundary.<br /><em>Keep the record.</em></h1>
        </div>
        <div class="bl-home-open-act">
          <a class="bl-btn bl-btn--primary" href="/app/markets" @click.prevent="emit('navigate', '/app/markets')">
            Open the board <ArrowRight :size="15" />
          </a>
          <button class="bl-btn" type="button" @click="toBoundary">Price a boundary</button>
        </div>
      </section>

      <!-- support tile: the thesis -->
      <section class="bl-tile bl-span-5 bl-home-brief">
        <p class="bl-lead">{{ brand.supportingLine }}</p>
        <p class="bl-note">Sample quotes, a user-priced model and a browser-local journal. Nothing here is live and nothing is signed.</p>
      </section>

      <!-- gauge band -->
      <section class="bl-tile bl-tile--surface bl-span-12 bl-home-gauge">
        <dl class="bl-gauge">
          <div><dt>Pairs listed</dt><dd>04</dd></div>
          <div><dt>Cap default</dt><dd>+5%</dd></div>
          <div><dt>Epoch</dt><dd>30d</dd></div>
          <div><dt>Feed</dt><dd>Static</dd></div>
          <div><dt>Records</dt><dd>Local</dd></div>
          <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd></div>
        </dl>
      </section>

      <!-- board: wide tile -->
      <section class="bl-tile bl-span-8 bl-board">
        <div class="bl-tile-head bl-board-head">
          <h2 id="tbl-title" class="bl-h2">The board</h2>
          <div class="bl-board-tools">
            <div class="bl-switch" role="group" aria-label="Position type">
              <button v-for="option in ['All', 'Income', 'Upside']" :key="option" type="button"
                      :class="{ 'is-live': side === option }" :aria-pressed="side === option"
                      @click="side = option">{{ option }}</button>
            </div>
            <label class="bl-search">
              <span class="visually-hidden">Filter the board</span>
              <input v-model="query" type="search" class="bl-input" placeholder="Filter by symbol" />
            </label>
          </div>
        </div>

        <div class="bl-table-wrap">
          <table class="bl-table bl-board-grid">
            <caption class="visually-hidden">Illustrative {{ brand.network }} pairs with modelled unit prices</caption>
            <thead>
              <tr>
                <th scope="col">Pair</th>
                <th scope="col" class="bl-num">Sample spot</th>
                <th scope="col" class="bl-num">Move</th>
                <th scope="col" class="bl-num" :class="{ 'bl-loud': side === 'Income' }">Income / unit</th>
                <th scope="col" class="bl-num" :class="{ 'bl-loud': side === 'Upside' }">Upside / unit</th>
                <th scope="col">Open</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filtered" :key="item.symbol" :class="{ 'is-chosen': item.symbol === selected }">
                <th scope="row">
                  <button class="bl-token" type="button" :aria-pressed="item.symbol === selected" @click="selected = item.symbol">
                    <span class="bl-token-mark" :class="{ 'is-live': item.symbol === selected }" aria-hidden="true">{{ item.initials }}</span>
                    <span class="bl-token-name"><b>{{ item.symbol }}</b><small>{{ item.name }}</small></span>
                  </button>
                </th>
                <td class="bl-num">{{ spot(item.spot) }}</td>
                <td class="bl-num" :class="item.change >= 0 ? 'is-pos' : 'is-neg'">{{ pct(item.change) }}</td>
                <td class="bl-num">{{ money(item.model.incomePrice) }}</td>
                <td class="bl-num">{{ money(item.model.upsidePrice) }}</td>
                <td><a class="bl-rowlink" :href="`/app/markets/${item.symbol}`"
                       :aria-label="`Open the ${item.symbol} sheet`"
                       @click.prevent="emit('navigate', `/app/markets/${item.symbol}`)">Sheet</a></td>
              </tr>
              <tr v-if="!filtered.length">
                <td class="bl-empty" colspan="6">
                  Nothing matches “{{ query }}”.
                  <button class="bl-rowlink" type="button" @click="query = ''">Clear filter</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="bl-note bl-board-note">* {{ brand.asset }} is a proposed symbol. No token has been issued and no contract address exists.</p>
      </section>

      <!-- quote: compact trade widget -->
      <section class="bl-tile bl-span-4 bl-quote" aria-labelledby="quote-title">
        <div class="bl-tile-head bl-quote-head">
          <h2 id="quote-title" class="bl-h2">Unit quote</h2>
          <span class="bl-chip bl-chip--accent"><i aria-hidden="true"></i>Sandbox</span>
        </div>
        <p class="bl-note">Example arithmetic only. No live quote is read and no order is placed.</p>

        <dl class="bl-rows bl-quote-read">
          <div><dt>Sample spot</dt><dd>{{ spot(asset.spot) }}</dd></div>
          <div><dt>Cap price K</dt><dd>{{ money(model.strike) }}</dd></div>
          <div><dt>Model / unit</dt><dd>{{ money(unitPrice) }}</dd></div>
          <div><dt>Leg</dt><dd>{{ side }}</dd></div>
        </dl>

        <div class="bl-quote-form">
          <div class="bl-field">
            <label for="quote-asset">Pair</label>
            <select id="quote-asset" v-model="selected" class="bl-input">
              <option v-for="item in assets" :key="item.symbol" :value="item.symbol">{{ item.symbol }} / {{ item.name }}</option>
            </select>
          </div>

          <div class="bl-field">
            <span class="bl-field-label">Leg</span>
            <div class="bl-switch" role="group" aria-label="Position leg">
              <button v-for="option in ['Income', 'Upside']" :key="option" type="button"
                      :class="{ 'is-live': side === option }" :aria-pressed="side === option"
                      @click="side = option">{{ option }}</button>
            </div>
          </div>

          <div class="bl-field">
            <label for="quote-units">Units</label>
            <span class="bl-combo">
              <input id="quote-units" v-model.number="units" class="bl-input" type="number" inputmode="decimal"
                     min="0.01" max="1000000" step="0.01" />
              <b>{{ selected }}</b>
            </span>
          </div>

          <div class="bl-field">
            <label for="quote-cap">Cap K <output>+{{ cap }}%</output></label>
            <input id="quote-cap" v-model.number="cap" class="bl-range" type="range" min="0" max="10" step="1" />
            <span class="bl-scale"><span>0%</span><span>10%</span></span>
          </div>

          <button class="bl-btn bl-btn--primary bl-btn--wide" type="button" :disabled="!amount" @click="toBoundary">
            See the split <ArrowRight :size="15" />
          </button>
        </div>

        <p class="bl-quote-total"><span>Modelled value</span><strong>{{ money(unitPrice * amount) }}</strong></p>
      </section>

      <!-- settlement split: figure + readout -->
      <section id="cap" class="bl-tile bl-span-7 bl-split">
        <div class="bl-tile-head">
          <h2 id="split-title" class="bl-h2">Settlement split</h2>
          <p class="bl-meta">{{ selected }} / cap +{{ cap }}% / settlement at the sample spot</p>
        </div>
        <figure class="bl-figure bl-split-figure">
          <svg viewBox="0 0 640 300" role="img" :aria-label="`${selected} settlement partition at a ${cap} percent cap`">
            <title>{{ selected }} settlement partition</title>
            <desc>Value below the cap is an income leg priced {{ money(model.incomePrice) }} per unit; value above the cap is an upside leg priced {{ money(model.upsidePrice) }} per unit.</desc>
            <g class="bl-split-grid">
              <line v-for="t in 5" :key="`g${t}`" :x1="60" :x2="620" :y1="40 + t * 44" :y2="40 + t * 44" />
            </g>
            <rect x="60" :y="40" :width="496 * model.incomeShare" height="220" class="bl-band-a" />
            <rect :x="60 + 496 * model.incomeShare" :y="40" :width="496 * model.upsideShare" height="220" class="bl-band-b" />
            <line x1="60" y1="40" x2="60" y2="260" class="bl-axis" />
            <line x1="60" y1="260" x2="620" y2="260" class="bl-axis" />
            <line :x1="60 + 496 * model.incomeShare" y1="40" :x2="60 + 496 * model.incomeShare" y2="260" class="bl-cap" />
            <text :x="60 + 496 * model.incomeShare + 8" y="58" class="bl-cap-label">CAP K {{ money(model.strike) }}</text>
            <text x="72" y="98" class="bl-band-label">INCOME</text>
            <text :x="620 - 8" y="98" class="bl-band-label is-end" text-anchor="end">UPSIDE</text>
            <text x="72" y="134" class="bl-value">{{ money(model.incomePrice) }} / unit</text>
            <text :x="620 - 8" y="134" class="bl-value is-end" text-anchor="end">{{ money(model.upsidePrice) }} / unit</text>
            <line x1="60" y1="292" x2="620" y2="292" class="bl-axis" />
            <text x="60" y="288" class="bl-tick">0</text>
            <text :x="60 + 496 * model.incomeShare" y="288" class="bl-tick" text-anchor="middle">K</text>
            <text x="620" y="288" class="bl-tick" text-anchor="end">settlement</text>
          </svg>
          <figcaption>{{ model.incomeShare >= model.upsideShare ? 'Most of the sample value sits below the cap.' : 'Most of the sample value sits above the cap.' }} Example arithmetic.</figcaption>
        </figure>
      </section>

      <section class="bl-tile bl-tile--surface bl-span-5 bl-split-read">
        <dl class="bl-rows">
          <div><dt>Income share</dt><dd>{{ (model.incomeShare * 100).toFixed(1) }}%</dd></div>
          <div><dt>Upside share</dt><dd>{{ (model.upsideShare * 100).toFixed(1) }}%</dd></div>
          <div><dt>Income at settlement</dt><dd>{{ money(model.incomeSettlement) }}</dd></div>
          <div><dt>Upside at settlement</dt><dd>{{ money(model.upsideSettlement) }}</dd></div>
          <div><dt>Model premium</dt><dd>{{ money(model.premium) }}</dd></div>
          <div><dt>Breakeven</dt><dd>{{ money(model.breakeven) }}</dd></div>
          <div><dt>Sample move</dt><dd :class="model.spotChangePercent >= 0 ? 'is-pos' : 'is-neg'">{{ signed(model.spotChangePercent) }}</dd></div>
          <div><dt>Cap</dt><dd>+{{ cap }}%</dd></div>
        </dl>
      </section>

      <!-- sample tape: full-bleed rail -->
      <section class="bl-tile bl-span-12 bl-tape">
        <div class="bl-tile-head">
          <h2 id="tape-title" class="bl-h2">Sample tape</h2>
          <p class="bl-meta">Not a feed</p>
        </div>
        <ul class="bl-tape-rail">
          <li v-for="item in tape" :key="item.symbol">
            <button type="button" :aria-pressed="item.symbol === selected"
                    :class="{ 'is-live': item.symbol === selected }" @click="selected = item.symbol">
              <b>{{ item.symbol }}</b>
              <em>{{ spot(item.spot) }}</em>
              <i :class="item.change >= 0 ? 'is-pos' : 'is-neg'">{{ pct(item.change) }}</i>
              <small>K {{ money(item.model.strike) }}</small>
            </button>
          </li>
        </ul>
      </section>

      <!-- briefing: head + four small tiles -->
      <section class="bl-tile bl-tile--plain bl-span-12 bl-brief-head">
        <h2 id="brief-title" class="bl-h2">Briefing</h2>
        <p class="bl-meta">Four leaves</p>
      </section>

      <section v-for="[num, title, body, to] in briefing" :key="num" class="bl-tile bl-span-3 bl-brief">
        <a class="bl-brief-link" :href="to" @click.prevent="to.startsWith('#') ? toBoundary() : emit('navigate', to)">
          <b class="bl-brief-num">{{ num }}</b>
          <span class="bl-brief-body">
            <strong>{{ title }}</strong>
            <em>{{ body }}</em>
          </span>
          <ArrowRight :size="16" aria-hidden="true" class="bl-brief-arrow" />
        </a>
      </section>

      <!-- limits: the accent band -->
      <section class="bl-tile bl-tile--accent bl-span-12 bl-limits">
        <div class="bl-limits-copy">
          <h2 id="disc-title" class="bl-h2">Limits of this preview</h2>
        </div>
        <ul class="bl-limits-list">
          <li>Quotes are illustrative samples, not a market feed.</li>
          <li>The payoff model uses values you enter.</li>
          <li>Journal records stay in this browser's storage.</li>
          <li>No custody, no signing, no trade execution.</li>
          <li>No contract address is published or implied.</li>
        </ul>
        <button class="bl-btn bl-limits-cta" type="button" @click="emit('navigate', '/risk')">Read the limits</button>
      </section>
    </div>
  </div>
</template>

<style scoped>
.bl-home { gap: var(--bl-gap); }

/* ------------------------------------------------------------------ opening */
.bl-home-open { gap: 22px; align-content: space-between; }
.bl-home-open-copy { display: grid; gap: 16px; align-content: start; }
.bl-home-title { font-size: clamp(38px, 4.8vw, 62px); }
.bl-home-open-act { display: flex; flex-wrap: wrap; gap: 10px; }
.bl-home-brief { gap: 12px; }
.bl-home-brief .bl-lead { max-width: 42ch; }

/* -------------------------------------------------------------------- gauge */
.bl-home-gauge { padding-block: clamp(12px, 1.4vw, 18px); }
.bl-gauge { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 4px; }
.bl-gauge > div { display: grid; gap: 4px; padding-inline: 14px; border-inline-start: 1px solid var(--bl-line-2); }
.bl-gauge > div:first-child { border-inline-start: 0; padding-inline-start: 0; }
.bl-gauge dt {
  color: var(--bl-muted);
  font: 600 9.5px/1.4 var(--bl-font-mono);
  letter-spacing: .1em;
  text-transform: uppercase;
}
.bl-gauge dd {
  color: var(--bl-ink);
  font: var(--bl-display-weight) clamp(18px, 1.7vw, 24px)/1.1 var(--bl-font-display);
  letter-spacing: -.02em;
  font-variant-numeric: tabular-nums;
}

/* -------------------------------------------------------------------- board */
.bl-board { gap: 14px; }
.bl-board-head { align-items: flex-start; }
.bl-board-tools { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.bl-search { display: block; min-width: 190px; }
.bl-search .bl-input { min-height: 36px; padding-block: 6px; font-size: 13px; }
.bl-board-grid { min-width: 560px; }
.bl-token {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0;
  border: 0;
  background: none;
  text-align: start;
}
.bl-token-mark {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 11px;
  background: var(--bl-surface-2);
  color: var(--bl-ink-soft);
  font: 600 11px/1 var(--bl-font-mono);
}
.bl-token-mark.is-live { background: var(--bl-accent-safe); color: #fff; }
.bl-token-name { display: grid; gap: 1px; }
.bl-token-name b { font: 600 12.5px/1.3 var(--bl-font-mono); letter-spacing: .03em; }
.bl-token-name small { color: var(--bl-muted); font: 400 11.5px/1.3 var(--bl-font-body); }
.bl-rowlink {
  border: 0;
  border-block-end: 1px solid rgba(194, 0, 93, .38);
  padding: 0 0 2px;
  background: none;
  color: var(--bl-accent-safe);
  font: 600 10.5px/1.4 var(--bl-font-mono);
  letter-spacing: .06em;
  text-decoration: none;
  text-transform: uppercase;
}
.bl-rowlink:hover { border-block-end-color: var(--bl-accent); }
.bl-empty { padding-block: 22px; color: var(--bl-muted); font: 400 13px/1.7 var(--bl-font-body); }
.bl-empty .bl-rowlink { margin-inline-start: 10px; }
.bl-board-note { padding-block-start: 2px; }

/* -------------------------------------------------------------------- quote */
.bl-quote { gap: 14px; align-content: start; }
.bl-quote-head { align-items: center; }
.bl-quote .bl-note { margin-block-start: -4px; }
.bl-quote-form { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 13px; }
.bl-quote-form > .bl-btn { grid-column: 1 / -1; }
.bl-combo { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 9px; }
.bl-combo b { color: var(--bl-muted); font: 600 11px/1 var(--bl-font-mono); letter-spacing: .06em; }
.bl-quote-total {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block-start: 12px;
  border-block-start: 2px solid var(--bl-ink);
}
.bl-quote-total span {
  color: var(--bl-muted);
  font: 600 9.5px/1.4 var(--bl-font-mono);
  letter-spacing: .12em;
  text-transform: uppercase;
}
.bl-quote-total strong {
  color: var(--bl-ink);
  font: var(--bl-display-weight) 25px/1 var(--bl-font-display);
  letter-spacing: -.03em;
  font-variant-numeric: tabular-nums;
}

/* -------------------------------------------------------------------- split */
.bl-split { gap: 14px; }
.bl-split-figure {
  background-image:
    radial-gradient(360px 200px at 100% 0%, rgba(230, 0, 111, .08), transparent 70%),
    linear-gradient(90deg, rgba(23, 11, 18, .035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(23, 11, 18, .035) 1px, transparent 1px);
  background-size: auto, 34px 34px, 34px 34px;
}
.bl-split-grid line { stroke: var(--bl-line-2); stroke-width: 1; }
.bl-band-a { fill: rgba(194, 0, 93, .14); }
.bl-band-b { fill: rgba(230, 0, 111, .4); }
.bl-axis { stroke: var(--bl-line-2); stroke-width: 1.5; }
.bl-cap { stroke: var(--bl-accent-safe); stroke-width: 2.5; stroke-dasharray: 6 5; }
.bl-cap-label { fill: var(--bl-accent-deep); font: 600 11px/1 var(--bl-font-mono); }
.bl-band-label { fill: var(--bl-ink); font: 600 12px/1 var(--bl-font-mono); letter-spacing: .12em; }
.bl-value { fill: var(--bl-ink-soft); font: 500 13px/1 var(--bl-font-mono); }
.bl-tick { fill: var(--bl-muted); font: 400 10px/1 var(--bl-font-mono); }
.bl-split-read .bl-rows > div { padding-block: 10px; }

/* --------------------------------------------------------------------- tape */
.bl-tape { gap: 12px; }
.bl-tape-rail { display: flex; gap: 9px; overflow-x: auto; padding-block-end: 4px; scrollbar-width: thin; }
.bl-tape-rail li { flex: 0 0 auto; }
.bl-tape-rail button {
  display: grid;
  grid-template-columns: auto minmax(64px, auto) auto;
  align-items: baseline;
  gap: 3px 12px;
  min-width: 176px;
  padding: 12px 15px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-surface);
  text-align: start;
  transition: border-color var(--bl-dur) var(--bl-ease), background-color var(--bl-dur) var(--bl-ease);
}
.bl-tape-rail button:hover { border-color: var(--bl-accent); background: var(--bl-tint); }
.bl-tape-rail button.is-live { border-color: var(--bl-accent); background: var(--bl-tint); }
.bl-tape-rail b { color: var(--bl-ink); font: 600 12.5px/1.3 var(--bl-font-mono); letter-spacing: .04em; }
.bl-tape-rail em { color: var(--bl-ink-soft); font: 500 12px/1.3 var(--bl-font-mono); font-style: normal; text-align: end; }
.bl-tape-rail i { font: 500 11px/1.3 var(--bl-font-mono); font-style: normal; text-align: end; }
.bl-tape-rail small { grid-column: 1 / -1; color: var(--bl-muted); font: 400 10px/1.4 var(--bl-font-mono); }

/* ------------------------------------------------------------------- brief */
.bl-brief-head { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; flex-wrap: wrap; padding-block: 6px 0; }
.bl-brief { padding: 0; overflow: hidden; }
.bl-brief-link {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-content: space-between;
  gap: 18px;
  height: 100%;
  padding: var(--bl-tile-pad);
  color: inherit;
  text-decoration: none;
  transition: background-color var(--bl-dur) var(--bl-ease);
}
.bl-brief-link:hover { background: var(--bl-tint); }
.bl-brief-num {
  grid-column: 1 / -1;
  color: var(--bl-accent-safe);
  font: 600 11px/1.4 var(--bl-font-mono);
  letter-spacing: .14em;
}
.bl-brief-body { display: grid; gap: 5px; align-content: start; }
.bl-brief-body strong {
  font: var(--bl-display-weight) 17px/1.3 var(--bl-font-display);
  letter-spacing: -.02em;
}
.bl-brief-body em { color: var(--bl-muted); font: 400 12.5px/1.6 var(--bl-font-body); font-style: normal; }
.bl-brief-arrow { color: var(--bl-accent); align-self: end; }

/* ------------------------------------------------------------------ limits */
.bl-limits {
  display: grid;
  grid-template-columns: minmax(0, 4fr) minmax(0, 7fr) auto;
  gap: 18px clamp(18px, 2.4vw, 34px);
  align-items: center;
}
.bl-limits .bl-h2 { color: #fff; }
.bl-limits-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 20px; }
.bl-limits-list li {
  position: relative;
  padding-inline-start: 18px;
  color: rgba(255, 255, 255, .94);
  font: 400 13px/1.6 var(--bl-font-body);
}
.bl-limits-list li::before {
  content: "";
  position: absolute;
  inset-inline-start: 0;
  inset-block-start: .58em;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255, 255, 255, .8);
}
.bl-limits-cta {
  border-color: transparent;
  background: #fff;
  color: var(--bl-accent-deep);
  white-space: nowrap;
}
.bl-limits-cta:hover { border-color: transparent; background: var(--bl-tint-2); color: var(--bl-accent-deep); }

/* -------------------------------------------------------------- responsive */
@media (max-width: 1200px) {
  .bl-gauge { grid-template-columns: repeat(3, minmax(0, 1fr)); row-gap: 12px; }
  .bl-gauge > div:nth-child(4) { border-inline-start: 0; padding-inline-start: 0; }
  .bl-limits { grid-template-columns: minmax(0, 1fr); }
  .bl-limits-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .bl-limits-cta { justify-self: start; }
}
@media (max-width: 900px) {
  .bl-quote-form { grid-template-columns: minmax(0, 1fr); }
  .bl-limits-list { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 820px) {
  .bl-board-grid { min-width: 0; }
  .bl-board-grid thead th, .bl-board-grid tbody th, .bl-board-grid tbody td { padding-inline: 7px; }
  .bl-board-grid thead th { font-size: 8.5px; letter-spacing: .04em; }
  .bl-board-grid .bl-token { gap: 8px; }
  .bl-board-grid .bl-token-mark { width: 26px; height: 26px; border-radius: 9px; }
  .bl-board-grid .bl-token-name b { font-size: 11.5px; }
  .bl-board-grid .bl-token-name small { font-size: 10px; }
}
@media (max-width: 620px) {
  .bl-gauge { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .bl-gauge > div { border-inline-start: 0; padding-inline: 0; }
  .bl-search { width: 100%; }
  .bl-board-tools { width: 100%; }
  .bl-board-tools .bl-switch { flex: 1 1 auto; }
  .bl-board-tools .bl-switch button { flex: 1 1 auto; }
  .bl-quote { padding: 16px; }
}
</style>
