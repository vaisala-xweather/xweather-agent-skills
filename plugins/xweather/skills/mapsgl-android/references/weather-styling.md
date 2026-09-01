# Weather layer styling - MapsGL Android

Verified against SDK paint types + `WeatherService` factories (1.6.x).
Docs recipes are secondary:
https://www.xweather.com/docs/mapsgl-android-sdk/getting-started/weather-data ,
https://www.xweather.com/docs/mapsgl-android-sdk/styling/weather-data

## Raster

```kotlin
val config = WeatherService.Satellite(controller.service) as WeatherLayerConfiguration<*, *>
val paint = config.layer.paint as RasterLayerPaint
paint.opacity = 0.8f
controller.addWeatherLayer(config)
```

## Sample (color scale)

```kotlin
val config = WeatherService.Temperatures(controller.service) as WeatherLayerConfiguration<*, *>
val paint = config.layer.paint as SampleLayerPaint
paint.opacity = 1.0f
paint.sample.colorScale = ColorScaleOptions(
    stops = listOf(
        ColorStop(-50.0, "#08306b"),
        ColorStop(0.0, "#deebf7"),
        ColorStop(25.0, "#fdbe85"),
        ColorStop(50.0, "#b10026"),
    ),
)
controller.addWeatherLayer(config)
```

## Particle

```kotlin
val config = WeatherService.WindParticles(controller.service) as WeatherLayerConfiguration<*, *>
val paint = config.layer.paint as ParticleLayerPaint
paint.opacity = 1.0f
paint.particle.density = ParticleDensity.NORMAL
paint.particle.speed = 1.0
paint.particle.trails = true
paint.particle.trailsFade = ParticleTrailLength.NORMAL  // Double const (.97)
paint.particle.size = Size(2)
controller.addWeatherLayer(config)
```

## Grid (wind direction arrows / barbs)

```kotlin
val config = WeatherService.WindDirectionArrows(controller.service) as WeatherLayerConfiguration<*, *>
val paint = config.layer.paint as GridLayerPaint
paint.opacity = 1.0f
paint.grid.spacing = 30.0
paint.icon.iconSize = IconSize(width = 40f, height = 20f)
paint.icon.allowOverlap = StyleValue.Constant(true)
paint.sample?.smoothing = 1f
controller.addWeatherLayer(config)
```

## Data-driven weather paint

For alerts `COLOR`, earthquakes `report.type`, etc., see `data-driven.md`.

## Related

- Descriptor/paint type map: `styles.md`
- Expressions: `expressions.md` / `data-driven.md`
