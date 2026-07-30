# Color Scales Reference

A color scale maps a continuous data range (e.g. -40°C to 40°C) to a gradient or a set of discrete
color bands, so a single `sample` layer (temperature, wind speed, pressure, etc.) can render every
pixel's underlying value as a color without per-feature styling. It's the mechanism behind both a
layer's on-map colors and its matching gradient legend (`references/legends.md`'s `bar` type).

Verified against `packages/webgl-maps/src/style/colors.ts` and `style/specs/sample.ts`.
Used for the `sample.colorscale` (and `heatmap.color`) paint property.

## ColorScaleOptions

```typescript
interface ColorScaleOptions {
  range?: { min: number; max: number };   // default 0..1
  stops?: Array<number | string>;         // flat [value, color, value, color, ...] pairs
  positions?: number[];                   // optional non-linear stop positions (0..1), instead of linear
  interval?: number;                      // auto-generate stepped breaks at this interval; 0 = smooth gradient
  breaks?: number[] | ((min, max, interval) => number[]);  // explicit stepped break values
  normalized?: boolean;                   // stops given as 0..1 instead of real data units
  interpolate?: boolean;                  // true = gradient (default), false = hard stepped colors
  masks?: Array<{                         // per-channel masked sub-scales (advanced/multiband data)
    channel: 'r'|'g'|'b'|'a';
    value: number;
    drawRange?: { min?: number; max?: number };
    colorscale: Partial<ColorScaleOptions>;
  }>;
}
```

`stops` values **must be in the same units as the underlying data** (e.g. °C, not °F, since MapsGL
stores weather data internally in metric — convert with your own `FtoC()`-style helper before
building stops if you're working in imperial units).

## Custom scale by explicit stops

```javascript
controller.addWeatherLayer('temperatures', {
  paint: {
    sample: {
      colorscale: {
        stops: [
          -60, '#FFFFFF',
          -40, '#58005b',
          -20, '#121475',
            0, '#81e8ff',
           20, '#ecf93d',
           40, '#6b0001',
           60, '#7b7b7b'
        ],
        interval: 5
      }
    }
  }
});
```

## Hard (non-gradient) color breaks

```javascript
controller.addWeatherLayer('temperatures', {
  paint: {
    sample: {
      drawRange: { max: 36 },      // clip anything above 36°C
      colorscale: {
        stops: [-80, '#992BFF', 28, '#0046FF'],
        interpolate: false          // hard boundaries instead of a gradient
      }
    }
  }
});
```

## Built-in named scales

```javascript
const names = mapsgl.styles.getColorScaleNames();     // list all built-in scale names
const colors = mapsgl.styles.getColors('Inferno');    // raw color array for a named scale
const colorscale = mapsgl.styles.getColorScale('Inferno');   // ready-to-use ColorScaleOptions (normalized)
layer.setPaintProperty('sample.colorscale', colorscale);

// prepend a transparent stop for partial-coverage data
const withTransparency = mapsgl.styles.getColorScale('Inferno', [], true);
```

Available names:
- **Perceptually uniform:** `Viridis`, `Inferno`, `Plasma`, `Magma`, `Cividis`, `Mako`, `Rocket`, `Turbo`
- **Sequential (ColorBrewer):** `OrRd`, `PuBu`, `BuPu`, `Oranges`, `BuGn`, `YlOrBr`, `YlGn`, `Reds`,
  `RdPu`, `Greens`, `YlGnBu`, `Purples`, `GnBu`, `Greys`, `YlOrRd`, `PuRd`, `Blues`, `PuBuGn`
- **Diverging:** `Spectral`, `RdYlGn`, `RdBu`, `PiYG`, `PRGn`, `RdYlBu`, `BrBG`, `RdGy`, `PuOr`
- **Qualitative:** `Set2`, `Accent`, `Set1`, `Set3`, `Dark2`, `Paired`, `Pastel2`, `Pastel1`
- **Cyclic:** `Rainbow`, `Sinebow`
- **Flat:** `White`, `Black`

`getColorScale(name, prefixColors?, startTransparent?)` builds evenly-spaced normalized stops
across the named palette; pass `prefixColors` to prepend extra colors, or `startTransparent: true`
to insert a fully-transparent leading stop (useful for scales like precipitation where 0 should be invisible).
