# MapsGL Apple SDK — API reference

The authoritative reference is the SDK's published DocC, per version:

```
https://cdn.aerisapi.com/sdk/ios/mapsgl/docs/v{version}/documentation/mapsglmaps
```

There is **no `latest` alias** — `.../docs/latest/...` returns 404. Resolve the version first:

```bash
curl -s https://www.xweather.com/docs/api/releases/versions \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["products"]["mapsgl-apple-sdk"]["version"])'
```

Only the `mapsglmaps` module is published. `MapsGLCore`, `MapsGLRenderer`, `MapsGLMapbox`, and
`MapsGLMapLibre` have no hosted DocC — read the adapter sources in the GitHub repo for those.

A machine-readable symbol index sits at
`https://cdn.aerisapi.com/sdk/ios/mapsgl/docs/v{version}/index/index.json`, and per-symbol JSON at
`.../data/documentation/mapsglmaps/<lowercased-symbol-path>.json`. Use the index to confirm a symbol
exists in a specific release before writing code against it — that is the reliable way to check
whether an API is new, renamed, or gone.

The version list page is https://www.xweather.com/docs/mapsgl-apple-sdk/api-reference.

Everything below reflects the SDK's public surface and is stable across recent releases; where the
Apple SDK diverges from the web documentation, this file follows the SDK.

---

## `XweatherAccount`

```swift
XweatherAccount(id: String, secret: String)
```

Properties: `id`, `secret`. Nothing else — it's a credential holder.

## `MapController`

Generic over the underlying map type: `MapController<MapType>`. The concrete controllers are
`MapboxMapController: MapController<MapboxMaps.MapboxMap>` and
`MapLibreMapController: MapController<MapLibre.MLNMapView>`.

### Initializers

```swift
// Base
MapController(map: MapType, window: UIWindow? = nil, account: XweatherAccount)

// Mapbox — convenience taking a MapView, reads `mapboxMap` and `window` from it
MapboxMapController(map: MapboxMaps.MapView, account: XweatherAccount)
MapboxMapController(map: MapboxMaps.MapboxMap, window: UIWindow? = nil, account: XweatherAccount)

// MapLibre — convenience taking the view, reads `window` from it
MapLibreMapController(map: MLNMapView, account: XweatherAccount)
MapLibreMapController(map: MLNMapView, window: UIWindow?, account: XweatherAccount)
```

In SwiftUI with Mapbox, `MapReader`'s proxy exposes a `MapboxMap`, not a `MapView`, so use the
`window:`-taking form with `UIWindow?.none`.

**Retain the controller.** It owns the layer/source registry, the timeline, and the event
subscriptions. A controller created in a `View.body` or a local goes away and the map stops updating.

### Properties

| Property | Type | Notes |
|---|---|---|
| `account` | `XweatherAccount` | |
| `map` | `MapType` | The underlying provider map |
| `window` | `UIWindow?` | |
| `service` | `WeatherService` | Pass to every `WeatherService.<Name>(service:)` config |
| `timeline` | `Timeline` | See `timeline.md` |
| `animationOptions` | `MapController.AnimationOptions` | `shouldPreloadData`, `shouldPauseWhileLoading`, `shouldResumeAfterLoading` |
| `layers` / `layerIds` | `[any MapsGLLayer]` / `[String]` | All layers, weather and custom |
| `sources` / `sourceIds` | `[any DataSource]` / `[String]` | |
| `weatherLayerIds` | `[String]` | Generated ids of active weather layers |
| `legendControl` | `LegendControl?` | |
| `dataInspector` | `DataInspectorControl?` | |

Masks are read back per kind rather than as a dictionary, and set on the layer descriptor:

```swift
func getMaskLayer(_ type: MaskLayerKind) -> AnyMapsGLLayer?
func beforeIdForMaskLayers() -> String?
```

```swift
config.layer.maskConfiguration = .water    // .none / .land / .water
```

See `styles.md` for custom mask configurations.

### Events

**Use the `on<Event>` `Signal` properties.** They are the current API; the `subscribe(to:)` family
below is deprecated.

