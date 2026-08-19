# MapsGL Android SDK - weather layer catalog

209 built-in weather layers, generated from the MapsGL Android SDK source on the
`feature/maptime-filter` branch.

**28 of these are not in the latest release (1.6.1) yet** and are marked *(unreleased)* below. They
compile only against the development branch - on a released artifact from JitPack they do not
exist. Everything unmarked is in 1.6.1.

**In Kotlin a layer is a `LayerCode` enum constant, not a string.** `LayerCode.TEMPERATURES`, not
`"temperatures"`. The enum names are *not* mechanical transforms of the wire codes -
`air-quality-co` is `LayerCode.CARBON_MONOXIDE`, `wind-dir` is `LayerCode.WIND_DIR` but its factory
is `WindDirectionArrows` - so never convert a code from the web docs by hand. Look it up here, or
let the IDE complete it. Each entry lists the wire code in parentheses.

Two ways to add any of them:

```kotlin
controller.addWeatherLayer(LayerCode.TEMPERATURES)               // defaults

val config = WeatherService.Temperatures(controller.service)     // to override paint first
config.layer.paint.opacity = 0.5f
controller.addWeatherLayer(config)
```

The first form calls `LayerCode.getConfigurationForLayerCode(code, service)` internally, so the two
are equivalent apart from the chance to mutate the configuration before it is added.

For each layer's **description, animatability, coverage, data range, update interval and cost
multiplier**, see the shared MapsGL layer documentation at
https://www.xweather.com/docs/mapsgl/weather-layers - those are properties of the data, not of the
SDK, and are identical across SDKs.

Sections are grouped by layer descriptor, which determines the paint namespace available. See
`references/weather-styling.md` for what each paint type exposes.

---

## Composite layers

These 21 codes expand into **several** sub-layers. Their configuration is a
`CompositeWeatherLayerConfiguration`, which carries a list of sub-configurations rather than a
single `layer`, so **paint cannot be set on a composite through its own configuration**. To
restyle one, add the constituent layers individually instead - e.g. `LayerCode.STORMCELLS_TRACKS`
and `LayerCode.STORMCELLS_POSITIONS` rather than `LayerCode.STORMCELLS`.

`LayerCode.BOUNDARIES` · `LayerCode.FIRES` · `LayerCode.FIRES_ICONS` · `LayerCode.HAIL_SEVERE_PROBABILITY` · `LayerCode.HAIL_SIZE` · `LayerCode.HAIL_THREATS` · `LayerCode.LIGHTNING_ALL` · `LayerCode.LIGHTNING_ALL_ICONS` · `LayerCode.LIGHTNING_DENSITY` · `LayerCode.LIGHTNING_DENSITY_CLOUD_TO_GROUND` · `LayerCode.LIGHTNING_DENSITY_INTRACLOUD` · `LayerCode.LIGHTNING_THREATS` · `LayerCode.PLACES` · `LayerCode.ROADS` · `LayerCode.STORMCELLS` · `LayerCode.TROPICAL_CYCLONES` · `LayerCode.TROPICAL_CYCLONES_ARCHIVE` · `LayerCode.TROPICAL_CYCLONES_ARCHIVE_ICONS` · `LayerCode.TROPICAL_CYCLONES_ICONS` · `LayerCode.TROPICAL_CYCLONES_INVESTS` · `LayerCode.TROPICAL_CYCLONES_INVESTS_ICONS`

---

## `SampleLayerDescriptor` - render type `sample` (67)

Paint namespaces: `paint.opacity`, `paint.sample`

