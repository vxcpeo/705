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
const legacyJournalKeys = ['Ivorane:journal:v1', 'Tikriva:journal:v1', 'Orbinza:journal:v1', 'Kovrane:journal:v1', 'kinovra:journal:v1', 'Kinovra:journal:v1', 'Scenarill:journal:v1', 'Solenzi:journal:v1', 'Filza:journal:v1', 'Pretiola:journal:v1']
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
  link.download = `librova-${record.value.id.toLowerCase()}.json`
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
  <section ref="root" class="lagoon" aria-labelledby="scenario-title">
    <section class="tide-band tide-band--first lagoon-open">
      <p class="tide-kicker"><FlaskConical :size="14" /> YOUR PRIVATE WORKSPACE</p>
      <h1 id="scenario-title" ref="heading" class="tide-display lagoon-display" tabindex="-1">Local scenario lab<span>.</span></h1>
      <p class="tide-lead">Put a number behind your next idea. Enter a reference price, explore a hypothetical move, and keep your reasoning close.</p>
      <p v-if="storageNotice" class="tide-notice tide-notice--alert" role="alert">{{ storageNotice }}</p>
      <p v-if="feedback" class="tide-notice tide-notice--ok" role="status">{{ feedback }}</p>
    </section>

    <div v-if="step === 'form'" class="tide-band lagoon-form-band">
      <div class="lagoon-form-grid">
        <form class="lagoon-form" @submit.prevent="review">
          <div class="lagoon-form-head">
            <div class="lagoon-face-title"><span class="lagoon-step">01 / INPUTS</span><h2 class="tide-h2">Set your assumption.</h2></div>
            <span class="tide-pill tide-pill--accent">LOCAL ONLY</span>
          </div>
          <div class="lagoon-fields">
            <div class="lagoon-pair">
            <div class="tide-field">
              <label for="amount">Amount <span>{{ brand.asset }} units</span></label>
              <input id="amount" class="tide-input" v-model="amount" inputmode="decimal" :aria-invalid="Boolean(errors.amount)" :aria-describedby="errors.amount ? 'amount-error' : undefined" />
              <p v-if="errors.amount" id="amount-error" class="lagoon-error">{{ errors.amount }}</p>
            </div>
            <div class="tide-field">
              <label for="base-price">Reference price <span>USD / {{ brand.asset }}</span></label>
              <input id="base-price" class="tide-input" v-model="basePrice" inputmode="decimal" :aria-invalid="Boolean(errors.basePrice)" :aria-describedby="errors.basePrice ? 'price-error' : undefined" />
              <p v-if="errors.basePrice" id="price-error" class="lagoon-error">{{ errors.basePrice }}</p>
            </div>
          </div>
          <div class="tide-field">
            <label for="move">Hypothetical move <output>{{ movePct }}%</output></label>
            <input id="move" v-model="movePct" class="tide-range" type="range" min="-90" max="100" step="0.5" />
            <div class="tide-scale"><span>-90%</span><span>0</span><span>+100%</span></div>
          </div>
          <div class="tide-field">
            <label for="move-text">Exact percentage <span>%</span></label>
            <input id="move-text" class="tide-input" v-model="movePct" inputmode="decimal" :aria-invalid="Boolean(errors.movePct)" :aria-describedby="errors.movePct ? 'move-error' : undefined" />
            <p v-if="errors.movePct" id="move-error" class="lagoon-error">{{ errors.movePct }}</p>
          </div>
          <div class="tide-field">
            <label for="note">Thesis note <span>OPTIONAL</span></label>
            <textarea id="note" class="tide-input" v-model="note" :maxlength="MAX_NOTE_LENGTH" :aria-invalid="Boolean(errors.note)" :aria-describedby="errors.note ? 'note-error' : 'note-count'" placeholder="What would make this move plausible?"></textarea>
            <p v-if="errors.note" id="note-error" class="lagoon-error">{{ errors.note }}</p>
            <p id="note-count" class="lagoon-count">{{ remaining }} characters remaining</p>
          </div>
          </div>
          <button class="tide-btn tide-btn--primary tide-btn--wide" type="submit">Review scenario <ArrowUpRight :size="17" /></button>
        </form>

        <div class="lagoon-aside">
          <div class="lagoon-aside-icon"><ShieldCheck :size="26" /></div>
          <span class="lagoon-step">A LITTLE SPACE TO THINK</span>
          <h2 class="tide-h2 lagoon-aside-title">Your idea.<br />Your assumptions.</h2>
          <p class="lagoon-aside-copy">This is a private what-if calculator. Reference prices are entered by you; they are not live quotes or execution prices.</p>
          <dl class="lagoon-aside-rows"><div><dt>Asset</dt><dd>{{ brand.asset }} / USD</dd></div><div><dt>Network</dt><dd>{{ brand.network }} - preview</dd></div><div><dt>Wallet</dt><dd>Not required</dd></div><div><dt>Storage</dt><dd>This browser only</dd></div></dl>
          <p class="lagoon-aside-foot">Fees, slippage and taxes are excluded. No transaction is created.</p>
        </div>
      </div>
    </div>

    <div v-else-if="step === 'review'" class="tide-band lagoon-record-band">
      <div class="lagoon-record">
        <div class="lagoon-record-head">
          <div class="lagoon-face-title"><span class="lagoon-step">02 / REVIEW</span><h2 class="tide-h2">Check the numbers.</h2></div>
          <ShieldCheck :size="24" />
        </div>
        <p class="lagoon-muted">Calculated from your assumptions.</p>
        <dl class="lagoon-rows"><div><dt>Reference amount</dt><dd>{{ Number(record.amount).toLocaleString() }} {{ brand.asset }}</dd></div><div><dt>Reference price</dt><dd>{{ currency(result.basePrice, 4) }}</dd></div><div><dt>Reference value</dt><dd>{{ currency(result.baselineValue, 4) }}</dd></div><div><dt>Scenario move</dt><dd :class="record.movePct >= 0 ? 'lagoon-positive' : 'lagoon-negative'">{{ percent(record.movePct) }}</dd></div><div><dt>Scenario value</dt><dd>{{ currency(result.scenarioValue, 4) }}</dd></div></dl>
        <div class="lagoon-delta"><span>Change in reference value</span><strong :class="result.deltaUsd >= 0 ? 'lagoon-positive' : 'lagoon-negative'">{{ result.deltaUsd >= 0 ? '+' : '' }}{{ currency(result.deltaUsd, 4) }}</strong></div>
        <div class="lagoon-actions"><button class="tide-btn tide-btn--primary" @click="save">Save to journal <Check :size="17" /></button><button class="tide-btn tide-btn--ghost" @click="edit">Edit inputs</button></div>
      </div>
    </div>

    <div v-else class="tide-band lagoon-record-band">
      <div class="lagoon-record">
        <div class="lagoon-record-head">
          <div class="lagoon-face-title"><span class="lagoon-step">03 / JOURNAL</span><h2 class="tide-h2">Your local record.</h2></div>
          <span class="lagoon-badge" :class="{ 'lagoon-unsaved': !isSaved }"><Check v-if="isSaved" :size="13" />{{ isSaved ? 'SAVED' : 'NOT SAVED' }}</span>
        </div>
        <div class="lagoon-stages" role="group" aria-label="Journal review stages"><button v-for="(label, i) in stages" :key="label" :class="{ current: record.stage === i, done: record.stage > i }" :aria-current="record.stage === i ? 'step' : undefined" @click="changeStage(i)"><span class="lagoon-stage-number"><Check v-if="record.stage > i" :size="13" /><template v-else>{{ i + 1 }}</template></span><span>{{ label }}</span><ChevronRight v-if="i < stages.length - 1" class="lagoon-stage-arrow" :size="14" /></button></div>
        <dl class="lagoon-rows"><div><dt>Amount</dt><dd>{{ Number(record.amount).toLocaleString() }} {{ brand.asset }}</dd></div><div><dt>Reference price</dt><dd>{{ currency(record.basePrice, 4) }}</dd></div><div><dt>Move</dt><dd :class="record.movePct >= 0 ? 'lagoon-positive' : 'lagoon-negative'">{{ percent(record.movePct) }}</dd></div><div><dt>Scenario value</dt><dd>{{ currency(result.scenarioValue, 4) }}</dd></div></dl>
        <blockquote v-if="record.note">{{ record.note }}</blockquote><p class="lagoon-muted">Created {{ new Date(record.createdAt).toLocaleString() }}. {{ isSaved ? 'Stored only in this browser.' : 'Export a copy to keep this record.' }}</p>
        <div class="lagoon-actions"><button class="tide-btn tide-btn--primary" @click="downloadJournal">Export JSON <ArrowDownToLine :size="16" /></button><button v-if="!isSaved" class="tide-btn tide-btn--ghost" @click="persist">Retry saving</button><button class="tide-btn tide-btn--ghost" @click="edit">Edit</button><button class="lagoon-delete" @click="removeJournal">Delete local record</button></div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* ---------------------------------------------------------------- opening */
