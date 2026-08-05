# MapsGL Apple SDK — weather layer catalog

182 built-in weather layers, generated from the Apple SDK's published DocC symbol index.

**In Swift a layer is a `WeatherService.LayerCode` case, not a string.** `.temperatures`, not `"temperatures"`.
The case names are *not* mechanical transforms of the JS/Raster Maps layer codes — `air-quality-pm2p5`
is `.particulateMatter2p5Micron` and `air-quality-no2` is `.nitrogenDioxide` — so never convert a code
from the web docs by hand. Look it up here, or let the compiler complete it.

The Apple SDK also supports **fewer** layers than the MapsGL JavaScript SDK (182 vs. 283).
If a layer exists in the MapsGL JavaScript catalog and not here, it is not available on Apple platforms — that is a real gap, not a naming problem.

Each entry reads: **`.case`** → its configuration struct. The struct is what you instantiate to
override defaults:

```swift
var config = WeatherService.Temperatures(service: controller.service)
config.layer.paint.opacity = 0.5   // opacity is on the layer paint, not on `paint.sample`
try controller.addWeatherLayer(config: config)
```

Every configuration struct carries the same four members: `code`, `layer` (the descriptor — paint and
quality live here), `legend`, and `presentation` (the data-inspector formatter). Composite layers are
the exception; see below.

For each layer's **description, animatability, coverage, data range, update interval and cost multiplier**,
see the shared MapsGL layer documentation at https://www.xweather.com/docs/mapsgl/weather-layers — those
attributes are properties of the data, not of the SDK, and are identical across SDKs. For what the
authenticated account may actually render, ask at runtime:

```swift
controller.service.loadLayerMetadata { result in ... }   // -> [WeatherLayerMetadata]
```

Generated from the DocC index for SDK 1.6.1. Regenerate with `python3 scripts/regenerate_references.py`;
the version is resolved from the releases endpoint, so this list tracks the current release.

---

## Composite layers

These 21 cases expand into **several** sub-layers. Their configuration struct exposes
`let layers: [any WeatherLayerConfiguration]` instead of a single `layer` — and it is a `let`, so
**you cannot override paint on a composite through its own config struct**. To restyle one, add the
constituent layers individually instead (e.g. `.stormcellsTracks` and `.stormcellsPositions` rather
than `.stormcells`).

`.boundaries` · `.fires` · `.firesIcons` · `.hailSevereProbability` · `.hailSize` · `.hailThreats` · `.lightningAll` · `.lightningAllIcons` · `.lightningDensity` · `.lightningDensityCloudToGround` · `.lightningDensityIntracloud` · `.lightningThreats` · `.places` · `.roads` · `.stormcells` · `.tropicalCyclones` · `.tropicalCyclonesArchive` · `.tropicalCyclonesArchiveIcons` · `.tropicalCyclonesIcons` · `.tropicalCyclonesInvests` · `.tropicalCyclonesInvestsIcons`

---

## `SampleLayerDescriptor` — render type `sample` (68)

Paint namespaces: `paint.opacity`, `paint.sample`

