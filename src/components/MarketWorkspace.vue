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
  <div class="quay">
    <!-- opening scene -->
    <section class="atlas-scene quay-open">
      <div class="atlas-scene-in quay-open-in">
        <div class="quay-open-copy">
          <p class="atlas-kicker">{{ brand.network }} / paper market</p>
          <h1 class="atlas-display quay-display" tabindex="-1">{{ pageTitle }}</h1>
          <p class="atlas-lead">{{ copy }}</p>
        </div>
        <a class="atlas-btn atlas-btn--ghost quay-back" href="/" @click.prevent="emit('navigate','/')"><ArrowLeft :size="15" /> Markets</a>
      </div>
    </section>

    <!-- sheet facts -->
    <section class="atlas-scene quay-facts-scene">
      <div class="atlas-scene-in">
        <dl class="atlas-facts quay-facts">
          <div><dt>Sheet</dt><dd>{{ pageTitle }}</dd><dd>{{ brand.network }} preview</dd></div>
          <div><dt>Cap default</dt><dd>+5%</dd><dd>30-day epoch</dd></div>
          <div><dt>Feed</dt><dd>Static</dd><dd>Not a live quote</dd></div>
          <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd><dd>Proposed, unissued</dd></div>
        </dl>
      </div>
    </section>

    <!-- asset detail -->
    <section v-if="symbol" class="atlas-scene quay-detail">
      <div class="atlas-scene-in">
        <div class="quay-detail-head">
          <h2 class="atlas-h2">{{ symbol }} / {{ brand.network }}</h2>
          <p class="atlas-meta">30-day epoch | +5% cap | illustrative values</p>
        </div>
        <div class="quay-detail-grid">
          <div class="atlas-face quay-passport">
            <div class="quay-passport-top">
              <span class="quay-mark" aria-hidden="true">{{ symbol.slice(0, 1) }}</span>
              <span class="quay-passport-name"><b>{{ symbol }}</b><small>Example series</small></span>
              <span class="atlas-pill atlas-pill--beam"><i aria-hidden="true"></i>Paper only</span>
            </div>
            <dl class="atlas-pairs quay-passport-rows">
              <div><dt>Reference</dt><dd>{{ symbol === 'SOL' ? '$182.00' : symbol === 'JUP' ? '$1.12' : symbol === 'BONK' ? '$0.000021' : '$1.00' }}</dd></div>
              <div><dt>Income model</dt><dd class="is-income">+5% cap</dd></div>
              <div><dt>Settlement</dt><dd>Not live</dd></div>
            </dl>
            <p class="atlas-note quay-passport-note">Illustrative values. No live quote, custody, signing or execution.</p>
          </div>
          <div class="quay-detail-figure">
            <PayoffExplorer :spot="symbol === 'SOL' ? 182 : symbol === 'JUP' ? 1.12 : symbol === 'BONK' ? 0.000021 : 1" :asset="symbol" />
          </div>
        </div>
      </div>
    </section>

    <!-- launchpad leaf -->
    <section v-else-if="pageTitle === 'Launchpad'" class="atlas-scene quay-leaf">
      <div class="atlas-scene-in">
        <div class="atlas-face atlas-face--halo quay-leaf-face">
          <div class="atlas-face-head">
            <h2 class="atlas-h2">Suggest a market.</h2>
            <span class="atlas-pill"><i aria-hidden="true"></i>Listing intake</span>
          </div>
          <span class="quay-leaf-mark"><WalletCards :size="19" /></span>
          <p class="quay-leaf-copy">Any SPL market unit with a verified price feed and USDC liquidity path may qualify. This preview records no wallet request or listing transaction.</p>
          <a class="atlas-btn atlas-btn--primary quay-leaf-cta" href="/docs#listing" @click.prevent="emit('navigate','/docs#listing')">Read listing notes <ArrowUpRight :size="15" /></a>
        </div>
      </div>
    </section>

    <!-- recompose leaf -->
    <section v-else-if="pageTitle === 'Recompose'" class="atlas-scene quay-leaf">
      <div class="atlas-scene-in">
        <div class="atlas-face atlas-face--halo quay-leaf-face">
          <div class="atlas-face-head">
            <h2 class="atlas-h2">One asset again.</h2>
            <span class="atlas-pill"><i aria-hidden="true"></i>Income + Upside</span>
          </div>
          <span class="quay-leaf-mark"><TrendingUp :size="19" /></span>
          <p class="quay-leaf-copy">Recomposition would require a wallet transaction. The local preview keeps this action visible while execution remains unavailable.</p>
          <button class="atlas-btn" type="button" disabled>Recompose unavailable</button>
        </div>
      </div>
    </section>

    <!-- board -->
    <template v-else>
      <section class="atlas-scene quay-board">
        <div class="atlas-scene-in">
          <!-- MarketTable renders its own section head ("Market quotes") plus the -->
          <!-- stats band, so the workspace does not repeat a heading here. -->
          <div class="quay-filters">
            <label class="quay-search">
              <Search :size="15" />
              <span class="sr-only">Search markets</span>
              <input v-model="query" class="atlas-input" type="search" placeholder="Search token or market" />
            </label>
            <div class="atlas-switch quay-side" aria-label="Position type">
              <button v-for="option in ['All','Income','Upside']" :key="option" type="button" :aria-pressed="side === option" :class="{ 'is-lit': side === option }" @click="side = option">{{ option }}</button>
            </div>
            <button class="atlas-btn quay-filter-toggle" type="button" :aria-expanded="showFilters" @click="showFilters = !showFilters"><SlidersHorizontal :size="15" /> Details</button>
          </div>
          <p v-if="showFilters" class="atlas-notice atlas-notice--flag quay-filter-details">All examples use a +5% cap, 30-day epoch and 25% model volatility.</p>

          <MarketTable :query="query" :side="side" @reset="query = ''" @navigate="to => emit('navigate',to)" />
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
/* ------------------------------------------------------------------ opening */
.quay-open { padding-bottom: clamp(28px, 3.4vw, 48px); }
.quay-open-in {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 26px;
  align-items: start;
}
.quay-open-copy { display: grid; gap: clamp(12px, 1.6vw, 20px); min-width: 0; }
.quay-display { font-size: clamp(38px, 5.4vw, 72px); }
.quay-back { justify-self: end; margin-top: 4px; flex: none; }

