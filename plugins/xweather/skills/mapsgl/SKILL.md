---
name: mapsgl
description: This skill should be used when working with the Xweather MapsGL JS SDK (@xweather/mapsgl) — setting up a MapsGL map controller for Mapbox GL, MapLibre GL, Google Maps, or Leaflet, and adding, removing, styling, filtering, masking, or animating MapsGL weather layers and custom data layers. Use it whenever a task mentions MapsGL, aerisweather.mapsgl, addWeatherLayer, weather map layers, or client-side WebGL weather rendering.
version: 0.1.0
---

# MapsGL

MapsGL (`@xweather/mapsgl`) renders weather and custom map data client-side in WebGL, layered on
top of Mapbox GL, MapLibre GL, Google Maps, or Leaflet. It requires an active Xweather account
with Weather API + Maps access (client id + secret).

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

Session billing note: a MapsGL "session" is up to 5 minutes of continuous interaction with any
active weather layer, billed in fixed 5-minute clock intervals; with a Weather API + Maps
subscription, 1 session = 150 accesses. This doesn't affect API usage, just worth knowing when a
user asks about cost/usage.

## Setup

### 1. Get API credentials

MapsGL needs **two separate sets of credentials**, and both are required — the map won't render
without either one:

1. **Xweather account keys** (`CLIENT_ID` / `CLIENT_SECRET`) — generated from the account portal at
   **https://data.portal.xweather.com/account/keys**. These authenticate MapsGL's own data
   requests and are what get passed to `new mapsgl.Account(id, secret)`.
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

**npm** — install `@xweather/mapsgl` plus whichever provider package applies:
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
import mapboxgl from 'mapbox-gl';
import * as mapsgl from '@xweather/mapsgl';
import 'mapbox-gl/dist/mapbox-gl.css';
import '@xweather/mapsgl/dist/mapsgl.css';

mapboxgl.accessToken = 'MAPBOX_TOKEN';
const map = new mapboxgl.Map({
  container: document.getElementById('map'),
  style: 'mapbox://styles/mapbox/light-v11',
  center: [-74.5, 40],
  zoom: 3
});

const account = new mapsgl.Account('CLIENT_ID', 'CLIENT_SECRET');
const controller = new mapsgl.MapboxMapController(map, { account });

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

Full per-provider snippets and the complete controller API (properties, events, all methods) are
in `references/api-reference.md`.

## Complete example

### CDN (plain HTML)

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

### npm (ES modules)

Same structure — swap the CDN `<script>` tags for package imports, and `aerisweather.mapsgl` for
the imported `mapsgl` namespace. No `window.addEventListener('load', ...)` wrapper is needed since
bundlers execute the module after the DOM is parsed (keep a `defer`/module script tag, or bundle
into the page's entry point).

```bash
npm install --save @xweather/mapsgl mapbox-gl
```

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MapsGL + Mapbox GL</title>
  <style>
    body, html { margin: 0; padding: 0; }
    #map { height: 100vh; width: 100%; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script type="module" src="./main.js"></script>
</body>
</html>
```

```javascript
// main.js
import mapboxgl from 'mapbox-gl';
import * as mapsgl from '@xweather/mapsgl';
import 'mapbox-gl/dist/mapbox-gl.css';
import '@xweather/mapsgl/dist/mapsgl.css';

mapboxgl.accessToken = 'MAPBOX_TOKEN';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v11',
  center: [-85.5, 40],
  zoom: 3
});

const account = new mapsgl.Account('CLIENT_ID', 'CLIENT_SECRET');
const controller = new mapsgl.MapboxMapController(map, { account });

controller.on('load', () => {
  controller.addWeatherLayer('radar');
  controller.addWeatherLayer('alerts-outline', {
    paint: { opacity: 0.5 }
  });
});
```

## Adding, removing, and listing weather layers

```javascript
controller.addWeatherLayer('radar');
controller.addWeatherLayer('wind-particles');

