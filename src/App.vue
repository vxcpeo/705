<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Menu } from 'lucide-vue-next'
import HomePage from './components/HomePage.vue'
import MarketWorkspace from './components/MarketWorkspace.vue'
import DocsPage from './components/DocsPage.vue'
import ScenarioLab from './components/ScenarioLab.vue'
import SolanaWalletButton from './components/SolanaWalletButton.vue'
import { brand } from './brand.js'

const pathname = ref(location.pathname.replace(/\/$/, '') || '/')
const railOpen = ref(false)
const appPage = computed(() => pathname.value.startsWith('/app/') || pathname.value === '/stats')

const nav = [
  ['01', 'Overview', '/', 'tape'],
  ['02', 'Board', '/app/markets', 'watchlist'],
  ['03', 'Journal', '/signal', 'local'],
  ['04', 'Reference', '/docs', 'method'],
  ['05', 'Boundary', '/#cap', 'model'],
  ['06', 'Limits', '/risk', 'disclosure'],
]
const colophonLinks = [
  ['Board', '/app/markets'],
  ['Journal', '/signal'],
  ['Reference', '/docs'],
  ['Limits', '/risk'],
  ['Terms', '/terms'],
  ['Privacy', '/privacy'],
]

const isCurrent = to => {
  if (to === '/') return pathname.value === '/'
  if (to === '/app/markets') return pathname.value.startsWith('/app/') || pathname.value === '/stats'
  if (to === '/signal') return pathname.value === '/signal'
  if (to === '/docs') return ['/docs'].includes(pathname.value)
  if (to === '/risk') return ['/risk', '/terms', '/privacy'].includes(pathname.value)
  return false
}

function scrollToHash() {
  if (location.hash) document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView({ behavior: 'instant' })
}

async function navigate(to) {
  const url = new URL(to, location.origin)
  if (url.pathname === location.pathname && url.hash) {
    history.pushState({}, '', url.pathname + url.hash)
    await nextTick()
    scrollToHash()
    return
  }
  history.pushState({}, '', url.pathname + url.hash)
  pathname.value = url.pathname.replace(/\/$/, '') || '/'
  await nextTick()
  if (url.hash) scrollToHash()
  else {
    window.scrollTo({ top: 0, behavior: 'instant' })
    document.querySelector('main h1')?.focus({ preventScroll: true })
  }
}

async function popState() {
  pathname.value = location.pathname.replace(/\/$/, '') || '/'
  railOpen.value = false
  await nextTick()
  scrollToHash()
}

function onKeydown(event) {
  if (event.key === 'Escape' && railOpen.value) {
    railOpen.value = false
    document.querySelector('.tide-index-toggle')?.focus()
  }
}

watch(pathname, path => {
  const title = path === '/' ? 'Overview'
    : path === '/signal' ? 'Journal'
      : path === '/docs' ? 'Reference'
        : path.split('/').pop().replace(/^./, letter => letter.toUpperCase())
  document.title = `${title} / ${brand.name}`
}, { immediate: true })

onMounted(() => {
  addEventListener('popstate', popState)
  addEventListener('keydown', onKeydown)
  nextTick(scrollToHash)
})

