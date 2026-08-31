---
name: weather-api
description: Build and run Xweather Weather API request URLs for data.api.xweather.com from plain-language requirements. Use when a task mentions the Xweather or legacy Aeris API, weather endpoints such as observations, conditions, forecasts, alerts, lightning, air quality, tropical cyclones, tides, or road weather; asks for an API URL or query; needs help debugging an empty or failed request; asks about access costs, endpoint multipliers, rate limits, or allowance usage; or needs guidance for the hosted Xweather MCP server at mcp.api.xweather.com, including availability, connection, authentication, and tool scoping. Also covers Xweather's attribution requirement — the 'Powered by Vaisala Xweather' credit and logo rules that apply wherever Xweather data or imagery is displayed.
compatibility: Skill instructions are provider-neutral. The bundled scripts/xwrequest.py needs Python 3 (standard library only) and network access to data.api.xweather.com.
license: MIT
metadata:
  author: Vaisala Xweather
  version: "0.14.0"
---

# Xweather Weather API URL builder

Turn a description of wanted weather data into a correct `data.api.xweather.com` URL — and, when
credentials are available, execute it and return the data alongside the URL.

## Request anatomy

```
https://data.api.xweather.com/{endpoint}/{action}/{:id}?{params}&client_id=…&client_secret=…
```

| Segment | Example | Notes |
|---|---|---|
| endpoint | `observations`, `conditions/summary` | *What* data. 59 of them — see `references/endpoints.md`. |
| action | `closest`, `within`, `search`, `route`, `contains`, `affects` | *How* to look it up. Omitted entirely for `:id` and `:all`. |
| `:id` | `seattle,wa`, `98109`, `44.97,-93.26`, `KMSP` | The place or record identifier. Goes in `p=` instead when an action occupies the path slot. |
| params | `filter=`, `query=`, `fields=`, `limit=`, `from=`/`to=`, `format=` | Shape the result. |
| credentials | `client_id` + `client_secret` | Query params on every request; no header form exists. |

`api.aerisapi.com` is the legacy host and still works — always emit `data.api.xweather.com`.

## Workflow

1. **Extract from the prompt:** what data, which place(s), what time, and what shape of answer
   (one record, N nearest, everything in an area, along a route, is-this-point-inside-a-polygon).
2. **Pick the endpoint.** Use the intent map below; confirm against `references/endpoints.md`.
3. **Pick the action** from the decision table below. Verify the endpoint actually supports it —
   `endpoints.md` lists supported actions per endpoint, and an unsupported one returns
   `not_implemented`.
4. **Add parameters.** `filter` and `query` tokens are endpoint-specific; only use tokens listed for
   that endpoint in `endpoints.md`. Read `references/filters.md` when choosing between similar
   tokens (`standard` vs `all` for alerts, `day` vs `daynight` vs `mdnt2mdnt` for forecasts) — grep
   for the `## /endpoint` heading rather than reading the whole file.
5. **Sanity-check against a documented example.** `references/examples.md` has the API's own example
   requests for every endpoint; `references/recipes.md` has 34 real-world queries by use case. If
   the request resembles one, copy its structure instead of inventing parameters.
6. **Emit the URL with its access cost** (see Access cost — always report it), then decide whether to
   run it (see Executing the request).

Never invent an endpoint, action, filter token, or query property. If unsure whether one exists,
check `endpoints.md`, or refetch the live catalog:

```bash
curl -s https://www.xweather.com/docs/api/weather-api/endpoints
```

That JSON (`{ endpoint: {...}, action: {...} }`) is the authoritative, always-current list of every
endpoint with its supported actions, params, filters, query properties, and sort fields — it is what
`references/endpoints.md` was generated from. Use it when a user asks about something the reference
doesn't cover, or when a request fails with `invalid_request` / `not_implemented`.

## Intent → endpoint

