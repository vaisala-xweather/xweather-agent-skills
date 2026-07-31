# Raster Maps layer catalog

159 layers. The layer code is what goes in the `{layers}` path segment; combine up to 10 with commas.

`x1` / `x5` / `x10` is the layer multiplier — its weight when computing map units (see `map-units.md`).

**Modifiers** listed on a layer are appended to the code with a dash, one option per modifier group:
`alerts` + Category `severe` → `alerts-severe`; `temperatures` + Source `rtma` → `temperatures-rtma`.
Modifier groups are independent, so a layer with two groups can take one option from each —
`alerts-severe-warnings`. These are different from the *layer modifiers* (`:opacity`, `:blur()`,
`:blend()`) in `modifiers.md`, which attach with a colon.

Where a modifier below reads *(options not enumerated in the catalog)*, the group exists but the
catalog publishes no values — check that layer's doc page or test the request instead of guessing a
suffix.

Regenerate from the live catalog: `curl -s https://www.xweather.com/docs/api/maps/layers`

---

## Base Maps

### `blue-marble` — Blue Marble

Blue marble base layer.

*x1 · Coverage: global*

### `flat` — Flat

Flat base layer.

*x1 · Coverage: global*

### `flat-dk` — Flat Dark

Dark version of flat base layer.

*x1 · Coverage: global*

### `terrain` — Terrain

Terrain base layer.

*x1 · Coverage: global*

### `terrain-dk` — Terrain - Dark

Dark terrain base layer.

*x1 · Coverage: global*

## Radar + Satellite

### `fradar` — Forecast Radar

Forecast Radar based on models, either the GFS, NAM, or HRRR

*x1 · Coverage: global · Range: HRRR (+18 hours), NAM(+72 hours), GFS (+15 days) · Updates: HRRR: 1 hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `fsatellite` — Forecast Satellite

Forecast satellite based on models, either the GFS, NAM, or HRRR

*x1 · Coverage: global · Range: +15 days · Updates: 6 hours*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `radar` — Radar

Radar information for regions globally

*x1 · Coverage: US, Puerto Rico, Guam, Canada, Australia, Japa, South Korea, Germany, Ireland, United Kingdom, Switzerland, Northern France, Belgium, Netherlands, japan, uk · Range: -30 days · Updates: US: 2 min, Global: 6-10 min*

- Modifier **Region**: _(options not enumerated in the catalog — see the layer docs)_

### `radar-global` — Radar - Global (Derived)

Global radar combining actual radar with satellite derived radar where actual radar information is unavailable

*x1 · Coverage: global · Range: -30 days · Updates: 2 min*

### `satellite` — Satellite - Infrared (B/W)

Black and white infrared satellite imagery.

*x1 · Coverage: global · Range: -7 days · Updates: US: 15 min, Global: 3hrs*

### `satellite-geocolor` — Satellite - GeoColor

Geocolor Global Satellite

*x1 · Coverage: global · Range: -7 days · Updates: US/Japan/AUS: 10 min, EU: 15 min*

### `satellite-infrared-color` — Satellite - Infrared (Color)

Color infrared satellite imagery based on cloud top temperature.

*x1 · Coverage: global · Range: -7 days · Updates: Global: 2 hrs, US: 15 min*

- Modifier **Region**: `-US` US/North America Only

### `satellite-visible` — Satellite - Visible

Visible satellite imagery.

*x1 · Coverage: north-america, central-america, east-pacific, west-atlantic · Range: -7 days · Updates: 15 minutes*

### `satellite-water-vapor` — Satellite - Water Vapor

Satellite imagery depicting the amount of water vapor in the atmosphere.

*x1 · Coverage: north-america, central-america, east-pacific, west-atlantic · Range: -7 days · Updates: 15 minutes*

## Observations

### `dew-points-text` — Dew Points - Text

Numeric values of dew point temperature.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `feels-like` — Feels Like

Feels-like, or apparent, temperature.

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `feels-like-text` — Feels Like - Text

Numeric values of feels-like temperature.

*x1 · Coverage: conus · Range: -7 days · Updates: 30 minutes*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `heat-index` — Heat Index

