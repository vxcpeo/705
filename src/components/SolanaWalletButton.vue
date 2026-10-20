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
  void nextTick(() => dialogPanel.value?.querySelector('.port-close')?.focus())
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
  <div class="port">
    <button
      type="button"
      class="atlas-btn port-trigger"
      :class="{ 'is-linked': address }"
      :aria-haspopup="'dialog'"
      :aria-expanded="modalOpen"
      :disabled="Boolean(pendingWallet)"
      @click="showModal"
    >
      <Wallet :size="16" />
      {{ pendingWallet ? 'Connecting…' : buttonLabel }}
    </button>

    <Teleport to="body">
      <div v-if="modalOpen" class="port-scrim" @click.self="closeModal" @keydown.esc.stop="closeModal">
        <section ref="dialogPanel" class="port-dialog" role="dialog" aria-modal="true" aria-labelledby="wallet-dialog-title" tabindex="-1" @keydown.stop="onDialogKeydown">
          <header class="port-head">
            <div class="port-head-copy">
              <span class="port-eyebrow">SOLANA / {{ solanaConfig.cluster.toUpperCase() }}</span>
              <h2 id="wallet-dialog-title" class="atlas-h2 port-title">{{ address ? 'Wallet connected' : 'Choose a wallet' }}</h2>
            </div>
            <button class="port-close" type="button" aria-label="Close wallet dialog" @click="closeModal"><X :size="18" /></button>
          </header>

          <div class="port-body">
            <div v-if="address" class="port-account">
              <span class="port-account-name"><Wallet :size="16" /> {{ activeWallet?.name || 'Solana wallet' }}</span>
              <code>{{ address }}</code>
              <button class="atlas-btn atlas-btn--ghost atlas-btn--wide port-disconnect" type="button" :disabled="Boolean(pendingWallet)" @click="disconnect">
                {{ pendingWallet ? 'Disconnecting…' : 'Disconnect wallet' }}
              </button>
            </div>

            <template v-else>
              <p class="port-copy">Connect a Solana account to display its public address. This site does not ask for transaction signatures.</p>
              <p class="atlas-notice atlas-notice--ok port-network"><ShieldCheck :size="15" /> Use a Solana wallet with an SPL account. The CA preview never asks for a seed phrase.</p>

              <p v-if="discovering" class="atlas-notice port-discovery" role="status">Looking for MetaMask, Phantom, Solflare and other Solana wallets…</p>
              <div v-else-if="wallets.length" class="port-options" aria-label="Available Solana wallets">
                <button v-for="wallet in wallets" :key="wallet.name" class="port-option" type="button" :disabled="Boolean(pendingWallet)" @click="connect(wallet)">
                  <img v-if="wallet.icon" class="port-option-icon" :src="wallet.icon" alt="" />
                  <span v-else class="port-option-icon port-option-placeholder"><Wallet :size="18" /></span>
                  <span class="port-option-name">{{ wallet.name }}</span>
                  <span v-if="pendingWallet === wallet.name" class="port-option-state">Connecting…</span>
                  <ExternalLink v-else :size="15" class="port-option-arrow" />
                </button>
              </div>
              <div v-else class="port-empty">
                <p>No compatible Solana wallet was detected.</p>
                <p class="port-empty-help">Install a wallet, enable its Solana account, then reopen this panel.</p>
                <div class="port-install">
                  <a href="https://metamask.io/download/" target="_blank" rel="noreferrer">MetaMask <ExternalLink :size="12" /></a>
                  <a href="https://phantom.app/download" target="_blank" rel="noreferrer">Phantom <ExternalLink :size="12" /></a>
                  <a href="https://solflare.com/download" target="_blank" rel="noreferrer">Solflare <ExternalLink :size="12" /></a>
                </div>
              </div>
            </template>

            <p v-if="errorMessage" class="atlas-notice atlas-notice--alert port-error" role="alert">{{ errorMessage }}</p>
            <p v-if="setupMessage" class="atlas-notice atlas-notice--flag port-setup" role="status">MetaMask connector: {{ setupMessage }}</p>
            <p class="port-foot">Only the selected wallet’s public Solana address is read.</p>
          </div>
        </section>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
