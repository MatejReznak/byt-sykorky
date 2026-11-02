// jednoduchý service worker: vždy najprv sieť (aby bola stránka aktuálna), bez siete posledná uložená verzia
const C="byt18-v1";
self.addEventListener("install",e=>self.skipWaiting());
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);
  if(e.request.method!=="GET"||u.hostname==="api.github.com")return; // rozloženie sa nikdy necachuje
  e.respondWith(fetch(e.request).then(r=>{if(r.ok){const c=r.clone();caches.open(C).then(x=>x.put(e.request,c));}return r;}).catch(()=>caches.match(e.request)));});
