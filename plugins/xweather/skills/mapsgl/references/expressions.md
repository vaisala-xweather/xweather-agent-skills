# Style Expressions Reference

Expressions let a paint value or a layer's `filter` be computed from each feature's own data at
render time — instead of one fixed color/size for a whole layer, a single expression can pick a
different color per alert type, size a circle by magnitude, or hide features below a threshold, all
declaratively (no JS callback, so the config stays plain, serializable JSON).

Verified against `packages/webgl-maps/src/style/expression.ts`. Syntax mirrors Mapbox GL style
expressions: a JSON array `[operator, ...args]`, where `args` can be literals or nested expressions.

```javascript
['operator', arg0, arg1, ...]
```

Used for:
- `layer.filter` (must evaluate to a boolean)
- any paint property value (data-driven styling)

## Differences from Mapbox GL expressions
- Only `zoom` is supported for camera state (no `pitch`, `distance-from-center`, etc.)
- No dedicated color-manipulation operators (`rgb`, `to-rgba`, etc.) — build color strings directly
- Extra operators not in Mapbox: `regex`, `to-unit`, `time` (current animation clock, used for
  time-filtered layers like tropical cyclone tracks), `to-date`, `to-locale-string`
- `get` supports dotted property paths (`['get', 'alert.info.color']`)

## Feature & camera access
| Operator | Purpose |
|---|---|
| `get` | Read a property from feature properties (or an object expression). Supports dotted paths. |
| `has` | Check property existence |
| `properties` | Return the full properties object |
| `zoom` | Current map zoom level |
| `time` | Current animation-timeline position (used in filters, e.g. `['<=', ['get','timestamp'], ['time']]`) |
| `var` / `let` | Variable lookup / scoped variable binding |
| `literal` | Return a JSON value unevaluated |
| `coalesce` | First argument that is not `null`/`undefined` |

## Type conversion / checks
`to-number`, `to-string`, `to-locale-string`, `to-unit`, `to-boolean`, `typeof`, `number`, `string`, `boolean`, `object`

## Comparison & logic
`==`, `!=`, `<`, `<=`, `>`, `>=`, `!`, `all`, `any`, `case`, `match`

> Legacy note: in expressions written before SDK v1.9.0, the first operand of a comparison could
> be a bare property-name string instead of `['get', ...]`. New code should always use `['get', ...]`.

## Math
Arithmetic: `+`, `-`, `*`, `/`, `%`, `^`
Functions: `abs`, `ceil`, `floor`, `round`, `min`, `max`, `sqrt`, `ln`, `ln2`, `log2`, `log10`,
`sin`, `cos`, `tan`, `asin`, `acos`, `atan`
Constants: `e`, `pi`

## String / array
`concat`, `downcase`, `upcase`, `at`, `in`, `index-of`, `length`, `slice`, `regex`

## Interpolation
- `step` — piecewise-constant function over ascending stops
- `interpolate` — linear/exponential interpolation between stops

## Example: hard color breaks by property value
```javascript
paint: {
  fill: {
    color: [
      'step', ['get', 'mag'],
      '#2ca02c',        // default (mag < 3)
      3, '#ff7f0e',      // mag >= 3
      5, '#d62728'       // mag >= 5
    ]
  }
}
```

## Example: filter by feature property
```javascript
controller.addLayer('big-quakes', {
  type: 'circle',
  source: 'earthquakes',
  filter: ['all', ['>=', ['get', 'mag'], 4], ['==', ['get', 'status'], 'reviewed']],
  paint: { circle: { radius: 6 } }
});
```