| The user wants | Endpoint |
|---|---|
| "What's the weather right now" — blended current conditions, global | `/conditions/{place}` |
| An actual reporting station's observation | `/observations/{place}` or `/observations/closest?p=…` |
| Forecast — daily, day/night, hourly, 3-hourly | `/forecasts/{place}?filter=day\|daynight\|1hr\|3hr` |
| "Will it rain in the next hour" | `/conditions/{place}?filter=minutelyprecip` |
| Hourly series across a past or future window | `/conditions/{place}?from=…&to=…` |
| Yesterday's / a past day's high, low, precip total | `/conditions/summary/{place}?from=-1day` or `/observations/summary/{place}` |
| Hour-by-hour history at a station | `/observations/archive/{place}?for=2024-06-05` (this endpoint takes `for=`, not `from`/`to`) |
| 30-year climate normals | `/normals/{place}?filter=daily\|monthly\|annual` |
| A plain-English weather summary sentence | `/phrases/summary/{place}` |
| Warnings, watches, advisories | `/alerts/{place}` — counts across a region: `/alerts/summary` |
| Lightning strikes near a point | `/lightning/closest?p=…&radius=25miles&limit=10` |
| Lightning/thunderstorm nowcast, next ~60 min | `/lightning/threats` |
| Radar-derived storm cells, hail, rotation, TVS | `/stormcells/{place}` · `/stormcells/closest` · `/stormcells/summary` |
| Hail nowcast · localized threat summary | `/hail/threats` · `/threats/{place}` |
| Confirmed storm damage reports (insurance, verification) | `/stormreports/search?query=state:…&filter=hail` |
| Hurricanes / typhoons, active or historical | `/tropicalcyclones` · `/tropicalcyclones/archive` |
| SPC severe convective outlook | `/convective/outlook/contains?p={place}` or `/convective/outlook/{place}` |
| Is this location in a drought area | `/droughts/monitor/contains?p={place}` or `/droughts/monitor/{place}` |
| Wildfires · fire weather outlook | `/fires/closest?p=…` · `/fires/outlook` |
| Earthquakes | `/earthquakes/closest` or `/earthquakes/within` |
| Air quality — current, forecast, historical, index only | `/airquality/{place}` · `/airquality/forecasts` · `/airquality/archive` · `/airquality/index` |
| Health or activity index (migraine, golf, biking, …) | `/indices/{type}/{place}` |
| Operational risk score for an activity | `/impacts/{activity}/{place}` |
| Sunrise, sunset, twilight, moonrise · moon phases | `/sunmoon/{place}` · `/sunmoon/moonphases` |
| Tides | `/tides/{place}?from=now&to=+1day` |
| Offshore / marine — waves, swell, sea temp | `/maritime/{place}` · `/maritime/archive` |
| Road conditions and driving risk | `/roadweather/{place}` · `/roadweather/analytics` · `/roadweather/conditions` |
| River and lake gauges, flood stage | `/rivers/closest` · `/rivers/gauges` |
| Solar irradiance for PV siting or yield | `/renewables/irradiance/summary` · `/archive` · `/tmy` |
| Hail history for a location | `/hail/archive/{place}?from=…&to=…` |
| Lightning climatology · wind-turbine strike risk | `/lightning/density/{place}` · `/lightning/turbinerisk/{place}?height=100m` |
| Geocoding, place/ZIP/airport lookup, nearby cities | `/places/search` · `/places/closest` · `/places/postalcodes` · `/places/airports` · `/countries` |
| Hyperlocal forecast from an Xcast sensor | `/xcast/forecasts/{device_id or place}` |
| **Any of the above along a driving route** | append `/route` and pass `p=lat,lon;lat,lon;…` |

`/conditions` vs `/observations` is the most common fork: `/conditions` is a modeled, gap-free blend
available for any coordinate on earth; `/observations` is what a physical station actually reported.
Reach for `/observations` when the user says "station", "METAR", "airport", or names a station id.

## Action decision table

