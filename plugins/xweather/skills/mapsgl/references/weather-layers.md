# Discovering Built-in Weather Layer Codes

Do not rely on a hardcoded layer list — the catalog changes as Xweather adds/retires layers.
Instead, fetch it live from the public docs endpoint:

```
https://www.xweather.com/docs/api/mapsgl/layers
```

This is a plain public JSON endpoint (no auth required). Fetch it with `WebFetch`/`curl` whenever
a task needs to look up a layer code, browse what's available in a category, verify a code exists,
or check whether a layer animates. Treat it as the source of truth over anything cached in this
skill or in prior conversation turns.

## Response shape

```json
{
  "layers": [
    {
      "id": "air-quality-co",
      "title": "Air Quality - CO",
      "description": "Measures the concentration of carbon monoxide (CO) in the air...",
      "type": "sample",
      "multiplier": 5,
      "imageUrl": "https://www.datocms-assets.com/.../mapsgl-layer-air-quality-co.jpg",
      "animatable": true,
      "categories": ["Air Quality"],
      "dataRange": "-15 to +4.5 days",
      "dataCoverage": ["Global"],
      "updateInterval": "3 hour"
    },
    ...
  ]
}
```

Field notes:
- **`id`** — the exact code to pass to `controller.addWeatherLayer(id)` / `getWeatherLayer` / `removeWeatherLayer` / `setWeatherLayerVisibility`.
- **`type`** — the render style (`raster`, `fill`, `line`, `circle`, `sample`, `grid`, `contour`, `particle`, `heatmap`, `symbol`, `text`, or `none`). `type: "none"` marks a **composite/alias** layer that expands into several sub-layers when added — `addWeatherLayer` returns an array of `WebGLLayer` for these (e.g. `boundaries`, `roads`, `fires`, `lightning-all`, `hail-threats`).
- **`categories`** — one or more of: `Popular`, `Radar + Satellite`, `Conditions`, `Forecasts`, `Severe`, `Lightning`, `Tropical`, `Maritime`, `Air Quality`, `Roads`, `Admin`, `Climate`, `Other`. A layer can appear in multiple categories (e.g. `Popular` overlaps others).
- **`animatable`** — whether the layer responds to `controller.timeline`.
- **`dataRange`** — how far back/forward in time data is available (e.g. `"-15 to +4.5 days"`, `"-7 days"`, `"+1 hour"`, or `"-"` for static data).
- **`dataCoverage`** — geographic coverage (e.g. `["Global"]`, `["US", "Canada"]`).
- **`updateInterval`** — how often the underlying data refreshes.
- **`multiplier`** — the layer's session-access-cost multiplier for billing purposes, not relevant to rendering.

There are ~280+ layers as of this writing, spanning admin/boundaries, radar & satellite,
current/forecast conditions, precipitation, severe weather, lightning, tropical cyclones,
maritime, air quality, road weather (per-region), and climate/hazard layers. Fetch the endpoint
rather than trusting that count.

## Recommended workflow

1. Fetch `https://www.xweather.com/docs/api/mapsgl/layers` once per task that needs layer discovery.
2. Filter the `layers` array client-side (e.g. by `categories` containing `"Roads"`, or `id`
   matching a search term) rather than re-fetching per query.
3. Use the matched `id` directly with `controller.addWeatherLayer(id)`.
4. If unsure whether a layer is composite, check `type === "none"` before assuming a single
   `WebGLLayer` is returned.

For account/plan-specific availability and any options metadata beyond what this endpoint exposes,
also consider `controller.weatherProvider.getLayerMetadata()` at runtime once the map is loaded —
it reflects exactly what the authenticated account can access.

## Critical: a weather layer's *code* is not its *layer id*

This is the single most common source of "my style update / opacity change silently does nothing"
bugs with built-in weather layers, and it's easy to hit because it's not obvious from the API shape.

The string you pass to `addWeatherLayer(code)` (e.g. `'temperatures'`) is a lookup key into
MapsGL's internal weather layer registry — it is **not** the id of the actual `WebGLLayer` that
ends up on the map. Internally, each weather layer definition specifies its own `id` (e.g. the
`'temperatures'` code currently resolves to a real layer id of `'conditions.temperature.fill'`,
verified against SDK source). These two strings have no reliable relationship to each other and
should never be assumed to match.

This matters because **not every controller method resolves the code for you**:

| Method | Takes the weather *code* directly? |
|---|---|
| `addWeatherLayer(code, ...)` | ✅ yes |
| `getWeatherLayer(code)` | ✅ yes |
| `hasWeatherLayer(code)` | ✅ yes |
| `removeWeatherLayer(code)` | ✅ yes |
| `setWeatherLayerVisibility(code, visible)` | ✅ yes |
| `getLayer(id)` | ❌ no — needs the real layer id |
| `findLayer(pattern)` | ❌ no — needs the real layer id |
| `setPaintProperty(id, prop, value)` | ❌ no — needs the real layer id |
| `moveLayer(id, beforeId)` | ❌ no — needs the real layer id |
| `removeLayer(id)` | ❌ no — needs the real layer id (use `removeWeatherLayer(code)` instead for weather layers) |

**`controller.setPaintProperty('temperatures', 'opacity', 0.5)` will silently do nothing** —
`setPaintProperty` calls `getLayer('temperatures')` internally, that lookup fails since
`'temperatures'` isn't a real layer id, and the whole call is a no-op (no error, no warning).

### The fix: always get the actual layer reference first

```javascript
// Option 1 — capture the return value when you add the layer (do this whenever you'll
// need to update the layer later, e.g. from a UI control)
const tempLayer = controller.addWeatherLayer('temperatures');
tempLayer.setPaintProperty('opacity', 0.5);

// Option 2 — look it up later by code if you don't have the original reference
const tempLayer = controller.getWeatherLayer('temperatures');
tempLayer.setPaintProperty('opacity', 0.5);

// Option 3 — if you specifically need controller.setPaintProperty (e.g. generic code that
// takes a layer id string), use the resolved layer's real `.id`, not the original code
const tempLayer = controller.getWeatherLayer('temperatures');
controller.setPaintProperty(tempLayer.id, 'opacity', 0.5);
```

Calling `.setPaintProperty()` directly on the layer instance (Options 1/2) is simplest and always
correct — prefer it over going back through `controller.setPaintProperty(code, ...)`.

### Composite codes return an array — iterate it

Codes marked composite in the catalog (`type: "none"`, e.g. `boundaries`, `roads`, `fires`,
`lightning-all`, `hail-threats`) resolve to **multiple** underlying layers.
`addWeatherLayer`/`getWeatherLayer` return an **array of `WebGLLayer`** for these, not a single
layer — you must iterate to update every sub-layer:

```javascript
const fireLayers = controller.addWeatherLayer('fires');

if (Array.isArray(fireLayers)) {
  fireLayers.forEach((layer) => layer.setPaintProperty('opacity', 0.6));
} else {
  fireLayers.setPaintProperty('opacity', 0.6);
}
```

Since you can't always know in advance whether a given code is composite (without checking the
catalog's `type` field first), defensively handle both shapes whenever you store/update a layer
reference returned by `addWeatherLayer`/`getWeatherLayer`.

`setWeatherLayerVisibility(code, visible)`, `removeWeatherLayer(code)`, and `hasWeatherLayer(code)`
all already handle composite codes internally (they recurse over every sub-layer for you) — this
gotcha only applies when you're working with the raw `WebGLLayer` instance(s) directly, e.g. to
change paint properties, opacity, or call `.show()`/`.hide()`/`.refresh()` individually.
