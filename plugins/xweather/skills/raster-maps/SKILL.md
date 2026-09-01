---
name: raster-maps
description: This skill should be used to build Xweather Raster Maps image URLs (maps.api.xweather.com) — either static map images or XYZ map tile URLs for Leaflet, Mapbox, Google Maps, OpenLayers and similar libraries — from a description of the weather imagery wanted. Use it whenever a task mentions Raster Maps, maps.api.xweather.com, maps.aerisapi.com, an Xweather weather map layer or overlay (radar, satellite, alerts, temperatures, lightning, tropical cyclones, air quality, base maps, admin overlays), a weather map image or tile layer, layer opacity/blur/blend/scale-hsla modifiers, or asks how Raster Maps usage is measured — map units, tile counts, the daily allowance, or how many accesses a static map or tile layer will consume. Also covers Xweather's attribution requirement — the 'Powered by Vaisala Xweather' credit and logo rules that apply wherever Xweather data or imagery is displayed.
compatibility: Skill instructions are provider-neutral. The bundled scripts/xwmap.py needs Python 3 (standard library only) and network access to maps.api.xweather.com.
license: MIT
metadata:
  author: Vaisala Xweather
  version: "0.14.1"
---

# Xweather Raster Maps URL builder

Turn a description of wanted weather imagery into a `maps.api.xweather.com` URL — as a standalone
static image or as a tile template for an interactive mapping library.

This is a different product from the Weather API: different host, different URL grammar, and
credentials sit **in the path**, not in the query string.

```
https://maps.api.xweather.com/{client_id}_{client_secret}/{layers}/…/{offset}.{format}
```

## Two output methods — ask which one

Every Raster Maps request is one of two shapes, and they are not interchangeable:

| | Static map | Map tiles |
|---|---|---|
| Produces | A single finished image | A 256×256 tile template a library fetches many of |
| Use when | Email, report, dashboard panel, `<img>` tag, Slack, PDF | Leaflet / Mapbox / Google Maps / OpenLayers / Apple Maps |
| Path | `{layers}/{w}x{h}/{place},{zoom}/{offset}.{fmt}` | `{layers}/{z}/{x}/{y}/{offset}.{fmt}` |
| Interactive | No — no pan or zoom | Yes |

**If the user hasn't said which one they want, ask before generating anything.** Use
Ask a direct either/or question — a structured-choice prompt if the agent has one, plain text otherwise.
Don't guess from weak signals and don't produce both by default — a tile template pasted into an
`<img>` tag renders one 256-pixel square, and a static URL handed to Leaflet fails outright.

Signals strong enough to skip the question: the user names a mapping library, says "tile layer" or
"XYZ", or gives `{z}/{x}/{y}` (→ tiles); or names pixel dimensions, says "image", "PNG for a
report", or shows an `<img>` tag (→ static).

## Workflow

1. **Determine the output method** — ask if not already clear (above).
2. **Pick the layers.** Use the intent map below and confirm codes against `references/layers.md`.
   Order matters: they composite left to right, so base map first, weather next, labels last.
3. **Add the geography.** Static: `place,zoom` or a `south,west,north,east` bounding box. Tiles: the
   library substitutes `{z}/{x}/{y}` — leave the placeholders in.
4. **Add the time offset.** `current` unless the user wants past or forecast imagery.
5. **Pick the format.** `png` for tile overlays (transparency is mandatory); `png` or `jpg` for
   static maps that include their own base layer.
6. **Apply modifiers** if the request implies them — opacity, blur, blend, recolour. See
   `references/modifiers.md`.
7. **Report the URL with its map-unit cost** (see Map units), then handle credentials (see below).
8. **Include the attribution.** Any markup you hand over — an `<img>` tag, a tile layer, a template —
   needs the Xweather credit alongside it. See "Attribution is required" below.

Never invent a layer code. Check `references/layers.md`, or refetch the live catalog:

```bash
curl -s https://www.xweather.com/docs/api/maps/layers
```

That JSON (`{ layers: [{ id, title, description, multiplier, modifiers, categories, dataRange,
dataCoverage, updateInterval }] }`) is the authoritative layer list and is what
`references/layers.md` was generated from.

## Intent → layer