| The question | Action | Shape |
|---|---|---|
| "…for Denver" | `:id` | `/alerts/denver,co` |
| "…everywhere / all active" | `:all` | `/tropicalcyclones?filter=all` |
| "…nearest N to me" | `closest` | `/lightning/closest?p=…&radius=25miles&limit=10` |
| "…inside this box / circle / polygon" | `within` | `/earthquakes/within?p=43.23,-96.92,45.62,-91.31&limit=10` |
| "…matching these criteria, anywhere" | `search` | `/observations/search?query=country:us&sort=temp:-1` |
| "…along this route" | `route` | `/observations/route?p=44.96,-93.27;44.91,-93.5` |
| "…is this point inside a warned/outlook/drought area" | `contains` | `/convective/outlook/contains?p=denver,co` |
| "…which towns does this storm/quake affect" | `affects` | `/stormcells/affects?p=…` |

**The location goes in `p=` for every action except `:id` and `:all`** — the path slot after the
endpoint is where the action name lives, so `/convective/outlook/contains/denver,co` fails with
`invalid_request: Invalid Action: contains/denver,co`. It's `/convective/outlook/contains?p=denver,co`.

Two more traps: `limit` defaults to **1**, so `closest`/`search`/`within` without it return a single
record; and `closest` with too small a `radius` returns `warn_no_data` rather than an error.

On polygon endpoints, `/{endpoint}/{place}` (the `:id` form) is a documented shorthand for
`contains` — `/droughts/monitor/san diego,ca` ≡ `/droughts/monitor/contains?p=san diego,ca`.

## Parameter essentials

| Parameter | Use |
|---|---|
| `p` | The place, when an action occupies the path slot. Also carries `within` geometry and `route` point lists. |
| `limit` / `skip` | Primary result count / offset. **Default `limit` is 1.** |
| `plimit` / `pskip` / `psort` | Same, for sub-elements (`periods` entries). |
| `radius` / `minradius` / `mindist` | Search radius (`25miles`, `10km`), donut inner radius, minimum spacing between returned points. |
| `filter` | Endpoint-specific selectors. `,` = AND, `;` = OR. |
| `query` | Value filtering, `property:value`. `,` = AND, `;` = OR. |
| `sort` | `property:-1` descending, `:1` ascending. |
| `from` / `to` / `for` | Range, or a single valid time. `now`, `today`, `friday`, `+3days`, `-12hours`, `2024-03-23`, `2024-06-05 16:00:00`. |
| `fields` | Comma list of dot-notated properties to return. |
| `format` | `json` (default), `geojson`, `csv`, `tsv`. |

Two things that bite:

- **`query=` values are metric**, regardless of which units you read back out. `temp`/`dewpt` in
  Celsius, `wind`/`gust` in knots, `pressure` in millibars. `query=temp:30` is ≥ 30 °C.
- **A bare number in `query=` means "greater than or equal"**, not "equals". Use `min:max` for a
  range, `!` for not-equal, `^` for starts-with, `NULL`/`!NULL` for null checks.

Full detail — every parameter, all place formats, date forms, query operators, sorting, batch
requests, response envelope, error and warning codes, cost headers — is in
`references/parameters.md`.

## Access cost — always report it

One HTTP request is not one access. Every URL you hand over must come with what it will cost against
the subscription allowance, unprompted — a `/impacts` request costs 25× a `/forecasts` one, and a
200-point route request costs 200×, which is not something a user should discover from an invoice.

```
accesses = endpoint multiplier × spatial multiplier × temporal multiplier
```

**The spatial multiplier is always 1** — no current endpoint uses it, so query area, radius and
geometry never affect cost. What's left is:

```
accesses = endpoint multiplier × intervals requested
```

The **endpoint multiplier** is a fixed constant: `Cost: xN` on each entry in
`references/endpoints.md`, or the grouped table in `references/access-cost.md`. The **temporal
multiplier** is the number of days or hours a single request covers, on endpoints that return a series
over a range — `/conditions/summary` bills one access per day, so a 30-day request is 30 accesses, not
one.