- `LayerCode.CARBON_MONOXIDE` (`air-quality-co`) -> `WeatherService.CarbonMonoxide`
- `LayerCode.AIR_QUALITY_HEALTH_INDEX_CATEGORIES` (`air-quality-health-index-categories`) -> `WeatherService.AirQualityHealthIndexCategories`
- `LayerCode.AIR_QUALITY_INDEX` (`air-quality-index`) -> `WeatherService.AirQualityIndex`
- `LayerCode.AIR_QUALITY_INDEX_CAI_CATEGORIES` (`air-quality-index-cai-categories`) -> `WeatherService.AirQualityIndexCaiCategories`
- `LayerCode.AIR_QUALITY_INDEX_CAQI_CATEGORIES` (`air-quality-index-caqi-categories`) -> `WeatherService.AirQualityIndexCaqiCategories`
- `LayerCode.AIR_QUALITY_INDEX_CATEGORIES` (`air-quality-index-categories`) -> `WeatherService.AirQualityIndexCategories`
- `LayerCode.AIR_QUALITY_INDEX_CHINA_CATEGORIES` (`air-quality-index-china-categories`) -> `WeatherService.AirQualityIndexChinaCategories`
- `LayerCode.AIR_QUALITY_INDEX_EAQI_CATEGORIES` (`air-quality-index-eaqi-categories`) -> `WeatherService.AirQualityIndexEaqiCategories`
- `LayerCode.AIR_QUALITY_INDEX_INDIA_CATEGORIES` (`air-quality-index-india-categories`) -> `WeatherService.AirQualityIndexIndiaCategories`
- `LayerCode.AIR_QUALITY_INDEX_UBA_DAQI_CATEGORIES` (`air-quality-index-uba-daqi-categories`) -> `WeatherService.AirQualityIndexUbaDaqiCategories`
- `LayerCode.AIR_QUALITY_INDEX_UK_DAQI_CATEGORIES` (`air-quality-index-uk-daqi-categories`) -> `WeatherService.AirQualityIndexUkDaqiCategories`
- `LayerCode.NITRIC_OXIDE` (`air-quality-no`) -> `WeatherService.NitricOxide`
- `LayerCode.NITROGEN_DIOXIDE` (`air-quality-no2`) -> `WeatherService.NitrogenDioxide`
- `LayerCode.OZONE` (`air-quality-o3`) -> `WeatherService.Ozone`
- `LayerCode.PARTICULATE_MATTER_10_MICRON` (`air-quality-pm10`) -> `WeatherService.ParticulateMatter10Micron`
- `LayerCode.PARTICULATE_MATTER_2P5_MICRON` (`air-quality-pm2p5`) -> `WeatherService.ParticulateMatter2p5Micron`
- `LayerCode.SULFUR_DIOXIDE` (`air-quality-so2`) -> `WeatherService.SulfurDioxide`
- `LayerCode.CLOUD_COVER` (`cloud-cover`) -> `WeatherService.CloudCover`
- `LayerCode.DEW_POINTS` (`dew-points`) -> `WeatherService.DewPoints`
- `LayerCode.FEELS_LIKE` (`feels-like`) -> `WeatherService.FeelsLike`
- `LayerCode.HAIL_SEVERE_PROBABILITY_AUSTRALIA` (`hail-severe-probability-australia`) -> `WeatherService.HailSevereProbabilityAustralia`
- `LayerCode.HAIL_SEVERE_PROBABILITY_EUROPE` (`hail-severe-probability-europe`) -> `WeatherService.HailSevereProbabilityEurope`
- `LayerCode.HAIL_SEVERE_PROBABILITY_JAPAN` (`hail-severe-probability-japan`) -> `WeatherService.HailSevereProbabilityJapan`
- `LayerCode.HAIL_SEVERE_PROBABILITY_UNITED_STATES` (`hail-severe-probability-us`) -> `WeatherService.HailSevereProbabilityUnitedStates`
- `LayerCode.HAIL_SIZE_AUSTRALIA` (`hail-size-australia`) -> `WeatherService.HailSizeAustralia`
- `LayerCode.HAIL_SIZE_EUROPE` (`hail-size-europe`) -> `WeatherService.HailSizeEurope`
- `LayerCode.HAIL_SIZE_JAPAN` (`hail-size-japan`) -> `WeatherService.HailSizeJapan`
- `LayerCode.HAIL_SIZE_UNITED_STATES` (`hail-size-us`) -> `WeatherService.HailSizeUnitedStates`
- `LayerCode.HEAT_INDEX` (`heat-index`) -> `WeatherService.HeatIndex`
- `LayerCode.HUMIDITY` (`humidity`) -> `WeatherService.Humidity`
- `LayerCode.LIGHTNING_DENSITY_AUSTRALIA` (`lightning-density-australia`) -> `WeatherService.LightningDensityAustralia`
- `LayerCode.LIGHTNING_DENSITY_CLOUD_TO_GROUND_AUSTRALIA` (`lightning-density-cloud-to-ground-australia`) -> `WeatherService.LightningDensityCloudToGroundAustralia`
- `LayerCode.LIGHTNING_DENSITY_CLOUD_TO_GROUND_EUROPE` (`lightning-density-cloud-to-ground-europe`) -> `WeatherService.LightningDensityCloudToGroundEurope`
- `LayerCode.LIGHTNING_DENSITY_CLOUD_TO_GROUND_JAPAN` (`lightning-density-cloud-to-ground-japan`) -> `WeatherService.LightningDensityCloudToGroundJapan`
- `LayerCode.LIGHTNING_DENSITY_CLOUD_TO_GROUND_UNITED_STATES` (`lightning-density-cloud-to-ground-us`) -> `WeatherService.LightningDensityCloudToGroundUnitedStates`
- `LayerCode.LIGHTNING_DENSITY_EUROPE` (`lightning-density-europe`) -> `WeatherService.LightningDensityEurope`
- `LayerCode.LIGHTNING_DENSITY_INTRACLOUD_AUSTRALIA` (`lightning-density-intracloud-australia`) -> `WeatherService.LightningDensityIntracloudAustralia`
- `LayerCode.LIGHTNING_DENSITY_INTRACLOUD_EUROPE` (`lightning-density-intracloud-europe`) -> `WeatherService.LightningDensityIntracloudEurope`
- `LayerCode.LIGHTNING_DENSITY_INTRACLOUD_JAPAN` (`lightning-density-intracloud-japan`) -> `WeatherService.LightningDensityIntracloudJapan`
- `LayerCode.LIGHTNING_DENSITY_INTRACLOUD_UNITED_STATES` (`lightning-density-intracloud-us`) -> `WeatherService.LightningDensityIntracloudUnitedStates`
- `LayerCode.LIGHTNING_DENSITY_JAPAN` (`lightning-density-japan`) -> `WeatherService.LightningDensityJapan`
- `LayerCode.LIGHTNING_DENSITY_UNITED_STATES` (`lightning-density-us`) -> `WeatherService.LightningDensityUnitedStates`
- `LayerCode.OCEAN_CURRENTS` (`ocean-currents`) -> `WeatherService.OceanCurrents`
- `LayerCode.PRECIPITATION` (`precip`) -> `WeatherService.Precipitation`
- `LayerCode.PRESSURE_MEAN_SEA_LEVEL` (`pressure-msl`) -> `WeatherService.PressureMeanSeaLevel`
- `LayerCode.RADAR` (`radar`) -> `WeatherService.Radar`
- `LayerCode.SNOW` (`snow`) -> `WeatherService.Snow`
- `LayerCode.SNOW_DEPTH` (`snow-depth`) -> `WeatherService.SnowDepth`
- `LayerCode.SEA_SURFACE_TEMPERATURES` (`sst`) -> `WeatherService.SeaSurfaceTemperatures`
- `LayerCode.STORM_SURGE` (`storm-surge`) -> `WeatherService.StormSurge`
- `LayerCode.SWELL_HEIGHTS` (`swell-heights`) -> `WeatherService.SwellHeights`
- `LayerCode.SWELL_PERIODS` (`swell-periods`) -> `WeatherService.SwellPeriods`
- `LayerCode.SWELL2_HEIGHTS` (`swell2-heights`) -> `WeatherService.Swell2Heights`
- `LayerCode.SWELL2_PERIODS` (`swell2-periods`) -> `WeatherService.Swell2Periods`
- `LayerCode.SWELL3_HEIGHTS` (`swell3-heights`) -> `WeatherService.Swell3Heights`
- `LayerCode.SWELL3_PERIODS` (`swell3-periods`) -> `WeatherService.Swell3Periods`
- `LayerCode.TEMPERATURES` (`temperatures`) -> `WeatherService.Temperatures`
- `LayerCode.TEMPERATURES_1_HOUR_CHANGE` (`temperatures-1hr-change`) -> `WeatherService.Temperatures1HourChange`
- `LayerCode.TEMPERATURES_24_HOUR_CHANGE` (`temperatures-24hr-change`) -> `WeatherService.Temperatures24HourChange`
- `LayerCode.TIDE_HEIGHTS` (`tide-heights`) -> `WeatherService.TideHeights`
- `LayerCode.ULTRAVIOLET_INDEX` (`uvi`) -> `WeatherService.UltravioletIndex`
- `LayerCode.VISIBILITY` (`visibility`) -> `WeatherService.Visibility`
- `LayerCode.WAVE_HEIGHTS` (`wave-heights`) -> `WeatherService.WaveHeights`
- `LayerCode.WAVE_PERIODS` (`wave-periods`) -> `WeatherService.WavePeriods`
- `LayerCode.WIND_CHILL` (`wind-chill`) -> `WeatherService.WindChill`
- `LayerCode.WIND_GUSTS` (`wind-gusts`) -> `WeatherService.WindGusts`
- `LayerCode.WIND_SPEEDS` (`wind-speeds`) -> `WeatherService.WindSpeeds`

