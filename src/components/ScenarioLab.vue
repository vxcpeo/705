<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { ArrowDownToLine, ArrowUpRight, Check, ChevronRight, FlaskConical, ShieldCheck } from 'lucide-vue-next'
import { brand, storageKeys } from '../brand.js'
import { DEFAULT_BASE_PRICE, MAX_NOTE_LENGTH, calculateScenario, createJournalRecord, restoreJournalRecord, validateScenarioInputs } from '../scenario.js'

defineProps({ wallet: { type: String, default: '' } })

const root = ref(null)
const heading = ref(null)
const amount = ref('1000')
const basePrice = ref(DEFAULT_BASE_PRICE)
const movePct = ref('-15')
const note = ref('')
const step = ref('form')
const record = ref(null)
const errors = ref({})
const feedback = ref('')
const storageNotice = ref('')
const isSaved = ref(false)
const stages = ['Inputs recorded', 'Assumption reviewed', 'Limits reviewed', 'Review complete']
const legacyJournalKeys = ['Ivorane:journal:v1', 'Tikriva:journal:v1', 'Orbinza:journal:v1', 'Kovrane:journal:v1', 'kinovra:journal:v1', 'Kinovra:journal:v1', 'Scenarill:journal:v1', 'Solenzi:journal:v1', 'Filza:journal:v1']
const input = computed(() => ({ amount: amount.value, basePrice: basePrice.value, movePct: movePct.value, note: note.value }))
const result = computed(() => record.value ? calculateScenario(record.value) : null)
const remaining = computed(() => MAX_NOTE_LENGTH - note.value.length)
const currency = (value, digits = 2) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: digits, maximumFractionDigits: digits }).format(value)
const percent = value => `${Number(value) > 0 ? '+' : ''}${Number(value).toFixed(2)}%`

async function focusHeading() {
  await nextTick()
  heading.value?.focus({ preventScroll: true })
}

function fillInputs(value) {
  amount.value = String(value.amount)
  basePrice.value = String(value.basePrice)
  movePct.value = String(value.movePct)
  note.value = value.note
}

async function review() {
  const validation = validateScenarioInputs(input.value)
  errors.value = validation.errors
  feedback.value = ''
  if (!validation.valid) {
    await nextTick()
    root.value?.querySelector('[aria-invalid="true"]')?.focus()
    return
  }
  record.value = createJournalRecord(validation.value, { id: `SC-${crypto.randomUUID()}`, createdAt: new Date().toISOString() })
  isSaved.value = false
  step.value = 'review'
  await focusHeading()
}

function persist() {
  if (!record.value) return false
  feedback.value = ''
  try {
    localStorage.setItem(storageKeys.journal, JSON.stringify(record.value))
    isSaved.value = true
    storageNotice.value = ''
    feedback.value = 'Saved locally on this device.'
    return true
  } catch {
    isSaved.value = false
    storageNotice.value = 'This record could not be saved to your browser. Export JSON to keep a copy, or retry saving.'
    return false
  }
}

async function save() {
  persist()
  step.value = 'journal'
  await focusHeading()
}

async function edit() {
  if (record.value) fillInputs(record.value)
  errors.value = {}
  feedback.value = ''
  step.value = 'form'
  await focusHeading()
}

async function removeJournal() {
  feedback.value = ''
  try {
    // Remove the older namespace too, so a deleted record cannot reappear on reload.
    legacyJournalKeys.forEach(key => localStorage.removeItem(key))
    localStorage.removeItem(storageKeys.journal)
  } catch {
    storageNotice.value = 'The browser could not delete your saved journal. Your current record is still available; try again or export a copy.'
    return
  }
  record.value = null
  isSaved.value = false
  step.value = 'form'
  amount.value = '1000'
  basePrice.value = DEFAULT_BASE_PRICE
  movePct.value = '-15'
  note.value = ''
  errors.value = {}
  storageNotice.value = ''
  feedback.value = 'Local journal removed.'
  await focusHeading()
}

function changeStage(stage) {
  if (!record.value) return
  record.value = { ...record.value, stage: Math.max(0, Math.min(3, stage)) }
  persist()
}

function downloadJournal() {
  if (!record.value) return
  const data = {
    ...record.value,
    calculations: result.value,
    disclaimer: 'User-entered price and move. Not a quote or forecast. This interface does not enable wallet transactions.',
  }
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }))
  const link = document.createElement('a')
  link.href = url
  link.download = `pretiola-${record.value.id.toLowerCase()}.json`
  link.click()
  URL.revokeObjectURL(url)
  feedback.value = 'Journal export prepared.'
}