- `.airQualityHealthIndexCategories` → `WeatherService.AirQualityHealthIndexCategories`
- `.airQualityIndex` → `WeatherService.AirQualityIndex`
- `.airQualityIndexCaiCategories` → `WeatherService.AirQualityIndexCaiCategories`
- `.airQualityIndexCaqiCategories` → `WeatherService.AirQualityIndexCaqiCategories`
- `.airQualityIndexCategories` → `WeatherService.AirQualityIndexCategories`
- `.airQualityIndexChinaCategories` → `WeatherService.AirQualityIndexChinaCategories`
- `.airQualityIndexEaqiCategories` → `WeatherService.AirQualityIndexEaqiCategories`
- `.airQualityIndexIndiaCategories` → `WeatherService.AirQualityIndexIndiaCategories`
- `.airQualityIndexUbaDaqiCategories` → `WeatherService.AirQualityIndexUbaDaqiCategories`
- `.airQualityIndexUkDaqiCategories` → `WeatherService.AirQualityIndexUkDaqiCategories`
- `.carbonMonoxide` → `WeatherService.CarbonMonoxide`
- `.cloudCover` → `WeatherService.CloudCover`
- `.dewPoints` → `WeatherService.DewPoints`
- `.feelsLike` → `WeatherService.FeelsLike`
- `.hailSevereProbabilityAustralia` → `WeatherService.HailSevereProbabilityAustralia`
- `.hailSevereProbabilityEurope` → `WeatherService.HailSevereProbabilityEurope`
- `.hailSevereProbabilityJapan` → `WeatherService.HailSevereProbabilityJapan`
- `.hailSevereProbabilityUnitedStates` → `WeatherService.HailSevereProbabilityUnitedStates`
- `.hailSizeAustralia` → `WeatherService.HailSizeAustralia`
- `.hailSizeEurope` → `WeatherService.HailSizeEurope`
- `.hailSizeJapan` → `WeatherService.HailSizeJapan`
- `.hailSizeUnitedStates` → `WeatherService.HailSizeUnitedStates`
- `.heatIndex` → `WeatherService.HeatIndex`
- `.humidity` → `WeatherService.Humidity`
- `.lightningDensityAustralia` → `WeatherService.LightningDensityAustralia`
- `.lightningDensityCloudToGroundAustralia` → `WeatherService.LightningDensityCloudToGroundAustralia`
- `.lightningDensityCloudToGroundEurope` → `WeatherService.LightningDensityCloudToGroundEurope`
- `.lightningDensityCloudToGroundJapan` → `WeatherService.LightningDensityCloudToGroundJapan`
- `.lightningDensityCloudToGroundUnitedStates` → `WeatherService.LightningDensityCloudToGroundUnitedStates`
- `.lightningDensityEurope` → `WeatherService.LightningDensityEurope`
- `.lightningDensityIntracloudAustralia` → `WeatherService.LightningDensityIntracloudAustralia`
- `.lightningDensityIntracloudEurope` → `WeatherService.LightningDensityIntracloudEurope`
- `.lightningDensityIntracloudJapan` → `WeatherService.LightningDensityIntracloudJapan`
- `.lightningDensityIntracloudUnitedStates` → `WeatherService.LightningDensityIntracloudUnitedStates`
- `.lightningDensityJapan` → `WeatherService.LightningDensityJapan`
- `.lightningDensityUnitedStates` → `WeatherService.LightningDensityUnitedStates`
- `.nitricOxide` → `WeatherService.NitricOxide`
- `.nitrogenDioxide` → `WeatherService.NitrogenDioxide`
- `.oceanCurrents` → `WeatherService.OceanCurrents`
- `.ozone` → `WeatherService.Ozone`
- `.particulateMatter10Micron` → `WeatherService.ParticulateMatter10Micron`
- `.particulateMatter2p5Micron` → `WeatherService.ParticulateMatter2p5Micron`
- `.precipitation` → `WeatherService.Precipitation`
- `.precipitationRate` → `WeatherService.PrecipitationRate`
- `.pressureMeanSeaLevel` → `WeatherService.PressureMeanSeaLevel`
- `.radar` → `WeatherService.Radar`
- `.seaSurfaceTemperatures` → `WeatherService.SeaSurfaceTemperatures`
- `.snow` → `WeatherService.Snow`
- `.snowDepth` → `WeatherService.SnowDepth`
- `.stormSurge` → `WeatherService.StormSurge`
- `.sulfurDioxide` → `WeatherService.SulfurDioxide`
- `.swell2Heights` → `WeatherService.Swell2Heights`
- `.swell2Periods` → `WeatherService.Swell2Periods`
- `.swell3Heights` → `WeatherService.Swell3Heights`
- `.swell3Periods` → `WeatherService.Swell3Periods`
- `.swellHeights` → `WeatherService.SwellHeights`
- `.swellPeriods` → `WeatherService.SwellPeriods`
- `.temperatures` → `WeatherService.Temperatures`
- `.temperatures1HourChange` → `WeatherService.Temperatures1HourChange`
- `.temperatures24HourChange` → `WeatherService.Temperatures24HourChange`
- `.tideHeights` → `WeatherService.TideHeights`
- `.ultravioletIndex` → `WeatherService.UltravioletIndex`
- `.visibility` → `WeatherService.Visibility`
- `.waveHeights` → `WeatherService.WaveHeights`
- `.wavePeriods` → `WeatherService.WavePeriods`
- `.windChill` → `WeatherService.WindChill`
- `.windGusts` → `WeatherService.WindGusts`
- `.windSpeeds` → `WeatherService.WindSpeeds`

## `RasterLayerDescriptor` — render type `raster` (5)

Paint namespaces: `paint.opacity`, `paint.raster`