## `RasterLayerDescriptor` - render type `raster` (5)

Paint namespaces: `paint.opacity`, `paint.raster`

- `LayerCode.SATELLITE` (`satellite`) -> `WeatherService.Satellite`
- `LayerCode.SATELLITE_GEOCOLOR` (`satellite-geocolor`) -> `WeatherService.SatelliteGeocolor`
- `LayerCode.SATELLITE_INFRARED_COLOR` (`satellite-infrared-color`) -> `WeatherService.SatelliteInfraredColor`
- `LayerCode.SATELLITE_VISIBLE` (`satellite-visible`) -> `WeatherService.SatelliteVisible`
- `LayerCode.SATELLITE_WATER_VAPOR` (`satellite-water-vapor`) -> `WeatherService.SatelliteWaterVapor`

## `ParticleLayerDescriptor` - render type `particles` (6)

Paint namespaces: `paint.opacity`, `paint.particle`

- `LayerCode.OCEAN_CURRENTS_PARTICLES` (`ocean-currents-particles`) -> `WeatherService.OceanCurrentsParticles`
- `LayerCode.SWELL_PARTICLES` (`swell-particles`) -> `WeatherService.SwellParticles`
- `LayerCode.SWELL2_PARTICLES` (`swell2-particles`) -> `WeatherService.Swell2Particles`
- `LayerCode.SWELL3_PARTICLES` (`swell3-particles`) -> `WeatherService.Swell3Particles`
- `LayerCode.WAVE_PARTICLES` (`wave-particles`) -> `WeatherService.WaveParticles`
- `LayerCode.WIND_PARTICLES` (`wind-particles`) -> `WeatherService.WindParticles`

