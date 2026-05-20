const CACHE_VERSION = 'ec-assets-v2026-05-20';
const ASSET_PATTERNS = [/^\/assets\//, /^\/fonts\//];
self.addEventListener('install', event => { self.skipWaiting(); });
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (url.origin !== location.origin || event.request.method !== 'GET') return;
  if (!ASSET_PATTERNS.some(rx => rx.test(url.pathname))) return;
  event.respondWith(caches.open(CACHE_VERSION).then(cache => cache.match(event.request).then(cached => {
    const network = fetch(event.request).then(response => { if (response && response.ok) cache.put(event.request, response.clone()); return response; }).catch(() => cached);
    return cached || network;
  })));
});
