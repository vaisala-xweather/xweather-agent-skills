# MapsGL Android SDK - API reference

Every signature below was read from the SDK source on the `feature/maptime-filter` branch. Where the
website documentation disagrees, follow this file.

The authoritative published reference is the SDK's KDoc, per version:

```
https://cdn.aerisapi.com/sdk/android/mapsgl/docs/v{version}/mapsglmaps/{package}/{-class-name}/index.html
```

There is **no `latest` alias** - `.../docs/latest/...` returns 404. Resolve the version first:

```bash
curl -s https://www.xweather.com/docs/api/releases/versions \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["products"]["mapsgl-android-sdk"]["version"])'
```

Class paths dash-case the Kotlin name: `MapController` becomes `-map-controller`, `LayerCode` becomes
`-layer-code`. Use the KDoc to confirm a symbol exists in a **released** build before writing code
against it - that is the reliable way to tell whether something is new, renamed, or branch-only.

Everything is under `com.xweather.mapsgl.*`. The published module is `mapsglmaps`.

## `XweatherAccount`

`com.xweather.mapsgl.config.weather.account.XweatherAccount`

```kotlin
val account = XweatherAccount(clientId, clientSecret)
```

Client id and secret from the Apps section of the Xweather account portal. **Mapbox tokens are
separate** and are configured through the Mapbox SDK, not through this type - MapsGL Android needs
both an Xweather account and Mapbox access/downloads tokens.

## `MapController`

`com.xweather.mapsgl.map.MapController` - the base controller. Everything below is inherited by
`MapboxMapController`, which is what you actually construct.

### Properties

```kotlin
val service: WeatherService            // built from the account
val timeline: Timeline                 // shared animation clock
val animationOptions: AnimationOptions // feeds the timeline
val dataInspector: DataInspectorControl
var legendControl: LegendControl?
val mapSessionId: Long
```

### Load events

`LiveData`, so observe them with a `LifecycleOwner`:

```kotlin
val onLoadStart: LiveData<Unit>
val onLoadComplete: LiveData<Unit>
val onLoadProgress: LiveData<MapLoadProgress>
```

```kotlin
controller.onLoadStart.observe(this) { binding.loadingBar.isVisible = true }
controller.onLoadComplete.observe(this) { binding.loadingBar.isVisible = false }
```

### Weather layers

```kotlin
fun addWeatherLayer(
    layerCode: LayerCode,
    id: String? = null,
    beforeId: String? = null,
    configure: ((WeatherConfiguration) -> Unit)? = null,
): TileLayer?

fun addWeatherLayer(
    config: WeatherConfiguration,
    id: String? = null,
    beforeId: String? = null,
    isCompoundLayer: Boolean = false,
): TileLayer?

fun removeWeatherLayer(code: LayerCode)
fun setWeatherLayerVisibility(code: LayerCode, visible: Boolean)
fun hasWeatherLayer(code: LayerCode): Boolean
fun getWeatherLayer(code: LayerCode): MapLayer<*, *>?
fun getConfigForCode(layerCode: LayerCode): WeatherConfiguration
```

`removeWeatherLayer` takes **only** the code - the website's extra-argument forms do not exist. The
`configure` lambda on the first overload is the least-typing way to tweak paint without building a
configuration by hand.

See `references/layers.md` for which codes exist.

### Custom sources and layers

```kotlin
fun addSource(descriptor: SourceDescriptor): DataSource
fun getSource(id: String): DataSource?
fun hasSource(id: String): Boolean
fun removeSource(id: String)

fun <P : LayerPaint> addLayer(descriptor: LayerDescriptor<P>, beforeID: String?): TileLayer?
fun getLayer(id: String): MapLayer<*, *>?
fun hasLayer(id: String): Boolean
fun moveLayer(id: String, beforeId: String?)
fun removeLayer(id: String, isCompounLayer: Boolean = false)
fun setLayerVisible(id: String, visible: Boolean = true)
fun setPaintProperty(layerId: String, property: String, value: Any)
```

Note the inconsistent casing: `addLayer` takes **`beforeID`**, while `addWeatherLayer` and `moveLayer`
take **`beforeId`**. `removeLayer`'s second parameter is spelled `isCompounLayer` in the SDK - a typo
that is part of the public API, so match it if you name the argument.

### Camera

```kotlin
fun getCenter(): Coordinate;    fun setCenter(center: Coordinate)
fun getZoom(): Double;          fun setZoom(zoom: Double)
fun getBounds(): LatLonBounds
fun getBearing(): Double
fun getPitch(): Double
fun getFov(): Double
fun getSize(): Size
```

### Controls and events

