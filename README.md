# Mangiare a Roma (e in Puglia)

An interactive food map with two regions, switched at the top of the page (`#puglia` links straight to the second):

- **Roma:** the 76 places in *The Katie Parla Guide to Eating Well in Rome* (April 2026): trattorie, pizzerie, pizza in teglia, quick bites, sweets, gelato, and markets & shops. Every branch the guide names gets its own pin.
- **Puglia:** 22 restaurants, bakeries, bars and gelaterie from the *Puglia Restaurant Guide (via Katie Parla)* notes, from Bari down to Patù. Take Five in Bari is left out because it has closed.

This is an unofficial companion map.

Open `index.html` from a local web server (for example, `python3 -m http.server` in this folder). The map tiles load from `tiles/`, so opening the file directly from disk won't show the basemap.

## GitHub Pages (phone and offline)

`.github/workflows/pages.yml` builds a standalone copy of the site (`python3 rome-food-map/src/build.py --site _site`) and deploys it to GitHub Pages on every push to `main` that touches this folder. You can also run it by hand from the Actions tab. The site is published at https://nathanielboyle.github.io/clubstack/.

The Pages build adds things the claude.ai artifact can't have:

- A web app manifest and icons, so **Add to Home Screen** opens the map full-screen like an app.
- A service worker that keeps the page and every map tile you've viewed available offline.
- A **Save … map for offline** button that downloads a region's tiles for the current light or dark theme: about 24 MB (light) or 16 MB (dark) for Rome, and 6 MB or 4 MB for Puglia.

"Directions" links still need a connection, since they open Google Maps.

## Features

- A pin for each place, colored and iconed by style, with a popup showing the name, style, address, a short description, any note the guide gives, and a Google Maps directions link.
- Filters by style, neighborhood, and search text. The list can be grouped by area or by style.
- "Want to go" and "Been" marks, saved in the browser's `localStorage`.
- Light and dark basemaps rendered specially for this map from OpenStreetMap and Overture Maps data.

## How the data was built

1. The place names and neighborhoods come from the guide PDF.
2. Street addresses came from web research, which also confirmed each place is still open (September 2026).
3. Coordinates come from matching each address to Italy's civic-number register, as published in Overture Maps (`theme=addresses`). Every address matched a numbered point exactly, and each point was cross-checked against a same-named business in Overture's `places` data. Six markets use the place point instead.
4. The basemap tiles are rendered from Overture's `base`, `buildings` and `transportation` themes: `tools/render_tiles.py` for Rome (street level everywhere), and `tools/render_tiles_puglia.py` for Puglia. Puglia has a regional map up to zoom 11, plus street-level detail for Bari, Polignano a Mare, Monopoli and Lecce. Both regions share one tile tree, since their tile coordinates don't overlap.
5. Puglia coordinates were matched the same way. Three exceptions are Da Tuccino (a rural contrada, so the pin is approximate), La Rotonda (no civic number; the listing on the SP90 is used) and Bleu Salento (the marina, no civic number).

Files:

- `places.json`: the dataset.
- `src/template.html`, `src/app.js` and `src/build.py`: assemble `index.html`, inlining Leaflet's CSS, the script and the data.
- `src/site/`: the extra files for the Pages build (service worker, manifest, icons).
- `tools/`: the Overture fetch, geocoding, dataset and tile scripts used to build the map. They expect the downloaded parquet files in `geo/`.

To rebuild the page after editing `places.json` or the template, run `python3 src/build.py`.

Left out: L'Elementare's summer-only Parco Appio venue.
