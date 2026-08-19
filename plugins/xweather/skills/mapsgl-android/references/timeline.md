# Timeline & animation - MapsGL Android

Verified against `Timeline`, `TimeAnimation`, `Animation`, `AnimationOptions`, `AnimationEvent` and
`TimeStringConverter` on the `feature/maptime-filter` branch. Docs pages are secondary when they
disagree: https://www.xweather.com/docs/mapsgl-android-sdk/getting-started/animating-data ·
https://www.xweather.com/docs/mapsgl-android-sdk/reference/timeline

## The inheritance chain matters

```
Animation          duration, delay, endDelay, timeScale, repeat, autoPlay, on/off, state
  └─ TimeAnimation start, end, currentDate, the setStart*/setEnd* helpers, goToDate, goToOffset
       └─ Timeline play, playFromDate, pause, resume, stop, restart, reset, toggle, goTo, position
```

`controller.timeline` is a `Timeline`, so everything above is available on it. Knowing which level a
member comes from explains why some things behave differently - the range helpers on `TimeAnimation`
regenerate intervals, while the playback methods on `Timeline` do not.

## Setting the time range

```kotlin
controller.timeline.start = calendarStart.time    // Date; defaults to 24 h ago
controller.timeline.end = Date()                  // Date; defaults to now
```

Relative strings are usually easier:

```kotlin
controller.timeline.setStartDateUsingRelativeTime("-1 day")
controller.timeline.setEndDateUsingRelativeTime("now")
controller.timeline.setEndDateUsingRelativeTime("12 hours", controller.timeline.start)
```

The parser accepts `"now"`, or `"{amount} {unit}"` where amount may be negative and fractional and
unit is one of **second(s), minute(s), hour(s), day(s), week(s), month(s), year(s)** - singular or
plural, case-insensitive. `"-0.5 day"` works. Fractional months and years are approximated and print
a warning to stderr, so prefer whole units there.

Absolute offsets take a `Long`:

```kotlin
controller.timeline.setStartDateUsingOffset(-24 * 3600 * 1000L)
controller.timeline.setEndDateUsingOffset(4 * 3600 * 1000L, controller.timeline.start)
```

**The offset is in milliseconds, despite the KDoc saying seconds.** The implementation is
`Date(relativeTo.time + offset)` and `Date.time` is milliseconds. Following the KDoc gives you a range
1000× too short.

Two behaviours of the offset helpers that the relative-time helpers do not share:

- **`setStartDateUsingOffset` clamps to a minimum one-hour range.** If the computed start lands within
  an hour of `end`, it is forced to `end - 1 hour` instead.
- **`setStartDateUsingOffset` calls `stop()`.** Setting the start this way halts playback;
  `setStartDateUsingRelativeTime` does not.

`start` must be earlier than `end`.

### Interval granularity is derived, not fixed

`intervalLength` defaults to 3600 (one hour) but is recomputed from the total range so the tick count
stays near **30** intervals. A short range gets finer steps down to an hour; a multi-day range gets
coarser ones. That is why a 7-day timeline does not animate hour by hour, and why frame count is not
simply range ÷ one hour.

## Playback

```kotlin
controller.timeline.play()                    // optional Double start position
controller.timeline.playFromDate(someDate)
controller.timeline.pause()
controller.timeline.resume()
controller.timeline.stop()
controller.timeline.restart()
controller.timeline.reset()
controller.timeline.toggle()
```

## Speed and pacing

```kotlin
controller.timeline.duration = 2.0    // seconds for one full pass
controller.timeline.delay = 0.0       // seconds before starting
controller.timeline.endDelay = 1.0    // seconds holding the last frame before repeating
controller.timeline.timeScale = 1.0   // playback rate multiplier, > 0
controller.timeline.repeat = true
controller.timeline.autoPlay = false
```

`duration` is wall-clock seconds for the whole animation, not per frame - a longer time range at the
same `duration` simply moves faster.

## Jumping to a point in time

