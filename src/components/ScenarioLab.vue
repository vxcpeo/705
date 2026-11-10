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
  link.download = `tallyria-${record.value.id.toLowerCase()}.json`
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
  <section ref="root" class="bl-page bl-lab" aria-labelledby="scenario-title">
    <div class="bl-bento bl-lab-grid">
      <section class="bl-tile bl-tile--tint bl-span-12 bl-lab-open">
        <div class="bl-lab-open-copy">
          <p class="bl-kicker"><FlaskConical :size="14" /> YOUR PRIVATE WORKSPACE</p>
          <h1 id="scenario-title" ref="heading" class="bl-display bl-lab-title" tabindex="-1">Local scenario lab<span>.</span></h1>
          <p class="bl-lead">Put a number behind your next idea. Enter a reference price, explore a hypothetical move, and keep your reasoning close.</p>
        </div>
        <div class="bl-lab-open-flags">
          <p v-if="storageNotice" class="bl-notice bl-notice--alert" role="alert">{{ storageNotice }}</p>
          <p v-if="feedback" class="bl-notice bl-notice--ok" role="status">{{ feedback }}</p>
        </div>
      </section>

      <form v-if="step === 'form'" class="bl-tile bl-lab-form bl-span-7" @submit.prevent="review">
        <div class="bl-lab-form-head">
          <div class="bl-lab-face"><span class="bl-lab-step">01 / INPUTS</span><h2 class="bl-h2">Set your assumption.</h2></div>
          <span class="bl-chip bl-chip--accent">LOCAL ONLY</span>
        </div>

        <div class="bl-lab-pair">
          <div class="bl-field">
            <label for="amount">Amount <span>{{ brand.asset }} units</span></label>
            <input id="amount" class="bl-input" v-model="amount" inputmode="decimal" :aria-invalid="Boolean(errors.amount)" :aria-describedby="errors.amount ? 'amount-error' : undefined" />
            <p v-if="errors.amount" id="amount-error" class="bl-lab-error">{{ errors.amount }}</p>
          </div>
          <div class="bl-field">
            <label for="base-price">Reference price <span>USD / {{ brand.asset }}</span></label>
            <input id="base-price" class="bl-input" v-model="basePrice" inputmode="decimal" :aria-invalid="Boolean(errors.basePrice)" :aria-describedby="errors.basePrice ? 'price-error' : undefined" />
            <p v-if="errors.basePrice" id="price-error" class="bl-lab-error">{{ errors.basePrice }}</p>
          </div>
        </div>

        <div class="bl-field">
          <label for="move">Hypothetical move <output>{{ movePct }}%</output></label>
          <input id="move" v-model="movePct" class="bl-range" type="range" min="-90" max="100" step="0.5" />
          <div class="bl-scale"><span>-90%</span><span>0</span><span>+100%</span></div>
        </div>

        <div class="bl-field">
          <label for="move-text">Exact percentage <span>%</span></label>
          <input id="move-text" class="bl-input" v-model="movePct" inputmode="decimal" :aria-invalid="Boolean(errors.movePct)" :aria-describedby="errors.movePct ? 'move-error' : undefined" />
          <p v-if="errors.movePct" id="move-error" class="bl-lab-error">{{ errors.movePct }}</p>
        </div>

        <div class="bl-field">
          <label for="note">Thesis note <span>OPTIONAL</span></label>
          <textarea id="note" class="bl-input bl-lab-textarea" v-model="note" :maxlength="MAX_NOTE_LENGTH" :aria-invalid="Boolean(errors.note)" :aria-describedby="errors.note ? 'note-error' : 'note-count'" placeholder="What would make this move plausible?"></textarea>
          <p v-if="errors.note" id="note-error" class="bl-lab-error">{{ errors.note }}</p>
          <p id="note-count" class="bl-lab-count">{{ remaining }} characters remaining</p>
        </div>

        <button class="bl-btn bl-btn--primary bl-btn--wide" type="submit">Review scenario <ArrowUpRight :size="17" /></button>
      </form>

      <div v-if="step === 'form'" class="bl-lab-quiet bl-tile bl-tile--plum bl-span-5">
        <span class="bl-lab-quiet-mark"><ShieldCheck :size="26" /></span>
        <span class="bl-lab-step bl-lab-step--light">A LITTLE SPACE TO THINK</span>
        <h2 class="bl-h2 bl-lab-quiet-title">Your idea.<br />Your assumptions.</h2>
        <p class="bl-lab-quiet-copy">This is a private what-if calculator. Reference prices are entered by you; they are not live quotes or execution prices.</p>
        <dl class="bl-lab-quiet-rows"><div><dt>Asset</dt><dd>{{ brand.asset }} / USD</dd></div><div><dt>Network</dt><dd>{{ brand.network }} - preview</dd></div><div><dt>Wallet</dt><dd>Not required</dd></div><div><dt>Storage</dt><dd>This browser only</dd></div></dl>
        <p class="bl-lab-quiet-foot">Fees, slippage and taxes are excluded. No transaction is created.</p>
      </div>

      <div v-else-if="step === 'review'" class="bl-tile bl-span-12 bl-lab-record">
        <div class="bl-lab-record-main">
          <div class="bl-lab-record-head">
            <div class="bl-lab-face"><span class="bl-lab-step">02 / REVIEW</span><h2 class="bl-h2">Check the numbers.</h2></div>
            <ShieldCheck :size="24" class="bl-lab-shield" />
          </div>
          <p class="bl-lab-muted">Calculated from your assumptions.</p>
          <dl class="bl-lab-rows"><div><dt>Reference amount</dt><dd>{{ Number(record.amount).toLocaleString() }} {{ brand.asset }}</dd></div><div><dt>Reference price</dt><dd>{{ currency(result.basePrice, 4) }}</dd></div><div><dt>Reference value</dt><dd>{{ currency(result.baselineValue, 4) }}</dd></div><div><dt>Scenario move</dt><dd :class="record.movePct >= 0 ? 'bl-pos' : 'bl-neg'">{{ percent(record.movePct) }}</dd></div><div><dt>Scenario value</dt><dd>{{ currency(result.scenarioValue, 4) }}</dd></div></dl>
        </div>
        <div class="bl-lab-record-side">
          <div class="bl-lab-delta"><span>Change in reference value</span><strong :class="result.deltaUsd >= 0 ? 'bl-pos' : 'bl-neg'">{{ result.deltaUsd >= 0 ? '+' : '' }}{{ currency(result.deltaUsd, 4) }}</strong></div>
          <div class="bl-lab-actions"><button class="bl-btn bl-btn--primary" @click="save">Save to journal <Check :size="17" /></button><button class="bl-btn" @click="edit">Edit inputs</button></div>
        </div>
      </div>

      <div v-else class="bl-tile bl-span-12 bl-lab-record">
        <div class="bl-lab-record-main">
          <div class="bl-lab-record-head">
            <div class="bl-lab-face"><span class="bl-lab-step">03 / JOURNAL</span><h2 class="bl-h2">Your local record.</h2></div>
            <span class="bl-lab-badge" :class="{ 'bl-lab-unsaved': !isSaved }"><Check v-if="isSaved" :size="13" />{{ isSaved ? 'SAVED' : 'NOT SAVED' }}</span>
          </div>
          <div class="bl-lab-stages" role="group" aria-label="Journal review stages"><button v-for="(label, i) in stages" :key="label" :class="{ 'stage-now': record.stage === i, 'stage-past': record.stage > i }" :aria-current="record.stage === i ? 'step' : undefined" @click="changeStage(i)"><span class="bl-lab-stage-num"><Check v-if="record.stage > i" :size="13" /><template v-else>{{ i + 1 }}</template></span><span>{{ label }}</span><ChevronRight v-if="i < stages.length - 1" class="bl-lab-stage-arrow" :size="14" /></button></div>
          <dl class="bl-lab-rows"><div><dt>Amount</dt><dd>{{ Number(record.amount).toLocaleString() }} {{ brand.asset }}</dd></div><div><dt>Reference price</dt><dd>{{ currency(record.basePrice, 4) }}</dd></div><div><dt>Move</dt><dd :class="record.movePct >= 0 ? 'bl-pos' : 'bl-neg'">{{ percent(record.movePct) }}</dd></div><div><dt>Scenario value</dt><dd>{{ currency(result.scenarioValue, 4) }}</dd></div></dl>
          <blockquote v-if="record.note">{{ record.note }}</blockquote><p class="bl-lab-muted">Created {{ new Date(record.createdAt).toLocaleString() }}. {{ isSaved ? 'Stored only in this browser.' : 'Export a copy to keep this record.' }}</p>
        </div>
        <div class="bl-lab-record-side">
          <div class="bl-lab-actions bl-lab-actions--stack"><button class="bl-btn bl-btn--primary" @click="downloadJournal">Export JSON <ArrowDownToLine :size="16" /></button><button v-if="!isSaved" class="bl-btn" @click="persist">Retry saving</button><button class="bl-btn" @click="edit">Edit</button><button class="bl-lab-delete" @click="removeJournal">Delete local record</button></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.bl-lab { gap: var(--bl-gap); }