.lagoon { display: grid; grid-template-columns: minmax(0, 1fr); }
.lagoon > * { min-width: 0; }
.lagoon-open {
  display: grid;
  gap: 12px;
  max-width: 780px;
  padding-block-end: clamp(20px, 2.6vw, 32px);
}
.lagoon-display { font-size: clamp(32px, 4.6vw, 54px); }
.lagoon-display span { color: var(--accent-deep); }
.lagoon-open .tide-notice { margin-block-start: 6px; }
.lagoon-form-band { padding-block-start: clamp(10px, 1.4vw, 16px); }
.lagoon-form-grid {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
  gap: clamp(18px, 2.6vw, 34px);
  align-items: start;
}

/* ------------------------------------------------------------------- form */
.lagoon-form {
  display: grid;
  gap: 18px;
  padding: clamp(18px, 2.4vw, 28px);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface);
  box-shadow: var(--shadow-soft);
}
.lagoon-form-head { display: flex; align-items: start; justify-content: space-between; gap: 14px; flex-wrap: wrap; }
.lagoon-face-title { display: grid; gap: 8px; }
.lagoon-step {
  display: block;
  color: var(--accent-deep);
  font: 600 9px/1.4 var(--font-mono);
  letter-spacing: .2em;
  text-transform: uppercase;
}
.lagoon-fields { display: grid; gap: 16px; min-width: 0; }
.lagoon-pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.lagoon-error { color: var(--danger); font: 400 11px/1.5 var(--font-mono); }
.lagoon-count { color: var(--muted); font: 400 10px/1.5 var(--font-mono); text-align: end; }
.lagoon-form textarea.tide-input { min-height: 104px; resize: vertical; font-family: var(--font-body); font-size: 13px; line-height: 1.6; }

