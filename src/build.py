"""Assemble the map page.

    python3 src/build.py                 # index.html (artifact page fragment)
    python3 src/build.py --site _site    # also a standalone site for GitHub Pages:
                                         # full HTML document, tiles, web app manifest,
                                         # icons and an offline service worker
"""
import argparse, hashlib, json, math, pathlib, re, shutil

here = pathlib.Path(__file__).resolve().parent
root = here.parent

ap = argparse.ArgumentParser()
ap.add_argument('--site', help='write a standalone site into this directory')
args = ap.parse_args()

css = re.sub(r'/\*.*?\*/', '', (here / 'leaflet.css').read_text(), flags=re.S)
data = json.loads((root / 'places.json').read_text())
html = (here / 'template.html').read_text()
html = html.replace('/*__SCRIPT__*/', (here / 'app.js').read_text())
html = html.replace('/*__LEAFLET_CSS__*/', css).replace('/*__DATA__*/[]', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
(root / 'index.html').write_text(html)
print('index.html', len(html), 'bytes,', len(data), 'places')

if args.site:
    site = pathlib.Path(args.site).resolve()
    if site.exists():
        shutil.rmtree(site)
    shutil.copytree(root / 'tiles', site / 'tiles')
    for f in (here / 'site').iterdir():
        shutil.copy(f, site / f.name)

    # Tile list per region and theme, for the "Save map for offline" button.
    def tile_lng(z, x):  # center longitude of a tile column
        return (x + 0.5) / 2 ** z * 360 - 180
    offline = {}
    for p in sorted((site / 'tiles').rglob('*.webp')):
        theme, z, x = p.relative_to(site / 'tiles').parts[:3]
        region = 'roma' if tile_lng(int(z), int(x)) < 15 else 'puglia'
        e = offline.setdefault(region, {}).setdefault(theme, {'files': [], 'bytes': 0})
        e['files'].append(str(p.relative_to(site)))
        e['bytes'] += p.stat().st_size
    (site / 'offline.json').write_text(json.dumps(offline, separators=(',', ':')))

    version = hashlib.sha1(html.encode()).hexdigest()[:10]
    sw = (site / 'sw.js').read_text().replace('__VERSION__', version)
    (site / 'sw.js').write_text(sw)

    head = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="Food map of Rome and Puglia: trattorie, pizzerie, bakeries, gelato and markets.">\n'
        '<meta name="theme-color" content="#FBF9F5" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#1A1917" media="(prefers-color-scheme: dark)">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="Mangiare">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="icon" href="icon-192.png">\n'
        '<link rel="apple-touch-icon" href="icon-180.png">\n'
        '<style>[hidden]{display:none!important}</style>\n'
    )
    page = html.replace('<div class="app">', '</head>\n<body data-standalone>\n<div class="app">', 1)
    (site / 'index.html').write_text(head + page + '\n</body>\n</html>\n')
    n = sum(len(t['files']) for r in offline.values() for t in r.values())
    print(f'site: {site} ({n} tiles, sw {version})')