.bl-lab-grid { align-items: start; }

/* ------------------------------------------------------------------ opening */
.bl-lab-open {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px 40px;
  flex-wrap: wrap;
}
.bl-lab-open-copy { display: grid; gap: 12px; max-width: 60ch; }
.bl-lab-title { font-size: clamp(34px, 4.2vw, 52px); }
.bl-lab-title span { color: var(--bl-accent); }
.bl-lab-open-flags { display: grid; gap: 8px; flex: 1 1 320px; }
.bl-lab-open-flags:empty { display: none; }

/* --------------------------------------------------------------------- form */
.bl-lab-form { gap: 16px; align-content: start; }
.bl-lab-form-head { display: flex; align-items: start; justify-content: space-between; gap: 14px; flex-wrap: wrap; }
.bl-lab-face { display: grid; gap: 7px; }
.bl-lab-step {
  display: block;
  color: var(--bl-accent-safe);
  font: 600 9.5px/1.4 var(--bl-font-mono);
  letter-spacing: .16em;
  text-transform: uppercase;
}
.bl-lab-step--light { color: var(--bl-accent-soft); }
.bl-lab-pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.bl-lab-error { color: var(--bl-bad); font: 400 11px/1.5 var(--bl-font-mono); }
.bl-lab-count { color: var(--bl-muted); font: 400 10px/1.5 var(--bl-font-mono); text-align: end; }
.bl-lab-textarea { min-height: 104px; resize: vertical; font-size: 13px; line-height: 1.6; }