onMounted(() => {
  try {
    const activeRaw = localStorage.getItem(storageKeys.journal)
    const legacyKey = legacyJournalKeys.find(key => localStorage.getItem(key))
    const legacyRaw = legacyKey ? localStorage.getItem(legacyKey) : null
    const raw = activeRaw || legacyRaw
    if (!raw) return
    const restored = restoreJournalRecord(JSON.parse(raw))
    if (!restored.valid) {
      storageNotice.value = 'The saved journal has an unsupported format. You can start a new scenario.'
      return
    }
    record.value = restored.value
    fillInputs(restored.value)
    step.value = 'journal'
    isSaved.value = true
    if (restored.migrated || legacyRaw) {
      if (persist()) feedback.value = 'Your earlier record is ready. Its original price is retained as your own assumption.'
    }
  } catch {
    storageNotice.value = 'Saved journal could not be restored. You can still calculate a scenario and export it.'
  }
})

defineExpose({ focusHeading })
</script>

<template>
  <section ref="root" class="lab" aria-labelledby="scenario-title">
    <section class="tty-scene log-open">
      <div class="tty-scene-in log-open-in">
        <p class="tty-kicker log-eyebrow"><FlaskConical :size="15" /> YOUR PRIVATE WORKSPACE</p>
        <h1 id="scenario-title" ref="heading" class="tty-display log-display" tabindex="-1">Local scenario lab<span>.</span></h1>
        <p class="tty-lead">Put a number behind your next idea. Enter a reference price, explore a hypothetical move, and keep your reasoning close.</p>
        <p v-if="storageNotice" class="tty-notice tty-notice--alert" role="alert">{{ storageNotice }}</p>
        <p v-if="feedback" class="tty-notice tty-notice--ok" role="status">{{ feedback }}</p>
      </div>
    </section>

    <div v-if="step === 'form'" class="tty-scene log-form-scene">
      <div class="tty-scene-in log-form-grid">
        <form class="tty-face log-form" @submit.prevent="review">
          <div class="tty-face-head">
            <div class="log-face-title"><span class="log-step">01 / INPUTS</span><h2 class="tty-h2">Set your assumption.</h2></div>
            <span class="tty-pill tty-pill--accent">LOCAL ONLY</span>
          </div>
          <div class="log-fields">
            <div class="log-pair">
            <div class="tty-field">
              <label for="amount">Amount <span>{{ brand.asset }} units</span></label>
              <input id="amount" class="tty-input" v-model="amount" inputmode="decimal" :aria-invalid="Boolean(errors.amount)" :aria-describedby="errors.amount ? 'amount-error' : undefined" />
              <p v-if="errors.amount" id="amount-error" class="log-error">{{ errors.amount }}</p>
            </div>
            <div class="tty-field">
              <label for="base-price">Reference price <span>USD / {{ brand.asset }}</span></label>
              <input id="base-price" class="tty-input" v-model="basePrice" inputmode="decimal" :aria-invalid="Boolean(errors.basePrice)" :aria-describedby="errors.basePrice ? 'price-error' : undefined" />
              <p v-if="errors.basePrice" id="price-error" class="log-error">{{ errors.basePrice }}</p>
            </div>
          </div>
          <div class="tty-field">
            <label for="move">Hypothetical move <output>{{ movePct }}%</output></label>
            <input id="move" v-model="movePct" class="tty-range log-range" type="range" min="-90" max="100" step="0.5" />
            <div class="tty-scale"><span>-90%</span><span>0</span><span>+100%</span></div>
          </div>
          <div class="tty-field">
            <label for="move-text">Exact percentage <span>%</span></label>
            <input id="move-text" class="tty-input" v-model="movePct" inputmode="decimal" :aria-invalid="Boolean(errors.movePct)" :aria-describedby="errors.movePct ? 'move-error' : undefined" />
            <p v-if="errors.movePct" id="move-error" class="log-error">{{ errors.movePct }}</p>
          </div>
          <div class="tty-field">
            <label for="note">Thesis note <span>OPTIONAL</span></label>
            <textarea id="note" class="tty-input" v-model="note" :maxlength="MAX_NOTE_LENGTH" :aria-invalid="Boolean(errors.note)" :aria-describedby="errors.note ? 'note-error' : 'note-count'" placeholder="What would make this move plausible?"></textarea>
            <p v-if="errors.note" id="note-error" class="log-error">{{ errors.note }}</p>
            <p id="note-count" class="log-count">{{ remaining }} characters remaining</p>
          </div>
          </div>
          <button class="tty-btn tty-btn--primary tty-btn--wide" type="submit">Review scenario <ArrowUpRight :size="17" /></button>
        </form>

        <div class="tty-face log-aside">
          <div class="log-aside-icon"><ShieldCheck :size="27" /></div>
          <span class="log-step">A LITTLE SPACE TO THINK</span>
          <h2 class="tty-h2 log-aside-title">Your idea.<br />Your assumptions.</h2>
          <p class="log-aside-copy">This is a private what-if calculator. Reference prices are entered by you; they are not live quotes or execution prices.</p>
          <dl class="tty-pairs log-aside-rows"><div><dt>Asset</dt><dd>{{ brand.asset }} / USD</dd></div><div><dt>Network</dt><dd>{{ brand.network }} - preview</dd></div><div><dt>Wallet</dt><dd>Not required</dd></div><div><dt>Storage</dt><dd>This browser only</dd></div></dl>
          <p class="log-aside-foot">Fees, slippage and taxes are excluded. No transaction is created.</p>
        </div>
      </div>
    </div>

    <div v-else-if="step === 'review'" class="tty-scene log-record-scene">
      <div class="tty-scene-in">
        <div class="tty-face log-record">
          <div class="tty-face-head">
            <div class="log-face-title"><span class="log-step">02 / REVIEW</span><h2 class="tty-h2">Check the numbers.</h2></div>
            <ShieldCheck :size="26" />
          </div>
          <p class="log-muted">Calculated from your assumptions.</p>
          <dl class="tty-pairs log-rows"><div><dt>Reference amount</dt><dd>{{ Number(record.amount).toLocaleString() }} {{ brand.asset }}</dd></div><div><dt>Reference price</dt><dd>{{ currency(result.basePrice, 4) }}</dd></div><div><dt>Reference value</dt><dd>{{ currency(result.baselineValue, 4) }}</dd></div><div><dt>Scenario move</dt><dd :class="record.movePct >= 0 ? 'log-positive' : 'log-negative'">{{ percent(record.movePct) }}</dd></div><div><dt>Scenario value</dt><dd>{{ currency(result.scenarioValue, 4) }}</dd></div></dl>
          <div class="log-delta"><span>Change in reference value</span><strong :class="result.deltaUsd >= 0 ? 'log-positive' : 'log-negative'">{{ result.deltaUsd >= 0 ? '+' : '' }}{{ currency(result.deltaUsd, 4) }}</strong></div>
          <div class="log-actions"><button class="tty-btn tty-btn--primary" @click="save">Save to journal <Check :size="17" /></button><button class="tty-btn tty-btn--ghost" @click="edit">Edit inputs</button></div>
        </div>
      </div>
    </div>

    <div v-else class="tty-scene log-record-scene">
      <div class="tty-scene-in">
        <div class="tty-face log-record">
          <div class="tty-face-head">
            <div class="log-face-title"><span class="log-step">03 / JOURNAL</span><h2 class="tty-h2">Your local record.</h2></div>
            <span class="log-badge" :class="{ 'log-unsaved': !isSaved }"><Check v-if="isSaved" :size="13" />{{ isSaved ? 'SAVED' : 'NOT SAVED' }}</span>
          </div>
          <div class="log-stages" role="group" aria-label="Journal review stages"><button v-for="(label, i) in stages" :key="label" :class="{ current: record.stage === i, done: record.stage > i }" :aria-current="record.stage === i ? 'step' : undefined" @click="changeStage(i)"><span class="log-stage-number"><Check v-if="record.stage > i" :size="13" /><template v-else>{{ i + 1 }}</template></span><span>{{ label }}</span><ChevronRight v-if="i < stages.length - 1" class="log-stage-arrow" :size="14" /></button></div>
          <dl class="tty-pairs log-rows"><div><dt>Amount</dt><dd>{{ Number(record.amount).toLocaleString() }} {{ brand.asset }}</dd></div><div><dt>Reference price</dt><dd>{{ currency(record.basePrice, 4) }}</dd></div><div><dt>Move</dt><dd :class="record.movePct >= 0 ? 'log-positive' : 'log-negative'">{{ percent(record.movePct) }}</dd></div><div><dt>Scenario value</dt><dd>{{ currency(result.scenarioValue, 4) }}</dd></div></dl>
          <blockquote v-if="record.note">{{ record.note }}</blockquote><p class="log-muted">Created {{ new Date(record.createdAt).toLocaleString() }}. {{ isSaved ? 'Stored only in this browser.' : 'Export a copy to keep this record.' }}</p>
          <div class="log-actions"><button class="tty-btn tty-btn--primary" @click="downloadJournal">Export JSON <ArrowDownToLine :size="16" /></button><button v-if="!isSaved" class="tty-btn tty-btn--ghost" @click="persist">Retry saving</button><button class="tty-btn tty-btn--ghost" @click="edit">Edit</button><button class="log-delete" @click="removeJournal">Delete local record</button></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* -------------------------------------------------------------------- open */
