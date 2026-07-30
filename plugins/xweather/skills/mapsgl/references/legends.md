# Legends Reference

A legend is the on-map key that explains what a layer's colors/symbols mean — a color gradient
with value labels for continuous data (temperature, wind speed) or a swatch-and-label list for
categorical data (alert types, risk levels). `controller.addLegendControl(target)` renders whatever
legend config is attached to each currently-active layer into one shared UI element; it's populated
automatically and updates as layers are added/removed/restyled.

Verified against `@xweather/mapsgl` SDK source (`packages/webgl-maps/src/control/legend/*.ts`).

Every built-in weather layer already ships a correctly-configured default legend. **You only need
to override `legend` when you've also overridden `paint` with colors the auto-detection can't
infer** (see `references/color-scales.md` and `references/expressions.md`).

## Legend shape

```typescript
interface LegendOptions {
  type: 'bar' | 'point';
  title?: string;
  width?: number;
  insets?: number | number[];
  enabled?: boolean;
  points?: Partial<PointLegendOptions>;               // for categorical/discrete data
  bar?: Partial<BarLegendOptions> | Partial<BarLegendOptions>[];  // for continuous/gradient data
  text?: Partial<{ family, color, stroke: { color, width }, size, style, weight, offset, shadow }>;
  onBeforeUpdate?: (options: Partial<LegendOptions>) => Partial<LegendOptions>;
}
```

Pick **`points`** for discrete categories/values (alert types, risk levels, storm reports) and
**`bar`** for a continuous gradient scale (temperature, wind speed, precipitation amount).

## `points` (categorical legend)

```typescript
interface PointLegendOptions {
  values: Array<{ key?: string; color: string; label: string }>
        | ((data?: Record<string, any>) => Promise<Array<{ color: string; label: string }>>);
  radius: number;
  margin: number | [number, number];
  requiresMapBounds: boolean;
  layerId: string;
}
```

```javascript
controller.addWeatherLayer('convective', {
  paint: { /* ... custom expression-based colors, see references/expressions.md ... */ },
  legend: {
    points: {
      values: [
        { color: '#ffea16', label: 'General' },
        { color: '#ffc41d', label: 'Marginal' },
        { color: '#ff891d', label: 'Slight' },
        { color: '#fa2311', label: 'Enhanced' },
        { color: '#fa23ec', label: 'Moderate' },
        { color: '#fac9eb', label: 'High' }
      ]
    }
  }
});
```

## `bar` (gradient/continuous legend)

```typescript
interface BarLegendOptions {
  height: number;
  rounded: boolean;
  equalWidth: boolean;   // default false — cell widths proportional to value spacing
  measurement: {
    type: string;          // e.g. 'temperature', 'speed', 'pressure' — must match a known Measurement type
    units: string;          // e.g. 'C', 'F', 'mph', 'km/h'
    converter?: (value: number, from: string, to: string) => number;
  };
  colorscale: Partial<ColorScaleOptions> & { resample?: 'linear' | /* other EasingCurve values */ string };
  labels: Partial<{
    values: Array<number | { value: number; label: string; position?: number; span?: number }>
          | ((units: string) => Array<number | { value: number; label: string }>);
    every: number | ((units: string) => number);      // label interval, in colorscale's units
    everyStep: number;                                  // label every N color-stop steps instead
    formatter: (value: number, index: number, state: { units: string }) => string;
    placement: 'top' | 'middle' | 'bottom';
    centered: boolean;
    marks: 'point' | 'line' | 'none';
    margin: number | [number, number];
    normalized: boolean;
    allowOverlap: boolean;
  }>;
}
```

`colorscale` here takes the same `ColorScaleOptions` shape used in `paint.sample.colorscale` (see
`references/color-scales.md`) — when you override a layer's colorscale, pass the **same stops** to
the legend's `bar.colorscale` so they stay in sync.

```javascript
const customTemperatureColorscale = {
  stops: [-40, '#1b1b3a', -20, '#2f4b7c', 0, '#00b4d8', 10, '#90e0ef', 20, '#ffd166', 30, '#f77f00', 40, '#d62828'],
  interval: 2,
  interpolate: true
};

controller.addWeatherLayer('temperatures', {
  paint: {
    sample: { colorscale: customTemperatureColorscale }
  },
  legend: {
    bar: {
      colorscale: customTemperatureColorscale,
      measurement: { type: 'temperature', units: 'C' },
      labels: { every: 10 }
    }
  }
});
```

This mirrors how MapsGL configures its own built-in temperature legend internally — matching
`colorscale` between `paint.sample` and `legend.bar` is the key detail; everything else has
sensible defaults.
