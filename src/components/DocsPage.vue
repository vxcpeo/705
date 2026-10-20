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
    <section v-if="legalPage" class="atlas-scene leaf-open">
      <div class="atlas-scene-in leaf-open-in">
        <p class="atlas-kicker">Local interface preview</p>
        <h1 class="atlas-display leaf-display" tabindex="-1">{{ legalTitle }}</h1>
        <p class="atlas-lead">This page describes how this local product demonstration should be read. It is not a production protocol policy, legal agreement, or investment recommendation.</p>
      </div>
    </section>

    <section v-if="legalPage" class="atlas-scene leaf-legal">
      <div class="atlas-scene-in leaf-legal-in">
        <div class="leaf-legal-copy">
          <p v-for="paragraph in legalBody" :key="paragraph">{{ paragraph }}</p>
        </div>
        <div class="leaf-legal-actions">
          <a class="atlas-btn atlas-btn--primary" href="/docs" @click.prevent="go('/docs')">Read how it works <ArrowRight :size="15" /></a>
          <a class="atlas-btn atlas-btn--ghost" href="/" @click.prevent="go('/')">Back to markets <ArrowRight :size="14" /></a>
        </div>
      </div>
    </section>

    <template v-else>
      <section class="atlas-scene leaf-open">
        <div class="atlas-scene-in leaf-open-in">
          <p class="atlas-kicker">{{ brand.network }} / Model notes</p>
          <h1 class="atlas-display leaf-display" tabindex="-1">How {{ brand.name }} works.</h1>
          <p class="atlas-lead">This preview models an illustrative split around a cap price. It does not custody SPL assets, run an auction, connect an oracle, or settle transactions.</p>
          <p class="atlas-note leaf-open-note">All displayed market values are examples. No token or Solana program has been issued by this preview.</p>
        </div>
      </section>

      <section class="atlas-scene leaf-index-scene">
        <div class="atlas-scene-in">
          <nav class="leaf-index" aria-label="On this page">
            <p class="leaf-index-label">On this page</p>
            <div class="leaf-index-rail">
              <a v-for="([id, label], index) in sections" :key="id" :href="`#${id}`"><b>{{ String(index + 1).padStart(2, '0') }}</b><span>{{ label }}</span></a>
            </div>
          </nav>
        </div>
      </section>

      <section class="atlas-scene leaf-body">
        <div class="atlas-scene-in">
          <div id="mechanism" class="leaf-section">
            <p class="atlas-kicker">Mechanism</p>
            <ol class="leaf-steps">
              <li v-for="[number, title, body] in steps" :key="number">
                <span class="leaf-step-number">{{ number }}</span>
                <div><h2 class="atlas-h3">{{ title }}</h2><p>{{ body }}</p></div>
              </li>
            </ol>
            <div class="leaf-roles">
              <article class="atlas-face leaf-role"><p class="leaf-role-label leaf-role-label--income">Income</p><h3 class="atlas-h3">Value up to K, plus any premium.</h3><p>Income still bears the underlying asset's downside. A premium does not protect the market unit from a price decline.</p></article>
              <article class="atlas-face leaf-role"><p class="leaf-role-label leaf-role-label--upside">Upside</p><h3 class="atlas-h3">Value above K.</h3><p>The modeled payoff is max(0, settlement price - K). A buyer's maximum modeled loss is the hypothetical premium paid.</p></article>
            </div>
          </div>

          <div id="concepts" class="leaf-section">
            <div class="leaf-section-head">
              <p class="atlas-kicker">Concepts</p>
              <h2 class="atlas-h2">Three parts of the model.</h2>
              <p class="leaf-intro">These illustrations describe a product concept, not deployed Solana programs.</p>
            </div>
            <ul class="leaf-cards">
              <li v-for="(concept, index) in concepts" :id="`concept-${concept.id}`" :key="concept.id" class="leaf-card">
                <figure class="leaf-figure">
                  <img :src="concept.image" :alt="concept.title" width="1200" height="750" loading="lazy" />
                  <figcaption>
                    <span class="leaf-card-index">{{ String(index + 1).padStart(2, '0') }}</span>
                    <h3 class="atlas-h3">{{ concept.title }}</h3>
                    <p>{{ concept.description }}</p>
                  </figcaption>
                </figure>
              </li>
            </ul>
          </div>

          <div id="settlement" class="leaf-section leaf-split">
            <div class="leaf-split-copy">
              <p class="atlas-kicker">Settlement</p>
              <h2 class="atlas-h2">A defined cap sets the split.</h2>
              <p>For starting price P0 and cap rate c, K = P0 x (1 + c). At assumed settlement price S, Upside receives max(0, S - K). Income receives value up to K plus any hypothetical auction premium.</p>
            </div>
            <div class="atlas-face leaf-formula">
              <p class="leaf-formula-label">Illustrative scenario</p>
              <strong>P0 $250 / 5% cap / K $262.50</strong>
              <dl class="atlas-facts atlas-facts--stack leaf-formula-cells"><div><dt>Settlement $200</dt><dd>Upside $0</dd></div><div><dt>Settlement $250</dt><dd>Upside $0</dd></div><div><dt>Settlement $300</dt><dd>Upside $37.50</dd></div></dl>
            </div>
          </div>

          <div class="leaf-prose">
            <div id="oracle" class="leaf-leaf"><p class="atlas-kicker">Oracle</p><h2 class="atlas-h2">No live price source is connected.</h2><p>A production series would need a named feed, market session, fallback behavior, and settlement window. This preview uses local assumptions and performs no oracle reads.</p></div>
            <div id="fees" class="leaf-leaf"><p class="atlas-kicker">Fees</p><h2 class="atlas-h2">No fee is charged by this demo.</h2><p>A 5% auction fee appeared in an earlier reference model. It is only a design assumption and is not active, binding, or a production term.</p></div>
            <div id="listing" class="leaf-leaf"><p class="atlas-kicker">Listing</p><h2 class="atlas-h2">Assets need a verified market path.</h2><p>A candidate SPL market unit would need a reliable price source and a USDC liquidity path. Listing, custody, jurisdiction, and program permissions require separate review before production.</p></div>
            <div id="risks" class="leaf-leaf"><p class="atlas-kicker">Risks</p><h2 class="atlas-h2">A premium does not remove risk.</h2><p>Income still bears underlying downside. Upside may expire without a payoff. Oracle, liquidity, smart contract, counterparty, market, and regulatory risks remain outside this interface.</p></div>
            <div id="token" class="leaf-leaf"><p class="atlas-kicker">Token</p><h2 class="atlas-h2">The proposed {{ brand.asset }} symbol is separate.</h2><p>Income and Upside describe modeled positions. {{ brand.asset }} is a proposed symbol only; it has not been issued, and no supply or utility is enabled in this preview.</p></div>
            <div id="documents" class="leaf-leaf"><p class="atlas-kicker">Journal</p><h2 class="atlas-h2">Keep assumptions in this browser.</h2><p>The scenario journal stores its record locally and can export it as JSON. It does not submit a transaction or publish the record on chain.</p><a class="atlas-link leaf-leaf-link" href="/signal" @click.prevent="go('/signal')">Open the journal <ArrowRight :size="14" /></a></div>
            <div id="terms" class="leaf-leaf"><p class="atlas-kicker">Terms</p><h2 class="atlas-h2">Terms for this local preview.</h2><p>This page is a readable product notice for the interface. It does not replace production terms or create a contractual relationship.</p><a class="atlas-link leaf-leaf-link" href="/terms" @click.prevent="go('/terms')">Read the demo terms <ExternalLink :size="13" /></a></div>
            <div id="privacy" class="leaf-leaf"><p class="atlas-kicker">Privacy</p><h2 class="atlas-h2">Your browser holds the journal state.</h2><p>No trade order or private key is requested by this documentation view. External links have their own privacy practices.</p><a class="atlas-link leaf-leaf-link" href="/privacy" @click.prevent="go('/privacy')">Read the demo privacy notice <ExternalLink :size="13" /></a></div>
          </div>

          <div id="overview" class="leaf-anchor" aria-label="Legacy overview anchor"></div>
          <div id="scenario" class="leaf-anchor" aria-label="Legacy scenario anchor"></div>
          <div id="journal" class="leaf-anchor" aria-label="Legacy journal anchor"></div>
          <div id="limits" class="leaf-anchor" aria-label="Legacy limits anchor"></div>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
