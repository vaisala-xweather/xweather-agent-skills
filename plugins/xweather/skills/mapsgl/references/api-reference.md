# MapsGL API Reference

Verified against `@xweather/mapsgl` SDK source (`packages/webgl-maps/src`).

## Account

```javascript
new mapsgl.Account(id: string, secret: string, serverOverrides?: { api?: string; maps?: string })
```

Auth is **always** client id + secret — there is no access-token constructor. `serverOverrides` is
only needed for enterprise/on-prem API endpoints.

```javascript
account.credentials();       // { id, secret }
account.canAccess(endpoint); // boolean
```

## Map Controller

One concrete class per map provider, all sharing the same base API:

- `mapsgl.MapboxMapController(map, opts)`
- `mapsgl.MaplibreMapController(map, opts)` (extends the Mapbox controller — same API)
- `mapsgl.GoogleMapController(map, opts)` (opts may also include `interleaved?: boolean`)
- `mapsgl.LeafletMapController(map, opts)`

```typescript
interface MapAdapterOptions {
  account: Account;
  units?: Partial<MapUnits>;
  animation?: Partial<TimeAnimationOptions & {
    pauseWhileLoading: boolean;
    resumeOnMoveEnd: boolean;
    preloadData: boolean;
  }>;
}
```

The controller isn't ready to accept layers until the underlying map has loaded — always gate
layer/source calls behind the `load` event (`controller.isReady` reflects the same state and is
checked internally; calling layer methods too early throws).

```javascript
controller.on('load', () => {
  controller.addWeatherLayer('temperatures');
});
```

### Weather layers

```typescript
hasWeatherLayer(id: string): boolean
getWeatherLayer(id: string): WebGLLayer | WebGLLayer[] | undefined
setWeatherLayerVisibility(id: string, visible: boolean): void
addWeatherLayer(id: string, overrides?: Partial<WeatherLayerOptions>, beforeId?: string): WebGLLayer | WebGLLayer[]
removeWeatherLayer(id: string): void
```

`addWeatherLayer` resolves deprecated/aliased codes automatically. Composite codes (see
`references/weather-layers.md`) return an array of `WebGLLayer`; `overrides.childLayers` can
target one sub-layer id inside a composite by id.

**Important:** `id` here is the weather layer *code* (e.g. `'temperatures'`) and every method in
this block correctly resolves that code internally, including composites. The generic layer
methods below (`getLayer`, `findLayer`, `setPaintProperty`, `moveLayer`, `removeLayer`) are
different — they take the actual underlying layer id, which is usually **not** the same string as
the weather layer code. See the "code vs. id" section in `references/weather-layers.md` before
using any of those four with a weather layer.

### Generic layers & sources

```typescript
hasSource(id: string): boolean
hasLayer(id: string): boolean
getSource(id: string): DataSource
getLayer(id: string): WebGLLayer          // real layer id required — NOT a weather layer code
findLayer(pattern: string): WebGLLayer    // real layer id/pattern required — NOT a weather layer code

addSource(id: string, config: Partial<SourceSpecification> | DataSource): DataSource
removeSource(id: string, dispose?: boolean): void   // dispose defaults true

addLayer(id: string, config: Partial<LayerSpecification> | WebGLLayer, beforeId?: string): WebGLLayer
removeLayer(id: string, dispose?: boolean): void    // dispose defaults true; real layer id required
moveLayer(id: string, beforeId?: string): void      // omit beforeId to move to top of stack; real layer id required

setPaintProperty(layerId: string, property: string, value: any): void   // real layer id required — NOT a weather layer code
```

