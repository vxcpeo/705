<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Activity } from 'lucide-vue-next'
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
    document.querySelector('.atlas-mast-more')?.focus()
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
  <a class="atlas-skip" href="#main">Skip to content</a>

  <div class="atlas-root">
    <header class="atlas-mast">
      <div class="atlas-mast-id">
        <a class="atlas-brand" href="/" :aria-label="`${brand.name} overview`" @click.prevent="navigate('/')">
          <img src="/icon.svg" alt="" width="34" height="34" decoding="async" aria-hidden="true" />
          <span>{{ brand.name }}</span>
        </a>
        <p class="atlas-brand-copy">{{ brand.network }} market terminal<br />Preview build</p>
      </div>

      <div class="atlas-mast-actions">
        <SolanaWalletButton class="atlas-wallet" />
        <a class="atlas-btn atlas-btn--ghost atlas-mast-open" href="/app/markets" @click.prevent="navigate('/app/markets')">Open the board</a>
        <button class="atlas-mast-more" type="button" :aria-expanded="railOpen" aria-controls="atlas-ribbon"
                :aria-label="railOpen ? 'Close telemetry' : 'Open telemetry'" @click="railOpen = !railOpen">
          <Activity :size="17" />
        </button>
      </div>

      <button v-if="railOpen" class="atlas-mast-scrim" type="button" tabindex="-1" aria-hidden="true" @click="railOpen = false"></button>

      <div id="atlas-ribbon" class="atlas-ribbon" :class="{ 'is-open': railOpen }" role="status" aria-label="Build status">
        <span class="atlas-ribbon-cell"><i aria-hidden="true"></i>Mode <b>Preview</b></span>
        <span class="atlas-ribbon-cell atlas-ribbon-cell--wide">Network <b>{{ brand.network }}</b></span>
        <span class="atlas-ribbon-cell atlas-ribbon-cell--wide">Unit <b>{{ brand.asset }} / not issued</b></span>
        <span class="atlas-ribbon-cell">Records <b>local only</b></span>
        <span class="atlas-ribbon-tail">{{ brand.handle }} / {{ brand.domain }} / targets, not registered</span>
      </div>
    </header>

    <nav class="atlas-dock" aria-label="Primary">
      <a v-for="[num, label, to, note] in nav" :key="to" class="atlas-dock-link" :href="to"
         :aria-current="isCurrent(to) ? 'page' : undefined" @click.prevent="navigate(to)">
        <b>{{ num }}</b><span>{{ label }}</span><small>{{ note }}</small>
      </a>
    </nav>

    <main id="main" class="atlas-stage">
      <HomePage v-if="pathname === '/'" @navigate="navigate" />
      <MarketWorkspace v-else-if="appPage" :path="pathname" @navigate="navigate" />
      <ScenarioLab v-else-if="pathname === '/signal'" />
      <DocsPage v-else-if="['/docs', '/risk', '/terms', '/privacy'].includes(pathname)" :path="pathname" @navigate="navigate" />
      <section v-else class="atlas-scene">
        <div class="atlas-scene-in atlas-stack atlas-lost">
          <p class="atlas-kicker">Error 404</p>
          <h1 class="atlas-display" tabindex="-1">No such leaf.</h1>
          <p class="atlas-lead">That path is not in this preview. Start from the overview or open the board.</p>
          <p class="atlas-lost-cta"><a class="atlas-btn atlas-btn--primary" href="/" @click.prevent="navigate('/')">Back to overview</a></p>
        </div>
      </section>

      <footer class="atlas-colophon">
        <div class="atlas-colophon-in">
          <div class="atlas-colophon-top">
            <div class="atlas-colophon-brand">
              <img src="/icon.svg" alt="" width="24" height="24" decoding="async" aria-hidden="true" />
              <b>{{ brand.name }}</b>
            </div>
            <p class="atlas-colophon-copy">{{ brand.network }} preview / illustrative values / no transactions / {{ brand.handle }} and {{ brand.domain }} are unregistered targets</p>
            <ul class="atlas-colophon-links">
              <li v-for="[label, to] in colophonLinks" :key="to"><a :href="to" @click.prevent="navigate(to)">{{ label }}</a></li>
            </ul>
          </div>

          <dl class="atlas-station">
            <div><dt>Feed</dt><dd class="is-hold">Static samples</dd></div>
            <div><dt>Unit</dt><dd>{{ brand.asset }} / unissued</dd></div>
            <div><dt>Stores</dt><dd>This browser</dd></div>
            <div><dt>Target</dt><dd>{{ brand.domain }}</dd></div>
          </dl>

          <p class="atlas-tiny">Illustrative values. No live quote, custody, signing or execution.</p>
        </div>
      </footer>
    </main>
  </div>
</template>

<style scoped>
.atlas-lost { max-width: 62ch; }
.atlas-lost-cta { margin: 8px 0 0; }
.atlas-wallet :deep(.atlas-btn) { width: 100%; }

@media (max-width: 720px) {
  .atlas-mast-open { display: none; }
}
</style>
