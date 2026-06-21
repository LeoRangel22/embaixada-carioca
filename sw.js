const CACHE_VERSION = 'ec-assets-v2026-06-21-p0';
const ASSET_PATTERNS = [/^\/assets\//, /^\/fonts\//];
const OFFLINE_URL = '/offline.html';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then(cache => cache.add(OFFLINE_URL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (url.origin !== location.origin || event.request.method !== 'GET') return;

  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() =>
        caches.open(CACHE_VERSION).then(cache => cache.match(OFFLINE_URL))
      )
    );
    return;
  }

  if (!ASSET_PATTERNS.some(rx => rx.test(url.pathname))) return;
  event.respondWith(caches.open(CACHE_VERSION).then(cache => cache.match(event.request).then(cached => {
    const network = fetch(event.request).then(response => { if (response && response.ok) cache.put(event.request, response.clone()); return response; }).catch(() => cached);
    return cached || network;
  })));
});