```kotlin
controller.timeline.goTo(0.5)                             // normalized position
controller.timeline.goTo(0.5, useTotalDuration = true)
controller.timeline.goToDate(someDate)
controller.timeline.goToOffset(3600 * 1000L)              // milliseconds from start
```

`useTotalDuration` decides whether the position is measured against the animation duration alone or
including `delay` and `endDelay`. It defaults to `false`, inherited from `Animation`.

`advance()` and `advanceToStopPosition()` are **`internal`** - they appear in the class but are not
callable from outside the SDK. `isAtEndPosition()` sits on `Timeline`'s **companion object**, so it is
`Timeline.isAtEndPosition()`, not a call on your instance.

## Reading current state

```kotlin
controller.timeline.position          // Double, normalized
controller.timeline.currentDate       // Date at the playhead
controller.timeline.deltaTime         // Long
controller.timeline.containsPast      // range extends before now
controller.timeline.containsFuture    // range extends past now
controller.timeline.isPast            // playhead is before now
controller.timeline.isFuture

controller.timeline.liveState.observe(owner) { state -> /* AnimationState */ }
```

`AnimationState` is `initial`, `playing`, `paused`, `stopped`, `loading`, `ready`. `liveState` is
`LiveData`, so observe it with a `LifecycleOwner` rather than polling.

## Events

```kotlin
import com.xweather.mapsgl.anim.AnimationEvent

controller.timeline.on(AnimationEvent.play) { /* ... */ }
controller.timeline.on(AnimationEvent.PAUSE) { /* ... */ }
controller.timeline.off(AnimationEvent.play, listener)
```

**The constant names are inconsistently cased in the SDK, and that is not a typo here:**

| Constant | String value |
|---|---|
| `AnimationEvent.play` | `"play"` |
| `AnimationEvent.stop` | `"stop"` |
| `AnimationEvent.advance` | `"advance"` |
| `AnimationEvent.range_change` | `"range:change"` |
| `AnimationEvent.PAUSE` | `"pause"` |
| `AnimationEvent.RESUME` | `"resume"` |
| `AnimationEvent.RESTART` | `"restart"` |
| `AnimationEvent.RESET` | `"reset"` |
| `AnimationEvent.INTERVAL_CHANGE` | `"interval:change"` |
| `AnimationEvent.TIMELINE_CHANGE` | `"timeline:change"` |

Four are lowercase and six are uppercase. Do not "normalize" them - use the spelling in this table.
Note also that several constant names differ from their string values, so prefer the constant over a
literal.

`on(event: String, listener: (Any) -> Unit)` comes from `Animation`, so it takes the string, not an
enum.

## A SeekBar scrubber

A scrubber that drives the timeline when dragged and follows it during playback. **Adapted from the
SDK's own demo app**, which is shipping code rather than something written against the headers -
including the two throttling decisions below, which the demo documents as measured rather than
guessed.

```xml
<SeekBar
    android:id="@+id/scrubber"
    android:layout_width="0dp"
    android:layout_height="wrap_content"
    android:max="10000" />          <!-- fine-grained: a coarse max makes the thumb step -->

<ImageButton android:id="@+id/playButton" ... />
<TextView    android:id="@+id/timeLabel" ... />
```

