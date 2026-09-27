import json, re, glob, sys, unicodedata, difflib, math, collections
import pyarrow.parquet as pq, shapely.wkb as wkb
def norm(s):
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().upper()
    s=s.replace("'"," ").replace("’"," ").replace('.',' ')
    return re.sub(r'\s+',' ',s).strip()
A=pq.read_table('geo/addresses.parquet',columns=['street','number','geometry']).to_pylist()
streets=collections.defaultdict(list)
for r in A:
    p=wkb.loads(r['geometry']); streets[norm(r['street'])].append((r['number'] or '',p.y,p.x))
SN=list(streets)
P=pq.read_table('geo/places.parquet',columns=['names','geometry','addresses','basic_category','operating_status']).to_pylist()
PL=[]
for r in P:
    n=(r['names'] or {}).get('primary') or ''
    g=wkb.loads(r['geometry']); ad=(r['addresses'] or [{}])[0] or {}
    PL.append((norm(n),n,g.y,g.x,ad.get('freeform'),r['basic_category'],r['operating_status']))
def dist(a,b,c,d): return math.hypot((a-c)*111320,(b-d)*111320*math.cos(math.radians(41.9)))
def numval(s):
    m=re.match(r'(\d+)',s or ''); return int(m.group(1)) if m else None
def geocode(addr):
    a=addr.split(',')
    # find the segment with street + number
    for seg in a:
        m=re.match(r"\s*([A-Za-zÀ-ÿ'’\. ]+?)\s+(\d+)",seg)
        if m and not re.match(r'\s*(box|mercato)',seg,re.I): break
    else: return None
    st=norm(m.group(1)); n=int(m.group(2))
    if st not in streets:
        c=difflib.get_close_matches(st,SN,n=1,cutoff=0.8)
        if not c: return ('nostreet',st)
        st=c[0]
    pts=streets[st]
    ex=[p for p in pts if numval(p[0])==n]
    if ex: return ('exact',st,n,ex[0][1],ex[0][2])
    same=[p for p in pts if numval(p[0]) is not None and numval(p[0])%2==n%2] or pts
    same.sort(key=lambda p:abs(numval(p[0]) - n) if numval(p[0]) is not None else 9e9)
    p=same[0]; return ('near',st,n,p[1],p[2],p[0])
STOP={'LA','IL','DI','DEL','DA','AL','E','DEI','DAL','PIZZA','GELATERIA','MERCATO','TRATTORIA','OSTERIA','HOSTERIA','CAFFE','ROMA','PASTICCERIA','NUOVO','THE','A','PIZZERIA'}
def names(name,lat,lng,r=1500):
    base=re.sub(r'\(.*?\)','',name); toks=[t for t in norm(base).split() if t not in STOP and len(t)>2]
    out=[]
    for p in PL:
        if toks and all(t in p[0] for t in toks[:2]):
            d=dist(lat,lng,p[2],p[3])
            if d<r: out.append((round(d),p[1],round(p[2],6),round(p[3],6),p[4],p[5],p[6]))
    return sorted(out)[:4]
if __name__=='__main__':
    for f in sys.argv[1:]:
        for e in json.load(open(f)):
            g=geocode(e['address'])
            ref=(g[3],g[4]) if g and g[0] in('exact','near') else (e['lat'],e['lng'])
            dd=round(dist(ref[0],ref[1],e['lat'],e['lng'])) if ref else None
            print(f"\n## {e['name']} | {e['address']} | agent {e['lat']},{e['lng']} ({e['coord_source']})\n  ADDR: {g}  (agent off by {dd} m)")
            for c in names(e['name'],*ref): print('  POI:',c)
