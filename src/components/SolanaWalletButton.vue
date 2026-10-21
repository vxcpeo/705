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
  void nextTick(() => dialogPanel.value?.querySelector('.wal-close')?.focus())
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
      class="tty-btn wal-trigger"
      :class="{ 'linked': address }"
      :aria-haspopup="'dialog'"
      :aria-expanded="modalOpen"
      :disabled="Boolean(pendingWallet)"
      @click="showModal"
    >
      <Wallet :size="16" />
      {{ pendingWallet ? 'Connecting…' : buttonLabel }}
    </button>

    <Teleport to="body">
      <div v-if="modalOpen" class="wal-scrim" @click.self="closeModal" @keydown.esc.stop="closeModal">
        <section ref="dialogPanel" class="wal-dialog" role="dialog" aria-modal="true" aria-labelledby="wallet-dialog-title" tabindex="-1" @keydown.stop="onDialogKeydown">
          <header class="wal-head">
            <div class="wal-head-copy">
              <span class="wal-eyebrow">SOLANA / {{ solanaConfig.cluster.toUpperCase() }}</span>
              <h2 id="wallet-dialog-title" class="tty-h2 wal-title">{{ address ? 'Wallet connected' : 'Choose a wallet' }}</h2>
            </div>
            <button class="wal-close" type="button" aria-label="Close wallet dialog" @click="closeModal"><X :size="18" /></button>
          </header>

          <div class="wal-body">
            <div v-if="address" class="wal-account">
              <span class="wal-account-name"><Wallet :size="16" /> {{ activeWallet?.name || 'Solana wallet' }}</span>
              <code>{{ address }}</code>
              <button class="tty-btn tty-btn--ghost tty-btn--wide wal-disconnect" type="button" :disabled="Boolean(pendingWallet)" @click="disconnect">
                {{ pendingWallet ? 'Disconnecting…' : 'Disconnect wallet' }}
              </button>
            </div>

            <template v-else>
              <p class="wal-copy">Connect a Solana account to display its public address. This site does not ask for transaction signatures.</p>
              <p class="tty-notice tty-notice--ok wal-network"><ShieldCheck :size="15" /> Use a Solana wallet with an SPL account. The CA preview never asks for a seed phrase.</p>

              <p v-if="discovering" class="tty-notice wal-discovery" role="status">Looking for MetaMask, Phantom, Solflare and other Solana wallets…</p>
              <div v-else-if="wallets.length" class="wal-options" aria-label="Available Solana wallets">
                <button v-for="wallet in wallets" :key="wallet.name" class="wal-option" type="button" :disabled="Boolean(pendingWallet)" @click="connect(wallet)">
                  <img v-if="wallet.icon" class="wal-option-icon" :src="wallet.icon" alt="" />
                  <span v-else class="wal-option-icon wal-option-placeholder"><Wallet :size="18" /></span>
                  <span class="wal-option-name">{{ wallet.name }}</span>
                  <span v-if="pendingWallet === wallet.name" class="wal-option-state">Connecting…</span>
                  <ExternalLink v-else :size="15" class="wal-option-arrow" />
                </button>
              </div>
              <div v-else class="wal-empty">
                <p>No compatible Solana wallet was detected.</p>
                <p class="wal-empty-help">Install a wallet, enable its Solana account, then reopen this panel.</p>
                <div class="wal-install">
                  <a href="https://metamask.io/download/" target="_blank" rel="noreferrer">MetaMask <ExternalLink :size="12" /></a>
                  <a href="https://phantom.app/download" target="_blank" rel="noreferrer">Phantom <ExternalLink :size="12" /></a>
                  <a href="https://solflare.com/download" target="_blank" rel="noreferrer">Solflare <ExternalLink :size="12" /></a>
                </div>
              </div>
            </template>

            <p v-if="errorMessage" class="tty-notice tty-notice--alert wal-error" role="alert">{{ errorMessage }}</p>
            <p v-if="setupMessage" class="tty-notice tty-notice--flag wal-setup" role="status">MetaMask connector: {{ setupMessage }}</p>
            <p class="wal-foot">Only the selected wallet’s public Solana address is read.</p>
          </div>
        </section>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
