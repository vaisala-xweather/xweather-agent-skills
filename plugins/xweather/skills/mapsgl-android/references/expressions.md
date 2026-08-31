# Expressions & StyleValue - MapsGL Android

Verified against `com.xweather.mapsgl.style.Expression` and `StyleValue` at the SDK's
`release/1.6.1` tag.

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
```

These are the only two map-state values on the companion in 1.6.1. There is no expression for the
timeline playhead - a filter cannot follow the animation clock in this release. Drive time-varying
content through `controller.timeline` instead (`references/timeline.md`).

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
Expression.interpolateExponential(input, base, stops)
Expression.interpolateCubicBezier(input, listOf(x1, y1, x2, y2), stops)
```

There are two `interpolate` overloads - a two-argument one that assumes linear, and a
three-argument one taking the interpolation type first. The exponential and cubic-bezier
siblings both take **`input` first**, then their curve parameters - and `interpolateCubicBezier`
takes the four control points as a single `List<Double>`, not four arguments.

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
| Map state | `zoom` `geometryType` |
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

In 1.6.1 vector weather layers are drawn as **Mapbox style layers**, and the descriptor's
`filter` is handed straight to Mapbox (`paintStyle.filter` in `MapboxMapController`). Mapbox
evaluates it, so the full Mapbox filter expression language is available - not a MapsGL subset.
The constraint is the other direction: an operator that `Expression` has no factory for has to be
built by hand as a raw list via the `Expression(raw)` constructor.

## Colors

Paint colors are `androidx.compose.ui.graphics.Color` (Compose), **not** `android.graphics.Color`
ints.

The SDK source has a `StyleColor` sealed class with `Color` / `Hex` / `RGBA` cases, but it is
**not in the published artifact** - it is minified away, so a consumer cannot reference it. Build
colors as Compose `Color`, or as strings inside an expression via `Expression.rgb` / `rgba`.

`Expression.rgb(r, g, b)` and `rgba(r, g, b, a)` build colors inside an expression tree, where each
component may itself be an expression.

## Caveats

- **`opacity` is a plain `Float`.** Only data-driven paint properties take a `StyleValue`.
- **The first `step` stop has no threshold** - passing one silently shifts the ramp.
- **Filters run in Mapbox, not MapsGL.** Anything Mapbox's filter grammar accepts will work;
  operators without an `Expression` factory must be built as raw lists.
- **No playhead expression.** A filter cannot reference the timeline position in 1.6.1.

Cookbooks for alerts, earthquakes and other real layers: `references/data-driven.md`.
Paint properties by render type: `references/weather-styling.md`.
