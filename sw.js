// Service Worker — Embaixada Carioca
// Versão: 1.0.0 | Cache offline para turistas sem sinal no bondinho

const CACHE_NAME = 'embaixada-carioca-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/cafe-da-manha.html',
  '/almoco.html',
  '/entardecer.html',
  '/eventos.html',
  '/cardapio.html',
  '/guia-do-rio.html',
  '/manifest.json',
  '/assets/logo-areia.svg',
  '/assets/logo-azul.svg',
  '/assets/logo-amarelo.svg',
  '/assets/hero.jpg',
  '/assets/cafe-da-manha-mesa-opt.jpg',
  '/assets/almoco-mesa-opt.jpg',
  '/assets/entardecer-banda-opt.jpg',
  '/assets/evento-chandon-opt.jpg',
];

// Instalar e cachear assets estáticos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Ativar e limpar caches antigos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Estratégia: Cache First para assets, Network First para HTML
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Ignorar requisições externas (TagMe, WhatsApp, etc.)
  if (url.origin !== location.origin) return;

  // Assets (imagens, SVGs): Cache First
  if (request.destination === 'image' || url.pathname.startsWith('/assets/')) {
    event.respondWith(
      caches.match(request).then((cached) => {
        return cached || fetch(request).then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          return response;
        });
      })
    );
    return;
  }

  // HTML: Network First com fallback para cache
  if (request.destination === 'document') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          return response;
        })
        .catch(() => caches.match(request).then((cached) => cached || caches.match('/')))
    );
    return;
  }
});
