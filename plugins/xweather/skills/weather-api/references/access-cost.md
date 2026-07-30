# Access cost — how many accesses a request consumes

One HTTP request is not one access. The number of accesses ("tokens", "hits") charged against the
subscription allowance is:

```
accesses = endpoint multiplier × spatial multiplier × temporal multiplier
```

Only the **endpoint multiplier is knowable before sending the request** — it is a fixed per-endpoint
constant, published in the catalog and tabulated below. The spatial and temporal multipliers are
computed server-side from the area and time range the request actually covers, and the API does not
publish the formula. So:

- Before sending: report the endpoint multiplier as a **floor** — "at least N accesses" — and flag
  any parameter that will push the spatial or temporal multiplier above 1.
- After sending: `X-Cost-Tokens` on the response is the **exact** charge. Prefer it over any estimate.

Do not invent spatial or temporal multiplier values. Saying "5 accesses minimum, more if the 30-day
range raises the temporal multiplier" is accurate; saying "15 accesses" when the temporal multiplier
was guessed is not.

## Endpoint multipliers

### ×25

`/impacts/:activity`

### ×12

`/hail/archive` · `/hail/threats` · `/lightning/analytics`

### ×10

`/lightning` · `/lightning/archive` · `/lightning/threats` · `/renewables/irradiance/summary` ·
`/roadweather/analytics`

### ×5

`/airquality` · `/airquality/archive` · `/airquality/forecasts` · `/maritime/archive` ·
`/roadweather/conditions`

### ×1

`/airquality/index` · `/alerts` · `/alerts/summary` · `/conditions` · `/conditions/summary` ·
`/convective/outlook` · `/countries` · `/droughts/monitor` · `/earthquakes` · `/energy/farm` ·
`/fires` · `/fires/outlook` · `/forecasts` · `/indices/:type` · `/lightning/density` ·
`/lightning/flash` · `/lightning/summary` · `/lightning/turbinerisk` · `/maritime` · `/normals` ·
`/normals/stations` · `/observations` · `/observations/archive` · `/observations/summary` ·
`/phrases/summary` · `/places` · `/places/airports` · `/places/postalcodes` ·
`/renewables/irradiance/archive` · `/renewables/irradiance/tmy` · `/rivers` · `/rivers/gauges` ·
`/roadweather` · `/stormcells` · `/stormcells/summary` · `/stormreports` · `/stormreports/summary` ·
`/sunmoon` · `/sunmoon/moonphases` · `/threats` · `/tides` · `/tides/stations` ·
`/tropicalcyclones` · `/tropicalcyclones/archive` · `/xcast/forecasts`

Regenerate from the live catalog — the `multiplier` field on each endpoint:

```bash
curl -s https://www.xweather.com/docs/api/weather-api/endpoints \
  | python3 -c 'import json,sys; d=json.load(sys.stdin)["endpoint"]; [print(v["multiplier"], "/"+v["title"]) for v in sorted(d.values(), key=lambda e:-e["multiplier"])]'
```

`endpoints.md` also carries each endpoint's multiplier inline as `Cost: xN`.

Two endpoints (`/lightning/density`, `/lightning/turbinerisk`) have no multiplier on their doc pages;
the catalog reports `1` for both, which is what's used here.

## What raises the spatial multiplier

Bigger query area → bigger multiplier. In rough order of impact:

- A `within` polygon or rectangle covering a large region, vs. a single point.
- A large `radius` on `closest` / `within` (`radius=300miles` costs more than `radius=10miles`).
- `search` with no geographic constraint — an unbounded query is the largest possible area.
- `affects`, which resolves an event's footprint to every place inside it.

A plain `:id` lookup for one location is the spatial-multiplier floor.

## What raises the temporal multiplier

Longer time range → bigger multiplier. A `for=` single point in time, or no time parameter at all,
is the floor. A `from`/`to` span raises it in proportion to the span.

The docs give one concrete data point:
`/conditions/seoul,kr?from=2024-01-01&to=+1month` — "this will count as 31 API accesses."
`/conditions` is a ×1 endpoint, so a one-month hourly range carried a ~31× temporal multiplier —
roughly one access per day of data returned. Treat that as a rule of thumb for daily-resolution time
series on ×1 endpoints, not as a formula that generalizes across endpoints.

## Cases charged by an exact, documented rule

**`route` — one access per point.** Not one access for the whole route. A 500-point route is 500
accesses, multiplied by the endpoint multiplier. This is the single easiest way to burn an allowance
by accident. The docs recommend thinning closely-spaced points from routing directions before
sending. Cost for a route request:

```
accesses ≈ point count × endpoint multiplier   (× temporal, if each point carries a `from`)
```

So 200 points against `/roadweather/analytics` (×10) is ~2,000 accesses.

**`batch` — each sub-request bills separately.** A `/batch` wrapping 10 requests costs the sum of
those 10, each with its own endpoint multiplier. Batching saves round trips and latency, not
accesses. Maximum 31 sub-requests.

**Errors are free.** Only 2xx responses are charged; 4xx and 5xx are not. A failed request costs
nothing, so retrying a fixed URL after an `invalid_location` is free.

## Reading the actual cost

| Header | Meaning |
|---|---|
| `X-Cost-Tokens` | Exact accesses charged for this request |
| `X-Cost-Multipliers` | `endpoint=10; spatial=3; temporal=1` — the three factors |
| `X-Cost-Endpoint` | Which endpoint was billed |

Note the plural in `X-Cost-Multipliers`; the Responses doc page lists it singular but the wire format
is plural.

Remaining allowance comes from the rate-limit headers: `X-RateLimit-Limit-Minute` /
`-Remaining-Minute` / `-Reset-Minute` for the minutely cap, and `X-RateLimit-Limit-Period` /
`-Remaining-Period` / `-Reset-Period` / `-Limit-Period-Type` for the subscription period. Exceeding
either returns `429` with `maxhits_min` or `maxhits`.

`scripts/xwrequest.py` prints all of these.

## Reducing cost

- **Narrow the time range.** This is usually the largest factor. `for=` instead of `from`/`to` when a
  single valid time answers the question.
- **Narrow the area.** Smallest `radius` that still returns data; a point instead of a polygon.
- **Prefer a cheaper endpoint for the same question.** `/airquality/index` (×1) instead of
  `/airquality` (×5) when only the index value is needed. `/lightning/summary` (×1) instead of
  `/lightning` (×10) when aggregate counts suffice. `/roadweather` (×1) instead of
  `/roadweather/analytics` (×10) without the analytics fields.
- **Thin route points.** Directions APIs emit points every few metres; most are redundant for weather.
- **`fields=` does not reduce cost.** It reduces payload size only — the request is charged the same.
- **`limit` does not reduce cost** either, beyond whatever effect a smaller result set has on the
  spatial/temporal factors. Cost tracks the data queried, not the rows returned.
