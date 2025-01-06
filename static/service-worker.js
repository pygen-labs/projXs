const CACHE_NAME = "projxs-cache-v1";
const urlsToCache = [
  "/",
  "/index.html",
  "/main.html",
  "/terms.html",
  "/static/css/styles.css", // Add your CSS files
  "/static/js/scripts.js",  // Add your JS files
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