/* ----------------------------------------------------------------- trigger */
.port { min-width: 0; }
.port-trigger { box-shadow: none; }
.port-trigger.is-linked {
  border-color: transparent;
  background: var(--beam);
  color: #04060d;
  box-shadow: 0 0 24px rgba(64, 179, 255, 0.35);
}
.port-trigger.is-linked:hover { background: #6bc4ff; border-color: transparent; }

/* ------------------------------------------------------------------- scrim */
.port-scrim {
  position: fixed;
  inset: 0;
  z-index: 120;
  display: grid;
  place-items: center;
  padding: 22px;
  background: rgba(3, 4, 10, 0.78);
  backdrop-filter: blur(10px);
}

/* ------------------------------------------------------------------ dialog */
.port-dialog {
  width: min(100%, 480px);
  max-height: min(760px, calc(100vh - 44px));
  overflow: auto;
  border: 1px solid var(--hair-2);
  border-radius: var(--r-lg);
  background: linear-gradient(180deg, var(--deck-2), var(--void-2) 60%);
  box-shadow: 0 0 0 1px rgba(64, 179, 255, 0.08), 0 40px 90px rgba(0, 0, 0, 0.8), var(--glow);
  outline: 0;
}
.port-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 22px 22px 18px;
  border-bottom: 1px solid var(--hair);
}
.port-head-copy { display: grid; gap: 9px; min-width: 0; }
.port-eyebrow {
  display: block;
  color: var(--beam);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.port-title { font-size: clamp(22px, 2.4vw, 28px); }
.port-close {
  display: grid;
  place-items: center;
  flex: none;
  width: 36px;
  height: 36px;
  border: 1px solid var(--hair-2);
  border-radius: 50%;
  background: transparent;
  color: var(--star);
  cursor: pointer;
  transition: color 160ms var(--ease), border-color 160ms var(--ease), background-color 160ms var(--ease);
}
.port-close:hover { color: var(--beam); border-color: var(--beam); background: rgba(64, 179, 255, 0.12); }

.port-body { display: grid; gap: 14px; padding: 20px 22px 22px; }
.port-copy { margin: 0; color: var(--star-mute); font: 400 14px/1.7 var(--font-body); }
.port-network { margin: 0; }

/* ------------------------------------------------------------------ wallets */
.port-options { display: grid; gap: 8px; }
.port-option {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 56px;
  padding: 9px 14px;
  border: 1px solid var(--hair-2);
  border-radius: var(--r-pill);
  background: rgba(11, 12, 21, 0.8);
  color: var(--star);
  text-align: left;
  cursor: pointer;
  transition: border-color 160ms var(--ease), background-color 160ms var(--ease);
}
.port-option:hover:not(:disabled) { border-color: var(--beam); background: rgba(64, 179, 255, 0.1); }
.port-option:disabled { opacity: 0.5; cursor: not-allowed; }
.port-option-icon {
  display: grid;
  place-items: center;
  flex: none;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--deck-3);
  box-shadow: inset 0 0 0 1px var(--hair-2);
}
img.port-option-icon { object-fit: contain; padding: 5px; }
.port-option-placeholder { color: var(--star-mute); }
.port-option-name { flex: 1 1 auto; min-width: 0; font: 500 13px/1.3 var(--font-mono); }
.port-option-state {
  color: var(--star-faint);
  font: 500 9px/1 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.port-option-arrow { flex: none; color: var(--star-faint); }

/* ------------------------------------------------------------------ account */
.port-account {
  display: grid;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  background: rgba(11, 12, 21, 0.8);
}
.port-account-name {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: var(--star-2);
  font: 500 10px/1 var(--font-mono);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.port-account code {
  display: block;
  padding: 10px 12px;
  border-radius: var(--r-sm);
  background: var(--void-2);
  color: var(--star);
  font: 400 12px/1.6 var(--font-mono);
  word-break: break-all;
}
.port-disconnect { justify-self: start; }

/* -------------------------------------------------------------------- empty */
.port-empty {
  display: grid;
  gap: 10px;
  padding: 16px;
  border: 1px solid var(--hair);
  border-radius: var(--r-md);
  background: rgba(11, 12, 21, 0.8);
}
.port-empty p { margin: 0; color: var(--star-2); font: 400 13px/1.7 var(--font-body); }
.port-empty-help { color: var(--star-mute) !important; font: 400 11px/1.7 var(--font-mono) !important; }
.port-install { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
.port-install a {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 13px;
  border: 1px solid var(--hair-2);
  border-radius: var(--r-pill);
  background: transparent;
  color: var(--star-2);
  font: 500 9px/1 var(--font-mono);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  text-decoration: none;
  transition: color 160ms var(--ease), border-color 160ms var(--ease);
}
.port-install a:hover { color: var(--beam); border-color: var(--beam); }

.port-discovery { margin: 0; }
.port-error { margin: 0; }
.port-setup { margin: 0; }
.port-foot {
  margin: 2px 0 0;
  padding-top: 14px;
  border-top: 1px solid var(--hair);
  color: var(--star-faint);
  font: 400 10px/1.8 var(--font-mono);
}

@media (max-width: 480px) {
  .port-scrim { padding: 0; place-items: stretch; }
  .port-dialog {
    width: 100%;
    max-height: 100vh;
    max-height: 100dvh;
    border: 0;
    border-radius: 0;
  }
}
</style>
