# MapsGL Apple SDK — paint properties, quality, color scales, filters, masks

A layer's paint object is namespaced by render type, and which namespaces exist is decided by the
layer descriptor. `layers.md` gives the descriptor for every built-in weather layer; the tables below
give the properties for each.

Two rules that apply everywhere:

1. **Data values are always metric.** Color-scale stops, draw ranges, and contour intervals are in
   °C, m/s, mm, hPa — regardless of what the app displays. Converting for display is a legend/format
   concern, not a paint concern.
2. **Styleable values are `StyleValue<T>`, an enum with two cases.** Write `.constant(x)` for a fixed
   value and `.expression(…)` for a data-driven one. There is no bare-value shorthand.

```swift
color: .constant(.red)
color: .expression(Expression.get("COLOR"))
```

## Where paint lives

For a built-in weather layer, mutate the configuration struct before adding it:

```swift
var config = WeatherService.Temperatures(service: controller.service)
config.layer.paint.opacity = 0.5            // paint hangs off `layer`
config.layer.quality = .low                 // quality is on the descriptor, not on paint
try controller.addWeatherLayer(config: config)
```

For a custom layer, pass paint to the descriptor's initializer:

```swift
let layer = FillLayerDescriptor(
    id: "alerts-fill",
    source: "alerts",
    paint: .init(
        fill: .init(color: .expression(Expression.get("COLOR"))),
        stroke: .init(color: .constant(.black))
    )
)
```

`addWeatherLayer(for:)` accepts no overrides. A customized weather layer must go through
`addWeatherLayer(config:)`.

## Paint by render type

Every layer paint type has `opacity: Opacity`, and **that is the only place opacity lives**. `Opacity`
is `ExpressibleByFloatLiteral`, so `paint.opacity = 0.5` works; `.full`, `.half`, `.none`, `.opaque`,
`.transparent` are provided.

`paint.sample.opacity` does **not** compile — `SamplePaint` has no `opacity` member, even though the
web documentation's override example shows it. Verified against 1.6.1. The render-type namespaces
(`sample`, `particle`, `grid`, `contour`, `raster`) carry data and geometry properties; opacity is
always one level up. `FillPaint` and `StrokePaint` *do* have their own `opacity`, because those are
per-geometry alphas layered on top of the layer opacity.

### `sample` — `SampleFillLayerPaint`

`opacity`, `sample: SamplePaint`. The workhorse for encoded weather grids (68 of the built-in layers).

| `SamplePaint` property | Type | Notes |
|---|---|---|
| `colorScale` | `ColorScaleSpecification` | See "Color scales" below |
| `drawRange` | `(any InclusiveBoundedRange<Double>)?` | Clip which values render — `...2.22`, `10...30` |
| `quality` | `DataQuality` | Per-paint override of the descriptor's `quality` |
| `interpolation` | `InterpolationMode` | `.none`, `.bilinear`, `.biquadratic`, `.bicubic` |
| `smoothing` | `Double` | Post-sample smoothing |
| `offset` | `Double` | Value offset applied before colorizing |
| `channel` | `SampleChannel` | Which color band(s) hold the data — `.r`/`.red`, `.g`, `.b`, `.a`; an `OptionSet` |
| `expression` | `SampleExpression` | How to decode packed channels — `.number`, `.vector`, `.angle`, `.difference`, `.sum`, `.custom` |
| `meld` | `Bool` | Blend across time steps |
| `multiband` | `Bool` | Data spans multiple bands |

`channel`, `expression`, `meld`, and `multiband` describe the *encoding* and are already correct for
built-in layers. Only touch them when building a `SampleLayerDescriptor` over your own encoded source.

### `raster` — `RasterLayerPaint`

`opacity`, `raster: RasterPaint`. `RasterPaint` has no configurable properties — for raster imagery
(satellite, radar imagery) opacity is the lever.

### `particles` — `ParticleLayerPaint`

`opacity`, `sample: SamplePaint`, `particle: ParticlePaint`.

| `ParticlePaint` property | Type | Notes |
|---|---|---|
| `density` | `ParticleDensity?` | `.minimal`, `.low`, `.normal`, `.high`, `.extreme`, `.count` |
| `count` | `Int?` | Explicit particle count; used when `density` is `.count` |
| `kind` | `ParticleKind` | `.circle` or `.bar` |
| `size` | `CGSize` | |
| `speed` | `Double` | Multiplier on the data's own velocity |
| `trails` | `Bool` | |
| `trailsFade` | `Double` | 0–1; lower fades faster |
| `dropRate` | `Double` | How often particles respawn |
| `dropRateBump` | `Double` | Extra respawn pressure in fast flow |

`sample` still applies — it's what colorizes the particles from the underlying speed grid.

Density is the main performance lever for particle layers on device. `.extreme` looks great on a
recent iPhone and will cost frames on older hardware.

### `grid` — `GridLayerPaint`

`opacity`, `sample: SamplePaint`, `grid: GridPaint`, `fill: FillPaint?`, `stroke: StrokePaint?`,
`icon: IconPaint`, `symbol: SymbolPlacementPaint`. Used for wind barbs and arrow grids.

