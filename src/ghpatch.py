# z artifact verzie (all/spajza.html) spraví verziu pre GitHub Pages: ukladanie rozloženia do súboru data/layout.json vo vetve "data" cez GitHub API
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
GH='''
/* ---------- GitHub: rozloženie je súbor data/layout.json vo vetve "data" (každé uloženie = commit) ---------- */
const GH={owner:"MatejReznak",repo:"byt-sykorky",path:"data/layout.json",branch:"data"};
function ghTok(){try{return localStorage.getItem("byt18-ghtok")||"";}catch(e){return "";}}
function ghHdr(){const t=ghTok();return t?{Authorization:"Bearer "+t,Accept:"application/vnd.github+json"}:{Accept:"application/vnd.github+json"};}
const ghUrl=()=>`https://api.github.com/repos/${GH.owner}/${GH.repo}/contents/${GH.path}`;
const b64e=s=>btoa(unescape(encodeURIComponent(s))),b64d=s=>decodeURIComponent(escape(atob(s.replace(/\\n/g,""))));
const ghStore={gh:true,sha:null,
  async get(){const r=await fetch(ghUrl()+"?ref="+GH.branch+"&t="+Date.now(),{headers:ghHdr(),cache:"no-store"});if(r.status===404)return{exists:false,data:()=>null};if(!r.ok)throw new Error("get "+r.status);
    const j=await r.json();this.sha=j.sha;const d=JSON.parse(b64d(j.content));return{exists:true,data:()=>d};},
  async set(d){if(!ghTok())throw new Error("notoken");const put=()=>fetch(ghUrl(),{method:"PUT",headers:{...ghHdr(),"Content-Type":"application/json"},
      body:JSON.stringify({message:"Uloženie rozloženia",branch:GH.branch,content:b64e(JSON.stringify(d)),...(this.sha?{sha:this.sha}:{})})});
    let r=await put();if(r.status===409||r.status===422){try{await this.get();}catch(e){}r=await put();}
    if(!r.ok)throw new Error("put "+r.status);const j=await r.json();this.sha=j.content&&j.content.sha;}};
function ghLink(){const t=prompt("Vlož GitHub token (fine-grained, repozitár byt-sykorky, Contents: Read and write).\\nUloží sa len v tomto zariadení. Prázdne = odpojiť.",ghTok());
  if(t===null)return;try{if(t.trim())localStorage.setItem("byt18-ghtok",t.trim());else localStorage.removeItem("byt18-ghtok");}catch(e){}location.reload();}
async function ghBoot(){statusEl.style.cursor="pointer";statusEl.title="Klikni: prepojenie s GitHubom (ukladanie zo všetkých zariadení)";statusEl.onclick=ghLink;
  store=ghStore;statusEl.textContent="Načítava sa z GitHubu…";
  try{const snapD=await store.get();if(snapD.exists){const d=snapD.data();if(d&&d.json){applyState(JSON.parse(d.json));sel=null;render();renderPanel();}}
    statusEl.textContent=ghTok()?"Uložené na GitHube":"Len na čítanie – klikni a prepoj GitHub";}
  catch(e){statusEl.textContent="GitHub nedostupný – ukladá sa v tomto prehliadači";store=null;}
  // pri návrate do okna načítaj novšiu verziu z iného zariadenia (ak tu nie sú neuložené zmeny)
  document.addEventListener("visibilitychange",async()=>{if(document.hidden||!store||/Neulož|Ukladá/.test(statusEl.textContent))return;
    try{const snapD=await store.get();const d=snapD.exists&&snapD.data();if(d&&d.json&&d.json!==JSON.stringify({items,step,showNames,showDims,showLines})){applyState(JSON.parse(d.json));sel=null;render();renderPanel();if(window.__rebuild3d)window.__rebuild3d();}}catch(e){}});
  const dl={save:async({filename,data})=>{const a=document.createElement("a");a.href=URL.createObjectURL(data);a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),4000);}};
  pngBtn.hidden=false;pngBtn.onclick=()=>busy(pngBtn,()=>exportPng(dl));pdfBtn.hidden=false;pdfBtn.onclick=()=>busy(pdfBtn,()=>exportPdf(dl));}
'''
rep('/* ---------- boot ---------- */',GH+'/* ---------- boot ---------- */')
rep('if(!use){statusEl.textContent="Ukladá sa v tomto prehliadači";return;}','if(!use){await ghBoot();return;}')
rep('try{await store.set(data);statusEl.textContent="Uložené";}\n      catch(e){statusEl.textContent="Uložené len v tomto prehliadači";}',
    'try{await store.set(data);statusEl.textContent=store.gh?"Uložené na GitHube":"Uložené";}\n      catch(e){statusEl.textContent=store.gh&&e.message==="notoken"?"Len v tomto zariadení – klikni a prepoj GitHub":"Uložené len v tomto prehliadači";}')
rep('}, now?50:700);','}, now?50:(store&&store.gh?3000:700));')
# aplikácia (PWA): ikona, manifest, service worker
rep('<meta charset=utf8>','<meta charset=utf8><link rel="manifest" href="manifest.webmanifest"><link rel="icon" type="image/png" href="icons/favicon-32.png"><link rel="apple-touch-icon" href="icons/apple-touch-icon.png"><meta name="theme-color" content="#1d5fd6"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Byt 1.8"><meta name="apple-mobile-web-app-status-bar-style" content="default">')
import re
s=re.sub(r'<title>[^<]*</title>','<title>Byt 1.8 Sýkorky</title>',s,count=1)
s=s.replace('</body>','<script>if("serviceWorker" in navigator)navigator.serviceWorker.register("sw.js").catch(()=>{});</script></body>',1)
open(dst,'w').write(s);print('ok',len(s))
