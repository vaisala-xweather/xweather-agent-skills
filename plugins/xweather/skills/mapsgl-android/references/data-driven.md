# Data-driven styling - MapsGL Android

Verified against SDK `Expression` / `StyleValue` / paint APIs (1.6.x).
Docs cookbooks are secondary:
https://www.xweather.com/docs/mapsgl-android-sdk/styling/data-driven ,
https://www.xweather.com/docs/mapsgl-android-sdk/advanced/layers

## Property -> style (`get` / `concat`)

Alerts MVT features expose `COLOR` as hex **without** `#`:

```kotlin
val config = WeatherService.Alerts(controller.service) as WeatherLayerConfiguration<*, *>
val paint = config.layer.paint as FillLayerPaint
paint.fill = FillPaint(
    color = StyleValue.Expression(
        Expression.concat(listOf("#", Expression.get("COLOR"))),
    ),
)
paint.stroke = StrokePaint(color = StyleValue.Constant(Color.Black))
controller.addWeatherLayer(config)
```

## `match` / `Step` (categorical)

```kotlin
val config = WeatherService.Earthquakes(controller.service) as WeatherLayerConfiguration<*, *>
val paint = config.layer.paint as CircleLayerPaint
paint.fill.color = StyleValue.Expression(
    Expression.match(
        Expression.downcase(Expression.get("report.type")),
        listOf(
            Expression.Step("mini", "#6fb314"),
            Expression.Step("minor", "#dfcb01"),
            Expression.Step("light", "#ce8f00"),
            Expression.Step("moderate", "#ff5d01"),
            Expression.Step("strong", "#e90004"),
            Expression.Step("major", "#ce0052"),
            Expression.Step("great", "#b90285"),
            Expression.Step("catastrophic", "#f500ff"),
        ),
        "#999999",
    ),
)
paint.circle.radius = StyleValue.Expression(
    Expression.match(
        Expression.downcase(Expression.get("report.type")),
        listOf(
            Expression.Step("minor", 8),
            Expression.Step("moderate", 10),
            Expression.Step("major", 14),
            Expression.Step("catastrophic", 20),
        ),
        5,
    ),
)
controller.addWeatherLayer(config)
```

## Custom fill from a vector source

```kotlin
controller.addSource(
    VectorSourceDescriptor(id = "alerts").apply {
        url = "https://maps{s}.aerisapi.com/[CLIENT_ID]_[CLIENT_SECRET]/alerts/{z}/{x}/{y}/0.pbf"
    },
)
controller.addLayer(
    FillLayerDescriptor(
        id = "alerts-fill",
        source = "alerts",
        paint = FillLayerPaint(
            fill = FillPaint(
                color = StyleValue.Expression(
                    Expression.concat(listOf("#", Expression.get("COLOR"))),
                ),
            ),
            stroke = StrokePaint(color = StyleValue.Constant(Color.Black)),
        ),
    ),
    beforeID = null,
)
```

## Notes

- Use `androidx.compose.ui.graphics.Color` with `StyleValue.Constant` for solid colors.
- Not every paint property is re-evaluated every frame after buffers are built -
  check the SDK paint/renderer behavior for limits.
- Filter expressions on descriptors are a **smaller** supported subset for GLES
  stencil paths - see `expressions.md`.
