# API reference cheat sheet - MapsGL Android (1.6.x)

Packages under `com.xweather.mapsgl.*`.  
KDoc hub: https://www.xweather.com/docs/mapsgl-android-sdk/api-reference

## Controllers

| Type | Role |
|---|---|
| `map.MapController` | Weather, sources, layers, timeline, legends, inspector |
| `map.mapbox.MapboxMapController` | `(MapView, XweatherAccount)` |

## Account / service

`config.weather.account.XweatherAccount(id, secret)`  
`controller.service` -> `WeatherService` (companion product factories)

## Weather

| API | Notes |
|---|---|
| `addWeatherLayer(LayerCode, id?, beforeId?, configure?)` | Built-in by code |
| `addWeatherLayer(WeatherConfiguration, ...)` | From `WeatherService.*` |
| `removeWeatherLayer(LayerCode)` | Code only |
| `setWeatherLayerVisibility` / `hasWeatherLayer` / `getWeatherLayer` | |
| `getConfigForCode` | |

## Sources & layers

| API | Notes |
|---|---|
| `addSource` / `getSource` / `removeSource(id)` | |
| `addLayer(descriptor, beforeID)` | Named param `beforeID` |
| `removeLayer(id)` | |

## Timeline

`controller.timeline` - `controller.animationOptions`  
Playback: `play` / `pause` / `resume` / `stop` / `restart` / `reset` / `toggle` /
`playFromDate` / `goTo` / `goToDate` / `goToOffset`  
Range: `start`/`end`, `setStartDateUsingOffset`, `set*UsingRelativeTime`  
Events: `AnimationEvent.*` - Load: `onLoadStart` / `onLoadComplete` LiveData

## UI

| API | Notes |
|---|---|
| `LegendControl()` + `add(LegendControl)` | |
| `addLegend(WeatherConfiguration)` | |
| `addDataInspectorControl` / `removeDataInspectorControl` | |
| `DataInspectorControl.setPresentation(layerId, Presentation)` | |
| `WeatherConfiguration.presentation` | `weather.common.Presentation` + `Units` |

## Style

`StyleValue`, `Expression`, `*LayerDescriptor`, `*Paint` / `*LayerPaint`

## Version / docs

```
https://www.xweather.com/docs/api/releases/versions -> mapsgl-android-sdk
https://www.xweather.com/docs/mapsgl-android-sdk/
```
