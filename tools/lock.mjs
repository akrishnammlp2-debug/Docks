#!/usr/bin/env node
// Study Desk private sync: lock private data so only paired phones can open it.
// Contains no secrets. Plain (unlocked) private data must NEVER be committed to this repository.
//
//   node tools/lock.mjs add-device "SD1-..." "Apoorva's iPhone"   pair a device (its public code only)
//   node tools/lock.mjs lock <plain.json> <name>                    write data/private/<name>.enc.json + update index
//   node tools/lock.mjs prune                                        drop ot-YYYY-MM-DD files older than 14 days
//   node tools/lock.mjs list                                         show paired devices and locked files
//
// <plain.json> uses the private-file format: { "app": "study-desk-private", "updated": "...",
//   "profile"?, "roster"?, "presenters"?, "ot"?: { "<ot id>": "Name · age sex · UHID" }, "cases"?: { "<n>": "UHID" } }
// Names: roster-YYYY-MM, presenters-YYYY-MM, profile, cases, ot-YYYY-MM-DD (one file each; same name = replaced).
import { readFileSync, writeFileSync, mkdirSync, existsSync, unlinkSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const { subtle } = globalThis.crypto;
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DEVICES = join(ROOT, 'keys', 'devices.json');
const PRIV = join(ROOT, 'data', 'private');
const INDEX = join(PRIV, 'index.json');

const b64u = {
  enc: buf => Buffer.from(buf).toString('base64url'),
  dec: s => new Uint8Array(Buffer.from(s, 'base64url')),
};
const readJson = (p, d) => (existsSync(p) ? JSON.parse(readFileSync(p, 'utf8')) : d);
const writeJson = (p, o) => { mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, JSON.stringify(o, null, 1) + '\n'); };
const rnd = n => globalThis.crypto.getRandomValues(new Uint8Array(n));

async function kidOf(raw) {
  const h = new Uint8Array(await subtle.digest('SHA-256', raw));
  return [...h.slice(0, 4)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function addDevice(code, name) {
  if (!code || !code.startsWith('SD1-')) throw new Error('Phone code must start with SD1-');
  const raw = b64u.dec(code.slice(4).trim());
  await subtle.importKey('raw', raw, { name: 'ECDH', namedCurve: 'P-256' }, true, []); // validates the key
  const kid = await kidOf(raw);
  const list = readJson(DEVICES, []).filter(d => d.kid !== kid);
  list.push({ kid, name: name || 'device', pub: b64u.enc(raw), added: new Date().toISOString().slice(0, 10) });
  writeJson(DEVICES, list);
  console.log(`paired ${name} (kid ${kid}). Re-lock every file in data/private so this device can open them.`);
}

async function lock(plainPath, name) {
  if (!/^[a-z0-9-]+$/.test(name || '')) throw new Error('name must be like ot-2026-11-12 or roster-2026-11');
  const plain = JSON.parse(readFileSync(plainPath, 'utf8'));
  if (plain.app !== 'study-desk-private') throw new Error('plain file must have "app": "study-desk-private"');
  const devices = readJson(DEVICES, []);
  if (!devices.length) throw new Error('no paired devices in keys/devices.json');

  const cekRaw = rnd(32);
  const cek = await subtle.importKey('raw', cekRaw, 'AES-GCM', false, ['encrypt']);
  const iv = rnd(12);
  const ct = await subtle.encrypt({ name: 'AES-GCM', iv }, cek, new TextEncoder().encode(JSON.stringify(plain)));

  const recipients = [];
  for (const d of devices) {
    const pub = await subtle.importKey('raw', b64u.dec(d.pub), { name: 'ECDH', namedCurve: 'P-256' }, false, []);
    const eph = await subtle.generateKey({ name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']);
    const shared = new Uint8Array(await subtle.deriveBits({ name: 'ECDH', public: pub }, eph.privateKey, 256));
    const info = new TextEncoder().encode('studydesk-v1|' + d.kid);
    const mat = new Uint8Array(shared.length + info.length); mat.set(shared); mat.set(info, shared.length);
    const kek = await subtle.importKey('raw', await subtle.digest('SHA-256', mat), 'AES-GCM', false, ['encrypt']);
    const wiv = rnd(12);
    const wk = await subtle.encrypt({ name: 'AES-GCM', iv: wiv }, kek, cekRaw);
    recipients.push({ kid: d.kid, epk: b64u.enc(await subtle.exportKey('raw', eph.publicKey)), iv: b64u.enc(wiv), wk: b64u.enc(wk) });
  }
  const file = name + '.enc.json';
  writeJson(join(PRIV, file), { v: 1, alg: 'ECDH-P256+SHA256+A256GCM', created: new Date().toISOString(), recipients, iv: b64u.enc(iv), ct: b64u.enc(ct) });
  const idx = readJson(INDEX, { files: [] });
  if (!idx.files.includes(file)) idx.files.push(file);
  idx.files.sort((a, b) => order(a) - order(b) || a.localeCompare(b));
  idx.updated = new Date().toISOString();
  writeJson(INDEX, idx);
  console.log(`locked ${name} for ${devices.length} device(s)`);
}
// profile/roster/presenters/cases first, then OT days oldest to newest
const order = f => (f.startsWith('ot-') ? 1 : 0);

function prune() {
  const keep = new Date(Date.now() - 14 * 864e5).toISOString().slice(0, 10);
  const idx = readJson(INDEX, { files: [] });
  idx.files = idx.files.filter(f => {
    const m = f.match(/^ot-(\d{4}-\d{2}-\d{2})\.enc\.json$/);
    if (m && m[1] < keep) { const p = join(PRIV, f); if (existsSync(p)) unlinkSync(p); console.log('removed', f); return false; }
    return true;
  });
  writeJson(INDEX, idx);
}

const [cmd, a, b] = process.argv.slice(2);
try {
  if (cmd === 'add-device') await addDevice(a, b);
  else if (cmd === 'lock') await lock(a, b);
  else if (cmd === 'prune') prune();
  else if (cmd === 'list') console.log({ devices: readJson(DEVICES, []).map(d => `${d.name} (${d.kid})`), files: readJson(INDEX, { files: [] }).files });
  else console.log('usage: add-device | lock | prune | list (see top of file)');
} catch (e) { console.error('error:', e.message); process.exit(1); }
