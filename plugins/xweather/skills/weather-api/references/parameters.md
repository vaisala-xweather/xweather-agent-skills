# Request anatomy, parameters, and syntax

## Anatomy

```
https://data.api.xweather.com/{endpoint}/{action}/{:id}?{parameters}&client_id=…&client_secret=…
                              └─ e.g. observations
                                        └─ e.g. closest / within / search / route (omit for :id or :all)
                                                 └─ a place, station id, or event id
```

- Base host: `data.api.xweather.com`. `api.aerisapi.com` is the legacy host and still resolves — use
  `data.api.xweather.com` for anything new.
- Always HTTPS.
- The action segment is omitted entirely for `:id` (`/observations/seattle,wa`) and `:all`
  (`/tropicalcyclones`).
- The location can go in the path (`/alerts/denver,co`) **or** in `p=` (`/alerts?p=denver,co`).
  Actions other than `:id` require `p=` because the path slot is taken by the action name.
- Order of query parameters does not matter.
- URL-encode spaces as `%20` (`palm%20springs,ca`) or `+` in place names (`king+county,wa`).

## Authentication

Every request needs `client_id` and `client_secret` as query parameters — there is no header or
bearer-token form:

```
https://data.api.xweather.com/places/98109?client_id={client_id}&client_secret={client_secret}
```

Credentials come from the account portal (Apps section) and are bound to a **namespace** registered
with the key pair — a top-level domain (`mydomain.com`, `*.mydomain.com`) for web, or a reverse-DNS
bundle id (`com.mydomain.MyProject`) for mobile. A request originating outside that namespace fails
with `unauthorized_namespace`.

## Global parameters

| Parameter | What it does |
|---|---|
| `p` | The place/location. Required for every action except `:id` (where the place sits in the path). Accepts any supported place format; for `within` it accepts multi-point geometry; for `route` a semicolon-separated list. |
| `limit` | Maximum number of primary results. **Default is 1** — a `closest`/`search`/`within` query without `limit` returns a single record. |
| `skip` | Skip N primary results (pagination, pairs with `limit`). |
| `plimit` | Maximum number of sub-elements, normally entries in a `periods` array. |
| `pskip` / `psort` / `pfilter` | `skip`/`sort`/`filter` applied to sub-elements instead of primary results. |
| `radius` | Search radius for `closest` / `within` (circle). Units: `miles`, `mile`, `mi`, `km`, `m`/`meter` — e.g. `radius=25miles`, `radius=10km`. |
| `minradius` | Inner radius; combined with `radius` produces a donut-shaped search. |
| `mindist` | Minimum spacing between returned points, for thinning dense station/point data. Default 1 km; minimum `1m`. `mindist=0` is allowed. |
| `lod` | Level of detail matching a map zoom level; alternative to `mindist` for map display. |
| `fields` | Comma-separated list of response properties to return, dot-notated (`ob.tempF`, `periods.maxTempF`). Cuts payload size dramatically. |
| `filter` | Endpoint-specific selectors. `,` = AND, `;` = OR. Valid tokens differ per endpoint — see `endpoints.md` / `filters.md`. |
| `query` | Value-based filtering, `property:value`. See Advanced queries below. |
| `sort` | `property` or `property:direction`. See Sorting below. |
| `from` / `to` | Time range. See Dates and times below. |
| `for` | A single point in time instead of a range. |
| `format` | `json` (default), `geojson`, `csv`, `tsv`. |
| `lang` | Response language, where the endpoint supports it (e.g. `/alerts`). |

Endpoint-specific extras: `height` (`/lightning/turbinerisk`), `tilt`, `azimuth`, `panel_mode`,
`horizon`, `preset` (`/renewables/irradiance/*`). `endpoints.md` lists the accepted `params` for
every endpoint — a parameter not in that list is either ignored or returns a `warn_invalid_param`
warning.

## Actions

| Action | Path form | Notes |
|---|---|---|
| `:id` | `/observations/seattle,wa` | The default single-location lookup. Identifier may be a place, station id, zone, or event id depending on endpoint. |
| `:all` | `/tropicalcyclones` | No action segment; returns everything the endpoint has (subject to `limit`). |
| `closest` | `/observations/closest?p=…&radius=…&limit=…` | Results ordered nearest → farthest. Without `limit` you get exactly one. Widen `radius` when empty. |
| `within` | `/earthquakes/within?p=…` | Results are unordered unless you pass `sort`. Geometry via `p`: <br>• circle — `p=45,-93&radius=50miles`<br>• rectangle — `p=43.23,-96.92,45.62,-91.31` (two corners)<br>• polygon — 3+ points, `p=36.89,-106.25,43.89,-106.56,44.82,-92.77,41.02,-87.76`; no need to close the ring |
| `search` | `/observations/search?query=state:mn&sort=temp:-1` | Generalized query; expects `query`. Unordered unless sorted. |
| `route` | `/observations/route?p=44.96,-93.27;44.91,-93.5;44.85,-93.46` | Semicolon-separated points, min 2. Returns an array of GeoJSON point features in the order supplied. Filters/queries/sorts apply per point. **Each point counts as a separate API access.** For long routes POST a JSON body instead (see below). |
| `affects` | `/earthquakes/affects?p=…` | Returns the *places* affected by an event, in the same shape as `places/within` — not endpoint-native objects. |
| `contains` | `/convective/outlook/contains?p=atlanta,ga` | For polygon products: returns the polygons a point falls inside. The inverse of `within`. On these endpoints the plain `:id` form is a documented shorthand for the same thing — `/droughts/monitor/san diego,ca` ≡ `/droughts/monitor/contains?p=san diego,ca`. |

