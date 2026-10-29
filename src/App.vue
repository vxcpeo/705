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
    document.querySelector('.bp-nav-toggle')?.focus()
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
  <a class="bp-skip" href="#main">Skip to content</a>

  <div class="bp-frame">
    <main id="main" class="bp-leaf">
      <div class="bp-dock">
        <a class="bp-dock-brand" href="/" :aria-label="`${brand.name} overview`" @click.prevent="navigate('/')">
          <img src="/icon.svg" alt="" width="30" height="30" decoding="async" aria-hidden="true" />
        </a>
        <span class="bp-dock-rule" aria-hidden="true"></span>
        <div class="bp-dock-actions">
          <SolanaWalletButton class="bp-wallet" />
          <a class="bp-btn bp-btn--solid" href="/app/markets" @click.prevent="navigate('/app/markets')">Open the board</a>
          <button class="bp-btn bp-btn--line bp-nav-toggle" type="button" :aria-expanded="railOpen" aria-controls="bp-index"
                  :aria-label="railOpen ? 'Close navigation' : 'Open navigation'" @click="railOpen = !railOpen">
            <Menu :size="16" />
          </button>
        </div>
      </div>

      <div class="bp-leaf-body">
        <div class="bp-route">
        <HomePage v-if="pathname === '/'" @navigate="navigate" />
        <MarketWorkspace v-else-if="appPage" :path="pathname" @navigate="navigate" />
        <ScenarioLab v-else-if="pathname === '/signal'" />
        <DocsPage v-else-if="['/docs', '/risk', '/terms', '/privacy'].includes(pathname)" :path="pathname" @navigate="navigate" />
        <section v-else class="bp-void">
          <div class="nf-sheet">
            <p class="bp-kicker">Error 404</p>
            <h1 class="bp-display" tabindex="-1">No such leaf.</h1>
            <p class="bp-lead">That path is not in this preview. Start from the overview or open the board.</p>
            <p class="nf-action"><a class="bp-btn bp-btn--solid" href="/" @click.prevent="navigate('/')">Back to overview</a></p>
          </div>
        </section>
        </div>
      </div>

      <div class="bp-proof">
        <dl class="bp-proof-grid">
          <div><dt>Feed</dt><dd>Static samples</dd></div>
          <div><dt>Unit</dt><dd>{{ brand.asset }} / unissued</dd></div>
          <div><dt>Stores</dt><dd>This browser</dd></div>
          <div><dt>Target</dt><dd>{{ brand.domain }}</dd></div>
        </dl>
        <p class="bp-proof-note">Illustrative values. No live quote, custody, signing or execution.</p>
      </div>
    </main>

    <button v-if="railOpen" class="bp-veil" type="button" tabindex="-1" aria-hidden="true" @click="railOpen = false"></button>

    <div class="bp-spine" role="complementary" aria-label="Terminal index">
      <div class="bp-spine-brand">
        <a class="bp-lockup" href="/" :aria-label="`${brand.name} overview`" @click.prevent="navigate('/')">
          <img src="/icon.svg" alt="" width="36" height="36" decoding="async" aria-hidden="true" />
          <b>{{ brand.name }}</b>
        </a>
        <p class="bp-spine-thesis">{{ brand.network }} market terminal<br />Preview build</p>
      </div>

      <nav id="bp-index" class="bp-index" :class="{ 'is-open': railOpen }" aria-label="Primary">
        <a v-for="[num, label, to, note] in nav" :key="to" class="bp-index-link" :href="to"
           :aria-current="isCurrent(to) ? 'page' : undefined" @click.prevent="navigate(to)">
          <b>{{ num }}</b>
          <span>{{ label }}</span>
          <small>{{ note }}</small>
        </a>
      </nav>

      <dl class="bp-instrument">
        <div class="bp-instrument-row"><dt>Mode</dt><dd><b>Preview</b></dd></div>
        <div class="bp-instrument-row"><dt>Network</dt><dd><b>{{ brand.network }}</b></dd></div>
        <div class="bp-instrument-row"><dt>Unit</dt><dd><b>{{ brand.asset }}</b> / not issued</dd></div>
        <div class="bp-instrument-row"><dt>Records</dt><dd><b>local only</b></dd></div>
      </dl>

      <p class="bp-spine-target">{{ brand.handle }} / {{ brand.domain }} / targets, not registered</p>

      <footer class="bp-foot">
        <div class="bp-foot-brand">
          <img src="/icon.svg" alt="" width="18" height="18" decoding="async" aria-hidden="true" />
          <b>{{ brand.name }}</b>
        </div>
        <p class="bp-foot-copy">{{ brand.network }} preview / illustrative values / no transactions / {{ brand.handle }} and {{ brand.domain }} are unregistered targets</p>
        <ul class="bp-foot-links">
          <li v-for="[label, to] in colophonLinks" :key="to"><a :href="to" @click.prevent="navigate(to)">{{ label }}</a></li>
        </ul>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.nf-sheet { max-width: 62ch; padding-block: clamp(30px, 8vh, 90px); }
.nf-action { margin-block-start: 18px; }
.bp-wallet :deep(.bp-btn) { width: 100%; }

@media (max-width: 1100px) {
  .bp-dock-brand { flex: 1 1 auto; }
}
@media (max-width: 680px) {
  .bp-dock-actions { flex-wrap: wrap; }
  .bp-lockup-text small { display: none; }
}
</style>
