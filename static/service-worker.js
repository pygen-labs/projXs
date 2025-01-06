const CACHE_NAME = "projxs-cache-v1";
const urlsToCache = [
  "/",
  "/main",
  "/terms.html",
  "/static/icons/icon-512x512.png",
  "/static/manifest.json"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
