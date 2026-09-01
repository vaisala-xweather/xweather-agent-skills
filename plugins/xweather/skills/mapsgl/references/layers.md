# MapsGL weather layer catalog

285 built-in weather layers. The **code** is the string passed to
`controller.addWeatherLayer(code)` — and to `getWeatherLayer`, `hasWeatherLayer`,
`removeWeatherLayer`, and `setWeatherLayerVisibility`. It is **not** the resulting `WebGLLayer`'s
`id`; see `weather-layers.md` for that distinction, which is the most common source of
silently-failing style updates.

This is a snapshot, regenerated from the live catalog by `scripts/regenerate_references.py`
and refreshed weekly in CI. For **account-specific availability** — what a given
subscription can actually render — call `controller.weatherProvider.getLayerMetadata()` at
runtime instead; this file reflects the public catalog, not entitlements. If a code here is
rejected at runtime, that's a plan question, not a typo.

Each entry reads: *render type · animatable · cost multiplier · coverage · data range · update interval*.

The **render type** determines which `paint` namespace styles the layer — a `sample` layer
is styled through `paint.sample`, a `line` layer through `paint.stroke`, and so on. See
`styles.md` for the property tables per type.

**There are no separate forecast layers.** Raster Maps splits observed from forecast (`temperatures`
vs. `ftemperatures`); MapsGL does not. One layer spans both, and the **data range** below is what
tells you how far each reaches — move the timeline to render a forecast interval rather than adding
a different layer. Two exceptions: the `satellite` layers are past-only (`-7 days`), with no MapsGL
forecast equivalent at all; and the `road-weather-*` / `froad-weather-*` pair is a genuine split, but
between a +2 hour nowcast and a +24 hour forecast — both forecasts, so there `f` marks range, not
past-versus-future.

---

## Composite layers

These 14 codes have render type `none`, meaning they expand into **several** sub-layers.
`addWeatherLayer` and `getWeatherLayer` return an **array** of `WebGLLayer` for them, so
iterate before setting paint properties:

`boundaries` · `fires` · `fires-icons` · `hail-threats` · `lightning-all` · `lightning-all-icons` · `lightning-threats` · `places` · `roads` · `stormcells` · `tropical-cyclones` · `tropical-cyclones-archive` · `tropical-cyclones-archive-icons` · `tropical-cyclones-icons`

## Cost multipliers

A layer's multiplier weights its contribution to session/access billing. It has no effect on
rendering.

- **x10** (5):
  `lightning-all` · `lightning-all-icons` · `lightning-strikes` · `lightning-strikes-icons` · `lightning-strikes-pulse`
- **x5** (84):
  `air-quality-co` · `air-quality-health-index-categories` · `air-quality-index-cai-categories` · `air-quality-index-china-categories` · `air-quality-index-eaqi-categories` · `air-quality-index-india-categories` · `air-quality-index-uba-daqi-categories` · `air-quality-index-uk-daqi-categories` · `air-quality-no` · `air-quality-no2` · `air-quality-o3` · `air-quality-pm10` · `air-quality-pm2p5` · `air-quality-so2` · `froad-weather-risk-hydroplane-australia` · `froad-weather-risk-hydroplane-europe` · `froad-weather-risk-hydroplane-japan` · `froad-weather-risk-hydroplane-new-zealand` · `froad-weather-risk-hydroplane-us` · `froad-weather-risk-low-viz-fog-australia` · `froad-weather-risk-low-viz-fog-europe` · `froad-weather-risk-low-viz-fog-japan` · `froad-weather-risk-low-viz-fog-new-zealand` · `froad-weather-risk-low-viz-fog-us` · `froad-weather-risk-low-viz-snow-australia` · `froad-weather-risk-low-viz-snow-europe` · `froad-weather-risk-low-viz-snow-japan` · `froad-weather-risk-low-viz-snow-new-zealand` · `froad-weather-risk-low-viz-snow-us` · `froad-weather-risk-rollover-australia` · `froad-weather-risk-rollover-europe` · `froad-weather-risk-rollover-japan` · `froad-weather-risk-rollover-new-zealand` · `froad-weather-risk-rollover-us` · `froad-weather-surface-australia` · `froad-weather-surface-europe` · `froad-weather-surface-japan` · `froad-weather-surface-new-zealand` · `froad-weather-surface-us` · `froad-weather-temperature-australia` · `froad-weather-temperature-europe` · `froad-weather-temperature-freeze-australia` · `froad-weather-temperature-freeze-europe` · `froad-weather-temperature-freeze-japan` · `froad-weather-temperature-freeze-new-zealand` · `froad-weather-temperature-freeze-us` · `froad-weather-temperature-japan` · `froad-weather-temperature-new-zealand` · `froad-weather-temperature-us` · `road-weather-risk-hydroplane-australia` · `road-weather-risk-hydroplane-europe` · `road-weather-risk-hydroplane-japan` · `road-weather-risk-hydroplane-new-zealand` · `road-weather-risk-hydroplane-us` · `road-weather-risk-low-viz-fog-australia` · `road-weather-risk-low-viz-fog-europe` · `road-weather-risk-low-viz-fog-japan` · `road-weather-risk-low-viz-fog-new-zealand` · `road-weather-risk-low-viz-fog-us` · `road-weather-risk-low-viz-snow-australia` · `road-weather-risk-low-viz-snow-europe` · `road-weather-risk-low-viz-snow-japan` · `road-weather-risk-low-viz-snow-new-zealand` · `road-weather-risk-low-viz-snow-us` · `road-weather-risk-rollover-australia` · `road-weather-risk-rollover-europe` · `road-weather-risk-rollover-japan` · `road-weather-risk-rollover-new-zealand` · `road-weather-risk-rollover-us` · `road-weather-surface-australia` · `road-weather-surface-europe` · `road-weather-surface-japan` · `road-weather-surface-new-zealand` · `road-weather-surface-us` · `road-weather-temperature-australia` · `road-weather-temperature-europe` · `road-weather-temperature-freeze-australia` · `road-weather-temperature-freeze-europe` · `road-weather-temperature-freeze-japan` · `road-weather-temperature-freeze-new-zealand` · `road-weather-temperature-freeze-us` · `road-weather-temperature-japan` · `road-weather-temperature-new-zealand` · `road-weather-temperature-us`
- **x1** — the remaining 196 layers, i.e. anything not listed above.

