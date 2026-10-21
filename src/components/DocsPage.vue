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
  <div class="leaf">
    <section v-if="legalPage" class="tty-scene doc-open">
      <div class="tty-scene-in doc-open-in">
        <p class="tty-kicker">Local interface preview</p>
        <h1 class="tty-display doc-display" tabindex="-1">{{ legalTitle }}</h1>
        <p class="tty-lead">This page describes how this local product demonstration should be read. It is not a production protocol policy, legal agreement, or investment recommendation.</p>
      </div>
    </section>

    <section v-if="legalPage" class="tty-scene doc-legal">
      <div class="tty-scene-in doc-legal-in">
        <div class="doc-legal-copy">
          <p v-for="paragraph in legalBody" :key="paragraph">{{ paragraph }}</p>
        </div>
        <div class="doc-legal-actions">
          <a class="tty-btn tty-btn--primary" href="/docs" @click.prevent="go('/docs')">Read how it works <ArrowRight :size="15" /></a>
          <a class="tty-btn tty-btn--ghost" href="/" @click.prevent="go('/')">Back to markets <ArrowRight :size="14" /></a>
        </div>
      </div>
    </section>

    <template v-else>
      <section class="tty-scene doc-open">
        <div class="tty-scene-in doc-open-in">
          <p class="tty-kicker">{{ brand.network }} / Model notes</p>
          <h1 class="tty-display doc-display" tabindex="-1">How {{ brand.name }} works.</h1>
          <p class="tty-lead">This preview models an illustrative split around a cap price. It does not custody SPL assets, run an auction, connect an oracle, or settle transactions.</p>
          <p class="tty-note doc-open-note">All displayed market values are examples. No token or Solana program has been issued by this preview.</p>
        </div>
      </section>

      <div class="doc-console">
        <nav class="doc-index" aria-label="On this page">
          <p class="doc-index-label">On this page</p>
          <div class="doc-index-rail">
            <a v-for="([id, label], index) in sections" :key="id" :href="`#${id}`"><b>{{ String(index + 1).padStart(2, '0') }}</b><span>{{ label }}</span></a>
          </div>
        </nav>

        <div class="doc-body">
          <div class="tty-scene-in">
          <div id="mechanism" class="doc-section">
            <p class="tty-kicker">Mechanism</p>
            <ol class="doc-steps">
              <li v-for="[number, title, body] in steps" :key="number">
                <span class="doc-step-number">{{ number }}</span>
                <div><h2 class="tty-h3">{{ title }}</h2><p>{{ body }}</p></div>
              </li>
            </ol>
            <div class="doc-roles">
              <article class="tty-face doc-role"><p class="doc-role-label doc-role-label--income">Income</p><h3 class="tty-h3">Value up to K, plus any premium.</h3><p>Income still bears the underlying asset's downside. A premium does not protect the market unit from a price decline.</p></article>
              <article class="tty-face doc-role"><p class="doc-role-label doc-role-label--upside">Upside</p><h3 class="tty-h3">Value above K.</h3><p>The modeled payoff is max(0, settlement price - K). A buyer's maximum modeled loss is the hypothetical premium paid.</p></article>
            </div>
          </div>

          <div id="concepts" class="doc-section">
            <div class="doc-section-head">
              <p class="tty-kicker">Concepts</p>
              <h2 class="tty-h2">Three parts of the model.</h2>
              <p class="doc-intro">These illustrations describe a product concept, not deployed Solana programs.</p>
            </div>
            <ul class="doc-cards">
              <li v-for="(concept, index) in concepts" :id="`concept-${concept.id}`" :key="concept.id" class="doc-card">
                <figure class="doc-figure">
                  <img :src="concept.image" :alt="concept.title" width="1200" height="750" loading="lazy" />
                  <figcaption>
                    <span class="doc-card-index">{{ String(index + 1).padStart(2, '0') }}</span>
                    <h3 class="tty-h3">{{ concept.title }}</h3>
                    <p>{{ concept.description }}</p>
                  </figcaption>
                </figure>
              </li>
            </ul>
          </div>

          <div id="settlement" class="doc-section doc-split">
            <div class="doc-split-copy">
              <p class="tty-kicker">Settlement</p>
              <h2 class="tty-h2">A defined cap sets the split.</h2>
              <p>For starting price P0 and cap rate c, K = P0 x (1 + c). At assumed settlement price S, Upside receives max(0, S - K). Income receives value up to K plus any hypothetical auction premium.</p>
            </div>
            <div class="tty-face doc-formula">
              <p class="doc-formula-label">Illustrative scenario</p>
              <strong>P0 $250 / 5% cap / K $262.50</strong>
              <dl class="tty-facts tty-facts--stack doc-formula-cells"><div><dt>Settlement $200</dt><dd>Upside $0</dd></div><div><dt>Settlement $250</dt><dd>Upside $0</dd></div><div><dt>Settlement $300</dt><dd>Upside $37.50</dd></div></dl>
            </div>
          </div>

          <div class="doc-prose">
            <div id="oracle" class="doc-leaf"><p class="tty-kicker">Oracle</p><h2 class="tty-h2">No live price source is connected.</h2><p>A production series would need a named feed, market session, fallback behavior, and settlement window. This preview uses local assumptions and performs no oracle reads.</p></div>
            <div id="fees" class="doc-leaf"><p class="tty-kicker">Fees</p><h2 class="tty-h2">No fee is charged by this demo.</h2><p>A 5% auction fee appeared in an earlier reference model. It is only a design assumption and is not active, binding, or a production term.</p></div>
            <div id="listing" class="doc-leaf"><p class="tty-kicker">Listing</p><h2 class="tty-h2">Assets need a verified market path.</h2><p>A candidate SPL market unit would need a reliable price source and a USDC liquidity path. Listing, custody, jurisdiction, and program permissions require separate review before production.</p></div>
            <div id="risks" class="doc-leaf"><p class="tty-kicker">Risks</p><h2 class="tty-h2">A premium does not remove risk.</h2><p>Income still bears underlying downside. Upside may expire without a payoff. Oracle, liquidity, smart contract, counterparty, market, and regulatory risks remain outside this interface.</p></div>
            <div id="token" class="doc-leaf"><p class="tty-kicker">Token</p><h2 class="tty-h2">The proposed {{ brand.asset }} symbol is separate.</h2><p>Income and Upside describe modeled positions. {{ brand.asset }} is a proposed symbol only; it has not been issued, and no supply or utility is enabled in this preview.</p></div>
            <div id="documents" class="doc-leaf"><p class="tty-kicker">Journal</p><h2 class="tty-h2">Keep assumptions in this browser.</h2><p>The scenario journal stores its record locally and can export it as JSON. It does not submit a transaction or publish the record on chain.</p><a class="tty-link doc-doc-link" href="/signal" @click.prevent="go('/signal')">Open the journal <ArrowRight :size="14" /></a></div>
            <div id="terms" class="doc-leaf"><p class="tty-kicker">Terms</p><h2 class="tty-h2">Terms for this local preview.</h2><p>This page is a readable product notice for the interface. It does not replace production terms or create a contractual relationship.</p><a class="tty-link doc-doc-link" href="/terms" @click.prevent="go('/terms')">Read the demo terms <ExternalLink :size="13" /></a></div>
            <div id="privacy" class="doc-leaf"><p class="tty-kicker">Privacy</p><h2 class="tty-h2">Your browser holds the journal state.</h2><p>No trade order or private key is requested by this documentation view. External links have their own privacy practices.</p><a class="tty-link doc-doc-link" href="/privacy" @click.prevent="go('/privacy')">Read the demo privacy notice <ExternalLink :size="13" /></a></div>
          </div>

          <div id="overview" class="doc-anchor" aria-label="Legacy overview anchor"></div>
          <div id="scenario" class="doc-anchor" aria-label="Legacy scenario anchor"></div>
          <div id="journal" class="doc-anchor" aria-label="Legacy journal anchor"></div>
          <div id="limits" class="doc-anchor" aria-label="Legacy limits anchor"></div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