/* -------------------------------------------------------------------- open */
.leaf-open { padding-bottom: clamp(22px, 2.6vw, 36px); }
.leaf-open-in { display: grid; gap: clamp(12px, 1.6vw, 20px); max-width: 900px; }
.leaf-display { font-size: clamp(36px, 5.2vw, 68px); }
.leaf-open-note { margin-top: 4px; }

/* ------------------------------------------------------------------- index */
.leaf-index-scene { padding-block: clamp(18px, 2vw, 26px); }
.leaf-index { display: grid; gap: 12px; }
.leaf-index-label {
  margin: 0;
  color: var(--star-faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.leaf-index-rail {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 8px;
  scroll-snap-type: x proximity;
  scrollbar-width: thin;
  scrollbar-color: var(--hair-2) transparent;
}
.leaf-index-rail a {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  flex: none;
  padding: 9px 15px;
  border: 1px solid var(--hair);
  border-radius: var(--r-pill);
  background: rgba(11, 12, 21, 0.7);
  color: var(--star-mute);
  font: 500 10px/1.2 var(--font-mono);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  text-decoration: none;
  scroll-snap-align: start;
  transition: color 180ms var(--ease), border-color 180ms var(--ease), background-color 180ms var(--ease);
}
.leaf-index-rail a b { color: var(--star-faint); font-weight: 500; }
.leaf-index-rail a:hover {
  color: var(--star);
  border-color: rgba(64, 179, 255, 0.5);
  background: rgba(64, 179, 255, 0.1);
}

/* -------------------------------------------------------------------- body */
.leaf-body { padding-top: clamp(10px, 1.4vw, 18px); }
.leaf-section { display: grid; gap: clamp(16px, 1.8vw, 24px); padding-bottom: clamp(34px, 4vw, 56px); scroll-margin-top: 130px; }
.leaf-section + .leaf-section { padding-top: clamp(34px, 4vw, 56px); border-top: 1px solid var(--hair); }
.leaf-section h2 { margin: 0; }
.leaf-section-head { display: grid; gap: 10px; }
.leaf-intro { margin: 0; color: var(--star-mute); font: 400 14px/1.7 var(--font-body); }

/* ------------------------------------------------------------------- steps */
.leaf-steps {
  display: grid;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
  border-top: 1px solid var(--hair);
}
.leaf-steps li {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--hair);
}
.leaf-steps h2 { margin: 0 0 5px; }
.leaf-steps p { margin: 0; max-width: 72ch; color: var(--star-mute); font: 400 13px/1.7 var(--font-body); }
.leaf-step-number {
  color: var(--beam);
  font: 500 11px/1.7 var(--font-mono);
  letter-spacing: 0.16em;
}

.leaf-roles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.leaf-role { display: grid; gap: 10px; align-content: start; }
.leaf-role-label {
  margin: 0;
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.leaf-role-label--income { color: var(--mint); }
.leaf-role-label--upside { color: var(--beam-2); }
.leaf-role h3 { margin: 0; }
.leaf-role p { margin: 0; color: var(--star-mute); font: 400 13px/1.7 var(--font-body); }

/* ------------------------------------------------------------------ cards */
.leaf-cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.leaf-card { min-width: 0; }
.leaf-figure {
  display: grid;
  margin: 0;
  height: 100%;
  border: 1px solid var(--hair);
  border-radius: var(--r-lg);
  background: linear-gradient(180deg, var(--deck-2), var(--void-2));
  overflow: hidden;
}
.leaf-figure img {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 10;
  object-fit: contain;
  border-bottom: 1px solid var(--hair);
  background: radial-gradient(120% 100% at 50% 0%, rgba(64, 179, 255, 0.1), transparent 70%);
  /* The supplied plates were drawn on paper. Inverted they read as night-chart
     proofs of the same drawing, so the illustration stays inside the deck. */
  filter: invert(0.93) hue-rotate(178deg) saturate(1.15) brightness(0.94) contrast(1.02);
  transition: filter 320ms var(--ease);
}
.leaf-figure:hover img { filter: invert(0.9) hue-rotate(178deg) saturate(1.3) brightness(1.02) contrast(1.02); }
.leaf-figure figcaption { padding: 18px 20px 22px; }
.leaf-card-index {
  display: block;
  margin-bottom: 8px;
  color: var(--beam);
  font: 500 9px/1 var(--font-mono);
  letter-spacing: 0.22em;
}
.leaf-figure h3 { margin: 0 0 8px; }
.leaf-figure p { margin: 0; color: var(--star-mute); font: 400 12px/1.7 var(--font-body); }

/* ------------------------------------------------------------------ split */
.leaf-split { grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); align-items: start; }
.leaf-split-copy { display: grid; gap: 10px; }
.leaf-split-copy p:last-child { margin: 0; max-width: 68ch; color: var(--star-mute); font: 400 14px/1.75 var(--font-body); }
.leaf-formula { display: grid; gap: 14px; align-content: start; }
.leaf-formula-label {
  margin: 0;
  color: var(--star-faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.leaf-formula strong {
  display: block;
  font: 500 14px/1.6 var(--font-mono);
  font-variant-numeric: tabular-nums;
  color: var(--star);
}
.leaf-formula-cells { border: 0; background: none; }

/* ------------------------------------------------------------------- prose */
.leaf-prose {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin-top: clamp(34px, 4vw, 56px);
  border-top: 1px solid var(--hair);
  background: var(--hair);
}
.leaf-leaf {
  display: grid;
  gap: 10px;
  align-content: start;
  min-width: 0;
  padding: clamp(20px, 2.4vw, 34px);
  background: var(--void-2);
  scroll-margin-top: 130px;
}
.leaf-leaf h2 { margin: 0; font-size: clamp(20px, 1.9vw, 27px); }
.leaf-leaf p:last-child { margin: 0; color: var(--star-mute); font: 400 13px/1.75 var(--font-body); }
.leaf-leaf-link { margin-top: 4px; }

.leaf-anchor { height: 1px; scroll-margin-top: 130px; }

/* ------------------------------------------------------------------- legal */
.leaf-legal-in { display: grid; gap: clamp(20px, 2.4vw, 32px); max-width: 780px; }
.leaf-legal-copy { display: grid; gap: 16px; }
.leaf-legal-copy p {
  margin: 0;
  color: var(--star-2);
  font: 400 15px/1.85 var(--font-body);
  padding-left: 20px;
  border-left: 1px solid var(--hair-2);
}
.leaf-legal-actions { display: flex; flex-wrap: wrap; gap: 12px; }

/* -------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  .leaf-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .leaf-roles { grid-template-columns: minmax(0, 1fr); }
  .leaf-split { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 860px) {
  .leaf-prose { grid-template-columns: minmax(0, 1fr); }
  .leaf-cards { grid-template-columns: minmax(0, 1fr); }
  .leaf-legal-actions { display: grid; }
  .leaf-legal-actions .atlas-btn { width: 100%; }
}
</style>
