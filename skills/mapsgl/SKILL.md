---
name: mapsgl
description: This skill should be used when working with the Xweather MapsGL JS SDK (@xweather/mapsgl) — setting up a MapsGL map controller for Mapbox GL, MapLibre GL, Google Maps, or Leaflet, and adding, removing, styling, filtering, masking, or animating MapsGL weather layers and custom data layers. Use it whenever a task mentions MapsGL, aerisweather.mapsgl, addWeatherLayer, weather map layers, or client-side WebGL weather rendering. Also use it for questions about how MapsGL usage or cost is measured — sessions, the 5-minute clock intervals, the 150x access multiplier, or how many accesses a MapsGL map consumes.
license: MIT
metadata:
  author: Vaisala Xweather
  version: "0.9.0"
---

# MapsGL

MapsGL (`@xweather/mapsgl`) renders weather and custom map data client-side in WebGL, layered on
top of Mapbox GL, MapLibre GL, Google Maps, or Leaflet. It requires an active Xweather account
with Weather API + Maps access (client id + secret).

## How to write MapsGL code examples

**Default to a single self-contained HTML file using vanilla JavaScript and the CDN build.** One
file the user can save and open in a browser — CDN `<script>`/`<link>` tags, a `<div>` for the map,
and a plain `<script>` block. No build step, no bundler, no package installs, no framework.

In that form, MapsGL lives on the global `aerisweather.mapsgl` namespace:

```javascript
const account = new aerisweather.mapsgl.Account('CLIENT_ID', 'CLIENT_SECRET');
const controller = new aerisweather.mapsgl.MapboxMapController(map, { account });
```

Only produce **npm / ES-module / bundler** code when the user explicitly asks for it, or when they're
plainly already working in such a project — an existing `package.json`, a `src/` tree with imports, or
they name a bundler. Same for **React or any other framework**: only on explicit request. Don't offer
a framework version alongside the vanilla one "in case", and don't reach for a framework because the
task looks app-shaped.

When the user is in an npm project, the translation is mechanical: swap the CDN tags for
`import * as mapsgl from '@xweather/mapsgl'` plus the map library's own import, and replace
`aerisweather.mapsgl.` with `mapsgl.`. Everything else — the controller API, layer codes, paint
objects, expressions — is identical, so the rest of this skill applies unchanged.

## Core concepts

| Concept | What it is |
|---|---|
| `Account` | Wraps client id/secret credentials used for all data requests |
| `MapController` | Adapter between the underlying map instance (Mapbox/MapLibre/Google/Leaflet) and MapsGL — the object almost everything below is called on |
| `DataSource` | Where layer data comes from: `raster`, `vector`, `geojson`, or `encoded` (RGBA-packed weather grids) |
| `WebGLLayer` | A visual rendering of a source: `raster`, `fill`, `line`, `circle`, `sample`, `grid`, `contour`, `particle`, `heatmap`, `symbol` |
| `paint` | Per-layer style config (colors, radii, colorscales, etc.), keyed by render type — see `references/styles.md` |
| Expressions | `['operator', ...args]` arrays for data-driven paint values and `filter`s — see `references/expressions.md` |
| `ColorScale` | Maps a continuous data range to a color gradient/steps, used by `paint.sample`/`paint.heatmap` and gradient legends — see `references/color-scales.md` |
| Legend (`LegendControl`) | An on-map UI element showing what a layer's colors/symbols mean; categorical (`points`) or gradient (`bar`) — see `references/legends.md` |
| `DataInspectorControl` | An on-map UI element that shows raw layer values at the clicked/hovered point |
| `timeline` (`Timeline`) | Drives time-based animation (play/pause/scrub) across every animated layer on a controller at once — see `references/timeline.md` |

Built-in **weather layers** are pre-wired combinations of an encoded source + one or more styled
layers, addressed by a single string code (e.g. `'temperatures'`, `'radar'`, `'alerts'`). Prefer
these over hand-building sources/layers unless visualizing custom or non-weather data.

## Usage is measured in sessions

MapsGL bills in **sessions**, not tiles, layers, or requests. A session is a continuous interaction
with a MapsGL map for **up to 5 minutes**, starting when any weather layer is added. On a Weather API
and Maps subscription, **1 session = 150 accesses** (a 150× multiplier).

Three rules produce every answer:

