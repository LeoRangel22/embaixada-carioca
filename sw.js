/* Embaixada Carioca Service Worker — performance cache */
const EC_CACHE = 'ec-static-2026-05-19.1';
const EC_ASSETS = [
  '/',
  '/assets/fonts/fonts.css',
  '/assets/logo-branco.svg',
  '/assets/hero-400w.webp',
  '/assets/hero-mobile.webp',
  '/assets/hero-800w.webp',
  '/assets/hero-1200w.webp',
  '/assets/hero.webp'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(EC_CACHE).then(cache => cache.addAll(EC_ASSETS)).catch(() => null)
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('ec-static-') && k !== EC_CACHE).map(k => caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isStatic = /\.(?:webp|jpg|jpeg|png|svg|css|js|woff2?)$/i.test(url.pathname);
  if (isStatic) {
    event.respondWith(
      caches.match(req).then(cached => cached || fetch(req).then(resp => {
        const copy = resp.clone();
        caches.open(EC_CACHE).then(cache => cache.put(req, copy)).catch(() => null);
        return resp;
      }).catch(() => cached))
    );
  }
});
