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
    document.querySelector('.bl-nav-toggle')?.focus()
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
  <a class="bl-skip" href="#main">Skip to content</a>

  <div class="bl-shell">
    <header class="bl-mast">
      <a class="bl-mark" href="/" :aria-label="`${brand.name} overview`" @click.prevent="navigate('/')">
        <img src="/icon.svg" alt="" width="34" height="34" decoding="async" aria-hidden="true" />
        <b class="bl-wordmark">{{ brand.name }}</b>
      </a>

      <nav id="bl-index" class="bl-nav" :class="{ 'is-open': railOpen }" aria-label="Primary">
        <a v-for="[num, label, to, note] in nav" :key="to" class="bl-navlink" :href="to"
           :aria-current="isCurrent(to) ? 'page' : undefined" @click.prevent="navigate(to)">
          <b>{{ num }}</b>
          <span>{{ label }}</span>
          <small>{{ note }}</small>
        </a>
      </nav>

      <div class="bl-mast-act">
        <SolanaWalletButton class="bl-wallet" />
        <a class="bl-btn bl-btn--solid" href="/app/markets" @click.prevent="navigate('/app/markets')">Open the board</a>
        <button class="bl-btn bl-btn--icon bl-nav-toggle" type="button" :aria-expanded="railOpen" aria-controls="bl-index"
                :aria-label="railOpen ? 'Close navigation' : 'Open navigation'" @click="railOpen = !railOpen">
          <Menu :size="18" />
        </button>
      </div>
    </header>

    <main id="main" class="bl-stage">
      <div class="bl-route">
        <HomePage v-if="pathname === '/'" @navigate="navigate" />
        <MarketWorkspace v-else-if="appPage" :path="pathname" @navigate="navigate" />
        <ScenarioLab v-else-if="pathname === '/signal'" />
        <DocsPage v-else-if="['/docs', '/risk', '/terms', '/privacy'].includes(pathname)" :path="pathname" @navigate="navigate" />
        <section v-else class="bl-page">
          <div class="bl-bento">
            <div class="bl-tile bl-tile--tint bl-span-8 bl-void">
              <p class="bl-kicker">Error 404</p>
              <h1 class="bl-display" tabindex="-1">No such leaf.</h1>
              <p class="bl-lead">That path is not in this preview. Start from the overview or open the board.</p>
              <p class="bl-void-action"><a class="bl-btn bl-btn--solid" href="/" @click.prevent="navigate('/')">Back to overview</a></p>
            </div>
          </div>
        </section>
      </div>
    </main>

    <button v-if="railOpen" class="bl-veil" type="button" tabindex="-1" aria-hidden="true" @click="railOpen = false"></button>

    <footer class="bl-foot">
      <div class="bl-foot-deck">
        <section class="bl-tile bl-tile--plum bl-span-4 bl-foot-about">
          <a class="bl-foot-mark" href="/" @click.prevent="navigate('/')">
            <img src="/icon.svg" alt="" width="22" height="22" decoding="async" aria-hidden="true" />
            <b>{{ brand.name }}</b>
          </a>
          <p class="bl-thesis">{{ brand.network }} market terminal<br />Preview build</p>
          <a class="bl-xlink" :href="brand.xUrl" target="_blank" rel="noopener noreferrer"
             :aria-label="`${brand.name} on X, ${brand.handle} (opens in a new tab)`">
            <span class="bl-xlink-badge" aria-hidden="true">X</span>
            <span>{{ brand.handle }}</span>
            <span class="bl-xlink-arrow" aria-hidden="true">↗</span>
          </a>
          <p class="bl-targets">{{ brand.domain }}</p>
          <img class="bl-foot-seal" src="/icon.svg" alt="" width="64" height="64" decoding="async" aria-hidden="true" />
        </section>

        <section class="bl-tile bl-span-4 bl-tile--surface">
          <dl class="bl-instrument">
            <div class="bl-instrument-row"><dt>Mode</dt><dd><b>Preview</b></dd></div>
            <div class="bl-instrument-row"><dt>Network</dt><dd><b>{{ brand.network }}</b></dd></div>
            <div class="bl-instrument-row"><dt>Unit</dt><dd><b>{{ brand.asset }}</b> / not issued</dd></div>
            <div class="bl-instrument-row"><dt>Records</dt><dd><b>local only</b></dd></div>
          </dl>
        </section>

        <section class="bl-tile bl-span-4">
          <dl class="bl-proof-grid">
            <div><dt>Feed</dt><dd>Static samples</dd></div>
            <div><dt>Unit</dt><dd>{{ brand.asset }} / unissued</dd></div>
            <div><dt>Stores</dt><dd>This browser</dd></div>
            <div><dt>Domain</dt><dd>{{ brand.domain }}</dd></div>
          </dl>
          <p class="bl-proof-note">Illustrative values. No live quote, custody, signing or execution.</p>
        </section>
      </div>

      <div class="bl-colophon">
        <p class="bl-colophon-copy">{{ brand.network }} preview / illustrative values / no transactions / {{ brand.domain }} / {{ brand.handle }}</p>
        <ul class="bl-colophon-links">
          <li v-for="[label, to] in colophonLinks" :key="to"><a :href="to" @click.prevent="navigate(to)">{{ label }}</a></li>
        </ul>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.bl-void { display: grid; gap: 14px; }
.bl-void-seal { width: 52px; height: 52px; border-radius: 14px; opacity: .9; }
.bl-void-action { padding-block-start: 6px; }
.bl-wallet :deep(.bl-btn) { width: 100%; }

.bl-foot-about { position: relative; overflow: hidden; }
.bl-xlink {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  width: fit-content;
  padding: 5px 12px 5px 5px;
  border: 1px solid var(--bl-plum-line);
  border-radius: var(--bl-radius-pill);
  color: var(--bl-plum-text);
  font: 600 11px/1.2 var(--bl-font-mono);
  letter-spacing: .03em;
  text-decoration: none;
  transition: border-color var(--bl-dur) var(--bl-ease), background var(--bl-dur) var(--bl-ease);
}
.bl-xlink:hover { border-color: var(--bl-accent); background: rgba(230, 0, 111, .16); }
.bl-xlink:focus-visible { outline: 2px solid var(--bl-accent-soft); outline-offset: 3px; }
.bl-xlink-badge {
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border-radius: 7px;
  background: var(--bl-accent);
  color: #fff;
  font: 700 10px/1 var(--bl-font-mono);
}
.bl-xlink-arrow { color: var(--bl-plum-muted); font-size: 12px; }
.bl-foot-seal {
  position: absolute;
  inset-block-end: -26px;
  inset-inline-end: -20px;
  width: 92px;
  height: 92px;
  opacity: .12;
  pointer-events: none;
}

.bl-veil {
  position: fixed;
  inset: 0;
  z-index: 30;
  border: 0;
  background: rgba(23, 11, 18, .45);
  backdrop-filter: blur(2px);
}

@media (max-width: 760px) {
  .bl-mast-act .bl-btn--solid { padding-inline: 14px; font-size: 11.5px; }
}
</style>
