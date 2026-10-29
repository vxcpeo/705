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
    <section class="bp-band bp-band--first gr-open">
      <div class="gr-open-copy">
        <p class="bp-kicker">{{ brand.network }} / paper market</p>
        <h1 class="bp-display gr-display" tabindex="-1">{{ pageTitle }}</h1>
        <p class="bp-lead">{{ copy }}</p>
      </div>
      <a class="bp-btn bp-btn--ghost gr-back" href="/" @click.prevent="emit('navigate','/')"><ArrowLeft :size="15" /> Markets</a>
    </section>

    <!-- asset detail -->
    <section v-if="symbol" class="bp-band gr-detail">
      <div class="gr-detail-head">
        <h2 class="bp-h2">{{ symbol }} / {{ brand.network }}</h2>
        <p class="bp-meta">30-day epoch | +5% cap | illustrative values</p>
      </div>
      <div class="gr-detail-grid">
        <div class="gr-passport">
          <div class="gr-spec-top">
            <span class="gr-mark" aria-hidden="true">{{ symbol.slice(0, 1) }}</span>
            <span class="gr-spec-name"><b>{{ symbol }}</b><small>Example series</small></span>
            <span class="bp-pill bp-pill--bp-cobalt"><i aria-hidden="true"></i>Paper only</span>
          </div>
          <dl class="gr-spec-rows">
            <div><dt>Reference</dt><dd>{{ symbol === 'SOL' ? '$182.00' : symbol === 'JUP' ? '$1.12' : symbol === 'BONK' ? '$0.000021' : '$1.00' }}</dd></div>
            <div><dt>Income model</dt><dd class="gr-inc">+5% cap</dd></div>
            <div><dt>Settlement</dt><dd>Not live</dd></div>
          </dl>
          <p class="bp-note">Illustrative values. No live quote, custody, signing or execution.</p>
        </div>
        <div class="gr-detail-figure">
          <PayoffExplorer :spot="symbol === 'SOL' ? 182 : symbol === 'JUP' ? 1.12 : symbol === 'BONK' ? 0.000021 : 1" :asset="symbol" />
        </div>
      </div>
    </section>

    <!-- launchpad leaf -->
    <section v-else-if="pageTitle === 'Launchpad'" class="bp-band gr-leaf">
      <div class="gr-leaf-sheet">
        <div class="gr-leaf-head">
          <h2 class="bp-h2">Suggest a market.</h2>
          <span class="bp-pill"><i aria-hidden="true"></i>Listing intake</span>
        </div>
        <span class="gr-leaf-mark"><WalletCards :size="20" /></span>
        <p class="gr-leaf-copy">Any SPL market unit with a verified price feed and USDC liquidity path may qualify. This preview records no wallet request or listing transaction.</p>
        <a class="bp-btn bp-btn--primary" href="/docs#listing" @click.prevent="emit('navigate','/docs#listing')">Read listing notes <ArrowUpRight :size="15" /></a>
      </div>
    </section>

    <!-- recompose leaf -->
    <section v-else-if="pageTitle === 'Recompose'" class="bp-band gr-leaf">
      <div class="gr-leaf-sheet">
        <div class="gr-leaf-head">
          <h2 class="bp-h2">One asset again.</h2>
          <span class="bp-pill"><i aria-hidden="true"></i>Income + Upside</span>
        </div>
        <span class="gr-leaf-mark"><TrendingUp :size="20" /></span>
        <p class="gr-leaf-copy">Recomposition would require a wallet transaction. The local preview keeps this action visible while execution remains unavailable.</p>
        <button class="bp-btn" type="button" disabled>Recompose unavailable</button>
      </div>
    </section>

    <!-- board -->
    <section v-else class="bp-band gr-board">
      <div class="gr-tools">
        <label class="gr-search">
          <Search :size="15" />
          <span class="visually-hidden">Search markets</span>
          <input v-model="query" class="bp-input" type="search" placeholder="Search token or market" />
        </label>
        <div class="bp-switch gr-side" aria-label="Position type">
          <button v-for="option in ['All','Income','Upside']" :key="option" type="button" :aria-pressed="side === option" :class="{ 'is-on': side === option }" @click="side = option">{{ option }}</button>
        </div>
        <button class="bp-btn bp-btn--quiet gr-filter-toggle" type="button" :aria-expanded="showFilters" @click="showFilters = !showFilters"><SlidersHorizontal :size="15" /> Details</button>
      </div>
      <p v-if="showFilters" class="bp-notice bp-notice--flag gr-filter-details">All examples use a +5% cap, 30-day epoch and 25% model volatility.</p>

      <div class="gr-deck">
        <div class="gr-main">
          <MarketTable :query="query" :side="side" @reset="query = ''" @navigate="to => emit('navigate',to)" />
        </div>
        <div class="gr-rail" role="complementary" aria-label="Market facts">
          <dl class="gr-facts">
            <div><dt>Sheet</dt><dd>{{ pageTitle }}</dd><dd>{{ brand.network }} preview</dd></div>
            <div><dt>Cap default</dt><dd>+5%</dd><dd>30-day epoch</dd></div>
            <div><dt>Feed</dt><dd>Static</dd><dd>Not a live quote</dd></div>
            <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd><dd>Proposed, unissued</dd></div>
          </dl>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ---------------------------------------------------------------- opening */