/* ------------------------------------------------------------------ aside */
.lagoon-aside {
  display: grid;
  gap: 12px;
  align-content: start;
  padding: clamp(18px, 2.4vw, 26px);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background:
    radial-gradient(420px 220px at 100% 0%, rgba(41, 141, 255, .16), transparent 70%),
    var(--surface-soft);
}
.lagoon-aside-icon {
  display: grid;
  place-items: center;
  width: 52px;
  height: 52px;
  border-radius: 18px;
  background: var(--surface);
  color: var(--accent-safe);
  box-shadow: inset 0 0 0 1px var(--line), 0 10px 24px rgba(30, 111, 217, .12);
}
.lagoon-aside-title { font-size: clamp(22px, 2.2vw, 30px); }
.lagoon-aside-copy { color: var(--ink-soft); font: 400 13px/1.7 var(--font-body); }
.lagoon-aside-rows { display: grid; border-block-start: 1px solid var(--line); }
.lagoon-aside-rows > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block: 10px;
  border-block-end: 1px solid var(--line);
}
.lagoon-aside-rows dt { color: var(--muted); font: 500 10px/1.5 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; }
.lagoon-aside-rows dd { font: 600 12px/1.5 var(--font-mono); }
.lagoon-aside-foot { color: var(--muted); font: 400 10px/1.7 var(--font-mono); }