| The user wants | Layer code |
|---|---|
| Radar | `radar` (regional, higher res) · `radar-global` (satellite-derived fill where radar is absent) |
| Future radar | `fradar` — add `-hrrr` / `-nam` / `-gfs` to pick the model |
| *Forecast of any `f`-prefixed layer* | Raster Maps splits observed from forecast — `temperatures` vs `ftemperatures`. **MapsGL doesn't**: one layer spans both there, so don't carry `f`-prefixed codes across. |
| Satellite | `satellite-geocolor` (the good-looking default) · `satellite-visible` · `satellite-infrared-color` · `satellite-water-vapor` |
| Watches and warnings | `alerts` — `-severe`, `-fire`, `-flood`, `-winter`, `-heat`, `-wind`, `-surge`, `-frost-freeze`; `-watches` / `-warnings` |
| Temperature | `temperatures` · forecast `ftemperatures` · labels `temperatures-text` |
| Feels-like, dew point, humidity, wind, gusts, visibility | `feels-like` · `dew-points` · `humidity` · `wind-speeds` · `wind-gusts` · `visibility` — each has an `f`-prefixed forecast twin and a `-text` label variant |
| Lightning | `lightning-strikes` (**×10**) · `lightning-flash` (×1) · `lightning-strike-density` (×1) |
| Storm cells, storm reports | `stormcells` · `stormreports` |
| Severe outlook, fire outlook, drought | `convective` · `fires-outlook` · `drought-monitor` |
| Hurricanes | `tropical-cyclones` plus the `tropical-cyclones-*` family (positions, track lines, forecast cones, icons, names) |
| Air quality | `air-quality-index` / `air-quality-index-categories` (×1) · individual pollutants and national scales (**×5**) |
| Snow, ice, precip accumulation | `snow-depth` · `fqsf-accum` · `fice-accum` · `fqpf-accum` · `precip` |
| Marine | `maritime-wave-heights` · `maritime-swell-*` · `maritime-sst` · `maritime-currents` · `maritime-tides` |
| Fronts and pressure | `surface-analysis` · `surface-analysis-fronts` · `surface-analysis-pressure` |
| Base map | `flat` · `flat-dk` · `terrain` · `terrain-dk` · `blue-marble` |
| Borders, cities, roads | `admin` (combined) · `admin-cities` / `-dk` · `states` · `counties` · `countries-outlines` · `roads` · `interstates` |
| Clip weather to land or water | the `Masks` layers — `land-flat`, `water-flat`, `clip-us-terrain`, … |

Layers with a **Modifier** group in `layers.md` take dash-joined options — `alerts-severe`,
`alerts-severe-warnings`, `temperatures-rtma`, `fradar-hrrr`. One option per group; groups combine.

A few modifier groups are described in the catalog without enumerated options (`radar`'s Region says
"either US or Global" but lists no values). Treat those as unconfirmed: say the modifier exists, and
check the layer's doc page or test the request rather than emitting a guessed suffix.

A conventional stack is base → weather → labels:

```
flat-dk,alerts,radar,admin
terrain,temperatures:blend(overlay),admin-cities
```

Maximum **10 layers** per request.

## URL shapes

When the URL goes into a page, the attribution goes with it:

```html
<img src="https://maps.api.xweather.com/{client_id}_{client_secret}/flat,radar,admin/800x600/minneapolis,mn,7/current.png"
     width="800" height="600" alt="Radar" />
<a href="https://www.xweather.com/" target="_blank" title="Powered by Vaisala Xweather">Powered by Vaisala Xweather</a>
```

For a tile layer, most mapping libraries take it as an attribution option instead — Leaflet and
Mapbox GL both accept an `attribution` string on the layer or source, which is the idiomatic place to
put it.

**Static, centre point** — place and zoom share one comma-joined segment:

```
https://maps.api.xweather.com/{client_id}_{client_secret}/flat,radar,admin/800x600/minneapolis,mn,7/current.png
https://maps.api.xweather.com/{client_id}_{client_secret}/radar/300x300/44.96,-93.27,7/current.png
```

**Static, bounding box** — `south,west,north,east`:

```
https://maps.api.xweather.com/{client_id}_{client_secret}/flat,radar,admin/320x320/30.1010,-85.9578,33.0948,-82.4421/current.png
```