1. **Sessions align to the wall clock** — boundaries at `:00`, `:05`, `:10`, `:15`. Not a rolling
   window from first interaction. What matters is how many 5-minute buckets the viewing touches, not
   how long it lasted.
2. **At least one session per data request.** No proration — 150 accesses is the floor.
3. **Inside a session, everything is free**: panning, zooming, animating, refreshing, and toggling
   layers. **Layer count does not affect cost.**

**When asked how usage is measured, show the arithmetic** — buckets → sessions → accesses — rather
than just a number. The documented example:

> A user views a radar layer from **8:03 to 8:07** — 4 minutes, but it straddles the `:05` boundary,
> so it touches two buckets (8:00–8:05 and 8:05–8:10) = **2 sessions = 300 accesses**.
>
> The same 4 minutes from **8:05 to 8:09** touches one bucket = **1 session = 150 accesses**. Same
> duration, half the cost, purely from clock alignment.

Two consequences worth volunteering unprompted, because they invert the intuition people bring from
tile-based pricing:

> **Adding layers is free.** Five layers viewed for four minutes costs 1 session — the same as one
> layer. There is no cost reason to limit how many layers a user enables. (On Raster Maps the same
> five layers would cost 5×.)
>
> **Short visits get almost no discount.** A 30-second view averages ~1.1 sessions and a 5-minute
> view ~2.0, so a visit ten times shorter costs 55% as much, not 10%. Drive-by page loads are the
> expensive traffic shape.

For capacity planning, a view of `d` minutes starting at a random time averages
`floor(d/5) + 1 + (d mod 5)/5` sessions — **not** `d/5`. Assuming one session per short view
underestimates by 10–20%. Table of common durations in `references/sessions.md`.

The only real lever is **when layers are on the map**: don't call `addWeatherLayer` until the user
asks for weather, and `removeWeatherLayer` when the map goes out of view or idle. Optimising layer
count, animation, or interaction is pointless — those are free.

Full model, more worked examples (long-running displays, high-traffic short visits), the MapsGL vs.
Raster Maps billing comparison, and reduction tactics: `references/sessions.md`.

## Setup

### 1. Get API credentials

MapsGL needs **two separate sets of credentials**, and both are required — the map won't render
without either one:

1. **Xweather account keys** (`CLIENT_ID` / `CLIENT_SECRET`) — generated from the account portal at
   **https://data.portal.xweather.com/account/keys**. These authenticate MapsGL's own data
   requests and are what get passed to `new aerisweather.mapsgl.Account(id, secret)`.
2. **The underlying map provider's own key/token** — independent of Xweather:
   - Mapbox GL → `mapboxgl.accessToken` (Mapbox account access token)
   - MapLibre GL → no key needed, but the `style` URL usually comes from a tile provider (e.g.
     MapTiler) that does require its own key
   - Google Maps → a Google Maps JavaScript API key, plus a **Map ID** with vector-map
     support enabled (required — MapsGL renders as a WebGL overlay on the vector basemap)
   - Leaflet → no key needed for the base `L.tileLayer`, though the tile provider used may require one

If a user reports "nothing renders" or an auth error, check both credential sets before digging
into MapsGL-specific config.

### 2. Install

Every install needs `@xweather/mapsgl` **plus** the map library being wrapped — MapsGL does not
bundle it, whether installing via CDN or npm.

**CDN** — include the map provider's own `<link>`/`<script>` tags *in addition to* MapsGL's, not
instead of them. MapsGL's CDN build exposes everything under `window.aerisweather.mapsgl`:

```html
<!-- 1. The underlying map library — example shown for Mapbox GL, swap for MapLibre/Leaflet's own CDN tags -->
<link href="https://api.mapbox.com/mapbox-gl-js/v3.12.0/mapbox-gl.css" rel="stylesheet" />
<script defer src="https://api.mapbox.com/mapbox-gl-js/v3.12.0/mapbox-gl.js"></script>

<!-- 2. MapsGL itself -->
<link href="https://cdn.aerisapi.com/sdk/js/mapsgl/1.9.2/aerisweather.mapsgl.css" rel="stylesheet" />
<script defer src="https://cdn.aerisapi.com/sdk/js/mapsgl/1.9.2/aerisweather.mapsgl.js"></script>
```

Per-provider CDN includes:

| Provider | CDN tags |
|---|---|
| Mapbox GL | `https://api.mapbox.com/mapbox-gl-js/<version>/mapbox-gl.{css,js}` |
| MapLibre GL | e.g. `https://unpkg.com/maplibre-gl@<version>/dist/maplibre-gl.{css,js}` |
| Leaflet | e.g. `https://unpkg.com/leaflet@<version>/dist/leaflet.{css,js}` |
| Google Maps | `<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>` (no separate CSS) |

Pin an explicit version for every `<script>`/`<link>` tag (MapsGL's and the map library's) rather
than `latest`, for anything beyond a quick prototype.

**npm** — *only when the user is already in a bundled project or asks for it.* Install
`@xweather/mapsgl` plus whichever provider package applies:
```bash
npm install --save @xweather/mapsgl mapbox-gl        # Mapbox GL
npm install --save @xweather/mapsgl maplibre-gl       # MapLibre GL
npm install --save @xweather/mapsgl leaflet           # Leaflet
npm install --save @xweather/mapsgl                   # Google Maps — loaded via <script> from Google, no npm package needed
```
```javascript
import * as mapsgl from '@xweather/mapsgl';
import '@xweather/mapsgl/dist/mapsgl.css';
```

### 3. Container markup

The map container needs explicit dimensions — a blank/invisible map is almost always a missing
CSS rule, not a JS error:
```html
<div id="map"></div>
<style>
  body, html { margin: 0; padding: 0; }
  #map { width: 100%; height: 100vh; }
</style>
```

### 4. Initialize a controller

Every provider follows the same pattern: create the native map, wrap it in the matching
`*MapController`, wait for `load`, then add layers. Only the map-creation step differs.

```javascript
mapboxgl.accessToken = 'MAPBOX_TOKEN';
const map = new mapboxgl.Map({
  container: document.getElementById('map'),
  style: 'mapbox://styles/mapbox/light-v11',
  center: [-74.5, 40],
  zoom: 3
});

const account = new aerisweather.mapsgl.Account('CLIENT_ID', 'CLIENT_SECRET');
const controller = new aerisweather.mapsgl.MapboxMapController(map, { account });

controller.on('load', () => {
  controller.addWeatherLayer('temperatures');
});
```

| Provider | Controller class | Map constructor |
|---|---|---|
| Mapbox GL | `MapboxMapController` | `new mapboxgl.Map({...})` |
| MapLibre GL | `MaplibreMapController` | `new maplibregl.Map({...})` |
| Google Maps | `GoogleMapController` | `new google.maps.Map(el, { mapId: '...', ... })` |
| Leaflet | `LeafletMapController` | `L.map('map').setView([lat, lon], zoom)` |

All four take `(map, { account, units?, animation? })`. Google's variant also accepts
`interleaved?: boolean`. **Always gate MapsGL calls behind `controller.on('load', ...)`** —
calling layer/source methods before load throws.

The four controller constructors and the complete controller API (properties, events, all methods)
are in `references/api-reference.md`.

## Complete example

**This is the shape to produce by default** — one file, saveable and openable in a browser. Adapt it
rather than starting from scratch: swap the map provider's CDN tags and constructor, change the
`addWeatherLayer` codes, and adjust `center`/`zoom`.

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MapsGL + Mapbox GL</title>

    <link href="https://api.mapbox.com/mapbox-gl-js/v3.12.0/mapbox-gl.css" rel="stylesheet" />
    <script defer src="https://api.mapbox.com/mapbox-gl-js/v3.12.0/mapbox-gl.js"></script>

    <link href="https://cdn.aerisapi.com/sdk/js/mapsgl/1.9.2/aerisweather.mapsgl.css" rel="stylesheet" />
    <script defer src="https://cdn.aerisapi.com/sdk/js/mapsgl/1.9.2/aerisweather.mapsgl.js"></script>

    <style>
    body, html { margin: 0; padding: 0; }
    #map { height: 100vh; width: 100%; }
    </style>
</head>
<body>
    <div id="map"></div>

    <script>
        window.addEventListener('load', () => {
            mapboxgl.accessToken = 'MAPBOX_TOKEN';
            const map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/light-v11',
                center: [-85.5, 40],
                zoom: 3
            });

            const account = new aerisweather.mapsgl.Account('CLIENT_ID', 'CLIENT_SECRET');
            const controller = new aerisweather.mapsgl.MapboxMapController(map, { account });

            controller.on('load', () => {
                // built-in weather layer, unstyled
                controller.addWeatherLayer('radar');

                // built-in weather layer with a custom style override
                controller.addWeatherLayer('alerts-outline', {
                    paint: {
                        opacity: 0.5
                    }
                });
            });
        });
    </script>
