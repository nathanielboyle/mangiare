"""Render Puglia basemap tiles: regional (tile z7-10) + street-level town boxes (tile z11-14)."""
import math, os, sys, io
import pyarrow.parquet as pq, shapely.wkb as wkb
from shapely.strtree import STRtree
from shapely.geometry import box
from shapely.ops import unary_union
import cairocffi as cairo
from PIL import Image
G='geo/puglia/'
REGION=(16.72,39.76,18.6,41.22)
TOWNS={'bari':(16.855,41.098,16.885,41.137),'polignano':(17.195,40.988,17.228,41.008),'monopoli':(17.296,40.940,17.318,40.955),'lecce':(18.158,40.341,18.192,40.366)}
BB=box(16.5,39.6,18.8,41.4)
def flags(v):
    s=set()
    for f in v or []: s|=set(f.get('values') or [])
    return s
def load(fn,cols,filt,flt=None):
    out=[]
    t=pq.read_table(G+fn,columns=cols+['geometry'],filters=flt)
    for r in t.to_pylist():
        k=filt(r)
        if k: out.append((k,wkb.loads(r['geometry'])))
    return out
land=[('land',unary_union([g.buffer(0) for k,g in load('land.parquet',['subtype','class'],lambda r:'x' if r['class']=='land' else None)]).intersection(BB))]
print('land',land[0][1].geom_type, file=sys.stderr)
LU={'park':'park','dog_park':'park','garden':'park','grass':'grass','meadow':'grass','pitch':'pitch','recreation_ground':'grass','playground':'grass','cemetery':'grass','plaza':'plaza','pedestrian':'plaza',
    'residential':'urban','commercial':'urban','retail':'urban','industrial':'urban'}
landuse=load('land_use.parquet',['class','subtype'],lambda r: LU.get(r['class']) or ('grass' if r['subtype']=='cemetery' else None))
_w=load('water.parquet',['class','subtype'],lambda r: None if r['class'] in ('swimming_pool','wastewater') or r['subtype'] in ('human_made','ocean','physical') else ('river' if r['subtype']=='river' else 'stream'))
water=[('water',g) for k,g in _w if g.geom_type!='LineString' and g.area<0.2]
wlines=[(k,g) for k,g in _w if g.geom_type=='LineString']
bld=[]
for n in TOWNS: bld+=load(f'bld_{n}.parquet',[],lambda r:'b')
RC={'motorway':'mw','trunk':'mw','primary':'pri','secondary':'sec','tertiary':'ter','residential':'res','unclassified':'res','living_street':'res','unknown':'res','service':'svc','pedestrian':'ped','footway':'foot','steps':'foot','path':'foot','cycleway':'foot'}
def segf(r):
    f=flags(r['road_flags'])|flags(r['rail_flags'])
    if f & {'is_tunnel','is_indoor','is_under_construction','is_abandoned','is_disused','is_covered'}: return None
    if r['subtype']=='rail':
        return ('rail','is_bridge' in f) if r['class'] in ('standard_gauge','narrow_gauge','light_rail','unknown') else None
    c=RC.get(r['class']); return (c,'is_bridge' in f) if c else None
seg=load('segment.parquet',['subtype','class','road_flags','rail_flags'],segf)
major=[s for s in seg if s[0][0] in ('mw','pri','sec','ter','rail')]
print('loaded',len(landuse),len(water),len(bld),len(seg),len(major),file=sys.stderr)
def tree(items): return (STRtree([g for _,g in items]),items)
T_LAND,T_LU,T_W,T_WL,T_B,T_S,T_MAJ=map(tree,(land,landuse,water,wlines,bld,seg,major))
PAL={
 'light':dict(sea='#AFC9C4',bg='#ECE7DE',urban='#E2DACD',park='#D2DCBA',grass='#DCE2C8',pitch='#CCD8B4',plaza='#F4F0E8',water='#A3C2BC',b='#E0D8CB',bs='#D4CBBC',
   rail='#B2AA9F',case='#D3CABB',res='#FFFFFF',svc='#F9F7F3',ped='#F6F2EA',foot='#DDD5C8',ter='#FFFFFF',sec='#FDF6E6',pri='#FBEBC8',mw='#F3D9A4',casemaj='#D8C49A',casemw='#C9A96C',coast='#98B8B2'),
 'dark':dict(sea='#152729',bg='#1B1A18',urban='#24221F',park='#1F261C',grass='#20261C',pitch='#222A1E',plaza='#26231F',water='#1C3436',b='#262320',bs='#2E2A26',
   rail='#45403A',case='#141312',res='#35312C',svc='#2D2A26',ped='#2E2A25',foot='#34302A',ter='#3B372F',sec='#433D32',pri='#4E4533',mw='#5E4E32',casemaj='#161412',casemw='#161412',coast='#22393A'),
}
WID={'mw':{8:.9,9:1.2,10:1.6,11:2.1,12:1.8,13:2.6,14:3.8,15:6},'pri':{8:.5,9:.8,10:1.1,11:1.5,12:1.5,13:2.3,14:3.4,15:5.4},'sec':{10:.5,11:.9,12:1.0,13:1.7,14:2.8,15:4.6},
 'ter':{11:.45,12:.6,13:1.1,14:2.1,15:3.6},'res':{13:.5,14:1.1,15:2.3},'svc':{14:.5,15:1.0},'ped':{14:.9,15:1.8},'foot':{15:.55},'rail':{10:.4,11:.5,12:.6,13:.8,14:1.0,15:1.4}}
