#!/usr/bin/env node
// Checks the ABG flashcard generator (v5.79): every scenario must give values that obey Henderson–Hasselbalch
// and an answer whose disorders match the scenario. Run after editing ABG_SC or abgRead in index.html:
//   node tools/flash_test.mjs
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const src = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '..', 'index.html'), 'utf8');
const code = src.match(/\/\* ---------- v5\.79[\s\S]*?function fcShow\(\)[^\n]*\n/)[0];
const r1 = x => Math.round(x * 10) / 10;
const { ABG_SC, abgMake } = new Function('D', 'state', 'esc', 'today', 'r1', code + '; return { ABG_SC, abgMake };')({}, { settings: {} }, String, () => '2026-11-23', r1);
let bad = 0;
for (const sc of ABG_SC) {
  let fail = 0, hh = 0;
  for (let i = 0; i < 500; i++) { const r = abgMake(sc, 's' + i); if (!r) { fail++; continue; }
    const ph = 6.1 + Math.log10(r.v.hco3 / (0.03 * r.v.pco2)); if (Math.abs(ph - r.v.ph) > 0.006) hh++; }
  const ok = fail <= 25 && !hh; if (!ok) bad++;
  console.log((ok ? 'ok  ' : 'FAIL') + ' ' + sc.id.padEnd(8) + ` no-fit ${fail}/500, HH errors ${hh}`);
}
process.exit(bad ? 1 : 0);