/* --------------------------------------------------------------- quiet tile */
.bl-lab-quiet { gap: 12px; align-content: start; background: var(--bl-plum); border-color: var(--bl-plum-line); }
.bl-lab-quiet-mark {
  display: grid;
  place-items: center;
  width: 50px;
  height: 50px;
  border-radius: 18px;
  background: rgba(255, 255, 255, .1);
  color: var(--bl-accent-soft);
}
.bl-lab-quiet-title { color: var(--bl-plum-text); font-size: clamp(22px, 2.2vw, 29px); }
.bl-lab-quiet-copy { color: var(--bl-plum-text); font: 400 13px/1.7 var(--bl-font-body); opacity: .82; }
.bl-lab-quiet-rows { display: grid; }
.bl-lab-quiet-rows > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding-block: 10px;
  border-block-end: 1px solid var(--bl-plum-line);
}
.bl-lab-quiet-rows dt { color: var(--bl-plum-muted); font: 600 10px/1.5 var(--bl-font-mono); letter-spacing: .08em; text-transform: uppercase; }
.bl-lab-quiet-rows dd { color: var(--bl-plum-text); font: 600 12px/1.5 var(--bl-font-mono); }
.bl-lab-quiet-foot { color: var(--bl-plum-muted); font: 400 10px/1.7 var(--bl-font-mono); }