Three comma-separated numbers means `lat,lon,zoom`; four means a bounding box. That count is the only
thing telling them apart, so a dropped coordinate silently changes what the request means.

**Tiles** — hand over the template with placeholders intact:

```
https://maps.api.xweather.com/{client_id}_{client_secret}/radar/{z}/{x}/{y}/current.png
https://maps{s}.api.xweather.com/{client_id}_{client_secret}/radar/{z}/{x}/{y}/current.png   # with subdomains: '1234'
```

Pair a tile URL with the matching library snippet — Leaflet, Mapbox GL, Google Maps, and OpenLayers
examples are in `references/url-formats.md`. Give the snippet, not just the URL; the URL alone is
rarely enough to get a layer on screen.

**Time offset:** `current` / `latest`, a relative offset (`-10minutes`, `+1hour`, `-3days`; integers
only, so `-90minutes` not `-1.5hours`), or a UTC valid time `YYYYMMDDhhiiss`.

**Format:** `png` (true colour), `png32`–`png256` (indexed, smaller), `jpg` / `jpg70`–`jpg100`,
`webp`. Prefix with `@2x` for retina. **Tile overlays must be `png` or `webp`** — JPEG has no alpha,
so a JPEG tile paints an opaque block over the base map.

Size limits: 5000×5000 on paid plans, 2000×2000 on the free developer trial.

## Map units — report the cost with the URL

Raster Maps measures usage in **map units**, against a **daily** allowance set by the subscription.
One map unit = **one 256×256 tile carrying one ×1 layer**.

```
tiles     = ceil(width / 256) × ceil(height / 256)
map units = tiles × Σ(multiplier of each layer)
```

Most layers are ×1, but `lightning-strikes` and the `lightning-all` family are **×10**, and
individual air-quality pollutant and national-index layers are **×5**. A layer listed twice counts
twice.

**Show the arithmetic, not just the total** — the division is where people get surprised:

> `flat,alerts,radar` at 800×600:
> ```
> 800 / 256 = 3.125 → 4 columns
> 600 / 256 = 2.34  → 3 rows
> 4 × 3 = 12 tiles × 3 layers = 36 map units
> ```

> `flat,lightning-strikes` at 800×600 → 12 tiles × (1 + 10) = **132 map units**, because
> `lightning-strikes` is a ×10 layer. `lightning-flash` or `lightning-strike-density` are ×1 if
> either answers the question.

Two facts worth volunteering, because both surprise people:

> **Combining layers into one request doesn't reduce map units.** `flat,radar,admin` as a single
> comma-joined request costs the same 3× as three separate layers — the docs are explicit that two
> layers cost 2× "either as separate layers or combined". Combining saves round trips and latency,
> not units.
>
> **Cost is quantised in 256-pixel steps.** 512×512 and 500×500 are both 4 tiles; 520×520 jumps to 9.
> Sizing just under a tile boundary is free savings.

### Static vs. interactive

For a **static image** the number is exact — you control the dimensions, so the calculation above is
the answer.

For **tiles**, it's an estimate and you should say so. A ~800×600 viewport is roughly 12 tiles, but
the container's real size and the map's centre shift it, and libraries commonly pull an extra row and
column to make panning smooth. More importantly: **every pan and zoom renders new tiles, each costing
again**, so an interactive map's lifetime cost is driven by user interaction rather than by initial
load. Give a per-viewport figure and name that caveat rather than implying a total.

**Caching is the biggest real-world lever.** Tiles and static images are cached in browser memory for
a period tied to the layer's update interval — radar refreshes every ~6 minutes, temperatures roughly
hourly — so re-requests inside that window don't generate new units. Native apps should implement
equivalent memory or file caching.

If the user is building something animated, multi-layer, and heavily interactive, mention that
**MapsGL bills completely differently** — in 5-minute sessions where layer count and interaction are
free — and may be far cheaper for that pattern. See the `mapsgl` skill.

Usage is visible in the account dashboard, with a Usage tab for history and per-application
breakdown; stats lag slightly behind real time.

`scripts/xwmap.py … --estimate-only` computes all of this from a path, pulling live multipliers from the
catalog. Full model, the multiplier tables, and reduction tactics: `references/map-units.md`.

## Credentials and returning the image