```kotlin
private val seekBarRange = 10_000.0
private var lastLabelUpdateMs = 0L
private val labelIntervalMs = 100L
private val timeFormat = SimpleDateFormat("MMM d, h:mm a", Locale.getDefault())

private fun wireScrubber(timeline: Timeline) {

    // 1. Dragging drives the timeline.
    binding.scrubber.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
        override fun onProgressChanged(bar: SeekBar?, progress: Int, fromUser: Boolean) {
            val position = progress / seekBarRange
            if (fromUser) timeline.goTo(position)

            // Reformatting the label allocates a Date and a formatted String — throttle it.
            val now = SystemClock.elapsedRealtime()
            if (fromUser || now - lastLabelUpdateMs >= labelIntervalMs) {
                lastLabelUpdateMs = now
                binding.timeLabel.text = timeFormat.format(timeline.currentDate)
            }
        }
        override fun onStartTrackingTouch(bar: SeekBar?) = Unit
        override fun onStopTrackingTouch(bar: SeekBar?) = Unit
    })

    // 2. Playback drives the scrubber. Deliberately NOT throttled — see below.
    timeline.on(AnimationEvent.advance) {
        binding.scrubber.progress = (timeline.position * seekBarRange).toInt()
    }

    // 3. Keep the play button in sync however state changed.
    binding.playButton.setOnClickListener { timeline.toggle() }
    timeline.on(AnimationEvent.play) { setPlayIcon(playing = true) }
    timeline.on(AnimationEvent.PAUSE) { setPlayIcon(playing = false) }
    timeline.on(AnimationEvent.stop) { setPlayIcon(playing = false) }

    setPlayIcon(playing = timeline.state == AnimationState.playing)
}
```

### Why one update is throttled and the other is not

**`AnimationEvent.advance` fires on every Choreographer frame during playback** - at the display's
refresh rate. `Timeline` takes an `fps` parameter but it does not throttle this event, so any work in
an `advance` listener runs 60-120 times a second.

- **Moving the thumb is not throttled.** Assigning `SeekBar.progress` is an int write. Throttling it
  to 100 ms was tried in the demo app and made the thumb visibly step and stutter, so it was reverted.
  The thumb should track the frame rate even when the layer redraw lags behind it.
- **Reformatting the time label is throttled** to ~100 ms. Each update allocates a `Date` plus
  formatted strings and calls `setText`, and on a long range the simulated time genuinely changes
  every frame, so there is no "skip if unchanged" shortcut. Profiling put this per-frame text path as
  the largest main-thread allocator during steady-state playback. Nobody perceives a label updating
  faster than about 10 times a second.

The general rule for `advance` listeners: keep them to cheap primitive assignments, and throttle
anything that allocates or formats.

Use a large `android:max` (10000, not 100). The position is a normalized `Double`, so a coarse max
quantizes it and produces visible stepping regardless of frame rate.

## Loading behaviour

```kotlin
controller.animationOptions.shouldPreloadData = true    // false by default
```

`shouldPreloadData` pre-fetches tiles across the whole timeline range so playback starts ready rather
than stalling while data arrives. It costs more downloads up front, and it is the single biggest
difference between smooth first playback and a visible stall.

Loading UI is driven from the controller, not the timeline:

```kotlin
controller.onLoadStart.observe(owner) { /* show spinner */ }
controller.onLoadComplete.observe(owner) { /* hide spinner */ }
controller.onLoadProgress.observe(owner) { progress -> /* MapLoadProgress */ }
```

## Animating a filter with the playhead

A layer filter referencing `["map-time"]` re-evaluates as the playhead moves, which is how
time-windowed features reveal during playback without rebuilding geometry:

```kotlin
descriptor.filter = Expression.lessThanOrEqual(Expression.get("timestamp"), Expression.mapTime)
```

`Expression.mapTime` is the timeline position in Unix seconds, not wall clock. The SDK splits such a
filter into a static part applied at geometry prep and a dynamic part applied at draw time. Full
detail: `references/expressions.md`.

## Animatable layers

Not every layer animates. Check `animatable` in the catalog at
https://www.xweather.com/docs/api/mapsgl/layers. Animation runs through the timeline plus the
tile/series interval path, so some shape and polygon sources will not move - follow the catalog
rather than assuming.

## Practical notes

- **Don't call `play()` before the map is loaded and layers are added.** Nothing happens, and no error
  is raised.
- **Session cost is unaffected by animating.** Playback inside an active session is free; what costs
  is how long weather layers stay attached. See `references/sessions.md`.
- **Setting the range stops playback** when you use `setStartDateUsingOffset`. Re-`play()` after.
- **A long range means coarser intervals**, not more frames - see the granularity note above.
