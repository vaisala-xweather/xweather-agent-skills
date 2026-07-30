# Layer Styling Reference (paint properties)

Every `WebGLLayer` renders its underlying data using one or more **render styles** (`raster`,
`fill`, `sample`, `particle`, etc.) — the render style is chosen based on the shape of the data
(static imagery, vector polygons/lines/points, gridded/encoded rasters, flow fields) and determines
which paint properties are available. `paint` is where you configure how that render style actually
looks: colors, sizes, opacity, colorscales.

Verified against `@xweather/mapsgl` SDK source (`packages/webgl-maps/src/style/specs/*.ts`).

A layer's `paint` object is namespaced by render style. Every leaf value is a `StyleValue<T>`,
meaning it can be:
- a constant (`'#ff0000'`, `4`, etc.)
- an **expression array** (see `references/expressions.md`) — `['get', 'FIELD']`, `['match', ...]`, `['interpolate', ...]`, etc.
- a data evaluator function: `(data) => value` (legacy)
- a `{ property: 'FIELD_NAME' }` data-driven lookup (legacy shorthand for `['get', 'FIELD_NAME']`)

**Always use expressions for data-driven styling in new code.** Evaluator functions and the
`{ property }` shorthand still work for backwards compatibility, but expressions are what MapsGL's
own docs and examples use, are declarative/serializable (safe to store as JSON config), and are
the only form that reliably supports future engine-level style optimizations. The rest of this
reference and skill only shows the expression form.

```typescript
interface PaintStyleSpec {
  opacity: StyleValue<number>;      // default 1, applies to the whole layer
  animated: StyleValue<boolean>;    // default false
  raster, fill, stroke, circle, grid, sample, particle, heatmap, contour, symbol, icon: Partial<...>;
  text: Partial<TextStyleSpec> | Array<Partial<TextStyleSpec>>;  // array = multiple labels/feature
}
```

`LayerType` values: `raster`, `fill`, `line` (aliases to stroke rendering), `circle`, `sample`,
`grid`, `heatmap`, `contour`, `particle` (`particles` is a deprecated alias), `symbol`
(`text` as a layer type is deprecated — use `symbol` + `paint.text`).

## raster
```typescript
{ meld: boolean }   // default false; smooths interpolation between time steps during animation
```

## fill
```typescript
{
  color: StyleValue<string | Color>;                 // default '#000000'
  pattern: StyleValue<string | { id: string; url: string }>;
  opacity: StyleValue<number>;
  sort: string | { property: string; direction?: 'asc'|'desc' };
}
```

## stroke (used for `type: 'line'` layers)
```typescript
{
  color: StyleValue<string | Color>;        // default '#000000'
  opacity: StyleValue<number>;
  thickness: StyleValue<number>;            // points, default 2
  lineJoin: 'bevel' | 'round' | 'miter';    // default 'round'
  lineCap: 'butt' | 'round' | 'square';     // default 'round'
}
```

## circle
```typescript
{ radius: StyleValue<number> }   // points, default 6
```

## sample
The workhorse style for gridded/encoded weather data (temperature, wind speed, pressure, etc.).
```typescript
{
  expression: 'number' | 'vector' | 'sum' | 'diff' | 'angle' | 'custom';  // default 'number'
  expressionOperation: { dataRange, value(data), chunk };  // for 'custom' expressions
  channel: 'r'|'g'|'b'|'a'|'rg'|'gb'|'rb'|'ra'|'ga'|'ba'|'rgb'|'gba'|'rgba' | ColorBand[];
  quality: 'minimal' | 'low' | 'normal' | 'medium' | 'high' | 'exact';  // DataQuality enum
  interpolation: 'none' | 'bilinear' | 'bicubic' | 'biquadratic';       // default 'bilinear'
  smoothing: number;                 // 0 (none) .. 1 (full), default 0
  colorscale: ColorScaleOptions;     // see references/color-scales.md
  offset: number;                    // default 0; shifts 'diff' results to a 0.5 midpoint
  meld: boolean;                     // default true
  dataRange: { min: number; max: number };
  drawRange: { min?: number; max?: number };  // clip rendering outside this value range
}
```

## grid
Samples underlying raster/encoded data onto a regular point grid, rendered via `symbol`/`icon`.
```typescript
{ spacing: StyleValue<number> }   // points, default 30
```

## contour
Isolines generated from encoded raster data.
```typescript
{
  interval: StyleValue<number>;       // default 1
  majorInterval: StyleValue<number>;  // default 0 (disabled); draws heavier lines every Nth interval
  width: StyleValue<number>;
  majorWidth: StyleValue<number>;
  scale: StyleValue<number>;
  offset: StyleValue<number>;
}
```

## particle
Flow-field animation for wind/currents.
```typescript
{
  type: 'circle' | 'bar' | 'arrow';
  count: StyleValue<number>;               // default 65536
  density: 'count'|'minimal'|'low'|'normal'|'high'|'extreme';  // ParticleDensity enum
  size: StyleValue<number | { width: number; height: number }>;  // default 2
  speedFactor: StyleValue<number>;         // default 1 (was `speed`, now deprecated)
  trails: StyleValue<boolean>;             // default true
  trailsFadeFactor: StyleValue<number>;    // 0-1, default 0.98 (was `trailsFade`, now deprecated)
  dropRate: StyleValue<number>;            // default 0.01
  dropRateBump: StyleValue<number>;        // default 0.01
}
```

## heatmap
```typescript
{
  color: StyleValue<Array<number | string>>;  // normalized 0..1 color scale stops
  radius: StyleValue<number>;                 // points, default 20
  blur: StyleValue<number>;                   // default 1
  intensity: StyleValue<number>;              // default 1
  weight: StyleValue<number>;                 // default 1
}
```