## `GridLayerDescriptor` - render type `grid` (6)

Paint namespaces: `paint.opacity`, `paint.grid`

- `LayerCode.SWELL_DIR` (`swell-dir`) -> `WeatherService.SwellDirectionGrid`
  - Gridded arrows: primary swell direction ([MaritimeGriddedArrows]).
- `LayerCode.SWELL2_DIR` (`swell2-dir`) -> `WeatherService.Swell2DirectionGrid`
- `LayerCode.SWELL3_DIR` (`swell3-dir`) -> `WeatherService.Swell3DirectionGrid`
- `LayerCode.WAVE_DIR` (`wave-dir`) -> `WeatherService.WaveDirectionGrid`
  - Gridded arrows: maritime wave direction ([MaritimeGriddedArrows]).
- `LayerCode.WIND_BARBS` (`wind-barbs`) -> `WeatherService.WindBarbs`
- `LayerCode.WIND_DIR` (`wind-dir`) -> `WeatherService.WindDirectionArrows`

## `ContourLayerDescriptor` - render type `contour` (3)

Paint namespaces: `paint.opacity`, `paint.contour`

- `LayerCode.PRESSURE_MEAN_SEA_LEVEL_CONTOUR` (`pressure-msl-contour`) -> `WeatherService.PressureMeanSeaLevelContour`
- `LayerCode.TEMPERATURES_CONTOUR` (`temperatures-contour`) -> `WeatherService.TemperaturesContour`
- `LayerCode.WIND_SPEEDS_CONTOUR` (`wind-speeds-contour`) -> `WeatherService.WindSpeedsContour`

## `FillLayerDescriptor` - render type `fill` (11)

Paint namespaces: `paint.opacity`, `paint.fill`