```swift
controller.onLoad.observe { _ in … }.store(in: &cancellables)
```

| Signal | Payload | Fires |
|---|---|---|
| `onLoad` | `Void` | Map and MapsGL are ready — gate all layer/source calls on this |
| `onLoadStart` | `Void` | A data load began (good for a spinner) |
| `onLoadProgress` | `Queue.Progress` | Load progress |
| `onLoadComplete` | `Void` | All in-flight loads finished |
| `onLayerAdded` / `onLayerRemoved` | `String` (layer id) | |
| `onSourceAdded` / `onSourceRemoved` | `String` (source id) | |
| `onMove` / `onMoveEnd` | `Void` | Camera movement |
| `onMapTap` | `(CGPoint, CLLocationCoordinate2D)` | |

There is also an event-type form via `Eventable`, but **three of its four methods are deprecated in
1.6.1** — "Use available on<event>.observe() methods instead":

```swift
controller.subscribe(to: MapEvents.Load.self) { _ in … }        // ⚠️ deprecated
controller.asyncSubscribe(to: MapEvents.Load.self) { _ in … }   // ⚠️ deprecated
controller.subscribeToNext(MapEvents.Load.self) { _ in … }      // ⚠️ deprecated
controller.publisher(for: MapEvents.Load.self)                  // not deprecated — a Combine Publisher
```

Don't write the deprecated three, and rewrite them when editing existing code. This matters because
the **web documentation's SwiftUI getting-started sample still uses
`subscribe(to: MapEvents.Load.self)`** — copying it produces a deprecation warning on a brand-new
project. The `onLoad.observe { … }` form is the direct replacement.

`publisher(for:)` remains useful when you want Combine operators (`receive(on:)`, `debounce`) rather
than a bare callback. Event types: `MapEvents.Load`, `.Unload`, `.Move`, `.MoveStart`, `.MoveEnd`,
`.Pan`, `.PanStart`, `.PanEnd`, `.Zoom`, `.ZoomStart`, `.ZoomEnd`, `.Resize`, `.TileBoundsChange`; and
`MapControllerEvents.LayerAdd`, `.LayerRemove`, `.SourceAdd`, `.SourceRemove`, `.LoadStart`,
`.LoadComplete`.

**Every observation returns an `AnyCancellable` you must retain.** Not storing it silently
unsubscribes, which reads as "the SDK never fired the event".

There is no error event on `MapController`. Failures surface as thrown errors from the `add…` methods
(`MapController.Error`: `.alreadyExists`, `.invalidSource`, `.invalidMetadata`,
`.float16NotSupportedOnPlatform`, and the `make…` variants).

### The layer and source API is `@MainActor`

`addWeatherLayer`, `removeWeatherLayer`, `setWeatherLayerVisibility`, `weatherLayer(for:)`,
`addSource`, `addLayer`, `getLayer`, `removeLayer`, `removeSource`, `addImage`, and
`add(legendControl:)` are all annotated `@MainActor`. Calling them from a background context is a
compile error under strict concurrency and a hop under Swift 5 mode — so keep controller work on the
main actor, and wrap any call made from a detached task or a non-isolated callback:

```swift
await MainActor.run { _ = try? controller.addWeatherLayer(for: .radar) }
```

The `onLoad` observer already runs on the main thread, so the common path needs nothing special.
`query(coord:layerIds:)` and `moveLayer` are *not* main-actor-isolated.

### Weather layers

```swift
@discardableResult @MainActor
func addWeatherLayer(for code: WeatherService.LayerCode,
                     id: String? = nil,
                     beforeId: String? = nil) throws -> (any MapsGLLayer)?

@discardableResult @MainActor
func addWeatherLayer(config: any WeatherLayerConfiguration,
                     id: String? = nil,
                     beforeId: String? = nil) throws -> (any MapsGLLayer)?

@MainActor func weatherLayer(for code: WeatherService.LayerCode) -> (any MapsGLLayer)?
@MainActor func hasWeatherLayer(for code: WeatherService.LayerCode) -> Bool
@MainActor func setWeatherLayerVisibility(for code: WeatherService.LayerCode, visible: Bool)
@MainActor func removeWeatherLayer(for code: WeatherService.LayerCode)
```

