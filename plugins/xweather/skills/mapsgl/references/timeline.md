# Timeline & Animation Reference

The timeline is what lets a weather layer show change over time instead of a single snapshot —
e.g. animating radar over the past few hours, or scrubbing through a temperature forecast. It's a
single shared clock: one timeline per controller drives every animatable layer added to it in
sync, rather than each layer animating independently.

Verified against `packages/webgl-maps/src/anim/{Animation,TimeAnimation,Timeline}.ts`.
`controller.timeline` is a `Timeline` (extends `TimeAnimation` extends `Animation`) created
automatically by the map controller's constructor, seeded from `opts.animation`.

## Setting the visible time range

```javascript
controller.on('load', () => {
  controller.timeline.startDate = new Date(2022, 10, 20, 17);
  controller.timeline.endDate = new Date(2022, 10, 23, 17);
});
```

Relative helpers (offsets in ms, or relative-time strings like `'-1 week'`, `'now'`, `'-3 days'`, `'12 hours'`):

```javascript
controller.timeline.setStartDateUsingOffset(-24 * 3600 * 1000);              // 24h ago
controller.timeline.setEndDateUsingOffset(4 * 3600 * 1000, controller.timeline.startDate);

controller.timeline.setStartDateUsingRelativeTime('-3 days');
controller.timeline.setEndDateUsingRelativeTime('12 hours', controller.timeline.startDate);
```

`startDate`/`endDate` setters throw a `TypeError` on an invalid `Date` — validate user input before
assigning. Start must precede end.

## Animation speed & playback

```typescript
interface AnimationDefaults {
  enabled: true; autoplay: false; duration: 1; delay: 0; endDelay: 0;
  timeScale: 1; repeat: true; manualAdvance: false; alwaysPlayFromBeginning: false;
}
```

```javascript
controller.timeline.duration = 2;      // seconds per full loop
controller.timeline.endDelay = 0;      // seconds held on the final frame before looping
controller.timeline.timeScale = 1;     // playback rate multiplier (> 0)

controller.timeline.play();
controller.timeline.pause();
controller.timeline.resume();
controller.timeline.stop();            // resets to start (or configured stop position)
controller.timeline.restart();
controller.timeline.toggle();
```

`play`/`pause`/`resume`/`stop`/`restart`/`goTo`/`goToDate`/`advance` on `Timeline` propagate to
every layer/source animation registered under it — you don't need to drive individual layers.

## Jumping to a specific moment

```javascript
controller.timeline.goToOffset(3600 * 1000); // 1 hour after start
controller.timeline.goToDate(new Date(controller.timeline.startDate.getTime() + 30 * 60 * 1000));
controller.timeline.goTo(0.5);               // normalized position, 0..1 of total duration
```

### `goToDate` only works inside the current range

**`goToDate(date)` cannot move outside `startDate`…`endDate`.** The timeline is a fixed window and
`goToDate` seeks *within* it — it does not extend the window to reach the date you asked for. Pass a
date outside the range and you won't get that data; the map stays where it was or clamps to an end,
with no error to tell you why.

Note the example above: it deliberately jumps to `startDate + 30 minutes`, a time already inside the
window. That is the only kind of date `goToDate` can honour.

So **set the range first, then seek**:

```javascript
const target = new Date('2026-08-09T18:00:00Z');

// Widen the window so it contains the target before seeking to it.
controller.timeline.startDate = new Date(target.getTime() - 3 * 3600 * 1000);
controller.timeline.endDate   = new Date(target.getTime() + 3 * 3600 * 1000);
controller.timeline.goToDate(target);
```

If a date might fall outside the current window, check before seeking and widen when it doesn't:

```javascript
function showAt(controller, target) {
  const { startDate, endDate } = controller.timeline;
  if (target < startDate || target > endDate) {
    controller.timeline.startDate = new Date(target.getTime() - 3 * 3600 * 1000);
    controller.timeline.endDate   = new Date(target.getTime() + 3 * 3600 * 1000);
  }
  controller.timeline.goToDate(target);
}
```

The window still has to sit inside what the *layer* actually carries — a range extending past a
layer's `dataRange` renders nothing for the part it doesn't cover, however the timeline is set. Check
the layer's range in `layers.md`.

## Read-only state

```
controller.timeline.currentDate      // Date, computed from position
controller.timeline.isAnimating      // boolean
controller.timeline.isPaused         // boolean
controller.timeline.isActive         // boolean
controller.timeline.containsPast     // boolean
controller.timeline.containsFuture   // boolean
controller.timeline.info             // { isActive, currentDate, startDate, endDate, deltaTime }
```

## Constraints & gotchas

- Start date must precede end date, or the setter throws.
- `goToDate(date)` seeks only *within* `startDate`…`endDate` — it never widens the window. A
  date outside the range silently fails to display. Set the range first; see "Jumping to a
  specific moment".
- Not all layer types animate — polygon/shape-only sources (e.g. static admin boundaries) don't
  respond to timeline changes; sample/grid/contour/particle weather layers do.
- The timeline repeats indefinitely by default (`repeat: true`); set `repeat: false` via the
  `animation` option passed into the map controller constructor if you want single-pass playback.