For a weather layer, get the `WebGLLayer` via `addWeatherLayer`'s return value or
`getWeatherLayer(code)` and call `.setPaintProperty(...)` on the instance instead of routing
through `controller.setPaintProperty(code, ...)` — the latter silently no-ops if `code` isn't a
real layer id (which for weather layers, it usually isn't). Full explanation in
`references/weather-layers.md`.

`config` for `addLayer`/`addSource` may be a plain spec object (auto-instantiated by `type`) or an
already-constructed layer/source instance.

### Querying data

```typescript
query(coord: { lat: number; lon: number }): Record<string, any>
queryPromise(coord): Promise<Record<string, any>>
```

Returns an object keyed by layer id containing the sampled value(s)/feature(s) at that coordinate.

### Controls

Two optional on-map UI widgets: a **legend** (explains what active layers' colors/symbols mean —
full config in `references/legends.md`) and a **data inspector** (shows the raw value(s) under the
cursor/click for active layers, useful for debugging or building a "click for details" feature).

```typescript
addLegendControl(target: HTMLElement | string, options?: Partial<LegendControlOptions>): LegendControl
removeLegendControl(): void
addDataInspectorControl(options?: Partial<DataInspectorControlOptions>): DataInspectorControl
removeDataInspectorControl(): void
```

```typescript
interface LegendControlOptions {
  width: number;                 // default 400
  insets: number | number[];     // default 4
  system: 'metric' | 'us';       // default 'metric'
  units: MapUnits;
  toggleOnClick: boolean;        // default true
}

interface DataInspectorControlOptions {
  event: 'click' | 'move';       // default 'click'
  stream: boolean;               // default true
  showCoordinates: boolean;      // default true
  tooltip: any;                  // default {}
}
```

### Properties

```
account, map, timeline, weatherProvider
sources: DataSource[]      sourceIds: string[]
layers: WebGLLayer[]       layerIds: string[]     weatherLayerIds: string[]
isReady: boolean
controls: { legend, dataInspector }
```

### Map state & misc

```typescript
getSize() / setSize(size)
getCenter() -> {lat, lon} / setCenter({lat, lon})
getBounds() -> {north, west, east, south}
getZoom() / setZoom(zoom)
getBearing() / getPitch() / getFov()
getUnits() / setUnits(units) / setUnitsForSystem(system)
setRefreshInterval(minutes: number, advanceToNow?: boolean)  // advanceToNow defaults true
resize()
toggleFullscreen()
dispose(all?: boolean)  // all defaults true — tears down layers/sources/controls
```

### Events (`controller.on(event, handler)` / `controller.off(...)`)

`load`, `unload`, `resize`, `click`, `dblclick`, `mousedown`, `mouseup`, `mouseover`, `mouseout`,
`mousemove`, `zoom`, `zoom:start`, `zoom:end`, `move`, `move:start`, `move:end`,
`load:start`, `load:progress`, `load:complete`, `units:change`, `tilebounds:change`,
`layer:add`, `layer:show`, `layer:hide`, `layer:load:start`, `layer:load:progress`,
`layer:load:complete`, `layer:remove`, `source:add`, `source:remove`

**There is no generic `error` event on the controller.** Do not write `controller.on('error', ...)`
— it's a natural pattern to reach for (most JS event emitters have one), but MapsGL's
`MapController` doesn't emit one and the handler will simply never fire. The event names above are
exhaustive for the controller itself. For load-failure diagnostics on a specific layer or source,
the `WebGLLayer`/`DataSource` instances returned by `getLayer(id)`/`getSource(id)` are themselves
event emitters with their own more granular events (e.g. tile/metadata load failures) — inspect
those directly rather than expecting the controller to surface them. For most app code, checking
`controller.hasWeatherLayer(id)`/`hasLayer(id)` after adding a layer, or wrapping calls in
try/catch, is sufficient.

## Data Sources

Four source types, all constructed via `controller.addSource(id, spec)` by setting `spec.type`:

```typescript
// shared base fields on every source
interface SourceSpecification {
  type: 'raster' | 'vector' | 'geojson' | 'encoded';
  id: string;
  metadataUrl?: string;
  attribution?: string;
  authenticator?: AnyAuthenticator;
  timeSeries?: { validTimes?: (string|Date)[]; maxValidTimes?: number; operation?: TimeSeriesOperation };
  transformRequest?: (source, request) => request;
}
```

**Tile sources** (`raster`, `vector`, `encoded`) additionally support:
```typescript
interface TileSourceSpecification extends SourceSpecification {
  minZoom?: number;   // default 0
  maxZoom?: number;   // default 21
  bounds?: { north, south, east, west };
  url: string;         // template with {x} {y} {z} {s} — see below
  tileSize?: number | { width: number; height: number };  // default 256
  projection?: 'EPSG:3857' | 'EPSG:4326';                  // default EPSG:3857
}
```

```javascript
controller.addSource('alerts', {
  type: 'vector',
  url: 'https://maps{s}.aerisapi.com/{client_id}_{client_secret}/alerts/{z}/{x}/{y}/0.pbf',
  minZoom: 4,
  maxZoom: 8
});
```

**GeoJSON source** (extends vector tiling internally, but takes data directly):
```typescript
interface GeoJSONSourceSpecification extends SourceSpecification {
  data?: string | GeoJSON.FeatureCollection;
  url?: string;
  dynamic?: boolean;   // default false — poll/refetch periodically
  transformGeoJSON?: (source, data) => data;
}
```

```javascript
controller.addSource('earthquakes', {
  type: 'geojson',
  data: 'https://data.api.xweather.com/earthquakes/search?query=mag:1&limit=200&format=geojson&client_id=ID&client_secret=SECRET'
});

// update later
controller.getSource('earthquakes').setUrl('...');
controller.getSource('earthquakes').setData({ type: 'FeatureCollection', features: [...] });
```

**Encoded source** — raster tiles with data packed into RGBA channels (used internally by nearly
every weather `sample`/`grid`/`contour`/`particle` layer):
```typescript
interface EncodedSourceSpecification extends TileSourceSpecification {
  datasets: Array<Partial<EncodedRasterDataset>>;
  transformTileData?: (data: RGBAImage, datasets) => void;
}
```

You will rarely hand-build an encoded source — it's set up for you by `addWeatherLayer`. Build one
directly only for custom gridded datasets outside the built-in weather catalog.

Removing a source only detaches it — it does not remove layers still referencing it:
```javascript
controller.removeSource('alerts');
```
