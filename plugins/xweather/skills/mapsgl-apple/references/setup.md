# MapsGL Apple SDK — installation and project setup

Source of truth: https://www.xweather.com/docs/mapsgl-apple-sdk/getting-started and the distribution
repo https://github.com/vaisala-xweather/mapsgl-apple-sdk.

## Requirements

| | |
|---|---|
| Platforms | iOS 16+, iPadOS 16+, Mac Catalyst 16+, visionOS 1+ |
| Language | Swift 5.9+ (`swift-tools-version: 5.9`) |
| Xcode | 15 or later |
| Rendering | Metal — the Simulator works, but device testing is worth doing early |
| Account | Active Xweather **Weather API and Maps** subscription |
| Map provider | Mapbox Maps 11.x **or** MapLibre Native for iOS 6.18.0+ |

There is **no native macOS (AppKit) target**. The manifest declares `.iOS`, `.macCatalyst`, and
`.visionOS` only, so a Mac build means Mac Catalyst. The docs' "macOS" phrasing refers to that.

The SDK ships as three binary xcframeworks plus one open Swift adapter per provider:

| Component | Form | Role |
|---|---|---|
| `MapsGLCore` | xcframework | Shared primitives, events, authentication |
| `MapsGLRenderer` | xcframework | Metal rendering |
| `MapsGLMaps` | xcframework | Public API — `MapController`, `WeatherService`, descriptors, controls, legends |
| `MapsGLMapbox` | Swift source | Mapbox adapter — `MapboxMapController` |
| `MapsGLMapLibre` | Swift source | MapLibre adapter — `MapLibreMapController` |

`turf-swift` is a transitive dependency of `MapsGLMaps` and is resolved for you.

## The provider decision comes first

The two providers are **not** a runtime switch. They resolve different Swift Package branches,
different transitive SDKs, and different map-view types, so changing it later means redoing the
package graph. Settle it before writing code: infer the provider when the project or request tells
you, and ask when it doesn't (see the SKILL.md rule).

| | Mapbox Maps | MapLibre Native |
|---|---|---|
| Controller | `MapboxMapController` | `MapLibreMapController` |
| Adapter module | `MapsGLMapbox` | `MapsGLMapLibre` |
| Map view type | `MapboxMaps.MapView` / `MapboxMaps.MapboxMap` | `MLNMapView` |
| SPM branch | `master` (or `release/x.y.z`) | `maplibre` (or `release/maplibre/x.y.z`) |
| Transitive SDK | `mapbox-maps-ios` `11.0.0..<12.0.0` | `maplibre-gl-native-distribution` 6.18.0+ |
| Runtime credential | `MapboxOptions.accessToken` (public token) | none |
| Build credential | Mapbox **secret** download token in `~/.netrc` | none |
| SwiftUI | Native `Map` + `MapReader` | Wrap `MLNMapView` in `UIViewRepresentable` |
| Extra constraint | Must set the mercator projection | none |

## Swift Package Manager

Preferred. In Xcode: **File ▸ Add Package Dependencies…**, enter
`https://github.com/vaisala-xweather/mapsgl-apple-sdk`, choose the **branch for your provider**, and
add the `MapsGL` library product to your app target.

```
master                    → latest Mapbox channel
maplibre                  → latest MapLibre channel
release/x.y.z             → pinned Mapbox release line
release/maplibre/x.y.z    → pinned MapLibre release line
```

The product name is `MapsGL` on every branch. What differs is which adapter target that product
includes — which is why a MapLibre branch genuinely has no `MapsGLMapbox` module to import, and vice
versa.

**Prefer a branch channel over a pin** unless the user asked for reproducible resolution. Branch
channels track the current release without hardcoding a version anywhere. When pinning is wanted,
resolve the version rather than guessing it:

```bash
curl -s https://www.xweather.com/docs/api/releases/versions \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["products"]["mapsgl-apple-sdk"]["version"])'
```

In a `Package.swift` of your own, the branch form is:

```swift
dependencies: [
    .package(url: "https://github.com/vaisala-xweather/mapsgl-apple-sdk.git", branch: "master"),
],
targets: [
    .target(name: "MyApp", dependencies: [
        .product(name: "MapsGL", package: "mapsgl-apple-sdk"),
    ]),
]
```

## CocoaPods

```ruby
target 'MyApp' do
  use_frameworks!
  pod 'MapsGL'
end
```

Then `pod install`, and open the generated `.xcworkspace` (not the `.xcodeproj`).

**CocoaPods builds a single module named `MapsGL`.** So in every source file:

```swift
import MapsGLMaps
import MapsGL      // replaces `import MapsGLMapbox` / `import MapsGLMapLibre`
```

Mixing the two conventions is the most common CocoaPods failure here — `No such module
'MapsGLMapbox'` in a CocoaPods project almost always means an SPM-shaped import survived.

## Carthage

```
github "vaisala-xweather/mapsgl-apple-sdk" ~> x.y.z
```

```bash
carthage update --use-xcframeworks
```

Then:

