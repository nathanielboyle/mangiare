const PLACES = /*__DATA__*/[];
const CATS = [
  {k:'trattoria', label:'Trattorie', one:'Trattoria'},
  {k:'pizzeria',  label:'Pizzerie', one:'Pizzeria'},
  {k:'teglia',    label:'Pizza in teglia', one:'Pizza in teglia'},
  {k:'quick',     label:'Quick bites', one:'Quick bite'},
  {k:'sweets',    label:'Sweets', one:'Sweets'},
  {k:'gelato',    label:'Gelato', one:'Gelato'},
  {k:'market',    label:'Markets & shops', one:'Market & shop'},
  {k:'bar',       label:'Bars & cafés', one:'Bar & café'},
];
const CAT = Object.fromEntries(CATS.map(c=>[c.k,c]));
const REGIONS = {
  roma: {
    name:'Rome', title:'Mangiare <em>a</em> Roma', areaAll:'All neighborhoods', areaWord:'Neighborhood',
    src:'Everything in Katie Parla’s <a href="https://katieparla.com/" target="_blank" rel="noopener">Guide to Eating Well in Rome</a> (2026) and her <a href="https://www.eater.com/maps/best-restaurants-rome-italy" target="_blank" rel="noopener">Eater Rome map</a> (March 2026), plus your own picks, pinned by street address. An unofficial companion map.',
    notes:'How Romans eat: notes from the guide', minZoom:11, maxBounds:[[41.79,12.39],[41.975,12.62]], noteLabel:'In the guide',
    labels:{trattoria:{label:'Trattorie & restaurants', one:'Restaurant'}},
  },
  puglia: {
    name:'Puglia', title:'Mangiare <em>in</em> Puglia', areaAll:'All towns', areaWord:'Town',
    src:'Restaurants, bakeries, bars and gelaterie from Bari to the tip of Salento, from your Puglia restaurant notes (via <a href="https://katieparla.com/" target="_blank" rel="noopener">Katie Parla</a>), pinned by street address.',
    notes:'Eating in Puglia: notes from the list', minZoom:8, maxBounds:[[39.6,16.4],[41.45,18.85]], noteLabel:'Katie’s note',
    labels:{trattoria:{label:'Restaurants & trattorie', one:'Restaurant'}, teglia:{label:'Bakeries', one:'Bakery'}, gelato:{label:'Gelato & granita', one:'Gelato & granita'}},
  },
};
const SOURCES={guide:{label:'Parla guide',long:'Katie Parla’s Rome guide'},eater:{label:'Eater',long:'Eater Rome map'},notes:{label:'Puglia notes',long:'Your Puglia notes'},you:{label:'Your pick',long:'Your picks'}};
const catLabel=(k,r=state.region)=>(REGIONS[r].labels[k]||CAT[k]).label;
const catOne=(k,r)=>(REGIONS[r].labels[k]||CAT[k]).one;
const ICON = {
  trattoria:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"><path d="M4.5 1.8v12.4M2.6 1.8v3.6a1.9 1.9 0 0 0 3.8 0V1.8"/><path d="M11.4 14.2V1.8c-1.7.6-2.4 2.6-2.4 5.2 0 1.2.5 1.9 1.3 2.1h1.1"/></svg>',
  pizzeria:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"><circle cx="8" cy="8" r="6.2"/><path d="M8 8 12.4 3.6M8 8v6.2"/><circle cx="5.4" cy="6.2" r=".9" fill="#fff" stroke="none"/><circle cx="10.6" cy="9.8" r=".9" fill="#fff" stroke="none"/></svg>',
  teglia:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"><rect x="1.8" y="4" width="12.4" height="8" rx="1.2"/><path d="M6 4v8M10 4v8"/></svg>',
  quick:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"><ellipse cx="8" cy="8" rx="6.3" ry="3.9" transform="rotate(-30 8 8)"/><path d="M5.7 9.6c1.3-.4 2.8-1.3 4-2.7" stroke-linecap="round"/></svg>',
  sweets:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"><path d="M2 13.6h12V8.4L2 5z"/><path d="M2 9.2l12 1.8"/><path d="M4.6 5.6c-.2-1.4.7-2.6 1.9-2.6" stroke-linecap="round"/></svg>',
  gelato:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"><path d="M4.4 7.4 8 14.6l3.6-7.2"/><path d="M4 7.4a4 4 0 1 1 8 0z"/></svg>',
  market:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"><path d="M1.8 6.6h12.4l-1.4 7.2H3.2z"/><path d="M5 6.6 7 2.4M11 6.6 9 2.4" stroke-linecap="round"/></svg>',
  bar:'<svg viewBox="0 0 16 16" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M2.4 2.6h11.2L8 8.6z"/><path d="M8 8.6v5M5.2 13.6h5.6"/></svg>',
};
const SVG = {
  star:'<svg viewBox="0 0 20 20" fill="currentColor"><path d="m10 2.2 2.4 5 5.4.6-4 3.7 1.1 5.4L10 14.2l-4.9 2.7 1.1-5.4-4-3.7 5.4-.6z"/></svg>',
  starO:'<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="m10 2.2 2.4 5 5.4.6-4 3.7 1.1 5.4L10 14.2l-4.9 2.7 1.1-5.4-4-3.7 5.4-.6z"/></svg>',
  check:'<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="7.6" fill="currentColor" stroke="none"/><path d="m6.6 10.2 2.3 2.3 4.6-4.8" stroke="var(--surface)"/></svg>',
  checkO:'<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="7.6"/><path d="m6.6 10.2 2.3 2.3 4.6-4.8"/></svg>',
  go:'<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M10 18s6-5.2 6-10a6 6 0 0 0-12 0c0 4.8 6 10 6 10z"/><circle cx="10" cy="8" r="2.2"/></svg>',
};
const esc = s => String(s??'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const color = k => `var(--c-${k})`;
const fullName = p => p.branch ? `${p.name} · ${p.branch}` : p.name;
const fold = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');

// ---- per-viewer marks (localStorage, fails soft) ----
const KEY='mangiare-roma-marks-v1';
let marks={want:[],been:[]};
try{ const s=JSON.parse(localStorage.getItem(KEY)||'null'); if(s&&Array.isArray(s.want)&&Array.isArray(s.been)) marks=s; }catch(e){}
const want=new Set(marks.want), been=new Set(marks.been);
function saveMarks(){ try{ localStorage.setItem(KEY, JSON.stringify({want:[...want],been:[...been]})); }catch(e){} }
function pref(k,v){ try{ if(v===undefined) return localStorage.getItem(KEY+'-'+k); localStorage.setItem(KEY+'-'+k,v); }catch(e){} return null; }

// ---- state ----
const allCats = r => CATS.map(c=>c.k).filter(k=>PLACES.some(p=>p.region===r&&p.cat===k));
const hashRegion = (location.hash||'').slice(1);
const state={region: REGIONS[hashRegion]?hashRegion:(REGIONS[pref('region')]?pref('region'):'roma'),
  cats:null, q:'', hood:'', src:'', show:'all', group:(pref('group')==='cat'?'cat':'hood'), sel:null};
state.cats=new Set(allCats(state.region));
const inRegion = p => p.region===state.region;

// ---- map ----
const map=L.map('map',{zoomControl:true,minZoom:8,maxZoom:17,zoomSnap:0.5,attributionControl:true,maxBoundsViscosity:0.8});
map.attributionControl.setPrefix(false);
const ATTR='© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> · <a href="https://overturemaps.org" target="_blank" rel="noopener">Overture Maps</a>';
// One tile tree; each set covers its own area and zoom range (tile zoom = display zoom - 1).
const TILESETS=[
  {bounds:[[41.808,12.418],[41.955,12.592]], minZoom:10, minNativeZoom:10, maxNativeZoom:15},  // Rome, street level
  {bounds:[[39.76,16.72],[41.22,18.6]], minZoom:8, minNativeZoom:8, maxNativeZoom:11}, // Puglia, regional
  {bounds:[[41.098,16.855],[41.137,16.885]], minZoom:12, minNativeZoom:12, maxNativeZoom:15}, // bari
  {bounds:[[40.988,17.195],[41.008,17.228]], minZoom:12, minNativeZoom:12, maxNativeZoom:15}, // polignano
  {bounds:[[40.94,17.296],[40.955,17.318]], minZoom:12, minNativeZoom:12, maxNativeZoom:15}, // monopoli
  {bounds:[[40.341,18.158],[40.366,18.192]], minZoom:12, minNativeZoom:12, maxNativeZoom:15}, // lecce
];
let tileLayers=[], tileTheme=null;
function isDark(){
  const t=document.documentElement.getAttribute('data-theme');
  if(t==='dark') return true; if(t==='light') return false;
  return window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches;
}
function setTiles(){
  const th=isDark()?'dark':'light'; if(th===tileTheme) return; tileTheme=th;
  const old=tileLayers;
  tileLayers=TILESETS.map(ts=>L.tileLayer(`tiles/${th}/{z}/{x}/{y}.webp`,Object.assign({tileSize:512,zoomOffset:-1,maxZoom:17,attribution:ATTR},ts)).addTo(map));
  if(old.length){ setTimeout(()=>old.forEach(l=>map.removeLayer(l)),900); }
}
setTiles();
try{ matchMedia('(prefers-color-scheme: dark)').addEventListener('change',setTiles); }catch(e){}
new MutationObserver(setTiles).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});