/* ----------------------------------------------------------------- record */
.lagoon-record-band { padding-block-start: clamp(10px, 1.4vw, 16px); }
.lagoon-record {
  display: grid;
  gap: 16px;
  max-width: 860px;
  padding: clamp(18px, 2.6vw, 30px);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  background:
    radial-gradient(560px 280px at 100% 0%, rgba(41, 141, 255, .1), transparent 70%),
    var(--surface);
  box-shadow: var(--shadow);
}
.lagoon-record-head { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.lagoon-record-head svg { color: var(--accent-safe); }
.lagoon-muted { color: var(--muted); font: 400 11px/1.7 var(--font-mono); }
.lagoon-rows { display: grid; border-block-start: 1px solid var(--line); }
.lagoon-rows > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding-block: 11px;
  border-block-end: 1px solid var(--line);
}
.lagoon-rows dt { color: var(--muted); font: 500 10px/1.5 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; }
.lagoon-rows dd { font: 600 13px/1.5 var(--font-mono); }
.lagoon-positive { color: var(--success); }
.lagoon-negative { color: var(--danger); }
.lagoon-delta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding: 18px 20px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: linear-gradient(120deg, rgba(41, 141, 255, .12), rgba(41, 141, 255, .03));
}
.lagoon-delta span { color: var(--muted); font: 600 9px/1.4 var(--font-mono); letter-spacing: .18em; text-transform: uppercase; }
.lagoon-delta strong { font: 600 30px/1 var(--font-display); letter-spacing: -.03em; }
.lagoon-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.lagoon-delete {
  border: 0;
  border-block-end: 1px solid var(--danger);
  padding: 0 0 3px;
  background: none;
  color: var(--danger);
  font: 600 9px/1.6 var(--font-mono);
  letter-spacing: .18em;
  text-transform: uppercase;
}
.lagoon-delete:hover { color: var(--ink); border-block-end-color: var(--ink); }

/* ----------------------------------------------------------------- stages */
.lagoon-stages {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--line);
  overflow: hidden;
}
.lagoon-stages button {
  display: flex;
  align-items: center;
  gap: 9px;
  min-height: 52px;
  padding: 10px 14px;
  border: 0;
  background: var(--surface);
  color: var(--muted);
  font: 600 9px/1.3 var(--font-mono);
  letter-spacing: .1em;
  text-transform: uppercase;
  text-align: start;
  transition: background-color var(--motion-duration) var(--motion-ease), color var(--motion-duration) var(--motion-ease);
}
.lagoon-stages button:hover { background: var(--surface-alt); color: var(--ink); }
.lagoon-stages button.done { color: var(--success); }
.lagoon-stages button.current { background: #e3f0ff; color: var(--accent-deep); }
.lagoon-stage-number {
  display: grid;
  place-items: center;
  flex: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px currentColor;
  font: 600 10px/1 var(--font-mono);
}
.lagoon-stage-arrow { margin-inline-start: auto; opacity: .5; }
.lagoon-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  flex: none;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(8, 122, 85, .1);
  color: var(--success);
  font: 600 9px/1 var(--font-mono);
  letter-spacing: .16em;
  text-transform: uppercase;
  white-space: nowrap;
}
.lagoon-unsaved { background: rgba(138, 90, 0, .1); color: var(--warning); }
.lagoon-record blockquote {
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-inline-start: 3px solid var(--accent);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  background: var(--surface-soft);
  color: var(--ink-soft);
  font: 400 13px/1.75 var(--font-body);
  white-space: pre-wrap;
}

/* -------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .lagoon-form-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 640px) {
  .lagoon-pair { grid-template-columns: minmax(0, 1fr); }
  .lagoon-stages { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .lagoon-stage-arrow { display: none; }
}
</style>
