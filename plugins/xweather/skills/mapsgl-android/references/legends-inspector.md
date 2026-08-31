# Legends & data inspector - MapsGL Android

Verified against `LegendControl`, `Legend`, `BarLegend`, `PointLegend`, `LegendCode`,
`DataInspectorControl`, `Presentation` and `MeasurementUnits` at the SDK's `release/1.6.1` tag.
Docs are secondary when they disagree:
https://www.xweather.com/docs/mapsgl-android-sdk/getting-started/legends ·
https://www.xweather.com/docs/mapsgl-android-sdk/controls/data-inspector

## `LegendControl`

```kotlin
val legendControl = LegendControl().apply { mapView = binding.mapView }
controller.add(legendControl)

parentLayout.addView(legendControl.getView())   // LegendContainerView
```

Built-in weather layers register and unregister their own legends once the control is attached.
Several layers can share one legend - it is removed only when the last referencing layer goes. That
ref-counting is why removing one layer sometimes leaves a legend on screen, which is correct rather
than a bug.

Position `getView()` with normal `ConstraintLayout` / `FrameLayout` params; the docs suggest
bottom-end with ~16dp margins and ~300dp width.

### Configuration

```kotlin
legendControl.units = MeasurementUnits.IMPERIAL   // or METRIC
legendControl.toggleUnitsOnTap = true             // default
legendControl.onUnitsToggled = { units -> /* mirror elsewhere in your UI */ }
legendControl.isHidden = false
legendControl.maxLegendContentHeightDp = 240
legendControl.backgroundColor = Color.Transparent  // Compose Color, not android.graphics.Color
legendControl.setHostTitleColor(Color.White)

legendControl.applyUnits(MeasurementUnits.METRIC)
legendControl.toggleUnits()
```

`toggleUnitsOnTap` is on by default, so tapping the legend flips imperial/metric whether or not you
wired anything up. Use `onUnitsToggled` to keep the rest of your UI in step.

`backgroundColor` and `setHostTitleColor` take **Compose** `androidx.compose.ui.graphics.Color` -
passing an `android.graphics.Color` int will not compile.

### Dark mode

```kotlin
legendControl.setDarkTheme(true)
legendControl.usesDarkTheme = true
```

`setDarkTheme` swaps the panel colour (roughly `0xCC000000` dark, `0xE6FFFFFF` light) and restyles
legends as they are added. Set it before adding layers so their legends pick it up.

## The two legend types

`Legend` is the interface (`id`, `title`, `titleFontSize`, `titleColorValue`, `units`). Two
implementations ship.

### `BarLegend` - continuous ranges

```kotlin
BarLegend<UnitType>(
    id = "my-legend",
    items = listOf(
        BarLegendItem(
            colorScaleOptions = ColorScaleOptions(stops = listOf(/* ... */)),
            labels = BarLegendLabels(values = /* Values<UnitType> */, placement = Placement.MIDDLE),
            height = BarLegendDefaults.barHeight,
            rounded = true,
        )
    ),
    title = "Temperature",
    measurement = MeasurementUnits.MeasurementType.TEMPERATURE,
    units = MeasurementUnits.IMPERIAL,
    resample = null,          // optional EasingCurve to redistribute the ramp
)
```

Generic over a `Dimension` unit type, and `currentUnits` defaults from `units.dimensions(measurement)`
- so setting `measurement` is what makes unit switching work. `MeasurementType` covers `TEMPERATURE`,
`TEMPERATURE_DELTA`, `SPEED`, `PRESSURE`, `DISTANCE`, `HEIGHT`, `PRECIPITATION`, `SNOWFALL`,
`DIRECTION`, `TIME`.

Each `BarLegendItem` carries its own `ColorScaleOptions`, so one legend can stack several bars.

### `PointLegend` - discrete categories

```kotlin
PointLegend(
    id = "alerts-legend",
    title = "Alerts",
    items = listOf(
        PointLegendItem(color = 0xFFFF0000.toInt(), label = "Warning"),
        PointLegendItem(color = 0xFFFFA500.toInt(), label = "Watch"),
    ),
    radius = 6.0,
    units = MeasurementUnits.IMPERIAL,
)
```

Note the asymmetry: **`PointLegendItem.color` is an `@ColorInt` Int**, not a Compose `Color`, unlike
everything else in the legend API.

`itemResolver` plus `layerId` lets a point legend build its items from the features actually on screen
rather than a fixed list - that is how the alerts legend shows only the alert types currently visible.
`layerId` is treated as a **regex**, so it can match a family of layer ids.

