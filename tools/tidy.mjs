#!/usr/bin/env node
// Docks tidy-up (Apoorva's rule, 16 Nov 2026): keep the app uncluttered.
//   OT lists ............ 5 days   (data/ot.json items + data/private/ot-YYYY-MM-DD.enc.json)
//   NBA games ........... 5 days   (counted back from the newest game in data/nba.json)
//   Painting of the day . 15 days  (data/art.json history)
//   Things I love facts . 15 days  (data/loves.json history)
//   Articles ............ 7 days   (data/articles.json items, by date added; Apoorva asked for this on 20 Nov 2026)
// NEVER trimmed: cases / SLCM records, schedule, advances, books, topics, bites, atotw or any other academic data.
//
//   node tools/tidy.mjs           trim and print what was removed (run before committing data updates)
import { readFileSync, writeFileSync, existsSync, unlinkSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DATA = join(ROOT, 'data');
const KEEP = { ot: 5, nba: 5, art: 15, loves: 15, articles: 7 };
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const todayIndia = () => new Date(Date.now() + 5.5 * 36e5).toISOString().slice(0, 10);
const addDays = (iso, n) => { const d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
const read = f => JSON.parse(readFileSync(join(DATA, f), 'utf8'));
const write = (f, o) => writeFileSync(join(DATA, f), JSON.stringify(o, null, 1) + '\n');
// NBA dates are "Nov 9" with no year: Jul–Dec belong to the season's first year, Jan–Jun to the next.
const nbaIso = k => { const [m, d] = String(k).split(' '); const i = MON.indexOf(m); return i < 0 ? '' : `${i >= 6 ? 2003 : 2004}-${String(i + 1).padStart(2, '0')}-${String(+d).padStart(2, '0')}`; };

const today = todayIndia();
const log = [];

if (existsSync(join(DATA, 'ot.json'))) {
  const j = read('ot.json'); const from = addDays(today, -(KEEP.ot - 1)); const n = j.items.length;
  j.items = j.items.filter(r => !r.date || r.date >= from);
  if (j.items.length !== n) { write('ot.json', j); log.push(`ot.json: removed ${n - j.items.length} rows before ${from}`); }
}

const PRIV = join(DATA, 'private'), INDEX = join(PRIV, 'index.json');
if (existsSync(INDEX)) {
  const idx = JSON.parse(readFileSync(INDEX, 'utf8')); const from = addDays(today, -(KEEP.ot - 1)); const n = idx.files.length;
  idx.files = idx.files.filter(f => {
    const m = f.match(/^ot-(\d{4}-\d{2}-\d{2})\.enc\.json$/);
    if (m && m[1] < from) { const p = join(PRIV, f); if (existsSync(p)) unlinkSync(p); return false; }
    return true;
  });
  if (idx.files.length !== n) { writeFileSync(INDEX, JSON.stringify(idx, null, 1) + '\n'); log.push(`private: removed ${n - idx.files.length} old OT files`); }
}

if (existsSync(join(DATA, 'nba.json'))) {
  const j = read('nba.json');
  if (j.games && j.games.length) {
    const ds = j.games.map(g => nbaIso(g[0])).filter(Boolean).sort(); const from = addDays(ds[ds.length - 1], -(KEEP.nba - 1)); const n = j.games.length;
    j.games = j.games.filter(g => { const x = nbaIso(g[0]); return !x || x >= from; });
    if (j.games.length !== n) { write('nba.json', j); log.push(`nba.json: removed ${n - j.games.length} older games`); }
  }
}

for (const f of ['art', 'loves']) {
  if (!existsSync(join(DATA, f + '.json'))) continue;
  const j = read(f + '.json'); const from = addDays(today, -(KEEP[f] - 1)); const n = (j.history || []).length;
  j.history = (j.history || []).filter(h => !h.date || h.date >= from);
  if (j.history.length !== n) { write(f + '.json', j); log.push(`${f}.json: removed ${n - j.history.length} entries before ${from}`); }
}

if (existsSync(join(DATA, 'articles.json'))) {
  const j = read('articles.json'); const from = addDays(today, -(KEEP.articles - 1)); const n = (j.items || []).length;
  j.items = (j.items || []).filter(a => !a.added || a.added >= from);
  if (j.items.length !== n) { write('articles.json', j); log.push(`articles.json: removed ${n - j.items.length} articles added before ${from}`); }
}

console.log(log.length ? log.join('\n') : 'Nothing to tidy.');
