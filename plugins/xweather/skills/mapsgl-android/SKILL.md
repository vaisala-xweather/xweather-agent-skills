---
name: mapsgl-android
description: >-
  This skill should be used when working with the Xweather MapsGL Android SDK
  (mapsgl-android-sdk / com.xweather.mapsgl) - setting up MapboxMapController,
  adding or removing weather layers via LayerCode or WeatherService configs,
  styling with StyleValue and Expression, custom sources and layers, legends,
  data inspector presentations, timeline animation, layer masks, or integrating
  the AAR/JitPack dependency into an Android app. Use it whenever a task mentions
  MapsGL Android, MapboxMapController, addWeatherLayer, LayerCode,
  WeatherService, XweatherAccount, or weather overlays on Mapbox Maps SDK for
  Android. Also covers MapsGL session-based usage/cost (shared with the JS SDK)
  and common Android gotchas (Mercator, OpenGL ES 3.0, minSdk 28, Mapbox peer
  dependency). Tracks the SDK's feature/maptime-filter branch, ahead of the
  current release, so some documented APIs are unreleased and flagged. When docs
  and SDK disagree, prefer the SDK (source / KDoc / demos) over xweather.com
  documentation.
license: MIT
metadata:
  author: Vaisala Xweather
  version: "0.12.1"
  platform: android
  sdk: mapsgl-android-sdk
---

# MapsGL Android

MapsGL Android renders weather and custom map data on top of the **Mapbox Maps
SDK for Android** (encoded grids via OpenGL ES custom layers; many vector
weather layers via Mapbox style layers). Requires an Xweather account (Weather
API + Maps) **and** Mapbox access / downloads tokens.

## Source of truth (read this first)

When answering or writing code, resolve conflicts in this order:

1. **The MapsGL Android SDK** - public Kotlin APIs in `mapsglmaps` / published AAR,
   in-repo demos under `app/`, and generated KDoc
2. **This skill** (kept to match the SDK)
3. **https://www.xweather.com/docs/mapsgl-android-sdk/** - useful for tutorials and
   recipes, but often lagging (deprecated ctors, wrong `removeWeatherLayer` args,
   missing Mapbox peer dep, "coming soon" for shipped features, invented overload
   shapes)

**Prefer the SDK to the docs.** If a docs snippet disagrees with a real method
signature, package, or demo in the SDK, follow the SDK and say so. Never invent an
API - if it isn't in the SDK source, KDoc or a demo, it doesn't exist.

Docs hub (optional context only):
https://www.xweather.com/docs/mapsgl-android-sdk/

**API scope:** public MapsGL Android APIs only - no internals.

**This skill tracks the `feature/maptime-filter` branch**, which is ahead of the
released SDK. Anything documented here that is not in the current release is
marked *(unreleased)* where it appears - `references/layers.md` flags 28 layer
codes that way. Unmarked APIs are in the released build. When writing code for a
project that depends on a published JitPack artifact rather than the branch, stay
on the unmarked surface, and say so if the user asks for something that is only
on the branch.

**Never hardcode a version number.** Resolve the current release when you need
one:

```bash
curl -s https://www.xweather.com/docs/api/releases/versions \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["products"]["mapsgl-android-sdk"]["version"])'
```

That endpoint is the release source of truth for every Xweather product, keyed by
product id - `mapsgl-android-sdk` here, alongside `mapsgl`, `mapsgl-apple-sdk`,
`weather-api`, `maps`, and others. It's a small public JSON document, no auth
needed.

A version is only needed for a deliberate Gradle pin or an API-reference URL.
Where this skill's `references/` note behaviour "on 1.6.x", that records what the
guidance was checked against - verify against the release you're actually on
before relying on it.

## How to write examples

**Default:** one Kotlin `Activity` / Fragment with ViewBinding + Mapbox `MapView`.
No Compose unless asked. Match the surrounding project when it disagrees with that
default - if it is a Fragment codebase, or already uses Compose interop, follow it.

## API reference

`references/api-reference.md` carries real signatures for every public type. The
published KDoc is the per-version authority:

```
https://cdn.aerisapi.com/sdk/android/mapsgl/docs/v{version}/mapsglmaps/{package}/{-class-name}/index.html
```

There is **no `latest` alias** - `/docs/latest/` returns 404. Resolve the version
first (above). Class paths dash-case the name: `MapController` becomes
`-map-controller`.

## How much of this has been proven

Not all of it to the same standard, and the difference matters when something here
disagrees with what you observe.

