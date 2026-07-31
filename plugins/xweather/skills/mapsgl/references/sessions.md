# MapsGL sessions — how usage is measured

MapsGL does not bill per tile, per layer, or per request. It bills in **sessions**.

> A session is a continuous user interaction with a MapsGL map for **up to 5 minutes**. It starts
> when any MapsGL layer is added to the map. Within a session, interaction is **unlimited**.

On a **Weather API and Maps** subscription — which includes MapsGL access — usage is counted in
accesses, and MapsGL carries a **150× multiplier**:

```
1 MapsGL session (5 minutes) = 150 accesses
```

## The three rules that decide the number

**1. Sessions are aligned to the wall clock, not to when the user arrived.**

Boundaries fall on clock times evenly divisible by 5 — `:00`, `:05`, `:10`, `:15`, and so on. A
session is not a rolling five-minute window starting at first interaction. This is the single most
misunderstood part of the model, and it means **elapsed viewing time doesn't determine the count —
how many 5-minute buckets you touch does.**

**2. At least one session is incurred per MapsGL data request.**

There is no partial or prorated session. Adding one layer and immediately closing the page still
costs a full session, so 150 accesses is the floor for any MapsGL usage at all.

**3. Inside a session, everything is free.**

Unlimited interaction: panning, zooming, animating over the timeline, refreshing data, and toggling
layers on and off. **The number of layers does not multiply the cost.** A map showing eight layers
costs exactly the same as a map showing one.

## Worked examples

**The documented example — 4 minutes of viewing, 2 sessions:**

A user opens a map with a radar layer at **8:03** and keeps watching until **8:07**.

```
8:00–8:05 bucket  → session 1
8:05–8:10 bucket  → session 2
                    2 sessions = 300 accesses
```

Four minutes of viewing, two sessions, because the view straddled the `:05` boundary.

**The same duration, half the cost:**

A user views the map from **8:05** to **8:09** — also 4 minutes.

```
8:05–8:10 bucket  → session 1
                    1 session = 150 accesses
```

Identical elapsed time, half the billing, purely from where it fell on the clock. You cannot control
this, so per-user cost is a distribution, not a fixed number.

### Estimating the average for capacity planning

For a view of `d` minutes starting at a uniformly random time, the expected number of sessions is:

```
expected sessions = floor(d / 5) + 1 + (d mod 5) / 5
```

Not `d / 5`, and not `ceil(d / 5)` — both understate it, because any view that isn't exactly
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

Read the 4-minute row against the worked example above: a 4-minute view stays inside one bucket only
when it starts in the first minute of that bucket, so it crosses a boundary **80 %** of the time —
hence 1.8 rather than 1. Use these figures for forecasting rather than the best case; assuming 150
accesses per short view underestimates by roughly 10–20 %.

**Layers are free — a heavy map costs the same as a light one:**

```
controller.addWeatherLayer('radar');
controller.addWeatherLayer('satellite-geocolor');
controller.addWeatherLayer('alerts');
controller.addWeatherLayer('temperatures');
controller.addWeatherLayer('wind-particles');
```

Five layers, viewed 9:00–9:04 → **1 session = 150 accesses**. The same four minutes with only
`radar` also costs 1 session. Adding layers to an existing MapsGL map is free; the same five layers
on a Raster Maps static map would cost 5× (see the comparison below).

**Interaction is free:**

A user opens a map at 10:00, then for four minutes pans across three states, zooms from z4 to z9,
scrubs the timeline through a 3-hour radar animation twice, and toggles alerts on and off.

→ **1 session = 150 accesses.** Every one of those actions is included.

**A long session — a wall display:**

A dashboard left running with a radar layer for an 8-hour shift:

```
8 hours = 480 minutes ÷ 5 = 96 sessions
96 × 150 = 14,400 accesses per display per shift
```

Worth flagging to anyone building kiosk or operations-centre displays: continuous unattended display
is the most expensive MapsGL pattern, because sessions keep accruing whether or not a human is
looking. Consider tearing the layer down when the display is idle or off-hours.

**Many short visits are the expensive shape:**

100 users each opening a map for 30 seconds, at random times:

```
30 seconds → 1.1 sessions expected (1 if it fits a bucket, 2 if it straddles one)
100 visits → ~110 sessions → ~16,500 accesses
```

Compare with 100 users each viewing for 5 continuous minutes: ~200 sessions, ~30,000 accesses. So the
30-second visits cost roughly **55 %** of what ten-times-longer visits cost — nothing like the 10×
discount the duration ratio suggests. Short-session traffic gets almost no benefit from being short,
which is the key planning insight: MapsGL rewards long engaged sessions and charges nearly full price
for drive-by page loads.

## MapsGL vs. Raster Maps billing

These are genuinely different models, and the right product depends on the usage pattern:

| | MapsGL | Raster Maps |
|---|---|---|
| Unit | Session (5-min clock bucket) | Map unit (one 256×256 tile × one ×1 layer) |
| More layers | **Free** — no effect on cost | **Multiplies** cost, per layer |
| Pan / zoom | **Free** within the session | Each new tile costs again |
| Animation | **Free** within the session | Each frame is a fresh set of tiles |
| Floor | 1 session = 150 accesses | 1 map unit |
| Cheapest for | Long, interactive, multi-layer sessions | One-off static images; brief, non-interactive views |

Rules of thumb:

- **A single static image on a page** — Raster Maps. An 800×600 one-layer image is 12 map units
  against MapsGL's 150-access floor.
- **An interactive, animated, multi-layer map** — MapsGL. Panning a 4-layer Raster Maps tile map
  quickly exceeds 150 accesses, and MapsGL's cost stops growing while the session lasts.
- **A brief look at one layer** — Raster Maps, since MapsGL charges a full session regardless.

## Reducing session consumption

The only real lever is **when layers are on the map**, since a session starts the moment a layer is
added and interaction inside it is free.

- **Don't add layers until the user asks for them.** A map that loads with no weather layer starts no
  session. Deferring `addWeatherLayer` until a toggle is switched on avoids charging visitors who
  never engage with the weather.
- **Remove layers when the map isn't visible.** `removeWeatherLayer` on tab-hidden, scroll-out-of-view,
  or an idle timeout stops further sessions accruing. `setWeatherLayerVisibility(code, false)` keeps
  resources loaded and is cheaper to reverse, but check whether it also stops data requests before
  relying on it for cost control — visibility and data fetching are not necessarily the same thing.
- **Batch layer changes freely.** Since toggling is free inside a session, there's no cost reason to
  restrict how many layers a user can enable.
- **Reconsider unattended displays.** They're the highest-consumption pattern; a scheduled teardown
  outside operating hours cuts them proportionally.

Adding more layers, animating, or letting users explore are *not* worth optimising — they cost
nothing extra.

## Answering usage questions

Report the arithmetic, not just a number: bucket count → sessions → accesses. Note when a duration
straddles a boundary, and give the range rather than a single figure when the start time is unknown.

Two things to be careful about:

- **The 150× multiplier applies to a Weather API and Maps subscription**, which is what the docs
  describe. Other plan shapes may count MapsGL differently — for a specific allowance, point the user
  at their account dashboard or account executive rather than extrapolating.
- **Session counts are a usage metric, not a rendering constraint.** Nothing about sessions changes
  what the map can do, and a session's expiry doesn't interrupt the user.
