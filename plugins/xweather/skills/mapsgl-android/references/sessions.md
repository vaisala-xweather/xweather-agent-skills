# MapsGL session cost on Android

MapsGL does not bill per tile, per layer, or per HTTP request. It bills in **sessions**, and the
model is not Android-specific - it is identical on Android, on Apple platforms, and on the web.

The maintained copy of the model lives in the `mapsgl` skill's `references/sessions.md`; both skills
ship in the same `xweather` plugin, so it is usually available, and it carries longer tables and the
Raster Maps comparison. The public documentation it derives from is
https://www.xweather.com/docs/mapsgl/getting-started/sessions. Prefer either over memory.

Enough of the model is repeated below to answer a cost question without them, because this skill can
be installed on its own.

## The three rules that decide the number

**1. Sessions align to the wall clock, not to when the user arrived.** Boundaries fall on clock
times divisible by 5 - `:00`, `:05`, `:10`, `:15`. A session is *not* a rolling five-minute window
starting at first interaction. This is the most misunderstood part of the model: **elapsed viewing
time doesn't determine the count, the number of 5-minute buckets touched does.**

**2. At least one session per MapsGL data request.** No proration. Adding one layer and immediately
finishing the Activity still costs a full session, so 150 accesses is the floor for any use at all.

**3. Inside a session, everything is free.** Panning, zooming, timeline animation, refreshing,
toggling layers. **Layer count does not multiply cost** - eight layers cost exactly what one costs.

On a **Weather API and Maps** subscription, MapsGL carries a **150x multiplier**:

```
1 MapsGL session (5 minutes) = 150 accesses
```

## Worked examples

Radar viewed **8:03-8:07** straddles the `:05` boundary:

```
8:00-8:05 bucket  -> session 1
8:05-8:10 bucket  -> session 2
                     2 sessions = 300 accesses
```

The same four minutes from **8:05-8:09** sits inside one bucket -> **1 session = 150 accesses**.
Identical elapsed time, half the billing, purely from where it fell on the clock.

## Estimating the average for capacity planning

For a view of `d` minutes starting at a uniformly random time, the expected number of sessions is:

```
expected sessions = floor(d / 5) + 1 + (d mod 5) / 5
```

Not `d / 5`, and not `ceil(d / 5)` - both understate it, because any view that isn't exactly
bucket-aligned touches one more bucket than its duration suggests.

| View duration | Expected sessions | Expected accesses |
|---|---|---|
| 30 seconds | 1.1 | 165 |
| 1 minute | 1.2 | 180 |
| 4 minutes | 1.8 | 270 |
| 5 minutes | 2.0 | 300 |
| 6 minutes | 2.2 | 330 |
| 10 minutes | 3.0 | 450 |
| 30 minutes | 7.0 | 1,050 |
| 45 minutes | 10.0 | 1,500 |

Use these for forecasting rather than the best case; assuming 150 accesses per short view
underestimates by roughly 10-20%.

**Many short visits are the expensive shape.** 100 users opening a map for 30 seconds each costs
~110 sessions (~16,500 accesses); 100 users viewing for a full 5 minutes costs ~200 sessions
(~30,000). Ten times the engagement for under twice the cost - MapsGL charges nearly full price for
drive-by launches.

## The only lever is when layers are attached

A session starts when a weather layer is added and everything inside it is free, so consumption is
governed by *how long weather layers are on a map* - not by what the user does with them. On Android
that maps onto the Activity/Fragment lifecycle, which is where the platform-specific work lives.

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

`onStop` is the right hook because it fires when the Activity stops being visible - the user pressing
Home, switching apps, or navigating to another Activity. `onDestroy` is too late and is not
guaranteed to run at all. This is the mobile failure mode with no web analogue: an app left open on
the weather screen and pocketed keeps layers attached and keeps accruing sessions, looking exactly
like an unattended kiosk.

### Configuration changes recreate the Activity

A rotation or a day/night switch destroys and recreates the Activity by default, which tears down and
rebuilds the controller. That does not multiply cost the way it might appear to - the rebuilt map
lands in the same wall-clock bucket, and buckets are what bill. Don't add `configChanges` handling for
cost reasons; do it for state and performance reasons if at all.

### Always-on displays are the expensive shape

A tablet kiosk or operations-centre screen left on a weather view accrues sessions continuously
whether or not anyone is watching:

```
8-hour shift = 480 minutes / 5 = 96 sessions
96 x 150 = 14,400 accesses per display per shift
```

Worth raising unprompted whenever a request describes a kiosk, a wall display, or a
`FLAG_KEEP_SCREEN_ON` weather view. A scheduled teardown outside operating hours cuts it
proportionally.

## Two Android traps

**`removeWeatherLayer` vs `setWeatherLayerVisibility`.** Not interchangeable for cost purposes:

| | Use for | Resources |
|---|---|---|
| `setWeatherLayerVisibility(code, visible)` | A UI switch the user flips repeatedly | Kept loaded - cheap to reverse, but visibility and data fetching are not necessarily the same thing |
| `removeWeatherLayer(code)` | `onStop`, or a screen going away | Disposed - this is the one to use when the goal is to stop consuming |

Reaching for visibility in `onStop` because it's "lighter" is the mistake: it's lighter on the
device, not necessarily on the bill.

**`DataQuality` is not a cost lever.** Lowering a descriptor's `quality` from `DataQuality.exact`
toward `DataQuality.low` reduces tile requests, bandwidth, and memory - all real wins on a phone, and
worth recommending on cellular. But session billing does not count requests, so it will not reduce
accesses. Don't present it as a cost optimization.

The same goes for particle density, animation duration, timeline scrubbing, and how many layers the
user enables. Optimize those for frame rate, memory, and clarity only.

## Answering usage questions

Report the arithmetic, not just a number: **buckets -> sessions -> accesses**. Note when a duration
straddles a boundary, and give a range rather than a single figure when the start time is unknown -
a 45-minute view costs 9 sessions (1,350 accesses) if it starts exactly on a boundary and 10 (1,500)
otherwise, so 1,500 is the number to plan for.

Two cautions:

- **The 150x multiplier applies to a Weather API and Maps subscription**, which is what the docs
  describe. Other plan shapes may count MapsGL differently - for a specific allowance, point the user
  at their account dashboard or account executive rather than extrapolating.
- **Session counts are a usage metric, not a rendering constraint.** Nothing about sessions changes
  what the map can do, and a session expiring does not interrupt the user.