**Built and run.** The Setup section and the Complete example below were applied to
a blank Android project, compiled, and run against MapsGL Android 1.6.1. That
covers `XweatherAccount`, `MapboxMapController`, `setCenter`/`setZoom`,
`onLoadStart`/`onLoadComplete`, `subscribeMapLoaded`, the Mercator `setProjection`,
`LegendControl`, `addDataInspectorControl`, `animationOptions.shouldPreloadData`,
`timeline.setStartDateUsingRelativeTime`/`end`/`play`/`pause`,
`addWeatherLayer`/`removeWeatherLayer`, `LayerCode.RADAR`, and the five
`com.xweather.mapsgl.*` import paths those need. The build also confirmed that a
consuming app's merged manifest picks up `largeHeap="true"` and the GLES 3.0
`uses-feature` from the SDK.

**Generated from the SDK.** `references/layers.md` is produced mechanically from
the `LayerCode` enum and the `WeatherService` factories, and re-checked against the
released KDoc.

**Read from the SDK source, not compiled.** Everything else - the rest of
`references/api-reference.md`, the styling, expression, legend, source and custom
layer material. The signatures were read out of the SDK rather than written from
memory, but no build has exercised them.

If a snippet from the third group does not compile, trust the SDK and say so.

## Core concepts

| Concept | What it is |
|---|---|
| `XweatherAccount` | Client id/secret |
| `MapboxMapController` | Mapbox adapter (`MapController` APIs) |
| `WeatherService` / `LayerCode` | Built-in weather configs / codes |
| Source / layer descriptors | Custom data + renderers |
| `StyleValue` / `Expression` | Paint + data-driven style |
| `LegendControl` / `DataInspectorControl` | On-map UI |
| `timeline` / `animationOptions` | Shared animation clock |

## Setup

### 1. Credentials - both sets are required

| | Where | Used for |
|---|---|---|
| Xweather client id + secret | https://data.portal.xweather.com/account/keys | `XweatherAccount(id, secret)` |
| Mapbox access token | `mapbox_access_token` string resource | Map rendering at runtime |
| Mapbox downloads token | `MAPBOX_DOWNLOADS_TOKEN` in `gradle.properties` | Resolving the Mapbox SDK at build time |

If nothing renders or auth fails, check **both** credential sets before digging
into MapsGL. A missing Mapbox token looks like a MapsGL failure but isn't.

### 2. Install

**Mapbox is a peer dependency** - MapsGL does not bring it transitively, and the
official getting-started page shows only JitPack. Add both repositories and both
dependencies:

```gradle
// settings.gradle
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven {
            url = uri("https://jitpack.io")
            // Prefer POM + artifact over JitPack's rewritten *.module, which breaks IDE KDoc
            metadataSources { mavenPom(); artifact() }
        }
        maven {
            url = uri("https://api.mapbox.com/downloads/v2/releases/maven")
            authentication { basic(BasicAuthentication) }
            credentials { username = "mapbox"; password = MAPBOX_DOWNLOADS_TOKEN }
        }
        // Required: the SDK has a transitive `api` dependency on
        // no.ecc.vectortile:java-vector-tile, which is published only here.
        maven { url = uri("https://maven.ecc.no/releases") }
    }
}
```

**All four repositories are required.** Omitting `maven.ecc.no` fails at dependency
resolution with `Could not find no.ecc.vectortile:java-vector-tile`, which reads
like a broken SDK release rather than a missing repository.

```gradle
// app/build.gradle - resolve vX.Y.Z from the releases endpoint, don't copy a literal
android {
    compileSdk 36
    defaultConfig { minSdk 28 }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = '17' }
    buildFeatures { viewBinding true }   // the examples below use ViewBinding
}

dependencies {
    implementation "com.github.vaisala-xweather:mapsgl-android-sdk:vX.Y.Z"
    implementation "com.mapbox.maps:android-ndk27:11.15.3"
}
```

Do **not** also add a `...:mapsglmaps` artifact - that duplicates the SDK.

### 3. Create the controller, then wait for the map to load

Two things have to be true before adding weather layers: the `MapView` must be
attached, and the Mapbox map must have loaded. Adding layers earlier silently
does nothing.

```kotlin
val controller = MapboxMapController(mapView, account)
mapView.mapboxMap.subscribeMapLoaded {
    // safe to add weather layers here
}
```

Use `MapboxMapController(mapView, account)`. The 4-argument constructor taking a
`Context` and `LifecycleOwner` is **deprecated** and merely delegates to this one,
despite still appearing throughout the website documentation.

Full install detail, credential wiring and the string resources:
`references/setup.md`.

