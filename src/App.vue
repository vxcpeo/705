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
    document.querySelector('.tty-command-more')?.focus()
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
  <a class="tty-skip" href="#main">Skip to content</a>

  <div class="tty-frame">
    <main id="main" class="tty-console">
      <div class="tty-status">
        <a class="tty-status-brand" href="/" :aria-label="`${brand.name} overview`" @click.prevent="navigate('/')">
          <img src="/icon.svg" alt="" width="18" height="18" decoding="async" aria-hidden="true" />
          <span>{{ brand.name }}</span>
        </a>
        <div class="tty-status-cells" role="status" aria-label="Build status">
          <span class="tty-status-cell"><i aria-hidden="true"></i>Mode <b>Preview</b></span>
          <span class="tty-status-cell">Network <b>{{ brand.network }}</b></span>
          <span class="tty-status-cell">Unit <b>{{ brand.asset }} / not issued</b></span>
          <span class="tty-status-cell">Records <b>local only</b></span>
        </div>
        <span class="tty-status-tail">{{ brand.handle }} / {{ brand.domain }} / targets, not registered</span>
      </div>

      <div class="tty-command">
        <div class="tty-command-line">
          <span class="tty-prompt" aria-hidden="true">&#10095;</span>
          <p class="tty-command-copy">{{ brand.network }} market terminal<br />Preview build</p>
        </div>
        <div class="tty-command-actions">
          <SolanaWalletButton class="tty-wallet" />
          <a class="tty-btn tty-btn--ghost" href="/app/markets" @click.prevent="navigate('/app/markets')">Open the board</a>
          <button class="tty-command-more" type="button" :aria-expanded="railOpen" aria-controls="tty-commands"
                  :aria-label="railOpen ? 'Close navigation' : 'Open navigation'" @click="railOpen = !railOpen">
            <Activity :size="17" />
          </button>
        </div>
      </div>

      <button v-if="railOpen" class="tty-nav-scrim" type="button" tabindex="-1" aria-hidden="true" @click="railOpen = false"></button>

      <div class="tty-deck">
        <nav id="tty-commands" class="tty-nav" :class="{ open: railOpen }" aria-label="Primary">
          <a v-for="[num, label, to, note] in nav" :key="to" class="tty-nav-link" :href="to"
             :aria-current="isCurrent(to) ? 'page' : undefined" @click.prevent="navigate(to)">
            <b>{{ num }}</b><span>{{ label }}</span><small>{{ note }}</small>
          </a>
        </nav>

        <div class="tty-stage">
          <HomePage v-if="pathname === '/'" @navigate="navigate" />
          <MarketWorkspace v-else-if="appPage" :path="pathname" @navigate="navigate" />
          <ScenarioLab v-else-if="pathname === '/signal'" />
          <DocsPage v-else-if="['/docs', '/risk', '/terms', '/privacy'].includes(pathname)" :path="pathname" @navigate="navigate" />
          <section v-else class="tty-scene">
            <div class="tty-scene-in tty-stack tty-lost">
              <p class="tty-kicker">Error 404</p>
              <h1 class="tty-display" tabindex="-1">No such leaf.</h1>
              <p class="tty-lead">That path is not in this preview. Start from the overview or open the board.</p>
              <p class="tty-lost-cta"><a class="tty-btn tty-btn--primary" href="/" @click.prevent="navigate('/')">Back to overview</a></p>
            </div>
          </section>

          <div class="tty-colophon">
            <div class="tty-colophon-in">
              <div class="tty-colophon-top">
                <div class="tty-colophon-brand">
                  <img src="/icon.svg" alt="" width="20" height="20" decoding="async" aria-hidden="true" />
                  <b>{{ brand.name }}</b>
                </div>
                <p class="tty-colophon-copy">{{ brand.network }} preview / illustrative values / no transactions / {{ brand.handle }} and {{ brand.domain }} are unregistered targets</p>
                <ul class="tty-colophon-links">
                  <li v-for="[label, to] in colophonLinks" :key="to"><a :href="to" @click.prevent="navigate(to)">{{ label }}</a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="tty-hint">
        <dl class="tty-station">
          <div><dt>Feed</dt><dd class="is-hold">Static samples</dd></div>
          <div><dt>Unit</dt><dd>{{ brand.asset }} / unissued</dd></div>
          <div><dt>Stores</dt><dd>This browser</dd></div>
          <div><dt>Target</dt><dd>{{ brand.domain }}</dd></div>
        </dl>
        <p class="tty-tiny">Illustrative values. No live quote, custody, signing or execution.</p>
      </div>
    </main>
  </div>
</template>

<style scoped>
.tty-lost { max-width: 62ch; padding-block: 24px; }
.tty-lost-cta { margin: 8px 0 0; }
.tty-wallet :deep(.tty-btn) { width: 100%; }

@media (max-width: 860px) {
  .tty-nav { display: none; }
  .tty-nav.open { display: flex; }
  .tty-command-more { display: grid; }
}
@media (min-width: 861px) {
  .tty-nav-scrim { display: none; }
}
</style>
