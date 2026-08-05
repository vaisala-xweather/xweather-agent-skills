# MapsGL Apple SDK — legends

A `LegendControl` manages the set of legends visible for a map and renders them into a `UIView`. Add
one to the controller and the built-in weather layers bring their own legends automatically.

```swift
let legendControl = LegendControl()
controller.add(legendControl: legendControl)   // @MainActor
// …
controller.removeLegendControl()
```

Legends are reference-counted: several weather layers can share one legend, and it disappears only when
every layer referencing it is gone. Adding and removing weather layers keeps the control in step with
no extra work.

**`LegendControl`'s mutating methods are `@MainActor`** — `add(legendControl:)` on the controller, and
`update(legend:)` / `removeLegend(id:force:)` on the control. Mark any helper that builds and commits a
legend `@MainActor`, or it won't compile. Building the legend value itself is not isolated, so only the
commit needs it.

## Placing the control's view

The control does not place itself — that's the app's job. Fix the **width** and let the height follow
the intrinsic content size.

### SwiftUI

`LegendControlView` bridges the control into a SwiftUI hierarchy. It reuses the `LegendControl` already
added to the controller, so customizations and custom legends survive:

```swift
struct ContentView: View {
    @State private var controller: LegendControl.Host?   // your MapController

    var body: some View {
        ZStack {
            WeatherMapView(onReady: { controller = $0 })

            VStack {
                Spacer()
                HStack {
                    Spacer()
                    LegendControlView(mapControllerProvider: { controller })
                        .frame(maxWidth: 300)
                        .padding()
                }
            }
        }
    }
}
```

`LegendControl.Host` is the protocol `MapController` conforms to — `legendControl`,
`add(legendControl:)`, `removeLegendControl()`. Typing the state as the protocol keeps the view free of
the provider-specific controller type.

The provider is a closure, called when the view needs the control, so it tolerates a controller that
doesn't exist yet on first layout.

### UIKit

`legendControl.view` is a read-only `UIView`:

```swift
hostView.addSubview(legendControl.view)
legendControl.view.translatesAutoresizingMaskIntoConstraints = false
NSLayoutConstraint.activate([
    legendControl.view.widthAnchor.constraint(equalToConstant: 300),
    legendControl.view.trailingAnchor.constraint(equalTo: hostView.trailingAnchor, constant: -8),
    legendControl.view.bottomAnchor.constraint(equalTo: hostView.bottomAnchor, constant: -8),
])
```

## Control configuration

Settable before or after the control is added:

| Property | Type | Notes |
|---|---|---|
| `view` | `UIView` | Read-only container |
| `backgroundColor` | `UIColor` | |
| `cornerRadius` | `Double` | |
| `insets` | `UIEdgeInsets` | Padding inside the container |
| `isHidden` | `Bool` | |
| `units` | `MeasurementUnits` | `.metric` / `.imperial`, or per-dimension |
| `toggleUnitsOnTap` | `Bool` | Let the user switch units by tapping the legend |

Methods: `add(legend:)`, `getLegend(id:)`, `update(legend:)`, `removeLegend(id:force:)`,
`updateLegendViews()`.

`toggleUnitsOnTap` is worth enabling on consumer apps — it's free unit switching with no UI of your own.

## The two legend types

### Bar legends — continuous ranges

`BarLegend<UnitType>` is generic over a `Dimension` (e.g. `UnitTemperature`), which is what lets it
convert labels between unit systems.

```swift
func heatIndexLegend() -> any Legend {
    let stops = [
        ColorStop(26.67, .fromString("#f33300")),   //  80 °F
        ColorStop(32.22, .fromString("#d00000")),   //  90 °F
        ColorStop(37.78, .fromString("#720000")),   // 100 °F
        ColorStop(43.33, .fromString("#ce0046")),   // 110 °F
        ColorStop(48.89, .fromString("#ff4b98")),   // 120 °F
        ColorStop(54.44, .fromString("#ffadad")),   // 130 °F
    ]

    let item = BarLegendItem<UnitTemperature>(
        colorScaleOptions: ColorScaleOptions(stops: stops, range: 26.67...54.44)
    )
    .height(14)
    .rounded(false)
    .labels(BarLegendLabels()
        .values(.every { units in units == UnitTemperature.celsius ? 5 : 10 }))

    return BarLegend(id: "heat-index")
        .title("Heat Index")
        .measurement(.temperature)
        .currentUnits(.celsius)
        .labelColor(.white)
        .titleColor(.black)
        .items([item])
}

legendControl.add(legend: heatIndexLegend())
```

`BarLegend` properties (all with matching builder methods): `id`, `title`, `items`, `currentUnits`,
`baseUnits`, `measurement`, `titleColor`, `titleFont`, `labelColor`, `labelFont`, `units`, `resample`.

`BarLegendItem<UnitType>`: `colorScaleOptions`, `height`, `rounded`, `margins`, `labels`.

`BarLegendLabels<UnitType>`: `values`, `formatter`, `normalized`, `placement`, `textShadow`,
`textStroke`. Label values can be set several ways:

```swift
BarLegendLabels().values(every: 10)                  // fixed interval
BarLegendLabels().values(labelValues: [0, 32, 100])  // specific values
BarLegendLabels().values(.every { units in … })      // interval that depends on display units
BarLegendLabels().values(.labels { _ in
    [(0.0, "Uncomfortable"), (0.5, "Hot"), (1.0, "Dangerous")]
})
```