</body>
</html>
```

Source: https://www.xweather.com/docs/mapsgl/examples/mapbox

Two details that matter in the single-file form specifically:

- The CDN tags use `defer`, so wrap the setup in `window.addEventListener('load', ...)`. Without it,
  `mapboxgl` and `aerisweather` aren't defined yet and the script throws.
- `#map` needs an explicit height. A silently blank map is nearly always this, not a JS error.

### npm / ES modules — only when asked

Same structure: swap the CDN `<script>` tags for package imports, and `aerisweather.mapsgl.` for the
imported `mapsgl.` namespace. The `window.addEventListener('load', ...)` wrapper is unnecessary since
bundlers execute the module after the DOM is parsed (keep a `defer`/module script tag, or bundle into
the page's entry point). Nothing else changes.

```javascript
// main.js — loaded via <script type="module" src="./main.js"></script>
import mapboxgl from 'mapbox-gl';
import * as mapsgl from '@xweather/mapsgl';
import 'mapbox-gl/dist/mapbox-gl.css';
import '@xweather/mapsgl/dist/mapsgl.css';

mapboxgl.accessToken = 'MAPBOX_TOKEN';
const map = new mapboxgl.Map({ container: 'map', style: 'mapbox://styles/mapbox/light-v11', center: [-85.5, 40], zoom: 3 });

const account = new mapsgl.Account('CLIENT_ID', 'CLIENT_SECRET');
const controller = new mapsgl.MapboxMapController(map, { account });

controller.on('load', () => {
  controller.addWeatherLayer('radar');
});
```

The host page is then just the container plus `<script type="module" src="./main.js"></script>` — the
`#map` height rule still applies.

## Adding, removing, and listing weather layers

```javascript
controller.addWeatherLayer('radar');
controller.addWeatherLayer('wind-particles');

// with overrides (data quality, time clamping, paint, legend, mask, filter, ...)
controller.addWeatherLayer('temperatures', {
  data: { quality: aerisweather.mapsgl.DataQuality.low },
});

controller.hasWeatherLayer('radar');            // boolean
controller.getWeatherLayer('temperatures');     // WebGLLayer | WebGLLayer[] | undefined
controller.setWeatherLayerVisibility('radar', false);  // hide without disposing
controller.removeWeatherLayer('radar');         // fully removes + frees resources

controller.weatherLayerIds;                     // currently-active weather layer codes
```

**A weather layer's code (e.g. `'temperatures'`) is not the same string as its actual layer id.**
If you'll need to update a weather layer's style/opacity/visibility-via-`.show()`/`.hide()` later,
capture what `addWeatherLayer` returns (or call `getWeatherLayer(code)` later) and operate on that
`WebGLLayer` instance directly — don't pass the code to `controller.setPaintProperty()`,
`getLayer()`, or `moveLayer()`, which expect the real layer id and will silently no-op on a code
they don't recognize. Composite codes return an **array** of layers to iterate over. Full
explanation and verified example in `references/weather-layers.md`.

**Never guess a layer code — look it up.** `references/layers.md` lists all 283 layers by category
with their render type, animatability, cost multiplier, coverage, data range, and update interval. It
is generated from the public catalog and refreshed weekly, so grep it first; no network call needed.

If a code isn't there, or the snapshot looks stale, fetch the live catalog:

```
https://www.xweather.com/docs/api/mapsgl/layers
```

A plain public JSON endpoint (no auth) returning `{ layers: [{ id, title, description, type,
categories, animatable, dataRange, dataCoverage, updateInterval, multiplier }, ...] }`. It overrides
the snapshot. For what the **authenticated account** can actually render — neither file knows about
entitlements — ask at runtime:

```javascript
controller.weatherProvider.getLayerMetadata().then((data) => console.log(data));
```

Some codes are **composite** (expand to multiple sub-layers, e.g. `boundaries`, `roads`,
`stormcells`) — `addWeatherLayer` returns an array for these, and `overrides.childLayers` can
target one sub-layer by id. All 14 composite codes are listed together at the top of
`references/layers.md`; they're the ones with render type `none`.

A layer's **render type also tells you how to style it** — a `sample` layer takes
`paint.sample.colorscale`, a `line` layer takes `paint.stroke`. Reading the type out of
`layers.md` before writing a `paint` override saves a round of guessing.

## Styling layers

Pass a `paint` object namespaced by render type. Full property tables for every render type
(`raster`, `fill`, `stroke`/`line`, `circle`, `sample`, `grid`, `contour`, `particle`, `heatmap`,
`icon`, `symbol`, `text`) are in `references/styles.md`.

**Always use MapsGL expressions — `['operator', ...args]` arrays — for any data-driven paint
value** (color/size/opacity derived from a feature property), not evaluator functions or the
`{ property }` shorthand. See `references/expressions.md` for the full operator reference.

```javascript
controller.addWeatherLayer('temperatures', {
  paint: {
    sample: {
      colorscale: {
        stops: [-40, '#58005b', 0, '#81e8ff', 20, '#ecf93d', 40, '#6b0001'],
        interval: 5
      }
    }
  }
});
```

Update a style after the layer exists — **for built-in weather layers, get the actual layer
instance first; the weather layer code is not a valid layer id** (see the "code vs. id" gotcha
below):
```javascript
const tempLayer = controller.getWeatherLayer('temperatures');   // or capture addWeatherLayer's return value
tempLayer.setPaintProperty('sample.colorscale', newColorScale);
```
For a layer you created yourself with `addLayer(id, ...)`, the id you chose *is* the real layer id,
so `controller.setPaintProperty(id, prop, value)` works directly.

**Custom (non-weather) layer**, styled with a static or data-driven fill:
```javascript
controller.addSource('alerts', {
  type: 'vector',
  url: 'https://maps{s}.aerisapi.com/CLIENT_ID_CLIENT_SECRET/alerts/{z}/{x}/{y}/0.pbf'
});
controller.addLayer('alerts-fill', {
  type: 'fill',
  source: 'alerts',
  paint: { fill: { color: ['get', 'COLOR'], opacity: 0.6 } }
});
// ...
controller.removeLayer('alerts-fill');
controller.removeSource('alerts');   // only after no layers reference it
```

For color scales (built-in named palettes + custom stops) see `references/color-scales.md`.
For expression syntax (data-driven values and `filter`) see `references/expressions.md`.
For layer masking (e.g. clip a weather layer to land/water or another layer's geometry) and
`filter`, see the bottom of `references/styles.md`.

## Custom data sources

Four source types: `raster`, `vector` (MVT), `geojson`, `encoded` (RGBA-packed grids — used
internally by weather layers, rarely built by hand). See `references/api-reference.md` for full
constructor options per type. Quick pattern:

```javascript
controller.addSource('earthquakes', {
  type: 'geojson',
  data: 'https://data.api.xweather.com/earthquakes/search?query=mag:1&limit=200&format=geojson&client_id=ID&client_secret=SECRET'
});
controller.getSource('earthquakes').setUrl('...');       // swap remote data
controller.getSource('earthquakes').setData({ ... });    // set static data directly
```

## Animating over time

`controller.timeline` controls playback across every animated layer at once. Full API
(setting ranges by Date/offset/relative string, speed, play/pause/goTo) is in
`references/timeline.md`. Quick start:

```javascript
controller.on('load', () => {
  controller.timeline.setStartDateUsingRelativeTime('-3 hours');
  controller.timeline.duration = 1.5;   // seconds per loop
  controller.timeline.play();
});
```

## Legends & data inspection

```javascript
controller.addLegendControl('#legend-container');   // auto-syncs with active weather layers
controller.removeLegendControl();

controller.addDataInspectorControl({ event: 'click' });  // click/hover to inspect raw values
controller.removeDataInspectorControl();
```

**If you override a layer's `paint` colors, override its `legend` too.** Auto-detection only works for
unmodified color scales, so a custom paint with a default legend produces a legend that lies about the
map. Use `legend: { points: {...} }` for categorical data and `legend: { bar: {...} }` for a
continuous gradient — and for a gradient, pass the **same `colorscale` stops** to both so they can't
drift apart:

```javascript
controller.addWeatherLayer('temperatures', {
  paint:  { sample: { colorscale: myColorscale } },
  legend: { bar: { colorscale: myColorscale, measurement: { type: 'temperature', units: 'C' } } }
});
```

Full field reference plus complete categorical and gradient examples: `references/legends.md`.

## Querying data at a point

```javascript
const results = controller.query({ lat: 40, lon: -74.5 });   // sync
const results = await controller.queryPromise({ lat: 40, lon: -74.5 });
// -> { [layerId]: sampled value(s) / feature(s) at that coordinate }
```

## Checklist for common tasks

- **"Build me a map / show me an example"** → one self-contained HTML file, vanilla JS, CDN tags,
  `aerisweather.mapsgl.*`. No bundler or framework unless explicitly requested. See
  "How to write MapsGL code examples" above.
- **"Add a weather layer"** → `controller.addWeatherLayer(code)` inside `on('load', ...)`; look the
  code up in `references/layers.md`, or fetch
  `https://www.xweather.com/docs/api/mapsgl/layers` if it isn't listed there.
- **"Remove/hide a layer"** → `removeWeatherLayer` (frees resources) vs
  `setWeatherLayerVisibility(code, false)` (cheap toggle, keeps resources loaded).
- **"Change the colors/thresholds of a layer"** → override `paint.sample.colorscale` (see
  `references/color-scales.md`); remember stop values must be in the data's native metric units.
- **"Toggle/update a weather layer's opacity or paint from a UI control (slider, checkbox, etc.)"**
  → don't call `controller.setPaintProperty(code, ...)` with the weather layer code — get the real
  layer with `controller.getWeatherLayer(code)` (or the value returned by `addWeatherLayer`) and
  call `.setPaintProperty(...)` on it directly; handle the array case for composite codes. This is
  the single most common silent-failure bug with built-in weather layers — see
  `references/weather-layers.md`.
- **"Only show values above/below X"** → `paint.sample.drawRange` for continuous data, or a
  `filter` expression for vector/geojson layers.
- **"Style based on a feature property"** → an expression: `['get', 'FIELD']` for a direct value,
  `['match', ['get', 'FIELD'], ...]` for categorical colors/sizes, `['interpolate', ['linear'],
  ['get', 'FIELD'], ...]` for continuous ranges. See `references/expressions.md`.
- **"Animate over time / add a time slider"** → `controller.timeline`, see `references/timeline.md`.
- **"Show a legend"** → `addLegendControl`; override `legend.points` (categorical) or `legend.bar`
  (gradient) if paint was customized — see `references/legends.md`.
- **"Add my own data (not a built-in weather layer)"** → `addSource` + `addLayer` with an explicit
  `type`/`paint`; see `references/api-reference.md`.
- **"What layers/options are available?"** → `references/layers.md` for the full listing by category;
  `https://www.xweather.com/docs/api/mapsgl/layers` if that snapshot might be stale; or
  `controller.weatherProvider.getLayerMetadata()` at runtime for account-specific availability. Never
  invent a code from memory — one of these three always has the answer.
- **"How many accesses / how much does this cost?"** → sessions, not tiles or layers: count the
  5-minute clock buckets the viewing touches, × 150 accesses. Show the arithmetic and mention that
  layers and interaction are free inside a session. See `references/sessions.md`.
- **"Handle load errors / show an error state"** → there is no `controller.on('error', ...)` —
  that event doesn't exist on `MapController` and will never fire. See the events note in
  `references/api-reference.md`.

## Reference files

- `references/api-reference.md` — full `Account`, `MapController`, and `DataSource` API (all methods, properties, events, per-provider setup)
- `references/layers.md` — all 283 weather layers by category: code, description, render type, animatability, cost multiplier, coverage, data range, update interval; composite codes and cost multipliers grouped up front
- `references/weather-layers.md` — how to discover layer codes, the catalog schema, and the code-vs-layer-id gotcha that silently breaks style updates
- `references/styles.md` — paint property spec for every render type, plus filters and masks
- `references/color-scales.md` — color scale config format and built-in named palettes
- `references/expressions.md` — style/filter expression operator reference
- `references/legends.md` — `points` (categorical) and `bar` (gradient) legend config reference
- `references/timeline.md` — animation/timeline API
- `references/sessions.md` — how MapsGL usage is measured: the session model, clock-aligned billing, worked examples, the MapsGL vs. Raster Maps comparison, and how to reduce consumption
