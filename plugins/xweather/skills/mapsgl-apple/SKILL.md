---
name: mapsgl-apple
description: This skill should be used when working with the Xweather MapsGL SDK for Apple platforms (the MapsGL iOS/iPadOS/macCatalyst/visionOS SDK) — installing it via Swift Package Manager, CocoaPods, Carthage or xcframeworks, creating a MapboxMapController or MapLibreMapController, and adding, removing, styling, animating or inspecting MapsGL weather layers in Swift. Use it whenever a task mentions MapsGL on iOS or Apple platforms, mapsgl-apple-sdk, MapsGLMaps, MapsGLMapbox, MapsGLMapLibre, XweatherAccount, WeatherService.LayerCode, addWeatherLayer in Swift, or a native weather map in SwiftUI or UIKit. Also use it for questions about MapsGL session usage or cost in an Apple app — sessions, the 5-minute clock intervals, the access multiplier, and which view and app lifecycle events should attach and detach weather layers. Also covers Xweather's attribution requirement — the 'Powered by Vaisala Xweather' credit and logo rules that apply wherever Xweather data or imagery is displayed.
license: MIT
metadata:
  author: Vaisala Xweather
  version: "0.13.0"
---

# MapsGL for Apple platforms

The Xweather MapsGL SDK for Apple platforms renders weather and custom map data client-side with
Metal, layered on top of **Mapbox Maps** or **MapLibre Native**. It requires an active Xweather
account with Weather API + Maps access (client id + secret).

Platform support comes from the package manifest: **iOS 16+, macCatalyst 16+, visionOS 1+**. There is
no native macOS (AppKit) target — a "macOS" app here means Mac Catalyst.

Docs: https://www.xweather.com/docs/mapsgl-apple-sdk/getting-started ·
Distribution + demo app: https://github.com/vaisala-xweather/mapsgl-apple-sdk

## Ask which map provider unless the context tells you

The map provider is not a stylistic preference that can be defaulted: Mapbox and MapLibre resolve
*different Swift Package branches*, different transitive SDKs, and different map-view types. Getting
it wrong means the code doesn't compile and the package graph has to be redone.

So **infer it when the context actually says, and ask when it doesn't.** Never pick one by default.

**Infer it** from evidence like:

- the user named the provider in their request;
- the project already integrates one — an `import MapsGLMapbox` / `import MapsGLMapLibre`, a resolved
  `mapbox-maps-ios` or `maplibre-gl-native-distribution` dependency, a `Podfile` naming one, an
  `MLNMapView` or `MapboxMaps.MapView` in the source, or a `MBXAccessToken` in an Info.plist;
- the project already uses the provider's SDK elsewhere, even without MapsGL — a Mapbox-based map
  screen means Mapbox.

When you infer, **say which provider you picked and what told you**, so a wrong read is cheap to
correct.

