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
  <div class="bl-page bl-docs">
    <div class="bl-bento">
      <template v-if="legalPage">
        <section class="bl-tile bl-tile--tint bl-span-7 bl-docs-legal-head">
          <p class="bl-kicker">Local interface preview</p>
          <h1 class="bl-display bl-docs-title" tabindex="-1">{{ legalTitle }}</h1>
          <p class="bl-lead">This page describes how this local product demonstration should be read. It is not a production protocol policy, legal agreement, or investment recommendation.</p>
          <footer class="bl-docs-legal-actions">
            <a class="bl-btn bl-btn--primary" href="/docs" @click.prevent="go('/docs')">Read how it works <ArrowRight :size="15" /></a>
            <a class="bl-btn" href="/" @click.prevent="go('/')">Back to markets <ArrowRight :size="14" /></a>
          </footer>
        </section>

        <section class="bl-tile bl-span-12 bl-docs-clauses">
          <ol class="bl-clause-list">
            <li v-for="(paragraph, index) in legalBody" :key="paragraph" class="bl-clause">
              <span class="bl-clause-num" aria-hidden="true">{{ String(index + 1).padStart(2, '0') }}</span>
              <p>{{ paragraph }}</p>
            </li>
          </ol>
        </section>
      </template>

      <template v-else>
        <section class="bl-tile bl-tile--tint bl-span-8 bl-docs-open">
          <p class="bl-kicker">{{ brand.network }} / Model notes</p>
          <h1 class="bl-display bl-docs-title" tabindex="-1">How {{ brand.name }} works.</h1>
          <p class="bl-lead">This preview models an illustrative split around a cap price. It does not custody SPL assets, run an auction, connect an oracle, or settle transactions.</p>
          <p class="bl-note">All displayed market values are examples. No token or Solana program has been issued by this preview.</p>
        </section>

        <nav class="bl-tile bl-tile--surface bl-span-4 bl-docs-index" aria-label="On this page">
          <p class="bl-docs-index-label">On this page</p>
          <div class="bl-docs-chips">
            <a v-for="([id, label], index) in sections" :key="id" :href="`#${id}`"><b>{{ String(index + 1).padStart(2, '0') }}</b><span>{{ label }}</span></a>
          </div>
        </nav>

        <section id="mechanism" class="bl-tile bl-span-7 bl-docs-steps">
          <p class="bl-kicker">Mechanism</p>
          <ol class="bl-steps">
            <li v-for="[number, title, body] in steps" :key="number">
              <span class="bl-step-number">{{ number }}</span>
              <div><h2 class="bl-h3">{{ title }}</h2><p>{{ body }}</p></div>
            </li>
          </ol>
        </section>

        <section class="bl-tile bl-tile--surface bl-span-5 bl-docs-roles">
          <div class="bl-role bl-role--income"><p class="bl-role-label">Income</p><h3 class="bl-h3">Value up to K, plus any premium.</h3><p>Income still bears the underlying asset's downside. A premium does not protect the market unit from a price decline.</p></div>
          <div class="bl-role bl-role--upside"><p class="bl-role-label">Upside</p><h3 class="bl-h3">Value above K.</h3><p>The modeled payoff is max(0, settlement price - K). A buyer's maximum modeled loss is the hypothetical premium paid.</p></div>
        </section>

        <section class="bl-tile bl-tile--plain bl-span-12 bl-docs-concepts-head">
          <p class="bl-kicker">Concepts</p>
          <h2 class="bl-h2">Three parts of the model.</h2>
          <p class="bl-docs-intro">These illustrations describe a product concept, not deployed Solana programs.</p>
        </section>

        <section v-for="(concept, index) in concepts" :id="`concept-${concept.id}`" :key="concept.id" class="bl-tile bl-span-4 bl-concept">
          <figure class="bl-concept-figure">
            <img :src="concept.image" :alt="concept.title" width="1200" height="750" loading="lazy" />
            <figcaption>
              <span class="bl-concept-index">{{ String(index + 1).padStart(2, '0') }}</span>
              <h3 class="bl-h3">{{ concept.title }}</h3>
              <p>{{ concept.description }}</p>
            </figcaption>
          </figure>
        </section>

        <section id="settlement" class="bl-tile bl-span-7 bl-docs-settlement">
          <p class="bl-kicker">Settlement</p>
          <h2 class="bl-h2">A defined cap sets the split.</h2>
          <p class="bl-docs-prose">For starting price P0 and cap rate c, K = P0 x (1 + c). At assumed settlement price S, Upside receives max(0, S - K). Income receives value up to K plus any hypothetical auction premium.</p>
        </section>

        <section class="bl-tile bl-tile--surface bl-span-5 bl-docs-formula">
          <p class="bl-formula-label">Illustrative scenario</p>
          <strong class="bl-formula-lead">P0 $250 / 5% cap / K $262.50</strong>
          <dl class="bl-formula-cells"><div><dt>Settlement $200</dt><dd>Upside $0</dd></div><div><dt>Settlement $250</dt><dd>Upside $0</dd></div><div><dt>Settlement $300</dt><dd>Upside $37.50</dd></div></dl>
        </section>

        <section class="bl-tile bl-span-12 bl-docs-glossary">
          <div class="bl-glossary">
            <div id="oracle" class="bl-gloss"><p class="bl-kicker">Oracle</p><h2 class="bl-h2">No live price source is connected.</h2><p>A production series would need a named feed, market session, fallback behavior, and settlement window. This preview uses local assumptions and performs no oracle reads.</p></div>
            <div id="fees" class="bl-gloss"><p class="bl-kicker">Fees</p><h2 class="bl-h2">No fee is charged by this demo.</h2><p>A 5% auction fee appeared in an earlier reference model. It is only a design assumption and is not active, binding, or a production term.</p></div>
            <div id="listing" class="bl-gloss"><p class="bl-kicker">Listing</p><h2 class="bl-h2">Assets need a verified market path.</h2><p>A candidate SPL market unit would need a reliable price source and a USDC liquidity path. Listing, custody, jurisdiction, and program permissions require separate review before production.</p></div>
            <div id="risks" class="bl-gloss"><p class="bl-kicker">Risks</p><h2 class="bl-h2">A premium does not remove risk.</h2><p>Income still bears underlying downside. Upside may expire without a payoff. Oracle, liquidity, smart contract, counterparty, market, and regulatory risks remain outside this interface.</p></div>
            <div id="token" class="bl-gloss"><p class="bl-kicker">Token</p><h2 class="bl-h2">The proposed {{ brand.asset }} symbol is separate.</h2><p>Income and Upside describe modeled positions. {{ brand.asset }} is a proposed symbol only; it has not been issued, and no supply or utility is enabled in this preview.</p></div>
            <div id="documents" class="bl-gloss"><p class="bl-kicker">Journal</p><h2 class="bl-h2">Keep assumptions in this browser.</h2><p>The scenario journal stores its record locally and can export it as JSON. It does not submit a transaction or publish the record on chain.</p><a class="bl-link" href="/signal" @click.prevent="go('/signal')">Open the journal <ArrowRight :size="14" /></a></div>
            <div id="terms" class="bl-gloss"><p class="bl-kicker">Terms</p><h2 class="bl-h2">Terms for this local preview.</h2><p>This page is a readable product notice for the interface. It does not replace production terms or create a contractual relationship.</p><a class="bl-link" href="/terms" @click.prevent="go('/terms')">Read the demo terms <ExternalLink :size="13" /></a></div>
            <div id="privacy" class="bl-gloss"><p class="bl-kicker">Privacy</p><h2 class="bl-h2">Your browser holds the journal state.</h2><p>No trade order or private key is requested by this documentation view. External links have their own privacy practices.</p><a class="bl-link" href="/privacy" @click.prevent="go('/privacy')">Read the demo privacy notice <ExternalLink :size="13" /></a></div>
          </div>
        </section>

        <div class="bl-docs-anchors">
          <div id="overview" aria-label="Legacy overview anchor"></div>
          <div id="scenario" aria-label="Legacy scenario anchor"></div>
          <div id="journal" aria-label="Legacy journal anchor"></div>
          <div id="limits" aria-label="Legacy limits anchor"></div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.bl-docs { gap: var(--bl-gap); }
