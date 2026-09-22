# Layer ordering — slots and stack rank

Added in **MapsGL 1.10.0**. Layers stack in **slots** (named bands in a fixed top-to-bottom order)
and, inside a slot, by **stack rank** (higher paints above). Together they replace the old approach of
hunting through the host style for a Mapbox/MapLibre layer id just to keep weather fills under admin
boundaries or radar above temperatures.

Source: <https://www.xweather.com/docs/mapsgl/getting-started/layer-ordering>

## Slots are opt-in

**Not enabled by default.** Stacking behaviour is unchanged until the controller is constructed with
`slots`:

```javascript
const controller = new aerisweather.mapsgl.MapboxMapController(map, {
    account,
    slots: true
});
```

`slots: true` takes the built-in bands and ranks. A config object overrides them (see
[Constructor config](#constructor-config)). Without `slots`, none of the slot APIs below have a model
to act on — so if a user asks for layer ordering, turn slots on at construction time, not later.

Once enabled, layers are added exactly as before: MapsGL picks each layer's slot from its render type
and its rank from its weather code, then projects that order onto the host map.

## Built-in slots (top → bottom)

| Slot | Typical contents | Default host placement |
|---|---|---|
| `overlay` | Day/night terminator, debug, other chrome | Topmost MapsGL band |
| `text` | Text / city-label layers (`LayerType.text`, or an id/code ending in `-text` / `.text`) | Above `inlay` |
| `inlay` | Particles, lines, circles, symbols, contours, grids, other vector marks | Above `underlay` |
| `underlay` | Raster, sample, heatmap, data, polygon fills | Classic Mapbox/MapLibre: below admin boundaries. Mapbox Standard: native `middle` band (below labels) |

**Slot order always wins across bands** — every `inlay` layer paints above every `underlay` layer
regardless of rank. Unknown layer types fall into `inlay`. Custom slots are inserted just below
`overlay` unless the full order is replaced.

**There is no `particles` slot.** Particle layers live in `inlay` with a particle stack rank (400), so
they stay under contours, lines, circles, and symbols when everything shares a band.

## Stack rank (within a slot)

Higher rank paints above. The built-in ranks form one global top → bottom chain, so layers still paint
sanely even when several types land in the same slot:

| Rank | Applies to |
|---|---|
| 1000 | Day/night overlay chrome |
| 900 | Text / label layers |
| 800 | Symbol |
| 700 | Circle (also grid) |
| 600 | Line (also query / voronoi / coverage masks) |
| 500 | Contour |
| 400 | Particle fields |
| 350 | Admin / boundary overlays (`BuiltinStackRank.boundaries`) |
| 300 | Radar |
| 200 | Satellite |
| 100 | Fill |
| 50 | Precip / snow / sleet / ice sample codes (`precip-*`, `snow-*`, `sleet-*`, `ice-*`) |
| 0 | Default — generic sample, data, debug, other unmarked types |

Typical resulting orders, bottom → top:

- `underlay`: temperatures → precip → fills → satellite → radar
- `inlay`: particles → contour → line → circle → symbol
- `overlay`: debug (0) → day/night (1000)

The day/night overlay is re-pinned to the top of the MapsGL list whenever other layers are added or
moved.

Rank resolves in this order: explicit `stackRank` on the layer → a custom `resolveStackRank` resolver
→ an exact weather-code match (`radar`, `satellite`, or configured overrides) → text key/type →
a radar/satellite/precip heuristic on the layer id → a layer-type default → `0`.

## The defaults are usually enough

These three calls already produce a sensible stack — temperatures and radar in `underlay` with radar
on top, wind particles in `inlay` above both, admin lines still visible on Mapbox/MapLibre:

```javascript
controller.on('load', () => {
    controller.addWeatherLayer('temperatures');
    controller.addWeatherLayer('radar');
    controller.addWeatherLayer('wind-particles');
});
```

No search for an `admin-*` layer id is needed. On classic Mapbox GL / MapLibre GL styles `underlay` is
pinned below the bottom-most administrative boundary layer in the loaded style; on Mapbox Standard
styles `underlay` maps to the native `middle` band and the other slots to `top`.

**Reach for an override only when the default order is actually wrong** for the map being built.

## Overriding slot and rank when adding

`slot` and `stackRank` are weather layer overrides (and valid on a custom layer specification passed
to `addLayer`):

```javascript
// Keep radar in underlay, but paint it below satellite (satellite defaults to 200)
controller.addWeatherLayer('radar', {
    stackRank: 150
});

// Lift alerts out of inlay into overlay
controller.addWeatherLayer('alerts', {
    slot: 'overlay'
});
```

## Moving layers after they are added

```javascript
const radar = controller.addWeatherLayer('radar');

controller.getSlot(radar.id);       // 'underlay'
controller.getStackRank(radar.id);  // 300

controller.moveLayerToSlot(radar.id, 'inlay');
controller.setStackRank(radar.id, 20);
```

`moveLayerToSlot` keeps the layer's current rank and re-inserts it among siblings in the target slot.

`setCodeStackRank('radar', 320)` changes the default rank for **future** inserts resolving from that
weather code — it does not move layers already on the map.

> **Weather code vs. layer id.** `moveLayerToSlot`, `setStackRank`, `getSlot`, and `getStackRank` all
> expect the real MapsGL layer id (e.g. `conditions.radar.fill`), not the weather code. Passing
> `'radar'` silently no-ops. Capture what `addWeatherLayer` returns, or call `getWeatherLayer(code)`.
> Composite codes return an **array** — iterate and move each one. Same trap as `setPaintProperty`;
> see `references/weather-layers.md`.

## Pinning a slot below a host style layer (classic styles)

On classic Mapbox GL / MapLibre GL styles each slot can be pinned below a host style layer id. That id
is the slot's **ceiling**: every MapsGL layer in the band inserts before it while still stacking among
themselves by rank.

```javascript
// Move the entire underlay band under waterway labels
controller.setSlotBeforeId('underlay', 'waterway-label');

// Restore the default (bottom-most admin boundary)
controller.setSlotBeforeId('underlay', null);

const ceiling = controller.getSlotHostBeforeId('underlay');
```

Changing a ceiling does **not** change slot membership or ranks — it only moves the band within the
host style stack.

Ceilings can also be seeded at construction:

```javascript
const controller = new aerisweather.mapsgl.MapboxMapController(map, {
    account,
    slots: {
        slots: {
            underlay: { beforeId: 'waterway-label' }
        }
    }
});
```

**Google Maps and Leaflet** honour MapsGL slot order and ranks among MapsGL layers, but expose no
classic style-layer stack, so `setSlotBeforeId` has no host ceiling to pin to.

## Mapbox Standard styles

Mapbox Standard styles (`mapbox://styles/mapbox/standard` and similar) have no classic `beforeId`
stack. MapsGL slots map into the native Standard bands `bottom` / `middle` / `top` instead. This is a
**host-style** concern on `MapboxMapController` only — MapLibre no-ops these methods; Google Maps and
Leaflet don't expose the bands at all.

Adapter defaults when unset:

| MapsGL slot | Default Standard band |
|---|---|
| `underlay` | `middle` (below labels) |
| `inlay`, `text`, `overlay`, custom slots | `top` (above labels) |

```javascript
if (controller.usesMapboxStandardSlots()) {
    // Lift underlay into the top Standard band (above labels)
    controller.setSlotMapboxSlot('underlay', 'top');

    controller.getSlotMapboxSlot('underlay');   // 'top'
    controller.listMapboxStandardSlots();       // ['bottom', 'middle', 'top']
}

// Restore adapter defaults (underlay → middle)
controller.setSlotMapboxSlot('underlay', null);
```

Seeded at construction with `slots: { slots: { underlay: { mapboxSlot: 'bottom' } } }`.

`setSlotMapboxSlot` preserves any classic `beforeId`, and `setSlotBeforeId` preserves any
`mapboxSlot` — the adapter uses whichever mapping matches the current style. On a Standard style,
`getSlotHostBeforeId('underlay')` does **not** fall back to an admin-boundary id; use
`getSlotMapboxSlot`.

## Slot ceiling vs. per-layer `beforeId`

| Mechanism | Scope | Slot membership |
|---|---|---|
| `setSlotBeforeId(slotId, hostLayerId)` | Entire slot band (classic Mapbox/MapLibre) | Layers stay slotted; the band moves together |
| `setSlotMapboxSlot(slotId, 'bottom'\|'middle'\|'top')` | Entire slot band (Mapbox Standard) | Layers stay slotted; the band moves |
| `addWeatherLayer` / `addLayer` / `moveLayer` with a **MapsGL** `beforeId` | That layer, relative to a sibling | Joins or stays in the target layer's slot |
| `addWeatherLayer` / `addLayer` / `moveLayer` with a **host style** `beforeId` | That one layer | Layer is **unassigned** from slots (escape hatch) |

```javascript
const temps = controller.addWeatherLayer('temperatures');

// Relative to another MapsGL layer — stays in the slot model
controller.addWeatherLayer('radar', null, temps.id);

// Absolute pin under a Mapbox style layer — leaves the slot model
controller.moveLayer(temps.id, 'admin-0-boundary');
```

Use slot ceilings for "put all underlay content under admin lines / labels". Use a per-layer host
`beforeId` only when a single layer must sit somewhere the slot model cannot express.

## Unslotted layers

Unslotted layers aren't bucketed into one "outside slots" group — they keep a true position in the
MapsGL stack and can sit above, between, or below the bands.

A layer becomes unslotted when pinned with a **host** style `beforeId`, or when `moveLayer` targets a
neighbour that is itself unslotted (or the mover is already unslotted). Slot membership changes only
in these cases:

| `moveLayer` target | Slot effect |
|---|---|
| Another **MapsGL** layer, **both** slotted | Mover joins the target's slot and reorders among siblings |
| Another **MapsGL** layer, **either** unslotted | Mover is unassigned; stack order changes absolutely |
| A **host** style layer id | Mover is unassigned; absolute pin on the host |
| Omitted — `moveLayer(id)` | Keeps the current slot, or assigns `overlay` if unslotted |

```javascript
controller.moveLayer(temps.id, 'admin-0-boundary');   // temps leaves the slot model
controller.moveLayer(radar.id, temps.id);             // radar follows it out of slots
controller.moveLayerToSlot(radar.id, 'underlay');     // rejoin; rank is preserved
```

## Custom slots

New slots are inserted below `overlay` by default:

```javascript
controller.defineSlot('below-poi', { beforeId: 'poi-label' });
controller.moveLayerToSlot(layer.id, 'below-poi');

// Or replace the full bottom → top order
controller.setSlotOrder([
    'underlay',
    'inlay',
    'below-poi',
    'text',
    'overlay'
]);
```

`setSlotOrder` defines unknown ids as empty slots; membership and ranks are unchanged, layers are just
reprojected onto the new band order.

## Constructor config

```javascript
const controller = new aerisweather.mapsgl.MapboxMapController(map, {
    account,
    slots: {
        typeMapping: { fill: 'inlay' },      // layer type → slot; unmapped types fall back to inlay
        stackRanks: { radar: 320 },          // default within-slot ranks by weather code / stack key
        slots: {                             // per-slot host placement
            underlay: { beforeId: 'waterway-label', mapboxSlot: 'middle' }
        }
    }
});
```

`SlotRegistryOptions` fields:

| Field | Type | Meaning |
|---|---|---|
| `slots` | `Record<string, { beforeId?: string; mapboxSlot?: 'bottom'\|'middle'\|'top' }>` | Per-slot overrides, keyed by slot id (built-in or custom) |
| `typeMapping` | `Record<string, string>` | Layer type → slot id overrides |
| `stackRanks` | `Record<string, number>` | Default ranks by weather code / stack key, merged over built-ins |
| `resolveStackRank` | `(ctx: { layerId: string; stackKey?: string; type?: string }) => number \| undefined` | Custom resolver; return `undefined` to fall through to `stackRanks` and the built-in rules |

## Inspecting order

```javascript
controller.listSlots();                     // SlotDefinition[], bottom → top, with beforeId / mapboxSlot
controller.getSlot(layer.id);               // slot id, or undefined if unslotted
controller.getStackRank(layer.id);          // within-slot rank
controller.getSlotHostBeforeId('underlay'); // host ceiling (classic styles)
```

## Method summary

| Method | Purpose |
|---|---|
| `defineSlot(id, { beforeId?, mapboxSlot? })` | Define or update a slot; returns the `SlotDefinition` |
| `setSlotOrder(ids[])` | Replace the bottom → top slot order |
| `listSlots()` | All slot definitions, bottom → top |
| `setSlotBeforeId(slotId, beforeId \| null)` | Pin a band below a host style layer (classic styles); `null` restores the default |
| `getSlotHostBeforeId(slotId)` | The host layer id a band pins below |
| `moveLayerToSlot(layerId, slotId)` | Move a layer between slots, preserving rank |
| `getSlot(layerId)` | Slot a layer belongs to |
| `setStackRank(layerId, rank)` | Set a layer's within-slot rank and re-insert it |
| `getStackRank(layerId)` | A layer's within-slot rank |
| `setCodeStackRank(code, rank)` | Default rank for **future** inserts from that weather code |
| `usesMapboxStandardSlots()` | Whether the current Mapbox style exposes Standard bands (`MapboxMapController`) |
| `setSlotMapboxSlot(slotId, band \| null)` | Pin a band into a Mapbox Standard band (`MapboxMapController`) |
| `getSlotMapboxSlot(slotId)` | The Standard band a slot maps into (`MapboxMapController`) |
| `listMapboxStandardSlots()` | Standard bands on the current style, bottom → top; empty when not a Standard style |

Every `layerId` above is a real MapsGL layer id, never a weather layer code.
