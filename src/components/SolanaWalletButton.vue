<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { ExternalLink, ShieldCheck, Wallet, X } from 'lucide-vue-next'
import {
  connectSolanaWallet,
  disconnectSolanaWallet,
  getSolanaWalletSetupError,
  getSolanaWallets,
  initializeSolanaWallets,
  watchAvailableSolanaWallets,
  watchSolanaWallet,
  solanaConfig,
} from '../solana.js'

const emit = defineEmits(['connected', 'disconnected'])
const wallets = shallowRef([])
const activeWallet = shallowRef(null)
const address = ref('')
const modalOpen = ref(false)
const discovering = ref(false)
const pendingWallet = ref('')
const errorMessage = ref('')
const setupMessage = ref('')
const dialogPanel = ref(null)
let stopWalletDiscovery = () => {}
let stopWalletEvents = () => {}
let returnFocus = null

const shortAddress = computed(() => address.value ? address.value.slice(0, 5) + '...' + address.value.slice(-5) : '')
const buttonLabel = computed(() => address.value ? shortAddress.value : 'Connect wallet')

function showModal() {
  returnFocus = document.activeElement
  modalOpen.value = true
  errorMessage.value = ''
  setupMessage.value = ''
  wallets.value = getSolanaWallets()
  discovering.value = true
  void nextTick(() => dialogPanel.value?.querySelector('.wl-close')?.focus())
  void initializeSolanaWallets()
    .then((available) => {
      wallets.value = available
      setupMessage.value = getSolanaWalletSetupError()
    })
    .catch((error) => {
      setupMessage.value = error?.message || 'Wallet discovery could not start.'
    })
    .finally(() => { discovering.value = false })
}

function closeModal() {
  modalOpen.value = false
  void nextTick(() => returnFocus?.focus?.())
}

function onDialogKeydown(event) {
  if (event.key === 'Escape') {
    event.preventDefault()
    closeModal()
    return
  }
  if (event.key !== 'Tab' || !dialogPanel.value) return
  const focusable = [...dialogPanel.value.querySelectorAll('button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])')]
  if (!focusable.length) return
  const first = focusable[0]
  const last = focusable[focusable.length - 1]
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault()
    last.focus()
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault()
    first.focus()
  }
}

function syncAddress(nextAddress) {
  const value = typeof nextAddress === 'string' ? nextAddress : nextAddress?.address || ''
  address.value = value
  if (!value) {
    activeWallet.value = null
    stopWalletEvents()
    stopWalletEvents = () => {}
    emit('disconnected')
  } else {
    emit('connected', value, activeWallet.value?.name || '')
  }
}

async function connect(wallet) {
  pendingWallet.value = wallet.name
  errorMessage.value = ''
  try {
    const result = await connectSolanaWallet(wallet)
    stopWalletEvents()
    activeWallet.value = result.wallet
    syncAddress(result.address)
    stopWalletEvents = watchSolanaWallet((event) => {
      const next = event?.accounts?.[0]?.address || event?.address || event?.publicKey?.toString?.() || event?.toString?.() || ''
      syncAddress(next)
    }, result.wallet)
  } catch (error) {
    errorMessage.value = error?.message || `Could not connect to ${wallet.name}.`
  } finally {
    pendingWallet.value = ''
  }
}

async function disconnect() {
  pendingWallet.value = activeWallet.value?.name || 'wallet'
  errorMessage.value = ''
  try {
    await disconnectSolanaWallet(activeWallet.value)
    syncAddress('')
    closeModal()
  } catch (error) {
    errorMessage.value = error?.message || 'Wallet could not disconnect.'
  } finally {
    pendingWallet.value = ''
  }
}

onMounted(() => {
  stopWalletDiscovery = watchAvailableSolanaWallets((available) => { wallets.value = available })
})

onBeforeUnmount(() => {
  stopWalletDiscovery()
  stopWalletEvents()
})
</script>