**Ask** when the evidence is absent or contradictory — a greenfield app, a project with no map
dependency yet, or one carrying traces of both. Weak circumstantial signals ("we want a dark map
style", "our designer sent Mapbox screenshots") are not evidence of an integration; ask rather than
build the whole package graph on them.

Trade-offs to offer alongside the question, briefly:

| | Mapbox Maps | MapLibre Native |
|---|---|---|
| Basemap key | Mapbox account access token required, plus a secret token to download the SDK | None — but the style URL's tile provider may need one (CARTO's public styles don't) |
| Cost | Mapbox map-load pricing applies | No basemap vendor cost |
| SwiftUI | Native `Map` view | `MLNMapView` wrapped in a `UIViewRepresentable` |
| MapsGL constraint | Must set the **mercator** projection — the default globe projection is incompatible | None |

## How to write MapsGL Apple examples

**Default to SwiftUI.** Produce UIKit only when the project is UIKit (a `UIViewController`-based app,
storyboards/XIBs, an `AppDelegate`/`SceneDelegate` pair with no SwiftUI `App`) or the user asks for
it. Match the surrounding project over the default whenever the two disagree — including Swift
concurrency style, view-model conventions, and how the app already stores secrets.

**Never hardcode a version number.** Resolve the current release when you need one:

```bash
curl -s https://www.xweather.com/docs/api/releases/versions \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["products"]["mapsgl-apple-sdk"]["version"])'
```

That endpoint is the release source of truth for every Xweather product, keyed by product id —
`mapsgl-apple-sdk` here, alongside `mapsgl`, `weather-api`, `maps`, and others. It's a small public
JSON document, no auth needed.

Most of the time you don't need a version at all: **prefer the Swift Package branch channels**
(below), which track the latest release without a pin. A version is only needed for a deliberate
pin, a CocoaPods/Carthage requirement, or an API-reference URL.

**Credentials never go in source.** Put the Xweather client id/secret and any Mapbox token in a
gitignored plist, xcconfig, or the keychain — whatever the project already uses — and read them at
runtime. The demo app's `AccessKeys.plist` pattern is a reasonable model when the project has none.
Write `"FILL_IN_WITH_YOUR_CLIENT_ID"`-style placeholders rather than inventing plausible keys.

**Every example must include the Xweather attribution.** It's a requirement of using the product, not
a nicety, so build it into the view rather than mentioning it afterwards. See "Attribution is
required".

## API reference

The full API reference is DocC, published per SDK version:

```
https://cdn.aerisapi.com/sdk/ios/mapsgl/docs/v{version}/documentation/mapsglmaps
```

Substitute the version from the releases endpoint above — **there is no `latest` alias**;
`.../docs/latest/...` 404s. Only the `mapsglmaps` module is published; `MapsGLCore`,
`MapsGLRenderer`, and the two adapter modules have no hosted DocC.

The version index page, which lists every published version, is
https://www.xweather.com/docs/mapsgl-apple-sdk/api-reference.

A machine-readable symbol index sits alongside it at
`https://cdn.aerisapi.com/sdk/ios/mapsgl/docs/v{version}/index/index.json` — useful for checking
whether a symbol exists in a given release before writing code against it.

`references/api-reference.md` carries the surface an agent needs most (controller, service, timeline,
controls, descriptors) so the common cases need no network call.

## Core concepts

| Concept | What it is |
|---|---|
| `XweatherAccount(id:secret:)` | Wraps client id/secret credentials used for all data requests |
| `MapController` | Adapter between the underlying map (`MapboxMaps.MapboxMap` / `MLNMapView`) and MapsGL — the object almost everything below is called on. Concrete: `MapboxMapController`, `MapLibreMapController` |
| `WeatherService` | The account-bound weather data service, reachable as `controller.service`. Namespaces every built-in layer configuration and `WeatherService.LayerCode` |
| `WeatherService.LayerCode` | Enum identifying a built-in weather layer — `.radar`, `.temperatures`, `.windParticles` |
| `WeatherService.<Name>` | Per-layer configuration struct (`WeatherService.Temperatures`) holding `layer`, `legend`, and `presentation`. Instantiate it to override defaults |
| Source descriptors | Where custom layer data comes from — `ImageSourceDescriptor`, `EncodedSourceDescriptor`, `VectorSourceDescriptor`, `GeoJSONSourceDescriptor` |
| Layer descriptors | How data is rendered — `RasterLayerDescriptor`, `SampleLayerDescriptor`, `ParticleLayerDescriptor`, `GridLayerDescriptor`, `ContourLayerDescriptor`, `FillLayerDescriptor`, `LineLayerDescriptor`, `CircleLayerDescriptor`, `SymbolLayerDescriptor`, `HeatmapLayerDescriptor` |
| `paint` | Per-descriptor style config, namespaced by render type — `paint.sample`, `paint.fill`, `paint.stroke`. See `references/styles.md` |
| `Expression` | Data-driven paint values and layer filters, built with static factories — `Expression.get("COLOR")`. See `references/expressions.md` |
| `ColorScaleOptions` / `ColorStop` | Maps a continuous data range to colors, used by `paint.sample.colorScale` and bar legends |
| `LegendControl` | Manages the legends visible on a map; auto-syncs with built-in weather layers. See `references/legends.md` |
| `DataInspectorControl` | Tap-to-inspect callout showing raw layer values at a coordinate |
| `controller.timeline` | Drives time animation across every animated layer at once. See `references/timeline.md` |

Built-in **weather layers** are pre-wired combinations of a source + styled layer(s), addressed by a
single `LayerCode` case. Prefer these over hand-building sources and layers unless visualizing custom
or non-weather data.

## Setup

### 1. Credentials

Two independent sets, both required:

1. **Xweather account keys** — `CLIENT_ID` / `CLIENT_SECRET` from
   https://data.portal.xweather.com/account/keys. Passed as `XweatherAccount(id:secret:)`.
2. **The map provider's own credentials** —
   - Mapbox → a public access token set on `MapboxOptions.accessToken`, **plus** a secret download
     token configured in `~/.netrc` so SPM/CocoaPods can fetch the Mapbox SDK at all. The secret
     token is a build-time requirement; forgetting it fails resolution, not runtime.
   - MapLibre → nothing for the SDK. The basemap `styleURL` points at a tile provider, which may need
     its own key (CARTO's public Positron/Dark Matter styles do not).

If nothing renders, check both sets before investigating MapsGL.

### 2. Install

**Swift Package Manager (preferred).** Add `https://github.com/vaisala-xweather/mapsgl-apple-sdk` and
pick the **branch matching your provider** — the package manifest at the repo root is
provider-specific per branch, so the branch *is* the provider choice:

| Channel | Branch | Resolves | Product |
|---|---|---|---|
| Latest Mapbox | `master` | `mapbox-maps-ios` 11.x | `MapsGL` |
| Latest MapLibre | `maplibre` | `maplibre-gl-native-distribution` 6.18+ | `MapsGL` |
| Pinned Mapbox | `release/x.y.z` | as above, frozen | `MapsGL` |
| Pinned MapLibre | `release/maplibre/x.y.z` | as above, frozen | `MapsGL` |

The product name is `MapsGL` on every branch; what differs is which adapter target it includes. Add
the `MapsGL` library product to the app target. Xcode resolves the three binary xcframeworks
(`MapsGLCore`, `MapsGLRenderer`, `MapsGLMaps`) plus the provider SDK and `turf-swift` automatically.

Use a branch channel unless the user asked to pin. Pinning to `release/…` is the right call for
release-managed apps; note that it also freezes the provider SDK range.

**CocoaPods** — `pod 'MapsGL'`, then `pod install` and open the generated `.xcworkspace`. CocoaPods
builds a single `MapsGL` module, so **`import MapsGL` replaces the adapter import**
(`import MapsGLMapbox` / `import MapsGLMapLibre`) in every source file. This is the most common
CocoaPods build error.

**Carthage** (`github "vaisala-xweather/mapsgl-apple-sdk" ~> x.y.z`, then
`carthage update --use-xcframeworks`) and **manual xcframework embedding** (download `MapsGL.zip`
from the releases page, embed the three xcframeworks as "Embed & Sign") both require adding the
provider SDK yourself and dropping the matching adapter *source directory*
(`MapsGLMapbox/` or `MapsGLMapLibre/`) straight into the project. When the adapter is compiled into
your target that way, **remove the `import MapsGLMapbox` / `import MapsGLMapLibre` lines** — the
types are already in your module.

### 3. Imports

```swift
import MapsGLMaps      // always
import MapsGLMapbox    // SPM, Mapbox channel   — omit for CocoaPods/Carthage/manual
import MapsGLMapLibre  // SPM, MapLibre channel — omit for CocoaPods/Carthage/manual
import MapsGL          // CocoaPods only, in place of the adapter import
import Combine         // controller events return AnyCancellable
```

### 4. Create the controller, then wait for load

```swift
let account = XweatherAccount(id: clientID, secret: clientSecret)
let controller = MapboxMapController(map: map, account: account)

controller.onLoad.observe { _ in
    _ = try? controller.addWeatherLayer(for: .radar)
}.store(in: &cancellables)
```

| Provider | Controller | Map argument |
|---|---|---|
| Mapbox | `MapboxMapController` | `MapboxMaps.MapView`, or `MapboxMaps.MapboxMap` + `window:` |
| MapLibre | `MapLibreMapController` | `MLNMapView` |

**Every layer/source call must be gated behind load**, and the observation returns an `AnyCancellable`
you must retain — `.store(in: &cancellables)`. Drop it and the observer is torn down immediately and
the map stays empty, with no error.

Use `onLoad.observe { … }`. The older `subscribe(to: MapEvents.Load.self) { … }` is **deprecated**
("Use available on<event>.observe() methods instead") — note that the web docs' SwiftUI sample still
shows it, so copying from there warns on a new project. Same for `asyncSubscribe` and
`subscribeToNext`; only `publisher(for:)` survives, for when you want Combine operators.

**The layer and source API is `@MainActor`.** `addWeatherLayer`, `removeWeatherLayer`,
`setWeatherLayerVisibility`, `weatherLayer(for:)`, `addSource`, `addLayer`, `addImage`, and
`add(legendControl:)` are all main-actor-isolated. The `onLoad` observer already runs on the main
thread, so the usual path needs nothing extra — but a call made from a detached task or a
non-isolated callback needs `await MainActor.run { … }`, or it won't compile under strict
concurrency.

**Mapbox requires the mercator projection.** The current Mapbox styles (streets/outdoor/satellite
streets v12, light/dark v11) default to the globe projection, which MapsGL cannot render onto:

```swift
try map.setProjection(.init(name: .mercator))
```

Symptom when missing: the basemap draws normally and MapsGL layers simply never appear.

## Complete example — SwiftUI

**Mapbox.** `MapReader` hands back a `MapboxMap`, so use the `window:`-taking initializer:

```swift
import SwiftUI
import Combine
import MapboxMaps
import MapsGLMaps
import MapsGLMapbox

struct WeatherMapView: View {
    // Read these from a gitignored plist / xcconfig / keychain — never commit them.
    private let xweatherClientID = "FILL_IN_WITH_YOUR_CLIENT_ID"
    private let xweatherClientSecret = "FILL_IN_WITH_YOUR_CLIENT_SECRET"

    final class Coordinator: ObservableObject {
        var controller: MapboxMapController?
        var cancellables: Set<AnyCancellable> = []
    }
    @StateObject private var coordinator = Coordinator()

    var body: some View {
        MapReader { proxy in
            Map(initialViewport: .camera(
                center: CLLocationCoordinate2D(latitude: 39.65, longitude: -93.10),
                zoom: 3.5
            ))
            .mapStyle(.light)
            .ignoresSafeArea()
            .overlay(alignment: .bottomTrailing) { XweatherAttribution() }
            .onAppear {
                guard let map = proxy.map, coordinator.controller == nil else { return }

                // MapsGL cannot render onto Mapbox's default globe projection.
                try? map.setProjection(.init(name: .mercator))

                let controller = MapboxMapController(
                    map: map,
                    window: UIWindow?.none,
                    account: XweatherAccount(id: xweatherClientID, secret: xweatherClientSecret)
                )
                coordinator.controller = controller

                controller.onLoad.observe { _ in
                    do {
                        try controller.addWeatherLayer(for: .radar)

                        var winds = WeatherService.WindParticles(service: controller.service)
                        winds.layer.paint.particle.density = .high
                        try controller.addWeatherLayer(config: winds)
                    } catch {
                        NSLog("Failed to add weather layer: \(error)")
                    }
                }.store(in: &coordinator.cancellables)
            }
        }
    }
}
```

Set the Mapbox token once, before any map is created — in the `App` initializer or an
`@main` type's `init()`:

```swift
MapboxOptions.accessToken = "FILL_IN_WITH_YOUR_MAPBOX_PUBLIC_ACCESS_TOKEN"
```

**MapLibre.** MapLibre ships no SwiftUI view, so wrap `MLNMapView`. No token, and no projection call:

```swift
import SwiftUI
import Combine
import MapLibre
import MapsGLMaps
import MapsGLMapLibre

struct WeatherMapView: UIViewRepresentable {
    private let xweatherClientID = "FILL_IN_WITH_YOUR_CLIENT_ID"
    private let xweatherClientSecret = "FILL_IN_WITH_YOUR_CLIENT_SECRET"

    final class Coordinator {
        var controller: MapLibreMapController?
        var cancellables: Set<AnyCancellable> = []
    }
    func makeCoordinator() -> Coordinator { Coordinator() }

    func makeUIView(context: Context) -> MLNMapView {
        let mapView = MLNMapView(frame: .zero)
        // Any MapLibre-compatible style. CARTO's public styles need no key.
        mapView.styleURL = URL(string: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json")!
        mapView.setCenter(
            CLLocationCoordinate2D(latitude: 39.65, longitude: -93.10),
            zoomLevel: 3.5,
            animated: false
        )

        let controller = MapLibreMapController(
            map: mapView,
            account: XweatherAccount(id: xweatherClientID, secret: xweatherClientSecret)
        )
        context.coordinator.controller = controller

        controller.onLoad.observe { _ in
            _ = try? controller.addWeatherLayer(for: .radar)
        }.store(in: &context.coordinator.cancellables)

        return mapView
    }

    func updateUIView(_ uiView: MLNMapView, context: Context) {}
}
```

Place the attribution over either map — required in both cases:

```swift
struct XweatherAttribution: View {
    var body: some View {
        Link(destination: URL(string: "https://www.xweather.com/")!) {
            Text("Powered by Vaisala Xweather")
                .font(.caption2)
                .padding(.horizontal, 6).padding(.vertical, 3)
                .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 3))
        }
        .padding(8)
    }
}
```

For UIKit, the shape is the same — build the map view in `viewDidLoad`, create the controller, and
observe `onLoad`. A worked UIKit example for both providers is in `references/setup.md`, and the
repo's `Demo/UIKit/MapViewController.swift` is the maintained version.

The demo app is the best full reference and covers both channels:
https://github.com/vaisala-xweather/mapsgl-apple-sdk/tree/master/Demo

## Weather layers

```swift
try controller.addWeatherLayer(for: .temperatures)
try controller.addWeatherLayer(for: .windParticles)

for code in [WeatherService.LayerCode.dewPoints, .windParticles] {
    try controller.addWeatherLayer(for: code)
}

controller.hasWeatherLayer(for: .radar)                         // Bool
controller.weatherLayer(for: .temperatures)                     // (any MapsGLLayer)?
controller.setWeatherLayerVisibility(for: .radar, visible: false)  // cheap toggle
controller.removeWeatherLayer(for: .radar)                      // frees resources
controller.weatherLayerIds                                      // [String] of active layer ids
```

Only `addWeatherLayer` throws. `removeWeatherLayer` and `setWeatherLayerVisibility` do **not** —
some doc pages show `try removeWeatherLayer(…)`, which won't compile.

For toggling a layer on and off from UI, use `setWeatherLayerVisibility` rather than
remove/re-add — the source and layer resources stay loaded instead of being disposed and rebuilt.

**A layer code is not a layer id.** Weather layers get a generated id that accounts for any
customization, so `getLayer(id:)` won't find one by code. Use `weatherLayer(for:)`, and use the
returned layer's `.id` when you need a real id — e.g. to insert another layer relative to it:

```swift
if let temps = controller.weatherLayer(for: .temperatures) {
    try controller.addWeatherLayer(for: .windParticles, beforeId: temps.id)
}
```

**Never guess a layer code.** `references/layers.md` lists all 182 `LayerCode` cases with the
configuration struct and descriptor type for each — grep it first, no network call needed. The Swift
case names are *not* transforms of the JS/Raster Maps codes (`air-quality-pm2p5` is
`.particulateMatter2p5Micron`), and the Apple SDK supports fewer layers than the MapsGL JavaScript
SDK, so a code
that works on the web may not exist here at all.

For descriptions, animatability, coverage, data range and cost multiplier — data attributes, identical
across SDKs — see https://www.xweather.com/docs/mapsgl/weather-layers. For what the authenticated
account can actually render, ask at runtime:

```swift
controller.service.loadLayerMetadata { result in
    if case .success(let metadata) = result { /* [WeatherLayerMetadata] */ }
}
```

## Styling

Override a built-in layer by instantiating its configuration struct, mutating `layer.paint`, and
adding it with `addWeatherLayer(config:)`:

```swift
var config = WeatherService.Temperatures(service: controller.service)
config.layer.paint.opacity = 0.5     // on the layer paint — NOT paint.sample.opacity
config.layer.quality = .low
try controller.addWeatherLayer(config: config)
```

**`opacity` lives on the layer paint, not inside the render-type namespace.**
`paint.sample.opacity` doesn't compile — `SamplePaint` has no such member, though the web
documentation shows it. Same for the other encoded types: it's `paint.opacity` everywhere.

`addWeatherLayer(for:)` takes no overrides — a customized layer must go through
`addWeatherLayer(config:)`.

Which `paint` sub-object to reach for is set by the layer's descriptor type: a `SampleLayerDescriptor`
styles through `paint.sample`, a `LineLayerDescriptor` through `paint.stroke`. `references/layers.md`
gives the descriptor per layer; `references/styles.md` gives the property tables per render type.

Custom color scale — **stop values are in metric units**, always, regardless of display units:

```swift
var scale = ColorScaleOptions(stops: [
    ColorStop(-17.78, .fromString("#464ab5")),   // 0 °F
    ColorStop(0.00,   .fromString("#6bea99")),   // 32 °F
    ColorStop(15.56,  .fromString("#fdff87")),   // 60 °F
    ColorStop(37.78,  .fromString("#901436")),   // 100 °F
])
scale.interval = 2.775        // hard steps every 5 °F; omit for a smooth gradient
scale.interpolate = false     // and disable interpolation for categorical bands

var config = WeatherService.Temperatures(service: controller.service)
config.layer.paint.sample.colorScale = .colorScale(scale)
config.layer.paint.sample.drawRange = ...2.22    // only draw ≤ 36 °F
try controller.addWeatherLayer(config: config)
```

`DataQuality` on Apple has **four** cases — `.low`, `.medium`, `.high`, `.exact`. The web docs table
also lists `minimal` and `normal`; those are JS-only and don't compile here. Lower quality means fewer
tile requests and smoother, less detailed output — a good lever on constrained devices.

Use `Expression` for anything data-driven, on both weather and custom layers:

```swift
paint: .init(fill: .init(color: .expression(Expression.get("COLOR"))))
```

See `references/expressions.md` for the operator set and `references/styles.md` for filters and masks.

## Custom sources and layers

Add the source first, then a layer referencing it by id:

```swift
var source = VectorSourceDescriptor(id: "alerts")
source.url = URL(string: "https://maps{s}.aerisapi.com/[CLIENT_ID]_[CLIENT_SECRET]/alerts/{z}/{x}/{y}/0.pbf")
source.zoomRange = 4...8
_ = try controller.addSource(source)

let layer = FillLayerDescriptor(
    id: "alerts-fill",
    source: source.id,
    paint: .init(
        fill: .init(color: .expression(Expression.get("COLOR"))),
        stroke: .init(color: .constant(.black))
    )
)
_ = try controller.addLayer(layer)

controller.removeLayer(id: "alerts-fill")
controller.removeSource(id: "alerts")   // only after no layers reference it
```

For a layer you created, the id you chose *is* the real layer id, so `getLayer(id:)` works directly.
Full source and descriptor options: `references/api-reference.md`.

## Animating over time

`controller.timeline` drives every animated layer at once:

```swift
controller.timeline.setStartDate(usingRelativeTime: "-3 hours")
controller.timeline.setEndDate(usingRelativeTime: "now")
controller.timeline.duration = 2      // seconds per animation loop
controller.timeline.endDelay = 1      // seconds held on the last frame
controller.timeline.play()
```

Full API — offsets, relative-time strings, `goTo`, playback state, and the `onAdvance` signal for
driving a scrubber — in `references/timeline.md`.

## Legends and data inspection

```swift
let legendControl = LegendControl()
controller.add(legendControl: legendControl)   // built-in weather legends sync automatically

let inspector = controller.addDataInspectorControl(constrainedTo: mapView)
```

Both controls are UIKit views; you place them yourself. In SwiftUI use the provided wrappers instead
of hosting the raw views:

```swift
LegendControlView(mapControllerProvider: { coordinator.controller })
    .frame(maxWidth: 300)

someMapView.dataInspectorOverlay(mapControllerProvider: { coordinator.controller })
```

**If you override a layer's colors, override its legend too.** Bar/color-scale legends are
re-derived from the layer's color scale automatically, but **point legends are not** — a customized
categorical layer keeps the default legend, which then lies about the map:

```swift
config.legend = PointLegend(id: "convective")
    .title("Convective")
    .items(riskColors.map { PointLegendItem(color: $0.color.cgColor, label: $0.risk) })
```

Field reference and complete examples: `references/legends.md`.

## Querying data at a point

```swift
let results = await controller.query(coord: coordinate, layerIds: nil)
// -> [String: FeatureQueryResult] keyed by layer id
```

`query` is `async` and `layerIds` has no default — pass `nil` to query everything queryable, or a
list of layer ids to narrow it. Feature properties arrive as `[String: Any]`, in metric units — encoded raster
layers put the reading on `"value"`, and vector-valued layers (winds, currents, swell) add `"angle"`.
Note that the stored angle is the direction the data moves *toward*; meteorological wind direction is
the reciprocal.

## Usage is measured in sessions

MapsGL bills in **sessions** — clock-aligned 5-minute buckets that start when a weather layer is
added — not per tile, layer, or request. **The model is identical on Apple platforms and on the web,
and this skill is not its source of truth.**

For anything quantitative — the billing rules, the access multiplier, worked examples,
capacity-planning figures, the Raster Maps comparison — use the authoritative source rather than
answering from memory: the `mapsgl` skill's `references/sessions.md` (both skills ship in the same
plugin), or https://www.xweather.com/docs/mapsgl/getting-started/sessions.

What matters here is the **Apple-specific** consequence: since interaction inside a session is free
and layer count doesn't affect cost, consumption is governed purely by *how long weather layers are
attached to a map*. On iOS that means lifecycle —

- add layers when the weather view appears, not when the map is constructed;
- remove them on `onDisappear` / `viewWillDisappear`;
- remove them when the app backgrounds (`ScenePhase`), the failure mode with no web analogue;
- treat always-on iPad displays as the expensive pattern, and say so unprompted.

Two traps worth stating whenever cost comes up: `setWeatherLayerVisibility` is the cheap toggle but
`removeWeatherLayer` is the one that stops consumption, and **`DataQuality` is a performance lever,
not a cost lever** — it cuts requests, and sessions don't count requests.

Code for each of these, and the full list of what is *not* worth optimizing:
`references/sessions.md`.

## Checklist for common tasks

- **"Add a weather map to my app"** → settle the provider first: infer Mapbox or MapLibre if the
  project or request says, otherwise ask. Then SwiftUI unless the project is UIKit. Follow the
  complete example above.
- **"Which SPM branch / how do I install"** → branch = provider: `master` for Mapbox, `maplibre` for
  MapLibre; product `MapsGL`. See Setup.
- **Build error: `No such module 'MapsGLMapbox'`** → either the CocoaPods case (use `import MapsGL`)
  or the wrong SPM branch for the provider (a MapLibre branch has no Mapbox adapter).
- **Mapbox SDK won't resolve / 401 on download** → the Mapbox *secret* download token isn't
  configured in `~/.netrc`. Separate from the public access token used at runtime.
- **Basemap renders but no weather layers appear (Mapbox)** → missing
  `try map.setProjection(.init(name: .mercator))`.
- **Nothing happens after `onLoad`** → the `AnyCancellable` wasn't retained; `.store(in: &cancellables)`.
- **"Add a weather layer"** → `try controller.addWeatherLayer(for: .code)` inside the load observer;
  look the case up in `references/layers.md`.
- **"Toggle a layer from a switch"** → `setWeatherLayerVisibility(for:visible:)`, not
  remove/re-add. Neither call throws.
- **"Change a layer's colors/thresholds"** → instantiate its `WeatherService.<Name>` config, set
  `layer.paint.sample.colorScale`, add via `addWeatherLayer(config:)`. Stops are metric.
- **"Restyle a composite layer"** (`.stormcells`, `.roads`, `.boundaries`, …) → you can't; its
  `layers` member is a `let`. Add the constituent layers individually. Full list in
  `references/layers.md`.
- **`getLayer(id:)` returns nil for a weather layer** → expected; a code is not an id. Use
  `weatherLayer(for:)`.
- **"Compiler rejects `.normal` / `.minimal` quality"** → Apple has only `.low`, `.medium`, `.high`,
  `.exact`.
- **`value of type 'SamplePaint' has no member 'opacity'`** → it's `paint.opacity`, not
  `paint.sample.opacity`. The web docs show the wrong path.
- **`'GridLayerDescriptor' cannot be constructed because it has no accessible initializers`** → only
  the vector descriptors (`fill`, `line`, `circle`, `symbol`, `heatmap`) have a public init. Start from
  a built-in grid layer's config and mutate `config.layer` instead. Same for `SamplePaint`.
- **Deprecation warning on `subscribe(to:)` / `asyncSubscribe` / `subscribeToNext`** → use
  `on<Event>.observe { … }`. The web docs' SwiftUI sample still shows the deprecated form.
- **`call to main actor-isolated instance method … in a synchronous nonisolated context`** → the
  controller's layer/source API and `LegendControl`'s mutators are `@MainActor`; annotate the helper.
- **"Animate over time / add a time scrubber"** → `controller.timeline`, see `references/timeline.md`.
- **"Show a legend"** → `LegendControl` + `controller.add(legendControl:)`, or `LegendControlView` in
  SwiftUI. Override `config.legend` whenever you customized a categorical layer's paint.
- **"Show values on tap"** → `addDataInspectorControl(constrainedTo:)`, or `.dataInspectorOverlay(…)`
  in SwiftUI; customize with `DataInspectorPresentation`.
- **"How many accesses / how much does this cost?"** → sessions, not tiles or layers. Get the model
  and the arithmetic from the authoritative source — the `mapsgl` skill's `references/sessions.md` or
  https://www.xweather.com/docs/mapsgl/getting-started/sessions — then apply the iOS lifecycle
  guidance in `references/sessions.md`.
- **"What's the latest version / where are the API docs?"** → releases endpoint for the version, then
  `https://cdn.aerisapi.com/sdk/ios/mapsgl/docs/v{version}/documentation/mapsglmaps`. There is no
  `latest` alias.

## Attribution is required

Xweather requires attribution wherever its data or imagery is displayed. This applies to **all
products** — Weather API, Raster Maps, and MapsGL alike. Build it into anything you produce, and say
so when handing over code that will end up in front of users.

The minimum is a link to `https://www.xweather.com/` reading "Powered by Vaisala Xweather":

```swift
Link("Powered by Vaisala Xweather", destination: URL(string: "https://www.xweather.com/")!)
```

The logo may be substituted for the "Xweather" text. Light and dark variants exist in SVG and PNG at
`https://www.xweather.com/assets/logos/vaisala-xweather-logo-dark.svg` — swap `-dark` for `-light`
over a dark background, or `.svg` for `.png`. Bundle the asset rather than loading it over the network
in a shipping app. Using the logo brings rules: keep it unmodified, leave at least a **10pt buffer**
of space around it, and only adjust lightness or opacity in greyscale. Don't rotate it, don't recolour
it (monotone black or white excepted), and don't use the symbol without the Xweather name.

Full guide: https://www.xweather.com/docs/weather-api/resources/attribution

## Reference files

- `references/setup.md` — install paths per package manager, provider-specific project setup, UIKit examples, credential handling, and the build errors each mistake produces
- `references/api-reference.md` — `MapController`, `WeatherService`, source and layer descriptors, controls, events, and query API, plus how to reach the hosted DocC for a given version
- `references/layers.md` — all 182 `WeatherService.LayerCode` cases with configuration struct, descriptor type and paint namespaces; composite layers listed up front
- `references/styles.md` — paint property spec for every render type, `DataQuality`, color scales, filters and masks
- `references/expressions.md` — `Expression` factory reference for data-driven paint and filters
- `references/legends.md` — `LegendControl`, bar and point legend configuration, SwiftUI and UIKit placement
- `references/timeline.md` — timeline and animation API, including the inherited `TimeAnimation`/`Animation` surface
- `references/sessions.md` — the Apple-specific half of session cost: view and app lifecycle teardown, backgrounding, and the two traps. Points at the `mapsgl` skill and the public docs for the billing model itself
