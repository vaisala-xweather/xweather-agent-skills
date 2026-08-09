# MapsGL Apple SDK — timeline and animation

Every `MapController` is created with a `Timeline`, reachable as `controller.timeline`. Never construct
one yourself; configure the controller's after the controller exists.

The timeline drives **every animated layer on the map at once**. Some vector/polygon datasets can't
animate; see the layer listing at https://www.xweather.com/docs/mapsgl/weather-layers for which do.
Because each source has its own update interval, sources animate independently and may show different
numbers of frames within one loop.

Timeline and animation support landed in SDK 1.1.0.

## The inheritance chain matters

`Timeline` inherits `TimeAnimation`, which inherits `Animation`. The `Timeline` DocC page only lists
its *own* members, so the properties you most want — `currentDate`, `position`, `onAdvance` — appear to
be missing. They're inherited. The tables below merge all three levels.

## Setting the time range

```swift
// Absolute dates
controller.timeline.startDate = Date(timeIntervalSinceNow: -3600 * 2)
controller.timeline.endDate = Date()

// Offsets, in seconds (TimeInterval). `relativeTo:` defaults to Date()
controller.timeline.setStartDate(usingOffset: -3600 * 24)
controller.timeline.setEndDate(usingOffset: 3600 * 4, relativeTo: controller.timeline.startDate)

// Relative time strings
controller.timeline.setStartDate(usingRelativeTime: "-3 hours")
controller.timeline.setEndDate(usingRelativeTime: "now")
```

The default range is two hours ago to now.

Rules: the start must be earlier than the end. Both may be in the past, the future, or straddle now —
a forecast timeline is `"now"` to `"+48 hours"`, an observation timeline `"-24 hours"` to `"now"`.

**Offsets are `TimeInterval`, i.e. seconds.** The web SDK's equivalent takes milliseconds; the Swift
API does not. `setStartDate(usingOffset: -3600 * 24)` is 24 hours, not 24 seconds.

Relative time strings support years, months, weeks, days, hours, minutes, and seconds, plus `"now"`,
and accept fractions:

```swift
controller.timeline.setStartDate(usingRelativeTime: "-1 week")
controller.timeline.setStartDate(usingRelativeTime: "-2 weeks")
controller.timeline.setStartDate(usingRelativeTime: "-0.5 day")
controller.timeline.setEndDate(usingRelativeTime: "1 week")
```

`relativeTo:` anchors the calculation. Chaining the end off the new start is the clean way to express
"twelve hours of data starting three days ago":

```swift
controller.timeline.setStartDate(usingRelativeTime: "-3 days")
controller.timeline.setEndDate(usingRelativeTime: "12 hours", relativeTo: controller.timeline.startDate)
```

## Playback

```swift
controller.timeline.play()
controller.timeline.play(position: 0.5)     // start from halfway
controller.timeline.pause()
controller.timeline.resume()
controller.timeline.stop()
controller.timeline.restart()
controller.timeline.toggle()
```

## Speed and pacing

```swift
controller.timeline.duration = 2      // seconds for one full loop; higher is slower
controller.timeline.endDelay = 1      // seconds held on the last frame before looping
controller.timeline.delay = 0         // seconds before the first frame
controller.timeline.timeScale = 1.0   // multiplier on playback rate
```

Defaults: `duration` 2 seconds, `endDelay` 1 second. Animation repeats indefinitely.

`duration` is the whole loop, not per frame — so a longer time range at the same `duration` moves
faster through the data, not slower. Adjust `duration` alongside the range when the perceived speed
should stay constant.

## Jumping to a point in time

```swift
// by offset in seconds from startDate
controller.timeline.goTo(offset: 3600)          // one hour past the start

// by date
let date = controller.timeline.startDate.addingTimeInterval(1800)
controller.timeline.goTo(date: date)

// by normalized position, 0…1
controller.timeline.goTo(position: 0.5)         // useTotalDuration defaults to false
```

**`goTo(date:)` seeks only within `startDate`…`endDate`.** Like the offset and position forms, it
moves the playhead inside the existing window — it does not widen the window to reach a date outside
it. So set the range before seeking to a specific time:

```swift
let target = Date()  // whatever moment you want to show
controller.timeline.startDate = target.addingTimeInterval(-3 * 3600)
controller.timeline.endDate   = target.addingTimeInterval(3 * 3600)
controller.timeline.goTo(date: target)
```

This is documented behaviour for the MapsGL JavaScript SDK and the timeline model is shared, but it
has not been separately verified against this SDK. Setting the range first is correct either way, so
prefer it over seeking blind. The window must also sit inside the layer's own data range.

