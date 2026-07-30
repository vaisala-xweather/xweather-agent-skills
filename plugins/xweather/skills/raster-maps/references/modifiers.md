# Layer modifiers

Modifiers attach to an individual layer code with a **colon**, affecting only that layer:

```
flat,radar:70:blur(2),admin
       └── radar at 70 % opacity with blur level 2
```

Chain as many as needed; **order between modifiers is arbitrary** — `radar:70:blur(2)` and
`radar:blur(2):70` are identical. The one exception is `blend`, which allows only one per layer.

Don't confuse these with the dash-joined *layer modifiers* in `layers.md` (`alerts-severe`,
`radar-us`, `temperatures-rtma`), which select a data variant rather than a visual treatment.

## Opacity — `:{0-100}`

The only modifier with no function-call syntax: a bare number after the colon.

0 is fully transparent, 100 fully opaque. Default 100.

```
flat,radar:75,admin-cities
terrain,alerts:80,radar:75,admin-cities
```

Per-layer opacity is what makes a multi-layer static map readable — dropping an alerts polygon layer
to 80 % lets terrain show through underneath.

## Blur — `:blur({amount})`

Integer; higher is blurrier, 0 is none. Softens hard colour transitions and the pixelation that
shows up when zooming past a layer's native resolution.

```
flat,radar:blur(2),admin-cities
terrain-dk,satellite:blur(4),radar:blur(1),admin-cities-dk
flat,radar:70:blur(2),admin-cities
```

## Gray — `:gray()`

Desaturates the layer. No arguments.

```
flat,temperatures:gray(),admin-cities-dk
```

The docs show both `temperatures:gray` and `temperatures:gray()` in different places; the
parenthesised form matches every other modifier and is the safer thing to emit.

## Invert — `:invert()`

Inverts the layer's colours. Useful when a layer designed for a light base map is being drawn over a
dark one, or vice versa.

```
flat,lightning-strikes:invert(),admin-cities
flat,lightning-strikes:invert():50,admin-cities
```

## Blend — `:blend({mode})`

Composites a layer onto everything beneath it. Blending happens between a **source** (the layer
carrying the modifier) and a **destination** (the accumulated image below it). With
`terrain,alerts,radar`:

- terrain: destination is blank, source is terrain
- alerts: destination is terrain, source is alerts
- radar: destination is `terrain,alerts`, source is radar

**Only one blend per layer** — `alerts:blend(grain-merge):blend(overlay)` is invalid and may error or
produce an unexpected result.

The common use is pulling terrain texture up through a flat weather layer:

```
terrain,temperatures:blend(overlay),admin-cities
terrain-dk,alerts:blend(grain-merge),admin-cities
temperatures,terrain:blend(grain-merge)      # reversed: terrain as the source
```

### Composite modes

Affect colour blending between layers.

| Mode | Effect |
|---|---|
| `overlay` | Source colours with the destination's light/dark structure. Good for terrain texture; works best over lighter destinations. |
| `multiply` | Multiplies source into destination. Darker result that highlights the source; best over lighter destinations. |
| `grain-merge` | Terrain texture through the source; works over both light and dark destinations. The most generally useful for weather-over-terrain. |
| `screen` | Multiplies the inverses — lighter result. Black is a no-op, white produces white. |
| `plus` | Adds source to destination, tinting toward the source. Best with darker sources. |
| `minus` | Subtracts source from destination, tinting away from the source. |
| `difference` | Per-channel subtraction of the darker from the lighter. White inverts, black is a no-op. |
| `exclusion` | Like `difference` but lower contrast. |
| `contrast` | Contrast adjustment. |
| `invert` | Inversion as a blend. |
| `grain-extract` | Inverse of `grain-merge`. |
| `darken` | Per channel, keeps whichever of source/destination is darker. |
| `lighten` | Per channel, keeps whichever is lighter. |
| `hue` | Destination's luminance and saturation, source's hue. |
| `saturation` | Destination's luminance and hue, source's saturation. Good for tinting monochrome imagery. |
| `color-dodge` | Brightens destination toward source by cutting contrast. Black is a no-op. |
| `color-burn` | Darkens destination toward source by raising contrast. White is a no-op. |
| `hard-light` | Multiply or screen depending on the source — like a harsh spotlight. |
| `soft-light` | The gentler version of `hard-light`. |

### Alpha modes

Porter–Duff compositing operators, used to build masks between layers rather than to mix colour:

`src` · `dst` · `src-over` · `dst-over` · `src-in` · `dst-in` · `src-out` · `dst-out` ·
`src-atop` · `dst-atop`

`src-in` against one of the `Masks` layers in `layers.md` is how you clip a weather layer to land,
water, or a country boundary.

## Scale HSLA — `:scale-hsla(h0,h1,s0,s1,l0,l1,a0,a1)`

Recolours a layer by rescaling hue, saturation, lightness, and alpha. Eight floats, each 0–1.

| Arg | Meaning |
|---|---|
| `h0` / `h1` | Primary / secondary hue to scale to |
| `s0` / `s1` | Primary / secondary saturation |
| `l0` / `l1` | Primary / secondary lightness |
| `a0` / `a1` | Primary / secondary alpha — almost always `0,1` |

Each channel is rescaled as `h = h0 + (hp × (h1 - h0))`, where `hp` is the source pixel's own value.
So:

- **Tint toward a colour:** set `h0`/`s0`/`l0` to that colour and `h1`/`s1`/`l1` to 0.
- **Convert entirely to a colour:** set both the primary and secondary of each channel to that
  colour's value.

### Converting a colour

Values must be normalised to 0–1 from standard HSL:

- Hue: `h / 360`
- Saturation: `s / 100`
- Lightness: `l / 100`

Red `#FF0000` is HSL(0, 100 %, 50 %) → hue `0`, saturation `1`, lightness `0.5`.
Blue is documented as HSL(250, 100 %, 50 %) → hue `0.69`, saturation `1`, lightness `0.5`.

### Worked recipes

All from the docs, verbatim. `lightning-strikes` renders in shades of grey by strike age, which is
what makes it the standard demo layer for recolouring.

**Tint toward a colour** — colour in the primary slots, `0` in the secondary:

```
lightning-strikes:scale-hsla(0,0,1,0,0.5,0,0,1)                 # red tint
lightning-strikes:scale-hsla(0.69,0,1,0,0.5,0,0,1)              # blue tint
lightning-strikes:invert():scale-hsla(0.69,0,1,0,0.5,0,0,1)     # invert first so strike centres take the tint
```

Tinting a grey layer leaves dark centres; `invert()` before `scale-hsla` pulls the centres toward the
target colour instead.

**Convert entirely to one colour** — same value in primary and secondary for each channel:

```
lightning-strikes:scale-hsla(0,0,1,1,0.5,0.5,0,1)               # solid red
```

**Pseudo-heatmap** from point data — recolour, invert, then blur heavily:

```
lightning-strikes:invert():scale-hsla(0.1,0.1,1,1,0.5,0.5,0,1):blur(5)
lightning-strikes:invert():scale-hsla(0.1,0.1,1,1,0.5,0.5,0,1):blur(10):70
```

**Drop shadow / glow** — draw the layer twice, once blackened and blurred underneath:

```
flat,admin-cities-dk,surface-analysis-fronts:scale-hsla(0,0,0,0,0,0,0,1):blur(10),surface-analysis
```

Note the cost: **a layer listed twice is billed twice.** The docs call this out explicitly for the
shadow recipe — it doubles the map units for that layer.

`scale-hsla` is available on all Maps subscriptions.