- `LayerCode.ALERTS` (`alerts`) -> `WeatherService.Alerts`
- `LayerCode.CONVECTIVE` (`convective`) -> `WeatherService.Convective`
- `LayerCode.DROUGHT_MONITOR` (`drought-monitor`) -> `WeatherService.DroughtMonitor`
- `LayerCode.FIRES_OUTLOOK` (`fires-outlook`) -> `WeatherService.FiresOutlook`
- `LayerCode.FIRES_PERIMETER` (`fires-perimeter`) -> `WeatherService.FiresPerimeter`
- `LayerCode.HAIL_THREATS_POLYGONS` (`hail-threats-polygons`) -> `WeatherService.HailThreatsPolygons`
- `LayerCode.LAND` (`land`) -> `WeatherService.Land`
- `LayerCode.LIGHTNING_THREATS_POLYGONS` (`lightning-threats-polygons`) -> `WeatherService.LightningThreatsPolygons`
- `LayerCode.STORMCELLS_CONES` (`stormcells-cones`) -> `WeatherService.StormcellsCones`
- `LayerCode.TROPICAL_CYCLONES_FORECAST_ERROR_CONES` (`tropical-cyclones-forecast-error-cones`) -> `WeatherService.TropicalCyclonesForecastErrorCones`
- `LayerCode.WATER` (`water`) -> `WeatherService.Water`

## `LineLayerDescriptor` - render type `line` (23)

Paint namespaces: `paint.opacity`, `paint.line`

- `LayerCode.ADMIN_2_BOUNDARIES` (`admin-2-boundaries`) -> `WeatherService.Admin2Boundaries`
- `LayerCode.ADMIN_3_4_BOUNDARIES` (`admin-3-4-boundaries`) -> `WeatherService.Admin34Boundaries`
- `LayerCode.ADMIN_5_6_BOUNDARIES` (`admin-5-6-boundaries`) -> `WeatherService.Admin56Boundaries`
- `LayerCode.ALERTS_OUTLINE` (`alerts-outline`) -> `WeatherService.AlertsOutline`
- `LayerCode.CONVECTIVE_OUTLINE` (`convective-outline`) -> `WeatherService.ConvectiveOutline`
- `LayerCode.DROUGHT_MONITOR_OUTLINE` (`drought-monitor-outline`) -> `WeatherService.DroughtMonitorOutline`
- `LayerCode.HAIL_THREATS_TRACKS` (`hail-threats-tracks`) -> `WeatherService.HailThreatsTracks`
- `LayerCode.LIGHTNING_THREATS_TRACKS` (`lightning-threats-tracks`) -> `WeatherService.LightningThreatsTracks`
- `LayerCode.ROAD_ALL` (`road-all`) -> `WeatherService.RoadAll`
- `LayerCode.ROAD_MOTORWAY` (`road-motorway`) -> `WeatherService.RoadMotorway`
- `LayerCode.ROAD_PRIMARY` (`road-primary`) -> `WeatherService.RoadPrimary`
- `LayerCode.ROAD_SECONDARY_TERTIARY` (`road-secondary-tertiary`) -> `WeatherService.RoadSecondaryTertiary`
- `LayerCode.ROAD_STREET` (`road-street`) -> `WeatherService.RoadStreet`
- `LayerCode.ROAD_TRUNK` (`road-trunk`) -> `WeatherService.RoadTrunk`
- `LayerCode.STORMCELLS_TRACKS` (`stormcells-tracks`) -> `WeatherService.StormcellsTracks`
- `LayerCode.TROPICAL_CYCLONES_BREAK_POINTS` (`tropical-cyclones-break-points`) -> `WeatherService.TropicalCyclonesBreakPoints`
- `LayerCode.TROPICAL_CYCLONES_FORECAST_LINES` (`tropical-cyclones-forecast-lines`) -> `WeatherService.TropicalCyclonesForecastLines`
- `LayerCode.TROPICAL_CYCLONES_FORECAST_LINES_INVESTS` (`tropical-cyclones-forecast-lines-invests`) -> `WeatherService.TropicalCyclonesForecastLinesInvests`
- `LayerCode.TROPICAL_CYCLONES_TRACK_LINES` (`tropical-cyclones-track-lines`) -> `WeatherService.TropicalCyclonesTrackLines`
- `LayerCode.TROPICAL_CYCLONES_TRACK_LINES_ARCHIVE` (`tropical-cyclones-track-lines-archive`) -> `WeatherService.TropicalCyclonesTrackLinesArchive`
- `LayerCode.TROPICAL_CYCLONES_TRACK_LINES_INVESTS` (`tropical-cyclones-track-lines-invests`) -> `WeatherService.TropicalCyclonesTrackLinesInvests`
- `LayerCode.WATERWAY_LAKE_RIVER_BOUNDARIES` (`waterway-lake-river-boundaries`) -> `WeatherService.WaterwayLakeRiverBoundaries`
- `LayerCode.WATERWAY_OCEAN_BOUNDARIES` (`waterway-ocean-boundaries`) -> `WeatherService.WaterwayOceanBoundaries`

