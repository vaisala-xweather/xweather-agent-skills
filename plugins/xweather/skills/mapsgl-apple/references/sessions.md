# MapsGL session cost on Apple platforms

**The billing model is not Apple-specific and is not documented here.** MapsGL bills in sessions —
clock-aligned 5-minute buckets, one session per data request minimum, unlimited interaction inside a
session — identically on iOS and on the web.

For the model itself — the three rules, worked examples, the expected-sessions table and
capacity-planning formula, the MapsGL vs. Raster Maps comparison, and how to answer a "how many
accesses?" question — use the authoritative sources, in this order:

1. **The `mapsgl` skill's `references/sessions.md`**, if that skill is available. It is the maintained
   copy; both skills ship in the same `xweather` plugin, so it usually is.
2. **https://www.xweather.com/docs/mapsgl/getting-started/sessions** — the public documentation the
   above is derived from.

Don't reconstruct the model from memory, and don't answer a cost question from this file alone. It
carries no multiplier, no worked arithmetic, and no planning figures — deliberately, so it cannot
drift from the source of truth.

The two facts the rest of this page rests on:

- a session is up to **5 minutes**, aligned to wall-clock boundaries (`:00`, `:05`, `:10`), and starts
  when a weather layer is added;
- **inside a session, layer count and interaction are free** — panning, zooming, animating,
  toggling layers, refreshing.

Everything below is the part that *is* Apple-specific: how that model interacts with view and app
lifecycle.

## The only lever is when layers are attached

Because a session starts when a layer is added and everything inside it is free, consumption is
governed by *how long weather layers are on a map*, not by what the user does with them. On Apple
platforms that maps onto lifecycle events, which is where the SDK-specific work lives.

### Defer until the user asks

A controller created with no weather layer starts no session. Add layers when the weather view
appears or a toggle is switched on, not when the map is constructed:

```swift
// Adding layers here — not in makeUIView / init — avoids charging users
// who never reach the weather screen.
.onAppear { addWeatherLayers() }
```

### Tear down when the map leaves the screen

```swift
.onDisappear {
    for code in activeCodes { controller.removeWeatherLayer(for: code) }
}
```

UIKit equivalent: `viewWillDisappear`. Covers tab switches, navigation pushes, and sheet dismissals —
all cases where an iOS map stays alive and attached while invisible, which a web page's unload would
have handled for you.

### Handle backgrounding

This is the mobile failure mode with no web analogue: an app suspended on the weather tab keeps
layers attached. Watch `ScenePhase` (or
`UIApplication.didEnterBackgroundNotification` in UIKit):

```swift
@Environment(\.scenePhase) private var scenePhase
// …
.onChange(of: scenePhase) { phase in
    switch phase {
    case .background: removeWeatherLayers()
    case .active:     addWeatherLayers()
    default:          break
    }
}
```

Without this, a user who leaves the app open and pockets the phone looks exactly like an unattended
kiosk display.

### Always-on iPad displays are the expensive shape

An iPad kiosk or wall display left on a weather view accrues sessions continuously, whether or not
anyone is watching. Worth raising unprompted whenever the request describes a kiosk, an
operations-centre screen, or a display app: a scheduled teardown outside operating hours cuts
consumption proportionally.

## Two Apple-specific traps

**`removeWeatherLayer` vs. `setWeatherLayerVisibility`.** They are not interchangeable for cost
purposes:

| | Use for | Resources |
|---|---|---|
| `setWeatherLayerVisibility(for:visible:)` | A UI switch the user flips repeatedly | Kept loaded — cheap to reverse, but visibility and data fetching are not necessarily the same thing |
| `removeWeatherLayer(for:)` | A screen going away, or backgrounding | Disposed — this is the one to use when the goal is to stop consuming |

Reaching for visibility on `onDisappear` because it's "lighter" is the mistake; it's lighter on the
device, not necessarily on the bill.

**`DataQuality` is not a cost lever.** Lowering `layer.quality` to `.low` reduces tile requests,
bandwidth, and memory — all real wins on a phone — but session billing does not count requests, so it
will not reduce accesses. Recommend it for performance and cellular-data reasons, and don't present it
as a cost optimization.

Similarly, nothing about particle density, animation `duration`, timeline scrubbing, or the number of
layers a user enables affects session cost. Optimize those for frame rate and clarity only.