/* -------------------------------------------------------------------- open */
.doc-open { padding-bottom: clamp(22px, 2.6vw, 36px); }
.doc-open-in { display: grid; gap: clamp(12px, 1.6vw, 20px); max-width: 900px; }
.doc-display { font-size: clamp(28px, 3.4vw, 44px); }
.doc-open-note { margin-top: 4px; }

/* ------------------------------------------------------------------- index */
.doc-console {
  display: grid;
  grid-template-columns: 208px minmax(0, 1fr);
  align-items: start;
  border-top: 1px solid var(--line);
}
.doc-index {
  position: sticky;
  top: calc(var(--strip-h) + 8px);
  display: grid;
  gap: 8px;
  align-content: start;
  padding: clamp(18px, 2vw, 28px) 14px clamp(18px, 2vw, 28px) var(--gutter);
  border-right: 1px solid var(--line);
}
.doc-index-label {
  margin: 0 0 2px;
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.doc-index-rail { display: grid; gap: 2px; }
.doc-index-rail a {
  display: grid;
  grid-template-columns: 22px minmax(0, 1fr);
  align-items: baseline;
  gap: 6px;
  padding: 5px 7px;
  border-left: 2px solid transparent;
  color: var(--muted);
  font: 500 10px/1.5 var(--font-mono);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  text-decoration: none;
  transition: color 160ms var(--ease), background-color 160ms var(--ease);
}
.doc-index-rail a b { color: var(--faint); font-weight: 500; }
.doc-index-rail a:hover {
  color: var(--ink);
  background: rgba(255, 255, 255, 0.04);
}
.doc-index-rail a:hover b { color: var(--accent-safe); }

/* -------------------------------------------------------------------- body */
.doc-body { padding: clamp(18px, 2.2vw, 30px) var(--gutter); }
.doc-section { display: grid; gap: clamp(16px, 1.8vw, 24px); padding-bottom: clamp(34px, 4vw, 56px); scroll-margin-top: 130px; }
.doc-section + .doc-section { padding-top: clamp(34px, 4vw, 56px); border-top: 1px solid var(--line); }
.doc-section h2 { margin: 0; }
.doc-section-head { display: grid; gap: 10px; }
.doc-intro { margin: 0; color: var(--muted); font: 400 14px/1.7 var(--font-body); }

/* ------------------------------------------------------------------- steps */
.doc-steps {
  display: grid;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
  border-top: 1px solid var(--line);
}
.doc-steps li {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--line);
}
.doc-steps h2 { margin: 0 0 5px; }
.doc-steps p { margin: 0; max-width: 72ch; color: var(--muted); font: 400 13px/1.7 var(--font-body); }
.doc-step-number {
  color: var(--accent-safe);
  font: 500 11px/1.7 var(--font-mono);
  letter-spacing: 0.16em;
}

