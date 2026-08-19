# Expressions & StyleValue - MapsGL Android

Verified against `com.xweather.mapsgl.style.Expression`, `StyleValue`, and the vector style
evaluators on the `feature/maptime-filter` branch.

A paint property is either a constant or an expression evaluated per feature. `Expression` builds
Mapbox-style trees; `StyleValue` is the wrapper a paint property actually holds.

## `StyleValue`

```kotlin
sealed class StyleValue<out T> {
    data class Constant<T>(val value: T) : StyleValue<T>()
    data class Expression(val expression: com.xweather.mapsgl.style.Expression) : StyleValue<Nothing>()
}
```

Read it back with `constantValue`, `expressionValue`, or `resolvedValue` (whichever side is set).

```kotlin
paint.fill.color = StyleValue.Constant(Color.Red)
paint.fill.color = StyleValue.Expression(Expression.get("color"))
```

Plain `Float` properties like `paint.opacity` are **not** wrapped - assign `0.7f` directly. Only the
data-driven paint properties take a `StyleValue`.

## Reading feature properties

```kotlin
Expression.get("temperature")        // top-level property
Expression.getPath("report.type")    // nested; get() auto-delegates when the name contains '.'
Expression.has("color")              // property present?
Expression.hasPath("report.type")
```

`get("a.b")` is rewritten to `getPath("a.b")` automatically, so either spelling works for nested
properties.

## Map state

```kotlin
Expression.zoom            // ["zoom"]
Expression.geometryType    // ["geometry-type"]
Expression.mapTime         // ["map-time"] - timeline playhead, Unix seconds
Expression.time            // ["time"] - alias for mapTime
```

`mapTime` is the **animation playhead**, not wall clock. See "Animating a filter over time" below.

## Branching

### `match` - discrete values to results

```kotlin
Expression.match(
    Expression.get("severity"),
    listOf(
        Expression.Step("extreme",  Color.Red),
        Expression.Step("severe",   Color(0xFFFF6600)),
        Expression.Step("moderate", Color.Yellow),
    ),
    fallback = Color.Gray,
)
```

`Step(value, result)` is the pair type; `match` flattens them into `["match", input, v1, r1, …, fallback]`.

### `step` - thresholds

```kotlin
Expression.step(
    Expression.get("magnitude"),
    listOf(
        Expression.Step(null, Color.Green),   // first stop: result only, no threshold
        Expression.Step(3.0,  Color.Yellow),
        Expression.Step(5.0,  Color.Red),
    ),
)
```

The **first** `Step` carries only a result - its `value` is the default below the first threshold and
is dropped when flattening. Subsequent stops are `threshold, result` pairs.

### `interpolate` - continuous ramps

```kotlin
Expression.interpolate(
    Expression.get("value"),
    listOf(0.0, Color.Blue, 50.0, Color.Yellow, 100.0, Color.Red),
)

// with an explicit interpolation type
Expression.interpolate(listOf("linear"), Expression.get("value"), stops)
Expression.interpolateExponential(base, input, stops)
Expression.interpolateCubicBezier(x1, y1, x2, y2, input, stops)
```

There are two `interpolate` overloads - a two-argument one that assumes linear, and a
three-argument one taking the interpolation type first.

### `switchCase` - arbitrary conditions

```kotlin
Expression.switchCase(
    listOf(
        Expression.Case(Expression.greaterThan(Expression.get("wind"), 50), Color.Red),
        Expression.Case(Expression.greaterThan(Expression.get("wind"), 25), Color.Yellow),
    ),
    fallback = Color.Green,
)
```

`Case(condition, result)`; emitted as `["case", …]`.

### `coalesce` - first non-null

```kotlin
Expression.coalesce(listOf(Expression.get("name_en"), Expression.get("name"), "Unknown"))
```

## Operator reference

Everything on `Expression`'s companion. The map-state entries are `val`s holding raw arrays; the
rest are factory functions returning an `Expression`.

