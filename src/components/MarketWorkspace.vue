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
    <section class="tty-scene wrk-open">
      <div class="tty-scene-in wrk-open-in">
        <div class="wrk-open-copy">
          <p class="tty-kicker">{{ brand.network }} / paper market</p>
          <h1 class="tty-display wrk-display" tabindex="-1">{{ pageTitle }}</h1>
          <p class="tty-lead">{{ copy }}</p>
        </div>
        <a class="tty-btn tty-btn--ghost wrk-back" href="/" @click.prevent="emit('navigate','/')"><ArrowLeft :size="15" /> Markets</a>
      </div>
    </section>

    <div class="wrk-deck">
      <div class="wrk-main">

    <!-- asset detail -->
    <section v-if="symbol" class="tty-scene wrk-detail">
      <div class="tty-scene-in">
        <div class="wrk-detail-head">
          <h2 class="tty-h2">{{ symbol }} / {{ brand.network }}</h2>
          <p class="tty-meta">30-day epoch | +5% cap | illustrative values</p>
        </div>
        <div class="wrk-detail-grid">
          <div class="tty-face wrk-passport">
            <div class="wrk-spec-top">
              <span class="wrk-mark" aria-hidden="true">{{ symbol.slice(0, 1) }}</span>
              <span class="wrk-spec-name"><b>{{ symbol }}</b><small>Example series</small></span>
              <span class="tty-pill tty-pill--accent"><i aria-hidden="true"></i>Paper only</span>
            </div>
            <dl class="tty-pairs wrk-spec-rows">
              <div><dt>Reference</dt><dd>{{ symbol === 'SOL' ? '$182.00' : symbol === 'JUP' ? '$1.12' : symbol === 'BONK' ? '$0.000021' : '$1.00' }}</dd></div>
              <div><dt>Income model</dt><dd class="inc">+5% cap</dd></div>
              <div><dt>Settlement</dt><dd>Not live</dd></div>
            </dl>
            <p class="tty-note wrk-spec-note">Illustrative values. No live quote, custody, signing or execution.</p>
          </div>
          <div class="wrk-detail-figure">
            <PayoffExplorer :spot="symbol === 'SOL' ? 182 : symbol === 'JUP' ? 1.12 : symbol === 'BONK' ? 0.000021 : 1" :asset="symbol" />
          </div>
        </div>
      </div>
    </section>

    <!-- launchpad leaf -->
    <section v-else-if="pageTitle === 'Launchpad'" class="tty-scene wrk-leaf">
      <div class="tty-scene-in">
        <div class="tty-face tty-face--halo wrk-doc-face">
          <div class="tty-face-head">
            <h2 class="tty-h2">Suggest a market.</h2>
            <span class="tty-pill"><i aria-hidden="true"></i>Listing intake</span>
          </div>
          <span class="wrk-doc-mark"><WalletCards :size="19" /></span>
          <p class="wrk-doc-copy">Any SPL market unit with a verified price feed and USDC liquidity path may qualify. This preview records no wallet request or listing transaction.</p>
          <a class="tty-btn tty-btn--primary wrk-doc-cta" href="/docs#listing" @click.prevent="emit('navigate','/docs#listing')">Read listing notes <ArrowUpRight :size="15" /></a>
        </div>
      </div>
    </section>

    <!-- recompose leaf -->
    <section v-else-if="pageTitle === 'Recompose'" class="tty-scene wrk-leaf">
      <div class="tty-scene-in">
        <div class="tty-face tty-face--halo wrk-doc-face">
          <div class="tty-face-head">
            <h2 class="tty-h2">One asset again.</h2>
            <span class="tty-pill"><i aria-hidden="true"></i>Income + Upside</span>
          </div>
          <span class="wrk-doc-mark"><TrendingUp :size="19" /></span>
          <p class="wrk-doc-copy">Recomposition would require a wallet transaction. The local preview keeps this action visible while execution remains unavailable.</p>
          <button class="tty-btn" type="button" disabled>Recompose unavailable</button>
        </div>
      </div>
    </section>

    <!-- board -->
    <template v-else>
      <section class="tty-scene wrk-board">
        <div class="tty-scene-in">
          <!-- MarketTable renders its own section head ("Market quotes") plus the -->
          <!-- stats band, so the workspace does not repeat a heading here. -->
          <div class="wrk-filters">
            <label class="wrk-search">
              <Search :size="15" />
              <span class="visually-hidden">Search markets</span>
              <input v-model="query" class="tty-input" type="search" placeholder="Search token or market" />
            </label>
            <div class="tty-switch wrk-side" aria-label="Position type">
              <button v-for="option in ['All','Income','Upside']" :key="option" type="button" :aria-pressed="side === option" :class="{ 'on': side === option }" @click="side = option">{{ option }}</button>
            </div>
            <button class="tty-btn wrk-filter-toggle" type="button" :aria-expanded="showFilters" @click="showFilters = !showFilters"><SlidersHorizontal :size="15" /> Details</button>
          </div>
          <p v-if="showFilters" class="tty-notice tty-notice--flag wrk-filter-details">All examples use a +5% cap, 30-day epoch and 25% model volatility.</p>

          <MarketTable :query="query" :side="side" @reset="query = ''" @navigate="to => emit('navigate',to)" />
        </div>
      </section>
    </template>
      </div>

      <div class="wrk-rail">
        <section class="tty-scene wrk-facts-scene">
          <div class="tty-scene-in">
            <dl class="tty-facts wrk-facts">
              <div><dt>Sheet</dt><dd>{{ pageTitle }}</dd><dd>{{ brand.network }} preview</dd></div>
              <div><dt>Cap default</dt><dd>+5%</dd><dd>30-day epoch</dd></div>
              <div><dt>Feed</dt><dd>Static</dd><dd>Not a live quote</dd></div>
              <div><dt>Unit</dt><dd>{{ brand.asset }}*</dd><dd>Proposed, unissued</dd></div>
            </dl>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ------------------------------------------------------------------ opening */