- `.satellite` → `WeatherService.Satellite`
- `.satelliteGeocolor` → `WeatherService.SatelliteGeocolor`
- `.satelliteInfraredColor` → `WeatherService.SatelliteInfraredColor`
- `.satelliteVisible` → `WeatherService.SatelliteVisible`
- `.satelliteWaterVapor` → `WeatherService.SatelliteWaterVapor`

## `ParticleLayerDescriptor` — render type `particles` (6)

Paint namespaces: `paint.opacity`, `paint.sample`, `paint.particle`

- `.oceanCurrentsParticles` → `WeatherService.OceanCurrentsParticles`
- `.swell2Particles` → `WeatherService.Swell2Particles`
- `.swell3Particles` → `WeatherService.Swell3Particles`
- `.swellParticles` → `WeatherService.SwellParticles`
- `.waveParticles` → `WeatherService.WaveParticles`
- `.windParticles` → `WeatherService.WindParticles`

## `GridLayerDescriptor` — render type `grid` (6)

Paint namespaces: `paint.opacity`, `paint.sample`, `paint.grid`, `paint.fill`, `paint.stroke`, `paint.icon`, `paint.symbol`

- `.swell2Direction` → `WeatherService.Swell2Direction`
- `.swell3Direction` → `WeatherService.Swell3Direction`
- `.swellDirection` → `WeatherService.SwellDirection`
- `.waveDirection` → `WeatherService.WaveDirection`
- `.windBarbs` → `WeatherService.WindBarbs`
- `.windDirection` → `WeatherService.WindDirection`

## `ContourLayerDescriptor` — render type `contour` (3)

Paint namespaces: `paint.opacity`, `paint.sample`, `paint.contour`

- `.pressureMeanSeaLevelContour` → `WeatherService.PressureMeanSeaLevelContour`
- `.temperaturesContour` → `WeatherService.TemperaturesContour`
- `.windSpeedsContour` → `WeatherService.WindSpeedsContour`

## `FillLayerDescriptor` — render type `fill` (11)

Paint namespaces: `paint.opacity`, `paint.fill`, `paint.stroke`

- `.alerts` → `WeatherService.Alerts`
- `.convective` → `WeatherService.Convective`
- `.droughtMonitor` → `WeatherService.DroughtMonitor`
- `.firesOutlook` → `WeatherService.FiresOutlook`
- `.firesPerimeter` → `WeatherService.FiresPerimeter`
- `.hailThreatsPolygons` → `WeatherService.HailThreatsPolygons`
- `.land` → `WeatherService.Land`
- `.lightningThreatsPolygons` → `WeatherService.LightningThreatsPolygons`
- `.stormcellsCones` → `WeatherService.StormcellsCones`
- `.tropicalCyclonesForecastErrorCones` → `WeatherService.TropicalCyclonesForecastErrorCones`
- `.water` → `WeatherService.Water`

## `LineLayerDescriptor` — render type `line` (23)

Paint namespaces: `paint.opacity`, `paint.stroke`

- `.admin2Boundaries` → `WeatherService.Admin2Boundaries`
- `.admin34Boundaries` → `WeatherService.Admin34Boundaries`
- `.admin56Boundaries` → `WeatherService.Admin56Boundaries`
- `.alertsOutline` → `WeatherService.AlertsOutline`
- `.convectiveOutline` → `WeatherService.ConvectiveOutline`
- `.droughtMonitorOutline` → `WeatherService.DroughtMonitorOutline`
- `.hailThreatsTracks` → `WeatherService.HailThreatsTracks`
- `.lightningThreatsTracks` → `WeatherService.LightningThreatsTracks`
- `.roadAll` → `WeatherService.RoadAll`
- `.roadMotorway` → `WeatherService.RoadMotorway`
- `.roadPrimary` → `WeatherService.RoadPrimary`
- `.roadSecondaryTertiary` → `WeatherService.RoadSecondaryTertiary`
- `.roadStreet` → `WeatherService.RoadStreet`
- `.roadTrunk` → `WeatherService.RoadTrunk`
- `.stormcellsTracks` → `WeatherService.StormcellsTracks`
- `.tropicalCyclonesBreakPoints` → `WeatherService.TropicalCyclonesBreakPoints`
- `.tropicalCyclonesForecastLines` → `WeatherService.TropicalCyclonesForecastLines`
- `.tropicalCyclonesForecastLinesInvests` → `WeatherService.TropicalCyclonesForecastLinesInvests`
- `.tropicalCyclonesTrackLines` → `WeatherService.TropicalCyclonesTrackLines`
- `.tropicalCyclonesTrackLinesArchive` → `WeatherService.TropicalCyclonesTrackLinesArchive`
- `.tropicalCyclonesTrackLinesInvests` → `WeatherService.TropicalCyclonesTrackLinesInvests`
- `.waterwayLakeRiverBoundaries` → `WeatherService.WaterwayLakeRiverBoundaries`
- `.waterwayOceanBoundaries` → `WeatherService.WaterwayOceanBoundaries`