| Group | Operators |
|---|---|
| Data | `get` `getPath` `has` `hasPath` `literal` `at` `length` `slice` `indexOf` `contains` |
| Map state | `zoom` `geometryType` `mapTime` `time` |
| Branching | `match` `step` `switchCase` `coalesce` |
| Interpolation | `interpolate` `interpolateExponential` `interpolateCubicBezier` |
| Comparison | `equals` `notEquals` `lessThan` `lessThanOrEqual` `greaterThan` `greaterThanOrEqual` |
| Logic | `and` `or` `not` |
| Arithmetic | `add` `subtract` `multiply` `divide` `mod` `abs` `ceil` `floor` `round` `min` `max` |
| String | `concat` `join` `upcase` `downcase` `format` |
| Color | `rgb` `rgba` |
| Casting | `toNumber` `toString` `toBoolean` `toJSONObject` |
| Variables | `bind` `variable` |

Helper types: `Expression.Step(value, result)`, `Expression.Case(condition, result)`,
`Expression.Variable(key, value)`.

`format(parts)` takes `List<Pair<StyleValue<String>, TextFormatOptions>>` for rich text runs, not a
plain string list.

## Filters on layer descriptors

Every layer descriptor carries `var filter: Expression?`. A filter is a boolean expression - features
that evaluate false are not drawn.

```kotlin
descriptor.filter = Expression.and(listOf(
    Expression.equals(Expression.get("type"), Expression.literal("SV")),
    Expression.greaterThan(Expression.get("severity"), Expression.literal(2)),
))
```

The vector style evaluators handle a broad operator set - `==` `!=` `<` `<=` `>` `>=` `!` `all` `any`
`case` `match` `step` `coalesce` `concat` `get` `has` `literal` `downcase` `upcase` `to-string`
`to-number` `zoom`, plus arithmetic in the circle evaluator. That is a large subset but **not** all
of Mapbox's expression language, so a filter leaning on an operator outside this list may silently
fail to match rather than erroring - keep filters to the list above and test on device.

## Animating a filter over time

`["map-time"]` resolves to the **timeline playhead** in Unix seconds, so a filter referencing it
re-evaluates as the animation runs. This is how time-windowed features (lightning strikes fading,
storm-cell tracks revealing) work without rebuilding geometry every frame.

```kotlin
// Show only features whose timestamp is at or before the playhead
descriptor.filter = Expression.lessThanOrEqual(
    Expression.get("timestamp"),
    Expression.mapTime,
)
```

The SDK splits such a filter internally: the clauses that don't reference map-time are applied once
when geometry is prepared, and the map-time clauses are re-applied at draw time - on the CPU for
symbols, and as a GPU reveal for fill and line using a baked feature time. A top-level `["all", …]`
is partitioned clause by clause; any other shape goes wholly to one side.

That splitting is internal - you write one filter and the SDK does the rest. The legacy spellings
`"mapTime"` and `"timeline"` are also accepted.

Playback itself is driven by `controller.timeline`, not by the filter. See `references/timeline.md`.

## Colors

Paint colors are `androidx.compose.ui.graphics.Color` (Compose), **not** `android.graphics.Color`
ints. `StyleColor` additionally accepts hex and rgba strings:

```kotlin
StyleColor.Color(Color.Red)
StyleColor.Hex("#ff0000")
StyleColor.RGBA("rgba(255,0,0,1)")
```

`Expression.rgb(r, g, b)` and `rgba(r, g, b, a)` build colors inside an expression tree, where each
component may itself be an expression.

## Caveats

- **`opacity` is a plain `Float`.** Only data-driven paint properties take a `StyleValue`.
- **The first `step` stop has no threshold** - passing one silently shifts the ramp.
- **Filters are not full Mapbox.** Stay on the operator list above.
- **`mapTime` is the playhead, not the clock.** It moves only while the timeline moves.

Cookbooks for alerts, earthquakes and other real layers: `references/data-driven.md`.
Paint properties by render type: `references/weather-styling.md`.