## `CircleLayerDescriptor` - render type `circle` (17)

Paint namespaces: `paint.opacity`, `paint.circle`

- `LayerCode.AIR_QUALITY` (`air-quality`) -> `WeatherService.AirQuality`
- `LayerCode.EARTHQUAKES` (`earthquakes`) -> `WeatherService.Earthquakes`
- `LayerCode.FIRES_OBS` (`fires-obs`) -> `WeatherService.FiresObs`
- `LayerCode.HAIL_THREATS_POINTS` (`hail-threats-points`) -> `WeatherService.HailThreatsPoints`
- `LayerCode.LIGHTNING_FLASH` (`lightning-flash`) -> `WeatherService.LightningFlash`
- `LayerCode.LIGHTNING_STRIKES` (`lightning-strikes`) -> `WeatherService.LightningStrikes`
- `LayerCode.LIGHTNING_THREATS_POINTS` (`lightning-threats-points`) -> `WeatherService.LightningThreatsPoints`
- `LayerCode.RIVER_OBSERVATIONS` (`river-observations`) -> `WeatherService.RiverObservations`
- `LayerCode.STORMCELLS_POSITIONS` (`stormcells-positions`) -> `WeatherService.StormcellsPositions`
- `LayerCode.STORMREPORTS` (`stormreports`) -> `WeatherService.Stormreports`
- `LayerCode.TROPICAL_CYCLONES_FORECAST_POINTS` (`tropical-cyclones-forecast-points`) -> `WeatherService.TropicalCyclonesForecastPoints`
- `LayerCode.TROPICAL_CYCLONES_FORECAST_POINTS_INVESTS` (`tropical-cyclones-forecast-points-invests`) -> `WeatherService.TropicalCyclonesForecastPointsInvests`
- `LayerCode.TROPICAL_CYCLONES_POSITIONS` (`tropical-cyclones-positions`) -> `WeatherService.TropicalCyclonesPositions`
- `LayerCode.TROPICAL_CYCLONES_POSITIONS_INVESTS` (`tropical-cyclones-positions-invests`) -> `WeatherService.TropicalCyclonesPositionsInvests`
- `LayerCode.TROPICAL_CYCLONES_TRACK_POINTS` (`tropical-cyclones-track-points`) -> `WeatherService.TropicalCyclonesTrackPoints`
- `LayerCode.TROPICAL_CYCLONES_TRACK_POINTS_ARCHIVE` (`tropical-cyclones-track-points-archive`) -> `WeatherService.TropicalCyclonesTrackPointsArchive`
- `LayerCode.TROPICAL_CYCLONES_TRACK_POINTS_INVESTS` (`tropical-cyclones-track-points-invests`) -> `WeatherService.TropicalCyclonesTrackPointsInvests`

## `SymbolLayerDescriptor` - render type `symbol` (17)

Paint namespaces: `paint.opacity`, `paint.icon`, `paint.text`

