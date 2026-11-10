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
  void nextTick(() => dialogPanel.value?.querySelector('.bl-wallet-close')?.focus())
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
  <div class="bl-wallet-slot">
    <button
      type="button"
      class="bl-btn bl-wallet-trigger"
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
      <div v-if="modalOpen" class="bl-wallet-scrim" @click.self="closeModal" @keydown.esc.stop="closeModal">
        <section ref="dialogPanel" class="bl-wallet-dialog" role="dialog" aria-modal="true" aria-labelledby="wallet-dialog-title" tabindex="-1" @keydown.stop="onDialogKeydown">
          <header class="bl-wallet-head">
            <div class="bl-wallet-head-copy">
              <span class="bl-wallet-eyebrow">SOLANA / {{ solanaConfig.cluster.toUpperCase() }}</span>
              <h2 id="wallet-dialog-title" class="bl-h2 bl-wallet-title">{{ address ? 'Wallet connected' : 'Choose a wallet' }}</h2>
            </div>
            <button class="bl-wallet-close" type="button" aria-label="Close wallet dialog" @click="closeModal"><X :size="18" /></button>
          </header>

          <div class="bl-wallet-body">
            <div v-if="address" class="bl-wallet-account">
              <span class="bl-wallet-account-name"><Wallet :size="16" /> {{ activeWallet?.name || 'Solana wallet' }}</span>
              <code>{{ address }}</code>
              <button class="bl-btn bl-btn--wide bl-wallet-disconnect" type="button" :disabled="Boolean(pendingWallet)" @click="disconnect">
                {{ pendingWallet ? 'Disconnecting…' : 'Disconnect wallet' }}
              </button>
            </div>

            <template v-else>
              <p class="bl-wallet-copy">Connect a Solana account to display its public address. This site does not ask for transaction signatures.</p>
              <p class="bl-notice bl-notice--ok bl-wallet-network"><ShieldCheck :size="15" /> Use a Solana wallet with an SPL account. The CA preview never asks for a seed phrase.</p>

              <p v-if="discovering" class="bl-notice bl-wallet-discovery" role="status">Looking for MetaMask, Phantom, Solflare and other Solana wallets…</p>
              <div v-else-if="wallets.length" class="bl-wallet-options" aria-label="Available Solana wallets">
                <button v-for="wallet in wallets" :key="wallet.name" class="bl-wallet-option" type="button" :disabled="Boolean(pendingWallet)" @click="connect(wallet)">
                  <img v-if="wallet.icon" class="bl-wallet-option-icon" :src="wallet.icon" alt="" />
                  <span v-else class="bl-wallet-option-icon bl-wallet-placeholder"><Wallet :size="18" /></span>
                  <span class="bl-wallet-option-name">{{ wallet.name }}</span>
                  <span v-if="pendingWallet === wallet.name" class="bl-wallet-option-state">Connecting…</span>
                  <ExternalLink v-else :size="15" class="bl-wallet-option-arrow" />
                </button>
              </div>
              <div v-else class="bl-wallet-empty">
                <p>No compatible Solana wallet was detected.</p>
                <p class="bl-wallet-empty-help">Install a wallet, enable its Solana account, then reopen this panel.</p>
                <div class="bl-wallet-install">
                  <a href="https://metamask.io/download/" target="_blank" rel="noreferrer">MetaMask <ExternalLink :size="12" /></a>
                  <a href="https://phantom.app/download" target="_blank" rel="noreferrer">Phantom <ExternalLink :size="12" /></a>
                  <a href="https://solflare.com/download" target="_blank" rel="noreferrer">Solflare <ExternalLink :size="12" /></a>
                </div>
              </div>
            </template>

            <p v-if="errorMessage" class="bl-notice bl-notice--alert bl-wallet-error" role="alert">{{ errorMessage }}</p>
            <p v-if="setupMessage" class="bl-notice bl-notice--flag bl-wallet-setup" role="status">MetaMask connector: {{ setupMessage }}</p>
            <p class="bl-wallet-foot">Only the selected wallet’s public Solana address is read.</p>
          </div>
        </section>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.bl-wallet-slot { display: inline-flex; }
