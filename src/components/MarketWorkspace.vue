<script setup>
import { ArrowLeft, ArrowUpRight, Search, SlidersHorizontal, TrendingUp, WalletCards } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import MarketTable from './MarketTable.vue'
import PayoffExplorer from './PayoffExplorer.vue'
import { brand } from '../brand.js'

const props = defineProps({ path: { type: String, default: '/app/markets' } })
const emit = defineEmits(['navigate'])
const query = ref('')
const side = ref('All')
const showFilters = ref(false)
const symbols = ['SOL', 'JUP', 'BONK', 'USDC']
const symbol = computed(() => {
  const match = props.path.match(/\/app\/markets\/([^/]+)/i)
  return match && symbols.includes(match[1].toUpperCase()) ? match[1].toUpperCase() : ''
})
const pageTitle = computed(() => props.path.includes('launchpad') ? 'Launchpad' : props.path.includes('auctions') ? 'Auctions' : props.path.includes('recompose') ? 'Recompose' : symbol.value ? `${symbol.value} market` : 'Markets')
const copy = computed(() => ({ Markets: 'Scan defined-cap series and compare the two sides of each market.', Launchpad: 'Record a candidate market for a future verified listing.', Auctions: 'Review the sample Upside auction surface without placing an order.', Recompose: 'Pair Income and Upside positions back into one market unit.' }[pageTitle.value] || 'Read the illustrative settlement path for this asset.'))
</script>

<template>
  <div class="bl-page bl-mkt">
    <div class="bl-bento">
      <!-- anchor tile: page identity -->
      <section class="bl-tile bl-tile--tint bl-span-7 bl-mkt-open">
        <div class="bl-mkt-open-copy">
          <p class="bl-kicker">{{ brand.network }} / paper market</p>
          <h1 class="bl-display bl-mkt-title" tabindex="-1">{{ pageTitle }}</h1>
          <p class="bl-lead">{{ copy }}</p>
        </div>
        <a class="bl-btn bl-mkt-back" href="/" @click.prevent="emit('navigate','/')"><ArrowLeft :size="15" /> Markets</a>
      </section>

      <!-- series passport -->
      <section v-if="symbol" class="bl-tile bl-tile--plum bl-span-5 bl-mkt-passport">
        <div class="bl-tile-head">
          <h2 class="bl-h2">{{ symbol }} / {{ brand.network }}</h2>
          <p class="bl-meta">30-day epoch | +5% cap | illustrative values</p>
        </div>
        <div class="bl-spec-top">
          <span class="bl-mark" aria-hidden="true">{{ symbol.slice(0, 1) }}</span>
          <span class="bl-spec-name"><b>{{ symbol }}</b><small>Example series</small></span>
          <span class="bl-chip"><i aria-hidden="true"></i>Paper only</span>
        </div>
        <dl class="bl-spec-rows">
          <div><dt>Reference</dt><dd>{{ symbol === 'SOL' ? '$182.00' : symbol === 'JUP' ? '$1.12' : symbol === 'BONK' ? '$0.000021' : '$1.00' }}</dd></div>
          <div><dt>Income model</dt><dd class="bl-inc">+5% cap</dd></div>
          <div><dt>Settlement</dt><dd>Not live</dd></div>
        </dl>
        <p class="bl-note">Illustrative values. No live quote, custody, signing or execution.</p>
      </section>

      <!-- launchpad intake -->
      <section v-else-if="pageTitle === 'Launchpad'" class="bl-tile bl-span-5 bl-mkt-leaf">
        <div class="bl-tile-head">
          <span class="bl-chip bl-chip--accent"><i aria-hidden="true"></i>Listing intake</span>
          <span class="bl-leaf-mark"><WalletCards :size="20" /></span>
        </div>
        <h2 class="bl-h2">Suggest a market.</h2>
        <p class="bl-mkt-leaf-copy">Any SPL market unit with a verified price feed and USDC liquidity path may qualify. This preview records no wallet request or listing transaction.</p>
        <a class="bl-btn bl-btn--primary" href="/docs#listing" @click.prevent="emit('navigate','/docs#listing')">Read listing notes <ArrowUpRight :size="15" /></a>
      </section>

      <!-- recompose note -->
      <section v-else-if="pageTitle === 'Recompose'" class="bl-tile bl-span-5 bl-mkt-leaf">
        <div class="bl-tile-head">
          <span class="bl-chip"><i aria-hidden="true"></i>Income + Upside</span>
          <span class="bl-leaf-mark"><TrendingUp :size="20" /></span>
        </div>
        <h2 class="bl-h2">One asset again.</h2>
        <p class="bl-mkt-leaf-copy">Recomposition would require a wallet transaction. The local preview keeps this action visible while execution remains unavailable.</p>
        <button class="bl-btn" type="button" disabled>Recompose unavailable</button>
      </section>

      <!-- facts, as four small tiles -->
      <section v-if="!symbol && !['Launchpad','Recompose'].includes(pageTitle)" class="bl-span-5 bl-mkt-facts" role="group" aria-label="Market facts">
        <dl class="bl-fact-tiles">
          <div class="bl-fact-tile"><dt>Sheet</dt><dd>{{ pageTitle }}</dd><dd>{{ brand.network }} preview</dd></div>
          <div class="bl-fact-tile"><dt>Cap default</dt><dd>+5%</dd><dd>30-day epoch</dd></div>
          <div class="bl-fact-tile"><dt>Feed</dt><dd>Static</dd><dd>Not a live quote</dd></div>
          <div class="bl-fact-tile"><dt>Unit</dt><dd>{{ brand.asset }}*</dd><dd>Proposed, unissued</dd></div>
        </dl>
      </section>

      <!-- payoff explorer: full band -->
      <div v-if="symbol" class="bl-span-12 bl-mkt-explore">
        <PayoffExplorer :spot="symbol === 'SOL' ? 182 : symbol === 'JUP' ? 1.12 : symbol === 'BONK' ? 0.000021 : 1" :asset="symbol" />
      </div>

      <!-- board: full band -->
      <section v-else-if="!['Launchpad','Recompose'].includes(pageTitle)" class="bl-tile bl-span-12 bl-mkt-board">
        <div class="bl-mkt-tools">
          <label class="bl-search">
            <Search :size="15" />
            <span class="visually-hidden">Search markets</span>
            <input v-model="query" class="bl-input" type="search" placeholder="Search token or market" />
          </label>
          <div class="bl-switch bl-mkt-side" aria-label="Position type">
            <button v-for="option in ['All','Income','Upside']" :key="option" type="button" :aria-pressed="side === option" :class="{ 'is-live': side === option }" @click="side = option">{{ option }}</button>
          </div>
          <button class="bl-btn bl-btn--quiet bl-mkt-filter" type="button" :aria-expanded="showFilters" @click="showFilters = !showFilters"><SlidersHorizontal :size="15" /> Details</button>
        </div>
        <p v-if="showFilters" class="bl-notice bl-notice--flag bl-mkt-details">All examples use a +5% cap, 30-day epoch and 25% model volatility.</p>

        <MarketTable :query="query" :side="side" @reset="query = ''" @navigate="to => emit('navigate',to)" />
      </section>
    </div>
  </div>
