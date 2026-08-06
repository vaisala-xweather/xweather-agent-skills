# Timeline & animation - MapsGL Android

Verified against SDK `Timeline` / `AnimationOptions` / `AnimationEvent` (1.6.x).
Docs pages are secondary if they disagree:
https://www.xweather.com/docs/mapsgl-android-sdk/getting-started/animating-data ,
https://www.xweather.com/docs/mapsgl-android-sdk/reference/timeline\r\n\r\n## Playback

```kotlin
controller.timeline.play()
controller.timeline.pause()
controller.timeline.resume()
controller.timeline.stop()
controller.timeline.restart()
controller.timeline.reset()
controller.timeline.toggle()
controller.timeline.playFromDate(fromDate)
controller.timeline.goTo(0.5)                 // normalized 0..1
controller.timeline.goToDate(someDate)
controller.timeline.goToOffset(3600 * 1000L)  // ms after start
```

## Time range

Prefer **`timeline.start` / `timeline.end`** (`Date`) on 1.6.x:

```kotlin
controller.timeline.start = calendarStart.time
controller.timeline.end = calendarEnd.time

controller.timeline.setStartDateUsingOffset(-24 * 3600 * 1000L)
controller.timeline.setEndDateUsingOffset(4 * 3600 * 1000L, controller.timeline.start)

controller.timeline.setStartDateUsingRelativeTime("-3 days")
controller.timeline.setEndDateUsingRelativeTime("12 hours", controller.timeline.start)
```

Relative strings support periods like `"-1 day"`, `"-0.5 day"`, `"now"`, hours/days/weeks, etc.

Via `AnimationOptions` (string or `Date` ctors exist):

```kotlin
// After constructing the controller - there is no 3-arg MapboxMapController+AnimationOptions ctor
controller.animationOptions.duration = 5.0
controller.animationOptions.endDelay = 3.0
controller.animationOptions.shouldPreloadData = true
```

Or build options and copy fields onto `controller.animationOptions` / set timeline
`start`/`end` from a `AnimationOptions(start = "-1 day", end = "now")` instance.

SDK default `AnimationOptions` start/end is typically **past 24h -> now** (not the
"2 hours ago" prose in some docs examples). Always set range explicitly when it matters.

Rules: start must be earlier than end.

## Speed

```kotlin
controller.timeline.duration = 2.0   // seconds for one full loop
controller.timeline.endDelay = 1.0   // hold last frame before repeat
controller.timeline.timeScale = 1.0  // >0 playback rate
```

## Events

```kotlin
import com.xweather.mapsgl.anim.AnimationEvent

controller.timeline.on(AnimationEvent.play) { /* ... */ }
controller.timeline.on(AnimationEvent.PAUSE) { /* ... */ }
controller.timeline.on(AnimationEvent.advance) { /* ... */ }
controller.timeline.on(AnimationEvent.range_change) { /* ... */ }
```

Other constants: `stop`, `RESUME`, `RESTART`, `RESET`, `INTERVAL_CHANGE`, `TIMELINE_CHANGE`.

## Loading UI

```kotlin
controller.onLoadStart.observe(owner) { /* show spinner */ }
controller.onLoadComplete.observe(owner) { /* hide spinner */ }
```

## Animatable layers

Check `animatable` in https://www.xweather.com/docs/api/mapsgl/layers.  
On 1.6.x, animation is the timeline + tile/series interval path. Some shape/polygon
sources may not animate - follow the catalog.

## Practical tips

- Don't call `play()` until the map is loaded and layers are added.
- `shouldPreloadData` reduces first-play stalls for long ranges (more downloads).
- Session billing: animating inside an active session does not add cost (`sessions.md`).
