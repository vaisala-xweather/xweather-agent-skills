# Map units — what a map costs

Raster Maps bills in **map units**, not requests. One map unit = one 256×256 tile carrying one ×1
layer. Subscriptions grant a daily map-unit allowance.

```
tiles     = ceil(width / 256) × ceil(height / 256)
map units = tiles × Σ(multiplier of each layer in the request)
```

The layer term is a **sum over the layer list, not a count** — most layers are ×1, but lightning is
×10 and air quality is ×5, and a layer listed twice is counted twice.

The docs state the formula as `tiles × layers` and their worked examples use ×1 layers only, so that
form is a special case of the sum above. Where a request mixes multipliers, sum them.

## Static maps

Exact and predictable — you control the dimensions.

800×600 with a single radar overlay:

```
800 / 256 = 3.125 → 4 columns
600 / 256 = 2.34  → 3 rows
4 × 3 = 12 tiles × 1 layer = 12 map units
```

The same map with `flat,alerts,radar` (three ×1 layers): 12 × 3 = **36 map units**.

The same map with `flat,lightning-strikes` (×1 + ×10): 12 × 11 = **132 map units**.

## Interactive tile maps

Estimated, not exact — the mapping library decides how many tiles to pull.

An 800×600 map viewport is ~12 tiles, so a single radar layer is ~12 map units and two layers ~24.
Beyond that:

- The container's actual size, and where the map is centred, shift the count.
- Many libraries request an extra row and column to make panning feel smooth.
- **Every pan and zoom renders new tiles**, each costing again. An interactive map's lifetime cost is
  driven by user interaction, not by the initial load.

Always describe interactive-map figures as per-viewport estimates, and say that panning and zooming
add more.

## Layer multipliers

### ×10

`lightning-all` · `lightning-all-15m` · `lightning-all-5m` · `lightning-strikes` ·
`lightning-strikes-15m-icons` · `lightning-strikes-5m-icons`

### ×5

`air-quality-co` · `air-quality-health-index-categories` · `air-quality-index-cai-categories` ·
`air-quality-index-caqi-categories` · `air-quality-index-china-categories` ·
`air-quality-index-eaqi-categories` · `air-quality-index-india-categories` ·
`air-quality-index-uba-daqi-categories` · `air-quality-index-uk-daqi-categories` ·
`air-quality-no` · `air-quality-no2` · `air-quality-o3` · `air-quality-pm10` ·
`air-quality-pm2p5` · `air-quality-so2`

### ×1

The other 138 layers, including every base map, overlay, mask, radar, satellite, forecast, maritime,
tropical, and severe layer. Notably `lightning-flash`, `lightning-flash-5m-icons`, and
`lightning-strike-density` are ×1 — only the `lightning-strikes` / `lightning-all` families are ×10.
Likewise `air-quality-index` and `air-quality-index-categories` are ×1 while the individual pollutant
and national-scale index layers are ×5.

Per-layer multipliers are also listed inline in `layers.md`. Regenerate from the live catalog:

```bash
curl -s https://www.xweather.com/docs/api/maps/layers \
  | python3 -c 'import json,sys; [print(l["multiplier"], l["id"]) for l in sorted(json.load(sys.stdin)["layers"], key=lambda x:-x["multiplier"])]'
```

## Raster Maps vs. MapsGL billing

MapsGL — the client-side WebGL SDK — measures usage in **sessions** rather than map units, and the
two models reward opposite patterns:

| | Raster Maps | MapsGL |
|---|---|---|
| Unit | Map unit (one 256×256 tile × one ×1 layer) | Session (5-minute wall-clock bucket) |
| More layers | **Multiplies** cost | **Free** |
| Pan / zoom | Each new tile costs again | **Free** within the session |
| Animation | Each frame is a fresh set of tiles | **Free** within the session |
| Floor | 1 map unit | 1 session = 150 accesses |

So:

- **A static image, or a brief non-interactive view** — Raster Maps. An 800×600 one-layer image is 12
  map units against MapsGL's 150-access floor.
- **An animated, multi-layer, heavily-panned map** — MapsGL is likely cheaper, since its cost stops
  growing once the session starts while Raster Maps keeps charging per tile.

Raise this whenever someone is costing out an interactive tile map with several layers; the crossover
comes quickly. Details in the `mapsgl` skill's `references/sessions.md`.

## Caching

Images are cached in the browser for a period tied to the layer's update interval — radar refreshes
every ~2–6 minutes, temperatures roughly hourly. Re-requesting inside that window doesn't generate
new units. Native apps should implement equivalent memory or file caching; it's the single biggest
lever on real-world consumption.

## Reducing map units

- **Combine layers into one request** rather than stacking separate tile layers in the mapping
  library. `flat,radar,admin` as one tile layer pulls one tile per position instead of three. It does
  not reduce the unit count itself (still summed per layer), but it cuts request volume and latency.
- **Smaller images.** Cost is quantised in 256-pixel steps, so 512×512 (4 tiles) and 500×500 (4
  tiles) cost the same, but 520×520 jumps to 9. Sizing to just under a tile boundary is free money.
- **Prefer the ×1 alternative** where it answers the question: `lightning-flash` or
  `lightning-strike-density` instead of `lightning-strikes`; `air-quality-index-categories` instead
  of a specific pollutant layer.
- **Don't plot a layer twice** unless the shadow/glow effect is worth double billing.
- Usage is visible in the account dashboard; the Usage tab breaks it down over time and by
  application. Stats lag slightly behind real time.

The docs don't say whether `@2x` retina requests are billed at the base tile grid or at the doubled
pixel dimensions. Don't assert either way — if it matters to a decision, check the dashboard after a
test request.
