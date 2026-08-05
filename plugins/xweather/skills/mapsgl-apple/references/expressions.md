# MapsGL Apple SDK — expressions

`Expression` builds data-driven paint values and layer filters. It's the Swift face of Mapbox-style
style expressions: an operator plus arguments, evaluated per feature (or per map state).

Two ways into a paint property:

```swift
color: .constant(.red)                            // static
color: .expression(Expression.get("COLOR"))       // data-driven
```

`StyleValue<T>` has exactly those two cases. Any styleable property accepts either.

Expressions are built with **static factory methods**, not array literals. `Expression(_ raw: Any)`
does accept a raw array, and `StyleValue.fromExpressionArray(_:)` exists, but prefer the factories —
they're type-checked at the call site and read far better in a diff.

## Reading feature properties

```swift
Expression.get("COLOR")                    // top-level property
Expression.get("details.risk.type")        // nested, dot-notation
Expression.getPath("a.b.c")                // explicit key-path form
Expression.has("COLOR", in: nil)           // property exists?
Expression.hasPath("details.risk")
```

Dot-notation in `get` walks nested objects, which is how most Xweather GeoJSON payloads are shaped —
earthquake features carry `report.mag` and `report.type`, convective outlooks carry
`details.risk.type`.

Vector tile properties are flat and SHOUTY (`COLOR`, `ADVISORY`, `CAT`, `VTEC`); GeoJSON from the
Weather API is nested and camelCase. Check the actual payload before writing the key — a wrong key
yields no error, just unstyled features.

## Map state

```swift
Expression.zoom             // static let: current zoom
Expression.pitch
Expression.geometryType
Expression.id
Expression.properties
```

For non-vector layers (`sample`, `particle`, …) map state is essentially all an expression can see,
since there are no discrete features to read.

## Branching

### `match` — discrete values to results

The most common shape. Takes an input, an array of `Expression.Step`, and a fallback:

```swift
Expression.match(
    Expression.downcase(Expression.get("report.type")),
    [
        Expression.Step(value: "mini",     result: UIColor.fromString("#6fb314")),
        Expression.Step(value: "minor",    result: UIColor.fromString("#dfcb01")),
        Expression.Step(value: "moderate", result: UIColor.fromString("#ff5d01")),
        Expression.Step(value: "major",    result: UIColor.fromString("#ce0052")),
    ],
    "#999999"
)
```

`Expression.Step<T>` is `init(value:result:)`. Building the steps by mapping over a table keeps the
colors and the legend labels from drifting apart:

```swift
let riskColors: [(risk: String, color: UIColor)] = [
    ("General",  .fromString("#ffea16")),
    ("Marginal", .fromString("#ffc41d")),
    ("Slight",   .fromString("#ff891d")),
]

let colorExpression = Expression.match(
    Expression.downcase(Expression.get("details.risk.type")),
    riskColors.map { Expression.Step(value: $0.risk.lowercased(), result: StyleColor.uiColor($0.color)) },
    "#999999"
)
// ...and the same array feeds PointLegendItem(color:label:) — see legends.md
```

Wrap the input in `downcase` whenever the data's casing isn't guaranteed. Mixed-case source values
silently falling through to the fallback is a common bug.

### `step` — thresholds

```swift
Expression.step(Expression.get("report.mag"), [
    Expression.Step(value: 0.0, result: 5.0),
    Expression.Step(value: 4.0, result: 10.0),
    Expression.Step(value: 6.0, result: 18.0),
])
```

Produces hard jumps at each threshold rather than a blend.

### `interpolate` — continuous ramps

```swift
Expression.interpolate(Expression.get("report.mag"), stops: [0.0, 4.0, 8.0, 20.0])
Expression.interpolate(["linear"], Expression.get("report.mag"), [0.0, 4.0, 8.0, 20.0])
Expression.interpolateExponential(Expression.zoom, base: 1.5, stops: [4, 2.0, 12, 8.0])
Expression.interpolateCubicBezier(Expression.zoom, controlPoints: [0.4, 0, 0.6, 1], stops: [4, 2.0, 12, 8.0])
```

`interpolate(_:stops:)` and the three-argument form both exist; stops alternate input value and output
value.

### `switchCase` — arbitrary conditions

```swift
Expression.switchCase([
    (condition: Expression.greaterThan(Expression.get("report.mag"), 6.0), result: UIColor.red),
    (condition: Expression.greaterThan(Expression.get("report.mag"), 4.0), result: UIColor.orange),
], fallback: UIColor.gray)
```

Use this when the branches test different properties; `match` and `step` only branch on one input.

### `coalesce` — first non-null

```swift
Expression.coalesce([Expression.get("COLOR"), Expression.get("color"), "#999999"])
```

## Operator reference

**Lookup / existence**
`get(_:)` · `getPath(_:)` · `has(_:in:)` · `hasPath(_:)` · `at(_:in:)` · `indexOf(_:in:)` ·
`length(_:)` · `slice(_:_:_:)` · `contains(_:in:)` · `properties` · `id` · `geometryType`

