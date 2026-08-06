# Weather layers - MapsGL Android (1.6.x)

Verified against SDK `LayerCode`, `WeatherService`, `MapController` weather APIs (1.6.x).
Docs are secondary:
https://www.xweather.com/docs/mapsgl-android-sdk/getting-started/weather-data\r\n\r\n## Critical: LayerCode != style layer id

```kotlin
val temperaturesLayer = controller.getWeatherLayer(LayerCode.TEMPERATURES)
val tempLayerId = temperaturesLayer?.id
// Stack another layer relative to temperatures:
controller.addWeatherLayer(
    WeatherService.WindParticles(controller.service),
    id = null,
    beforeId = tempLayerId,
)
```

Do **not** use `getLayer("temperatures")` with the weather code string.

## Remove / visibility

```kotlin
controller.setWeatherLayerVisibility(LayerCode.RADAR, visible = false)
controller.removeWeatherLayer(LayerCode.RADAR)   // LayerCode - not a style layer id
controller.hasWeatherLayer(LayerCode.RADAR)
```

(Some older docs snippets pass a layer id into `removeWeatherLayer` - that is **not**
the 1.6.x API.)

## Common codes / factories

| LayerCode | WeatherService factory | Notes |
|---|---|---|
| `TEMPERATURES` | `Temperatures` | Sample fill |
| `RADAR` | `Radar` | Raster, animatable |
| `SATELLITE` | `Satellite` | Raster |
| `PRECIPITATION` | ... | `precip` |
| `WIND_SPEEDS` / `WIND_PARTICLES` / `WIND_BARBS` | `WindSpeeds` / `WindParticles` / `WindBarbs` | Encoded / particle / grid |
| `WIND_DIR` / arrows | `WindDirectionArrows` | Grid |
| `ALERTS` / `ALERTS_OUTLINE` | `Alerts` / `AlertsOutline` | Vector fill/line |
| `EARTHQUAKES` | `Earthquakes` | GeoJSON circles |
| `BOUNDARIES` / `ROADS` / `PLACES` | composites | Multi-layer |

Composites expand into multiple sublayers when added.

## Paint overrides

See `weather-styling.md` for raster / sample / particle / grid paint overrides.

## Custom vs weather

- Weather: `addWeatherLayer(LayerCode)` or `addWeatherLayer(WeatherConfiguration)`
- Custom: `addSource` + `addLayer` - see `sources.md` and `custom-layers.md`
