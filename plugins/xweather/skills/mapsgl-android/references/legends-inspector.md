# Legends & data inspector - MapsGL Android

Verified against SDK `LegendControl`, `DataInspectorControl`, `Presentation`, `Units` (1.6.x).
Docs are secondary if they disagree:
https://www.xweather.com/docs/mapsgl-android-sdk/getting-started/legends ,
https://www.xweather.com/docs/mapsgl-android-sdk/controls/data-inspector

## LegendControl

```kotlin
val legendControl = LegendControl()
controller.add(legendControl)
legendControl.setDarkTheme(true) // optional

val legendView = legendControl.getView()
parentLayout.addView(legendView)
// Position with ConstraintLayout / FrameLayout params (docs: bottom-end, ~16dp margins, ~300dp width)
```

Built-in weather layers add/remove legends automatically once the control is
attached. Multiple layers may share one legend - it is removed only when all
referencing layers are gone.

Custom paint on a weather config is reflected in the legend when you mutate
paint before `addWeatherLayer` (see `weather-styling.md`).

For fully custom legends on custom layers, see the advanced legends guide:
https://www.xweather.com/docs/mapsgl-android-sdk/advanced/legends

## DataInspectorControl

```kotlin
val control = controller.addDataInspectorControl(mapView)
controller.removeDataInspectorControl()
```

### Custom presentation on the weather config

```kotlin
import com.xweather.mapsgl.weather.common.Presentation
import com.xweather.mapsgl.weather.common.Units

val tempsConfig = WeatherService.Temperatures(controller.service)
tempsConfig.presentation = Presentation(
    title = "Temperature (-F)",
    fn = { features ->
        val featureMap = features as? Map<*, *> ?: return@Presentation ""
        val tempC = (featureMap["value"] as? Float) ?: return@Presentation ""
        String.format("%.1f", Units.CtoF(tempC))
    },
)
controller.addWeatherLayer(tempsConfig)
```

Encoded values are metric (temperature -C, wind m/s). Wind layers may expose
`value` and `angle` (direction **to**; weather "from" is often `angle - 180`).

```kotlin
val windsConfig = WeatherService.WindSpeeds(controller.service)
windsConfig.presentation = Presentation(
    title = "Winds (mph)",
    fn = { features ->
        val featureMap = features as? Map<*, *> ?: return@Presentation ""
        val speedMs = (featureMap["value"] as? Float) ?: return@Presentation ""
        val angleDeg = (featureMap["angle"] as? Float) ?: return@Presentation ""
        val fromAngle = angleDeg - 180
        "${String.format("%.1f", Units.msToMph(speedMs))}, ${String.format("%.0f", fromAngle)} degrees"
    },
)
controller.addWeatherLayer(windsConfig)
```

### Custom presentation after the layer exists

```kotlin
val tempsPresentation = Presentation(
    title = "Temperature (-F)",
    fn = { features ->
        val featureMap = features as? Map<*, *> ?: return@Presentation ""
        val tempC = (featureMap["value"] as? Float) ?: return@Presentation ""
        String.format("%.1f", Units.CtoF(tempC))
    },
)
controller.getWeatherLayer(LayerCode.TEMPERATURES)?.let { layer ->
    control.setPresentation(layer.id, tempsPresentation)
}
```

## Attribution

Mapbox attribution/logo are MapView settings. Follow Mapbox / Xweather terms for
production credits.
