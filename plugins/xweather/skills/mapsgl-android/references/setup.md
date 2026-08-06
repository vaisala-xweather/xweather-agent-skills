# Setup - MapsGL Android (1.6.x)

Verified against SDK constructors, demos, and Gradle packaging (1.6.x).
Getting-started docs are secondary when they disagree (e.g. deprecated 4-arg controller).
https://www.xweather.com/docs/mapsgl-android-sdk/getting-started\r\n\r\n## Credentials (both required)

1. **Xweather** client id + secret - https://data.portal.xweather.com/account/keys  
   Passed to `XweatherAccount(id, secret)`.
2. **Mapbox**
   - Runtime: `mapbox_access_token` (or Mapbox token setup per Mapbox docs)
   - Gradle downloads: `MAPBOX_DOWNLOADS_TOKEN` in `gradle.properties` for Mapbox Maven

If nothing renders or auth fails, check **both** credential sets before digging into MapsGL.

## Gradle

### settings.gradle repositories

```gradle
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://jitpack.io") }
        maven {
            url = uri("https://api.mapbox.com/downloads/v2/releases/maven")
            authentication { basic(BasicAuthentication) }
            credentials {
                username = "mapbox"
                password = MAPBOX_DOWNLOADS_TOKEN
            }
        }
    }
}
```

Official getting-started shows only JitPack; **also** add Mapbox Maven - MapsGL does not
ship Mapbox transitively.

### App dependency

Look up `products["mapsgl-android-sdk"].version` from
https://www.xweather.com/docs/api/releases/versions:

```gradle
dependencies {
    implementation "com.github.vaisala-xweather:mapsgl-android-sdk:vX.Y.Z"
    implementation "com.mapbox.maps:android-ndk27:11.15.3"
}
```

Do **not** also add a duplicate `...:mapsglmaps` multi-module artifact.

## Strings

```xml
<string name="mapbox_access_token">pk....</string>
<string name="xweather_client_id">...</string>
<string name="xweather_client_secret">...</string>
```

## Minimal Activity (MapLoaded - preferred ready signal)

Prefer waiting for **map loaded** before adding weather layers (SDK demos + reliable ready signal):

```kotlin
import com.mapbox.maps.MapLoadedCallback
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

val mapLoadedCallback = MapLoadedCallback {
    // Config factory (good when you will override paint / presentation):
    mapController.addWeatherLayer(WeatherService.Temperatures(mapController.service))
    // Or LayerCode when defaults are enough:
    // mapController.addWeatherLayer(LayerCode.TEMPERATURES)
}

mapView.viewTreeObserver.addOnGlobalLayoutListener(object : ViewTreeObserver.OnGlobalLayoutListener {
    override fun onGlobalLayout() {
        mapView.viewTreeObserver.removeOnGlobalLayoutListener(this)
        mapController = MapboxMapController(mapView, account)
        with(mapController) {
            mapboxMap?.setProjection(projection(ProjectionName.MERCATOR))
            mapboxMap?.loadStyle(Style.LIGHT)
            mapboxMap?.subscribeMapLoaded(mapLoadedCallback)
        }
    }
})
```

**Constructor:** use `MapboxMapController(mapView, account)`.  
Do **not** use the deprecated `(mapView, baseContext, account, lifecycleOwner)` form from older docs.

There is **no** `MapboxMapController(mapView, account, AnimationOptions(...))` overload on 1.6.x -
configure `mapController.animationOptions` or `mapController.timeline` after construction.

## Loading indicator

```kotlin
mapController.onLoadStart.observe(this) { binding.loadingBar.isVisible = true }
mapController.onLoadComplete.observe(this) { binding.loadingBar.isVisible = false }
```

## External links (secondary to SDK)\r\n\r\n- Hub: https://www.xweather.com/docs/mapsgl-android-sdk/
- Getting started: https://www.xweather.com/docs/mapsgl-android-sdk/getting-started
- Layer catalog JSON: https://www.xweather.com/docs/api/mapsgl/layers
- Releases JSON: https://www.xweather.com/docs/api/releases/versions