.shoal { display: grid; grid-template-columns: minmax(0, 1fr); }
.shoal > * { min-width: 0; }
.gr-open {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  padding-block-end: clamp(22px, 3vw, 34px);
}
.gr-open-copy { display: grid; gap: 10px; max-width: 46ch; }
.gr-display { font-size: clamp(34px, 5vw, 58px); margin-block-start: 4px; }
.gr-open-copy .bp-lead { margin-block-start: 0; }
.gr-back { flex: none; }

/* ----------------------------------------------------------------- detail */
.gr-detail-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-block-end: clamp(16px, 2vw, 24px);
}
.gr-detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(18px, 2.4vw, 30px);
  align-items: start;
}
.gr-passport {
  max-width: 520px;
  display: grid;
  gap: 16px;
  padding: clamp(16px, 2vw, 22px);
  border: 1px solid var(--bp-line);
  border-radius: var(--bp-r-md);
  background: linear-gradient(170deg, var(--bp-paper), var(--bp-paper-3));
  box-shadow: var(--bp-shadow-soft);
}
.gr-spec-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.gr-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 46px;
  height: 46px;
  border-radius: 15px;
  background: var(--bp-cobalt-safe);
  color: #fff;
  font: 600 16px/1 var(--bp-font-mono);
  box-shadow: 0 10px 24px rgba(0, 0, 204, .28);
}
.gr-spec-name { display: grid; gap: 2px; margin-inline-end: auto; }
.gr-spec-name b { font: 600 22px/1.1 var(--bp-font-display); letter-spacing: -.02em; }
.gr-spec-name small { color: var(--bp-muted); font: 500 10px/1.4 var(--bp-font-mono); letter-spacing: .12em; text-transform: uppercase; }
.gr-spec-rows { display: grid; }
.gr-spec-rows > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding-block: 11px;
  border-block-end: 1px solid var(--bp-line);
}
.gr-spec-rows dt { color: var(--bp-muted); font: 500 10px/1.5 var(--bp-font-mono); letter-spacing: .1em; text-transform: uppercase; }
.gr-spec-rows dd { font: 600 13px/1.5 var(--bp-font-mono); }
.gr-spec-rows dd.gr-inc { color: var(--bp-success); }
.gr-detail-figure { min-width: 0; }

/* ------------------------------------------------------------------- leaf */
.gr-leaf-sheet {
  display: grid;
  gap: 16px;
  justify-items: start;
  max-width: 720px;
  padding: clamp(20px, 3vw, 34px);
  border: 1px solid var(--bp-line);
  border-radius: var(--bp-r-lg);
  background:
    radial-gradient(480px 240px at 100% 0%, rgba(0, 0, 255, .14), transparent 70%),
    var(--bp-paper);
  box-shadow: var(--bp-shadow);
}
.gr-leaf-head { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; width: 100%; }
.gr-leaf-mark {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: var(--bp-paper-2);
  color: var(--bp-cobalt-deep);
  box-shadow: inset 0 0 0 1px var(--bp-line);
}
.gr-leaf-copy { max-width: 60ch; color: var(--bp-ink-2); font: 400 14px/1.7 var(--bp-font-body); }

/* ------------------------------------------------------------------ board */
.gr-tools {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-block-end: 16px;
}
.gr-search {
  display: flex;
  align-items: center;
  gap: 9px;
  flex: 1 1 260px;
  max-width: 400px;
  color: var(--bp-muted);
}
.gr-search .bp-input { min-height: 42px; font-family: var(--bp-font-body); font-size: 13px; }
.gr-side { flex: none; }
.gr-filter-toggle { margin-inline-start: auto; }
.gr-filter-details { margin-block-end: 18px; }

.gr-deck {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(14px, 2vw, 20px);
  align-items: start;
}
.gr-main { min-width: 0; }
.gr-rail {
  order: -1;
  border: 1px solid var(--bp-line);
  border-radius: var(--bp-r-md);
  background: var(--bp-paper-3);
  overflow: hidden;
}
.gr-facts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
.gr-facts > div {
  display: grid;
  gap: 4px;
  padding: 14px 16px;
  border-inline-end: 1px solid var(--bp-line);
}
.gr-facts > div:last-child { border-inline-end: 0; }
.gr-facts dt { color: var(--bp-muted); font: 600 9px/1.4 var(--bp-font-mono); letter-spacing: .12em; text-transform: uppercase; }
.gr-facts dd { color: var(--bp-ink); font: 600 15px/1.35 var(--bp-font-display); letter-spacing: -.01em; }
.gr-facts dd + dd { color: var(--bp-muted); font: 400 10px/1.5 var(--bp-font-mono); }

/* -------------------------------------------------------------- responsive */
@media (max-width: 1180px) {
  .gr-facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .gr-facts > div:nth-child(odd) { border-inline-end: 1px solid var(--bp-line); }
  .gr-facts > div:nth-child(-n+2) { border-block-end: 1px solid var(--bp-line); }
}
@media (max-width: 760px) {
  .gr-search { max-width: none; flex: 1 1 100%; }
  .gr-filter-toggle { margin-inline-start: 0; }
  .gr-facts { grid-template-columns: minmax(0, 1fr); }
  .gr-facts > div:nth-child(odd) { border-inline-end: 0; }
}
</style>