Heat index, where temperatures are at or above 80F (26.67C).

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `heat-index-text` — Heat-index - Text

Numeric values of heat index temperature.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `humidity` — Humidity

Relative humidity percentage.

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `humidity-text` — Humidity - Text

Numeric value of relative humidity percentage.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `precip` — Precipitation

Accumulated precipitation amounts per interval.

*x1 · Coverage: conus, alaska, puerto-rico · Range: -7 days · Updates: Hourly, Daily (AHPS)*

- Modifier **Time Range**: `-1h` 1 Hour, `-1d` 1 Day, `-7d` 7 Day, `-14d` 14 Day, `-30d` 30 Day, `-60d` 60 Day, `-90d` 90 Day, `-180d` 180 Day, `-mtd` Month to Date, `-ytd` Year to Date, `-wytd` Water Yr to Date (Oct 1)

### `precip-depart` — Precip Departure

Departure from precipitation normals.

*x1 · Coverage: conus, alaska, puerto-rico · Range: -7 days · Updates: Daily*

- Modifier **Time Range**: `-1d` 1 Day, `-7d` 7 Day, `-14d` 14 Day, `-30d` 30 Day, `-60d` 60 Day, `-90d` 90 Day, `-180d` 180 Day, `-mtd` Month to Date, `-ytd` Year to Date, `-wytd` Water Yr to Date (Oct 1)

### `precip-depart-percent` — Percent Precip Depart

Departure from precipitation normals as a percentage. 

*x1 · Coverage: conus, puerto-rico, alaska · Range: 7 days · Updates: Daily*

- Modifier **Time Range**: `-1d` 1 Day, `-7d` 7 Day, `-14d` 14 Day, `-30d` 30 Day, `-60d` 60 Day, `-90d` 90 Day, `-180d` 180 Day, `-mtd` Month to Date, `-ytd` Year to Date, `-wytd` Water Yr to Date (Oct 1)

### `precip-normals` — Precip Normals

Precipitation normals for a given time range.

*x1 · Coverage: conus, alaska, puerto-rico · Range: -7 days · Updates: Daily*

- Modifier **Time Range**: `-1d` 1 Day, `-7d` 7 Day, `-14d` 14 Day, `-30d` 30 Day, `-60d` 60 Day, `-90d` 90 Day, `-180d` 180 Day, `-mtd` Month to Date, `-ytd` Year to Date, `-wytd` Water Yr to Date (Oct 1)

### `river-observations` — River Gauge Observations

River and Lake Gauge observations from the NOAA Advanced Hydrologic Prediction Service (AHPS)

*x1 · Coverage: us · Range: -7 days · Updates: Hourly*

- Modifier **Category**: `-flooding` Gauges Reporting Flooding, `-low-threshold` Gauges Reporting Low Water

### `snow-depth` — Estimated Snow Depth

.

*x1 · Coverage: global, north-america · Range: -7 days · Updates: day*

- Modifier **Coverage**: `-global` Global

### `sst` — Sea Surface Temperatures

Sea surface temperatures across the globe.

*x1 · Coverage: global · Range: -7 days · Updates: Daily*

### `surface-analysis` — Surface Analysis

Frontal and pressure analysis. 

*x1 · Coverage: north-america · Range: -7 days · Updates: 12 hours*

### `surface-analysis-fronts` — Surface Fronts

Surface analysis of fronts only.

*x1 · Coverage: north-america · Range: -7 days · Updates: 12 hours*

### `surface-analysis-pressure` — Surface Pressure

Surface analysis of pressure only.

*x1 · Coverage: north-america · Range: -7 days · Updates: 12 hours*

### `surface-analysis-pressure-text` — Surface Pressure - Text

Surface analysis of pressure with numeric pressure values.

*x1 · Coverage: north-america · Range: -7 days · Updates: 12 hours*

- Modifier **Map Theme**: `-dk` Dark

### `temperatures` — 2 meter Surface Temperatures

Surface temperatures.

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `temperatures-text` — Temperatures - Text

Numeric values of surface temperatures.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Unites**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `visibility` — Visibility