- `LayerCode.FIRES_OBS_ICONS` (`fires-obs-icons`) -> `WeatherService.FiresObsIcons`
- `LayerCode.FIRES_OBS_NAMES` (`fires-obs-names`) -> `WeatherService.FiresObsNames`
- `LayerCode.LIGHTNING_STRIKES_ICONS` (`lightning-strikes-icons`) -> `WeatherService.LightningStrikesIcons`
- `LayerCode.PLACE_CITY` (`place-city`) -> `WeatherService.PlaceCity`
- `LayerCode.PLACE_COUNTRY` (`place-country`) -> `WeatherService.PlaceCountry`
- `LayerCode.PLACE_NEIGHBORHOOD` (`place-neighborhood`) -> `WeatherService.PlaceNeighborhood`
- `LayerCode.PLACE_STATE` (`place-state`) -> `WeatherService.PlaceState`
- `LayerCode.TROPICAL_CYCLONES_FORECAST_POINT_ICONS` (`tropical-cyclones-forecast-point-icons`) -> `WeatherService.TropicalCyclonesForecastPointIcons`
- `LayerCode.TROPICAL_CYCLONES_FORECAST_POINT_ICONS_INVESTS` (`tropical-cyclones-forecast-point-icons-invests`) -> `WeatherService.TropicalCyclonesForecastPointIconsInvests`
- `LayerCode.TROPICAL_CYCLONES_NAMES` (`tropical-cyclones-names`) -> `WeatherService.TropicalCyclonesNames`
- `LayerCode.TROPICAL_CYCLONES_NAMES_ARCHIVE` (`tropical-cyclones-names-archive`) -> `WeatherService.TropicalCyclonesNamesArchive`
- `LayerCode.TROPICAL_CYCLONES_NAMES_INVESTS` (`tropical-cyclones-names-invests`) -> `WeatherService.TropicalCyclonesNamesInvests`
- `LayerCode.TROPICAL_CYCLONES_POSITION_ICONS` (`tropical-cyclones-position-icons`) -> `WeatherService.TropicalCyclonesPositionIcons`
- `LayerCode.TROPICAL_CYCLONES_POSITION_ICONS_INVESTS` (`tropical-cyclones-position-icons-invests`) -> `WeatherService.TropicalCyclonesPositionIconsInvests`
- `LayerCode.TROPICAL_CYCLONES_TRACK_POINT_ICONS` (`tropical-cyclones-track-point-icons`) -> `WeatherService.TropicalCyclonesTrackPointIcons`
- `LayerCode.TROPICAL_CYCLONES_TRACK_POINT_ICONS_ARCHIVE` (`tropical-cyclones-track-point-icons-archive`) -> `WeatherService.TropicalCyclonesTrackPointIconsArchive`
- `LayerCode.TROPICAL_CYCLONES_TRACK_POINT_ICONS_INVESTS` (`tropical-cyclones-track-point-icons-invests`) -> `WeatherService.TropicalCyclonesTrackPointIconsInvests`

## `HeatmapLayerDescriptor` - render type `heatmap` (5)

Paint namespaces: `paint.opacity`, `paint.heatmap`

- `LayerCode.EARTHQUAKES_HEAT` (`earthquakes-heat`) -> `WeatherService.EarthquakesHeat`
- `LayerCode.FIRES_OBS_HEAT` (`fires-obs-heat`) -> `WeatherService.FiresObsHeat`
- `LayerCode.LIGHTNING_STRIKES_HEAT` (`lightning-strikes-heat`) -> `WeatherService.LightningStrikesHeat`
- `LayerCode.STORMCELLS_HEAT` (`stormcells-heat`) -> `WeatherService.StormcellsHeat`
- `LayerCode.STORMREPORTS_HEAT` (`stormreports-heat`) -> `WeatherService.StormreportsHeat`

## `DataQueryLayerDescriptor` - render type `query` (28)

Paint namespaces: `paint.opacity`, `paint.text`

**These have no `WeatherService` factory.** They all share one configuration built by
`WeatherConfigurations.DataQueryText(service, code)`, which takes the code as a second
argument - so there is no `WeatherService.TemperaturesText(...)` and writing one will not
compile. Add them by `LayerCode`, or call `DataQueryText` directly if you need to override
paint:

```kotlin
controller.addWeatherLayer(LayerCode.TEMPERATURES_TEXT)

val config = WeatherConfigurations.DataQueryText(controller.service, LayerCode.TEMPERATURES_TEXT)
```

They render city labels sampled from their parent data layer, and are the `query` layer type.

