const CACHE_NAME = 'artstyle-v1';
const ASSETS = [
  './',
  './index.html',
  './logo.png',
  './manifest.json',
  './model.onnx'
];

// Instalación: Forzamos la activación inmediata
self.addEventListener('install', (event) => {
  self.skipWaiting(); 
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Activación: Limpiamos cachés antiguas y tomamos el control de las pestañas
self.addEventListener('activate', (event) => {
  event.waitUntil(
    Promise.all([
      self.clients.claim(),
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cache) => {
            if (cache !== CACHE_NAME) {
              return caches.delete(cache);
            }
          })
        );
      })
    ])
  );
});

// Estrategia: Primero red, si falla, caché (para que siempre intente buscar lo nuevo)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});