## Complete example

A single Activity that renders an animated radar layer with a legend, tears down
on `onStop` so it stops consuming sessions, and carries the required attribution.
**This example has been built and run** - see "How much of this has been proven"
above.

```xml
<!-- res/layout/activity_weather_map.xml -->
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <com.mapbox.maps.MapView
        android:id="@+id/mapView"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <ProgressBar
        android:id="@+id/progress"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:visibility="gone"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <TextView
        android:id="@+id/attribution"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:padding="8dp"
        android:text="Powered by Vaisala Xweather"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

```kotlin
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.ViewTreeObserver
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.isVisible
import com.example.yourapp.databinding.ActivityWeatherMapBinding   // generated by ViewBinding
import com.mapbox.maps.extension.style.layers.properties.generated.ProjectionName
import com.mapbox.maps.extension.style.projection.generated.projection
import com.mapbox.maps.extension.style.projection.generated.setProjection
import com.xweather.mapsgl.config.weather.account.XweatherAccount
import com.xweather.mapsgl.controls.legend.LegendControl
import com.xweather.mapsgl.types.Coordinate
import com.xweather.mapsgl.map.mapbox.MapboxMapController
import com.xweather.mapsgl.weather.LayerCode
import java.util.Date

class WeatherMapActivity : AppCompatActivity() {

    private lateinit var binding: ActivityWeatherMapBinding
    private var controller: MapboxMapController? = null
    private val activeCodes = listOf(LayerCode.RADAR)
    private var weatherAttached = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityWeatherMapBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.attribution.setOnClickListener {
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://www.xweather.com/")))
        }

        val account = XweatherAccount(
            getString(R.string.xweather_client_id),
            getString(R.string.xweather_client_secret),
        )