/* ----------------------------------------------------------------- trigger */
.port { min-width: 0; }
.wal-trigger { box-shadow: none; }
.wal-trigger.linked {
  border-color: transparent;
  background: var(--accent);
  color: #050608;
  box-shadow: 0 0 24px rgba(255, 0, 0, 0.35);
}
.wal-trigger.linked:hover { background: #ff6b6b; border-color: transparent; }

/* ------------------------------------------------------------------- scrim */
.wal-scrim {
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
.wal-dialog {
  width: min(100%, 480px);
  max-height: min(760px, calc(100vh - 44px));
  overflow: auto;
  border: 1px solid var(--line-2);
  border-radius: var(--radius-lg);
  background: linear-gradient(180deg, var(--surface-2), var(--bg-2) 60%);
  box-shadow: 0 0 0 1px rgba(255, 0, 0, 0.08), 0 40px 90px rgba(0, 0, 0, 0.8), var(--glow);
  outline: 0;
}
.wal-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 22px 22px 18px;
  border-bottom: 1px solid var(--line);
}
.wal-head-copy { display: grid; gap: 9px; min-width: 0; }
.wal-eyebrow {
  display: block;
  color: var(--accent-safe);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.wal-title { font-size: clamp(22px, 2.4vw, 28px); }
.wal-close {
  display: grid;
  place-items: center;
  flex: none;
  width: 36px;
  height: 36px;
  border: 1px solid var(--line-2);
  border-radius: 50%;
  background: transparent;
  color: var(--ink);
  cursor: pointer;
  transition: color 160ms var(--ease), border-color 160ms var(--ease), background-color 160ms var(--ease);
}
.wal-close:hover { color: var(--accent-safe); border-color: var(--accent-safe); background: rgba(255, 0, 0, 0.12); }

.wal-body { display: grid; gap: 14px; padding: 20px 22px 22px; }
.wal-copy { margin: 0; color: var(--muted); font: 400 14px/1.7 var(--font-body); }
.wal-network { margin: 0; }

/* ------------------------------------------------------------------ wallets */
.wal-options { display: grid; gap: 8px; }
.wal-option {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 56px;
  padding: 9px 14px;
  border: 1px solid var(--line-2);
  border-radius: var(--radius-pill);
  background: rgba(10, 14, 20, 0.8);
  color: var(--ink);
  text-align: left;
  cursor: pointer;
  transition: border-color 160ms var(--ease), background-color 160ms var(--ease);
}
.wal-option:hover:not(:disabled) { border-color: var(--accent-safe); background: rgba(255, 0, 0, 0.1); }
.wal-option:disabled { opacity: 0.5; cursor: not-allowed; }
.wal-option-icon {
  display: grid;
  place-items: center;
  flex: none;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--surface-3);
  box-shadow: inset 0 0 0 1px var(--line-2);
}
img.wal-option-icon { object-fit: contain; padding: 5px; }
.wal-option-placeholder { color: var(--muted); }
.wal-option-name { flex: 1 1 auto; min-width: 0; font: 500 13px/1.3 var(--font-mono); }
.wal-option-state {
  color: var(--faint);
  font: 500 9px/1 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.wal-option-arrow { flex: none; color: var(--faint); }

/* ------------------------------------------------------------------ account */
.wal-account {
  display: grid;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: rgba(10, 14, 20, 0.8);
}
.wal-account-name {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: var(--ink-2);
  font: 500 10px/1 var(--font-mono);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.wal-account code {
  display: block;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  background: var(--bg-2);
  color: var(--ink);
  font: 400 12px/1.6 var(--font-mono);
  word-break: break-all;
}
.wal-disconnect { justify-self: start; }

/* -------------------------------------------------------------------- empty */
.wal-empty {
  display: grid;
  gap: 10px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: rgba(10, 14, 20, 0.8);
}
.wal-empty p { margin: 0; color: var(--ink-2); font: 400 13px/1.7 var(--font-body); }
.wal-empty-help { color: var(--muted) !important; font: 400 11px/1.7 var(--font-mono) !important; }
.wal-install { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
.wal-install a {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 13px;
  border: 1px solid var(--line-2);
  border-radius: var(--radius-pill);
  background: transparent;
  color: var(--ink-2);
  font: 500 9px/1 var(--font-mono);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  text-decoration: none;
  transition: color 160ms var(--ease), border-color 160ms var(--ease);
}
.wal-install a:hover { color: var(--accent-safe); border-color: var(--accent-safe); }

.wal-discovery { margin: 0; }
.wal-error { margin: 0; }
.wal-setup { margin: 0; }
.wal-foot {
  margin: 2px 0 0;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  color: var(--faint);
  font: 400 10px/1.8 var(--font-mono);
}

@media (max-width: 480px) {
  .wal-scrim { padding: 0; place-items: stretch; }
  .wal-dialog {
    width: 100%;
    max-height: 100vh;
    max-height: 100dvh;
    border: 0;
    border-radius: 0;
  }
}
</style>