.log-open { padding-bottom: clamp(20px, 2.4vw, 32px); }
.log-open-in { display: grid; gap: clamp(12px, 1.6vw, 18px); max-width: 880px; }
.log-eyebrow { letter-spacing: 0.18em; }
.log-display { font-size: clamp(28px, 3.4vw, 46px); }
.log-display span { color: var(--accent-safe); }
.log-open-in .tty-notice { margin-top: 6px; }

/* -------------------------------------------------------------------- form */
.log-form-scene { padding-top: clamp(18px, 2vw, 28px); }
.log-form-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(0, 0.85fr);
  gap: clamp(16px, 2.2vw, 32px);
  align-items: start;
}
.log-form { display: grid; gap: 18px; }
.log-aside { display: grid; gap: 12px; align-content: start; }
.log-aside-title { font-size: clamp(22px, 2.2vw, 30px); }
.log-aside-copy { margin: 0; color: var(--muted); font: 400 13px/1.75 var(--font-body); }
.log-aside-icon {
  display: grid;
  place-items: center;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(255, 0, 0, 0.12);
  color: var(--accent-safe);
  box-shadow: inset 0 0 0 1px rgba(255, 0, 0, 0.36), 0 0 30px rgba(255, 0, 0, 0.2);
}
.log-aside-rows { border-top: 1px solid var(--line); }
.log-aside-foot {
  margin: 0;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  color: var(--faint);
  font: 400 10px/1.8 var(--font-mono);
}
.log-pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.log-fields { display: grid; gap: 16px; min-width: 0; }
.log-error { margin: 0; color: var(--rose); font: 400 11px/1.5 var(--font-mono); }
.log-count { margin: 0; color: var(--faint); font: 400 10px/1.5 var(--font-mono); text-align: right; }
.log-range { accent-color: var(--accent-safe); }
.log-step {
  display: block;
  color: var(--accent-safe);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.log-face-title { display: grid; gap: 8px; }
.log-face-title h2 { margin: 0; }

/* ------------------------------------------------------------------ record */
.log-record { display: grid; gap: 16px; max-width: 900px; margin-inline: auto; }
.log-muted { margin: 0; color: var(--faint); font: 400 11px/1.7 var(--font-mono); }
.log-rows { border-top: 1px solid var(--line); }
.log-positive { color: var(--mint); }
.log-negative { color: var(--rose); }
.log-delta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding: 18px 20px;
  border-radius: var(--radius-md);
  background: linear-gradient(140deg, rgba(255, 0, 0, 0.12), rgba(255, 0, 200, 0.06));
  box-shadow: inset 0 0 0 1px var(--line-2);
}
.log-delta span {
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.log-delta strong { font: 400 30px/1 var(--font-display); letter-spacing: -0.02em; }
.log-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.log-delete {
  border: 0;
  border-bottom: 1px solid var(--rose);
  padding: 0 0 3px;
  background: none;
  color: var(--rose);
  font: 500 9px/1.6 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  cursor: pointer;
}
.log-delete:hover { color: var(--ink); border-bottom-color: var(--ink); }

/* ------------------------------------------------------------------ stages */
.log-stages {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--line);
  overflow: hidden;
}
.log-stages button {
  display: flex;
  align-items: center;
  gap: 9px;
  min-height: 54px;
  padding: 10px 14px;
  border: 0;
  background: var(--bg-2);
  color: var(--faint);
  font: 500 9px/1.3 var(--font-mono);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  text-align: left;
  cursor: pointer;
  transition: background-color 160ms var(--ease), color 160ms var(--ease);
}
.log-stages button:hover { background: var(--surface-2); color: var(--ink); }
.log-stages button.done { color: var(--mint); }
.log-stages button.current { background: rgba(255, 0, 0, 0.16); color: var(--accent-safe); }
.log-stage-number {
  display: grid;
  place-items: center;
  flex: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px currentColor;
  font: 500 10px/1 var(--font-mono);
}
.log-stage-arrow { margin-left: auto; opacity: 0.55; }
.log-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  flex: none;
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  background: rgba(92, 225, 160, 0.12);
  color: var(--mint);
  font: 500 9px/1 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  white-space: nowrap;
}
.log-unsaved { background: rgba(242, 201, 76, 0.12); color: var(--amber); }
.log-record blockquote {
  margin: 0;
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-left: 2px solid var(--accent);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  background: var(--bg-2);
  color: var(--ink-2);
  font: 400 13px/1.75 var(--font-body);
  white-space: pre-wrap;
}

/* -------------------------------------------------------------- responsive */
@media (max-width: 1000px) {
  .log-form-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 640px) {
  .log-pair { grid-template-columns: minmax(0, 1fr); }
  .log-stages { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .log-stage-arrow { display: none; }
}
</style>
