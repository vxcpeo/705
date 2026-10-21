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
  <div class="shoal">
    <!-- opening band -->
    <section class="tide-band tide-band--first shoal-open">
      <div class="shoal-open-copy">
        <p class="tide-kicker">{{ brand.network }} / paper market</p>
        <h1 class="tide-display shoal-display" tabindex="-1">{{ pageTitle }}</h1>
        <p class="tide-lead">{{ copy }}</p>
      </div>
      <a class="tide-btn tide-btn--ghost shoal-back" href="/" @click.prevent="emit('navigate','/')"><ArrowLeft :size="15" /> Markets</a>
    </section>

    <!-- asset detail -->
    <section v-if="symbol" class="tide-band shoal-detail">
      <div class="shoal-detail-head">
        <h2 class="tide-h2">{{ symbol }} / {{ brand.network }}</h2>
        <p class="tide-meta">30-day epoch | +5% cap | illustrative values</p>
      </div>
      <div class="shoal-detail-grid">
        <div class="shoal-passport">
          <div class="shoal-spec-top">
            <span class="shoal-mark" aria-hidden="true">{{ symbol.slice(0, 1) }}</span>
            <span class="shoal-spec-name"><b>{{ symbol }}</b><small>Example series</small></span>
            <span class="tide-pill tide-pill--accent"><i aria-hidden="true"></i>Paper only</span>
          </div>
          <dl class="shoal-spec-rows">
            <div><dt>Reference</dt><dd>{{ symbol === 'SOL' ? '$182.00' : symbol === 'JUP' ? '$1.12' : symbol === 'BONK' ? '$0.000021' : '$1.00' }}</dd></div>
            <div><dt>Income model</dt><dd class="shoal-inc">+5% cap</dd></div>
            <div><dt>Settlement</dt><dd>Not live</dd></div>
          </dl>
          <p class="tide-note">Illustrative values. No live quote, custody, signing or execution.</p>
        </div>
        <div class="shoal-detail-figure">
          <PayoffExplorer :spot="symbol === 'SOL' ? 182 : symbol === 'JUP' ? 1.12 : symbol === 'BONK' ? 0.000021 : 1" :asset="symbol" />
        </div>
      </div>
    </section>

    <!-- launchpad leaf -->
    <section v-else-if="pageTitle === 'Launchpad'" class="tide-band shoal-leaf">
      <div class="shoal-leaf-sheet">
        <div class="shoal-leaf-head">
          <h2 class="tide-h2">Suggest a market.</h2>
          <span class="tide-pill"><i aria-hidden="true"></i>Listing intake</span>
        </div>
        <span class="shoal-leaf-mark"><WalletCards :size="20" /></span>
        <p class="shoal-leaf-copy">Any SPL market unit with a verified price feed and USDC liquidity path may qualify. This preview records no wallet request or listing transaction.</p>
        <a class="tide-btn tide-btn--primary" href="/docs#listing" @click.prevent="emit('navigate','/docs#listing')">Read listing notes <ArrowUpRight :size="15" /></a>
      </div>
    </section>

    <!-- recompose leaf -->
    <section v-else-if="pageTitle === 'Recompose'" class="tide-band shoal-leaf">
      <div class="shoal-leaf-sheet">
        <div class="shoal-leaf-head">
          <h2 class="tide-h2">One asset again.</h2>
          <span class="tide-pill"><i aria-hidden="true"></i>Income + Upside</span>
        </div>
        <span class="shoal-leaf-mark"><TrendingUp :size="20" /></span>
        <p class="shoal-leaf-copy">Recomposition would require a wallet transaction. The local preview keeps this action visible while execution remains unavailable.</p>
        <button class="tide-btn" type="button" disabled>Recompose unavailable</button>
      </div>
    </section>

    <!-- board -->
    <section v-else class="tide-band shoal-board">
      <div class="shoal-tools">
        <label class="shoal-search">
          <Search :size="15" />
          <span class="visually-hidden">Search markets</span>
          <input v-model="query" class="tide-input" type="search" placeholder="Search token or market" />
        </label>
        <div class="tide-switch shoal-side" aria-label="Position type">
          <button v-for="option in ['All','Income','Upside']" :key="option" type="button" :aria-pressed="side === option" :class="{ 'is-on': side === option }" @click="side = option">{{ option }}</button>
        </div>
        <button class="tide-btn tide-btn--quiet shoal-filter-toggle" type="button" :aria-expanded="showFilters" @click="showFilters = !showFilters"><SlidersHorizontal :size="15" /> Details</button>
      </div>
      <p v-if="showFilters" class="tide-notice tide-notice--flag shoal-filter-details">All examples use a +5% cap, 30-day epoch and 25% model volatility.</p>

      <div class="shoal-deck">
        <div class="shoal-main">
          <MarketTable :query="query" :side="side" @reset="query = ''" @navigate="to => emit('navigate',to)" />
        </div>
        <aside class="shoal-rail" aria-label="Market facts">
          <dl class="shoal-facts">
            <div><dt>Sheet</dt><dd>{{ pageTitle }}</dd><dd>{{ brand.network }} preview</dd></div>
            <div><dt>Cap default</dt><dd>+5%</dd><dd>30-day epoch</dd></div>
            <div><dt>Feed</dt><dd>Static</dd><dd>Not a live quote</dd></div>
            <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd><dd>Proposed, unissued</dd></div>
          </dl>
        </aside>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ---------------------------------------------------------------- opening */