// with overrides (data quality, time clamping, paint, legend, mask, filter, ...)
controller.addWeatherLayer('temperatures', {
  data: { quality: mapsgl.DataQuality.low },
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

**Never hardcode or guess a layer code.** Look it up live from the public layer catalog endpoint:

```
https://www.xweather.com/docs/api/mapsgl/layers
```

Fetch this JSON endpoint (no auth needed) whenever a task needs to find, browse, or verify a layer
code — it returns `{ layers: [{ id, title, description, type, categories, animatable,
dataRange, dataCoverage, updateInterval, multiplier }, ...] }` for all ~280+ built-in layers.
See `references/weather-layers.md` for the full schema and category list. For account/plan-specific
availability at runtime, also consider:

```javascript
controller.weatherProvider.getLayerMetadata().then((data) => console.log(data));
```

Some codes are **composite** (expand to multiple sub-layers, e.g. `boundaries`, `roads`,
`stormcells`) — `addWeatherLayer` returns an array for these, and `overrides.childLayers` can
target one sub-layer by id.

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

If a weather layer's `paint` is overridden with custom colors, also override its `legend` so the
legend reflects the real styling (auto-detection only works for unmodified color scales). Use
`legend: { points: {...} }` for categorical data and `legend: { bar: {...} }` for a continuous
gradient (e.g. a custom temperature colorscale) — full field reference in `references/legends.md`.

```javascript
const riskColors = {
  general: '#ffea16', marginal: '#ffc41d', slight: '#ff891d',
  enhanced: '#fa2311', moderate: '#fa23ec', high: '#fac9eb'
};

controller.addWeatherLayer('convective', {
  paint: {
    fill: {
      color: [
        'match', ['downcase', ['get', 'details.risk.type']],
        'general', riskColors.general,
        'marginal', riskColors.marginal,
        'slight', riskColors.slight,
        'enhanced', riskColors.enhanced,
        'moderate', riskColors.moderate,
        'high', riskColors.high,
        '#000000'
      ],
      opacity: 0.7
    }
  },
  legend: {
    points: {
      values: [
        { color: riskColors.general, label: 'General' },
        { color: riskColors.marginal, label: 'Marginal' },
        { color: riskColors.slight, label: 'Slight' },
        { color: riskColors.enhanced, label: 'Enhanced' },
        { color: riskColors.moderate, label: 'Moderate' },
        { color: riskColors.high, label: 'High' }
      ]
    }
  }
});
```

For a continuous scale (e.g. a custom temperature colorscale), override `legend.bar` instead, using
the **same `colorscale` stops** as the paint override so the legend and the map stay in sync:
```javascript
const customTemperatureColorscale = {
  stops: [-40, '#1b1b3a', -20, '#2f4b7c', 0, '#00b4d8', 10, '#90e0ef', 20, '#ffd166', 30, '#f77f00', 40, '#d62828'],
  interval: 2
};

controller.addWeatherLayer('temperatures', {
  paint: { sample: { colorscale: customTemperatureColorscale } },
  legend: {
    bar: {
      colorscale: customTemperatureColorscale,
      measurement: { type: 'temperature', units: 'C' },
      labels: { every: 10 }
    }
  }
});
```

## Querying data at a point

```javascript
const results = controller.query({ lat: 40, lon: -74.5 });   // sync
const results = await controller.queryPromise({ lat: 40, lon: -74.5 });
// -> { [layerId]: sampled value(s) / feature(s) at that coordinate }
```

## Checklist for common tasks

- **"Add a weather layer"** → `controller.addWeatherLayer(code)` inside `on('load', ...)`; look up
  the code by fetching `https://www.xweather.com/docs/api/mapsgl/layers` (see
  `references/weather-layers.md`) if unsure.
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
- **"What layers/options are available?"** → fetch `https://www.xweather.com/docs/api/mapsgl/layers`
  for the full catalog, or `controller.weatherProvider.getLayerMetadata()` at runtime for
  account-specific availability. Never trust a static/hardcoded list.
- **"Handle load errors / show an error state"** → there is no `controller.on('error', ...)` —
  that event doesn't exist on `MapController` and will never fire. See the events note in
  `references/api-reference.md`.

## Reference files

- `references/api-reference.md` — full `Account`, `MapController`, and `DataSource` API (all methods, properties, events, per-provider setup)
- `references/weather-layers.md` — how to fetch and use the live weather-layer catalog endpoint
- `references/styles.md` — paint property spec for every render type, plus filters and masks
- `references/color-scales.md` — color scale config format and built-in named palettes
- `references/expressions.md` — style/filter expression operator reference
- `references/legends.md` — `points` (categorical) and `bar` (gradient) legend config reference
- `references/timeline.md` — animation/timeline API
