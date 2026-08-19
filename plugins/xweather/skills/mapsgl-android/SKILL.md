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
  dependency). Covers only public MapsGL Android APIs. When docs and SDK disagree,
  prefer the SDK (source / KDoc / demos) over xweather.com documentation.
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
signature, package, or demo in the SDK, follow the SDK and say so. Do not invent
JS-only or unreleased APIs.

Docs hub (optional context only):
https://www.xweather.com/docs/mapsgl-android-sdk/

**API scope:** public MapsGL Android APIs only - no internals.

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
No Compose unless asked.

```kotlin
val account = XweatherAccount(
    getString(R.string.xweather_client_id),
    getString(R.string.xweather_client_secret),
)
val controller = MapboxMapController(mapView, account)
```

Resolve the release tag (above) before pinning, rather than copying `vX.Y.Z`:

```gradle
implementation "com.github.vaisala-xweather:mapsgl-android-sdk:vX.Y.Z"
implementation "com.mapbox.maps:android-ndk27:11.15.3"
```

Full install + **MapLoaded** pattern: `references/setup.md`.

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

## Common tasks

### Weather layers

```kotlin
controller.addWeatherLayer(LayerCode.TEMPERATURES)
controller.addWeatherLayer(WeatherService.Temperatures(controller.service))
controller.removeWeatherLayer(LayerCode.TEMPERATURES)
```

Details + LayerCode vs id: `references/weather-layers.md`.  
Paint overrides: `references/weather-styling.md`.

### Timeline

```kotlin
controller.timeline.setStartDateUsingRelativeTime("-1 day")
controller.timeline.end = Date()
controller.timeline.play()
```

Full API: `references/timeline.md`.

### Legends / inspector

```kotlin
controller.add(LegendControl())
val inspector = controller.addDataInspectorControl(mapView)
```

Presentations: `references/legends-inspector.md`.

### Custom sources & layers

`references/sources.md`, `references/custom-layers.md`, `references/data-driven.md`.

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
| `references/api-reference.md` | Method map |
| `references/android-gotchas.md` | Platform pitfalls |