Both `addWeatherLayer` overloads are `@discardableResult`, so `try controller.addWeatherLayer(for:)`
on its own line is fine. `addSource` and `addLayer` are **not**, so those need `_ =` or a binding.

**Only the `add` forms throw.** `setWeatherLayerVisibility` and `removeWeatherLayer` do not — `try`
on them won't compile, despite what some doc pages show.

`for:` / `forCode:` labels both exist as overloads; `for:` is the documented spelling.

A weather layer's **code is not its layer id**: the SDK generates an id that accounts for
customization, so `getLayer(id:)` will not find a weather layer by code. Read `.id` off the layer
returned by `weatherLayer(for:)` when you need the real id.

### Custom sources and layers

```swift
@MainActor func addSource(_ descriptor: any SourceDescriptor) throws -> (any DataSource)?
@MainActor func getSource(id: String) -> (any DataSource)?
func hasSource(id: String) -> Bool
@MainActor func removeSource(id: String)

@MainActor func addLayer(_ descriptor: some LayerDescriptor,
                         beforeId: String? = nil) throws -> (any MapsGLLayer)?
@MainActor func getLayer(id: String) -> (any MapsGLLayer)?
func hasLayer(id: String) -> Bool
func moveLayer(id: String, beforeId: String?) throws
@MainActor func removeLayer(id: String)
```

Neither `addSource` nor `addLayer` is `@discardableResult` — discarding the result warns, so write
`_ = try controller.addLayer(layer)` or bind it.

Order matters: add the source before any layer that references it by id. Remove layers before the
source they use.

### Images, coordinates, querying

```swift
@MainActor func addImage(id: String, image: UIImage, sdf: Bool = false) throws

func point(for coordinate: CLLocationCoordinate2D) -> CGPoint
func coordinate(for point: CGPoint) -> CLLocationCoordinate2D

func query(coord: CLLocationCoordinate2D,
           layerIds: [String]?) async -> [String: FeatureQueryResult]
```

`query` is `async`, keyed by layer id, and `layerIds` has **no default** — pass `nil` explicitly to
query every queryable layer: `await controller.query(coord: coordinate, layerIds: nil)`. `FeatureQueryResult` has `layerId` and
`features: [QueriedFeature]`; a `QueriedFeature` has `id`, `source`, `sourceLayer`, and
`properties: [String: Any]`.

Property conventions for encoded weather layers:

- the reading is on `"value"`, as a `Float`, in **metric** units;
- vector-valued layers (winds, ocean currents, swell, waves) also carry `"angle"`, and that angle is
  the direction the data moves **toward** — meteorological wind direction is `angle - 180`.

Register a custom image before adding a layer that names it, then reference it by id from an
`icon.image`:

```swift
try controller.addImage(id: "my-grid-icon", image: UIImage(named: "my-grid-icon")!)

var config = WeatherService.WindBarbs(service: controller.service)
config.layer.paint.icon.image = .constant("my-grid-icon")
config.layer.paint.icon.size = .constant(24)
config.layer.paint.grid.spacing = 40
try controller.addWeatherLayer(config: config)
```

**Don't try to build a `GridLayerDescriptor` yourself.** The web documentation's custom-image example
constructs one directly:

```swift
let layer = GridLayerDescriptor(id: "custom-grid", source: source.id, paint: .init(…))   // ⚠️ won't compile
```

That does not compile in 1.6.1 — `GridLayerDescriptor` "cannot be constructed because it has no
accessible initializers", and neither can `SamplePaint`. Only the **vector** descriptors expose a
public memberwise `init(id:source:paint:)`; see the descriptor tables below. To get a custom
symbol grid, start from a built-in grid weather layer's configuration and mutate its `layer`, as
above.

### Controls

```swift
@MainActor func add(legendControl: LegendControl)
func removeLegendControl()

@discardableResult func addDataInspectorControl(constrainedTo host: UIView) -> DataInspectorControl
func removeDataInspectorControl()
```

## `WeatherService`

Reachable as `controller.service`; also constructible as `WeatherService(account:)`.