- `LayerCode.AIR_QUALITY_CO_TEXT` (`air-quality-co-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City CO labels sampled from `LayerCode.CARBON_MONOXIDE` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_INDEX_CAI_TEXT` (`air-quality-index-cai-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City CAI AQI labels sampled from `LayerCode.AIR_QUALITY_INDEX_CAI_CATEGORIES` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_INDEX_CHINA_TEXT` (`air-quality-index-china-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City China AQI labels sampled from `LayerCode.AIR_QUALITY_INDEX_CHINA_CATEGORIES` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_INDEX_EAQI_TEXT` (`air-quality-index-eaqi-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City EAQI labels sampled from `LayerCode.AIR_QUALITY_INDEX_EAQI_CATEGORIES` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_INDEX_INDIA_TEXT` (`air-quality-index-india-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City India AQI labels sampled from `LayerCode.AIR_QUALITY_INDEX_INDIA_CATEGORIES` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_INDEX_TEXT` (`air-quality-index-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City AQI labels sampled from `LayerCode.AIR_QUALITY_INDEX` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_INDEX_UBA_DAQI_TEXT` (`air-quality-index-uba-daqi-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City UBA DAQI labels sampled from `LayerCode.AIR_QUALITY_INDEX_UBA_DAQI_CATEGORIES` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_INDEX_UK_DAQI_TEXT` (`air-quality-index-uk-daqi-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City UK DAQI labels sampled from `LayerCode.AIR_QUALITY_INDEX_UK_DAQI_CATEGORIES` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_NO_TEXT` (`air-quality-no-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City NO labels sampled from `LayerCode.NITRIC_OXIDE` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_NO2_TEXT` (`air-quality-no2-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City NO₂ labels sampled from `LayerCode.NITROGEN_DIOXIDE` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_O3_TEXT` (`air-quality-o3-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City O₃ labels sampled from `LayerCode.OZONE` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_PM10_TEXT` (`air-quality-pm10-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City PM10 labels sampled from `LayerCode.PARTICULATE_MATTER_10_MICRON` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_PM2P5_TEXT` (`air-quality-pm2p5-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City PM2.5 labels sampled from `LayerCode.PARTICULATE_MATTER_2P5_MICRON` (data-query / `query` layer type).
- `LayerCode.AIR_QUALITY_SO2_TEXT` (`air-quality-so2-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City SO₂ labels sampled from `LayerCode.SULFUR_DIOXIDE` (data-query / `query` layer type).
- `LayerCode.DEW_POINTS_TEXT` (`dew-points-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City dew-point labels sampled from `LayerCode.DEW_POINTS` (data-query / `query` layer type).
- `LayerCode.FEELS_LIKE_TEXT` (`feels-like-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City feels-like labels sampled from `LayerCode.FEELS_LIKE` (data-query / `query` layer type).
- `LayerCode.HEAT_INDEX_TEXT` (`heat-index-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City heat-index labels sampled from `LayerCode.HEAT_INDEX` (data-query / `query` layer type).
- `LayerCode.HUMIDITY_TEXT` (`humidity-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City humidity labels sampled from `LayerCode.HUMIDITY` (data-query / `query` layer type).
- `LayerCode.PRECIP_TEXT` (`precip-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City precipitation labels sampled from `LayerCode.PRECIPITATION` (data-query / `query` layer type).
- `LayerCode.PRESSURE_MSL_TEXT` (`pressure-msl-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City MSL pressure labels sampled from `LayerCode.PRESSURE_MEAN_SEA_LEVEL` (data-query / `query` layer type).
- `LayerCode.SNOW_TEXT` (`snow-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City snow labels sampled from `LayerCode.SNOW` (data-query / `query` layer type).
- `LayerCode.TEMPERATURES_24_HOUR_CHANGE_TEXT` (`temperatures-24hr-change-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City 24-hour temperature-change labels sampled from `LayerCode.TEMPERATURES_24_HOUR_CHANGE` (data-query / `query` layer type).
- `LayerCode.TEMPERATURES_TEXT` (`temperatures-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City temperature labels sampled from `LayerCode.TEMPERATURES` (data-query / `query` layer type).
- `LayerCode.UVI_TEXT` (`uvi-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City UV-index labels sampled from `LayerCode.ULTRAVIOLET_INDEX` (data-query / `query` layer type).
- `LayerCode.VISIBILITY_TEXT` (`visibility-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City visibility labels sampled from `LayerCode.VISIBILITY` (data-query / `query` layer type).
- `LayerCode.WIND_CHILL_TEXT` (`wind-chill-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City wind-chill labels sampled from `LayerCode.WIND_CHILL` (data-query / `query` layer type).
- `LayerCode.WIND_GUSTS_TEXT` (`wind-gusts-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City wind-gust labels sampled from `LayerCode.WIND_GUSTS` (data-query / `query` layer type).
- `LayerCode.WIND_SPEEDS_TEXT` (`wind-speeds-text`) -> `WeatherConfigurations.DataQueryText` *(unreleased)*
  - City wind-speed labels sampled from `LayerCode.WIND_SPEEDS` (data-query / `query` layer type).

---

Generated from the MapsGL Android SDK source, branch `feature/maptime-filter` at `f5a20414` (2026-08-19).
*(unreleased)* markers come from diffing against the published KDoc for 1.6.1 at
`cdn.aerisapi.com/sdk/android/mapsgl/docs/v1.6.1/`.

If a layer appears in the MapsGL JavaScript catalog but not here, it is not available on Android -
a real gap, not a naming problem. Check `LayerCode` in the IDE against the build you actually
depend on before assuming this list matches it.
