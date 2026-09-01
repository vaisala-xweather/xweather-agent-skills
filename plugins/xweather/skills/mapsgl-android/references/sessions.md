# MapsGL session cost on Android

**The billing model is not Android-specific and is not documented here.** MapsGL bills in sessions -
clock-aligned 5-minute buckets, one session per data request minimum, unlimited interaction inside a
session - identically on Android, on Apple platforms, and on the web.

For the model itself - the rules, worked examples, the access multiplier, the expected-sessions table
and capacity-planning formula, the MapsGL vs Raster Maps comparison, and how to answer a "how many
accesses?" question - use the authoritative sources, in this order:

1. **The `mapsgl` skill's `references/sessions.md`**, if that skill is available. It is the maintained
   copy; both skills ship in the same `xweather` plugin, so it usually is.
2. **https://www.xweather.com/docs/mapsgl/getting-started/sessions** - the public documentation the
   above is derived from.

Don't reconstruct the model from memory, and don't answer a cost question from this file alone. It
carries no multiplier, no worked arithmetic, and no planning figures - deliberately, so it cannot
drift from the source of truth.

The two facts the rest of this page rests on:

- a session is up to **5 minutes**, aligned to wall-clock boundaries (`:00`, `:05`, `:10`), and starts
  when a weather layer is added;
- **inside a session, layer count and interaction are free** - panning, zooming, animating over the
  timeline, toggling layers, refreshing.

Everything below is the part that *is* Android-specific: how that model interacts with the Activity
and Fragment lifecycle.

## The only lever is when layers are attached

Because a session starts when a layer is added and everything inside it is free, consumption is
governed by *how long weather layers are on a map*, not by what the user does with them. On Android
that maps onto lifecycle callbacks, which is where the SDK-specific work lives.

### Defer until the user asks

A `MapboxMapController` created with no weather layer starts no session. Add layers when the weather
UI is actually reached or a toggle is switched on, not in `onCreate` alongside controller
construction:

```kotlin
// In the toggle handler or when the weather view is shown - not at construction.
controller.addWeatherLayer(LayerCode.RADAR)
```

That avoids charging users who open the app and never reach the weather screen.

### Tear down in onStop, not onDestroy

```kotlin
override fun onStop() {
    super.onStop()
    activeCodes.forEach { controller.removeWeatherLayer(it) }
}

override fun onStart() {
    super.onStart()
    if (weatherVisible) activeCodes.forEach { controller.addWeatherLayer(it) }
}
```

`onStop` fires when the Activity stops being visible - Home pressed, app switched, another Activity
navigated to. `onDestroy` is too late and is not guaranteed to run at all. In a Fragment, use
`onStop` on the Fragment, or `viewLifecycleOwner` if you are observing lifecycle state.

This is the mobile failure mode with no web analogue: an app left open on the weather screen and
pocketed keeps layers attached and keeps accruing sessions, looking exactly like an unattended
display. A web page's unload would have handled this for you.

### Configuration changes are not a cost concern

A rotation or a day/night switch destroys and recreates the Activity by default, tearing down and
rebuilding the controller. That looks alarming but does not multiply cost: the rebuilt map lands in
the same wall-clock bucket, and buckets are what bill. Don't add `configChanges` handling for cost
reasons - do it for state and performance reasons if at all.

### Always-on displays are the expensive shape

A tablet kiosk, wall display, or any weather view holding `FLAG_KEEP_SCREEN_ON` accrues sessions
continuously, whether or not anyone is watching. Worth raising unprompted whenever the request
describes a kiosk, an operations-centre screen, or a display app: a scheduled teardown outside
operating hours cuts consumption proportionally.

## Two Android traps

**`removeWeatherLayer` vs `setWeatherLayerVisibility`.** They are not interchangeable for cost
purposes:

| | Use for | Resources |
|---|---|---|
| `setWeatherLayerVisibility(code, visible)` | A UI switch the user flips repeatedly | Kept loaded - cheap to reverse, but visibility and data fetching are not necessarily the same thing |
| `removeWeatherLayer(code)` | `onStop`, or a screen going away | Disposed - this is the one to use when the goal is to stop consuming |

Reaching for visibility in `onStop` because it's "lighter" is the mistake; it's lighter on the
device, not necessarily on the bill.

**`DataQuality` is not a cost lever.** Lowering a descriptor's `quality` from `DataQuality.exact`
toward `DataQuality.low` reduces tile requests, bandwidth, and memory - all real wins on a phone, and
worth recommending on cellular. But session billing does not count requests, so it will not reduce
accesses. Recommend it for performance and data-usage reasons, and don't present it as a cost
optimization.

Similarly, nothing about particle density, animation duration, timeline scrubbing, or the number of
layers a user enables affects session cost. Optimize those for frame rate, memory, and clarity only.
