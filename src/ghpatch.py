# z artifact verzie (all/spajza.html) spraví verziu pre GitHub Pages: ukladanie rozloženia do súboru data/layout.json vo vetve "data" cez GitHub API
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
GH='''
/* ---------- GitHub: rozloženie je súbor data/layout.json vo vetve "data" (každé uloženie = commit) ---------- */
const GH={owner:"MatejReznak",repo:"byt-sykorky",branch:"data"};
const verPath=id=>id==="main"?"data/layout.json":`data/versions/${id}.json`;
function ghTok(){try{return localStorage.getItem("byt18-ghtok")||"";}catch(e){return "";}}
function ghHdr(){const t=ghTok();return t?{Authorization:"Bearer "+t,Accept:"application/vnd.github+json"}:{Accept:"application/vnd.github+json"};}
const ghUrl=p=>`https://api.github.com/repos/${GH.owner}/${GH.repo}/contents/${p}`;
const b64e=s=>btoa(unescape(encodeURIComponent(s))),b64d=s=>decodeURIComponent(escape(atob(s.replace(/\\n/g,""))));
// súbory vo vetve "data": layout.json (verzia 1), versions/<id>.json (ďalšie verzie), versions.json (zoznam a názvy)
const ghF={sha:{},
  async get(p){const r=await fetch(ghUrl(p)+"?ref="+GH.branch+"&t="+Date.now(),{headers:ghHdr(),cache:"no-store"});if(r.status===404){delete this.sha[p];return null;}if(!r.ok)throw new Error("get "+r.status);
    const j=await r.json();this.sha[p]=j.sha;return JSON.parse(b64d(j.content));},
  async put(p,d,msg){if(!ghTok())throw new Error("notoken");const go=()=>fetch(ghUrl(p),{method:"PUT",headers:{...ghHdr(),"Content-Type":"application/json"},
      body:JSON.stringify({message:msg,branch:GH.branch,content:b64e(JSON.stringify(d)),...(this.sha[p]?{sha:this.sha[p]}:{})})});
    let r=await go();if(r.status===409||r.status===422){try{await this.get(p);}catch(e){}r=await go();}
    if(!r.ok)throw new Error("put "+r.status);const j=await r.json();this.sha[p]=j.content&&j.content.sha;},
  async del(p,msg){if(!this.sha[p])await this.get(p);if(!this.sha[p])return;const r=await fetch(ghUrl(p),{method:"DELETE",headers:{...ghHdr(),"Content-Type":"application/json"},body:JSON.stringify({message:msg,branch:GH.branch,sha:this.sha[p]})});if(!r.ok)throw new Error("del "+r.status);delete this.sha[p];}};
let VERS=[{id:"main",name:"Verzia 1"}],VER=(()=>{try{return localStorage.getItem("byt18-ver")||"main";}catch(e){return "main";}})();
const ghStore={gh:true,
  async get(){const d=await ghF.get(verPath(VER));return d?{exists:true,data:()=>d}:{exists:false,data:()=>null};},
  async set(d){const n=(VERS.find(v=>v.id===VER)||{}).name||VER;await ghF.put(verPath(VER),d,"Uloženie: "+n);}};
function ghLink(){const t=prompt("Vlož GitHub token (fine-grained, repozitár byt-sykorky, Contents: Read and write).\\nUloží sa len v tomto zariadení. Prázdne = odpojiť.",ghTok());
  if(t===null)return;try{if(t.trim())localStorage.setItem("byt18-ghtok",t.trim());else localStorage.removeItem("byt18-ghtok");}catch(e){}location.reload();}
const isMob=()=>document.documentElement.dataset.dev==="mob";
function verUI(){let el=document.getElementById("verSel");if(!el){el=document.createElement("select");el.id="verSel";el.title="Verzia rozloženia";
    el.style.cssText="max-width:170px;min-height:34px;border:1px solid #c9cfd6;border-radius:8px;padding:0 6px;font:500 13px system-ui,sans-serif;background:#fff;color:#1b2430;margin-right:6px";
    statusEl.parentNode.insertBefore(el,statusEl);el.onchange=()=>verAction(el.value);}
  const o=VERS.map(v=>`<option value="v:${v.id}"${v.id===VER?" selected":""}>${v.name.replace(/</g,"&lt;")}</option>`).join("");
  el.innerHTML=o+(isMob()?"":`<option disabled>──────────</option><option value="new">＋ Nová verzia (kópia tejto)…</option><option value="ren">✎ Premenovať túto verziu…</option>${VER==="main"?"":'<option value="del">🗑 Zmazať túto verziu…</option>'}`);}
async function verFlush(){if(/Neulož|Ukladá/.test(statusEl.textContent)&&ghTok()&&!isMob()){clearTimeout(saveTimer);try{await ghStore.set({json:JSON.stringify({items,step,showNames,showDims,showLines}),updated:Date.now()});}catch(e){}}}
async function verLoad(id){await verFlush();VER=id;try{localStorage.setItem("byt18-ver",id);}catch(e){}statusEl.textContent="Načítava sa verzia…";
  try{const s=await ghStore.get();if(s.exists){const d=s.data();if(d&&d.json){applyState(JSON.parse(d.json));}}hist=[];undoBtn.disabled=true;sel=null;render();renderPanel();
    statusEl.textContent=isMob()?"Len na prezeranie":ghTok()?"Uložené na GitHube":"Len na čítanie – klikni a prepoj GitHub";}catch(e){statusEl.textContent="Verziu sa nepodarilo načítať";}verUI();}
async function verAction(v){const cur=VERS.find(x=>x.id===VER);
  if(v.startsWith("v:")){const id=v.slice(2);if(id!==VER)await verLoad(id);return;}
  verUI();if(!ghTok()){alert("Na vytváranie a úpravu verzií najprv prepoj GitHub (klikni na stav v hlavičke a vlož token).");return;}
  try{
    if(v==="new"){const n=prompt("Názov novej verzie (skopíruje sa aktuálne rozloženie):","Verzia "+(VERS.length+1));if(!n||!n.trim())return;
      await verFlush();const id="v"+Date.now().toString(36);statusEl.textContent="Vytvára sa verzia…";
      await ghF.put(verPath(id),{json:JSON.stringify({items,step,showNames,showDims,showLines}),updated:Date.now()},"Nová verzia: "+n.trim());
      VERS.push({id,name:n.trim()});await ghF.put("data/versions.json",{list:VERS},"Verzie: pridaná "+n.trim());await verLoad(id);}
    if(v==="ren"){const n=prompt("Nový názov verzie:",cur?cur.name:"");if(!n||!n.trim())return;cur.name=n.trim();await ghF.put("data/versions.json",{list:VERS},"Verzie: premenovaná na "+cur.name);verUI();}
    if(v==="del"&&VER!=="main"){if(!confirm(`Naozaj zmazať verziu „${cur.name}“? (V histórii na GitHube ostane.)`))return;
      clearTimeout(saveTimer);await ghF.del(verPath(VER),"Zmazaná verzia: "+cur.name);VERS=VERS.filter(x=>x.id!==VER);await ghF.put("data/versions.json",{list:VERS},"Verzie: zmazaná "+cur.name);VER="main";await verLoad("main");}
  }catch(e){alert("Nepodarilo sa: "+e.message);verUI();}}
async function ghBoot(){statusEl.style.cursor="pointer";statusEl.title="Klikni: prepojenie s GitHubom (ukladanie zo všetkých zariadení)";statusEl.onclick=ghLink;
  store=ghStore;statusEl.textContent="Načítava sa z GitHubu…";
  try{const vl=await ghF.get("data/versions.json");if(vl&&vl.list&&vl.list.length)VERS=vl.list;}catch(e){}
  if(!VERS.some(v=>v.id===VER))VER="main";verUI();
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
# na telefóne len na prezeranie: v pôdoryse sa nedá nič posúvať ani pridávať, nič sa neukladá
VIEW="document.documentElement.dataset.dev===\"mob\""
rep('  if(tool==="select"){\n    const hEl=','  if('+VIEW+'){drag={mode:"pan",sx:e.clientX,sy:e.clientY,vb:{...vb}};render();return;} // telefón: len posun a priblíženie\n  if(tool==="select"){\n    const hEl=')
rep('function save(now){\n','function save(now){\n  if('+VIEW+'){statusEl.textContent="Len na prezeranie";return;}\n')
s=s.replace('</head>','<style>html[data-dev=mob] #t-line,html[data-dev=mob] #t-rect,html[data-dev=mob] #undo,html[data-dev=mob] label[for=imp],html[data-dev=mob] #panel,html[data-dev=mob] #sheetbtn{display:none!important}</style></head>',1)
rep('    statusEl.textContent=ghTok()?"Uložené na GitHube":"Len na čítanie – klikni a prepoj GitHub";}','    statusEl.textContent='+VIEW+'?"Len na prezeranie":ghTok()?"Uložené na GitHube":"Len na čítanie – klikni a prepoj GitHub";}')
# obrázok: ikona pri pridaní odkazu na plochu + náhľad pri zdieľaní odkazu
U="https://matejreznak.github.io/byt-sykorky/"
rep('<meta charset=utf8>','<meta charset=utf8><link rel="icon" type="image/png" href="icons/favicon-32.png"><link rel="apple-touch-icon" href="icons/apple-touch-icon.png"><meta property="og:title" content="Byt 1.8 Sýkorky"><meta property="og:description" content="Pôdorys a 3D bytu s realistickým svetlom"><meta property="og:image" content="'+U+'icons/preview.jpg"><meta property="og:url" content="'+U+'"><meta name="twitter:card" content="summary_large_image">')
import re
s=re.sub(r'<title>[^<]*</title>','<title>Byt 1.8 Sýkorky</title>',s,count=1)
open(dst,'w').write(s);print('ok',len(s))
