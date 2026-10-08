// Offline support for the GitHub Pages copy. Network first, so a new build shows up when you're
// online; after 4 seconds without an answer (a train tunnel), serve the cached page instead.
const CACHE = "konbini-ears-v2";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icons/apple-touch-icon.png"];

self.addEventListener("install", e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)));
});
self.addEventListener("activate", e => e.waitUntil(
  caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim())
));

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  const cached = () => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match("./index.html"));
  const network = fetch(e.request).then(r => {
    if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
    return r;
  });
  const slow = new Promise(resolve => setTimeout(resolve, 4000)).then(cached);
  e.respondWith(Promise.race([network.catch(cached), slow.then(r => r || network)]));
});
