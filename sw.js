// JALEP Service Worker v3 — cache versioned for auto-invalidation
const CACHE_NAME = "jalep-v3-2026-09-16";
const STATIC_ASSETS = [
  "/jalep-mano/",
  "/jalep-mano/index.html",
  "/jalep-mano/servicos.html",
  "/jalep-mano/sobre.html",
  "/jalep-mano/lab.html",
  "/jalep-mano/contato.html",
  "/jalep-mano/faq.html",
  "/jalep-mano/portfolio.html",
  "/jalep-mano/timeline.html",
  "/jalep-mano/stack.html",
  "/jalep-mano/team.html",
  "/jalep-mano/pricing.html",
  "/jalep-mano/blog.html",
  "/jalep-mano/docs.html",
  "/jalep-mano/changelog.html",
  "/jalep-mano/status.html",
  "/jalep-mano/jalepos.html",
  "/jalep-mano/terminal.html",
  "/jalep-mano/wallpaper.html",
  "/jalep-mano/hardware.html",
  "/jalep-mano/parceiros.html",
  "/jalep-mano/depoimentos.html",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  // Activate immediately — don't wait for old SW to die
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  // Take control of all clients immediately
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  const url = new URL(event.request.url);

  // Never cache API calls or non-GET requests
  if (url.hostname === 'generativelanguage.googleapis.com') return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetched = fetch(event.request).then((response) => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => cached);
      return cached || fetched;
    })
  );
});