Visibility as a distance.

*x1 · Coverage: conus · Range: -7 days · Updates: 15 minutes*

### `wave-heights` — Wave Heights

Global wave heights.

*x1 · Coverage: global · Range: -7 days · Updates: hourly*

### `wind-chill` — Wind Chill

Wind chill, where temperatures are at or below 40F (4.44C).

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `wind-chill-text` — Wind Chill - Text

Numeric values of wind chill temperatures.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `wind-dir` — Wind Direction

Surface wind direction depicted by arrows.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Map Theme**: `-dk` Dark

### `wind-gusts` — 10 meter Surface Wind Gusts

Surface wind gusts.

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `wind-gusts-text` — Wind Gusts - Text

Numeric values of surface wind gusts.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `wind-speeds` — 10 meter Surface Winds

Surface wind speeds.

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `wind-speeds-text` — Wind Speeds - Text

Numeric values of surface wind speeds.

*x1 · Coverage: global · Range: -7 days · Updates: 30 minutes*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

## Forecasts

### `fdew-points` — Forecast Dew Points

Forecast dew point temperature.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

### `ffeels-like` — Forecast Feels Like

Forecast feels-like temperature.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

### `fheat-index` — Forecast Heat Index

Forecast heat index temperature. 

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

### `fhumidity` — Forecast Humidity

Forecast relative humidity percentage.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

### `fice-accum` — Forecast Ice Accum

Forecast ice accumulation.

*x1 · Coverage: us · Range: +15 days · Updates: 6 hours*

- Modifier **Model**: `-ndfd` National Digital Forecast Database (NDFD)

### `fjet-stream` — Forecast Jet Stream (250mb)

Forecast jet stream at 250 mb. 

*x1 · Coverage: global · Range: +15 days*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `fpressure-msl` — Forecast Pressure

Forecast mean sea level pressure.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

### `fpressure-msl-isobars` — Forecast Pressure - Isobars

Forecast mean sea level pressure depicted with isobars.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `fqpf-1h` — Forecast Precip (1 Hour Intervals)

Forecast accumulated precipitation amounts in hourly intervals.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `fqpf-6h` — Forecast Precip (6 Hour Intervals)

Forecast accumulated precipitation amounts in 6 hour intervals.

*x1 · Coverage: us · Range: +15 days · Updates: 6 hours*

- Modifier **Model**: `-ndfd` National Digital Forecast Database (NDFD)

### `fqpf-accum` — Forecast Precip Accum

Forecast accumulated precipitation amounts in a given interval.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

### `fqsf-1h` — Forecast Snow (1 Hour Intervals)

Forecast snow accumulations over a 1 hour interval. 

*x1 · Coverage: global · Range: +15 days · Updates: 6 hours*

- Modifier **Ratio**: `-kuchera` Kuchera, `-10to1` 10-to-1

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `fqsf-accum` — Forecast Snow Accum

.

*x1 · Coverage: global · Range: +15 days · Updates: 6 hours*

- Modifier **Ratio**: `-kuchera` Kuchera, `-10to1` 10-to-1

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `fsnow-depth` — Forecast Snow Depth

Forecast snow depth. 

*x1 · Coverage: global · Range: +15 days · Updates: 6 hours*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `fsurface-analysis` — Forecast Surface Analysis

.

*x1 · Coverage: north-america · Updates: 12 hours*

### `fsurface-analysis-fronts` — Forecast Surface Fronts

.

*x1 · Coverage: north-america · Updates: 12 hours*

### `fsurface-analysis-pressure` — Forecast Surface Pressure

.

*x1 · Coverage: north-america · Updates: 12 hours*

### `fsurface-analysis-pressure-text` — Forecast Surface Pressure - Text

.

*x1 · Coverage: north-america · Updates: 12 hours*

- Modifier **Map Theme**: `-dk` Dark

### `ftemperatures` — Forecast Temperatures

Forecast surface temperatures. 

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1 hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

### `ftemperatures-max` — Forecast High Temps

Forecast high temperatures.

*x1 · Coverage: us, puerto-rico, guam · Range: +15 days · Updates: Daily*