        // Wait for the MapView to be attached before constructing the controller.
        binding.mapView.viewTreeObserver.addOnGlobalLayoutListener(
            object : ViewTreeObserver.OnGlobalLayoutListener {
                override fun onGlobalLayout() {
                    binding.mapView.viewTreeObserver.removeOnGlobalLayoutListener(this)
                    if (binding.mapView.parent == null) return
                    setUpMap(account)
                }
            })
    }

    private fun setUpMap(account: XweatherAccount) {
        val c = MapboxMapController(binding.mapView, account)
        controller = c

        c.setCenter(Coordinate(39.5, -98.0))
        c.setZoom(4.0)

        // Loading UI, driven by the controller's own signals.
        c.onLoadStart.observe(this) { binding.progress.isVisible = true }
        c.onLoadComplete.observe(this) { binding.progress.isVisible = false }

        binding.mapView.mapboxMap.subscribeMapLoaded {
            // MapsGL requires Mercator.
            binding.mapView.mapboxMap.style?.setProjection(projection(ProjectionName.MERCATOR))

            c.add(LegendControl().apply { mapView = binding.mapView })
            c.addDataInspectorControl(binding.mapView)

            // Pre-fetch tiles across the range so play() doesn't stall.
            c.animationOptions.shouldPreloadData = true
            c.timeline.setStartDateUsingRelativeTime("-1 day")
            c.timeline.end = Date()

            attachWeather()
        }
    }

    private fun attachWeather() {
        val c = controller ?: return
        if (weatherAttached) return
        activeCodes.forEach { c.addWeatherLayer(it) }
        weatherAttached = true
        c.timeline.play()
    }

    override fun onStart() {
        super.onStart()
        if (controller != null) attachWeather()
    }

    // Sessions accrue while layers are attached — detach when not visible.
    override fun onStop() {
        super.onStop()
        val c = controller ?: return
        c.timeline.pause()
        activeCodes.forEach { c.removeWeatherLayer(it) }
        weatherAttached = false
    }
}
```

Points worth carrying into any example you write: construct only after the view is
attached, set Mercator, add layers inside `subscribeMapLoaded`, and detach in
`onStop`.

## Weather layers

```kotlin
controller.addWeatherLayer(LayerCode.TEMPERATURES)                        // defaults
controller.addWeatherLayer(WeatherService.Temperatures(controller.service)) // to override paint
controller.addWeatherLayer(LayerCode.RADAR) { config -> /* tweak */ }      // configure lambda
controller.removeWeatherLayer(LayerCode.TEMPERATURES)                     // code only
controller.setWeatherLayerVisibility(LayerCode.RADAR, false)
```

`removeWeatherLayer` takes **only** the code - the extra-argument forms in the
website docs don't exist.

**`LayerCode` is not the style layer id.** To stack something relative to a
weather layer, get the real id first:

```kotlin
val id = controller.getWeatherLayer(LayerCode.TEMPERATURES)?.id
controller.addWeatherLayer(WeatherService.WindParticles(controller.service), beforeId = id)
```

Which codes exist, with wire code, factory and render type: `references/layers.md`.
Add/remove detail: `references/weather-layers.md`.

## Styling

Paint lives on the configuration's `layer.paint`, and its concrete type depends on
the layer's render type. `opacity` is a plain `Float`:

```kotlin
val config = WeatherService.Temperatures(controller.service) as WeatherLayerConfiguration<*, *>
val paint = config.layer.paint as SampleLayerPaint
paint.opacity = 1.0f
paint.sample.colorScale = ColorScaleOptions(stops = listOf(/* ... */))
controller.addWeatherLayer(config)
```

Render types and their paint namespaces are listed per section in
`references/layers.md`. `DataQuality` (`exact`, `high`, `medium`, `normal`, `low`)
trades resolution for bandwidth - a performance lever, never a cost one.

Paint by render type: `references/weather-styling.md`. Descriptor and paint
overview: `references/styles.md`. `StyleValue` / `Expression`:
`references/expressions.md`. Data-driven cookbooks: `references/data-driven.md`.

## Custom sources and layers

```kotlin
val source = controller.addSource(
    GeoJSONSourceDescriptor(id = "my-data", url = "https://example.com/data.geojson")
)
controller.addLayer(FillLayerDescriptor(/* ... */), beforeID = null)
controller.removeLayer("my-layer")
controller.removeSource("my-data")
```

Note `addLayer` takes **`beforeID`** while `addWeatherLayer` and `moveLayer` take
**`beforeId`**, and `removeLayer`'s second parameter is spelled `isCompounLayer` in
the public API.

Source descriptors: `references/sources.md`. Layer descriptors and `addLayer`
recipes: `references/custom-layers.md`.

## Animating over time

```kotlin
controller.animationOptions.shouldPreloadData = true   // false by default
controller.timeline.setStartDateUsingRelativeTime("-1 day")
controller.timeline.end = Date()
controller.timeline.play()
```

`shouldPreloadData` is the difference between playback that starts immediately and
playback that stalls while tiles arrive. Playback, range, events and the load-UI
signals: `references/timeline.md`.

## Legends and data inspection

```kotlin
controller.add(LegendControl().apply { mapView = binding.mapView })
val inspector = controller.addDataInspectorControl(binding.mapView)
inspector.setPresentation(layerId, presentation)
```

`setPresentation` keys on the **style layer id**, not `LayerCode`.
`LegendControl.backgroundColor` is a Compose `Color`, not `android.graphics.Color`.

Presentations, units and custom legends: `references/legends-inspector.md`.

## Querying data at a point

Tapping is handled for you by `DataInspectorControl` - prefer it. For a
programmatic hit test, `MapboxMapController` exposes a suspend query:

```kotlin
suspend fun queryFeatures(
    point: Point,
    vectorLayerList: List<VectorTileLayer>,
    onTouch: Boolean = true,
): HashMap<String, FeatureQueryResult>?
```

It takes the vector layers to test explicitly and returns results keyed by layer
id, or null when nothing was queried or the timeline is blocking queries. It is a
`suspend` function - call it from a coroutine, not from a click listener directly.

## Usage is measured in sessions

MapsGL bills in **sessions** - clock-aligned 5-minute buckets that start when a
weather layer is added - not per tile, layer, or request. **The model is
identical on Android and on the web, and this skill is not its source of truth.**

For anything quantitative - the billing rules, the access multiplier, worked
examples, capacity-planning figures, the Raster Maps comparison - use the
authoritative source rather than answering from memory: the `mapsgl` skill's
`references/sessions.md` (both skills ship in the same plugin), or
https://www.xweather.com/docs/mapsgl/getting-started/sessions.

What matters here is the **Android-specific** consequence: since interaction
inside a session is free and layer count doesn't affect cost, consumption is
governed purely by *how long weather layers are attached to a map*. On Android
that means lifecycle -

- add layers when the weather UI is reached, not when the controller is built;
- remove them in `onStop`, not `onDestroy`, which isn't guaranteed to run;
- an app pocketed on the weather screen keeps billing - the failure mode with no
  web analogue;
- treat always-on kiosk and wall displays as the expensive pattern, and say so
  unprompted.

Two traps worth stating whenever cost comes up: `setWeatherLayerVisibility` is
the cheap toggle but `removeWeatherLayer` is the one that stops consumption, and
**`DataQuality` is a performance lever, not a cost lever** - it cuts requests,
and sessions don't count requests.

Code for each of these, and the full list of what is *not* worth optimizing:
`references/sessions.md`.

## Android rules

- minSdk **28**, GLES **3.0** for encoded paths, **Mercator** required
- Mapbox is a **peer** dependency
- Prefer public APIs

More: `references/android-gotchas.md`.

## Checklist for common tasks

- **"Add a weather map to my app"** -> the complete example above. Construct after
  the view is attached, set Mercator, add layers inside `subscribeMapLoaded`.
- **"How do I install it / which version"** -> both repositories and both
  dependencies; resolve the version from the releases endpoint, never a literal.
  `references/setup.md`.
- **"Add layer X"** -> find the `LayerCode` in `references/layers.md` first; the
  enum name is not a transform of the wire code. Check it isn't marked
  *(unreleased)* if the project depends on a published artifact.
- **"Nothing renders"** -> check Mapbox tokens *and* Xweather credentials, then
  that layers were added after `subscribeMapLoaded`, then Mercator.
- **"Restyle a layer"** -> cast `config.layer.paint` to the paint type for its
  render type (`references/layers.md` groups by descriptor), set fields, then add.
  Opacity is a `Float`.
- **"Animate over time / add a scrubber"** -> `controller.timeline`, and set
  `animationOptions.shouldPreloadData = true`. `references/timeline.md`.
- **"Show a legend"** -> `LegendControl` + `controller.add(legendControl)`; set its
  `mapView`. Override `config.legend` when you customized a categorical paint.
- **"Show values on tap"** -> `addDataInspectorControl(mapView)`, customize with
  `setPresentation(layerId, presentation)` keyed by style layer id.
- **"Stack layers in a specific order"** -> resolve the real style layer id via
  `getWeatherLayer(code)?.id` and pass it as `beforeId`.
- **"How many accesses will this cost?"** -> sessions, not tiles or layers. Get the
  model and arithmetic from the `mapsgl` skill's `references/sessions.md` or the
  public docs, then apply the Android lifecycle guidance in
  `references/sessions.md`.
- **"Where are the API docs?"** -> releases endpoint for the version, then the
  KDoc URL pattern above. There is no `latest` alias.

## Attribution is required

Xweather requires attribution wherever its data or imagery is displayed. This applies to **all
products** - Weather API, Raster Maps, and MapsGL alike. Build it into anything you produce, and say
so when handing over code that will end up in front of users.

The minimum is a link to `https://www.xweather.com/` reading "Powered by Vaisala Xweather":