// labels: [text, lat, lng, tier]; tier 1 always, 2 from mid zoom, 'm' landmark from high zoom
const LABELS=[
  ['Centro Storico',41.8985,12.4735,1],['Trastevere',41.8872,12.4665,1],['Testaccio',41.8762,12.4745,1],['Prati',41.9085,12.4640,1],
  ['Monti',41.8955,12.4905,1],['Esquilino',41.8985,12.5060,1],['EUR',41.8330,12.4715,1],['Garbatella',41.8600,12.4880,1],
  ['Ostiense',41.8700,12.4830,1],['San Giovanni',41.8830,12.5130,1],['Monteverde',41.8765,12.4545,1],['San Lorenzo',41.8975,12.5165,1],
  ['Tor Pignattara',41.8790,12.5360,1],['Aventino',41.8835,12.4800,2],['Nomentano',41.9170,12.5120,1],['Flaminio',41.9255,12.4695,1],
  ['Trionfale',41.9115,12.4490,2],['Tuscolano',41.8660,12.5470,1],['Appio-Latino',41.8745,12.5095,2],['San Paolo',41.8545,12.4800,2],
  ['Marconi',41.8585,12.4660,2],['Montesacro',41.9385,12.5300,1],['Ponte Milvio',41.9395,12.4700,2],['Parioli',41.9255,12.4940,1],
  ['Vaticano',41.9035,12.4520,2],['Casal Bertone',41.9005,12.5335,2],['Pigneto',41.8895,12.5285,2],['Ghetto',41.8922,12.4760,2],
  ['Gianicolense',41.8740,12.4400,2],['Re di Roma',41.8810,12.5170,2],['Centocelle',41.8860,12.5640,1],['Roma 70',41.8370,12.5010,2],['Isola Tiberina',41.8905,12.4770,2],
  ['Colosseo',41.8902,12.4922,'m'],['Pantheon',41.8986,12.4768,'m'],['Piazza Navona',41.8992,12.4731,'m'],["Campo de' Fiori",41.8956,12.4722,'m'],
  ['San Pietro',41.9022,12.4539,'m'],['Termini',41.9010,12.5015,'m'],['Fontana di Trevi',41.9009,12.4833,'m'],['Piramide',41.8757,12.4818,'m'],
  ['Circo Massimo',41.8859,12.4852,'m'],['Villa Pamphili',41.8850,12.4470,'m'],['Villa Borghese',41.9135,12.4870,'m'],['Piazza di Spagna',41.9057,12.4823,'m'],
  ['Piazza del Popolo',41.9107,12.4763,'m'],['Bocca della Verità',41.8881,12.4817,'m'],['Piazza Vittorio',41.8951,12.5048,'m'],['Stazione Trastevere',41.8724,12.4661,'m'],
  ['Palazzo della Civiltà',41.8368,12.4654,'m'],
  ['Bari',41.1258,16.862,'town'],['Polignano a Mare',40.9944,17.2225,'town'],['Monopoli',40.9522,17.2999,'town'],['Fasano',40.8344,17.3584,'town'],
  ['Alberobello',40.7841,17.2377,'town'],['Lecce',40.357,18.1718,'town'],['San Cataldo',40.3902,18.3062,'town'],['Guagnano',40.4012,17.949,'town'],
  ['Nardò',40.1763,18.0306,'town'],['Otranto',40.1457,18.4908,'town'],['Ruffano',39.9841,18.2475,'town'],['Patù',39.8413,18.3384,'town'],
  ['Gallipoli',40.0547,17.9758,'town'],['Alezio',40.0613,18.0582,'town'],
  ['Brindisi',40.6375,17.9455,'town2'],['Taranto',40.4712,17.2432,'town2'],['Ostuni',40.7276,17.5764,'town2'],['Martina Franca',40.7042,17.34,'town2'],
  ['Locorotondo',40.7552,17.3265,'town3'],['Galatina',40.1743,18.1678,'town3'],['Maglie',40.1185,18.2989,'town3'],['Santa Maria di Leuca',39.7967,18.3545,'town3'],
  ['Torre Canne',40.8389,17.4655,'town3'],['Savelletri',40.873,17.409,'town3'],['Bari Vecchia',41.1300,16.8680,2],
  ['Mare Adriatico',41.05,17.75,'sea'],['Mar Ionio',39.95,17.55,'sea'],
];
const labelLayer=L.layerGroup().addTo(map);
function lab(text,lat,lng,cls){ L.marker([lat,lng],{interactive:false,keyboard:false,icon:L.divIcon({className:'',html:`<div class="lab ${cls}">${esc(text)}</div>`,iconSize:[0,0]})}).addTo(labelLayer); }
LABELS.forEach(([n,a,b,t])=>lab(n,a,b,t==='m'?'mark':t==='sea'?'river sea':t==='town'||t==='town2'?t:t==='town3'?'town2 t3':'hood t'+t));
lab('Tevere',41.8915,12.4735,'river'); lab('Tevere',41.9205,12.4715,'river t2');
function zoomClass(){ const z=map.getZoom(), c=map.getContainer();
  c.classList.toggle('z-reg',z<10); c.classList.toggle('z-lo',z<13); c.classList.toggle('z-mid',z>=13&&z<14.5); c.classList.toggle('z-hi',z>=14.5); }
