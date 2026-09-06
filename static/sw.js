/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Service Worker: Offline-First Caching & Mountain Corridor Resilience Sync
 */

const CACHE_NAME = 'nera-pwa-v3.0';
const STATIC_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/js/map.js',
  '/static/js/routing.js',
  '/static/js/prediction.js',
  '/static/js/simulation.js',
  '/static/js/supplies.js',
  '/static/js/fieldReport.js',
  '/static/js/alerts.js',
  '/static/manifest.json',
  '/static/icons/icon-192.svg',
  '/static/icons/icon-512.svg'
];

// Install Event: Precache application shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[NERA SW] Precaching app shell and offline GIS assets...');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Clean up outdated caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => {
          console.log('[NERA SW] Purging old cache:', key);
          return caches.delete(key);
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Cache-First for static assets, Network-First for dynamic API feeds
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Handle API requests: Network first with cached fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(networkResponse => {
          if (networkResponse && networkResponse.status === 200 && event.request.method === 'GET') {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
          }
          return networkResponse;
        })
        .catch(() => {
          // If offline, attempt serving from cache
          return caches.match(event.request).then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            return new Response(JSON.stringify({
              status: 'offline_mode',
              message: 'Zero-connectivity mountain pass mode active. Data loaded from local device cache.'
            }), {
              headers: { 'Content-Type': 'application/json' }
            });
          });
        })
    );
    return;
  }

  // Handle static assets & CDNs: Cache first, falling back to network
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then(networkResponse => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
        }
        return networkResponse;
      }).catch(err => {
        console.warn('[NERA SW] Offline asset fetch failed:', url.pathname);
      });
    })
  );
});