/* ------------------------------------------------------------------- record */
.bl-lab-record {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
  gap: 18px clamp(18px, 2.4vw, 34px);
  align-items: start;
}
.bl-lab-record-main { display: grid; gap: 14px; min-width: 0; }
.bl-lab-record-side { display: grid; gap: 14px; align-content: start; }
.bl-lab-record-head { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.bl-lab-shield { color: var(--bl-accent-safe); }
.bl-lab-muted { color: var(--bl-muted); font: 400 11px/1.7 var(--bl-font-mono); }
.bl-lab-rows { display: grid; }
.bl-lab-rows > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding-block: 11px;
  border-block-end: 1px solid var(--bl-line);
}
.bl-lab-rows > div:last-child { border-block-end: 0; }
.bl-lab-rows dt { color: var(--bl-muted); font: 600 10px/1.5 var(--bl-font-mono); letter-spacing: .08em; text-transform: uppercase; }
.bl-lab-rows dd { font: 600 13px/1.5 var(--bl-font-mono); }
.bl-pos { color: var(--bl-good); }
.bl-neg { color: var(--bl-bad); }
.bl-lab-delta {
  display: grid;
  gap: 8px;
  padding: 18px 20px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: linear-gradient(140deg, var(--bl-tint), var(--bl-paper) 70%);
}
.bl-lab-delta span { color: var(--bl-muted); font: 600 9.5px/1.4 var(--bl-font-mono); letter-spacing: .14em; text-transform: uppercase; }
.bl-lab-delta strong { font: var(--bl-display-weight) 30px/1 var(--bl-font-display); letter-spacing: -.03em; }
.bl-lab-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.bl-lab-actions--stack { display: grid; justify-items: start; }
.bl-lab-actions--stack .bl-btn { width: 100%; }
.bl-lab-delete {
  border: 0;
  border-block-end: 1px solid var(--bl-bad);
  padding: 0 0 3px;
  background: none;
  color: var(--bl-bad);
  font: 600 9.5px/1.6 var(--bl-font-mono);
  letter-spacing: .14em;
  text-transform: uppercase;
}
.bl-lab-delete:hover { color: var(--bl-ink); border-block-end-color: var(--bl-ink); }

/* ------------------------------------------------------------------- stages */
.bl-lab-stages { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px; }
.bl-lab-stages button {
  display: flex;
  align-items: center;
  gap: 9px;
  min-height: 54px;
  padding: 10px 13px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
  background: var(--bl-paper);
  color: var(--bl-muted);
  font: 600 9.5px/1.3 var(--bl-font-mono);
  letter-spacing: .08em;
  text-transform: uppercase;
  text-align: start;
  transition: background-color var(--bl-dur) var(--bl-ease), color var(--bl-dur) var(--bl-ease);
}
.bl-lab-stages button:hover { background: var(--bl-surface); color: var(--bl-ink); }
.bl-lab-stages button.stage-past { color: var(--bl-good); border-color: rgba(15, 123, 77, .3); }
.bl-lab-stages button.stage-now { background: var(--bl-accent-safe); border-color: var(--bl-accent-safe); color: #fff; }
.bl-lab-stage-num {
  display: grid;
  place-items: center;
  flex: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px currentColor;
  font: 600 10px/1 var(--bl-font-mono);
}
.bl-lab-stage-arrow { margin-inline-start: auto; opacity: .5; }
.bl-lab-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  flex: none;
  padding: 6px 12px;
  border-radius: var(--bl-radius-pill);
  background: rgba(15, 123, 77, .1);
  color: var(--bl-good);
  font: 600 9px/1 var(--bl-font-mono);
  letter-spacing: .14em;
  text-transform: uppercase;
  white-space: nowrap;
}
.bl-lab-unsaved { background: rgba(138, 90, 0, .12); color: var(--bl-warn); }
.bl-lab-record blockquote {
  padding: 15px 18px;
  border: 1px solid var(--bl-line);
  border-inline-start: 3px solid var(--bl-accent);
  border-radius: 0 var(--bl-r-sm) var(--bl-r-sm) 0;
  background: var(--bl-surface);
  color: var(--bl-ink-soft);
  font: 400 13px/1.75 var(--bl-font-body);
  white-space: pre-wrap;
}

@media (max-width: 1080px) {
  .bl-lab-record { grid-template-columns: minmax(0, 1fr); }
  .bl-lab-actions--stack { justify-items: stretch; }
}
@media (max-width: 640px) {
  .bl-lab-pair { grid-template-columns: minmax(0, 1fr); }
  .bl-lab-stages { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .bl-lab-stage-arrow { display: none; }
}
</style>