1. Add the provider SDK to the project yourself (Mapbox 11+ per Mapbox's instructions, or MapLibre
   Native for iOS).
2. Add every xcframework from `Carthage/Build` under **General ▸ Frameworks, Libraries, and Embedded
   Content**.
3. Download `MapsGL.zip` from the releases page, extract it, and add the **adapter source directory**
   for your provider (`MapsGLMapbox/` or `MapsGLMapLibre/`) to the app target.

Because the adapter is compiled into your own module, **remove `import MapsGLMapbox` /
`import MapsGLMapLibre`** from your sources — the types are already in scope, and the import won't
resolve.

## Manual xcframework embedding

1. Add the provider SDK to the project yourself.
2. Download and extract `MapsGL.zip` from
   https://github.com/vaisala-xweather/mapsgl-apple-sdk/releases, giving
   `MapsGLCore.xcframework`, `MapsGLRenderer.xcframework`, `MapsGLMaps.xcframework`, and the two
   adapter source directories.
3. Add the three xcframeworks under **General ▸ Frameworks, Libraries, and Embedded Content**, setting
   each to **Embed & Sign**.
4. Add the adapter source directory for your provider to the app target — and again, drop the adapter
   `import`.

`Embed & Sign` matters: `Do Not Embed` builds fine and then crashes at launch with a dyld
"Library not loaded" error.

## Credentials

### Xweather

Client id and secret from https://data.portal.xweather.com/account/keys, passed as:

```swift
XweatherAccount(id: clientID, secret: clientSecret)
```

### Mapbox — two different tokens

This trips people up because the two are used at different times:

| Token | Where | When |
|---|---|---|
| **Public** access token (`pk.…`) | `MapboxOptions.accessToken` in code, or `MBXAccessToken` in Info.plist | Runtime, to load basemap tiles |
| **Secret** download token (`sk.…`) | `~/.netrc`, `machine api.mapbox.com` | Build time, so SPM/CocoaPods can download the Mapbox SDK at all |

Without the secret token, package resolution fails with a 401 before any code compiles. Without the
public token, the app builds and shows a blank/erroring basemap.

Set the public token once, before any map view is created:

```swift
@main
struct MyApp: App {
    init() {
        MapboxOptions.accessToken = AccessKeys.shared.mapboxAccessToken
    }
    var body: some Scene { WindowGroup { WeatherMapView() } }
}
```

### MapLibre

No SDK credential. The basemap comes from whatever `styleURL` you point at, and that provider may or
may not require a key. CARTO's public styles need none and are what the demo app uses:

```
https://basemaps.cartocdn.com/gl/positron-gl-style/style.json      (light)
https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json   (dark)
```

### Keeping keys out of the repository

Never commit real keys, and never inline them in a shipping app's source. Follow whatever the project
already does. If it has no convention, the demo app's pattern is a reasonable default: a gitignored
`AccessKeys.plist` with a checked-in `AccessKeys-Sample.plist` template, read through a small
accessor type. An xcconfig with `.gitignore`d overrides works equally well. For anything
user-specific, use the keychain.

In generated examples, write obvious placeholders — `"FILL_IN_WITH_YOUR_CLIENT_ID"` — so a forgotten
substitution fails loudly instead of looking like a real key.

## Provider-specific project setup

### Mapbox: the mercator projection is required

Mapbox's current styles (streets / outdoor / satellite-streets v12, light / dark v11) default to the
**globe** projection, which MapsGL cannot render onto given current Mapbox GL SDK limits. Set mercator
on every Mapbox map you attach a controller to:

```swift
try map.setProjection(.init(name: .mercator))          // MapboxMap, e.g. from MapReader's proxy
try mapView.mapboxMap.setProjection(.init(name: .mercator))   // MapView
```

Symptom when missing: the basemap renders perfectly and MapsGL layers never appear — no error, no
warning.

### MapLibre: Metal backend

The MapsGL MapLibre adapter target is compiled with `MLN_RENDER_BACKEND_METAL`, so use the
Metal-capable MapLibre Native distribution (6.18.0+, which the package resolves). Nothing to configure
in the app target.

### Frame rate

The demo app raises the preferred frame rate range, which noticeably smooths particle and animated
layers on high-refresh displays:

```swift
// UIKit
let maxFPS = Float(UIScreen.main.maximumFramesPerSecond)
mapView.preferredFrameRateRange = .init(minimum: maxFPS * 2 / 3, maximum: maxFPS, preferred: maxFPS)

// SwiftUI, Mapbox
Map(initialViewport: viewport)
    .frameRate(range: (maxFPS * 2 / 3)...maxFPS, preferred: maxFPS)
```

## UIKit setup

### Mapbox