| Member | Notes |
|---|---|
| `account` | `XweatherAccount` |
| `style` | `MapStyle` — sprite/image registration |
| `isStyleLoaded` | `Bool` |
| `maxSourceValidTimes` | `Int` — how many time steps a source keeps |
| `layerConfiguration(for:)` | `(any WeatherConfiguration)?` for a `LayerCode` |
| `loadLayerMetadata(completion:)` | `Result<[WeatherLayerMetadata], Error>` — account-visible layers |

`WeatherLayerMetadata`: `id`, `title`, `description`, `type`, `categories`, `animatable`, `dataRange`,
`dataCoverage`, `updateInterval`, `imageUrl`, `unit`, `valueRange`.

Nested types: `WeatherService.LayerCode`, `WeatherService.LegendCode`,
`WeatherService.PresentationFormat`, and one configuration struct per layer.

### Weather layer configuration structs

Named after the layer code — `.temperatures` → `WeatherService.Temperatures`. Every one has:

```swift
init(service: WeatherService)

let code: WeatherService.LayerCode
var layer: <SomeLayerDescriptor>          // paint, quality, masks, filter
var legend: (any Legend)?
var presentation: DataInspectorPresentation?
```

Composite layers are the exception: they expose `let layers: [any WeatherLayerConfiguration]` and no
single `layer`, so their paint cannot be overridden through the struct. Full list in `layers.md`.

```swift
var config = WeatherService.Temperatures(service: controller.service)
config.layer.paint.opacity = 0.5     // not paint.sample.opacity — see styles.md
config.layer.quality = .low
try controller.addWeatherLayer(config: config)
```

## Source descriptors

All conform to `SourceDescriptor`, all initialize as `init(id: String)`, and all share:

| Property | Type |
|---|---|
| `id` | `String` |
| `url` | `URL?` |
| `metadataURL` | `URL?` |
| `zoomRange` | `(any InclusiveBoundedRange<Int>)?` — e.g. `4...8` |
| `bounds` | `MapBounds<LatitudeLongitude>?` |
| `tileSize` | `TileSize?` |
| `attribution` | `String?` |
| `authenticator` | `(any Authenticator)?` |
| `transformer` | `(any SourceTransformer)?` |
| `kind` | `DataSourceKind` |

| Descriptor | Adds | For |
|---|---|---|
| `ImageSourceDescriptor` | `useTimeSeries` | Raster tile imagery |
| `VectorSourceDescriptor` | `useTimeSeries` | Mapbox Vector Tiles |
| `EncodedSourceDescriptor` | `datasets: [any EncodedDataset]?` | RGBA-packed weather grids |
| `GeoJSONSourceDescriptor` | `data: GeoJSONSourceData`, `useTimeSeries` | GeoJSON, remote or inline |

```swift
var alerts = VectorSourceDescriptor(id: "alerts")
alerts.url = URL(string: "https://maps{s}.aerisapi.com/[CLIENT_ID]_[CLIENT_SECRET]/alerts/{z}/{x}/{y}/0.pbf")
alerts.zoomRange = 4...8
_ = try controller.addSource(alerts)

var quakes = GeoJSONSourceDescriptor(id: "earthquakes")
quakes.url = URL(string: "https://data.api.xweather.com/earthquakes/search?query=mag:1&limit=200&format=geojson&client_id=[CLIENT_ID]&client_secret=[CLIENT_SECRET]")
_ = try controller.addSource(quakes)

// or inline
quakes.data = .string(geoJSONString)
```

Updating a live source — downcast to the concrete type:

```swift
if let source = controller.getSource(id: "alerts") as? VectorTileSource {
    source.setTileURL(URL(string: "…/alerts/{z}/{x}/{y}/202205061110.pbf"))
}

if let source = controller.getSource(id: "earthquakes") as? MapsGLMaps.GeoJSONSource {
    source.setURL(newURL)
    source.setData(.string(newGeoJSON))
}
```

## Layer descriptors

All conform to `LayerDescriptor` and share `id`, `source` (a source id string), `paint`, `quality`,
`timing`, `maskConfiguration`, and `type: LayerKind`.

