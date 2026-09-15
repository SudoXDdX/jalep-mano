// JALEP Service Worker v2
const CACHE_NAME = "jalep-v2-cache";
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
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
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