.bl-wallet-trigger { gap: 7px; }
.bl-wallet-trigger.is-linked { border-color: var(--bl-accent); color: var(--bl-accent-safe); }

/* ----------------------------------------------------------------- dialog */
.bl-wallet-scrim {
  position: fixed;
  inset: 0;
  z-index: 60;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(23, 11, 18, .42);
  backdrop-filter: blur(3px);
}
.bl-wallet-dialog {
  width: min(460px, 100%);
  max-height: min(86vh, 720px);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-lg);
  background: var(--bl-paper);
  box-shadow: 0 40px 90px rgba(23, 11, 18, .3);
  overflow: hidden;
}
.bl-wallet-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 22px 16px;
  border-block-end: 1px solid var(--bl-line);
  background: linear-gradient(160deg, var(--bl-tint), var(--bl-paper) 70%);
}
.bl-wallet-head-copy { display: grid; gap: 6px; }
.bl-wallet-eyebrow { color: var(--bl-accent-safe); font: 600 9px/1.4 var(--bl-font-mono); letter-spacing: .16em; }
.bl-wallet-title { font-size: 24px; }
.bl-wallet-close {
  display: grid;
  place-items: center;
  flex: none;
  width: 36px;
  height: 36px;
  border: 1px solid var(--bl-line);
  border-radius: 50%;
  background: var(--bl-paper);
  color: var(--bl-ink-soft);
}
.bl-wallet-close:hover { border-color: var(--bl-accent); color: var(--bl-accent-safe); }

.bl-wallet-body { display: grid; gap: 12px; padding: 18px 22px 22px; overflow: auto; }
.bl-wallet-copy { color: var(--bl-ink-soft); font: 400 13px/1.7 var(--bl-font-body); }
.bl-wallet-network { display: flex; gap: 8px; align-items: start; }
.bl-wallet-account { display: grid; gap: 10px; }
.bl-wallet-account-name { display: inline-flex; align-items: center; gap: 8px; font: 600 13px/1.4 var(--bl-font-body); }
.bl-wallet-account code {
  display: block;
  padding: 10px 12px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-surface);
  color: var(--bl-ink-soft);
  font: 500 11px/1.6 var(--bl-font-mono);
  word-break: break-all;
}
.bl-wallet-options { display: grid; gap: 8px; }
.bl-wallet-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-paper);
  text-align: start;
  transition: border-color var(--bl-dur) var(--bl-ease), background-color var(--bl-dur) var(--bl-ease);
}
.bl-wallet-option:hover { border-color: var(--bl-accent); background: var(--bl-tint); }
.bl-wallet-option-icon { width: 26px; height: 26px; border-radius: 8px; object-fit: contain; }
.bl-wallet-placeholder { display: grid; place-items: center; background: var(--bl-surface-2); color: var(--bl-accent-safe); }
.bl-wallet-option-name { font: 600 13px/1.4 var(--bl-font-body); }
.bl-wallet-option-state { margin-inline-start: auto; color: var(--bl-muted); font: 500 10px/1.4 var(--bl-font-mono); }
.bl-wallet-option-arrow { margin-inline-start: auto; color: var(--bl-muted); }
.bl-wallet-empty {
  display: grid;
  gap: 6px;
  padding: 14px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-surface);
}
.bl-wallet-empty p { font: 400 13px/1.6 var(--bl-font-body); }
.bl-wallet-empty-help { color: var(--bl-muted); }
.bl-wallet-install { display: flex; flex-wrap: wrap; gap: 8px 16px; margin-block-start: 4px; }
.bl-wallet-install a {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--bl-accent-safe);
  font: 600 11px/1.6 var(--bl-font-mono);
  letter-spacing: .03em;
  text-decoration: none;
  border-block-end: 1px solid rgba(194, 0, 93, .3);
}
.bl-wallet-foot { color: var(--bl-muted); font: 400 10px/1.7 var(--bl-font-mono); }
.bl-wallet-error, .bl-wallet-setup, .bl-wallet-discovery { margin: 0; }

@media (max-width: 520px) {
  .bl-wallet-scrim { padding: 10px; align-items: end; }
  .bl-wallet-dialog { border-end-start-radius: 22px; border-end-end-radius: 22px; max-height: 88vh; }
}
</style>
