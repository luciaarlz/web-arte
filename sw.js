const CACHE_NAME = 'art-vision-v1';
const assets = [
  './',
  './index.html',
  './manifest.json',
  './model.onnx',
  'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(assets)));
});

self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(res => res || fetch(e.request)));
});