<template>
  <div class="dock">
    <button
      type="button"
      class="bp-btn wl-trigger"
      :class="{ 'is-linked': address }"
      :aria-haspopup="'dialog'"
      :aria-expanded="modalOpen"
      :disabled="Boolean(pendingWallet)"
      @click="showModal"
    >
      <Wallet :size="15" />
      {{ pendingWallet ? 'Connecting…' : buttonLabel }}
    </button>

    <Teleport to="body">
      <div v-if="modalOpen" class="wl-scrim" @click.self="closeModal" @keydown.esc.stop="closeModal">
        <section ref="dialogPanel" class="wl-dialog" role="dialog" aria-modal="true" aria-labelledby="wallet-dialog-title" tabindex="-1" @keydown.stop="onDialogKeydown">
          <header class="wl-head">
            <div class="wl-head-copy">
              <span class="wl-eyebrow">SOLANA / {{ solanaConfig.cluster.toUpperCase() }}</span>
              <h2 id="wallet-dialog-title" class="bp-h2 wl-title">{{ address ? 'Wallet connected' : 'Choose a wallet' }}</h2>
            </div>
            <button class="wl-close" type="button" aria-label="Close wallet dialog" @click="closeModal"><X :size="18" /></button>
          </header>

          <div class="wl-body">
            <div v-if="address" class="wl-account">
              <span class="wl-account-name"><Wallet :size="16" /> {{ activeWallet?.name || 'Solana wallet' }}</span>
              <code>{{ address }}</code>
              <button class="bp-btn bp-btn--ghost bp-btn--wide wl-disconnect" type="button" :disabled="Boolean(pendingWallet)" @click="disconnect">
                {{ pendingWallet ? 'Disconnecting…' : 'Disconnect wallet' }}
              </button>
            </div>

            <template v-else>
              <p class="wl-copy">Connect a Solana account to display its public address. This site does not ask for transaction signatures.</p>
              <p class="bp-notice bp-notice--ok wl-network"><ShieldCheck :size="15" /> Use a Solana wallet with an SPL account. The CA preview never asks for a seed phrase.</p>

              <p v-if="discovering" class="bp-notice wl-discovery" role="status">Looking for MetaMask, Phantom, Solflare and other Solana wallets…</p>
              <div v-else-if="wallets.length" class="wl-options" aria-label="Available Solana wallets">
                <button v-for="wallet in wallets" :key="wallet.name" class="wl-option" type="button" :disabled="Boolean(pendingWallet)" @click="connect(wallet)">
                  <img v-if="wallet.icon" class="wl-option-icon" :src="wallet.icon" alt="" />
                  <span v-else class="wl-option-icon wl-option-placeholder"><Wallet :size="18" /></span>
                  <span class="wl-option-name">{{ wallet.name }}</span>
                  <span v-if="pendingWallet === wallet.name" class="wl-option-state">Connecting…</span>
                  <ExternalLink v-else :size="15" class="wl-option-arrow" />
                </button>
              </div>
              <div v-else class="wl-empty">
                <p>No compatible Solana wallet was detected.</p>
                <p class="wl-empty-help">Install a wallet, enable its Solana account, then reopen this panel.</p>
                <div class="wl-install">
                  <a href="https://metamask.io/download/" target="_blank" rel="noreferrer">MetaMask <ExternalLink :size="12" /></a>
                  <a href="https://phantom.app/download" target="_blank" rel="noreferrer">Phantom <ExternalLink :size="12" /></a>
                  <a href="https://solflare.com/download" target="_blank" rel="noreferrer">Solflare <ExternalLink :size="12" /></a>
                </div>
              </div>
            </template>

            <p v-if="errorMessage" class="bp-notice bp-notice--alert wl-error" role="alert">{{ errorMessage }}</p>
            <p v-if="setupMessage" class="bp-notice bp-notice--flag wl-setup" role="status">MetaMask connector: {{ setupMessage }}</p>
            <p class="wl-foot">Only the selected wallet’s public Solana address is read.</p>
          </div>
        </section>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.dock { display: inline-flex; }
.wl-trigger { gap: 7px; }
.wl-trigger.is-linked { border-color: var(--bp-cobalt); color: var(--bp-cobalt-safe); }