## Built-in legends

`LegendCode` is an auto-generated enum of **63** legend ids, each able to build its legend:

```kotlin
val legend: Legend = LegendCode.ACCUM_PRECIP.getLegend()
```

Codes are id-style strings - `accum-precip`, `accum-snow`, `air-quality-index`,
`air-quality-index-cai`, and so on. Use it to start from a stock legend and adjust, rather than
building a colour ramp from scratch.

**`LegendCode` and `LayerCode` are different enums with different names for the same thing.** The
temperature legend is `LegendCode.TEMPERATURE` (singular) while the layer is `LayerCode.TEMPERATURES`
(plural), and there are 63 legend codes against 209 layer codes, so there is no one-to-one mapping.
Look the legend code up rather than deriving it from the layer code.

Do not hand-edit `LegendCode.kt`; it is generated.

## Overriding a weather layer's legend

Every `WeatherLayerConfiguration` carries `var legend: Legend?`. Set it before adding the layer:

```kotlin
val config = WeatherService.Temperatures(controller.service)
config.legend = LegendCode.TEMPERATURE.getLegend().apply { title = "Temp (F)" }
controller.addWeatherLayer(config)
```

**Whenever you customize a categorical layer's paint, override its legend too** - the stock legend
describes the stock colours and will otherwise disagree with what is drawn.

`controller.addLegend(forConfig)` registers a configuration's legend explicitly, which is useful when
you built the configuration but added its layers by another route.

## Updating and removing

```kotlin
legendControl.add(legend)
legendControl.replaceLegend(id, newLegend)     // swap in place, keeps position
legendControl.legends                          // Map<String, Legend>, read-only view
controller.removeLegendControl()
```

`replaceLegend` is the way to change a legend that is already on screen - removing and re-adding
disturbs ordering and loses the ref count.

## `DataInspectorControl`

```kotlin
val control = controller.addDataInspectorControl(binding.mapView)
controller.removeDataInspectorControl()

control.cancelCalloutWhenOffScreen = true      // default
control.show(screenPoint, coordinate)
control.move(screenPoint)
control.update()
control.hide()
control.bringCalloutToFront()
```

Also reachable as `controller.dataInspector` without adding it.

### Presentations - formatting the callout

A `Presentation` has a title and a function turning the feature payload into display text.

```kotlin
import com.xweather.mapsgl.weather.common.Presentation
import com.xweather.mapsgl.weather.common.Units

val tempsConfig = WeatherService.Temperatures(controller.service)
tempsConfig.presentation = Presentation(
    title = "Temperature (F)",
    fn = { features ->
        val featureMap = features as? Map<*, *> ?: return@Presentation ""
        val tempC = (featureMap["value"] as? Float) ?: return@Presentation ""
        String.format("%.1f", Units.CtoF(tempC))
    },
)
controller.addWeatherLayer(tempsConfig)
```

**Encoded values are metric** - temperature in °C, wind in m/s - so convert in the presentation.
`Units` carries the helpers (`CtoF`, `msToMph`, …).

Wind layers expose `value` and `angle`. **`angle` is the direction the wind is blowing *toward*;** the
meteorological "from" bearing is `angle - 180`:

```kotlin
val windsConfig = WeatherService.WindSpeeds(controller.service)
windsConfig.presentation = Presentation(
    title = "Winds (mph)",
    fn = { features ->
        val featureMap = features as? Map<*, *> ?: return@Presentation ""
        val speedMs = (featureMap["value"] as? Float) ?: return@Presentation ""
        val angleDeg = (featureMap["angle"] as? Float) ?: return@Presentation ""
        "${String.format("%.1f", Units.msToMph(speedMs))}, ${String.format("%.0f", angleDeg - 180)} degrees"
    },
)
controller.addWeatherLayer(windsConfig)
```

### Setting a presentation after the layer exists

`setPresentation` keys on the **style layer id**, not `LayerCode` - resolve it first:

```kotlin
controller.getWeatherLayer(LayerCode.TEMPERATURES)?.let { layer ->
    control.setPresentation(layer.id, tempsPresentation)
}
control.removePresentation(layerId)
```

Passing `LayerCode.TEMPERATURES.value` or the string `"temperatures"` will not match.

## Attribution

The Mapbox logo and attribution are `MapView` settings and are governed by Mapbox's terms. Xweather's
own "Powered by Vaisala Xweather" credit is separate and always required - see the attribution
section of `SKILL.md`.