**`normalized` decides how label positions are read.** With `.labels` returning values in 0…1, set
`normalized(true)`, or the labels are interpreted as data values, fall outside
`colorScaleOptions.range`, and silently don't render — the most common "my labels vanished" cause:

```swift
var item = legend.items[0]
item.labels = item.labels
    .normalized(true)
    .values(.labels { _ in [(0.0, "Low"), (0.5, "Moderate"), (1.0, "Extreme")] })
legendControl.update(legend: legend.items([item]))
```

Pass the **same `ColorScaleOptions`** to the layer's `paint.sample.colorScale` and to the legend's
`colorScaleOptions`. Build it once in a `let` and hand it to both — separate copies drift.

### Point legends — categories

```swift
func airQualityLegend() -> any Legend {
    PointLegend(id: "air-quality")
        .title("Air Quality")
        .radius(6)
        .margins(CGSize(width: 3, height: 5))
        .items([
            PointLegendItem(color: .fromString("#29e11f"), label: "Good"),
            PointLegendItem(color: .fromString("#f8f92a"), label: "Moderate"),
            PointLegendItem(color: .fromString("#f9681b"), label: "Sensitive Groups"),
            PointLegendItem(color: .fromString("#f60115"), label: "Unhealthy"),
            PointLegendItem(color: .fromString("#7a2c83"), label: "Very Unhealthy"),
            PointLegendItem(color: .fromString("#65001b"), label: "Hazardous"),
        ])
}
```

`PointLegend`: `id`, `title`, `items`, `itemResolver`, `layerId`, `radius`, `margins`, `titleColor`,
`titleFont`, `labelColor`, `labelFont`, `units`.

`PointLegendItem(color: CGColor, label: String)`. Note `CGColor` — from a `UIColor`, use
`.cgColor`; from a hex string, `.fromString("#…")`.

`itemResolver` lets items be derived from the layer's data at render time instead of hardcoded.

## Overriding a weather layer's legend

**If you customize a categorical layer's paint, you must also override its legend.** Bar/color-scale
legends are re-derived from the layer's color scale automatically, so a custom `sample` scale updates
its own legend. Point legends cannot be inferred from paint, so a customized categorical layer keeps
the default legend — which then shows colors the map isn't using.

Build the color table once and drive both the expression and the legend from it:

```swift
let riskColors: [(risk: String, color: UIColor)] = [
    ("General",  .fromString("#ffea16")),
    ("Marginal", .fromString("#ffc41d")),
    ("Slight",   .fromString("#ff891d")),
    ("Enhanced", .fromString("#fa2311")),
    ("Moderate", .fromString("#fa23ec")),
    ("High",     .fromString("#fac9eb")),
]

var config = WeatherService.Convective(service: controller.service)

config.layer.paint.fill = .init(
    color: .expression(Expression.match(
        Expression.downcase(Expression.get("details.risk.type")),
        riskColors.map {
            Expression.Step(value: $0.risk.lowercased(), result: StyleColor.uiColor($0.color))
        },
        "#999999"
    ))
)

// Same source of truth — the legend cannot drift from the map.
config.legend = PointLegend(id: "convective")
    .title("Convective")
    .items(riskColors.map { PointLegendItem(color: $0.color.cgColor, label: $0.risk) })

try controller.addWeatherLayer(config: config)
```

Setting `config.legend` before adding is better than adding the layer and patching the control
afterwards: there's no window where the wrong legend is on screen, and the legend is removed with the
layer.

## Updating a legend in place

`Legend` values are value types with builder methods, so "updating" means producing a modified copy and
committing it:

```swift
legendControl.backgroundColor = .black
legendControl.update(legend: legend.titleColor(.white).labelColor(.white))
```

Updating a bar legend's color scale:

```swift
let options = ColorScaleOptions(stops: newStops)
let updated = legend.items(legend.items.map { $0.colorScaleOptions(options) })
legendControl.update(legend: updated)
```

`update(legend:)` matches on `id`, so keep ids stable across updates.

## Removing legends

```swift
legendControl.removeLegend(id: "air-quality")
legendControl.removeLegend(id: "air-quality", force: true)
```

Because legends are reference-counted, `removeLegend` decrements rather than deletes — a legend shared
by two layers survives the first call. `force: true` deletes regardless. Reach for `force` only when
you know no layer still needs it; otherwise a later layer removal leaves the map without its legend.

## Dark mode

The control's colors are set explicitly, not derived from the trait collection, so respond to the
color scheme yourself:

```swift
// SwiftUI
.onChange(of: colorScheme) { scheme in
    legendControl.backgroundColor = (scheme == .dark) ? .black : .white
    legendControl.update(legend: legend
        .titleColor(scheme == .dark ? .white : .black)
        .labelColor(scheme == .dark ? .white : .black))
}
```

Docs: https://www.xweather.com/docs/mapsgl-apple-sdk/getting-started/legends ·
https://www.xweather.com/docs/mapsgl-apple-sdk/controls/legend ·
https://www.xweather.com/docs/mapsgl-apple-sdk/advanced/legends ·
https://www.xweather.com/docs/mapsgl-apple-sdk/reference/legends
