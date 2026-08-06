# Expressions & StyleValue - MapsGL Android (1.6.x)

## StyleValue

```kotlin
StyleValue.Constant(value)
StyleValue.Expression(Expression(...))
StyleValue.fromExpressionArray(listOf("get", "temperature"))
```

## Expression helpers

`com.xweather.mapsgl.style.Expression` - Mapbox-style trees.

```kotlin
Expression.get("temperature")
Expression.getPath("report.type")
Expression.literal(0)
Expression.rgb(255, 0, 0)
Expression.concat(listOf("#", Expression.get("COLOR")))
Expression.downcase(Expression.get("report.type"))
Expression.interpolate(/* ... */)
Expression.match(input, listOf(Expression.Step(...), ...), fallback)
Expression.lessThanOrEqual(Expression.get("value"), Expression.literal(10))
```

Also: arithmetic, comparisons, `interpolateExponential` / `interpolateCubicBezier`,
`geometryType`, `zoom`, etc. See SDK `Expression.kt`.

For cookbooks (alerts, earthquakes): **`data-driven.md`**.

## Filters on layer descriptors

Optional `filter: Expression?`. GLES stencil mask evaluation on **1.6.x** supports
a small subset (`==`, `!=`, `all`, `any`, `!`, `get`, `literal`). Do not assume
full Mapbox coverage or JS `map-time` playhead filters as a public Android scrub
API - use `controller.timeline` for animation.

## Colors

Prefer `androidx.compose.ui.graphics.Color` with paint APIs.
