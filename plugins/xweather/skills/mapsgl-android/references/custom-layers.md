# Custom map layers - MapsGL Android (1.6.x)

Verified against SDK layer descriptors + `MapController.addLayer(descriptor, beforeID)` (1.6.x).
Docs are secondary:
https://www.xweather.com/docs/mapsgl-android-sdk/advanced/layers\r\n\r\n## Fill example (alerts MVT)

```kotlin
import androidx.compose.ui.graphics.Color

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

Parameter name is **`beforeID`** (Kotlin). Some docs snippets say `beforeId` /
`insertBeforeId` - use `beforeID` for `addLayer`.

## Remove

```kotlin
controller.removeLayer("alerts-fill")
controller.removeSource("alerts")
```

## Notes

- `source` on the descriptor must match the source id from `addSource`.
- For MVT, set `sourceLayer` when the tile has named layers; GeoJSON usually uses
  `sourceLayer = null`.
- Weather products: prefer `addWeatherLayer` - see `weather-layers.md` /
  `weather-styling.md`.