`GridPaint` has one property: `spacing: Double` — screen-space distance between sampled symbols.
Raise it to declutter, lower it for density.

`icon.image` names a registered image; register it with `controller.addImage(id:image:)` first.

### `contour` — `ContourLayerPaint`

`opacity`, `sample: SamplePaint`, `contour: ContourPaint`.

| `ContourPaint` property | Type | Notes |
|---|---|---|
| `interval` | `StyleValue<Double>` | Isoline spacing, in the data's metric units |
| `majorInterval` | `StyleValue<Double>` | Spacing of emphasized lines |
| `width` / `majorWidth` | `StyleValue<Double>` | Line widths |
| `scale` | `StyleValue<Double>` | |
| `offset` | `StyleValue<Double>` | |

The web docs describe `contour` as "coming soon" for the Apple SDK; the type and three built-in
contour layers (`.temperaturesContour`, `.windSpeedsContour`, `.pressureMeanSeaLevelContour`) do exist.
Treat it as supported but less exercised than `sample`.

### `fill` — `FillLayerPaint`

`opacity`, `fill: FillPaint`, `stroke: StrokePaint?`.

| `FillPaint` property | Type |
|---|---|
| `color` | `StyleValue<UIColor>` |
| `opacity` | `StyleValue<Double>` |
| `pattern` | `StyleValue<String>?` — a registered image id |
| `sortKey` | `StyleValue<String>?` |

### `line` — `LineLayerPaint`

`opacity`, `stroke: StrokePaint`.

| `StrokePaint` property | Type |
|---|---|
| `color` | `StyleValue<UIColor>` |
| `opacity` | `StyleValue<Double>` |
| `thickness` | `StyleValue<Double>` |
| `lineJoin` | `StyleValue<StrokePaint.LineJoin>` |
| `lineCap` | `StyleValue<StrokePaint.LineCap>` |
| `miterLimit` | `StyleValue<Double>` |

Note the name: it's `thickness`, not `width`.

### `circle` — `CircleLayerPaint`

`opacity`, `fill: FillPaint`, `stroke: StrokePaint`, `circle: CirclePaint`.

`CirclePaint`: `radius: StyleValue<Double>`, `sortKey: StyleValue<Double>?`.

Radius is the natural place for a data-driven expression — see `expressions.md` for the
magnitude-scaled earthquake example.

### `symbol` — `SymbolLayerPaint`

`opacity`, `fill: FillPaint?`, `stroke: StrokePaint?`, `icon: IconPaint`, `text: [TextPaint]`.

`text` is an **array**, so a symbol can carry several independently styled labels.

| `IconPaint` property | Type |
|---|---|
| `image` | `StyleValue<String>?` — registered image id |
| `atlas` | `IconAtlasPaint?` — sprite sheet |
| `source` | `IconSourcePaint` |
| `type` | `String?` |
| `size` | `StyleValue<Double>?` |
| `fixedSize` | `CGSize?` |
| `anchor` | `StyleValue<Anchor>` |
| `offset` | `StyleValue<AnchorOffset>` |
| `padding` | `StyleValue<Double>` |
| `rotation` | `StyleValue<Double>` |
| `allowOverlap` | `StyleValue<Bool>` |
| `placement` | `SymbolPlacementPaint` |

| `TextPaint` property | Type |
|---|---|
| `value` | `StyleValue<String>` — the label content; usually an expression |
| `size` | `StyleValue<Double>?` |
| `font` | `StyleValue<[String]>?` |
| `weight` | `StyleValue<String>?` |
| `color` / `outlineColor` | `StyleValue<UIColor>` / `StyleValue<UIColor>?` |
| `opacity` | `StyleValue<Double>` |
| `align` | `StyleValue<TextJustification>` |
| `transform` | `StyleValue<TextTransform>` |
| `anchor` / `offset` | `StyleValue<Anchor>` / `StyleValue<AnchorOffset>` |
| `padding` / `rotation` | `StyleValue<Double>` |
| `letterSpacing` / `lineHeight` / `maxWidth` | `StyleValue<Double>?` |
| `allowOverlap` | `StyleValue<Bool>` |

`SymbolPlacementPaint` adds `rotateWithMap: Bool` and `pitchWithMap: Bool` alongside the shared
`allowOverlap`/`anchor`/`offset`/`padding`/`rotation`.

### `heatmap` — `HeatmapLayerPaint`

`opacity`, `heatmap: HeatmapPaint`.

`HeatmapPaint`: `color: StyleValue<UIColor>`, `intensity: StyleValue<Double>`,
`radius: StyleValue<Double>`, `weight: StyleValue<Double>`.

`weight` is where a per-feature expression usually goes — weighting strikes by amperage, quakes by
magnitude.

## Data quality

`quality: DataQuality` on the layer descriptor (and overridable on `SamplePaint`) sets the
level-of-detail the data renders at. **The Apple SDK has four cases:**

| Case | Effect |
|---|---|
| `.low` | Less detail, more smoothing. Good for slowly varying fields like surface pressure |
| `.medium` | |
| `.high` | More detail. Useful for radar and satellite |
| `.exact` | Data tiles 1:1 with the map's zoom. Can significantly affect performance |