## `CircleLayerDescriptor` — render type `circle` (17)

Paint namespaces: `paint.opacity`, `paint.fill`, `paint.stroke`, `paint.circle`

- `.airQuality` → `WeatherService.AirQuality`
- `.earthquakes` → `WeatherService.Earthquakes`
- `.firesObs` → `WeatherService.FiresObs`
- `.hailThreatsPoints` → `WeatherService.HailThreatsPoints`
- `.lightningFlash` → `WeatherService.LightningFlash`
- `.lightningStrikes` → `WeatherService.LightningStrikes`
- `.lightningThreatsPoints` → `WeatherService.LightningThreatsPoints`
- `.riverObservations` → `WeatherService.RiverObservations`
- `.stormcellsPositions` → `WeatherService.StormcellsPositions`
- `.stormreports` → `WeatherService.Stormreports`
- `.tropicalCyclonesForecastPoints` → `WeatherService.TropicalCyclonesForecastPoints`
- `.tropicalCyclonesForecastPointsInvests` → `WeatherService.TropicalCyclonesForecastPointsInvests`
- `.tropicalCyclonesPositions` → `WeatherService.TropicalCyclonesPositions`
- `.tropicalCyclonesPositionsInvests` → `WeatherService.TropicalCyclonesPositionsInvests`
- `.tropicalCyclonesTrackPoints` → `WeatherService.TropicalCyclonesTrackPoints`
- `.tropicalCyclonesTrackPointsArchive` → `WeatherService.TropicalCyclonesTrackPointsArchive`
- `.tropicalCyclonesTrackPointsInvests` → `WeatherService.TropicalCyclonesTrackPointsInvests`

## `SymbolLayerDescriptor` — render type `symbol` (17)

Paint namespaces: `paint.opacity`, `paint.fill`, `paint.stroke`, `paint.icon`, `paint.text`

- `.firesObsIcons` → `WeatherService.FiresObsIcons`
- `.firesObsNames` → `WeatherService.FiresObsNames`
- `.lightningStrikesIcons` → `WeatherService.LightningStrikesIcons`
- `.placeCity` → `WeatherService.PlaceCity`
- `.placeCountry` → `WeatherService.PlaceCountry`
- `.placeNeighborhood` → `WeatherService.PlaceNeighborhood`
- `.placeState` → `WeatherService.PlaceState`
- `.tropicalCyclonesForecastPointIcons` → `WeatherService.TropicalCyclonesForecastPointIcons`
- `.tropicalCyclonesForecastPointIconsInvests` → `WeatherService.TropicalCyclonesForecastPointIconsInvests`
- `.tropicalCyclonesNames` → `WeatherService.TropicalCyclonesNames`
- `.tropicalCyclonesNamesArchive` → `WeatherService.TropicalCyclonesNamesArchive`
- `.tropicalCyclonesNamesInvests` → `WeatherService.TropicalCyclonesNamesInvests`
- `.tropicalCyclonesPositionIcons` → `WeatherService.TropicalCyclonesPositionIcons`
- `.tropicalCyclonesPositionIconsInvests` → `WeatherService.TropicalCyclonesPositionIconsInvests`
- `.tropicalCyclonesTrackPointIcons` → `WeatherService.TropicalCyclonesTrackPointIcons`
- `.tropicalCyclonesTrackPointIconsArchive` → `WeatherService.TropicalCyclonesTrackPointIconsArchive`
- `.tropicalCyclonesTrackPointIconsInvests` → `WeatherService.TropicalCyclonesTrackPointIconsInvests`

## `HeatmapLayerDescriptor` — render type `heatmap` (5)

Paint namespaces: `paint.opacity`, `paint.heatmap`

- `.earthquakesHeat` → `WeatherService.EarthquakesHeat`
- `.firesObsHeat` → `WeatherService.FiresObsHeat`
- `.lightningStrikesHeat` → `WeatherService.LightningStrikesHeat`
- `.stormcellsHeat` → `WeatherService.StormcellsHeat`
- `.stormreportsHeat` → `WeatherService.StormreportsHeat`