.shoal { display: grid; grid-template-columns: minmax(0, 1fr); }
.shoal > * { min-width: 0; }
.shoal-open {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  padding-block-end: clamp(22px, 3vw, 34px);
}
.shoal-open-copy { display: grid; gap: 10px; max-width: 46ch; }
.shoal-display { font-size: clamp(34px, 5vw, 58px); margin-block-start: 4px; }
.shoal-open-copy .tide-lead { margin-block-start: 0; }
.shoal-back { flex: none; }

/* ----------------------------------------------------------------- detail */
.shoal-detail-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-block-end: clamp(16px, 2vw, 24px);
}
.shoal-detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(18px, 2.4vw, 30px);
  align-items: start;
}
.shoal-passport {
  max-width: 520px;
  display: grid;
  gap: 16px;
  padding: clamp(16px, 2vw, 22px);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: linear-gradient(170deg, var(--surface), var(--surface-soft));
  box-shadow: var(--shadow-soft);
}
.shoal-spec-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.shoal-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 46px;
  height: 46px;
  border-radius: 15px;
  background: var(--accent-safe);
  color: #fff;
  font: 600 16px/1 var(--font-mono);
  box-shadow: 0 10px 24px rgba(13, 113, 227, .28);
}
.shoal-spec-name { display: grid; gap: 2px; margin-inline-end: auto; }
.shoal-spec-name b { font: 600 22px/1.1 var(--font-display); letter-spacing: -.02em; }
.shoal-spec-name small { color: var(--muted); font: 500 10px/1.4 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; }
.shoal-spec-rows { display: grid; }
.shoal-spec-rows > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding-block: 11px;
  border-block-end: 1px solid var(--line);
}
.shoal-spec-rows dt { color: var(--muted); font: 500 10px/1.5 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; }
.shoal-spec-rows dd { font: 600 13px/1.5 var(--font-mono); }
.shoal-spec-rows dd.shoal-inc { color: var(--success); }
.shoal-detail-figure { min-width: 0; }

/* ------------------------------------------------------------------- leaf */
.shoal-leaf-sheet {
  display: grid;
  gap: 16px;
  justify-items: start;
  max-width: 720px;
  padding: clamp(20px, 3vw, 34px);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  background:
    radial-gradient(480px 240px at 100% 0%, rgba(41, 141, 255, .14), transparent 70%),
    var(--surface);
  box-shadow: var(--shadow);
}
.shoal-leaf-head { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; width: 100%; }
.shoal-leaf-mark {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: var(--surface-alt);
  color: var(--accent-deep);
  box-shadow: inset 0 0 0 1px var(--line);
}
.shoal-leaf-copy { max-width: 60ch; color: var(--ink-soft); font: 400 14px/1.7 var(--font-body); }

/* ------------------------------------------------------------------ board */
.shoal-tools {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-block-end: 16px;
}
.shoal-search {
  display: flex;
  align-items: center;
  gap: 9px;
  flex: 1 1 260px;
  max-width: 400px;
  color: var(--muted);
}
.shoal-search .tide-input { min-height: 42px; font-family: var(--font-body); font-size: 13px; }
.shoal-side { flex: none; }
.shoal-filter-toggle { margin-inline-start: auto; }
.shoal-filter-details { margin-block-end: 18px; }

.shoal-deck {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(14px, 2vw, 20px);
  align-items: start;
}
.shoal-main { min-width: 0; }
.shoal-rail {
  order: -1;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface-soft);
  overflow: hidden;
}
.shoal-facts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
.shoal-facts > div {
  display: grid;
  gap: 4px;
  padding: 14px 16px;
  border-inline-end: 1px solid var(--line);
}
.shoal-facts > div:last-child { border-inline-end: 0; }
.shoal-facts dt { color: var(--muted); font: 600 9px/1.4 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; }
.shoal-facts dd { color: var(--ink); font: 600 15px/1.35 var(--font-display); letter-spacing: -.01em; }
.shoal-facts dd + dd { color: var(--muted); font: 400 10px/1.5 var(--font-mono); }

/* -------------------------------------------------------------- responsive */
@media (max-width: 1180px) {
  .shoal-facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .shoal-facts > div:nth-child(odd) { border-inline-end: 1px solid var(--line); }
  .shoal-facts > div:nth-child(-n+2) { border-block-end: 1px solid var(--line); }
}
@media (max-width: 760px) {
  .shoal-search { max-width: none; flex: 1 1 100%; }
  .shoal-filter-toggle { margin-inline-start: 0; }
  .shoal-facts { grid-template-columns: minmax(0, 1fr); }
  .shoal-facts > div:nth-child(odd) { border-inline-end: 0; }
}
</style>
