// Embaixada Carioca — Service Worker v2.0
const CACHE_NAME = 'embaixada-carioca-v2';
const OFFLINE_URL = '/offline.html';

const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/cafe-da-manha.html',
  '/almoco.html',
  '/entardecer.html',
  '/eventos.html',
  '/cardapio.html',
  '/guia-do-rio.html',
  '/offline.html',
  '/manifest.json',
  '/assets/logo-branco.svg',
  '/assets/icon-192.png',
  '/assets/icon-512.png',
];

// Instalar e pré-cachear recursos essenciais
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRECACHE_URLS);
    }).then(() => self.skipWaiting())
  );
});

// Ativar e limpar caches antigos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Estratégia: Network First para HTML, Cache First para assets
self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    // Para navegação: tenta rede, fallback para cache, fallback para offline
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
          return response;
        })
        .catch(() => {
          return caches.match(event.request)
            .then(cached => cached || caches.match(OFFLINE_URL));
        })
    );
  } else if (
    event.request.url.includes('/assets/') ||
    event.request.url.includes('.webp') ||
    event.request.url.includes('.png') ||
    event.request.url.includes('.svg') ||
    event.request.url.includes('.css') ||
    event.request.url.includes('.js')
  ) {
    // Para assets: Cache First
    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(response => {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
          return response;
        });
      })
    );
  }
});
