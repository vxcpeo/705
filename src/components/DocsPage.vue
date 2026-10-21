<script setup>
import { computed } from 'vue'
import { ArrowRight, ExternalLink } from 'lucide-vue-next'
import { concepts } from '../concepts.js'
import { brand } from '../brand.js'

const props = defineProps({
  path: { type: String, default: '/docs' },
})
const emit = defineEmits(['navigate'])

const sections = [
  ['mechanism', 'Mechanism'],
  ['concepts', 'Concepts'],
  ['settlement', 'Settlement'],
  ['oracle', 'Oracle'],
  ['fees', 'Fees'],
  ['listing', 'Listing'],
  ['risks', 'Risks'],
  ['token', 'Token'],
  ['documents', 'Journal'],
  ['terms', 'Terms'],
  ['privacy', 'Privacy'],
]

const steps = [
  ['01', 'Choose a market unit', 'Select an SPL asset from the watchlist. Prices in this build are illustrative examples.'],
  ['02', 'Set a cap', 'The model pairs an Income position with an Upside position around cap price K.'],
  ['03', 'Price the scenario', 'Auction and premium mechanics are part of the reference design; no auction runs here.'],
  ['04', 'Review settlement', 'Change the assumed settlement price to see how the modeled value splits at K.'],
  ['05', 'Recompose the pair', 'The design describes matching positions recombining into one market unit. This action is not implemented.'],
]

const legalPage = computed(() => ['/risk', '/terms', '/privacy'].includes(props.path))
const legalTitle = computed(() => ({ '/risk': 'Risk notice.', '/terms': 'Terms of this demo.', '/privacy': 'Privacy notice.' }[props.path] || ''))
const legalBody = computed(() => ({
  '/risk': [
    'This local interface is an educational scenario lab. It does not create, sell, or settle a financial product.',
    'Income positions retain downside exposure to the underlying SPL market unit. Upside can expire without a payoff and its maximum modeled loss is the premium paid. Verify the underlying, oracle, liquidity, and legal status independently before relying on any model output.',
  ],
  '/terms': [
    'This website is a local product demonstration. Prices, markets, wallets, and contract references are illustrative unless a connected production integration says otherwise.',
    `Use of this demo does not create an account, custody relationship, order, or agreement with ${brand.name}. Contract references and the scenario lab are read-only in this build.`,
  ],
  '/privacy': [
    'The demo keeps journal state in your browser. You can read the pages without connecting a wallet, and this interface does not send a trade order.',
    'External links, such as the chart provider or X, are governed by their own policies. Do not enter secrets, seed phrases, or private keys into this local demo.',
  ],
}[props.path] || []))

function go(to) { emit('navigate', to) }
</script>