- Modifier **Model**: `-ndfd` National Digital Forecast Database (NDFD)

### `ftemperatures-max-text` — Forecast High Temps - Text

Numeric value showing forecast high temperatures. 

*x1 · Coverage: global · Range: +15 days · Updates: Daily*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `ftemperatures-min` — Forecast Low Temps

Forecast low temperatures. 

*x1 · Coverage: us, guam, puerto-rico · Range: +15 days · Updates: Daily*

- Modifier **Model**: `-ndfd` National Digital Forecast Database (NDFD)

### `ftemperatures-min-text` — Forecast Low Temps - Text

Numeric value of forecast low temperature. 

*x1 · Coverage: global · Range: +15 days · Updates: Daily*

- Modifier **Units**: `-metric` Metric

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `fvisibility` — Forecast Visibility

Forecast visibility as a distance.

*x1 · Coverage: conus · Range: +15 days · Updates: HRRR: 1hr, NAM: 6hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM)

### `fwind-chill` — Forecast Wind Chill

Forecast wind chill temperatures.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS)

### `fwind-speeds` — Forecast Winds

Forecast surface wind speeds.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

## Severe

### `alerts` — Alerts

All currently active US, Canadian and European alerts as issued by the National Weather Service (NWS), Environment Canada (EC), MeteoAlarm, Australian Bureau of Meteorology (AUSBOM), and the UK Met Office.

*x1 · Coverage: us, canada, europe, australia, japan, south-korea · Range: -30 days · Updates: 2-3 minutes*

- Modifier **Category**: `-severe` Severe Alerts, `-fire` Fire Alerts, `-flood` Flood Alerts, `-frost-freeze` Frost/Freeze Alerts, `-heat` Heat Alerts, `-wind` Wind Alerts, `-winter` Winter Alerts, `-surge` Storm Surge Alerts

- Modifier **Advisory Type**: `-watches` Watches Only, `-warnings` Warning Only

- Modifier **Style**: `-outlines` Alert Outlines

### `fires-obs-icons` — Fires - Icons

Current fires observed depicted via icon. 

*x1 · Coverage: us, canada · Range: -7 days · Updates: Daily*

### `fires-obs-points` — Fires - Points

Current fires observed.

*x1 · Coverage: us, canada · Range: -7 days · Updates: Daily*

### `stormcells` — Stormcells

Radar-derived data that attempts to identify and track storm cell movement, along with reporting cell intensity and certain severe weather signatures within the cell, like rotation and hail. This layer is a combination of `stormcells-positions`, `stormcells-tracks`, and `stormcells-cones`.

*x1 · Coverage: us · Range: -7 days · Updates: 3 minutes*

- Modifier **Category**: `-general` General, `-hail` Hail, `-major` Major, `-rotating` Rotating, `-tornado` Tornado

### `stormreports` — Storm Reports

24 hours of storm reports throughout the US.

*x1 · Coverage: us · Range: -7 days · Updates: 15 minutes*

- Modifier **Category**: `-avalanche` Avalanche, `-blizzard` Blizzard, `-fire` Fire, `-flood` Flood, `-fog` Fog, `-hail` Hail, `-ice` Ice, `-lightning` Lightning, `-rain` Rain, `-snow` Snow, `-tides` Tides, `-tornado` Tornado, `-wind` Wind

## Lightning

### `lightning-all` — Lightning All

Aggregated cloud-to-ground and intracloud lightning flashes in the last 5 or 15 (default) minutes.

*x10 · Coverage: global · Range: -7 days · Updates: 5 minutes*

- Modifier **Icon Size**: `-lg` Large

### `lightning-all-15m` — Lightning All - 15m

Aggregated cloud-to-ground and intracloud lightning flashes in the last 15 minutes.

*x10 · Coverage: global · Range: -7 days · Updates: 15 minutes*

- Modifier **Icon Size**: `-lg` Large

### `lightning-flash` — Lightning Flash

Aggregated cloud-to-ground and intracloud lightning flashes in the last 5 minutes.