.wrk-open { padding-bottom: clamp(28px, 3.4vw, 48px); }
.wrk-open-in {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 26px;
  align-items: start;
}
.wrk-open-copy { display: grid; gap: clamp(12px, 1.6vw, 20px); min-width: 0; }
.wrk-display { font-size: clamp(30px, 3.6vw, 46px); }
.wrk-back { justify-self: end; margin-top: 4px; flex: none; }

/* -------------------------------------------------------------------- facts */
.wrk-facts-scene { padding-block: clamp(24px, 2.8vw, 38px); }
.wrk-facts { --cols: 4; }

/* ------------------------------------------------------------------- detail */
.wrk-detail-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: clamp(18px, 2vw, 28px);
}
.wrk-detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 300px) minmax(0, 1fr);
  gap: clamp(18px, 2.4vw, 36px);
  align-items: start;
}
.wrk-passport { display: grid; gap: 18px; align-content: start; }
.wrk-spec-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.wrk-mark {
  display: grid;
  place-items: center;
  flex: none;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #ff6b6b, #a30000 68%, #2a0303);
  color: #050608;
  font: 500 15px/1 var(--font-mono);
  box-shadow: 0 0 34px rgba(255, 0, 0, 0.42);
}
.wrk-spec-name { display: grid; gap: 2px; margin-right: auto; min-width: 0; }
.wrk-spec-name b { font: 400 22px/1.1 var(--font-display); letter-spacing: 0.01em; }
.wrk-spec-name small { color: var(--faint); font: 400 10px/1.4 var(--font-mono); letter-spacing: 0.14em; text-transform: uppercase; }
.wrk-spec-rows { border-top: 1px solid var(--line); }
.wrk-spec-rows dd.inc { color: var(--mint); }
.wrk-spec-note { padding-top: 14px; border-top: 1px solid var(--line); }
.wrk-detail-figure { min-width: 0; }

/* --------------------------------------------------------------------- leaf */
.wrk-doc-face {
  display: grid;
  gap: 16px;
  justify-items: start;
  max-width: 860px;
  margin-inline: auto;
}
.wrk-doc-mark {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: rgba(255, 0, 0, 0.12);
  color: var(--accent-safe);
  box-shadow: inset 0 0 0 1px rgba(255, 0, 0, 0.4);
}
.wrk-doc-copy {
  margin: 0;
  max-width: 62ch;
  color: var(--muted);
  font: 400 14px/1.7 var(--font-body);
}
.wrk-doc-cta { margin-top: 4px; }

/* -------------------------------------------------------------------- board */
.wrk-filters {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: clamp(16px, 2vw, 24px);
}
.wrk-search {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1 1 260px;
  max-width: 380px;
  color: var(--faint);
}
.wrk-search .tty-input { min-height: 44px; }
.wrk-side { flex: none; }
.wrk-filter-toggle { margin-left: auto; }
.wrk-filter-details { margin-bottom: 18px; }

/* --------------------------------------------------------------- pane deck */
.wrk-deck {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 300px);
  align-items: stretch;
  border-top: 1px solid var(--line);
}
.wrk-main { min-width: 0; }
.wrk-main > .tty-scene { border-bottom: 0; }
.wrk-rail {
  min-width: 0;
  display: flex;
  flex-direction: column;
  border-left: 1px solid var(--line);
  background: rgba(13, 20, 27, 0.35);
}
.wrk-facts { --cols: 1; border-top: 0; border-bottom: 0; }
.wrk-rail .wrk-facts > * + * { border-top: 1px solid var(--line); }

/* ---------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .wrk-detail-grid { grid-template-columns: minmax(0, 1fr); }
  .wrk-deck { grid-template-columns: minmax(0, 1fr); }
  .wrk-rail { border-left: 0; border-top: 1px solid var(--line); }
  .wrk-facts { --cols: 2; }
}
@media (max-width: 900px) {
  .wrk-open-in { grid-template-columns: minmax(0, 1fr); }
  .wrk-back { justify-self: start; }
  .wrk-search { max-width: none; flex: 1 1 100%; }
  .wrk-filter-toggle { margin-left: 0; }
}
</style>