**Without credentials:** hand over the URL with `{client_id}` and `{client_secret}` placeholders and
say where keys come from (the API Keys page at https://data.portal.xweather.com/account/keys). Nothing
else to do.

**With credentials — ask before fetching.** If the user has supplied a client id and secret, ask
whether they want the image requested and shown, or just the URL to copy. Ask; don't assume. Fetching spends real map units against their allowance, and for a tile template there's no
single meaningful image to return anyway.

If they say yes:

```bash
export XWEATHER_CLIENT_ID='…' XWEATHER_CLIENT_SECRET='…'
python3 scripts/xwmap.py 'flat,radar,admin/800x600/minneapolis,mn,7/current.png' -o radar.png
```

Invoke it as `python3 scripts/xwmap.py`, resolved relative to this skill's directory. Some clients
also expose it as a bare `xwmap` command on PATH — use that if available, but don't assume it.

The script prints the placeholder URL and the map-unit estimate, saves the image, and detects the
JSON error body that Raster Maps returns in place of an image on failure. Read the saved file back
to view it, and say where it was written.

For a **tile** URL, offer to render one representative tile (or a small static equivalent of the same
layers) rather than pretending a `{z}/{x}/{y}` template resolves to one image.

### Handling credentials

- **Show the URL with `{client_id}` / `{client_secret}` placeholders in your reply**, not the literal
  keys — Raster Maps URLs get pasted into HTML, committed configs, and shared dashboards, and the
  credentials are right there in the path. If the user explicitly asks for a populated copy-paste
  URL, give it to them; that's their call.
- Don't write credentials into a file or committed config unless asked. Note that a tile URL used in
  client-side JavaScript exposes the key pair to anyone viewing the page — which is why Xweather ties
  each key pair to a registered namespace (domain or bundle id).
- `403` with `{"error":{"code":"authorization_error"}}` means bad keys or a namespace mismatch. Note
  this envelope differs from the Weather API's `{"success","error","response"}`, and the status is
  403 rather than 401.

## Gotchas

| Symptom | Cause |
|---|---|
| Tile layer hides the base map entirely | JPEG format on an overlay tile. Use `png` or `webp`. |
| One small square instead of a map | A tile URL used as a static image. Switch to the static form. |
| Blank or transparent image | Layer has no data for that place or time — check the layer's `Coverage` and `Range` in `layers.md`. Radar is regional; `radar-global` fills the gaps. |
| Map is centred wrong or wildly zoomed | Three vs. four coordinates — `lat,lon,zoom` vs. bounding box. |
| Labels buried under the weather | Put `admin` / `admin-cities` last in the layer list. |
| Nothing renders at high zoom | Past the layer's max zoom, or past its data range for the requested offset. |
| Blend has no effect | Two blends on one layer — only one is allowed per layer. |
| Layer code rejected | A legacy alias (`sat`, `cities`, `frad`) — use the catalog code (`satellite-geocolor`, `admin-cities`, `fradar`). |
| Higher bill than expected | A ×10 lightning or ×5 air-quality layer, a layer plotted twice, or an interactive map being panned. |

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

- `references/layers.md` — every layer by category: code, description, multiplier, coverage, data
  range, update interval, and each layer's dash-joined modifier options.
- `references/url-formats.md` — static centre-point and bounding-box forms, tile form, library
  snippets for Leaflet / Mapbox GL / Google Maps / OpenLayers, time offsets, image-quality
  extensions, layer combination rules, error envelope.
- `references/modifiers.md` — colon-attached modifiers: opacity, blur, gray, invert, all blend modes,
  and `scale-hsla` with the documented tint / recolour / heatmap / shadow recipes.
- `references/map-units.md` — the cost model, layers grouped by multiplier, caching, and how to
  reduce consumption.
- `scripts/xwmap.py` — estimates map units from a path (`--estimate-only`) and fetches
  the image using `XWEATHER_CLIENT_ID` / `XWEATHER_CLIENT_SECRET` from the environment.

Related: the `weather-api` skill covers the Weather **data** API
(`data.api.xweather.com`), and `mapsgl` covers the MapsGL JavaScript SDK. Raster Maps is
the server-rendered image product — reach for MapsGL instead when the user wants animated,
styleable, client-side layers.