*x1 · Coverage: global · Range: -7 days · Updates: 5 minutes*

### `lightning-flash-5m-icons` — Lightning Flash - Icons 5m

Aggregated cloud-to-ground and intracloud lightning flashes in the last 5 minutes.

*x1 · Coverage: global · Range: -7 days · Updates: 5 minutes*

- Modifier **Icon Size**: `-lg` Large

### `lightning-strike-density` — Lightning Strike Density

A heat map of the number of lightning strikes within an 8km resolution, as provided by NOAA

*x1 · Coverage: central-america, east-pacific, us · Range: -7 days · Updates: 15 minutes*

### `lightning-strikes` — Lightning Strikes

Cloud-to-ground lightning strikes in the last 5 or 15 (default) minutes.

*x10 · Coverage: global · Range: -7 days · Updates: 5 minutes*

- Modifier **Timeframe**: `-15m` 15 minutes, `-5m` 5 minutes

### `lightning-strikes-15m-icons` — Lightning Strikes - Icons 15m

Cloud-to-ground lightning strikes in the last 15 minutes.

*x10 · Coverage: global · Range: -7 days · Updates: 15 minutes*

- Modifier **Icon Size**: `-lg` Large

### `lightning-strikes-5m-icons` — Lightning Strikes - Icons 5m

Cloud-to-ground lightning strikes in the last 5 minutes.

*x10 · Coverage: global · Range: -7 days · Updates: 5 minutes*

- Modifier **Icon Size**: `-lg` Large

## Air Quality

### `air-quality-co` — Carbon Monoxide (CO)

Carbon Monoxide concentration.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-health-index-categories` — Air Quality Health Index

Vaisala Xweather Air Quality Health Index, presenting how air quality affects an individual's health.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index` — AQI

Air Quality Index.

*x1 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-cai-categories` — Korean Comprehensive Air-quality Index

Korean Comprehensive Air-quality Index (CAI) categories and calculations

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-caqi-categories` — Common Air Quality Index

Common Air Quality Index categories and calculations

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-categories` — AQI: Categories

Air Quality Index Categories.

*x1 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-china-categories` — Chinese Government Air Quality Index

Chinese Government AQI categories

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-eaqi-categories` — European Air Quality Index

European Air Quality Index categories and calculations

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-india-categories` — India Air Quality Index

India AQI categories

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-uba-daqi-categories` — German Air Quality Index

German Air Quality categories and calculations

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-index-uk-daqi-categories` — UK Air Quality Index

UK AQI categories and calculations

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-no` — Nitrogen Monoxide (NO)

Nitrogen Monoxide concentration.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-no2` — Nitrogen Dioxide (NO2)

Nitrogen Dioxide concentration.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-o3` — Ozone (O3)

Ozone concentration.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-pm10` — Particle Pollution (PM10)

Particulate Matter < 10um concentration.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-pm2p5` — Particle Pollution (PM2.5)

Particulate Matter < 2.5um concentration.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

### `air-quality-so2` — Sulfer Dioxide (SO2)

Sulfer Dioxide concentration.

*x5 · Coverage: global · Range: -7 days  to +4.5 days · Updates: 12 hours*

## Maritime

### `maritime-currents` — Ocean Currents

Ocean Currents

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-sst` — Sea Surface Temperature

Sea Surface Temperatures

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-surges` — Storm Surge Height

Amount of abnormal rise of water over and above the predicted astronomical tides due to storm activity. (Not inland storm surge)

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-swell-2-heights` — Secondary Swell Heights

Secondary Swell Heights

*x1 · Coverage: global · Range: -7 days · Updates: 8 hours*

### `maritime-swell-2-periods` — Secondary Swell Periods

Secondary Swell Periods

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-swell-3-heights` — Tertiary Swell Heights

Tertiary Swell Heights

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-swell-3-periods` — Tertiary Swell Periods

Tertiary Swell Periods

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-swell-heights` — Primary Swell Heights

Primary Swell Heights

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-swell-periods` — Primary Swell Periods

Primary Swell Periods

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-tides` — Tide Height

Tide Height

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-wave-heights` — Primary Wave Heights