```kotlin
findViewById<TextView>(R.id.attribution).apply {
    text = "Powered by Vaisala Xweather"
    setOnClickListener {
        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://www.xweather.com/")))
    }
}
```

The logo may be substituted for the "Xweather" text. Light and dark variants exist in SVG and PNG at
`https://www.xweather.com/assets/logos/vaisala-xweather-logo-dark.svg` - swap `-dark` for `-light`
over a dark background, or `.svg` for `.png`. Bundle the asset as a drawable rather than loading it
over the network in a shipping app. Using the logo brings rules: keep it unmodified, leave at least a
**10dp buffer** of space around it, and only adjust lightness or opacity in greyscale. Don't rotate
it, don't recolour it (monotone black or white excepted), and don't use the symbol without the
Xweather name.

Full guide: https://www.xweather.com/docs/weather-api/resources/attribution

## Reference index

| File | Use when |
|---|---|
| `references/setup.md` | Install, MapLoaded, credentials |
| `references/layers.md` | The layer catalog - every `LayerCode`, its wire code, factory and render type |
| `references/api-reference.md` | Real signatures for every public type, and the KDoc URL pattern |
| `references/weather-layers.md` | LayerCode / WeatherService add/remove |
| `references/weather-styling.md` | Raster/sample/particle/grid paint |
| `references/timeline.md` | Range, playback, events, load UI |
| `references/styles.md` | Descriptor/paint overview |
| `references/expressions.md` | StyleValue / Expression |
| `references/data-driven.md` | match/get/concat cookbooks |
| `references/sources.md` | Vector / GeoJSON / encoded sources |
| `references/custom-layers.md` | addLayer fill/circle/... |
| `references/legends-inspector.md` | Legends + Presentation |
| `references/sessions.md` | The Android half of session cost: lifecycle teardown + traps. Points at the `mapsgl` skill for the billing model itself |
| `references/android-gotchas.md` | Platform pitfalls |