<template>
  <div class="strand">
    <section v-if="legalPage" class="tide-band tide-band--first strand-open">
      <p class="tide-kicker">Local interface preview</p>
      <h1 class="tide-display strand-display" tabindex="-1">{{ legalTitle }}</h1>
      <p class="tide-lead">This page describes how this local product demonstration should be read. It is not a production protocol policy, legal agreement, or investment recommendation.</p>
    </section>

    <section v-if="legalPage" class="tide-band strand-legal">
      <div class="strand-legal-copy">
        <p v-for="paragraph in legalBody" :key="paragraph">{{ paragraph }}</p>
      </div>
      <div class="strand-legal-actions">
        <a class="tide-btn tide-btn--primary" href="/docs" @click.prevent="go('/docs')">Read how it works <ArrowRight :size="15" /></a>
        <a class="tide-btn tide-btn--ghost" href="/" @click.prevent="go('/')">Back to markets <ArrowRight :size="14" /></a>
      </div>
    </section>

    <template v-else>
      <section class="tide-band tide-band--first strand-open">
        <p class="tide-kicker">{{ brand.network }} / Model notes</p>
        <h1 class="tide-display strand-display" tabindex="-1">How {{ brand.name }} works.</h1>
        <p class="tide-lead">This preview models an illustrative split around a cap price. It does not custody SPL assets, run an auction, connect an oracle, or settle transactions.</p>
        <p class="tide-note strand-open-note">All displayed market values are examples. No token or Solana program has been issued by this preview.</p>
      </section>

      <div class="strand-doc">
        <nav class="strand-index" aria-label="On this page">
          <p class="strand-index-label">On this page</p>
          <div class="strand-index-rail">
            <a v-for="([id, label], index) in sections" :key="id" :href="`#${id}`"><b>{{ String(index + 1).padStart(2, '0') }}</b><span>{{ label }}</span></a>
          </div>
        </nav>

        <div class="strand-body">
          <div id="mechanism" class="strand-section">
            <p class="tide-kicker">Mechanism</p>
            <ol class="strand-steps">
              <li v-for="[number, title, body] in steps" :key="number">
                <span class="strand-step-number">{{ number }}</span>
                <div><h2 class="tide-h3">{{ title }}</h2><p>{{ body }}</p></div>
              </li>
            </ol>
            <div class="strand-roles">
              <article class="strand-role"><p class="strand-role-label strand-role-label--income">Income</p><h3 class="tide-h3">Value up to K, plus any premium.</h3><p>Income still bears the underlying asset's downside. A premium does not protect the market unit from a price decline.</p></article>
              <article class="strand-role"><p class="strand-role-label strand-role-label--upside">Upside</p><h3 class="tide-h3">Value above K.</h3><p>The modeled payoff is max(0, settlement price - K). A buyer's maximum modeled loss is the hypothetical premium paid.</p></article>
            </div>
          </div>

          <div id="concepts" class="strand-section">
            <div class="strand-section-head">
              <p class="tide-kicker">Concepts</p>
              <h2 class="tide-h2">Three parts of the model.</h2>
              <p class="strand-intro">These illustrations describe a product concept, not deployed Solana programs.</p>
            </div>
            <ul class="strand-cards">
              <li v-for="(concept, index) in concepts" :id="`concept-${concept.id}`" :key="concept.id" class="strand-card">
                <figure class="strand-figure">
                  <img :src="concept.image" :alt="concept.title" width="1200" height="750" loading="lazy" />
                  <figcaption>
                    <span class="strand-card-index">{{ String(index + 1).padStart(2, '0') }}</span>
                    <h3 class="tide-h3">{{ concept.title }}</h3>
                    <p>{{ concept.description }}</p>
                  </figcaption>
                </figure>
              </li>
            </ul>
          </div>

          <div id="settlement" class="strand-section strand-split">
            <div class="strand-split-copy">
              <p class="tide-kicker">Settlement</p>
              <h2 class="tide-h2">A defined cap sets the split.</h2>
              <p>For starting price P0 and cap rate c, K = P0 x (1 + c). At assumed settlement price S, Upside receives max(0, S - K). Income receives value up to K plus any hypothetical auction premium.</p>
            </div>
            <div class="strand-formula">
              <p class="strand-formula-label">Illustrative scenario</p>
              <strong>P0 $250 / 5% cap / K $262.50</strong>
              <dl class="strand-formula-cells"><div><dt>Settlement $200</dt><dd>Upside $0</dd></div><div><dt>Settlement $250</dt><dd>Upside $0</dd></div><div><dt>Settlement $300</dt><dd>Upside $37.50</dd></div></dl>
            </div>
          </div>

          <div class="strand-prose">
            <div id="oracle" class="strand-leaf"><p class="tide-kicker">Oracle</p><h2 class="tide-h2">No live price source is connected.</h2><p>A production series would need a named feed, market session, fallback behavior, and settlement window. This preview uses local assumptions and performs no oracle reads.</p></div>
            <div id="fees" class="strand-leaf"><p class="tide-kicker">Fees</p><h2 class="tide-h2">No fee is charged by this demo.</h2><p>A 5% auction fee appeared in an earlier reference model. It is only a design assumption and is not active, binding, or a production term.</p></div>
            <div id="listing" class="strand-leaf"><p class="tide-kicker">Listing</p><h2 class="tide-h2">Assets need a verified market path.</h2><p>A candidate SPL market unit would need a reliable price source and a USDC liquidity path. Listing, custody, jurisdiction, and program permissions require separate review before production.</p></div>
            <div id="risks" class="strand-leaf"><p class="tide-kicker">Risks</p><h2 class="tide-h2">A premium does not remove risk.</h2><p>Income still bears underlying downside. Upside may expire without a payoff. Oracle, liquidity, smart contract, counterparty, market, and regulatory risks remain outside this interface.</p></div>
            <div id="token" class="strand-leaf"><p class="tide-kicker">Token</p><h2 class="tide-h2">The proposed {{ brand.asset }} symbol is separate.</h2><p>Income and Upside describe modeled positions. {{ brand.asset }} is a proposed symbol only; it has not been issued, and no supply or utility is enabled in this preview.</p></div>
            <div id="documents" class="strand-leaf"><p class="tide-kicker">Journal</p><h2 class="tide-h2">Keep assumptions in this browser.</h2><p>The scenario journal stores its record locally and can export it as JSON. It does not submit a transaction or publish the record on chain.</p><a class="tide-link" href="/signal" @click.prevent="go('/signal')">Open the journal <ArrowRight :size="14" /></a></div>
            <div id="terms" class="strand-leaf"><p class="tide-kicker">Terms</p><h2 class="tide-h2">Terms for this local preview.</h2><p>This page is a readable product notice for the interface. It does not replace production terms or create a contractual relationship.</p><a class="tide-link" href="/terms" @click.prevent="go('/terms')">Read the demo terms <ExternalLink :size="13" /></a></div>
            <div id="privacy" class="strand-leaf"><p class="tide-kicker">Privacy</p><h2 class="tide-h2">Your browser holds the journal state.</h2><p>No trade order or private key is requested by this documentation view. External links have their own privacy practices.</p><a class="tide-link" href="/privacy" @click.prevent="go('/privacy')">Read the demo privacy notice <ExternalLink :size="13" /></a></div>
          </div>

          <div id="overview" class="strand-anchor" aria-label="Legacy overview anchor"></div>
          <div id="scenario" class="strand-anchor" aria-label="Legacy scenario anchor"></div>
          <div id="journal" class="strand-anchor" aria-label="Legacy journal anchor"></div>
          <div id="limits" class="strand-anchor" aria-label="Legacy limits anchor"></div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