ORDER=['foot','svc','res','ped','ter','sec','pri','mw']
def merc(lng,lat,z,S):
    n=2**z*S; x=(lng+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n; return x,y
def tile_bounds(x,y,z):
    def ll(px,py):
        n=2**z; return px/n*360-180, math.degrees(math.atan(math.sinh(math.pi*(1-2*py/n))))
    w,nn=ll(x,y); e,s=ll(x+1,y+1); return w,s,e,nn
def path(ctx,geom,f):
    t=geom.geom_type
    if t=='Polygon':
        for ring in [geom.exterior,*geom.interiors]:
            pts=[f(*c[:2]) for c in ring.coords]; ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]; ctx.close_path()
    elif t=='LineString':
        pts=[f(*c[:2]) for c in geom.coords]
        if pts: ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]
    elif hasattr(geom,'geoms'):
        for g in geom.geoms: path(ctx,g,f)
def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def render(x,y,T,scale,theme,out):
    Z=T+1; P=PAL[theme]; S=512*scale
    w,s,e,n=tile_bounds(x,y,T); q=box(w,s,e,n).buffer((e-w)*0.03)
    ox,oy=x*S,y*S
    f=lambda lng,lat:(lambda p:(p[0]-ox,p[1]-oy))(merc(lng,lat,T,S))
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,S,S); c=cairo.Context(surf)
    c.set_source_rgb(*hexc(P['sea'])); c.paint()
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    # land mask, clipped to tile first to keep paths small
    lg=land[0][1].intersection(q)
    if not lg.is_empty:
        c.new_path(); path(c,lg,f); c.set_source_rgb(*hexc(P['bg'])); c.fill_preserve()
        c.set_source_rgb(*hexc(P['coast'])); c.set_line_width(0.8*scale); c.stroke()
    def fill(tr,keys,minz=0,maxz=99):
        if not(minz<=Z<=maxz): return
        t,items=tr; idx=t.query(q)
        for k in keys:
            c.new_path()
            for i in idx:
                if items[i][0]==k: path(c,items[i][1],f)
            c.set_source_rgb(*hexc(P[k])); c.fill()
    fill(T_LU,['urban'],8,12); fill(T_LU,['grass','park','pitch'],12); fill(T_LU,['plaza'],14)
    fill(T_W,['water'])
    t,items=T_WL; idx=t.query(q)
    for k,wd in (('river',{9:.6,10:.8,11:1,12:1.6,13:2,14:2.5,15:3}.get(Z)),('stream',{14:.8,15:1.2}.get(Z))):
        if not wd: continue
        c.new_path()
        for i in idx:
            if items[i][0]==k: path(c,items[i][1],f)
        c.set_source_rgb(*hexc(P['water'])); c.set_line_width(wd*scale); c.stroke()
    if Z>=14:
        t,items=T_B; idx=t.query(q); c.new_path()
        for i in idx: path(c,items[i][1],f)
        c.set_source_rgb(*hexc(P['b'])); c.fill_preserve()
        if Z>=15: c.set_source_rgb(*hexc(P['bs'])); c.set_line_width(0.5*scale); c.stroke()
        c.new_path()
    t,items=(T_S if Z>=12 else T_MAJ); idx=t.query(q)
    byk={}
    for i in idx:
        (k,br),g=items[i]; byk.setdefault((k,br),[]).append(g)
    def stroke(geoms,col,wpx,dash=None):
        c.new_path()
        for g in geoms: path(c,g,f)
        c.set_source_rgb(*hexc(col)); c.set_line_width(wpx*scale); c.set_dash([d*scale for d in dash] if dash else []); c.stroke()
    for br in (False,True):
        wd=WID['rail'].get(Z)
        if wd and ('rail',br) in byk: stroke(byk[('rail',br)],P['rail'],wd,[3,2] if Z>=14 else None)
        if Z>=14:
            for k in ORDER:
                wd=WID[k].get(Z)
                if not wd or k=='foot' or (k,br) not in byk: continue
                cc=P['casemw'] if k=='mw' else P['casemaj'] if k in('pri','sec') else P['case']
                stroke(byk[(k,br)],cc,wd+(1.4 if br else 0.9))
        for k in ORDER:
            wd=WID[k].get(Z)
            if wd and (k,br) in byk: stroke(byk[(k,br)],P[k],wd,[1.2,1.4] if k=='foot' else None)
    buf=io.BytesIO(); surf.write_to_png(buf); buf.seek(0)
    Image.open(buf).convert('RGB').save(out,'WEBP',quality=86,method=6)
def tiles_for(bb,T):
    W,S,E,N=bb; x0,y0=[int(v) for v in merc(W,N,T,1)]; x1,y1=[int(v) for v in merc(E,S,T,1)]
    return [(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)]
def jobs():
    js=set()
    for T in range(7,11): js|={(T,x,y) for x,y in tiles_for(REGION,T)}
    for bb in TOWNS.values():
        for T in range(11,15): js|={(T,x,y) for x,y in tiles_for(bb,T)}
    return sorted(js)
if __name__=='__main__':
    root=sys.argv[1]; J=jobs(); print(len(J),'tiles per theme',file=sys.stderr)
    for theme in ('light','dark'):
        for T,x,y in J:
            d=f'{root}/{theme}/{T}/{x}'; os.makedirs(d,exist_ok=True)
            render(x,y,T,4 if T==14 else 2,theme,f'{d}/{y}.webp')
        print(theme,'done',file=sys.stderr)
