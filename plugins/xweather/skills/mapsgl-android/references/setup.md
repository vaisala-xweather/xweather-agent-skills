# Setup - MapsGL Android

**These instructions have been executed, not just written.** A blank Android project was scaffolded
from this file and `SKILL.md`, built against MapsGL Android 1.6.1, and run. Everything below is what
that took - including the `maven.ecc.no` repository and the ViewBinding flag, both of which were
missing until the build failed on them.

Read against the SDK's Gradle files, library manifest and constructors on the `feature/maptime-filter`
branch. The getting-started page is secondary when it disagrees - it still shows the deprecated
4-argument controller and omits the Mapbox dependency entirely.
https://www.xweather.com/docs/mapsgl-android-sdk/getting-started

## Requirements

| | Value | Why |
|---|---|---|
| `minSdk` | **28** | Hard floor; the library manifest will fail to merge below it |
| `compileSdk` / `targetSdk` | 36 | What the SDK is built against |
| NDK | 29.0.14033849 | Matches the `android-ndk27` Mapbox variant |
| Java | **17** (`sourceCompatibility`, `jvmTarget`) | Build fails on 11 |
| Kotlin | 2.1.10 | |
| AGP | 8.11.2 | |
| OpenGL ES | **3.0**, declared `required="true"` | Encoded raster layers are GLES custom layers |
| Projection | **Mercator** | Globe is not supported |

The GLES 3.0 requirement is declared in the SDK's own manifest as
`<uses-feature android:glEsVersion="0x00030000" android:required="true" />`, which merges into your
app - so **Google Play will filter out devices without GLES 3.0**. That is intended, but it is a
distribution consequence worth knowing before you ship.

## Credentials - both sets are required

1. **Xweather** client id + secret - https://data.portal.xweather.com/account/keys
   Passed to `XweatherAccount(id, secret)`. Bound to a namespace (reverse-DNS bundle id for mobile);
   a request from outside it fails regardless of whether the URL is right.
2. **Mapbox** - two *different* tokens:
   - **Runtime**: a public `pk.` token, as the `mapbox_access_token` string resource. Without it the
     basemap is blank and weather layers have nothing to draw on.
   - **Build**: a secret `sk.` downloads token as `MAPBOX_DOWNLOADS_TOKEN` in `gradle.properties`,
     used to resolve the Mapbox SDK from Mapbox Maven. Without it the build fails at dependency
     resolution, before any of this runs.

If nothing renders or auth fails, check **both** credential sets before digging into MapsGL. A
missing Mapbox token presents as a MapsGL failure but isn't one.

### Keeping keys out of the repository

`gradle.properties` in the repo root is committed by default - put `MAPBOX_DOWNLOADS_TOKEN` in
`~/.gradle/gradle.properties` instead, or read it from the environment. Xweather credentials in
`strings.xml` ship inside the APK and are extractable; the namespace binding is what limits the
damage, so set it correctly rather than relying on the secret staying secret.

## Gradle

### settings.gradle repositories

```gradle
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
            credentials {
                username = "mapbox"
                password = MAPBOX_DOWNLOADS_TOKEN
            }
        }
        // The SDK has a transitive `api` dependency on
        // no.ecc.vectortile:java-vector-tile, published only here.
        maven { url = uri("https://maven.ecc.no/releases") }
    }
}
```

The official getting-started shows only JitPack. **All four repositories are required.**

- **Mapbox Maven** - MapsGL treats Mapbox as a peer dependency and does not ship it transitively.
- **`maven.ecc.no`** - hosts `no.ecc.vectortile:java-vector-tile`, which the SDK exposes as an `api`
  dependency. Omitting it fails at dependency resolution with
  `Could not find no.ecc.vectortile:java-vector-tile:1.4.1`, which looks like a broken SDK release
  rather than a missing repository. This is the single most likely reason a first build fails.

The `metadataSources` block is worth keeping: JitPack publishes a rewritten Gradle `*.module`
descriptor that resolves fine but loses the sources/KDoc wiring, so the IDE shows no documentation
for SDK symbols. Preferring the POM and artifact avoids that.

### App dependency

Resolve the version rather than copying a literal - `products["mapsgl-android-sdk"].version` from
https://www.xweather.com/docs/api/releases/versions:

```gradle
dependencies {
    implementation "com.github.vaisala-xweather:mapsgl-android-sdk:vX.Y.Z"
    implementation "com.mapbox.maps:android-ndk27:11.15.3"
}
```

Do **not** also add a `...:mapsglmaps` artifact - that duplicates the SDK.

`android-ndk27` is a Mapbox *variant*, not a version suffix: Mapbox publishes builds against
different NDK versions and this is the one MapsGL is compiled against. Swapping it for the plain
`com.mapbox.maps:android` artifact can produce native-linkage failures at runtime rather than at
build time.

## What the SDK merges into your app

Two things arrive from the library that are easy to miss.

**Manifest attributes.** The SDK's library manifest declares an `<application>` block with
`allowBackup`, `icon`, `label`, `supportsRtl` and **`largeHeap="true"`**. These merge into your app's
manifest. `largeHeap` in particular is a real behavioural change you did not opt into - if your app
has its own heap strategy, override it explicitly:

```xml
<application
    android:largeHeap="false"
    tools:replace="android:largeHeap">
```

Any attribute you set yourself and the library also sets will raise a manifest-merger error until you
add `tools:replace` for it.

**Transitive dependencies.** The SDK exposes several deps as `api`, so they land on your compile
classpath whether you asked or not: `androidx.appcompat`, `com.google.android.material`,
`androidx.compose.ui:ui-graphics`, `androidx.navigation:navigation-compose`, Glide, `hilt-android`,
and `no.ecc.vectortile:java-vector-tile`. That is why `LegendControl.backgroundColor` is a Compose
`Color`, and why `maven.ecc.no` has to be in your repository list. You do not have to adopt Compose
or Hilt to use the SDK, but version conflicts with your own copies of these will surface as
duplicate-class or resolution errors.

## Strings

```xml
<string name="mapbox_access_token">pk....</string>
<string name="xweather_client_id">...</string>
<string name="xweather_client_secret">...</string>
```

## Minimal Activity - wait for map loaded

Two conditions must hold before adding weather layers: the `MapView` is attached, and the Mapbox map
has loaded. Adding earlier silently does nothing.

```kotlin
import com.mapbox.maps.Style
import com.mapbox.maps.extension.style.layers.properties.generated.ProjectionName
import com.mapbox.maps.extension.style.projection.generated.projection
import com.mapbox.maps.extension.style.projection.generated.setProjection
import com.xweather.mapsgl.config.weather.account.XweatherAccount
import com.xweather.mapsgl.map.mapbox.MapboxMapController
import com.xweather.mapsgl.weather.LayerCode
import com.xweather.mapsgl.weather.WeatherService

val account = XweatherAccount(
    getString(R.string.xweather_client_id),
    getString(R.string.xweather_client_secret),
)

mapView.viewTreeObserver.addOnGlobalLayoutListener(
    object : ViewTreeObserver.OnGlobalLayoutListener {
        override fun onGlobalLayout() {
            mapView.viewTreeObserver.removeOnGlobalLayoutListener(this)
            if (mapView.parent == null) return

            mapController = MapboxMapController(mapView, account)
            mapController.mapboxMap?.setProjection(projection(ProjectionName.MERCATOR))

            mapView.mapboxMap.subscribeMapLoaded {
                // Config factory - use when you will override paint or presentation:
                mapController.addWeatherLayer(WeatherService.Temperatures(mapController.service))
                // Or LayerCode when defaults are enough:
                // mapController.addWeatherLayer(LayerCode.TEMPERATURES)
            }
        }
    })
```

**Constructor:** `MapboxMapController(mapView, account)`. The
`(mapView, baseContext, account, lifecycleOwner)` form still shown in older docs is deprecated and
merely delegates to this one. There is **no** `(mapView, account, AnimationOptions(...))` overload -
configure `mapController.animationOptions` and `mapController.timeline` after construction.

### Mercator, and when to set it

MapsGL requires the Mercator projection. There are two working placements, and the difference matters:

```kotlin
// Before loading a style - fine when you don't replace the style afterwards
mapController.mapboxMap?.setProjection(projection(ProjectionName.MERCATOR))

// After a style loads - use this when you also call loadStyle()
mapView.mapboxMap.subscribeMapLoaded {
    mapView.mapboxMap.style?.setProjection(projection(ProjectionName.MERCATOR))
}
```

Projection is a style property, so a later `loadStyle()` can drop it. If you swap the basemap style
at any point, re-apply the projection after the new style loads.

## Placing weather layers relative to the basemap

Weather layers are added on top by default. To keep basemap labels above the weather, pass the id of
an existing style layer as `beforeId` - weather is then inserted *below* it:

```kotlin
val style = mapView.mapboxMap.style
val labelLayerId = style?.styleLayers?.firstOrNull { info ->
    style.getStyleLayerProperty(info.id, "type").value?.toString() == "symbol"
}?.id
mapController.addWeatherLayer(LayerCode.TEMPERATURES, beforeId = labelLayerId)
```

The SDK's own KDoc for `beforeId` reads "existing layer id to insert **below** in the stack", so the
weather layer lands underneath the label layer you name.

The other approach the demos use is to blank the basemap's own labels instead, which avoids the
ordering question entirely:

```kotlin
// Clear text on every symbol layer in the loaded style
for (layerInfo in style.styleLayers) {
    if (style.getStyleLayerProperty(layerInfo.id, "type").value?.toString() != "symbol") continue
    runCatching { style.setStyleLayerProperty(layerInfo.id, "text-field", Value.valueOf("")) }
}
```

To stack weather layers relative to *each other*, resolve the real style layer id first -
`LayerCode` is not a style layer id:

```kotlin
val id = mapController.getWeatherLayer(LayerCode.TEMPERATURES)?.id
mapController.addWeatherLayer(WeatherService.WindParticles(mapController.service), beforeId = id)
```

## Loading indicator

```kotlin
mapController.onLoadStart.observe(this) { binding.loadingBar.isVisible = true }
mapController.onLoadComplete.observe(this) { binding.loadingBar.isVisible = false }
mapController.onLoadProgress.observe(this) { p -> binding.bar.progress = /* from MapLoadProgress */ }
```

These are `LiveData` - observe them with a `LifecycleOwner`, not a raw callback.

## Build and runtime failures

| Symptom | Cause |
|---|---|
| `Could not find no.ecc.vectortile:java-vector-tile` | `maven.ecc.no` missing from `settings.gradle` - the most common first-build failure |
| `ActivityXBinding` unresolved in an example | `buildFeatures { viewBinding true }` not enabled |
| Dependency resolution fails on `com.mapbox.maps` | Mapbox Maven repo missing from `settings.gradle`, or `MAPBOX_DOWNLOADS_TOKEN` unset |
| 401 from `api.mapbox.com` during build | Downloads token is wrong, expired, or is a `pk.` public token where an `sk.` secret one is needed |
| Manifest merger error on an `<application>` attribute | The library sets it too - add `tools:replace` for that attribute |
| `minSdk` merge failure | Your `minSdk` is below 28 |
| Build fails with Java target errors | `sourceCompatibility` / `jvmTarget` below 17 |
| Duplicate class / version conflict on Compose, Material, Glide or Hilt | Your versions differ from the ones the SDK exposes as `api` |
| Blank map, no basemap tiles | Runtime `mapbox_access_token` missing or invalid |
| Basemap renders, no weather at all | Xweather credentials wrong, or namespace mismatch |
| Weather layers added but never appear | Added before `subscribeMapLoaded`, or the `MapView` was not yet attached |
| Weather misaligned or absent at low zoom | Projection is globe - set Mercator |
| No IDE documentation for SDK symbols | JitPack's rewritten `*.module` - add the `metadataSources` block |
| Layers vanish after a basemap change | `loadStyle()` dropped the projection and the layers - re-apply after the style loads |

## External links (secondary to the SDK)

- Hub: https://www.xweather.com/docs/mapsgl-android-sdk/
- Getting started: https://www.xweather.com/docs/mapsgl-android-sdk/getting-started
- Releases JSON: https://www.xweather.com/docs/api/releases/versions
- KDoc: `https://cdn.aerisapi.com/sdk/android/mapsgl/docs/v{version}/mapsglmaps/` - no `latest` alias