onBeforeUnmount(() => {
  removeEventListener('popstate', popState)
  removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <a class="tide-skip" href="#main">Skip to content</a>

  <div class="tide-shell">
    <button v-if="railOpen" class="tide-scrim" type="button" tabindex="-1" aria-hidden="true" @click="railOpen = false"></button>
    <header class="tide-mast">
      <div class="tide-mast-top">
        <a class="tide-brand" href="/" :aria-label="`${brand.name} overview`" @click.prevent="navigate('/')">
          <img src="/icon.svg" alt="" width="34" height="34" decoding="async" aria-hidden="true" />
          <b>{{ brand.name }}</b>
        </a>
        <div class="tide-mast-actions">
          <SolanaWalletButton class="tide-wallet" />
          <a class="tide-btn tide-btn--primary" href="/app/markets" @click.prevent="navigate('/app/markets')">Open the board</a>
          <button class="tide-btn tide-btn--quiet tide-index-toggle" type="button" :aria-expanded="railOpen" aria-controls="tide-index"
                  :aria-label="railOpen ? 'Close navigation' : 'Open navigation'" @click="railOpen = !railOpen">
            <Menu :size="16" />
          </button>
        </div>
      </div>

      <p class="tide-mast-line">{{ brand.network }} market terminal<br />Preview build</p>

      <nav id="tide-index" class="tide-index" :class="{ 'is-open': railOpen }" aria-label="Primary">
        <a v-for="[num, label, to, note] in nav" :key="to" class="tide-index-link" :href="to"
           :aria-current="isCurrent(to) ? 'page' : undefined" @click.prevent="navigate(to)">
          <b>{{ num }}</b><span>{{ label }}</span><small>{{ note }}</small>
        </a>
      </nav>

      <dl class="tide-instrument">
        <div class="tide-instrument-row"><dt>Mode</dt><dd><b>Preview</b></dd></div>
        <div class="tide-instrument-row"><dt>Network</dt><dd><b>{{ brand.network }}</b></dd></div>
        <div class="tide-instrument-row"><dt>Unit</dt><dd><b>{{ brand.asset }}</b> / not issued</dd></div>
        <div class="tide-instrument-row"><dt>Records</dt><dd><b>local only</b></dd></div>
      </dl>
      <p class="tide-mast-tail">{{ brand.handle }} / {{ brand.domain }} / targets, not registered</p>

      <div class="tide-mast-foot">
        <div class="tide-foot-brand">
          <img src="/icon.svg" alt="" width="20" height="20" decoding="async" aria-hidden="true" />
          <b>{{ brand.name }}</b>
        </div>
        <p class="tide-foot-copy">{{ brand.network }} preview / illustrative values / no transactions / {{ brand.handle }} and {{ brand.domain }} are unregistered targets</p>
        <ul class="tide-foot-links">
          <li v-for="[label, to] in colophonLinks" :key="to"><a :href="to" @click.prevent="navigate(to)">{{ label }}</a></li>
        </ul>
      </div>
    </header>

    <main id="main" class="tide-stage">
      <div class="tide-stage-inner">
        <HomePage v-if="pathname === '/'" @navigate="navigate" />
        <MarketWorkspace v-else-if="appPage" :path="pathname" @navigate="navigate" />
        <ScenarioLab v-else-if="pathname === '/signal'" />
        <DocsPage v-else-if="['/docs', '/risk', '/terms', '/privacy'].includes(pathname)" :path="pathname" @navigate="navigate" />
        <section v-else class="tide-band tide-band--first">
          <div class="wave-notfound">
            <p class="tide-kicker">Error 404</p>
            <h1 class="tide-display" tabindex="-1">No such leaf.</h1>
            <p class="tide-lead">That path is not in this preview. Start from the overview or open the board.</p>
            <p class="wave-notfound-cta"><a class="tide-btn tide-btn--primary" href="/" @click.prevent="navigate('/')">Back to overview</a></p>
          </div>
        </section>
      </div>

      <div class="tide-proof">
        <dl>
          <div><dt>Feed</dt><dd>Static samples</dd></div>
          <div><dt>Unit</dt><dd>{{ brand.asset }} / unissued</dd></div>
          <div><dt>Stores</dt><dd>This browser</dd></div>
          <div><dt>Target</dt><dd>{{ brand.domain }}</dd></div>
        </dl>
        <p>Illustrative values. No live quote, custody, signing or execution.</p>
      </div>
    </main>
  </div>
</template>

<style scoped>
.wave-notfound { max-width: 62ch; padding-block: clamp(30px, 8vh, 90px); }
.wave-notfound-cta { margin-block-start: 16px; }
.tide-wallet :deep(.tide-btn) { width: 100%; }

@media (max-width: 1080px) {
  .tide-mast-top { display: flex; align-items: center; gap: 10px; }
  .tide-brand { flex: 1 1 auto; }
}
@media (max-width: 640px) {
  .tide-mast-actions { flex-wrap: wrap; }
  .tide-brand small { display: none; }
}
</style>
