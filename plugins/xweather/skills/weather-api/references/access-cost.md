# Access cost — how many accesses a request consumes

One HTTP request is not one access. The number of accesses ("tokens", "hits") charged against the
subscription allowance is:

```
accesses = endpoint multiplier × spatial multiplier × temporal multiplier
```

**The spatial multiplier is always 1 today.** No current Weather API endpoint uses it. It exists in
the cost header for endpoints Xweather may introduce later, so don't factor area, radius, or query
geometry into an estimate — a `within` polygon spanning three states costs the same as a single-point
`:id` lookup. In practice:

```
accesses = endpoint multiplier × temporal multiplier
```

The **endpoint multiplier** is a fixed per-endpoint constant, published in the catalog and tabulated
below. The **temporal multiplier** is the number of time intervals a single request covers, on the
endpoints that bill that way — see below. Both are knowable before sending, so a cost estimate is
usually exact rather than a floor.

`X-Cost-Tokens` on the response is the authoritative charge. Prefer it when the request has actually
run, and use it to check any estimate you weren't sure about.

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

## The spatial multiplier

**Always 1.** Nothing in the Weather API currently uses it. The factor is present in the
`X-Cost-Multipliers` header, and Xweather may attach it to future endpoints, but today it never
raises a bill.

So area is *not* a cost lever. A `within` polygon covering several states, `radius=300miles`, and a
single-point `:id` lookup all carry the same spatial factor. Don't tell anyone to shrink a radius or
tighten a bounding box to save accesses — it won't, and it may cost them the data they needed.

## The temporal multiplier

**This is the one that actually varies.** On endpoints that return a series over a requested range,
one request is charged **one access per interval returned**, not one access for the request.

The clearest example is `/conditions/summary`, which bills **one access per day**:

```
/conditions/summary/minneapolis,mn?from=-30days&to=now   → 30 days = 30 accesses
/conditions/summary/minneapolis,mn                       → 1 day   =  1 access
```

The docs give the same shape for `/conditions`:
`/conditions/seoul,kr?from=2024-01-01&to=+1month` — "this will count as 31 API accesses."

So the arithmetic is `endpoint multiplier × intervals requested`. A 30-day pull from a ×5 endpoint
that bills daily is 150 accesses, not 5.

**Not every endpoint bills this way**, and Xweather doesn't publish an exhaustive list of which do.
Treat a multi-interval `from`/`to` range as the signal: if a single request will return N days or N
hours of data, assume N intervals and say so. A request for a single point in time — `for=`, or no
time parameter at all — is one interval.

When you're unsure whether a given endpoint bills per interval, say the range is the thing that could
multiply the cost and point at `X-Cost-Tokens` for the exact figure, rather than guessing a number.

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

- **Narrow the time range.** The only real lever. Each day or hour you ask for on a per-interval
  endpoint is another access, so `for=` instead of a `from`/`to` span when a single valid time answers
  the question, and don't request 30 days when 7 will do.
- **Prefer a cheaper endpoint for the same question.** `/airquality/index` (×1) instead of
  `/airquality` (×5) when only the index value is needed. `/lightning/summary` (×1) instead of
  `/lightning` (×10) when aggregate counts suffice. `/roadweather` (×1) instead of
  `/roadweather/analytics` (×10) without the analytics fields.
- **Thin route points.** Directions APIs emit points every few metres; most are redundant for weather.
- **`fields=` does not reduce cost.** It reduces payload size only — the request is charged the same.
- **`limit` does not reduce cost** either. Cost tracks the time range queried, not the rows returned.
- **Narrowing the area does nothing.** The spatial multiplier is always 1, so a smaller `radius` or a
  tighter bounding box saves no accesses — it only risks returning less data than the user needed.