**Vector descriptors** additionally have `sourceLayer: String?` and `filter: Expression?`, and take a
memberwise `init(id:source:paint:)`:

| Descriptor | Paint type | `LayerKind` |
|---|---|---|
| `FillLayerDescriptor` | `FillLayerPaint` | `.fill` |
| `LineLayerDescriptor` | `LineLayerPaint` | `.line` |
| `CircleLayerDescriptor` | `CircleLayerPaint` | `.circle` |
| `SymbolLayerDescriptor` | `SymbolLayerPaint` | `.symbol` |
| `HeatmapLayerDescriptor` | `HeatmapLayerPaint` | `.heatmap` |

**Encoded/raster descriptors** have no `filter` or `sourceLayer`:

| Descriptor | Paint type | `LayerKind` |
|---|---|---|
| `RasterLayerDescriptor` | `RasterLayerPaint` | `.raster` |
| `SampleLayerDescriptor` | `SampleFillLayerPaint` | `.sample` |
| `ParticleLayerDescriptor` | `ParticleLayerPaint` | `.particles` |
| `GridLayerDescriptor` | `GridLayerPaint` | `.grid` |
| `ContourLayerDescriptor` | `ContourLayerPaint` | `.contour` |

Paint property tables are in `styles.md`.

## `Timeline`

`controller.timeline`, never constructed by hand. Inherits `TimeAnimation`, which inherits `Animation`,
so its usable surface is larger than the `Timeline` DocC page alone shows. See `timeline.md`.

## `LegendControl`

```swift
let control = LegendControl()
controller.add(legendControl: control)
```

Properties: `view: UIView`, `backgroundColor`, `cornerRadius`, `insets`, `isHidden`, `units`,
`toggleUnitsOnTap`.
Methods: `add(legend:)`, `getLegend(id:)`, `update(legend:)`, `removeLegend(id:force:)`,
`updateLegendViews()`.

`LegendControl`'s mutating methods are **`@MainActor`** — `update(legend:)` and
`removeLegend(id:force:)` included. It renders UIKit views, so this is expected, but a helper that
builds and commits a legend needs the annotation or it won't compile:

```swift
@MainActor
func applyDarkMode(_ control: LegendControl, _ legend: some Legend) {
    control.backgroundColor = .black
    control.update(legend: legend.titleColor(.white))
}
```

SwiftUI: `LegendControlView(mapControllerProvider: { controller })` — reuses an already-added control
if there is one. See `legends.md`.

## `DataInspectorControl`

```swift
let inspector = controller.addDataInspectorControl(constrainedTo: mapView)
inspector.setPresentation(for: layerId, presentation: DataInspectorPresentation(title:format:))
inspector.removePresentation(for: layerId)
inspector.hide()
```

Also `defaultValueFormatter: ([QueriedFeature]) -> String?`, `show(at:coordinate:)`, `move(to:)`,
`update()`.

SwiftUI: `.dataInspectorOverlay(mapControllerProvider: { controller })` on the map view.

Presentations are keyed by **layer id**, so resolve a weather layer first:

```swift
if let temps = controller.weatherLayer(for: .temperatures) {
    inspector.setPresentation(for: temps.id, presentation: presentation)
}
```

Or set it on the configuration before adding the layer, which avoids the id lookup:

```swift
var config = WeatherService.Temperatures(service: controller.service)
config.presentation = .init(title: "Temperature (°F)", format: { features in
    guard let value = features.first?.properties["value"] as? Float else { return nil }
    let celsius = Measurement(value: Double(value), unit: UnitTemperature.celsius)
    return String(format: "%.1f", celsius.converted(to: .fahrenheit).value)
})
try controller.addWeatherLayer(config: config)
```

## `MeasurementUnits`

`.metric` and `.imperial` presets, plus per-dimension units: `temperature`, `temperatureDelta`,
`speed`, `rate`, `distance`, `height`, `precipitation`, `snowfall`, `pressure`, `direction`,
`concentration`, `intensity`, `ratio`, `time`. Used by legends (`LegendControl.units`) for display.

Underlying data is always metric; these affect presentation only.