.bl-docs-title { font-size: clamp(32px, 4.2vw, 52px); }

/* ------------------------------------------------------------------- legal */
.bl-docs-legal-head { gap: 12px; }
.bl-docs-legal-actions { display: flex; flex-wrap: wrap; gap: 10px; padding-block-start: 6px; }
.bl-docs-clauses { padding-block: clamp(14px, 1.6vw, 20px); }
.bl-clause-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 clamp(20px, 3vw, 44px); }
.bl-clause {
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr);
  gap: 14px;
  padding-block: 16px;
  border-block-start: 1px solid var(--bl-line);
}
.bl-clause:first-child, .bl-clause:nth-child(2) { border-block-start: 0; }
.bl-clause-num { color: var(--bl-accent-safe); font: 600 10px/1.8 var(--bl-font-mono); letter-spacing: .1em; }
.bl-clause p { max-width: 62ch; color: var(--bl-ink-soft); font: 400 15px/1.75 var(--bl-font-body); }

/* -------------------------------------------------------------------- open */
.bl-docs-open { gap: 12px; }
.bl-docs-index { gap: 10px; }
.bl-docs-index-label {
  color: var(--bl-muted);
  font: 600 9.5px/1.4 var(--bl-font-mono);
  letter-spacing: .14em;
  text-transform: uppercase;
}
.bl-docs-chips { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px; }
.bl-docs-chips a {
  display: grid;
  grid-template-columns: 20px minmax(0, 1fr);
  gap: 7px;
  align-items: baseline;
  padding: 7px 9px;
  border: 1px solid transparent;
  border-radius: var(--bl-r-xs);
  color: var(--bl-ink-soft);
  font: 500 12.5px/1.4 var(--bl-font-body);
  text-decoration: none;
  transition: background-color var(--bl-dur) var(--bl-ease), border-color var(--bl-dur) var(--bl-ease);
}
.bl-docs-chips a:hover { background: var(--bl-paper); border-color: var(--bl-line); color: var(--bl-accent-safe); }
.bl-docs-chips b { color: var(--bl-muted); font: 500 9px/1.6 var(--bl-font-mono); }