```swift
import UIKit
import Combine
import MapboxMaps
import MapsGLMaps
import MapsGLMapbox

final class WeatherMapViewController: UIViewController {
    private var mapView: MapboxMaps.MapView!
    private var controller: MapboxMapController!
    private var cancellables: Set<AnyCancellable> = []

    override func viewDidLoad() {
        super.viewDidLoad()

        let options = MapInitOptions(
            cameraOptions: CameraOptions(
                center: CLLocationCoordinate2D(latitude: 39.65, longitude: -93.10),
                zoom: 3.5
            ),
            styleURI: .light
        )
        mapView = MapboxMaps.MapView(frame: view.bounds, mapInitOptions: options)
        try! mapView.mapboxMap.setProjection(.init(name: .mercator))
        mapView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(mapView)

        controller = MapboxMapController(
            map: mapView,
            account: XweatherAccount(id: clientID, secret: clientSecret)
        )

        controller.onLoad.observe { [weak self] _ in
            guard let self else { return }
            do {
                try self.controller.addWeatherLayer(for: .radar)
            } catch {
                NSLog("Failed to add weather layer: \(error)")
            }
        }.store(in: &cancellables)
    }
}
```

`MapboxMapController(map:account:)` accepts a `MapView` directly — it reads `mapboxMap` and `window`
off it. The `init(map:window:account:)` form taking a `MapboxMap` is for cases where you only have the
map object, which is what SwiftUI's `MapReader` proxy hands you.

### MapLibre

```swift
import UIKit
import Combine
import MapLibre
import MapsGLMaps
import MapsGLMapLibre

final class WeatherMapViewController: UIViewController {
    private var mapView: MLNMapView!
    private var controller: MapLibreMapController!
    private var cancellables: Set<AnyCancellable> = []

    override func viewDidLoad() {
        super.viewDidLoad()

        mapView = MLNMapView(frame: view.bounds)
        mapView.styleURL = URL(string: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json")!
        mapView.setCenter(
            CLLocationCoordinate2D(latitude: 39.65, longitude: -93.10),
            zoomLevel: 3.5,
            animated: false
        )
        mapView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(mapView)

        controller = MapLibreMapController(
            map: mapView,
            account: XweatherAccount(id: clientID, secret: clientSecret)
        )

        controller.onLoad.observe { [weak self] _ in
            _ = try? self?.controller.addWeatherLayer(for: .radar)
        }.store(in: &cancellables)
    }
}
```

## Placing weather layers under basemap labels

Weather layers added with no `beforeId` go on top of everything, including street and place labels.
Both demo channels compute an insertion point — the first symbol layer that draws text — and pass it
as `beforeId`:

```swift
// Mapbox
let labelLayerId = controller.map.allLayerIdentifiers.first { layer in
    layer.type == .symbol
        && !(controller.map.layerProperty(for: layer.id, property: "text-field").value is NSNull)
}?.id

// MapLibre
let labelLayerId = controller.map.style?.layers
    .compactMap { $0 as? MLNSymbolStyleLayer }
    .first { $0.text != nil }?
    .identifier

try controller.addWeatherLayer(for: .radar, beforeId: labelLayerId)
```

Worth offering unprompted for any opaque fill or sample layer — radar over unreadable labels is the
most common "looks wrong" complaint.

## Build and runtime failures, and what causes them

| Symptom | Cause |
|---|---|
| `No such module 'MapsGLMapbox'` | CocoaPods (use `import MapsGL`), the adapter source added directly (drop the import), or the MapLibre SPM branch (no Mapbox adapter exists on it) |
| `No such module 'MapsGLMapLibre'` | Same, mirrored — usually the `master`/Mapbox branch |
| Package resolution fails, 401 from `api.mapbox.com` | Mapbox secret download token missing from `~/.netrc` |
| dyld: Library not loaded: `MapsGLMaps` | Manual embedding with `Do Not Embed` instead of `Embed & Sign` |
| Basemap renders, weather layers never appear (Mapbox) | Globe projection — call `setProjection(.init(name: .mercator))` |
| Nothing happens inside `onLoad` | The returned `AnyCancellable` wasn't retained; `.store(in: &cancellables)` |
| Layers appear then vanish, or controller stops responding | The `MapController` isn't retained — hold it in a coordinator/view model, not a local |
| `Cannot find '.normal'` / `'.minimal'` in `DataQuality` | JS-only cases; Apple has `.low`, `.medium`, `.high`, `.exact` |
| `try` on `removeWeatherLayer` won't compile | It doesn't throw; only `addWeatherLayer`, `addLayer`, `addSource`, and `addImage` do |
| `value of type 'SamplePaint' has no member 'opacity'` | Opacity is `paint.opacity`, not `paint.sample.opacity` — the web docs show the wrong path |
| `'GridLayerDescriptor' cannot be constructed because it has no accessible initializers` | Only vector descriptors have a public init; build grid/sample/particle/contour/raster layers from a built-in weather layer's config. Same for `SamplePaint` |
| Deprecation warning on `subscribe(to:)`, `asyncSubscribe`, `subscribeToNext` | Replaced by `on<Event>.observe { … }`. The web docs' SwiftUI sample still uses the deprecated call |
| `call to main actor-isolated instance method … in a synchronous nonisolated context` | The controller's layer/source API and `LegendControl`'s mutators are `@MainActor` — annotate the calling function |
| Radar/satellite drawn over street labels | No `beforeId` — see above |