Primary Wave Heights

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-wave-periods` — Primary Wave Periods

Primary Wave Periods

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

### `maritime-wind-wave-heights` — Primary Wind Wave Heights

Primary Wind Wave Heights

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*

## Tropical

### `tropical-cyclones` — Tropical Cyclones

Active tropical cyclones with up to a 5 day forecast.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-break-points` — Tropical Cyclones - Breakpoints

Coastal areas under cyclone watches or warnings.

*x1 · Coverage: east-pacific, west-atlantic · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-forecast-error-cones` — Tropical Cyclones - Forecast Error Cones

Probable track of the center of a tropical cyclone

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-forecast-lines` — Tropical Cyclones - Forecast Lines

Probable track of the center of a tropical cyclone, displayed as lines.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-forecast-point-icons` — Tropical Cyclones - Forecast Icons

Probable track of the center of a tropical cyclone, displayed as icons.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-forecast-points` — Tropical Cyclones - Forecast Points

Probable track of the center of a tropical cyclone, displayed as points.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-invests` — Tropical Invests

Displays active Tropical Invests (Tropical disturbances under investigation for further development).

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-invests-names` — Tropical Invests - Names

The names of the active tropical invests.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

- Modifier **Font Size**: `-lg` Large

### `tropical-cyclones-invests-position-icons` — Tropical Invests - Icons

The current position of tropical invests as an icon (L).

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-invests-positions` — Tropical Invests - Positions

The current position of tropical invests (as a dot).

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-names` — Tropical Cyclones - Names

Active tropical cyclones with up to a 5 day forecast, displayed with cyclone names.

*x1 · Coverage: global · Range: -7 Days · Updates: 1-6 hours*

- Modifier **Font Size**: `-lg` Large

### `tropical-cyclones-position-icons` — Tropical Cyclones - Position Icons

Current positions of active tropical cyclones depicted with an icon of storm intensity. 

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-positions` — Tropical Cyclones - Positions

Current positions of active tropical cyclones.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-track-lines` — Tropical Cyclones - Track Lines