/* ---------------------------------------------------------------- opening */
.strand { display: grid; grid-template-columns: minmax(0, 1fr); }
.strand > * { min-width: 0; }
.strand-open {
  display: grid;
  gap: 12px;
  padding-block-end: clamp(20px, 2.6vw, 32px);
}
.strand-display { font-size: clamp(32px, 4.8vw, 56px); }
.strand-open-note { padding-block-start: 4px; }

/* ------------------------------------------------------------------ legal */
.strand-legal {
  display: grid;
  gap: 22px;
  max-width: 820px;
}
.strand-legal-copy { display: grid; gap: 14px; color: var(--ink-soft); font: 400 15px/1.75 var(--font-body); }
.strand-legal-actions { display: flex; flex-wrap: wrap; gap: 10px; }

/* --------------------------------------------------------------- document */
.strand-doc {
  display: grid;
  grid-template-columns: minmax(180px, 3fr) minmax(0, 9fr);
  gap: clamp(20px, 3vw, 40px);
  align-items: start;
  padding-block-start: clamp(8px, 1.4vw, 16px);
}
.strand-index {
  position: sticky;
  inset-block-start: 20px;
  display: grid;
  gap: 10px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface-soft);
}
.strand-index-label {
  color: var(--muted);
  font: 600 9px/1.4 var(--font-mono);
  letter-spacing: .16em;
  text-transform: uppercase;
}
.strand-index-rail { display: grid; gap: 1px; }
.strand-index-rail a {
  display: grid;
  grid-template-columns: 26px minmax(0, 1fr);
  gap: 8px;
  align-items: baseline;
  padding: 7px 8px;
  border-radius: 8px;
  color: var(--ink-soft);
  font: 500 12px/1.4 var(--font-body);
  text-decoration: none;
  transition: background-color var(--motion-duration) var(--motion-ease), color var(--motion-duration) var(--motion-ease);
}
.strand-index-rail a:hover { background: var(--surface-alt); color: var(--accent-deep); }
.strand-index-rail b { color: var(--muted); font: 500 9px/1.5 var(--font-mono); letter-spacing: .06em; }

