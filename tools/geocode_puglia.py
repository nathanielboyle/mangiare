import json, re, unicodedata, difflib, math, collections, sys
import pyarrow.parquet as pq, shapely.wkb as wkb
def norm(s):
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().upper()
    return re.sub(r'\s+',' ',s.replace("'"," ").replace("’"," ").replace('.',' ')).strip()
A=pq.read_table('geo/puglia/address.parquet',columns=['street','number','address_levels','postal_city','geometry']).to_pylist()
S=collections.defaultdict(list)
for r in A:
    lv=[x['value'] for x in (r['address_levels'] or [])]; town=norm(lv[-1] if lv else r['postal_city'] or '')
    p=wkb.loads(r['geometry']); S[(town,norm(r['street']))].append((r['number'] or '',p.y,p.x))
P=pq.read_table('geo/puglia/place.parquet',columns=['names','geometry','addresses','basic_category','operating_status']).to_pylist()
PL=[]
for r in P:
    n=(r['names'] or {}).get('primary') or ''; g=wkb.loads(r['geometry']); ad=(r['addresses'] or [{}])[0] or {}
    PL.append((norm(n),n,g.y,g.x,ad.get('freeform'),ad.get('locality'),r['basic_category'],r['operating_status']))
def dist(a,b,c,d): return math.hypot((a-c)*111320,(b-d)*111320*math.cos(math.radians(40.5)))
def num(s): m=re.match(r'(\d+)',s or ''); return int(m.group(1)) if m else None
def geocode(town,street,n):
    town=norm(town); st=norm(street)
    keys=[k for k in S if k[0]==town]
    if (town,st) not in S:
        c=difflib.get_close_matches(st,[k[1] for k in keys],n=1,cutoff=0.75)
        if not c: return ('nostreet',st,difflib.get_close_matches(st,[k[1] for k in keys],n=3,cutoff=0.5))
        st=c[0]
    pts=S[(town,st)]; ex=[p for p in pts if num(p[0])==n]
    if ex: return ('exact',st,ex[0][0],ex[0][1],ex[0][2])
    same=sorted([p for p in pts if num(p[0]) is not None],key=lambda p:abs(num(p[0])-n))
    return ('near',st,same[0][0],same[0][1],same[0][2]) if same else ('nonum',st)
def poi(tokens,lat=None,lng=None,r=3000):
    out=[]
    for p in PL:
        if all(t in p[0] for t in tokens):
            d=round(dist(lat,lng,p[2],p[3])) if lat else None
            if d is None or d<r: out.append((d,p[1],round(p[2],6),round(p[3],6),p[4],p[5],p[6],p[7]))
    return sorted(out,key=lambda x:(x[0] or 0))[:5]