Tropical cyclone track lines for active storms only.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-track-point-icons` — Tropical Cyclones - Track Icons

Active tropical cyclone tracks, displayed as icons.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

### `tropical-cyclones-track-points` — Tropical Cyclones - Track Points

Active tropical cyclone tracks, displayed as points.

*x1 · Coverage: global · Range: -7 days · Updates: 1-6 hours*

## Outlooks

### `convective` — Convective Outlook

SPC Convective Outlook throughout the US.

*x1 · Coverage: conus · Updates: As needed*

- Modifier **Category**: `-hail` Hail, `-torn` Tornado, `-wind` Wind

### `drought-monitor` — Drought Monitor

Latest drought summary and severity as issued by the National Drought Mitigation Center.

*x1 · Coverage: us · Updates: Weekly*

### `fires-dryltg-outlook` — Fires Outlook (Dry Lightning)

Fire Weather Outlook for dry lightning

*x1 · Coverage: conus · Updates: Daily*

### `fires-outlook` — Fires Outlook

Fire weather outlooks and fire conditions as issued by the Storm Prediction Center (SPC).

*x1 · Coverage: conus · Updates: Daily*

### `precip-outlook-6-10d-cpc` — 6-10d Precip Outlook

The CPC 6 to 10 day Precipitation outlook

*x1 · Coverage: us · Updates: Daily*

### `precip-outlook-8-14d-cpc` — 8-14d Precip Outlook

The CPC 8 to 14 day Precipitation outlook

*x1 · Coverage: us · Updates: Daily*

### `temperatures-outlook-6-10d-cpc` — 6-10d Temp Outlook

The CPC 6 to 10 day Temperature outlook

*x1 · Coverage: us · Updates: Daily*

### `temperatures-outlook-8-14d-cpc` — 8-14d Temp Outlook

The CPC 8 to 14 day Temperature outlook

*x1 · Coverage: us · Updates: Daily*

## Overlays

### `admin` — Admin

Administration boundaries and labels, including country, states major cities

*x1 · Coverage: global*

- Modifier **Font Size**: `-lg` Large

### `admin-cities` — Admin - City Names

Standard admin layers with emphasis on city names versus state / country names.

*x1 · Coverage: global*

- Modifier **Font Size**: `-lg` Large

### `admin-cities-dk` — Admin - City Names - Dark

Standard admin layers with emphasis on city names versus state / country names.

*x1 · Coverage: global*

- Modifier **Font Size**: `-lg` Large

### `admin-dk` — Admin - Dark

Administration boundaries and labels, including country, states major cities

*x1 · Coverage: global*

- Modifier **Font Size**: `-lg` Large

### `counties` — County Lines

County / Parish outlines within the US.

*x1 · Coverage: us*

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `countries-outlines` — Country Outlines

Country outlines across the globe.

*x1 · Coverage: global*

- Modifier **Map Theme**: `-dk` Dark

### `interstates` — Interstates

Major interstates / highways around the globe.

*x1 · Coverage: global*

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

### `rivers` — Rivers

Rivers across the globe.

*x1 · Coverage: global*

- Modifier **Map Theme**: `-dk` Dark

### `roads` — Roads

Major roads across the U.S.

*x1 · Coverage: us*

- Modifier **Map Theme**: `-dk` Dark

### `states` — States / Provinces

State / Province outlines and labels

*x1 · Coverage: global*

- Modifier **State Outlines**: `-outlines` No Text Labels

- Modifier **Map Theme**: `-dk` Dark

- Modifier **Font Size**: `-lg` Large

## Masks

### `clip-us-blue-marble` — Blue Marble - Clip US

Blue Marble base layer with transparent US

*x1 · Coverage: us*

### `clip-us-terrain` — Terrain - Clip US

Terrain base layer with transparent US

*x1 · Coverage: us*

- Modifier **Map Theme**: `-dk` Dark

### `land-blue-marble` — Blue Marble - Land Mask

Land mask using blue marble base layer.

*x1 · Coverage: global*

### `land-flat` — Flat - Land Mask

Flat base layer with transparent US.

*x1 · Coverage: global*

- Modifier **Map Theme**: `-dk` Dark

### `land-terrain` — Terrain - Land Mask

Terrain land mask. 

*x1 · Coverage: global*

- Modifier **Map Theme**: `-dk` Dark

### `land-us-flat` — Flat - Land Mask (US Only)

Flat base layer with transparent US only.

*x1 · Coverage: us*

### `water-depth` — Water Mask - Bathymetry

Bathymetry water mask. 

*x1 · Coverage: global*

- Modifier **Map Theme**: `-dk` Dark

### `water-flat` — Water Mask

Water mask. 

*x1 · Coverage: global*

- Modifier **Map Theme**: `-dk` Dark

## Uncategorized

### `clip-us-flat` — Flat - Clip US

Flat base layer with transparent US.

*x1 · Coverage: us*

- Modifier **Map Theme**: `-dk` Dark

### `dew-points` — Dew Points

Dew point temperature.

*x1 · Coverage: global · Range: -7 days · Updates: 1hr*

- Modifier **Source**: `-rtma` Real-Time Mesoscale Analysis (RTMA)

### `fwind-gusts` — Forecast Wind Gusts

Forecast surface wind gusts.

*x1 · Coverage: global · Range: +15 days · Updates: HRRR: 1hr, NAM/GFS: 6 hrs*

- Modifier **Model**: `-hrrr` High-Resolution Rapid Refresh (HRRR), `-nam` North American Mesoscale Forecast System (NAM), `-gfs` Global Forecast System (GFS), `-ndfd` National Digital Forecast Database (NDFD)

### `lightning-all-5m` — Lightning All - 5m

Aggregated cloud-to-ground and intracloud lightning flashes in the last 5 minutes.

*x10 · Coverage: global · Range: -7 days · Updates: 5 minutes*

- Modifier **Icon Size**: `-lg` Large

### `maritime-wind-wave-periods` — Primary Wind Wave Periods

Primary Wind Wave Periods

*x1 · Coverage: global · Range: -7 days · Updates: 6 hours*