**`goTo(offset:)` is `TimeInterval`, i.e. seconds** — the API documents it as "the time interval to
advance from the start date". The web docs page shows `goTo(offset: 3600 * 1000)`, which is a
millisecond value carried over from the MapsGL JavaScript SDK; passing that in Swift jumps a thousand hours and
clamps to the end of the range. Every offset in this API is seconds.

## Reading current state

| Member | Type | From |
|---|---|---|
| `currentDate` | `Date` | `TimeAnimation` |
| `startDate` / `endDate` | `Date` | `TimeAnimation` |
| `position` | `Double` | `Animation` — 0…1 within the loop |
| `totalPosition` | `Double` | `Animation` |
| `state` | `AnimationState` | `Animation` |
| `isAnimating` / `isPaused` / `isActive` | `Bool` | `Animation` |
| `isPast` / `isFuture` | `Bool` | `TimeAnimation` |
| `containsPast` / `containsFuture` | `Bool` | `TimeAnimation` |
| `elapsed` / `lastElapsed` | `TimeInterval` | `Animation` |
| `totalDuration` | `TimeInterval` | `Animation` |
| `mode` | `Timing.ClampMode` | `TimeAnimation` |
| `getPosition(from:)` | `(Date) -> Double` | `TimeAnimation` |

## Events

| Signal | Payload | From |
|---|---|---|
| `onAdvance` | `Animation.Progress` | `Animation` — fires per frame |
| `onPlay` / `onPause` / `onResume` / `onStop` | `Void` | `Animation` |
| `onRestart` / `onReset` / `onEnd` | `Void` | `Animation` |
| `onRangeChange` | `DateInterval` | `TimeAnimation` |
| `onTimelineChange` | `Void` | `Timeline` |
| `onAnimationAdded` / `onAnimationRemoved` | `Animation` | `Timeline` |

`onAdvance` is what drives a scrubber. It fires on the render loop, so hop to the main queue before
touching SwiftUI state:

```swift
controller.timeline.onAdvance.publisher
    .receive(on: DispatchQueue.main)
    .sink { _ in
        position = controller.timeline.position
        currentDate = controller.timeline.currentDate
    }
    .store(in: &cancellables)
```

## Loading behavior

`controller.animationOptions` controls how playback interacts with data loading:

| Option | Effect |
|---|---|
| `shouldPreloadData` | Fetch animation frames ahead while paused — smoother first loop, more upfront network |
| `shouldPauseWhileLoading` | Pause automatically when frames aren't ready yet |
| `shouldResumeAfterLoading` | Resume once loading finishes |

```swift
controller.animationOptions.shouldPreloadData = true
controller.animationOptions.shouldPauseWhileLoading = true
controller.animationOptions.shouldResumeAfterLoading = true
```

Also available directly:

```swift
await controller.preloadAnimationData()
```

Pause-while-loading plus resume-after is the combination that avoids the stutter users read as a bug.
Preloading trades cellular data for smoothness — worth exposing as a setting on mobile rather than
forcing it on.

Use `controller.onLoadStart` / `onLoadProgress` / `onLoadComplete` to show a spinner during frame
loads.

## A SwiftUI scrubber

```swift
struct TimelineControls<MapType>: View {
    let controller: MapController<MapType>
    @Binding var position: Double
    @Binding var isPlaying: Bool

    var body: some View {
        HStack {
            Button(isPlaying ? "Pause" : "Play") {
                isPlaying ? controller.timeline.pause() : controller.timeline.play()
                isPlaying.toggle()
            }
            Slider(value: $position, in: 0...1) { editing in
                if editing { controller.timeline.pause() }
                else { controller.timeline.goTo(position: position, useTotalDuration: false) }
            }
            Text(controller.timeline.currentDate, style: .time)
                .monospacedDigit()
        }
    }
}
```

Pause on scrub-begin and seek on scrub-end; seeking on every slider change fights the animation and
triggers a data request per frame.

A maintained version of this control, for both SwiftUI and UIKit, is in the demo app:
https://github.com/vaisala-xweather/mapsgl-apple-sdk/tree/master/Demo

## Adding your own animations

The timeline is a general animation container, not weather-specific:

```swift
controller.timeline.add(animation: animation)
controller.timeline.remove(animation: animation)
controller.timeline.removeById(id: "my-animation")
controller.timeline.clear()
```

Rarely needed — MapsGL registers a `TimeSeriesAnimator` for each animatable source automatically.

Docs: https://www.xweather.com/docs/mapsgl-apple-sdk/getting-started/animating-data ·
https://www.xweather.com/docs/mapsgl-apple-sdk/reference/timeline
