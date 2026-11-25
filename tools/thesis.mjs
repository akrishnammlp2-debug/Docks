#!/usr/bin/env node
// Thesis tracker: add TURP cases picked from a urology list.
//
//   node tools/thesis.mjs add <plain.json> [--replace]
//
// <plain.json> (kept OUTSIDE the repo, deleted afterwards):
//   { "date": "2026-11-26", "cases": [ { "patient": "...", "age": "68 M", "uhid": "...",
//       "procedure": "TURP", "time": "09:00", "ot": "...", "unit": "...", "surgeon": "...", "notes": "..." } ] }
//
// Only TURP cases go in (not TURBT). The tool refuses anything that doesn't look like TURP.
// Public fields (date, time, OT, procedure, unit, surgeon, notes) go to data/thesis.json.
// Name · age sex · UHID are locked to the paired devices in data/private/thesis-<date>.enc.json.
// A date already in the tracker is refused unless --replace (replacing keeps the same ids in order).
// Thesis data is never pruned.
import { readFileSync, writeFileSync, unlinkSync, mkdtempSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const PUB = join(ROOT, 'data', 'thesis.json');
export const isTurp = p => /\bTURP\b|trans\s*-?\s*urethral\s+resection\s+of\s+(the\s+)?prostate/i.test(p || '') && !/\bTURBT\b|bladder\s+tumou?r|ha?emorrh?oid/i.test(p || '');

const [cmd, file, flag] = process.argv.slice(2);
if (cmd !== 'add' || !file) { console.log('usage: node tools/thesis.mjs add <plain.json> [--replace]'); process.exit(1); }
const plain = JSON.parse(readFileSync(file, 'utf8'));
const date = plain.date;
if (!/^\d{4}-\d{2}-\d{2}$/.test(date || '')) throw new Error('date must be YYYY-MM-DD');
const cases = (plain.cases || []);
const bad = cases.filter(c => !isTurp(c.procedure));
if (bad.length) throw new Error('not TURP: ' + bad.map(c => c.procedure).join(' | '));
const khsb = cases.filter(c => /\bKHS/i.test([c.ward, c.notes].join(' ')));
if (khsb.length) throw new Error('KHSB ward cases are not added to the thesis: ' + khsb.map(c => c.procedure).join(' | '));
if (!cases.length) { console.log('no TURP cases; nothing added'); process.exit(0); }

const pub = JSON.parse(readFileSync(PUB, 'utf8'));
const had = pub.items.filter(r => r.date === date);
if (had.length && flag !== '--replace') throw new Error(`${date} already has ${had.length} thesis case(s). Use --replace to redo that day.`);
pub.items = pub.items.filter(r => r.date !== date);

const priv = { app: 'study-desk-private', updated: new Date().toISOString(), thesis: {} };
cases.forEach((c, i) => {
  const id = `th-${date}-${String(i + 1).padStart(2, '0')}`;
  const row = { id, date, order: i + 1 };
  for (const k of ['time', 'ot', 'procedure', 'unit', 'surgeon', 'notes']) if (c[k] != null && String(c[k]).trim()) row[k] = String(c[k]).trim();
  pub.items.push(row);
  priv.thesis[id] = [c.patient, c.age, c.uhid].map(x => (x || '').toString().trim()).join(' · ');
});
pub.items.sort((a, b) => a.date.localeCompare(b.date) || a.order - b.order);
pub.updated = new Date().toISOString().slice(0, 10);
writeFileSync(PUB, JSON.stringify(pub, null, 1) + '\n');

const tmp = join(mkdtempSync(join(tmpdir(), 'thesis-')), 'plain.json');
writeFileSync(tmp, JSON.stringify(priv));
try { execFileSync('node', [join(ROOT, 'tools', 'lock.mjs'), 'lock', tmp, 'thesis-' + date], { stdio: 'inherit' }); }
finally { unlinkSync(tmp); }
console.log(`added ${cases.length} TURP case(s) for ${date}`);