</template>

<style scoped>
.bl-mkt { gap: var(--bl-gap); }

/* ------------------------------------------------------------------ opening */
.bl-mkt-open { align-content: space-between; gap: 20px; }
.bl-mkt-open-copy { display: grid; gap: 12px; align-content: start; }
.bl-mkt-title { font-size: clamp(36px, 4.4vw, 56px); }
.bl-mkt-back { justify-self: start; }
.bl-mkt-open .bl-lead { max-width: 46ch; }

/* ---------------------------------------------------------------- passport */
.bl-mkt-passport { gap: 16px; }
.bl-mkt-passport .bl-h2 { color: var(--bl-plum-text); }
.bl-mkt-passport .bl-meta { color: var(--bl-plum-muted); }
.bl-mkt-passport .bl-note { color: var(--bl-plum-muted); }
.bl-spec-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.bl-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 46px;
  height: 46px;
  border-radius: 15px;
  background: linear-gradient(150deg, var(--bl-accent), var(--bl-accent-safe));
  color: #fff;
  font: 600 16px/1 var(--bl-font-mono);
}
.bl-spec-name { display: grid; gap: 2px; margin-inline-end: auto; }
.bl-spec-name b { color: var(--bl-plum-text); font: 600 22px/1.1 var(--bl-font-display); letter-spacing: -.02em; }
.bl-spec-name small {
  color: var(--bl-plum-muted);
  font: 600 9.5px/1.4 var(--bl-font-mono);
  letter-spacing: .1em;
  text-transform: uppercase;
}
.bl-spec-rows { display: grid; }
.bl-spec-rows > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding-block: 10px;
  border-block-end: 1px solid var(--bl-plum-line);
}
.bl-spec-rows > div:last-child { border-block-end: 0; }
.bl-spec-rows dt { color: var(--bl-plum-muted); font: 600 10px/1.5 var(--bl-font-mono); letter-spacing: .08em; text-transform: uppercase; }
.bl-spec-rows dd { color: var(--bl-plum-text); font: 600 13px/1.5 var(--bl-font-mono); }
.bl-spec-rows dd.bl-inc { color: #7fe0b0; }

/* -------------------------------------------------------------------- leaf */
.bl-mkt-leaf { gap: 14px; align-content: start; }
.bl-mkt-leaf .bl-h2 { margin-block-start: 2px; }
.bl-leaf-mark {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: var(--bl-tint);
  color: var(--bl-accent-safe);
}
.bl-mkt-leaf-copy { max-width: 58ch; color: var(--bl-ink-soft); font: 400 14px/1.7 var(--bl-font-body); }

/* ------------------------------------------------------------------- facts */
.bl-fact-tiles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--bl-gap); }
.bl-fact-tile {
  display: grid;
  gap: 4px;
  align-content: start;
  padding: 14px 16px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-md);
  background: var(--bl-surface);
}
.bl-fact-tile dt {
  color: var(--bl-muted);
  font: 600 9.5px/1.4 var(--bl-font-mono);
  letter-spacing: .12em;
  text-transform: uppercase;
}
.bl-fact-tile dd { color: var(--bl-ink); font: var(--bl-display-weight) 15px/1.35 var(--bl-font-display); letter-spacing: -.01em; }
.bl-fact-tile dd + dd { color: var(--bl-muted); font: 400 10.5px/1.5 var(--bl-font-mono); }

/* ------------------------------------------------------------------- board */
.bl-mkt-board { gap: 16px; }
.bl-mkt-tools { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.bl-search {
  display: flex;
  align-items: center;
  gap: 9px;
  flex: 1 1 260px;
  max-width: 400px;
  color: var(--bl-muted);
}
.bl-search .bl-input { min-height: 42px; font-size: 13px; }
.bl-mkt-side { flex: none; }
.bl-mkt-filter { margin-inline-start: auto; }
.bl-mkt-details { margin-block-start: -2px; }
.bl-mkt-explore { min-width: 0; }

@media (max-width: 900px) {
  .bl-search { max-width: none; flex: 1 1 100%; }
  .bl-mkt-filter { margin-inline-start: 0; }
}
@media (max-width: 560px) {
  .bl-fact-tiles { grid-template-columns: minmax(0, 1fr); }
}
</style>