Both are knowable up front, so give a real number:

> `https://data.api.xweather.com/airquality/beijing,cn?filter=china&client_id={client_id}&client_secret={client_secret}`
> **Cost: 5 accesses** — `/airquality` is ×5, one point in time.

> `https://data.api.xweather.com/conditions/summary/minneapolis,mn?from=-30days&to=now&client_id={client_id}&client_secret={client_secret}`
> **Cost: 30 accesses** — `/conditions/summary` is ×1 and bills one access per day, so 30 days of
> summaries is 30 accesses. Shortening the range is the only way to reduce it.

> `https://data.api.xweather.com/lightning/within?p=43.23,-96.92,45.62,-91.31&limit=500&client_id={client_id}&client_secret={client_secret}`
> **Cost: 10 accesses** — `/lightning` is ×10. The multi-state bounding box costs nothing extra; area
> is not a cost factor.

Don't tell anyone to shrink a radius or tighten a bounding box to save accesses — it doesn't work.
Where you're unsure whether an endpoint bills per interval, name the range as the thing that could
multiply the cost and point at `X-Cost-Tokens`, rather than inventing a number.

When you actually run the request, `X-Cost-Tokens` is the exact charge — quote it instead of the
estimate.

Cases with an exact documented rule, worth calling out whenever they apply:

- **`route` charges one access per point**, times the endpoint multiplier. 200 points against
  `/roadweather/analytics` (×10) is ~2,000 accesses. Always state the point count and the product.
- **`batch` charges each sub-request separately.** It saves round trips, not accesses. Max 31.
- **4xx and 5xx cost nothing.** Only 2xx is charged, so retrying a corrected URL is free.
- **`fields=` and `limit` don't reduce cost.** They shrink the payload, not the charge.

The expensive endpoints, worth flagging when one is chosen: `/impacts` (×25); `/hail/archive`,
`/hail/threats`, `/lightning/analytics` (×12); `/lightning`, `/lightning/archive`,
`/lightning/threats`, `/renewables/irradiance/summary`, `/roadweather/analytics` (×10); `/airquality`
and its archive/forecasts, `/maritime/archive`, `/roadweather/conditions` (×5). If a cheaper endpoint
answers the same question — `/airquality/index` (×1) for just the index, `/lightning/summary` (×1) for
aggregate counts, `/roadweather` (×1) without analytics fields — say so.

Full model, the complete multiplier table, and cost-reduction tactics: `references/access-cost.md`.

## Executing the request

Default behavior with no credentials: **produce the URL only**, with `{client_id}` and
`{client_secret}` placeholders, and explain what it returns. Mention that keys from the API Keys page
of https://data.portal.xweather.com/account/keys let you run it and return live data.

When the user supplies a client id and secret — in the prompt, in a `.env`, or already exported —
run the request and return **both the response and the URL**. Never leave the URL out; it is half
the deliverable.

Preferred: put the credentials in the environment and use the bundled helper, which keeps the secret
out of the command line and out of its own output.

```bash
export XWEATHER_CLIENT_ID='…' XWEATHER_CLIENT_SECRET='…'
python3 scripts/xwrequest.py '/observations/seattle,wa?filter=allstations&limit=3'
```

Invoke it as `python3 scripts/xwrequest.py`, resolved relative to this skill's directory. Some
clients also expose it as a bare `xwrequest` command on PATH — use that if available, but don't
assume it.

It prints the URL with credential placeholders, the HTTP status, the accesses charged with the
`endpoint`/`spatial`/`temporal` breakdown, the remaining minutely and period allowance, and the
pretty-printed body. `--post file.json` sends a JSON body for long `/route` requests; `--raw` skips
pretty-printing for CSV/TSV.

Plain `curl` works too, with the credentials referenced as shell variables rather than pasted:

```bash
curl -s "https://data.api.xweather.com/observations/seattle,wa?limit=3&client_id=$XWEATHER_CLIENT_ID&client_secret=$XWEATHER_CLIENT_SECRET"
```

### Handling credentials

- **Show the URL with `{client_id}` / `{client_secret}` placeholders in your reply**, not the literal
  key values — replies get pasted into tickets, chats, and commits. If the user explicitly asks for
  a fully populated copy-paste URL, give it to them; that's their call to make.
- Don't write credentials into a file, a script, or a committed config unless asked. If they're
  already in a `.env` that the project reads, use that.
- A `401` / `invalid_client` means the keys are wrong. `unauthorized_namespace` means the keys are
  valid but the request came from outside the domain or bundle id they were registered against —
  common when testing server-side keys locally, and not something a different URL will fix.

### What to report back

1. The URL, with credential placeholders.
2. **The access cost** — `X-Cost-Tokens` when the request ran, the endpoint-multiplier floor when it
   didn't. This goes in every reply that contains a URL, whether or not the user asked.
3. A one-line reading of the data that answers what was actually asked ("62 °F, overcast, wind
   9 mph from the NNE at KBFI as of 14:53 local"), not just a JSON dump.
4. The relevant slice of the response — trimmed if it's long, since a 168-period hourly forecast is
   not a useful thing to paste in full.
5. Anything worth knowing: warnings in the `error` field even on a 200, a cost that's high because of
   the time range, remaining allowance if it's running low, or an empty result that means "widen the
   radius".

If the reply contains several URLs, give each its own cost line and a total.

## Debugging a request that doesn't work

| Symptom | Likely cause |
|---|---|
| `invalid_location` | Place string didn't resolve — try another supported format (ZIP, `city,state`, lat/lon). |
| `warn_location` on a 200 | No state given for a US/CA city; the API guessed by population. Add the state. |
| `warn_no_data`, empty array | `closest`/`within` radius too small, or the time window has no records. Widen it. |
| One result when several were expected | `limit` defaults to 1. |
| `not_implemented` | That action isn't supported on that endpoint — check `endpoints.md`. |
| `warn_invalid_param`, parameter silently dropped | Parameter not supported on that endpoint, or not included in the account's plan. |
| `insufficient_scope` | Dataset isn't on the subscription (historical add-on, premium polygons, etc.). |
| HTTP 200 with `invalid_request: Invalid Action: …` | A place was put in the path *after* an action name. Move it to `p=`. |
| `404` | Endpoint path is wrong. |
| `429` with `maxhits_min` / `maxhits` | Per-minute or subscription-period access limit hit — check the `X-RateLimit-*` headers and see `access-cost.md`. |
| Nothing wrong, but huge response | Add `fields=`, lower `limit`/`plimit`. |

## The Xweather MCP server — an alternative to building URLs

Xweather runs a hosted MCP server at **`https://mcp.api.xweather.com/mcp`**. Connected to an MCP
client, it turns a plain-language question into the necessary Xweather calls directly — no endpoint,
action, filter, or field names to get right.

Raise it when the user is asking questions *of* the weather rather than building an application
against the API: "what's the lightning risk in Tampa," "compare this week's rainfall for Seattle and
Portland." Keep using this skill for URLs when they need a request to embed in their own code, want to
understand the API's structure, or are debugging an existing integration. The two complement each
other — the MCP server answers questions; this skill produces artifacts.

**It is not bundled with this plugin.** Adding it is one command:

```bash
claude mcp add --transport http xweather https://mcp.api.xweather.com/mcp \
  --header "Authorization: Bearer CLIENT_ID_CLIENT_SECRET"
```

Add `--scope user` to make it available across all projects, or `--scope project` to share it with a
repo via `.mcp.json`.

### Authentication

The token is the **client id and secret joined by a single underscore** — `abc123_def456` — not two
separate parameters. Three ways to pass it:

| Method | When |
|---|---|
| `Authorization: Bearer <client_id>_<client_secret>` | Preferred for clients that support custom request headers. |
| `?api_key=<client_id>_<client_secret>` | For clients that cannot set custom request headers. |
| OAuth 2.0 | Supported, but verify current Xweather OAuth guidance before recommending it because client interoperability varies. |

### Scoping the tools

Six tag groups exist: `general` (current conditions, impacts, air quality), `forecast`, `summary`
(aggregations), `tropical`, `lightning`, `roadweather`. Filter them with query parameters:

```
https://mcp.api.xweather.com/mcp?include_tags=forecast,summary
```

Also `exclude_tags`, `include_tools`, `exclude_tools` (exact tool names like
`xweather_get_current_weather`). Precedence runs `exclude_tools` → `exclude_tags` → `include_tools` →
`include_tags`.

Recommend scoping when the user has other MCP servers connected — loading all six groups crowds the
model's tool choices, which is the reason Xweather documents the filters at all.

### Diagnosing a failed connection

| Response | Meaning |
|---|---|
| `401 invalid_token` | Missing or wrong token. The body suggests clearing tokens and re-registering — that's generic MCP OAuth advice and doesn't apply to bearer-key auth; check the token value instead. |
| `500` | Usually a malformed token: both halves and exactly one underscore are required. |
| `403` | Valid credentials, but the subscription doesn't include MCP access. |

MCP access may need a specific subscription tier, so "is it available to me?" is an account question
— point the user at their account executive rather than guessing.

## Attribution is required

Xweather requires attribution wherever its data or imagery is displayed. This applies to **all
products** — Weather API, Raster Maps, and MapsGL alike. Build it into anything you produce, and say
so when handing over code or URLs that will end up in front of users.

The minimum is a link to `https://www.xweather.com/` reading "Powered by Vaisala Xweather":

```html
<a href="https://www.xweather.com/" target="_blank" title="Powered by Vaisala Xweather">Powered by Vaisala Xweather</a>
```

The logo may be substituted for the "Xweather" text. Light and dark variants exist in SVG and PNG:

```html
<a href="https://www.xweather.com/" target="_blank" title="Powered by Vaisala Xweather">
  <img src="https://www.xweather.com/assets/logos/vaisala-xweather-logo-dark.svg" alt="Vaisala Xweather" height="40" />
</a>
```

Swap `-dark` for `-light` over a dark background, or `.svg` for `.png`. Using the logo brings rules:
keep it unmodified, leave at least a **10px buffer** of space around it, and only adjust lightness or
opacity in greyscale. Don't rotate it, don't recolour it (monotone black or white excepted), and don't
use the symbol without the Xweather name.

Full guide: https://www.xweather.com/docs/weather-api/resources/attribution

## Reference files

- `references/endpoints.md` — every endpoint: description, coverage, data range, update interval,
  cost multiplier, and the exact supported actions / params / filters / query props / sort fields.
- `references/access-cost.md` — the access-cost model, every endpoint grouped by multiplier, what
  raises the spatial and temporal factors, the exact `route`/`batch`/error rules, cost-reduction
  tactics, and the cost + rate-limit headers.
- `references/parameters.md` — request anatomy, every parameter, all 8 actions with their geometry
  and POST forms, place formats, date forms, query operators, sorting, output formats, batch
  requests, response envelope, error/warning codes, cost headers.
- `references/filters.md` — what each endpoint's `filter` tokens and `query` properties actually
  mean. Search for the `## /endpoint` heading you need rather than reading it end to end.
- `references/examples.md` — the API docs' own example requests for every endpoint, with
  descriptions. The best model for correct URL shape.
- `references/recipes.md` — 34 real-world queries by industry/use case, plus the patterns behind
  them.
- `scripts/xwrequest.py` — runs a request using `XWEATHER_CLIENT_ID` / `XWEATHER_CLIENT_SECRET` from
  the environment; prints the placeholder URL, status, accesses charged with the multiplier
  breakdown, remaining allowance, and the body.