/* -------------------------------------------------------------------- facts */
.quay-facts-scene { padding-block: clamp(24px, 2.8vw, 38px); }
.quay-facts { --cols: 4; }

/* ------------------------------------------------------------------- detail */
.quay-detail-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: clamp(18px, 2vw, 28px);
}
.quay-detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 300px) minmax(0, 1fr);
  gap: clamp(18px, 2.4vw, 36px);
  align-items: start;
}
.quay-passport { display: grid; gap: 18px; align-content: start; }
.quay-passport-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.quay-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #6bc4ff, #1b6ea8 68%, #0a2c44);
  color: #04060d;
  font: 500 15px/1 var(--font-mono);
  box-shadow: 0 0 34px rgba(64, 179, 255, 0.42);
}
.quay-passport-name { display: grid; gap: 2px; margin-right: auto; min-width: 0; }
.quay-passport-name b { font: 400 22px/1.1 var(--font-display); letter-spacing: 0.01em; }
.quay-passport-name small { color: var(--star-faint); font: 400 10px/1.4 var(--font-mono); letter-spacing: 0.14em; text-transform: uppercase; }
.quay-passport-rows { border-top: 1px solid var(--hair); }
.quay-passport-rows dd.is-income { color: var(--mint); }
.quay-passport-note { padding-top: 14px; border-top: 1px solid var(--hair); }
.quay-detail-figure { min-width: 0; }

/* --------------------------------------------------------------------- leaf */
.quay-leaf-face {
  display: grid;
  gap: 16px;
  justify-items: start;
  max-width: 860px;
  margin-inline: auto;
}
.quay-leaf-mark {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: rgba(64, 179, 255, 0.12);
  color: var(--beam);
  box-shadow: inset 0 0 0 1px rgba(64, 179, 255, 0.4);
}
.quay-leaf-copy {
  margin: 0;
  max-width: 62ch;
  color: var(--star-mute);
  font: 400 14px/1.7 var(--font-body);
}
.quay-leaf-cta { margin-top: 4px; }

/* -------------------------------------------------------------------- board */
.quay-filters {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: clamp(16px, 2vw, 24px);
}
.quay-search {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1 1 260px;
  max-width: 380px;
  color: var(--star-faint);
}
.quay-search .atlas-input { min-height: 44px; }
.quay-side { flex: none; }
.quay-filter-toggle { margin-left: auto; }
.quay-filter-details { margin-bottom: 18px; }

/* ---------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .quay-detail-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 900px) {
  .quay-open-in { grid-template-columns: minmax(0, 1fr); }
  .quay-back { justify-self: start; }
  .quay-search { max-width: none; flex: 1 1 100%; }
  .quay-filter-toggle { margin-left: 0; }
}
</style>
