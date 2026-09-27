// Offline support for the GitHub Pages build.
// Page: network first, falls back to the cached copy. Tiles and CDN assets: cache first.
// Tiles live in a cache that survives new deploys, so a saved map stays saved.
const VERSION = '__VERSION__';
const PAGE_CACHE = 'page-' + VERSION;
const TILE_CACHE = 'tiles-v1';
const CDN_CACHE = 'cdn-v1';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'offline.json',
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(PAGE_CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys
    .filter(k => k.startsWith('page-') && k !== PAGE_CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
async function cacheFirst(cacheName, req) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req) || (cacheName !== PAGE_CACHE && await caches.match(req));
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok || res.type === 'opaque') cache.put(req, res.clone());
  return res;
}
async function networkFirst(req) {
  const cache = await caches.open(PAGE_CACHE);
  try {
    const res = await fetch(req);
    if (res.ok) cache.put(req, res.clone());
    return res;
  } catch (err) {
    return (await cache.match(req)) || (await cache.match('index.html')) || Response.error();
  }
}
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin === location.origin) {
    if (url.pathname.includes('/tiles/')) return e.respondWith(cacheFirst(TILE_CACHE, req));
    if (req.mode === 'navigate' || url.pathname.endsWith('.json')) return e.respondWith(networkFirst(req));
    return e.respondWith(cacheFirst(PAGE_CACHE, req));
  }
  if (/^(cdnjs\.cloudflare\.com|fonts\.googleapis\.com|fonts\.gstatic\.com)$/.test(url.hostname))
    return e.respondWith(cacheFirst(CDN_CACHE, req));
});