.strand-body { display: grid; gap: clamp(28px, 4vw, 48px); min-width: 0; }
.strand-section { display: grid; gap: 16px; scroll-margin-block-start: 24px; }
.strand-section-head { display: grid; gap: 8px; }
.strand-intro { color: var(--muted); font: 400 13px/1.7 var(--font-body); }

/* ------------------------------------------------------------------ steps */
.strand-steps { display: grid; gap: 0; border-block-start: 1px solid var(--line); }
.strand-steps li {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 16px;
  padding-block: 15px;
  border-block-end: 1px solid var(--line);
}
.strand-step-number { color: var(--accent-safe); font: 600 12px/1.6 var(--font-mono); letter-spacing: .08em; }
.strand-steps p { margin-block-start: 4px; color: var(--ink-soft); font: 400 14px/1.7 var(--font-body); }

.strand-roles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.strand-role {
  display: grid;
  gap: 8px;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: linear-gradient(170deg, var(--surface), var(--surface-soft));
}
.strand-role p { color: var(--muted); font: 400 13px/1.7 var(--font-body); }
.strand-role-label {
  font: 600 9px/1.4 var(--font-mono);
  letter-spacing: .16em;
  text-transform: uppercase;
}
.strand-role-label--income { color: var(--success); }
.strand-role-label--upside { color: var(--accent-safe); }

/* ---------------------------------------------------------------- concepts */
.strand-cards { display: grid; gap: 18px; }
.strand-card { scroll-margin-block-start: 24px; }
.strand-figure {
  display: grid;
  gap: 14px;
  padding: clamp(12px, 1.6vw, 18px);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface);
}
.strand-figure img { width: 100%; height: auto; border-radius: var(--radius-sm); border: 1px solid var(--line); }
.strand-figure figcaption { display: grid; grid-template-columns: 40px minmax(0, 1fr); gap: 4px 14px; align-items: baseline; }
.strand-card-index { color: var(--accent-deep); font: 600 11px/1.5 var(--font-mono); letter-spacing: .1em; grid-row: span 2; }
.strand-figure figcaption p { color: var(--muted); font: 400 13px/1.7 var(--font-body); }

/* --------------------------------------------------------------- settlement */
.strand-split { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: clamp(18px, 2.6vw, 32px); align-items: start; }
.strand-split-copy { display: grid; gap: 10px; }
.strand-split-copy p { color: var(--ink-soft); font: 400 14px/1.75 var(--font-body); }
.strand-formula {
  display: grid;
  gap: 10px;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface-soft);
}
.strand-formula-label { color: var(--muted); font: 600 9px/1.4 var(--font-mono); letter-spacing: .16em; text-transform: uppercase; }
.strand-formula strong { color: var(--ink); font: 600 16px/1.4 var(--font-display); letter-spacing: -.01em; }
.strand-formula-cells { display: grid; gap: 1px; background: var(--line); border: 1px solid var(--line); border-radius: var(--radius-sm); overflow: hidden; }
.strand-formula-cells > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding: 10px 12px;
  background: var(--surface);
}
.strand-formula-cells dt { color: var(--ink-soft); font: 500 11px/1.5 var(--font-mono); }
.strand-formula-cells dd { color: var(--ink); font: 600 12px/1.5 var(--font-mono); }

/* ------------------------------------------------------------------ prose */
.strand-prose { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.strand-leaf {
  display: grid;
  gap: 8px;
  align-content: start;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface);
  scroll-margin-block-start: 24px;
}
.strand-leaf p { color: var(--muted); font: 400 13px/1.7 var(--font-body); }
.strand-leaf .tide-link { margin-block-start: 4px; }
.strand-anchor { position: absolute; width: 1px; height: 1px; overflow: hidden; }

/* -------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .strand-doc { grid-template-columns: minmax(0, 1fr); }
  .strand-index { position: static; }
  .strand-index-rail { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 780px) {
  .strand-roles, .strand-split, .strand-prose { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 520px) {
  .strand-index-rail { grid-template-columns: minmax(0, 1fr); }
  .strand-steps li { grid-template-columns: 32px minmax(0, 1fr); }
}
</style>