The web docs also list `minimal` and `normal`; those are JS-only and **do not exist in Swift** — using
them is a compile error. There is no explicit "default" case: leave `quality` unset to take the
descriptor's default.

Lower quality means fewer tile requests, less memory, and smoother frames on constrained devices —
recommend it for performance. It does **not** reduce session billing (see `sessions.md`).

## Color scales

`paint.sample.colorScale` is a `ColorScaleSpecification`, an enum:

```swift
case colorScale(ColorScaleOptions)     // a gradient or stepped scale
case masks([ColorMaskOptions])         // channel masking
```

It also has a convenience initializer, so both of these compile:

```swift
config.layer.paint.sample.colorScale = ColorScaleSpecification(stops: stops)
config.layer.paint.sample.colorScale = .colorScale(options)
```

`ColorScaleOptions`:

| Property | Type | Notes |
|---|---|---|
| `stops` | `[ColorStop]` | `ColorStop(value, cgColor)` — value in metric units |
| `interval` | `Double` | Quantize into steps of this size. Omit/0 for a smooth gradient |
| `interpolate` | `Bool` | `false` gives hard bands between stops |
| `range` | `ClosedRange<Double>?` | Explicit data range; used by bar legends |
| `positions` | `[Double]?` | Normalized stop positions, as an alternative to values |
| `normalized` | `Bool` | Treat stop values as 0–1 rather than data units |
| `isGradient` | `Bool` | Derived |

`ColorStop(_ value: Double, _ color: CGColor)`, and `.fromString("#rrggbb")` builds the color:

```swift
var scale = ColorScaleOptions(stops: [
    ColorStop(-17.78, .fromString("#464ab5")),   //   0 °F
    ColorStop(0.00,   .fromString("#6bea99")),   //  32 °F
    ColorStop(15.56,  .fromString("#fdff87")),   //  60 °F
    ColorStop(37.78,  .fromString("#901436")),   // 100 °F
])
```

Three presentations from the same stops:

```swift
// smooth gradient — leave interval and interpolate alone
config.layer.paint.sample.colorScale = .colorScale(scale)

// stepped every 5 °F
scale.interval = 2.775
config.layer.paint.sample.colorScale = .colorScale(scale)

// hard categorical bands
scale.interpolate = false
config.layer.paint.sample.colorScale = .colorScale(scale)
```

Comment your stops with the imperial equivalent when the app is US-facing. `-17.78` reads as noise;
`-17.78  // 0 °F` reads as a decision, and it's how the official examples are written.

**`drawRange` clips rather than colors.** To show only freezing temperatures, don't add a transparent
stop — set the range:

```swift
config.layer.paint.sample.drawRange = ...2.22   // ≤ 36 °F only; no lower bound
```

**Custom paint means custom legend for categorical layers.** Bar/color-scale legends re-derive
themselves from the layer's color scale, but point legends can't be inferred and will keep showing the
defaults. See `legends.md`.

## Filters

Vector layer descriptors (`fill`, `line`, `circle`, `symbol`, `heatmap`) have
`filter: Expression?` — features the expression rejects are not rendered at all:

```swift
var layer = CircleLayerDescriptor(id: "big-quakes", source: "earthquakes", paint: paint)
layer.filter = Expression.greaterThan(Expression.get("report.mag"), 4.0)
```

Encoded descriptors (`sample`, `particles`, `grid`, `contour`, `raster`) have no `filter` — use
`paint.sample.drawRange` to restrict them by value instead.

## Masks

Every layer descriptor has `maskConfiguration: LayerMaskConfiguration`, which clips rendering to a
region. Presets cover the common cases:

```swift
config.layer.maskConfiguration = .land    // draw only over land
config.layer.maskConfiguration = .water   // draw only over water
config.layer.maskConfiguration = .none
```

Spell the type out where there's no context to infer from:

```swift
_ = [LayerMaskConfiguration.none, .land, .water]
```

To clip against your own layers instead, build the configuration from layer references:

```swift
config.layer.maskConfiguration = LayerMaskConfiguration(
    layers: [LayerMaskReference(layerId: "my-clip-layer")],
    invert: false,      // true renders everywhere EXCEPT the referenced geometry
    mode: .all          // .all = inside every reference; .any = inside at least one
)
```

`LayerMaskReference(layerId:)` names a layer already on the map, so add the clip layer first.
`Mode` has exactly two cases, `.all` and `.any`, and only matters with more than one reference.
`isEnabled` is **get-only** — a configuration is active because it has references, so clear
`maskConfiguration` back to `.none` to turn masking off rather than looking for a toggle.

Read an active mask layer back with `getMaskLayer(_:)`, keyed by `MaskLayerKind` (`.land` / `.water`),
and get the insertion point masks use with `beforeIdForMaskLayers()`. Neither is main-actor-isolated:

```swift
_ = controller.getMaskLayer(.land)
_ = controller.beforeIdForMaskLayers()
```

Sea-surface temperature masked to water, or a temperature field masked to land, is the usual reason to
reach for this.