Supported actions vary per endpoint — check `endpoints.md` before using one.

Corner order for a `within` rectangle is documented inconsistently: the `within` action page says
"lower left (SW) first, then upper right (NE)", while `/observations/archive` documents the same
parameter as "top latitude, left longitude, bottom latitude, right longitude". If a rectangle query
comes back empty, swap the pairs before assuming the request is otherwise wrong — or use a polygon,
which is unambiguous.

### Long routes via POST

POST a JSON array to the `route` action. Each element is either a parameter object or a GeoJSON
`Feature` with a `Point`/`LineString` geometry:

```json
[
  { "p": "44.96,-93.27", "id": 1, "from": "+20minutes" },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [-93.265, 44.9778] },
    "id": "1",
    "properties": { "from": "+20minutes" }
  }
]
```

`p` is any supported place format; `id` (optional) becomes the returned feature's id; `from`
(optional) sets the valid time for that point — useful for ETA-based forecasts along a route. A
`LineString` carries a single properties object, so split it into individual `Point` features if
each point needs its own `from`.

## Supported places

Usable in the path as `:id` or in `p=`:

| Format | Example |
|---|---|
| Latitude,longitude | `37.25,-97.25` (`p=` only) |
| City, state | `seattle,wa` · `seattle,washington` |
| City, state, country | `toronto,on,ca` · `guangzhou,gd,china` |
| City, country | `paris,fr` · `tokyo,japan` |
| Postal / ZIP code | `98109` (US and Canada) |
| ICAO station code | `KMPX` · `KBFI` |
| IATA airport code | `MSP` · `ROA` |
| County / parish | `king+county,wa` |
| State-country id | `WAC033` |
| FIPS code | `fips:53033` |
| NOAA weather zone | `MNZ029` · `zone:MNZ029` |
| Canadian location code | `CLC-049930` |
| European alert zone | `zone:FR052` |
| PWS station | `PWS_3183437707` · `PWS_VILLONWMR2` |

A place given without a state/province for a US or Canadian city (`atlanta,us`) still resolves, but
returns a `warn_location` warning and picks the highest-population match — always include the state
when you know it.

## Dates and times

`from`, `to`, and `for` all accept the same forms:

| Form | Examples |
|---|---|
| Keyword | `now` · `today` |
| Weekday name | `friday` |
| Relative offset | `+1day` · `+3days` · `-12hours` · `+6hr` · `-10minutes` · `+1month` |
| ISO date | `2024-03-23` |
| Date + time | `2024-06-05 16:00:00` (local time at the requested location) |

- `for=` pins a single valid time: `/conditions/minneapolis,mn?for=-4hours`.
- `from=` + `to=` produce a series: `/conditions/paris,france?from=-12hours&to=now&plimit=12`.
- Relative values are also valid inside `query=`: `query=issued:-10minutes`,
  `query=begins:-6hours:6hours`.
- Long ranges multiply cost — `from=2024-01-01&to=+1month` on `/conditions` bills as 31 accesses.
- Past dates on most endpoints require the historical add-on on the account.

## Advanced queries (`query=`)

Format: `query={property}:{operator}{value}` or `query={property}:{min}:{max}`.

| Operator | Meaning | Example |
|---|---|---|
| *(none)* | Exact match for strings; **greater than or equal** for numbers | `query=name:seattle` · `query=hail:80` |
| `min:max` | Inclusive range | `query=hail:40:80` |
| `!` | Not equal | `query=state:!va` |
| `^` | Starts with | `query=name:^minn` |
| `NULL` / `!NULL` | Is / is not null | `query=rh:NULL` · `query=temp:!NULL` |

Combine with `,` for **AND** and `;` for **OR**:

```
/places/search?query=name:seattle,state:wa      → name is seattle AND state is wa
/places/search?query=name:seattle;name:austin   → name is seattle OR austin
```

