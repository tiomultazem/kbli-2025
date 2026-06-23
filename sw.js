const CACHE_NAME = 'kbli2025-cache-v1';
const ASSETS = [
  './',
  './index.html',
  './index.css?v=1.5',
  './logo bps.png',
  './01_kategori.json',
  './02_golongan_pokok.json',
  './03_golongan.json',
  './04_subgolongan.json',
  './05_kelompok.json',
  './manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const fetchPromise = fetch(e.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(e.request, networkResponse.clone());
          });
        }
        return networkResponse;
      }).catch(() => {
        // Abaikan error fetch saat offline
      });
      return cachedResponse || fetchPromise;
    })
  );
});
