# Mangiare a Roma

An interactive map of the 76 places in *The Katie Parla Guide to Eating Well in Rome* (April 2026): trattorie, pizzerie, pizza in teglia, quick bites, sweets, gelato, and markets & shops. Every branch the guide names gets its own pin. This is an unofficial companion map.

Open `index.html` from a local web server (for example, `python3 -m http.server` in this folder). The map tiles load from `tiles/`, so opening the file directly from disk won't show the basemap.

## Features

- A pin for each place, colored and iconed by style, with a popup showing the name, style, address, a short description, any note the guide gives, and a Google Maps directions link.
- Filters by style, neighborhood, and search text. The list can be grouped by area or by style.
- "Want to go" and "Been" marks, saved in the browser's `localStorage`.
- Light and dark basemaps rendered specially for this map from OpenStreetMap and Overture Maps data.

## How the data was built

1. The place names and neighborhoods come from the guide PDF.
2. Street addresses came from web research, which also confirmed each place is still open (September 2026).
3. Coordinates come from matching each address to Italy's civic-number register, as published in Overture Maps (`theme=addresses`). Every address matched a numbered point exactly, and each point was cross-checked against a same-named business in Overture's `places` data. Six markets use the place point instead.
4. The basemap tiles are rendered by `tools/render_tiles.py` from Overture's `base`, `buildings` and `transportation` themes.

Files:

- `places.json`: the dataset.
- `src/template.html` and `src/build.py`: assemble `index.html`, inlining Leaflet's CSS and the data.
- `tools/`: the Overture fetch, geocoding, dataset and tile scripts used to build the map. They expect the downloaded parquet files in `geo/`.

To rebuild the page after editing `places.json` or the template, run `python3 src/build.py`.

Left out: L'Elementare's summer-only Parco Appio venue.