## icon
Underlies `symbol`-type point rendering (images, glyphs, or custom GLSL).
```typescript
{
  image: StyleValue<string | { id: string; url: string; sdf?: boolean }>;
  atlas: { ids: string[]; interval?: number };
  size: StyleValue<{ width: number; height: number }>;   // default 20x20
  anchor: StyleValue<SymbolAnchor>;   // 'top-left'|'top'|'top-right'|'left'|'center'|'right'|'bottom-left'|'bottom'|'bottom-right'
  offset: StyleValue<{ x: number; y: number }>;
  padding: StyleValue<number | [number, number]>;   // default 6
  rotation: StyleValue<number>;       // radians, default 0
  animated: boolean;                  // default false
  shader: StyleValue<string>;         // GLSL fragment shader override
  shaderOnBeforeCompile: (shader: { vertex: string; fragment: string }) => void;
  uniforms: Record<string, any>;
  factor: StyleValue<number>;         // default 1
}
```

## symbol
Placement/collision behavior for icon + text layers (rendered together as one symbol layer).
```typescript
{
  key: StyleValue<string>;
  rank: string | { property: string; direction?: 'asc'|'desc' };
  fadeOpacity: boolean;         // default true
  pitchWithMap: boolean;        // default true
  rotateWithMap: boolean;       // default true
  scaleWithMap: boolean;
  sizeAttenuation: boolean;     // default true
  allowOverlap: boolean;        // default true
  overlapMode: 'layer' | 'map'; // default 'layer'
  sortKey: StyleValue<Array<{ property: string; direction?: 'asc'|'desc' }>>;
}
```

## text
```typescript
{
  value: StyleValue<string>;    // e.g. ['get', 'FIELD']
  size: StyleValue<number>;     // default 12
  font: StyleValue<string>;     // default 'Inter'
  weight: StyleValue<'normal'|'bold'>;
  color: StyleValue<string | Color>;         // default '#000000'
  outlineColor: StyleValue<string | Color>;
  opacity: StyleValue<number>;
  align: StyleValue<'left'|'center'|'right'>;
  transform: StyleValue<'none'|'uppercase'|'lowercase'|'capitalize'>;
  anchor: StyleValue<SymbolAnchor>;
  offset: StyleValue<{ x: number; y: number }>;
  padding: StyleValue<number | [number, number]>;
  rotation: StyleValue<number>;   // degrees
  letterSpacing: StyleValue<number>;
  lineHeight: StyleValue<number>;
  maxWidth: StyleValue<number>;   // points, default 140
}
```
Pass an array of text style objects to `paint.text` to render multiple data-driven labels on one feature.

## Updating styles after creation

There's no bulk `setStyle()` — update one property at a time, directly on the layer instance:

```javascript
// custom layer you created yourself — the id you chose is a real layer id
const layer = controller.getLayer('alerts-fill');
layer.setPaintProperty('fill.color', newColor);

// built-in weather layer — use getWeatherLayer(code), NOT controller.getLayer(code) /
// controller.setPaintProperty(code, ...). The weather layer code is not a real layer id —
// see the "code vs. id" section in references/weather-layers.md.
const tempLayer = controller.getWeatherLayer('temperatures');
tempLayer.setPaintProperty('sample.colorscale', newColorScale);
```

`WebGLLayer` instance methods: `show()`, `hide()`, `setPaintProperty(property, value)`,
`refresh(clear?: boolean)`, `queryFeatures(coord, zoom)`, `dispose()`.

## Data-driven styling patterns

Use expressions (see `references/expressions.md` for the full operator list). `get` supports
dotted paths for nested properties.

```javascript
// direct property lookup
paint: { fill: { color: ['get', 'alert.info.color'] } }

// categorical lookup with a fallback, via `match`
paint: {
  fill: {
    color: [
      'match', ['get', 'report.type'],
      'tornado', '#d62728',
      'hail', '#1f77b4',
      'wind', '#2ca02c',
      '#000000'   // fallback for unmatched values
    ]
  }
}

// continuous value driving both color and size, via `interpolate`
paint: {
  fill: { color: ['interpolate', ['linear'], ['get', 'mag'], 0, '#2ca02c', 4, '#ff7f0e', 6, '#d62728'] },
  circle: { radius: ['interpolate', ['linear'], ['get', 'mag'], 0, 3, 6, 12] }
}
```
Some paint properties are evaluated once at data-load time and won't update on later property
changes — if a live style override isn't taking effect, re-add the layer instead of mutating it.

## Filters

`filter` on a layer config is a `FilterExpression` (see `references/expressions.md`), evaluated
per-feature to decide whether it renders:
```javascript
controller.addLayer('big-quakes', {
  type: 'circle',
  source: 'earthquakes',
  filter: ['>=', ['get', 'mag'], 4],
  paint: { circle: { radius: 6 }, fill: { color: '#d62728' } }
});
```

## Masks

Restrict a layer to render only where other layers (or built-in land/water) are present:
```typescript
interface LayerMaskSpecification {
  layerIds?: string[];         // custom layer ids to mask against
  type?: 'land' | 'water';     // built-in geographic masks
  invert?: boolean;            // default false — show outside the mask instead
  mode?: 'all' | 'any';        // default 'all'
}
```
```javascript
controller.addWeatherLayer('temperatures', { mask: { type: 'land' } });
controller.addWeatherLayer('temperatures', { mask: { layerIds: ['admin-mask'] } });
```
