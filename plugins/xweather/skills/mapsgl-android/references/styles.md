# Styles, descriptors & paint - MapsGL Android (1.6.x)

Verified against SDK descriptors and paint types (1.6.x).
Docs overview is secondary:
https://www.xweather.com/docs/mapsgl-android-sdk/styling\r\n\r\n## Layer render types

| Type | Role |
|---|---|
| raster | Static imagery |
| fill | Polygon fills |
| line | Lines |
| circle | Point circles |
| symbol | Icons / glyphs |
| sample | Encoded -> color scale |
| grid | Encoded sample -> symbol grid |
| contour | Encoded -> isolines |
| particle | Flow fields |
| heatmap | Point density |

(Intro pages that still say grid/contour "coming soon" are stale - styling and
advanced-layer docs + 1.6.x SDK support them.)

## Descriptors (`layers.spec`)

`Raster`, `Sample`, `Contour`, `Particle`, `Fill`, `Line`, `Circle`, `Symbol`,
`Grid`, `Heatmap` - see `custom-layers.md`.

On **1.6.x**, many vector weather layers draw via **Mapbox style layers**;
encoded sample/contour/particle/grid use **GLES** custom layers.

## Paint

Low-level: `SamplePaint`, `RasterPaint`, `FillPaint`, `StrokePaint`, `CirclePaint`,
`IconPaint`, `TextPaint`, `HeatmapPaint`, `ParticlePaint`, `ContourPaint`, `GridPaint`.

Wrappers: `SampleLayerPaint`, `FillLayerPaint`, `LineLayerPaint`, `CircleLayerPaint`,
`SymbolLayerPaint`, `GridLayerPaint`, `ParticleLayerPaint`, `RasterLayerPaint`, ...

### IconPaint (1.6.x)

`allowOverlap`, `image`, `size`, optional `iconSize`, optional `atlas`, `anchor`,
`offset`, `padding`, `rotation`, `rotationUsesDataDirection`.  
**No** public custom fragment `shader` on 1.6.x.

## Layer masks

Land/ocean/country-style masks via descriptor mask fields (stencil budget ~8).
See SDK README / docs.

## Weather vs custom

- Built-in weather paint overrides: **`weather-styling.md`**
- Data-driven expressions: **`data-driven.md`**
- Custom sources/layers: **`sources.md`**, **`custom-layers.md`**
