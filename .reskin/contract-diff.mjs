#!/usr/bin/env node
/**
 * Fast source-contract diff against the frozen reskin baseline.
 * Prints the same issues/warnings verify.mjs would report for the source side,
 * without building or launching a browser.
 *
 *   node .reskin/contract-diff.mjs
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const SKILL = 'C:/Users/Administrator/.dsh/skills/reskin/scripts/inventory.mjs';
const { analyzeProject, contractDiff } = await import(pathToFileURL(SKILL).href);

const outDir = path.resolve('.reskin');
const baseline = JSON.parse(await fs.readFile(path.join(outDir, 'baseline', 'content-contract.json'), 'utf8'));
const current = await analyzeProject(process.cwd());
const diff = contractDiff(baseline, current.contentContract, { allowAdditions: true });

console.log(`archetype: ${current.archetype.id} (${current.archetype.family})  accent-anchor: ${(current.palette[0] || {}).hex}`);
console.log(`tokens: ${current.stats.staticTextTokens} text, ${current.stats.bindingTokens} bindings, ${current.stats.eventTokens} events · hash ${current.contentContractHash.slice(0, 12)}`);
console.log(`issues: ${diff.issues.length}`);
for (const issue of diff.issues) console.log(`  FAIL ${issue}`);
const additive = diff.warnings.filter((w) => w.startsWith('visibleText: added'));
console.log(`visible additions: ${additive.length} (these also fail the gate)`);
for (const w of additive) console.log(`  FAIL ${w}`);
const rest = diff.warnings.filter((w) => !w.startsWith('visibleText: added'));
console.log(`warnings: ${rest.length}`);
for (const w of rest.slice(0, 40)) console.log(`  warn ${w}`);
process.exitCode = diff.issues.length || additive.length ? 1 : 0;