Cost does not follow the layer name. `air-quality-o3` is x5 while `air-quality-o3-text` —
its label variant — is x1, and the per-region `road-weather-risk-*` layers are x5 while
`road-weather-summary-*` are x1. Check the entry rather than inferring from the prefix.

---

## Radar + Satellite

### `radar` — Radar

Depicts areas of precipitation, including intensity and precipitation type (rain, mix, snow).

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 5 min · Also: Popular, Forecasts*

### `satellite` — Satellite

Black and white infrared satellite imagery.

*raster · animatable · x1 · Coverage: Global · Range: -7 days · Updates: US: 15 min, Global: 3 hour*

### `satellite-geocolor` — Geocolor Satellite

Geocolor satellite imagery.

*raster · animatable · x1 · Coverage: Global · Range: -7 days · Updates: US, Japan, Australia: 10 min, Europe: 15 min*

### `satellite-infrared-color` — Infrared Color Satellite

Color infrared satellite imagery based on cloud top temperature.

*raster · animatable · x1 · Coverage: Global · Range: -7 days · Updates: US: 15 min, Global: 2 hour*

### `satellite-visible` — Visible Satellite

Visible satellite imagery.

*raster · animatable · x1 · Coverage: Global · Range: -7 days · Updates: 15 min*

### `satellite-water-vapor` — Water Vapor Satellite

Satellite imagery depicting the amount of water vapor in the atmosphere.

*raster · animatable · x1 · Coverage: Global · Range: -7 days · Updates: 15 min*

## Conditions

### `cloud-cover` — Cloud Cover

Cloud cover as a percentage.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `cloud-cover-text` — Cloud Cover (Text)

Cloud cover as a percentage as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `dew-points` — Dew Points

Dew point temperature.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `dew-points-text` — Dew Points (Text)

Dew point temperature as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `feels-like` — Feels Like Temperatures

Feels-like, or apparent, temperature. This is a combination of the heat index for temperatures at or above 80F (26.67C) or wind chill at temperatures at or below 40F (4.44C).

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `feels-like-text` — Feels Like Temperatures (Text)

Feels-like, or apparent, temperatures as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `heat-index` — Heat Index

Heat index, where temperatures are at or above 80F (26.67C)

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `heat-index-text` — Heat Index (Text)

Heat index as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `humidity` — Humidity

Relative humidity percentage.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `humidity-text` — Humidity (Text)

Relative humidity percentage as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `ice` — 1-Hour Ice

Accumulated ice amounts per hour.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `ice-accum` — Accumulated Ice

Accumulated ice amounts for a selected time range. This layer uses the "sum" data operation to calculate the total ice across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `ice-accum-text` — Accumulated Ice (Text)

Accumulated ice amounts for a selected time range as text values for global locations. This layer uses the "sum" data operation to calculate the total ice across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `ice-text` — 1-Hour Ice (Text)

1-hour ice amounts per hour as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `precip` — 1-Hour Precipitation

Accumulated precipitation amounts per hour.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `precip-accum` — Accumulated Precipitation

Accumulated precipitation amounts for a selected time range. This layer uses the "sum" data operation to calculate the total precipitation across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `precip-accum-text` — Accumulated Precipitation (Text)

Accumulated precipitation amounts for a selected time range as text values for global locations. This layer uses the "sum" data operation to calculate the total precipitation across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `precip-text` — 1-Hour Precipitation (Text)

1-hour precipitation amounts per hour as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `pressure-msl` — Surface Pressure

Mean sea level pressure (MSLP).

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `pressure-msl-contour` — Surface Pressure (Contour)

Mean sea level pressure (MSLP).

*contour · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `pressure-msl-text` — Surface Pressure (Text)

Mean sea level pressure (MSLP) as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `river-observations` — River Observations

River and lake observations about water level and flood stages.

*circle · static · x1 · Coverage: US · Range: -7 days · Updates: 1 hour*

### `sleet` — 1-Hour Sleet

Accumulated sleet amounts per hour.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `sleet-accum` — Accumulated Sleet

Accumulated sleet amounts for a selected time range. This layer uses the "sum" data operation to calculate the total sleet across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `sleet-accum-text` — Accumulated Sleet (Text)

Accumulated sleet amounts for a selected time range as text values for global locations. This layer uses the "sum" data operation to calculate the total sleet across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `sleet-text` — 1-Hour Sleet (Text)

1-hour sleet amounts per hour as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `snow` — 1-Hour Snowfall

Accumulated snowfall amounts per hour.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `snow-accum` — Accumulated Snowfall

Accumulated snowfall amounts for a selected time range. This layer uses the "sum" data operation to calculate the total snowfall across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `snow-accum-text` — Accumulated Snowfall (Text)

Accumulated snowfall amounts for a selected time range as text values for global locations. This layer uses the "sum" data operation to calculate the total snowfall across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `snow-depth` — Snow Depth

Snow depth on the ground.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `snow-depth-text` — Snow Depth (Text)

Snow depth on the ground as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `snow-text` — 1-Hour Snowfall (Text)

1-hour snowfall amounts per hour as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures` — Temperatures

Surface temperatures.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts, Popular*

### `temperatures-24hr-change` — 24-Hour Temperature Change

Change in degrees of temperature between the requested time and the same time 24-hours ago.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures-24hr-change-text` — 24-Hour Temperature Change (Text)

Change in degrees of temperature as text values between the requested time and the same time 24 hours ago.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures-contour` — Temperatures (Contour)

Surface temperatures as isolines.

*contour · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures-max` — Maximum Temperatures

Maximum temperatures for a selected time range. This layer uses the "max" data operation to calculate the maximum temperature across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures-max-text` — Maximum Temperatures (Text)

Maximum temperatures for a selected time range as text values for global locations. This layer uses the "max" data operation to calculate the maximum temperatures across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures-min` — Minimum Temperature

Minimum temperatures for a selected time range. This layer uses the "min" data operation to calculate the minimum temperature across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures-min-text` — Minimum Temperatures (Text)

Minimum temperatures for a selected time range as text values for global locations. This layer uses the "min" data operation to calculate the minimum temperatures across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `temperatures-text` — Temperatures (Text)

Surface temperatures as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `uvi` — Ultraviolet Index (UVI)

Ultraviolet index (UVI) at the requested time.

*sample · animatable · x1 · Coverage: Global · Range: -7 days · Updates: 1 hour*

### `uvi-text` — Ultraviolet Index (Text)

Ultraviolet index (UVI) at the requested time interval as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `visibility` — Visibility

Visibility as a distance.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `visibility-text` — Visibility (Text)

Surface visibility as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-barbs` — Wind Barbs