**Comparison**
`equals(_:_:)` · `notEquals(_:_:)` · `lessThan(_:_:)` · `lessThanOrEqual(_:_:)` ·
`greaterThan(_:_:)` · `greaterThanOrEqual(_:_:)`

**Logic**
`and(_:)` · `or(_:)` · `not(_:)`

**Branching**
`match(_:_:_:)` · `step(_:_:)` · `switchCase(_:fallback:)` · `coalesce(_:)` · `interpolate(_:stops:)` ·
`interpolate(_:_:_:)` · `interpolateExponential(_:base:stops:)` ·
`interpolateCubicBezier(_:controlPoints:stops:)`

**Arithmetic**
`add(_:_:)` · `subtract(_:)` · `subtract(_:_:)` · `multiply(_:_:)` · `divide(_:_:)` · `mod(_:_:)` ·
`pow(_:_:)` · `abs(_:)` · `ceil(_:)` · `floor(_:)` · `round(_:)` · `sqrt(_:)` · `min(_:)` · `max(_:)` ·
`ln(_:)` · `ln2()` · `log2(_:)` · `log10(_:)` · `e()` · `pi()` · `random(min:max:seed:)`

**Trigonometry**
`sin(_:)` · `cos(_:)` · `tan(_:)` · `asin(_:)` · `acos(_:)` · `atan(_:)`

**Type coercion / testing**
`toBoolean(_:)` · `toBoolean(_:fallback:)` · `toNumber(_:)` · `toString(_:)` · `typeof(_:)` ·
`isArray(_:)` · `isArray(_:type:)` · `isArray(_:type:length:)` · `isNumber(_:fallback:)` ·
`isObject(_:fallback:)` · `isString(_:fallback:)` · `literal(_:)`

**Strings**
`concat(_:)` · `upcase(_:)` · `downcase(_:)` · `format(_:)` · `numberFormat(_:options:)`

**Color**
`rgb(_:_:_:)` · `rgba(_:_:_:_:)`

**Variables**
`bind(_:output:)` · `variable(_:)` — bind intermediate values once and reuse them:

```swift
Expression.bind([("mag", Expression.get("report.mag"))],
                output: Expression.greaterThan(Expression.variable("mag"), 5.0))
```

**Introspection** (on an expression instance)
`raw` · `asArray()` · `toJSONObject()` · `evaluateLiteral()`

## Complete example — two properties from one field

Color *and* size driven by earthquake magnitude class:

```swift
let magnitudeColors: [(type: String, color: UIColor, radius: Double)] = [
    ("mini",         .fromString("#6fb314"),  5),
    ("minor",        .fromString("#dfcb01"),  8),
    ("light",        .fromString("#ce8f00"),  9),
    ("moderate",     .fromString("#ff5d01"), 10),
    ("strong",       .fromString("#e90004"), 12),
    ("major",        .fromString("#ce0052"), 14),
    ("great",        .fromString("#b90285"), 17),
    ("catastrophic", .fromString("#f500ff"), 20),
]

let magnitudeClass = Expression.downcase(Expression.get("report.type"))

let layer = CircleLayerDescriptor(
    id: "earthquakes",
    source: "earthquakes",
    paint: .init(
        fill: .init(color: .expression(Expression.match(
            magnitudeClass,
            magnitudeColors.map { Expression.Step(value: $0.type, result: $0.color) },
            "#999999"
        ))),
        stroke: .init(color: .constant(.white), thickness: .constant(3)),
        circle: .init(radius: .expression(Expression.match(
            magnitudeClass,
            magnitudeColors.map { Expression.Step(value: $0.type, result: $0.radius) },
            5.0
        )))
    )
)
_ = try controller.addLayer(layer)
```

Sizing as well as coloring is what makes the visualization readable — a single hue per magnitude class
tells the user much less than radius plus hue.

## Filters

`filter` on a vector layer descriptor is an `Expression?`. Rejected features are never rendered:

```swift
var layer = CircleLayerDescriptor(id: "big-quakes", source: "earthquakes", paint: paint)
layer.filter = Expression.and([
    Expression.greaterThan(Expression.get("report.mag"), 4.0),
    Expression.notEquals(Expression.get("report.type"), "mini"),
])
```

Encoded layers (`sample`, `particle`, `grid`, `contour`, `raster`) have no `filter` — restrict them by
value with `paint.sample.drawRange` instead. See `styles.md`.

## Caveats

- **Data-driven styling is really a vector feature.** For `sample`, `particle`, and other encoded
  layers, expressions only see map state, not per-pixel data values. Use color scales and `drawRange`
  to express data there.
- **Some paint properties are resolved once**, before data buffers are built, and can't be updated
  after the layer exists. Set them in the descriptor rather than mutating later.
- **A wrong property key fails silently.** Features either take the fallback or don't render;
  there's no diagnostic. When output looks wrong, verify the key against the real payload first — for
  Xweather sources, request the same data as JSON and read one feature.

Docs: https://www.xweather.com/docs/mapsgl-apple-sdk/styling/data-driven
