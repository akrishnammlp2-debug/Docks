// Inemuri (formerly Study Desk / Docks) offline support. Bump CACHE whenever index.html, icons or manifest change.
// The data folder is NOT cached here: the app keeps its own saved copy of each data file.
const CACHE = 'study-desk-v187';
const PICS = 'study-desk-pics'; // Off duty pictures (Wikimedia), kept a few days so they open instantly
const PIC_DAYS = 3, PIC_MAX = 80;
const ECGP = 'inemuri-ecg-pics'; // real ECG tracings (Wikimedia Commons, ?ecg=1): kept with no expiry so flashcards and ECG notes work offline
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-180.png', './icon-512.png', './img/side-sky.jpg'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE && k !== PICS && k !== ECGP).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const isPic = url => (/(^|\.)wikimedia\.org$/.test(url.hostname) && (url.pathname.includes('/Special:FilePath/') || url.hostname === 'upload.wikimedia.org')) || url.hostname === 'covers.openlibrary.org' || url.hostname === 'static.tvmaze.com' || /\.mzstatic\.com$/.test(url.hostname);

async function picture(req) {
  const c = await caches.open(PICS);
  const hit = await c.match(req.url);
  if (hit) { const at = +(hit.headers.get('x-sd-at') || 0); if (!at || Date.now() - at < PIC_DAYS * 864e5 || hit.type === 'opaque') return hit; }
  try {
    const res = await fetch(req);
    if (res.ok || res.type === 'opaque') {
      c.put(req.url, res.clone()).then(async () => { const keys = await c.keys(); for (let i = 0; i < keys.length - PIC_MAX; i++) c.delete(keys[i]); });
    }
    return res;
  } catch (err) { if (hit) return hit; throw err; }
}

async function ecgPic(req) {
  const c = await caches.open(ECGP);
  const hit = await c.match(req.url);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok || res.type === 'opaque') c.put(req.url, res.clone());
  return res;
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (isPic(url) && url.searchParams.get('ecg') === '1') { e.respondWith(ecgPic(req)); return; }
  if (isPic(url)) { e.respondWith(picture(req)); return; }
  if (url.origin !== location.origin) return;
  if (url.pathname.includes('/data/')) return; // always straight to the network
  if (req.mode === 'navigate') {
    // newest page from GitHub, but don't keep you waiting on weak Wi-Fi: after 3 s use the saved copy
    const net = fetch(req, { cache: 'no-store' }).then(res => { const copy = res.clone(); caches.open(CACHE).then(c => c.put('./index.html', copy)); return res; });
    net.catch(() => {});
    e.respondWith(Promise.race([net, new Promise(r => setTimeout(r, 3000)).then(() => caches.match('./index.html')).then(h => h || net)]).catch(() => caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
});

// phone notifications from Docks (sent by the private sync repository's notification job)
self.addEventListener('push', e => {
  let d = {}; try { d = e.data ? e.data.json() : {}; } catch (_) { d = { title: 'Inemuri', body: e.data ? e.data.text() : '' }; }
  e.waitUntil(self.registration.showNotification(d.title || 'Inemuri', { body: d.body || '', tag: d.tag || undefined, icon: 'icon-180.png', badge: 'icon-180.png', data: { tab: d.tab || 'today' } }));
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = new URL('./#' + ((e.notification.data && e.notification.data.tab) || 'today'), self.registration.scope).href;
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
    for (const c of list) { if ('focus' in c) { c.navigate ? c.navigate(url).catch(() => {}) : null; return c.focus(); } }
    return self.clients.openWindow ? self.clients.openWindow(url) : null;
  }));
});