.doc-roles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.doc-role { display: grid; gap: 10px; align-content: start; }
.doc-role-label {
  margin: 0;
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.doc-role-label--income { color: var(--mint); }
.doc-role-label--upside { color: var(--accent-2); }
.doc-role h3 { margin: 0; }
.doc-role p { margin: 0; color: var(--muted); font: 400 13px/1.7 var(--font-body); }

/* ------------------------------------------------------------------ cards */
.doc-cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.doc-card { min-width: 0; }
.doc-figure {
  display: grid;
  margin: 0;
  height: 100%;
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  background: linear-gradient(180deg, var(--surface-2), var(--bg-2));
  overflow: hidden;
}
.doc-figure img {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 10;
  object-fit: contain;
  border-bottom: 1px solid var(--line);
  background: radial-gradient(120% 100% at 50% 0%, rgba(255, 0, 0, 0.1), transparent 70%);
  /* The supplied plates were drawn on paper. Inverted they read as night-chart
     proofs of the same drawing, so the illustration stays inside the deck. */
  filter: invert(0.93) hue-rotate(178deg) saturate(1.15) brightness(0.94) contrast(1.02);
  transition: filter 320ms var(--ease);
}
.doc-figure:hover img { filter: invert(0.9) hue-rotate(178deg) saturate(1.3) brightness(1.02) contrast(1.02); }
.doc-figure figcaption { padding: 18px 20px 22px; }
.doc-card-index {
  display: block;
  margin-bottom: 8px;
  color: var(--accent-safe);
  font: 500 9px/1 var(--font-mono);
  letter-spacing: 0.22em;
}
.doc-figure h3 { margin: 0 0 8px; }
.doc-figure p { margin: 0; color: var(--muted); font: 400 12px/1.7 var(--font-body); }

/* ------------------------------------------------------------------ split */
.doc-split { grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); align-items: start; }
.doc-split-copy { display: grid; gap: 10px; }
.doc-split-copy p:last-child { margin: 0; max-width: 68ch; color: var(--muted); font: 400 14px/1.75 var(--font-body); }
.doc-formula { display: grid; gap: 14px; align-content: start; }
.doc-formula-label {
  margin: 0;
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.doc-formula strong {
  display: block;
  font: 500 14px/1.6 var(--font-mono);
  font-variant-numeric: tabular-nums;
  color: var(--ink);
}
.doc-formula-cells { border: 0; background: none; }

/* ------------------------------------------------------------------- prose */
.doc-prose {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin-top: clamp(34px, 4vw, 56px);
  border-top: 1px solid var(--line);
  background: var(--line);
}
.doc-leaf {
  display: grid;
  gap: 10px;
  align-content: start;
  min-width: 0;
  padding: clamp(20px, 2.4vw, 34px);
  background: var(--bg-2);
  scroll-margin-top: 130px;
}
.doc-leaf h2 { margin: 0; font-size: clamp(20px, 1.9vw, 27px); }
.doc-leaf p:last-child { margin: 0; color: var(--muted); font: 400 13px/1.75 var(--font-body); }
.doc-doc-link { margin-top: 4px; }

.doc-anchor { height: 1px; scroll-margin-top: 130px; }

/* ------------------------------------------------------------------- legal */
.doc-legal-in { display: grid; gap: clamp(20px, 2.4vw, 32px); max-width: 780px; }
.doc-legal-copy { display: grid; gap: 16px; }
.doc-legal-copy p {
  margin: 0;
  color: var(--ink-2);
  font: 400 15px/1.85 var(--font-body);
  padding-left: 20px;
  border-left: 1px solid var(--line-2);
}
.doc-legal-actions { display: flex; flex-wrap: wrap; gap: 12px; }

/* -------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .doc-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .doc-roles { grid-template-columns: minmax(0, 1fr); }
  .doc-split { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 900px) {
  .doc-console { grid-template-columns: minmax(0, 1fr); }
  .doc-index {
    position: static;
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 4px 8px;
    padding: 10px var(--gutter);
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }
  .doc-index-label { margin: 0 8px 0 0; }
  .doc-index-rail { display: flex; flex-wrap: wrap; gap: 2px 6px; }
  .doc-index-rail a { border-left: 0; padding: 4px 6px; }
}
@media (max-width: 860px) {
  .doc-prose { grid-template-columns: minmax(0, 1fr); }
  .doc-cards { grid-template-columns: minmax(0, 1fr); }
  .doc-legal-actions { display: grid; }
  .doc-legal-actions .tty-btn { width: 100%; }
}
</style>
