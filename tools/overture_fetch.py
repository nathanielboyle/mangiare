import os, sys, time, pyarrow.dataset as ds, pyarrow.fs as fs, pyarrow.compute as pc, pyarrow.parquet as pq
REL="overturemaps-us-west-2/release/2026-09-23.1"
px=os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
s3=fs.S3FileSystem(anonymous=True, region='us-west-2', proxy_options=px)
def fetch(theme, typ, out, bbox=(12.33,41.76,12.66,42.02), cols=None):
    t=time.time()
    d=ds.dataset(f"{REL}/theme={theme}/type={typ}/", filesystem=s3, format='parquet')
    f=((pc.field('bbox','xmin')<bbox[2])&(pc.field('bbox','xmax')>bbox[0])&(pc.field('bbox','ymin')<bbox[3])&(pc.field('bbox','ymax')>bbox[1]))
    tb=d.to_table(filter=f, columns=cols)
    pq.write_table(tb,out); print(typ, tb.num_rows, round(time.time()-t), 's', file=sys.stderr)
if __name__=='__main__':
    fetch(sys.argv[1], sys.argv[2], sys.argv[3])