Query values use the API's native units, which are **metric** even when you read Fahrenheit fields
out of the response: `temp` and `dewpt` in Celsius, `wind`/`gust` in knots, `pressure` in millibars.
`query=temp:30` means ≥ 30 °C.

Valid query properties are per-endpoint — `endpoints.md` lists the names, `filters.md` explains them.

## Sorting

`sort={property}` or `sort={property}:{direction}`, where direction is `1` (ascending, default),
`-1` (descending), or `0` (disable sorting). Chain properties with commas; they apply in order.

```
/places/within?p=minneapolis,mn&radius=50miles&sort=pop:-1&limit=10
/observations/search?query=country:us&sort=temp:-1
/observations/search?query=country:us&sort=state,temp:-1&limit=500
```

With `closest`, distance wins over `sort`. With `within`, only `sort` applies.

## Output formats and reducing output

`format=json` (default) · `geojson` · `csv` · `tsv`.

```
/observations?format=csv&fields=ob.windMPH,ob.tempF,ob.humidity,id,obDateTime
```

CSV/TSV column order follows `fields` order, but nested groups (`ob.*`) must stay contiguous.

`fields` is the single biggest lever on payload size:

```
/observations/minneapolis,mn?fields=ob.tempF,ob.weather,ob.icon
/forecasts/minneapolis,mn?fields=periods.timestamp,periods.minTempF,periods.maxTempF
```

For arrays, `periods.maxTempF` and `periods[#].storms.hail` both work — the `[#]` form indexes into
the array explicitly.

## Batch requests

```
/batch/minneapolis,mn?requests=/observations,/forecasts,/alerts
/batch?requests=/observations/atlanta,ga,/observations/minneapolis,mn,/observations/seattle,wa
/batch/minneapolis,mn?requests=/observations,/forecasts%3Ffilter=6hr,/alerts%3Ffilter=all
```

- Parameters on the outer `/batch` request apply to every sub-request; a parameter inside an
  individual request overrides the global one.
- Inside `requests=`, URL-encode `?` as `%3F` and `&` as `%26`.
- Maximum 31 sub-requests. Each one bills separately.

## Responses

```json
{ "success": true, "error": null, "response": [ ...results... ] }
```

`response` is an **array** for multi-result actions and an **object** for `:id` requests — except
`/forecasts`, which always returns an array.

On error, `success` is `false`, `error` is `{ code, description }`, and `response` is `[]`. A
*warning* keeps `success: true` and still returns data, with `error` holding the warning code.

### Status codes

| Code | Meaning |
|---|---|
| 200 | Success (may still carry a warning) |
| 401 | Invalid `client_id` / `client_secret` |
| 404 | Unknown path — check the endpoint name |
| 429 | Rate limit or subscription-period limit reached |
| 5xx | Server-side error |

### Error codes

`deprecated` · `insufficient_scope` · `internal_error` · `invalid_client` · `invalid_coordinate` ·
`invalid_data` · `invalid_id` · `invalid_location` · `invalid_query` · `invalid_request` ·
`maxhits` · `maxhits_daily` · `maxhits_min` · `no_location` · `not_implemented` ·
`unauthorized_namespace`

Most common in practice:
- `invalid_client` — missing or wrong credentials.
- `unauthorized_namespace` — valid keys, but the request origin is outside the registered namespace.
- `invalid_location` — the place string didn't resolve; try a different supported format.
- `insufficient_scope` — the account/plan doesn't include that dataset.
- `not_implemented` — that action isn't supported on that endpoint.

### Warning codes

`warn_deprecated` · `warn_invalid_param` (parameter dropped — often a plan restriction) ·
`warn_location` (incomplete place, assumptions made) · `warn_no_data` (query returned nothing).

`warn_no_data` on a `closest` query usually means the radius is too small, not that the request is
wrong.

### Cost and rate-limit headers

| Header | Example |
|---|---|
| `X-Cost-Endpoint` | `conditions/summary` |
| `X-Cost-Tokens` | `30` |
| `X-Cost-Multipliers` | `endpoint=10; spatial=3; temporal=1` |
| `X-RateLimit-Limit-Minute` / `-Remaining-Minute` / `-Reset-Minute` | Minutely allowance, remaining, reset time (GMT) |
| `X-RateLimit-Limit-Period-Type` | The billing period duration |
| `X-RateLimit-Limit-Period` / `-Remaining-Period` / `-Reset-Period` | Period allowance, remaining, reset time (GMT) |

The multiplier header is `X-Cost-Multipliers`, **plural** — the Responses doc page lists it singular,
but the wire format is plural. Match both if you're parsing it.

`X-Cost-Tokens` = endpoint × spatial × temporal. Only **2xx** responses are charged; 4xx and 5xx are
free. Full cost model, the per-endpoint multiplier table, and route/batch rules are in
`access-cost.md`.
