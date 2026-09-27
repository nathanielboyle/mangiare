"""Assemble index.html from template.html + Leaflet CSS + places.json."""
import json, pathlib, re, sys
here = pathlib.Path(__file__).resolve().parent
root = here.parent
css = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else (here / 'leaflet.css').read_text()
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
data = json.loads((root / 'places.json').read_text())
html = (here / 'template.html').read_text()
html = html.replace('/*__LEAFLET_CSS__*/', css).replace('/*__DATA__*/[]', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
(root / 'index.html').write_text(html)
print('index.html', len(html), 'bytes,', len(data), 'places')