/* ------------------------------------------------------------------- steps */
.bl-docs-steps { gap: 12px; }
.bl-steps { display: grid; gap: 0; }
.bl-steps li {
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr);
  gap: 14px;
  padding-block: 14px;
  border-block-start: 1px solid var(--bl-line);
}
.bl-steps li:first-child { border-block-start: 0; padding-block-start: 0; }
.bl-step-number { color: var(--bl-accent-safe); font: 600 12px/1.7 var(--bl-font-mono); letter-spacing: .06em; }
.bl-steps p { margin-block-start: 3px; color: var(--bl-ink-soft); font: 400 14px/1.7 var(--bl-font-body); }

.bl-docs-roles { gap: 12px; }
.bl-role { display: grid; gap: 7px; padding: 16px; border: 1px solid var(--bl-line); border-radius: var(--bl-r-sm); background: var(--bl-paper); }
.bl-role p { color: var(--bl-muted); font: 400 13px/1.7 var(--bl-font-body); }
.bl-role-label { font: 600 9.5px/1.4 var(--bl-font-mono); letter-spacing: .14em; text-transform: uppercase; }
.bl-role--income .bl-role-label { color: var(--bl-good); }
.bl-role--upside .bl-role-label { color: var(--bl-accent-safe); }

/* ---------------------------------------------------------------- concepts */
.bl-docs-concepts-head { gap: 8px; padding-block: 10px 0; }
.bl-docs-intro { color: var(--bl-muted); font: 400 13px/1.7 var(--bl-font-body); }
.bl-concept { padding: 10px; }
.bl-concept-figure { display: grid; gap: 12px; }
.bl-concept-figure img {
  width: 100%;
  height: auto;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-sm);
}
.bl-concept-figure figcaption { display: grid; grid-template-columns: 34px minmax(0, 1fr); gap: 3px 10px; align-items: baseline; padding: 0 6px 6px; }
.bl-concept-index { grid-row: span 2; color: var(--bl-accent-safe); font: 600 11px/1.6 var(--bl-font-mono); letter-spacing: .08em; }
.bl-concept-figure figcaption p { color: var(--bl-muted); font: 400 13px/1.65 var(--bl-font-body); }

/* -------------------------------------------------------------- settlement */
.bl-docs-settlement { gap: 10px; }
.bl-docs-prose { color: var(--bl-ink-soft); font: 400 14.5px/1.75 var(--bl-font-body); }
.bl-docs-formula { gap: 10px; align-content: start; }
.bl-formula-label { color: var(--bl-muted); font: 600 9.5px/1.4 var(--bl-font-mono); letter-spacing: .14em; text-transform: uppercase; }
.bl-formula-lead { color: var(--bl-ink); font: var(--bl-display-weight) 17px/1.4 var(--bl-font-display); letter-spacing: -.01em; }
.bl-formula-cells { display: grid; gap: 6px; }
.bl-formula-cells > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  padding: 10px 13px;
  border: 1px solid var(--bl-line);
  border-radius: var(--bl-r-xs);
  background: var(--bl-paper);
}
.bl-formula-cells dt { color: var(--bl-ink-soft); font: 500 11px/1.5 var(--bl-font-mono); }
.bl-formula-cells dd { color: var(--bl-accent-safe); font: 600 12px/1.5 var(--bl-font-mono); }

/* ---------------------------------------------------------------- glossary */
.bl-docs-glossary { padding-block: clamp(16px, 2vw, 26px); }
.bl-glossary { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 clamp(22px, 3vw, 48px); }
.bl-gloss {
  display: grid;
  gap: 7px;
  align-content: start;
  padding-block: 18px;
  border-block-start: 1px solid var(--bl-line);
}
.bl-gloss:nth-child(1), .bl-gloss:nth-child(2) { border-block-start: 0; }
.bl-gloss p { color: var(--bl-muted); font: 400 13.5px/1.7 var(--bl-font-body); }
.bl-gloss .bl-link { justify-self: start; font: 500 12.5px/1.6 var(--bl-font-body); }

.bl-docs-anchors { position: absolute; width: 1px; height: 1px; overflow: hidden; }

@media (max-width: 1080px) {
  .bl-docs-chips { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 780px) {
  .bl-clause-list, .bl-glossary { grid-template-columns: minmax(0, 1fr); }
  .bl-clause:nth-child(2), .bl-gloss:nth-child(2) { border-block-start: 1px solid var(--bl-line); }
  .bl-docs-chips { grid-template-columns: minmax(0, 1fr); }
}
</style>