map.on('zoomend',zoomClass);

// markers
const markers={};
function pinHtml(p){
  const cls=['pin']; if(want.has(p.id)) cls.push('want'); if(been.has(p.id)) cls.push('been'); if(state.sel===p.id) cls.push('sel');
  return `<div class="${cls.join(' ')}" style="background:${color(p.cat)}">${ICON[p.cat]}</div>`;
}
function iconFor(p){ return L.divIcon({className:'',html:pinHtml(p),iconSize:[30,30],iconAnchor:[15,15],popupAnchor:[0,-14]}); }
const gmaps = p => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(p.name+', '+p.address)}`;
function popupHtml(p){
  const w=want.has(p.id), b=been.has(p.id);
  return `<div class="pop">
    <div class="cat"><i style="background:${color(p.cat)}"></i>${esc(catOne(p.cat,p.region))}</div>
    <h3>${esc(p.name)}${p.branch?`<small>${esc(p.branch)} location</small>`:''}</h3>
    <div class="style">${esc(p.style)} · ${esc(p.hood)}</div>
    ${p.price||p.hours?`<div class="style">${[p.price,p.hours].filter(Boolean).map(esc).join(' · ')}</div>`:''}
    <div class="srcs">${p.src.map(k=>`<span class="srctag s-${k}">${esc(SOURCES[k].label)}</span>`).join('')}</div>
    <div class="addr">${esc(p.address)}</div>
    <p class="bl">${esc(p.blurb)}</p>
    ${p.order?`<div class="guide"><b>What to order</b>${esc(p.order)}</div>`:''}
    ${p.guide?`<div class="guide"><b>${esc(REGIONS[p.region].noteLabel)}</b>${esc(p.guide)}</div>`:''}
    ${p.eater?`<div class="guide"><b>Eater · ${esc(p.eaterLabel||'Tip')}</b>${esc(p.eater)}</div>`:''}
    ${p.mine?`<div class="guide mine"><b>Your note</b>${esc(p.mine)}</div>`:''}
    ${p.warn?`<div class="guide warn"><b>Heads up</b>${esc(p.warn)}</div>`:''}
    <div class="acts">
      <a class="go" href="${gmaps(p)}" target="_blank" rel="noopener">${SVG.go}Directions</a>
      <button type="button" class="want" data-act="want" data-id="${p.id}" aria-pressed="${w}">${w?SVG.star:SVG.starO}Want to go</button>
      <button type="button" class="been" data-act="been" data-id="${p.id}" aria-pressed="${b}">${b?SVG.check:SVG.checkO}Been</button>
    </div></div>`;
}
PLACES.forEach(p=>{
  const m=L.marker([p.lat,p.lng],{icon:iconFor(p),title:fullName(p),riseOnHover:true,keyboard:true});
  m.bindPopup(()=>popupHtml(p),{maxWidth:320,autoPanPadding:[24,24]});
  m.on('popupopen',()=>select(p.id));
  m.on('popupclose',()=>{ if(state.sel===p.id){ state.sel=null; refreshPin(p); markSelInList(); } });
  markers[p.id]=m;
});
function refreshPin(p){ markers[p.id].setIcon(iconFor(p)); }

// ---- filtering ----
function matches(p){
  if(!inRegion(p)) return false;
  if(!state.cats.has(p.cat)) return false;
  if(state.hood && p.hood!==state.hood) return false;
  if(state.src && !p.src.includes(state.src)) return false;
  if(state.show==='want' && !want.has(p.id)) return false;
  if(state.show==='been' && !been.has(p.id)) return false;
  if(state.show==='todo' && been.has(p.id)) return false;
  if(state.q){ const hay=fold(p.name+' '+(p.branch||'')+' '+p.style+' '+p.hood+' '+p.address+' '+catLabel(p.cat,p.region)+' '+p.src.map(k=>SOURCES[k].label).join(' '));
    if(!state.q.split(/\s+/).every(t=>hay.includes(t))) return false; }
  return true;
}
const visible = () => PLACES.filter(matches);

// ---- UI: region, chips, area select ----
const srcSel=document.getElementById('src-filter');
const chipsEl=document.getElementById('chips'), hoodSel=document.getElementById('hood'), qEl=document.getElementById('q');
function renderChips(){
  chipsEl.innerHTML=allCats(state.region).map(k=>{ const n=PLACES.filter(p=>inRegion(p)&&p.cat===k).length;
    return `<button type="button" class="chip" data-cat="${k}" aria-pressed="${state.cats.has(k)}"><span class="dot" style="background:${color(k)}">${ICON[k]}</span>${esc(catLabel(k))} <span class="n">${n}</span></button>`; }).join('');
}
chipsEl.addEventListener('click',e=>{
  const b=e.target.closest('.chip'); if(!b) return; const k=b.dataset.cat, all=allCats(state.region);
  // first click from "all on" isolates the category; otherwise toggle
  if(state.cats.size===all.length){ state.cats=new Set([k]); }
  else if(state.cats.has(k)){ state.cats.delete(k); if(!state.cats.size) state.cats=new Set(all); }
  else state.cats.add(k);
  renderChips(); update(true);
});
function renderHoods(){
  const counts={}; PLACES.filter(inRegion).forEach(p=>counts[p.hood]=(counts[p.hood]||0)+1);
  const R=REGIONS[state.region];
  hoodSel.setAttribute('aria-label',R.areaWord);
  hoodSel.innerHTML=`<option value="">${esc(R.areaAll)}</option>`+Object.keys(counts).sort((a,b)=>a.localeCompare(b))
    .map(h=>`<option value="${esc(h)}">${esc(h)} (${counts[h]})</option>`).join('');
  hoodSel.value=state.hood;
  const sc={}; PLACES.filter(inRegion).forEach(p=>p.src.forEach(k=>sc[k]=(sc[k]||0)+1));
  const keys=Object.keys(SOURCES).filter(k=>sc[k]);
  srcSel.innerHTML=`<option value="">All sources</option>`+keys.map(k=>`<option value="${k}">${esc(SOURCES[k].long)} (${sc[k]})</option>`).join('');
  srcSel.value=state.src; srcSel.parentElement.hidden=keys.length<2;
}
hoodSel.addEventListener('change',()=>{ state.hood=hoodSel.value; update(true); });
srcSel.addEventListener('change',()=>{ state.src=srcSel.value; update(true); });
qEl.addEventListener('input',()=>{ state.q=fold(qEl.value.trim()); update(false); });
document.querySelectorAll('[data-show]').forEach(b=>b.addEventListener('click',()=>{ state.show=b.dataset.show;
  document.querySelectorAll('[data-show]').forEach(x=>x.setAttribute('aria-pressed',x===b)); update(true); }));
document.querySelectorAll('[data-group]').forEach(b=>{ b.setAttribute('aria-pressed',b.dataset.group===state.group);
  b.addEventListener('click',()=>{ state.group=b.dataset.group; pref('group',state.group);
  document.querySelectorAll('[data-group]').forEach(x=>x.setAttribute('aria-pressed',x===b)); renderList(visible()); }); });
document.querySelectorAll('[data-rcount]').forEach(el=>el.textContent=PLACES.filter(p=>p.region===el.dataset.rcount).length);
document.querySelectorAll('[data-region]').forEach(b=>b.addEventListener('click',()=>setRegion(b.dataset.region,true)));

function setRegion(r,animate){
  state.region=r; pref('region',r);
  try{ history.replaceState(null,'',r==='roma'?location.pathname+location.search:'#'+r); }catch(e){}
  const R=REGIONS[r];
  document.querySelectorAll('[data-region]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.region===r));
  document.getElementById('rname').textContent=R.name;
  document.getElementById('title').innerHTML=R.title;
  document.getElementById('src').innerHTML=R.src;
  document.getElementById('notes-sum').textContent=R.notes;
  document.querySelectorAll('[data-notes]').forEach(ul=>ul.hidden=ul.dataset.notes!==r);
  document.title=R.title.replace(/<[^>]+>/g,'');
  state.cats=new Set(allCats(r)); state.hood=''; state.src=''; state.q=''; qEl.value='';
  if(state.sel){ const m=markers[state.sel]; if(m) m.closePopup(); state.sel=null; }
  map.setMaxBounds(null); map.setMinZoom(R.minZoom);
  renderChips(); renderHoods();
  const pts=PLACES.filter(inRegion).map(p=>[p.lat,p.lng]);
  const opts={padding:[28,28],maxZoom:r==='roma'?14:10};
  if(animate) map.flyToBounds(pts,Object.assign({duration:.8},opts)); else map.fitBounds(pts,opts);
  map.once('moveend',()=>map.setMaxBounds(R.maxBounds));
  update(false);
}

// ---- list ----
const listEl=document.getElementById('list');
function itemHtml(p){
  const w=want.has(p.id), b=been.has(p.id);
  return `<div class="item${state.sel===p.id?' sel':''}" data-id="${p.id}" role="button" tabindex="0" aria-label="${esc(fullName(p))}, ${esc(p.style)}">
    <span class="pinmini" style="background:${color(p.cat)}">${ICON[p.cat]}</span>
    <div><div class="nm">${esc(p.name)}${p.branch?` <small>· ${esc(p.branch)}</small>`:''}</div>
    <div class="meta">${esc(p.style)}${state.group==='cat'?` <span class="h">· ${esc(p.hood)}</span>`:''}${p.region==='roma'?` <span class="h">· ${p.src.map(k=>esc(SOURCES[k].label)).join(', ')}</span>`:''}</div></div>
    <div class="marks">
      <button type="button" class="mk want" data-act="want" data-id="${p.id}" aria-pressed="${w}" title="Want to go" aria-label="Want to go: ${esc(fullName(p))}">${w?SVG.star:SVG.starO}</button>
      <button type="button" class="mk been" data-act="been" data-id="${p.id}" aria-pressed="${b}" title="Been" aria-label="Been: ${esc(fullName(p))}">${b?SVG.check:SVG.checkO}</button>
    </div></div>`;
}
function renderList(vis){
  if(!vis.length){ listEl.innerHTML=`<div class="empty">No places match these filters.<br><button type="button" id="reset">Clear filters</button></div>`;
    document.getElementById('reset').onclick=resetFilters; return; }
  const groups=new Map(), order=allCats(state.region);
  if(state.group==='cat'){ order.forEach(k=>{ const g=vis.filter(p=>p.cat===k); if(g.length) groups.set(catLabel(k),g); }); }
  else { const by={}; vis.forEach(p=>(by[p.hood]=by[p.hood]||[]).push(p));
    Object.keys(by).sort((a,b)=>by[b].length-by[a].length||a.localeCompare(b)).forEach(h=>groups.set(h,by[h])); }
  let html=''; for(const [g,items] of groups){
    items.sort((a,b)=>state.group==='cat'?a.name.localeCompare(b.name):(order.indexOf(a.cat)-order.indexOf(b.cat))||a.name.localeCompare(b.name));
    html+=`<section class="group"><h2>${esc(g)}<span>${items.length}</span></h2>${items.map(itemHtml).join('')}</section>`; }
  listEl.innerHTML=html;
}
function resetFilters(){ state.cats=new Set(allCats(state.region)); state.q=''; qEl.value=''; state.hood=''; hoodSel.value=''; state.src=''; srcSel.value=''; state.show='all';
  document.querySelectorAll('[data-show]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.show==='all')); renderChips(); update(true); }
listEl.addEventListener('click',e=>{
  const act=e.target.closest('[data-act]'); if(act){ e.stopPropagation(); toggleMark(+act.dataset.id,act.dataset.act); return; }
  const it=e.target.closest('.item'); if(it) focusPlace(+it.dataset.id);
});
listEl.addEventListener('keydown',e=>{ if((e.key==='Enter'||e.key===' ')&&e.target.classList.contains('item')){ e.preventDefault(); focusPlace(+e.target.dataset.id); } });
document.getElementById('map').addEventListener('click',e=>{ const act=e.target.closest('[data-act]'); if(act) toggleMark(+act.dataset.id,act.dataset.act); });

function markSelInList(){ listEl.querySelectorAll('.item').forEach(el=>el.classList.toggle('sel',+el.dataset.id===state.sel)); }
function select(id){
  const prev=state.sel; state.sel=id;
  if(prev&&prev!==id){ const pp=PLACES.find(x=>x.id===prev); if(pp) refreshPin(pp); }
  refreshPin(PLACES.find(x=>x.id===id)); markSelInList();
  const el=listEl.querySelector(`.item[data-id="${id}"]`);
  if(el && window.matchMedia('(min-width: 821px)').matches){ const r=el.getBoundingClientRect(), lr=listEl.getBoundingClientRect(); if(r.top<lr.top+40||r.bottom>lr.bottom) el.scrollIntoView({block:'center',behavior:'smooth'}); }
}
function focusPlace(id){
  const p=PLACES.find(x=>x.id===id), m=markers[id];
  if(!map.hasLayer(m)) m.addTo(map);
  if(window.matchMedia('(max-width: 820px)').matches) document.querySelector('.mapwrap').scrollIntoView({behavior:'smooth',block:'start'});
  map.flyTo([p.lat,p.lng],Math.max(map.getZoom(),15),{duration:.6});
  map.once('moveend',()=>m.openPopup());
}
function toggleMark(id,kind){
  const set=kind==='want'?want:been; set.has(id)?set.delete(id):set.add(id);
  if(kind==='been'&&been.has(id)) want.delete(id);
  saveMarks(); const p=PLACES.find(x=>x.id===id); refreshPin(p);
  const m=markers[id]; if(m.isPopupOpen()) m.setPopupContent(popupHtml(p));
  update(false,true);
}

// ---- update ----
function update(fit,keepMap){
  const vis=visible(), ids=new Set(vis.map(p=>p.id));
  PLACES.forEach(p=>{ const m=markers[p.id], on=ids.has(p.id);
    if(on&&!map.hasLayer(m)) m.addTo(map);
    if(!on&&map.hasLayer(m)&&!(keepMap&&m.isPopupOpen())) map.removeLayer(m); });
  const reg=PLACES.filter(inRegion);
  document.getElementById('t-show').textContent=vis.length;
  document.getElementById('t-want').textContent=reg.filter(p=>want.has(p.id)).length;
  document.getElementById('t-been').textContent=reg.filter(p=>been.has(p.id)).length;
  document.getElementById('total').textContent=reg.length;
  renderList(vis);
  if(fit&&vis.length){ map.flyToBounds(vis.map(p=>[p.lat,p.lng]),{padding:[40,40],maxZoom:15.5,duration:.5}); }
}
// ---- offline (GitHub Pages build only; the artifact sandbox has no service workers) ----
const standalone = document.body.hasAttribute('data-standalone') && 'serviceWorker' in navigator && 'caches' in window;
let offlineList=null;
const offEl=document.getElementById('offline');
async function offlineStatus(){
  if(!standalone||!offEl) return;
  offEl.hidden=false;
  try{ if(!offlineList) offlineList=await (await fetch('offline.json')).json(); }catch(e){ offEl.hidden=true; return; }
  const th=isDark()?'dark':'light', set=(offlineList[state.region]||{})[th]; if(!set){ offEl.hidden=true; return; }
  const cache=await caches.open('tiles-v1'); let have=0;
  const keys=new Set((await cache.keys()).map(r=>new URL(r.url).pathname));
  const base=new URL('.',location.href).pathname;
  set.files.forEach(f=>{ if(keys.has(base+f)) have++; });
  const mb=Math.round(set.bytes/1e6), name=REGIONS[state.region].name;
  const btn=offEl.querySelector('button'), msg=offEl.querySelector('span');
  if(have>=set.files.length){ btn.hidden=true; msg.textContent=`${name} map saved for offline use (${th} theme).`; }
  else { btn.hidden=false; btn.disabled=false; btn.textContent=`Save ${name} map for offline (${mb} MB)`;
    msg.textContent=have?`${Math.round(100*have/set.files.length)}% saved`:''; }
}
async function saveOffline(){
  const th=isDark()?'dark':'light', set=offlineList[state.region][th];
  const btn=offEl.querySelector('button'), msg=offEl.querySelector('span'); btn.disabled=true;
  try{ if(navigator.storage&&navigator.storage.persist) await navigator.storage.persist(); }catch(e){}
  const cache=await caches.open('tiles-v1'); let done=0, failed=0, i=0;
  async function worker(){ while(i<set.files.length){ const f=set.files[i++];
    try{ if(!(await cache.match(f))) await cache.add(f); }catch(e){ failed++; }
    done++; if(done%8===0||done===set.files.length) msg.textContent=`Saving… ${Math.round(100*done/set.files.length)}%`; } }
  await Promise.all(Array.from({length:6},worker));
  if(failed){ msg.textContent=`${failed} tiles didn't download. Check your connection and try again.`; btn.disabled=false; }
  else offlineStatus();
}
if(standalone){
  navigator.serviceWorker.register('sw.js').catch(()=>{});
  offEl.querySelector('button').addEventListener('click',saveOffline);
  document.querySelectorAll('[data-region]').forEach(b=>b.addEventListener('click',()=>setTimeout(offlineStatus,0)));
  new MutationObserver(()=>setTimeout(offlineStatus,0)).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  try{ matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>setTimeout(offlineStatus,0)); }catch(e){}
  offlineStatus();
}

setRegion(state.region,false); zoomClass();
setTimeout(()=>map.invalidateSize(),0); window.addEventListener('resize',()=>map.invalidateSize());