/* ----------------------------------------------------------------- dialog */
.wl-scrim {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(8, 27, 43, .38);
  backdrop-filter: blur(3px);
}
.wl-dialog {
  width: min(460px, 100%);
  max-height: min(86vh, 720px);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  border: 1px solid var(--bp-line);
  border-radius: var(--bp-r-lg);
  background: var(--bp-paper);
  box-shadow: 0 40px 90px rgba(8, 27, 43, .28);
  overflow: hidden;
}
.wl-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 22px 16px;
  border-block-end: 1px solid var(--bp-line);
  background:
    radial-gradient(320px 160px at 100% 0%, rgba(0, 0, 255, .16), transparent 70%),
    var(--bp-paper);
}
.wl-head-copy { display: grid; gap: 6px; }
.wl-eyebrow { color: var(--bp-cobalt-safe); font: 600 9px/1.4 var(--bp-font-mono); letter-spacing: .18em; }
.wl-title { font-size: 24px; }
.wl-close {
  display: grid;
  place-items: center;
  flex: none;
  width: 34px;
  height: 34px;
  border: 1px solid var(--bp-line);
  border-radius: 12px;
  background: var(--bp-paper);
  color: var(--bp-ink-2);
}
.wl-close:hover { border-color: var(--bp-cobalt); color: var(--bp-cobalt-safe); }

.wl-body {
  display: grid;
  gap: 12px;
  padding: 18px 22px 22px;
  overflow: auto;
}
.wl-copy { color: var(--bp-ink-2); font: 400 13px/1.7 var(--bp-font-body); }
.wl-network { display: flex; gap: 8px; align-items: start; }
.wl-account { display: grid; gap: 10px; }
.wl-account-name { display: inline-flex; align-items: center; gap: 8px; font: 600 13px/1.4 var(--bp-font-body); }
.wl-account code {
  display: block;
  padding: 10px 12px;
  border: 1px solid var(--bp-line);
  border-radius: var(--bp-r-sm);
  background: var(--bp-paper-3);
  color: var(--bp-ink-2);
  font: 500 11px/1.6 var(--bp-font-mono);
  word-break: break-all;
}
.wl-options { display: grid; gap: 8px; }
.wl-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border: 1px solid var(--bp-line);
  border-radius: var(--bp-r-sm);
  background: var(--bp-paper);
  text-align: start;
  transition: border-color var(--bp-motion-duration) var(--bp-motion-ease), background-color var(--bp-motion-duration) var(--bp-motion-ease);
}
.wl-option:hover { border-color: var(--bp-cobalt); background: var(--bp-paper-3); }
.wl-option-icon { width: 26px; height: 26px; border-radius: 8px; object-fit: contain; }
.wl-option-placeholder { display: grid; place-items: center; background: var(--bp-paper-2); color: var(--bp-cobalt-safe); }
.wl-option-name { font: 600 13px/1.4 var(--bp-font-body); }
.wl-option-state { margin-inline-start: auto; color: var(--bp-muted); font: 500 10px/1.4 var(--bp-font-mono); }
.wl-option-arrow { margin-inline-start: auto; color: var(--bp-muted); }
.wl-empty { display: grid; gap: 6px; padding: 14px; border: 1px solid var(--bp-line); border-radius: var(--bp-r-sm); background: var(--bp-paper-3); }
.wl-empty p { font: 400 13px/1.6 var(--bp-font-body); }
.wl-empty-help { color: var(--bp-muted); }
.wl-install { display: flex; flex-wrap: wrap; gap: 8px 16px; margin-block-start: 4px; }
.wl-install a {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--bp-cobalt-safe);
  font: 600 11px/1.6 var(--bp-font-mono);
  letter-spacing: .04em;
  text-decoration: none;
  border-block-end: 1px solid rgba(0, 0, 204, .3);
}
.wl-foot { color: var(--bp-muted); font: 400 10px/1.7 var(--bp-font-mono); }
.wl-error, .wl-setup, .wl-discovery { margin: 0; }

@media (max-width: 520px) {
  .wl-scrim { padding: 10px; align-items: end; }
  .wl-dialog { border-end-start-radius: 22px; border-end-end-radius: 22px; max-height: 88vh; }
}
</style>