Surface wind speeds and direction depicted by wind barbs.

*grid · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-chill` — Wind Chill

Wind chill, where temperatures are at or below 40F (4.44C).

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-chill-text` — Wind Chill (Text)

Wind chill as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-dir` — Wind Direction

Surface wind direction depicted by a grid of arrows.

*grid · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-gusts` — Wind Gusts

Surface wind gusts.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-gusts-max` — Maximum Wind Gusts

Maximum wind gusts for a selected time range. This layer uses the "max" data operation to calculate the maximum wind gusts across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-gusts-max-text` — Maximum Wind Gusts (Text)

Maximum wind gusts for a selected time range as text values for global locations. This layer uses the "max" data operation to calculate the maximum wind gusts across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-gusts-text` — Wind Gusts (Text)

Surface wind gusts as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-particles` — Wind Particles

Surface wind speeds and direction depicted by particles moving in a vector flow field.

*particle · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts, Popular*

### `wind-particles-arrow` — Wind Particles (Arrow)

Surface wind speeds and direction depicted by arrow symbols moving in a vector flow field.

*particle · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-speeds` — Wind Speeds

Surface wind speeds.

*sample · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-speeds-contour` — Wind Speeds (Contour)

Surface wind speeds as isolines.

*contour · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-speeds-max` — Maximum Wind Speeds

Maximum wind speeds for a selected time range. This layer uses the "max" data operation to calculate the maximum wind speeds across the map timeline's full time range.

*sample · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-speeds-max-text` — Maximum Wind Speeds (Text)

Maximum wind speeds for a selected time range as text values for global locations. This layer uses the "max" data operation to calculate the maximum wind speeds across the map timeline's full time range.

*text · animatable · x1 · Coverage: Global · Range: -7 days to +15 days · Updates: 1 hour · Also: Forecasts*

### `wind-speeds-text` — Wind Speeds (Text)

Surface wind speeds as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -7 to +15 days · Updates: 1 hour · Also: Forecasts*

## Severe

### `alerts` — Alerts

All currently active US, Canadian and European alerts as issued by the National Weather Service (NWS), Environment Canada (EC), MeteoAlarm, Australian Bureau of Meteorology (AUSBOM), and the UK Met Office.

*fill · animatable · x1 · Coverage: US, Canada, Europe, Australia, Brazil, India, Mexico, South Africa, South Korea, Japan · Range: -7 days · Updates: 2 min · Also: Popular*

### `alerts-outline` — Alerts (Outline)

All currently active US, Canadian and European alerts as issued by the National Weather Service (NWS), Environment Canada (EC), MeteoAlarm, and the UK Met Office.

*line · animatable · x1 · Coverage: US, Canada, Europe, Australia, South Korea, South Africa, Brazil, India, Japan, Mexico · Range: -7 days · Updates: 2 min*

### `convective` — Convective Outlook

Provides information on potential severe weather, including thunderstorms, tornadoes, damaging high winds, and hail as issued by the Storm Prediciton Center (SPC).

*fill · static · x1 · Range: +8 days · Updates: Varies*

### `convective-outline` — Convective Outlook (Outline)

Provides information on potential severe weather, including thunderstorms, tornadoes, damaging high winds, and hail as issued by the Storm Prediciton Center (SPC).

*line · static · x1 · Range: +8 days · Updates: Varies*

### `hail-severe-probability` — Severe Hail Probability