```kotlin
fun add(legendControl: LegendControl?)
fun removeLegendControl()
fun addLegend(forConfig: WeatherLayerConfiguration<*, *>)

fun addDataInspectorControl(mapView: MapView): DataInspectorControl
fun removeDataInspectorControl()

fun on(name: String, callback: (Any) -> Unit)
fun off(name: String, callback: (Any) -> Unit)
fun trigger(type: String, data: Any? = null)
```

### Lifecycle

`MapController` implements `DefaultLifecycleObserver` (`onCreate` / `onStart` / `onStop` /
`onDestroy`) and exposes `fun shutdown()`. Registering it against a `LifecycleOwner` is what keeps
GL resources tied to the host Activity. For the **cost** consequences of when layers are attached,
see `references/sessions.md`.

## `MapboxMapController`

`com.xweather.mapsgl.map.mapbox.MapboxMapController` - `MapController` over the Mapbox Maps SDK.

```kotlin
constructor(mapView: MapView, account: XweatherAccount)                 // use this one

@Deprecated(level = WARNING)
constructor(mapView: MapView, baseContext: Context,
            account: XweatherAccount, lifecycleOwner: LifecycleOwner)   // delegates to the above
```

```kotlin
val controller = MapboxMapController(mapView, account)
var mapboxMap: MapboxMap?     // non-null after construction, main thread only
```

Those are the **only two** constructors. The 4-argument form is deprecated and just delegates to the
2-argument one, so the extra `Context` and `LifecycleOwner` do nothing - but a lot of website
documentation still shows it, so expect to see it in code you're asked to fix.

**There is no `MapboxMapController(mapView, account, AnimationOptions(...))` overload.** Configure
animation through `controller.animationOptions` after construction instead.

Mapbox forbids reading `MapboxMap.cameraState` or coordinate bounds off the main thread, which is why
the controller caches a camera snapshot internally. Don't reach into `mapboxMap` from a render or IO
thread.

## `WeatherService`

`com.xweather.mapsgl.weather.WeatherService` - built for you as `controller.service`.

Its companion carries **182 configuration factories**, one per non-composite layer plus the
composites, each taking the service:

```kotlin
fun Temperatures(service: WeatherService): WeatherLayerConfiguration<EncodedSourceDescriptor, SampleLayerDescriptor>
fun Alerts(service: WeatherService): WeatherLayerConfiguration<VectorSourceDescriptor, FillLayerDescriptor>
fun Boundaries(service: WeatherService): CompositeWeatherLayerConfiguration
```

`references/layers.md` maps every `LayerCode` to its factory and descriptor types.

A parallel `WeatherConfigurations` class holds the same factories and is what
`LayerCode.getConfigurationForLayerCode` calls. Prefer `WeatherService` - it is the public surface the
demos use. The one thing only `WeatherConfigurations` has is `DataQueryText(service, code)`, shared by
the `*-text` data-query layers.

`WeatherService.PrecipitationRate` exists but is reachable from no `LayerCode`.

## Source descriptors

`com.xweather.mapsgl.sources.source.spec` - all implement `SourceDescriptor` (`id`, `kind`) and share
the same optional fields:

```kotlin
data class EncodedSourceDescriptor(
    override val id: String,
    var url: String? = null,
    var metadataUrl: String? = null,
    var minZoom: Float? = null,
    var maxZoom: Float? = null,
    var bounds: LatLonBounds? = null,
    var tileSize: TileSize? = null,
    var attribution: String? = null,
    var authenticator: XweatherAuthenticator? = null,
    var datasets: List<EncodedDataset>? = null,
) : SourceDescriptor
```

| Descriptor | For |
|---|---|
| `EncodedSourceDescriptor` | Xweather encoded raster grids - adds `datasets` |
| `VectorSourceDescriptor` | MVT vector tiles |
| `GeoJSONSourceDescriptor` | GeoJSON - adds `bundledAssetPath` for an in-app asset |
| `ImageSourceDescriptor` | Plain raster imagery |
| `XweatherEncodedSourceDescriptor` | Encoded, with the fields non-optional |

See `references/sources.md`.

## Layer descriptors and paint

`com.xweather.mapsgl.layers.spec` - `SampleLayerDescriptor`, `RasterLayerDescriptor`,
`ParticleLayerDescriptor`, `GridLayerDescriptor`, `ContourLayerDescriptor`, `FillLayerDescriptor`,
`LineLayerDescriptor`, `CircleLayerDescriptor`, `SymbolLayerDescriptor`, `HeatmapLayerDescriptor`,
`DataQueryLayerDescriptor`.

Each carries `var quality: DataQuality` (`exact`, `high`, `medium`, `normal`, `low`) and a paint
object. Paint types live in `com.xweather.mapsgl.layers.style`, all implementing `PaintStyle` with
`var opacity: Float`:

```kotlin
class SampleStyle(
    var expression: SampleExpression = SampleExpression.NUMBER,
    var channel: List<ColorBand> = listOf(ColorBand.red),
    var quality: DataQuality = DataQuality.normal,
    var interpolation: InterpolationMode = InterpolationMode.BICUBIC,
    var smoothing: Float = 0.0f,
    var offset: Float = 0.0f,
    var drawRange: ClosedRange<Double>? = null,
    var colorScale: ColorScaleOptions = ColorScaleOptions(),
    var opacity: Float = 1.0f,
    var multiband: Boolean = false,
    var meld: Boolean = true,
)
```

`ParticleStyle` adds `density`, `count`, `size`, `speedFactor`, `trails`, `trailsFadeFactor`,
`dropRate`, `dropRateBump`.

**Opacity is a plain `Float`, not a wrapped style value** - `paint.opacity = 0.7f`. See
`references/weather-styling.md` and `references/styles.md`.

## `Timeline`

`com.xweather.mapsgl.anim.Timeline`, built from `AnimationOptions` and reachable as
`controller.timeline`. Playback:

```kotlin
fun play(positionInput: Double? = null)
fun playFromDate(fromDate: Date)
fun pause();  fun resume();  fun stop();  fun restart();  fun reset();  fun toggle()
fun goTo(position: Double, useTotalDuration: Boolean)
fun goToDate(date: Date)
fun advance(progress: Double, useTotalDuration: Boolean)
fun advanceToStopPosition()
fun isAtEndPosition(): Boolean

var position: Double
var timeScale: Double        // default 1.0
var autoPlay: Boolean
var repeat: Boolean
```

Range control comes from its `TimeAnimation` base:

```kotlin
var start: Date              // defaults to 24 h ago
var end: Date                // defaults to now
var currentDate: Date
val deltaTime: Long
val containsPast: Boolean;  val containsFuture: Boolean
val isPast: Boolean;        val isFuture: Boolean

fun setStartDateUsingOffset(offset: Long, relativeTo: Date = Date())
fun setEndDateUsingOffset(offset: Long, relativeTo: Date = Date())
fun setStartDateUsingRelativeTime(offset: String, relativeTo: Date = Date())
fun setEndDateUsingRelativeTime(offset: String, relativeTo: Date = Date())
fun goToOffset(offset: Long)
fun clampDateRange(min: Date, max: Date)
```

```kotlin
controller.timeline.setStartDateUsingRelativeTime("-1 day")
controller.timeline.end = Date()
controller.timeline.play()
```

`val liveState: LiveData<AnimationState>` exposes playback state. See `references/timeline.md`.

## `AnimationOptions`

`com.xweather.mapsgl.anim.AnimationOptions`, as `controller.animationOptions`. The field that matters
most is `var shouldPreloadData: Boolean` - when true the SDK pre-fetches tiles across the timeline
range so playback starts ready rather than stalling. It is `false` by default.

## `LegendControl`

`com.xweather.mapsgl.controls.legend.LegendControl`

```kotlin
class LegendControl()

var mapView: MapView?
var units: MeasurementUnits = MeasurementUnits.IMPERIAL
var toggleUnitsOnTap: Boolean = true
var onUnitsToggled: ((MeasurementUnits) -> Unit)?
var usesDarkTheme: Boolean = false
var backgroundColor: Color = Color.Transparent
var maxLegendContentHeightDp: Int
var isHidden: Boolean = false
var legends: Map<String, Legend>

fun getView(): LegendContainerView
fun setDarkTheme(enabled: Boolean = true)
fun setHostTitleColor(color: Color)
fun applyUnits(units: MeasurementUnits)
fun toggleUnits()
fun add(legend: Legend)
fun replaceLegend(id: String, legend: Legend)
```

`backgroundColor` is a **Compose** `androidx.compose.ui.graphics.Color`, not an Android
`android.graphics.Color` int.

## `DataInspectorControl`

`com.xweather.mapsgl.controls.DataInspectorControl`, reachable as `controller.dataInspector` or from
`addDataInspectorControl(mapView)`.

```kotlin
class DataInspectorControl(mapController: MapController)

val view: ConstraintLayout?
var cancelCalloutWhenOffScreen: Boolean = true

fun show(point: ScreenCoordinate, coordinate: Point)
fun move(point: ScreenCoordinate)
fun update()
fun hide()
fun bringCalloutToFront()
fun setPresentation(layerId: String, presentation: Presentation)
fun removePresentation(layerId: String)
```

`setPresentation` is keyed by **style layer id**, not by `LayerCode` - get it from the returned
`TileLayer`, or via `getWeatherLayer(code)?.id`. See `references/legends-inspector.md`.

## Units

`MeasurementUnits` (`IMPERIAL` / `METRIC`) drives legend and inspector formatting.
`LegendControl.units` and `applyUnits` set it; `toggleUnits` flips it and fires `onUnitsToggled`.