Maximum probability for severe hail (1"+ diameter) in hourly intervals.

*sample · animatable · x1 · Coverage: US, Europe, Japan, Australia · Range: -7 days*

### `hail-severe-probability-max` — Max Severe Hail Probability

Maximum probability for severe hail (1"+ diameter) for a selected time range. This layer uses the "max" data operation to calculate the maximum value across the map timeline's full time range.

*sample · animatable · x1 · Coverage: US, Europe, Japan, Australia · Range: -7 days*

### `hail-size` — Hail Size

Maximum observed hail size in hourly intervals.

*sample · animatable · x1 · Coverage: US, Europe, Japan, Australia · Range: -7 days*

### `hail-size-max` — Max Hail Size

Maximum observed hail size for a selected time range. This layer uses the "max" data operation to calculate the maximum value across the map timeline's full time range.

*sample · animatable · x1 · Coverage: US, Europe, Japan, Australia · Range: -7 days*

### `hail-threats` — Hail Threats

Hail nowcast providing current and forecast hail threat areas.

*none · animatable · x1 · Coverage: US, Canada, Japan, Europe, Australia · Range: -7 days to +1 hour · Updates: 2 minutes*

### `hail-threats-points` — Hail Threats - Points

Hail nowcast points providing current and forecast hail threat areas.

*circle · animatable · x1 · Coverage: US, Europe, Japan, Australia, Canada · Range: -7 days to +1 hour · Updates: 2 minutes*

### `hail-threats-polygons` — Hail Threats - Polygons

Hail nowcast polygons providing current and forecast hail threat areas.

*fill · animatable · x1 · Coverage: Europe, Japan, Australia, Canada, US · Range: -7 days to +1 hour · Updates: 2 minutes*

### `hail-threats-tracks` — Hail Threats - Tracks

Hail nowcast tracks providing current and forecast hail threat areas.

*line · animatable · x1 · Coverage: US, Europe, Japan, Australia, Canada · Range: -7 days to +1 hour · Updates: 2 minutes*

### `lightning-all` — Lightning Strikes (All)

Aggregated cloud-to-ground and intracloud lightning flashes.

*none · animatable · x10 · Coverage: Global · Range: -7 days · Updates: 5 min · Also: Popular, Lightning*

### `lightning-all-icons` — Lightning Strikes (All, Icons)

Aggregated cloud-to-ground and intracloud lightning flashes (as icons).

*none · animatable · x10 · Coverage: Global · Range: -7 days · Updates: 5 min · Also: Lightning*

### `lightning-density` — Lightning Density

Number of lightning strikes (cloud-to-ground and intracloud) per hour.

*sample · static · x1 · Coverage: US, Europe, Japan, Australia · Also: Lightning*

### `lightning-density-accum` — Accumulated Lightning Density 

Accumulated number of lightning strikes (cloud-to-ground and intracloud) for a selected time range. This layer uses the "sum" data operation to calculate the total density across the map timeline's full time range.

*sample · static · x1 · Coverage: US, Europe, Japan, Australia · Also: Lightning*

### `lightning-density-cloud-to-ground` — Lightning Density - Cloud-to-Ground

Number of cloud-to-ground lightning strikes per hour.

*sample · static · x1 · Coverage: US, Europe, Japan, Australia · Also: Lightning*

### `lightning-density-cloud-to-ground-accum` — Accumulated Lightning Density - Cloud-to-Ground

Accumulated number of cloud-to-ground lightning strikes for a selected time range. This layer uses the "sum" data operation to calculate the total density across the map timeline's full time range.

*sample · static · x1 · Coverage: US, Europe, Japan, Australia · Also: Lightning*

### `lightning-density-intracloud` — Lightning Density - Intracloud

Number of intracloud lightning strikes per hour within a given region.

*sample · static · x1 · Coverage: US, Europe, Japan, Australia · Also: Lightning*

### `lightning-density-intracloud-accum` — Accumulated Lightning Density - Intracloud

Accumulated number of intracloud lightning strikes for a selected time range. This layer uses the "sum" data operation to calculate the total density across the map timeline's full time range.

*sample · static · x1 · Coverage: US, Europe, Japan, Australia · Also: Lightning*

### `lightning-flash` — Lightning (Flash)

Consolidated cloud-to-ground and cloud-to-cloud lightning strikes. Multiple lightning strikes within a 10km area and cloud-to-cloud pulses within a 20km area, within split seconds of each other, may be combined as an individual lightning flash.

*circle · animatable · x1 · Coverage: Global · Range: -7 days · Updates: 5 min · Also: Lightning*

### `lightning-strikes` — Lightning Strikes

Cloud-to-ground lightning strikes.

*circle · animatable · x10 · Coverage: Global · Range: -7 days · Updates: 5 min · Also: Lightning*

### `lightning-strikes-icons` — Lightning Strikes (Icons)

Cloud-to-ground lightning strikes as icons.

*symbol · animatable · x10 · Coverage: Global · Range: -7 days · Updates: 5 min · Also: Lightning*

### `lightning-strikes-pulse` — Lightning Strikes Pulse

Cloud-to-ground lightning strikes as pulsing effects.

*symbol · animatable · x10 · Coverage: Global · Range: -7 days · Updates: 5 min · Also: Lightning*

### `lightning-threats` — Lightning Threats

Lightning nowcasts providing global thunderstorm activity potential.

*none · animatable · x1 · Coverage: Global · Range: +1 hour · Updates: 2 minutes · Also: Lightning*

### `lightning-threats-points` — Lightning Threats - Points

Forecast points for thunderstorm activity potential.

*circle · animatable · x1 · Coverage: Global · Range: +1 hour · Updates: 2 minutes · Also: Lightning*

### `lightning-threats-polygons` — Lightning Threats - Polygons

Forecast polygons for thunderstorm activity potential.

*fill · animatable · x1 · Coverage: Global · Range: +1 hour · Updates: 2 minutes · Also: Lightning*

### `lightning-threats-tracks` — Lightning Threats - Tracks

Forecast tracks for thunderstorm activity potential.

*line · animatable · x1 · Coverage: Global · Range: +1 hour · Updates: 2 minutes · Also: Lightning*

### `stormcells` — Storm Cells

Radar-derived data that attempts to identify and track storm cell movement, along with reporting cell intensity and certain severe weather signatures within the cell, like rotation and hail.

*none · animatable · x1 · Coverage: US · Range: -7 days · Updates: 3 min*

### `stormcells-cones` — Storm Cell Forecast Cones

Forecast cone component of observed storm cells.

*fill · animatable · x1 · Coverage: US · Range: -7 days · Updates: 3 min*

### `stormcells-heat` — Storm Cells (Heatmap)

Radar-derived data that attempts to identify and track storm cell movement, along with reporting cell intensity and certain severe weather signatures within the cell, like rotation and hail.

*heatmap · animatable · x1 · Coverage: US · Range: -7 days · Updates: 3 min*

### `stormcells-positions` — Storm Cell Positions

Position component of observed storm cells.

*circle · animatable · x1 · Coverage: US · Range: -7 days · Updates: 3 min*

### `stormcells-tracks` — Storm Cell Tracks

Forecast track component of observed storm cells.

*line · animatable · x1 · Coverage: US · Range: -7 days · Updates: 3 min*

### `stormreports` — Storm Reports

Local storm reports (LSR) as transmitted by the National Weather Service (NWS).

*circle · animatable · x1 · Coverage: US · Range: -7 days · Updates: 15 min*

### `stormreports-heat` — Storm Reports  (Heatmap)

Local storm reports (LSR) as transmitted by the National Weather Service (NWS).

*heatmap · animatable · x1 · Coverage: US · Range: -7 days · Updates: 15 min*

## Tropical

### `tropical-cyclones` — Tropical Cyclones

Combined layer consisting of tropical cyclone tracks, lines, positions, names, and forecasts for active storms only.

*none · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-archive` — Tropical Cyclones Archive

Combined layer consisting of tropical cyclone tracks and lines for all active and past storms.

*none · static · x1 · Coverage: Global · Updates: 1-6 hours*

### `tropical-cyclones-archive-icons` — Tropical Cyclones Archive (Icons)

Combined layer consisting of tropical cyclone tracks (as icons) and lines for all active and past storms.

*none · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-forecast-error-cones` — Tropical Cyclones Forecast Error Cones

Tropical cyclone forecast error cones for active storms only.

*fill · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-forecast-lines` — Tropical Cyclones Forecast Lines

Tropical cyclone forecast track lines for active storms only.

*line · static · x1 · Coverage: Global · Updates: 1-6 hours*

### `tropical-cyclones-forecast-point-icons` — Tropical Cyclones Forecast Points (Icons)

Tropical cyclone forecast track points (as icons) for active storms only.

*symbol · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-forecast-points` — Tropical Cyclones Forecast Points

Tropical cyclone forecast track points for active storms only.

*circle · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-icons` — Tropical Cyclones (Icons)

Combined layer consisting of tropical cyclone tracks (as icons), lines, positions (as icons), names, and forecasts for active storms only.

*none · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-invests` — Tropical Cyclones Invests

Current tropical invests, which are areas of low pressure with the potential of further tropical development.

*circle · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-names` — Tropical Cyclones Names

Current names of active tropical cyclones.

*text · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-position-icons` — Tropical Cyclones Positions (Icons)

Current positions (as icons) of active tropical cyclones.

*symbol · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-positions` — Tropical Cyclones Positions

Current positions of active tropical cyclones.

*circle · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-track-lines` — Tropical Cyclones Track Lines

Tropical cyclone track lines for active storms only.

*line · static · x1 · Coverage: Global · Updates: 1-6 hours*

### `tropical-cyclones-track-lines-archive` — Tropical Cyclones Track Lines Archive

Tropical cyclone track lines for all active and past storms.

*line · static · x1 · Coverage: Global · Updates: 1-6 hours*

### `tropical-cyclones-track-point-icons` — Tropical Cyclones Track Points (Icons)

Tropical cyclone track points (as icons) for active storms only.

*symbol · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-track-point-icons-archive` — Tropical Cyclones Track Points Archive (Icons)

Tropical cyclone track points as icons for all active and past storms.

*symbol · static · x1 · Coverage: Global · Updates: 1-6 hour*

### `tropical-cyclones-track-points` — Tropical Cyclones Track Points

Tropical cyclone track points for active storms only.

*circle · static · x1 · Coverage: Global · Updates: 1-6 hours*

### `tropical-cyclones-track-points-archive` — Tropical Cyclones Track Points Archive

Tropical cyclone track points for all active and past storms.

*circle · static · x1 · Coverage: Global · Updates: 1-6 hour*

## Maritime

### `ocean-currents` — Ocean Currents

Ocean current speeds.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +7 days · Updates: 6 hour*

### `ocean-currents-particles` — Ocean Currents (Particles)

Ocean current speeds and direction depicted by particles moving in a vector flow field.

*particle · animatable · x1 · Coverage: Global · Range: -15 to +7 days · Updates: 6 hour*

### `sst` — Sea Surface Temperatures

Ocean temperature close to the surface.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +7 days · Updates: 6 hour*

### `storm-surge` — Storm Surge

Amount of abnormal rise of water over and above the predicted astronomical tides due to storm activity. (Not inland storm surge)

*sample · animatable · x1 · Coverage: Global · Range: -15 to +7 days · Updates: 6 hour*

### `swell-dir` — Swell Direction

Direction of movement of primary ocean swells.

*grid · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell-heights` — Swell Heights

Primary swell height, which is the difference between the elevations of a swell crest and a neighboring trough.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell-particles` — Swell Direction (Particles)

Direction of movement of primary ocean swells depicted by particles moving in a vector flow field. The speed of particles does not indicate the speed of swells.

*particle · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell-periods` — Swell Periods

Primary swell period, which is the time it takes for two successive swell crests to reach a fixed point. The greater the number of seconds between swells, the larger the resulting wave.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell2-dir` — Swell 2 Direction

Direction of movement of secondary ocean swells.

*grid · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell2-heights` — Swell 2 Heights

Secondary swell height, which is the difference between the elevations of a swell crest and a neighboring trough.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell2-particles` — Swell 2 Direction (Particles)

Direction of movement of secondary ocean swells depicted by particles moving in a vector flow field. The speed of particles does not indicate the speed of swells.

*particle · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell2-periods` — Swell 2 Periods

Secondary swell period, which is the time it takes for two successive swell crests to reach a fixed point. The greater the number of seconds between swells, the larger the resulting wave.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell3-dir` — Swell 3 Direction

Direction of movement of tertiary ocean swells.

*grid · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell3-heights` — Swell 3 Heights

Tertiary swell height, which is the difference between the elevations of a swell crest and a neighboring trough.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell3-particles` — Swell 3 Direction (Particles)

Direction of movement of tertiary ocean swells depicted by particles moving in a vector flow field. The speed of particles does not indicate the speed of swells.

*particle · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `swell3-periods` — Swell 3 Periods

Tertiary swell period, which is the time it takes for two successive swell crests to reach a fixed point. The greater the number of seconds between swells, the larger the resulting wave.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `tide-heights` — Tide Heights

Height of the tide relative to the chart (tidal) datum, which can be positive or negative. The tidal datum is the height of the water used as a zero reference.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +7 days · Updates: 6 hour*

### `wave-dir` — Wave Direction

Direction of movement of ocean waves.

*grid · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `wave-heights` — Wave Heights

Significant wave height, which is the difference between the elevations of a wave crest and a neighboring trough.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `wave-particles` — Wave Direction (Particles)

Direction of movement of ocean waves depicted by particles moving in a vector flow field. The speed of particles does not indicate the speed of waves.

*particle · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

### `wave-periods` — Wave Periods

Wave period, which is the time it takes for two successive wave crests to reach a fixed point. The greater the number of seconds between waves, the larger the resulting wave.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +15 days · Updates: 6 hour*

## Air Quality

### `air-quality-co` — Air Quality - CO

Measures the concentration of carbon monoxide (CO) in the air. Vehicles and other machinery that burn fossil fuels are the greatest sources of CO.

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-co-text` — Air Quality - CO (Text)

Concentration of carbon monoxide (CO) in the air as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-health-index-categories` — Air Quality Health Index

Vaisala Xweather Air Quality Health Index, presenting how air quality affects an individual's health.

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 12 hour*

### `air-quality-index` — Air Quality Index

Reflects the concentration of key air pollutants and how they related to health concerns.

*sample · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-cai-categories` — Air Quality Index - Korean Comprehensive Categories (CAI)

Korean Comprehensive Air-quality Index (CAI) categories and calculations

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-cai-text` — Air Quality Index - Korean Comprehensive Categories (Text)

Korean Comprehensive Air-quality Index (CAI) categories and calculations as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-categories` — Air Quality Index Categories

Reflects the concentration of key air pollutants and how they related to health concerns. AQI is depicted by the AirNow air quality categories as outlined at https://www.airnow.gov/aqi/aqi-basics/

*sample · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-china-categories` — Air Quality Index - Chinese Government Categories

Chinese Government AQI categories

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-china-text` — Air Quality Index - Chinese Government Categories (Text)

Chinese Government AQI calculations as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-eaqi-categories` — Air Quality Index - European Categories

European Air Quality Index categories and calculations

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-eaqi-text` — Air Quality Index - European Categories (Text)

European Air Quality Index calculations as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-india-categories` — Air Quality Index - India Categories

India AQI categories

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-india-text` — Air Quality Index - India Categories (Text)

India AQI calculations as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-text` — Air Quality Index (Text)

Air quality index as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-uba-daqi-categories` — Air Quality Index - German Categories

German Air Quality categories and calculations

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-uba-daqi-text` — Air Quality Index - German Categories (Text)

German Air Quality calculations as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-uk-daqi-categories` — Air Quality Index - UK Categories

UK AQI categories and calculations

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-index-uk-daqi-text` — Air Quality Index - UK Categories (Text)

UK AQI calculations as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-no` — Air Quality - NO

Measures the concentration of nitrogen monoxide (NO) in the air.

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-no-text` — Air Quality - NO (Text)

Concentration of nitrogen monoxide (NO) in the air as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-no2` — Air Quality - NO2

Measures the concentration of nitrogen dioxide (NO2) in the air. NO2 primarily gets in the air from the burning of fuel and forms from the emissions from vehicles, power plants and off-road equipment.

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-no2-text` — Air Quality - NO2 (Text)

Concentration of nitrogen dioxide (NO2) in the air as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-o3` — Air Quality - O3

Measures the concentration of ozone (O3) in the air.

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-o3-text` — Air Quality - O3 (Text)

Concentration of ozone (O3) in the air as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-pm10` — Air Quality - PM10

Measures the concentration of particulate matter in the air whose particles are generally 10 micrometers and smaller (PM10).

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-pm10-text` — Air Quality - PM10 (Text)

Concentration of particulate matter in the air as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-pm2p5` — Air Quality - PM2.5

Measures the concentration of particulate matter in the air whose particles are generally 2.5 micrometers and smaller (PM2.5).

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-pm2p5-text` — Air Quality - PM2.5 (Text)

Concentration of particulate matter in the air as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-so2` — Air Quality - SO2

Measures the concentration of sulfur dioxide (SO2) in the air. SO2 results from the burning of either sulfur or materials containing sulfur.

*sample · animatable · x5 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

### `air-quality-so2-text` — Air Quality - SO2 (Text)

Concentration of sulfur dioxide (SO2) as text values for global locations.

*text · animatable · x1 · Coverage: Global · Range: -15 to +4.5 days · Updates: 3 hour*

## Climate

### `drought-monitor` — Drought Monitor

Latest drought summary and severity as issued by the National Drought Mitigation Center.

*fill · static · x1 · Coverage: US · Updates: 1 week*

### `drought-monitor-outline` — Drought Monitor (Outline)

Latest drought summary and severity as issued by the National Drought Mitigation Center.

*line · static · x1 · Coverage: US · Updates: 1 week*

### `fires` — Wildfires

Active wildfire positions, names, and perimeters when available.

*none · animatable · x1 · Coverage: US, Canada · Range: -7 days · Updates: 1 day*

### `fires-icons` — Wildfires (Icons)

Active wildfire positions (icons), names, and perimeters when available.

*none · animatable · x1 · Range: -7 days · Updates: 1 day*

### `fires-obs` — Wildfires Positions

Positions of currently active wildfires.

*circle · animatable · x1 · Coverage: US, Canada · Range: -7 days · Updates: 1 day*

### `fires-obs-heat` — Wildfires (Heatmap)

Currently active wildfires.

*heatmap · animatable · x1 · Coverage: US, Canada · Updates: 1 day*

### `fires-obs-icons` — Wildfires Positions (Icons)

Positions (icons) of currently active wildfires.

*symbol · animatable · x1 · Coverage: US, Canada · Range: -7 days · Updates: 1 day*

### `fires-obs-names` — Wildfire Names

Names and acreage of currently active wildfires.

*text · animatable · x1 · Coverage: US, Canada · Range: -7 days · Updates: 1 day*

### `fires-outlook` — Fires Outlook

Fire weather outlooks and fire conditions as issued by the Storm Prediction Center (SPC).

*fill · static · x1 · Updates: 1 day*

### `fires-perimeter` — Wildfire Perimeters

Depicts the boundaries of active wildfires, outlining the affected area to help assess impact, track fire progression, and support emergency response efforts

*fill · static · x1 · Coverage: Continental US*

### `fires-vpd` — Vapor Pressure Deficit (VPD)

Indicates the difference between the amount of moisture in the air and its maximum holding capacity. Higher VPD indicates drier conditions, increasing vegetation flammability and wildfire risk.

*sample · animatable · x1 · Coverage: Global*

## Roads

### `froad-weather-risk-hydroplane-australia` — Road Weather Hydroplane Risk Forecast (Australia)

Extended forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: Australia · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-hydroplane-europe` — Road Weather Hydroplane Risk Forecast (Europe)

Extended forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: Europe · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-hydroplane-japan` — Road Weather Hydroplane Risk Forecast (Japan)

Extended forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: Japan · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-hydroplane-new-zealand` — Road Weather Hydroplane Risk Forecast (New Zealand)

Extended forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-hydroplane-us` — Road Weather Hydroplane Risk Forecast (US)

Extended forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: US · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-fog-australia` — Road Weather Low-Visibility Fog Risk Forecast (Australia)

Extended forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: Australia · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-fog-europe` — Road Weather Low-Visibility Fog Risk Forecast (Europe)

Extended forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: Europe · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-fog-japan` — Road Weather Low-Visibility Fog Risk Forecast (Japan)

Extended forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: Japan · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-fog-new-zealand` — Road Weather Low-Visibility Fog Risk Forecast (New Zealand)

Extended forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-fog-us` — Road Weather Low-Visibility Fog Risk Forecast (US)

Extended forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: US · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-snow-australia` — Road Weather Low-Visibility Snow Risk Forecast (Australia)

Extended forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: Australia · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-snow-europe` — Road Weather Low-Visibility Snow Risk Forecast (Europe)

Extended forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: Europe · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-snow-japan` — Road Weather Low-Visibility Snow Risk Forecast (Japan)

Extended forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: Japan · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-snow-new-zealand` — Road Weather Low-Visibility Snow Risk Forecast (New Zealand)

Extended forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-low-viz-snow-us` — Road Weather Low-Visibility Snow Risk Forecast (US)

Extended forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: US · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-rollover-australia` — Road Weather Rollover Risk Forecast (Australia)

Extended forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: Australia · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-rollover-europe` — Road Weather Rollover Risk Forecast (Europe)

Extended forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: Europe · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-rollover-japan` — Road Weather Rollover Risk Forecast (Japan)

Extended forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: Japan · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-rollover-new-zealand` — Road Weather Rollover Risk Forecast (New Zealand)

Extended forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hours*

### `froad-weather-risk-rollover-us` — Road Weather Rollover Risk Forecast (US)

Extended forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: US · Range: +24 hours · Updates: 6 hours*

### `froad-weather-summary-australia` — Road Weather Summary Forecast (Australia)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: Australia · Range: +24 hours · Updates: 6 hours*

### `froad-weather-summary-europe` — Road Weather Summary Forecast (Europe)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: Europe · Range: +24 hours · Updates: 6 hours*

### `froad-weather-summary-japan` — Road Weather Summary Forecast (Japan)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: Japan · Range: +24 hours · Updates: 6 hours*

### `froad-weather-summary-new-zealand` — Road Weather Summary Forecast (New Zealand)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hours*

### `froad-weather-summary-us` — Road Weather Summary Forecast (US)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: US · Range: +24 hours · Updates: 6 hours*

### `froad-weather-surface-australia` — Road Weather Surface Forecast (Australia)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: Australia · Range: +24 hours · Updates: 6 hour*

### `froad-weather-surface-europe` — Road Weather Surface Forecast (Europe)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: Europe · Range: +24 hours · Updates: 6 hour*

### `froad-weather-surface-japan` — Road Weather Surface Forecast (Japan)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: Japan · Range: +24 hours · Updates: 6 hour*

### `froad-weather-surface-new-zealand` — Road Weather Surface Forecast (New Zealand)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hour*

### `froad-weather-surface-us` — Road Weather Surface Forecast (US)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: US · Range: +24 hours · Updates: 6 hour*

### `froad-weather-temperature-australia` — Road Weather Temperature Forecast (Australia)

Extended forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: Australia · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-europe` — Road Weather Temperature Forecast (Europe)

Extended forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: Europe · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-freeze-australia` — Road Weather Freezing Temperature Forecast (Australia)

Extended forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: Australia · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-freeze-europe` — Road Weather Freezing Temperature Forecast (Europe)

Extended forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: Europe · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-freeze-japan` — Road Weather Freezing Temperature Forecast (Japan)

Extended forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: Japan · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-freeze-new-zealand` — Road Weather Freezing Temperature Forecast (New Zealand)

Extended forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-freeze-us` — Road Weather Freezing Temperature Forecast (US)

Extended forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: US · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-japan` — Road Weather Temperature Forecast (Japan)

Extended forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: Japan · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-new-zealand` — Road Weather Temperature Forecast (New Zealand)

Extended forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: New Zealand · Range: +24 hours · Updates: 6 hours*

### `froad-weather-temperature-us` — Road Weather Temperature Forecast (US)

Extended forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: US · Range: +24 hours · Updates: 6 hours*

### `road-weather-risk-hydroplane-australia` — Road Weather Hydroplane Risk Short-Term Forecast (Australia)

Nowcast and short-term forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: Australia · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-hydroplane-europe` — Road Weather Hydroplane Risk Short-Term Forecast (Europe)

Nowcast and short-term forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: Europe · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-hydroplane-japan` — Road Weather Hydroplane Risk Short-Term Forecast (Japan)

Nowcast and short-term forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: Japan · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-hydroplane-new-zealand` — Road Weather Hydroplane Risk Short-Term Forecast (New Zealand)

Nowcast and short-term forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-hydroplane-us` — Road Weather Hydroplane Risk Short-Term Forecast (US)

Nowcast and short-term forecast. Depicts the risk of a hydroplaning due to weather and road conditions.

*line · static · x5 · Coverage: US · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-fog-australia` — Road Weather Low-Visibility Fog Risk Short-Term Forecast (Australia)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: Australia · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-fog-europe` — Road Weather Low-Visibility Fog Risk Short-Term Forecast (Europe)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: Europe · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-fog-japan` — Road Weather Low-Visibility Fog Risk Short-Term Forecast (Japan)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: Japan · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-fog-new-zealand` — Road Weather Low-Visibility Fog Risk Short-Term Forecast (New Zealand)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-fog-us` — Road Weather Low-Visibility Fog Risk Short-Term Forecast (US)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to fog.

*line · static · x5 · Coverage: US · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-snow-australia` — Road Weather Low-Visibility Snow Risk Short-Term Forecast (Australia)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: Australia · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-snow-europe` — Road Weather Low-Visibility Snow Risk Short-Term Forecast (Europe)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: Europe · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-snow-japan` — Road Weather Low-Visibility Snow Risk Short-Term Forecast (Japan)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: Japan · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-snow-new-zealand` — Road Weather Low-Visibility Snow Risk Short-Term Forecast (New Zealand)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-low-viz-snow-us` — Road Weather Low-Visibility Snow Risk Short-Term Forecast (US)

Nowcast and short-term forecast. Depicts the risk of experiencing reduced visibility due to snow.

*line · static · x5 · Coverage: US · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-rollover-australia` — Road Weather Rollover Risk Short-Term Forecast (Australia)

Nowcast and short-term forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: Australia · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-rollover-europe` — Road Weather Rollover Risk Short-Term Forecast (Europe)

Nowcast and short-term forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: Europe · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-rollover-japan` — Road Weather Rollover Risk Short-Term Forecast (Japan)

Nowcast and short-term forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: Japan · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-rollover-new-zealand` — Road Weather Rollover Risk Short-Term Forecast (New Zealand)

Nowcast and short-term forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min*

### `road-weather-risk-rollover-us` — Road Weather Rollover Risk Short-Term Forecast (US)

Nowcast and short-term forecast. Depicts the risk of a rollover due to weather and road conditions.

*line · static · x5 · Coverage: US · Range: +2 hours · Updates: 15 min*

### `road-weather-summary-australia` — Road Weather Summary Short-Term Forecast (Australia)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: Australia · Range: +2 hours · Updates: 15 min*

### `road-weather-summary-europe` — Road Weather Summary Short-Term Forecast (Europe)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: Europe · Range: +2 hours · Updates: 15 min*

### `road-weather-summary-japan` — Road Weather Summary Short-Term Forecast (Japan)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: Japan · Range: +2 hours · Updates: 15 min*

### `road-weather-summary-new-zealand` — Road Weather Summary Short-Term Forecast (New Zealand)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min*

### `road-weather-summary-us` — Road Weather Summary Short-Term Forecast (US)

Depicts a summary of road conditions based on severity, where green indicates dry roads with no issues, yellow indicates the potential for hazardous road conditions (wet, slick), and red indicates a high risk of adverse road conditions.

*line · static · x1 · Coverage: US · Range: +2 hours · Updates: 15 min*

### `road-weather-surface-australia` — Road Weather Surface Short-Term Forecast (Australia)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: Australia · Range: +2 hours · Updates: 15 min · Also: Popular*

### `road-weather-surface-europe` — Road Weather Surface Short-Term Forecast (Europe)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: Europe · Range: +2 hours · Updates: 15 min · Also: Popular*

### `road-weather-surface-japan` — Road Weather Surface Short-Term Forecast (Japan)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: Japan · Range: +2 hours · Updates: 15 min · Also: Popular*

### `road-weather-surface-new-zealand` — Road Weather Surface Short-Term Forecast (New Zealand)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min · Also: Popular*

### `road-weather-surface-us` — Road Weather Surface Short-Term Forecast (US)

Depicts the condition of the road surface, such as dry, moist, wet slush, snow or ice.

*line · static · x5 · Coverage: US · Range: +2 hours · Updates: 15 min · Also: Popular*

### `road-weather-temperature-australia` — Road Weather Temperature Short-Term Forecast (Australia)

Nowcast and short-term forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: Australia · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-europe` — Road Weather Temperature Short-Term Forecast (Europe)

Nowcast and short-term forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: Europe · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-freeze-australia` — Road Weather Freezing Temperature Short-Term Forecast (Australia)

Nowcast and short-term forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: Australia · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-freeze-europe` — Road Weather Freezing Temperature Short-Term Forecast (Europe)

Nowcast and short-term forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: Europe · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-freeze-japan` — Road Weather Freezing Temperature Short-Term Forecast (Japan)

Nowcast and short-term forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: Japan · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-freeze-new-zealand` — Road Weather Freezing Temperature Short-Term Forecast (New Zealand)

Nowcast and short-term forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-freeze-us` — Road Weather Freezing Temperature Short-Term Forecast (US)

Nowcast and short-term forecast. Depicts areas where the road surface is near, at, or well-below freezing.

*line · static · x5 · Coverage: US · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-japan` — Road Weather Temperature Short-Term Forecast (Japan)

Nowcast and short-term forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: Japan · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-new-zealand` — Road Weather Temperature Short-Term Forecast (New Zealand)

Nowcast and short-term forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: New Zealand · Range: +2 hours · Updates: 15 min*

### `road-weather-temperature-us` — Road Weather Temperature Short-Term Forecast (US)

Nowcast and short-term forecast. Depicts the temperature of the road surface.

*line · static · x5 · Coverage: US · Range: +2 hours · Updates: 15 min*

## Admin

### `admin-2-boundaries` — Boundaries - Level 2

Administrative information for country borders.

*line · static · x1 · Coverage: Global*

### `admin-3-4-boundaries` — Boundaries - Level 3 & 4

Administrative information for geographical regions such as states and provinces.

*line · static · x1 · Coverage: Global*

### `admin-5-6-boundaries` — Boundaries - Level 5 & 6

Administrative information for regions, districts, and counties.

*line · static · x1 · Coverage: Global*

### `boundaries` — Boundaries

Administrative and natural boundaries.

*none · static · x1 · Coverage: Global*

### `place-city` — Place - Cities

City and town name labels.

*text · static · x1 · Coverage: Global*

### `place-country` — Place - Countries

Country name labels.

*text · static · x1 · Coverage: Global*

### `place-neighborhood` — Place - Neighborhoods

Neighborhood, village, and suburb name labels.

*text · static · x1 · Coverage: Global*

### `place-state` — Place - States

State and province name labels.

*text · static · x1 · Coverage: Global*

### `places` — Places

Combination of administrative place name labels.

*none · static · x1 · Coverage: Global*

### `power-generators` — Power Generators

Individual oil, solar, and wind power generators, such as wind turbines and solar grids.

*circle · static · x1 · Coverage: Global*

### `power-lines` — Power Lines

Major electric power transmission lines.

*line · static · x1 · Coverage: Global*

### `power-plants` — Power Plants

Electric power plant structures.

*fill · static · x1 · Coverage: Global*

### `road-motorway` — Road - Motorways

Restricted access major divided highways, normally with 2 or more running lanes (e.g. freeway, autobahn, etc).

*line · static · x1 · Coverage: Global*

### `road-primary` — Road - Primary

Most important roads in a country's system after motorways and trunks that often link cities and larger towns.

*line · static · x1 · Coverage: Global*

### `road-secondary-tertiary` — Road - Secondary & Tertiary

Lower-capacity highways and roads that often link towns and villages.

*line · static · x1 · Coverage: Global*

### `road-street` — Road - Streets

City and residential streets.

*line · static · x1 · Coverage: Global*

### `road-trunk` — Road - Trunks

Most important roads in a country's system that aren't motorways.

*line · static · x1 · Coverage: Global*

### `roads` — Roads

Combination of various road layers.

*none · static · x1 · Coverage: Global*

### `water` — Water

Natural bodies of water.

*fill · static · x1 · Coverage: Global*

### `waterway-lake-river-boundaries` — Boundaries - Rivers & Lakes

Natural boundaries along lakes and rivers.

*line · static · x1 · Coverage: Global*

### `waterway-ocean-boundaries` — Boundaries - Oceans

Natural boundaries along coastlines.

*line · static · x1 · Coverage: Global*

### `waterways-text` — Waterways (Text)

Waterway name labels.

*text · static · x1 · Coverage: Global*

## Other

### `earthquakes` — Earthquakes

Real-time global earthquake information.

*circle · static · x1 · Coverage: Global · Range: -7 days · Updates: 5 min*

### `earthquakes-heat` — Earthquakes (Heatmap)

Real-time global earthquake information.

*heatmap · static · x1 · Coverage: Global · Range: -7 days · Updates: 5 min*
