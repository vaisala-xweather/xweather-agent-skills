# Xweather Weather API — endpoint catalog

Every endpoint below is a path under `https://data.api.xweather.com`. Full request shape:
`https://data.api.xweather.com/{endpoint}/{action}/{:id}?{params}&client_id=…&client_secret=…`

`Cost` is the endpoint access multiplier. Multiply it by the number of time intervals a request
covers to get the accesses charged — `/conditions/summary` bills one access per day, so 30 days
is 30. The spatial multiplier in the cost header is always 1 today, so query area never affects
cost (see `access-cost.md`).

Filter tokens containing `#` are templates, not literals: `#hr` → `1hr`, `3hr`, `6hr`, `24hr`;
`#min` → `1min`, `5min`, `15min`; `day#` → `day1` … `day8`. A trailing `*` (only `pop*`, on
`/stormcells/summary`) marks a property usable with the `affects` action only.

Regenerate this list from the live catalog at any time:
`curl -s https://www.xweather.com/docs/api/weather-api/endpoints` (JSON: `{ endpoint: {...}, action: {...} }`).

---

## `/airquality`

Air Quality Index (AQI), Health Index (AQHI) and pollutant information globally.

*Coverage: global · Range: Latest · Updates: 1 hour · Cost: x5*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `filter`, `fields`, `format`, `plimit`, `pskip`, `psort`, `lang` |
| Filters | `airnow`, `cai`, `caqi`, `china`, `eaqi`, `germany`, `india`, `uk` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/airquality

## `/airquality/archive`

A historical dataset providing comprehensive air quality data around the globe.

*Coverage: global · Range: Jan 2024 to now · Updates: 1 hour · Cost: x5*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `fields`, `filter`, `from`, `to`, `plimit`, `pskip`, `lang` |
| Filters | `#hr`, `airnow`, `cai`, `caqi`, `china`, `eaqi`, `germany`, `india`, `uk` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/airquality-archive

## `/airquality/forecasts`

Future air quality around the globe including each individual pollutant.

*Coverage: global · Range: +5 days · Updates: 1 hour · Cost: x5*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `filter`, `fields`, `plimit`, `pskip`, `from`, `to`, `lang` |
| Filters | `day`, `daynight`, `#hr`, `airnow`, `cai`, `caqi`, `china`, `eaqi`, `germany`, `india`, `uk` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/airquality-forecasts

## `/airquality/index`

Air Quality Index for locations around the world

*Coverage: global · Range: Latest · Updates: Hourly · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p` |
| Filters | — |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/airquality-index

## `/alerts`

Mild to severe weather events issued to the public from the Canadian, European, and US governments.

*Coverage: us, canada, europe, australia · Range: Latest · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `limit`, `filter`, `query`, `sort`, `fields`, `lang`, `format` |
| Filters | `standard`, `warning`, `watch`, `advisory`, `outlook`, `statement`, `severe`, `flood`, `tropical`, `winter`, `marine`, `nonprecip`, `forecast`, `all`, `wind`, `fire`, `tsunami`, `now`, `synopsis`, `tornado`, `emergency`, `hassmallpoly`, `distinct`, `county`, `nonmarine`, `geo` |
| Query props | `type`, `loc`, `sig`, `sigp`, `name`, `active`, `emergency`, `id`, `issued`, `begins`, `expires`, `added` |
| Sort fields | `type`, `loc`, `sig`, `sigp`, `country`, `state`, `name`, `active`, `emergency`, `id`, `issued`, `begins`, `expires`, `added` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/alerts

## `/alerts/summary`

Summary of active weather events across Canada, the US, and Europe. This endpoint is derived from the /alerts endpoint.

*Coverage: us, europe, canada · Range: Latest · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `search`, `within` |
| Params | `fields`, `filter`, `limit`, `query`, `radius` |
| Filters | `warning`, `watch`, `advisory`, `outlook`, `statement`, `severe`, `flood`, `tropical`, `winter`, `marine`, `nonprecip`, `forecast`, `all`, `wind`, `fire`, `tsunami`, `now`, `synopsis`, `tornado`, `emergency`, `canada`, `usa`, `allcountries`, `hassmallpoly`, `distinct`, `nonmarine` |
| Query props | `type`, `wxzone`, `sig`, `sigp`, `name`, `issued`, `expires`, `active`, `emergency`, `issued`, `begins`, `expires`, `added` |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/alerts-summary

## `/conditions`

Global current, forecast, and past conditions for a specific date/time or in hourly intervals. Minutely precipitation forecasts are also available.

*Coverage: global · Range: 2004 to +15days · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `for`, `plimit`, `psort`, `pskip`, `filter`, `from`, `to`, `fields`, `lang` |
| Filters | `minutelyprecip`, `#min`, `#hr` |
| Query props | — |
| Sort fields | `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/conditions

## `/conditions/summary`

Global current and past conditions as a daily summary or a summary in specified intervals.

*Coverage: global · Range: 2004 to +15 days · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `for`, `from`, `to`, `plimit`, `psort`, `pskip`, `filter`, `lang` |
| Filters | `day`, `#hr` |
| Query props | — |
| Sort fields | `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/conditions-summary

## `/convective/outlook`

SPC's outlook for convective activity across the US. This includes the SPC's convective, hail, tornado, wind, and thunderstorm product.

*Coverage: conus · Range: +8 days · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `affects`, `contains`, `search` |
| Params | `filter`, `from`, `limit`, `p`, `query`, `radius`, `skip`, `sort`, `to` |
| Filters | `cat`, `prob`, `conhazo`, `torn`, `xtorn, sigtorn`, `alltorn`, `hail`, `xhail, sighail`, `allhail`, `wind`, `xwind, sigwind`, `allwind`, `all`, `general`, `marginal`, `slight`, `enhanced`, `moderate`, `high`, `day#` |
| Query props | `id`, `cat`, `day`, `type`, `name`, `code` |
| Sort fields | `id`, `cat`, `day`, `type`, `name`, `code`, `bdt`, `edt`, `idt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/convective-outlook

## `/countries`

Geographical data related to countries around the world.

*Coverage: global · Updates: Variable · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `search` |
| Params | `p`, `limit`, `query`, `skip`, `fields` |
| Filters | — |
| Query props | `name`, `iso`, `iso3`, `pop`, `area`, `altname` |
| Sort fields | `name`, `iso`, `iso3`, `pop` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/countries

## `/droughts/monitor`

Official drought areas per the National Drought Mitigation Center.

*Coverage: conus · Range: Latest · Updates: Weekly · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `affects`, `contains`, `search` |
| Params | `filter`, `limit`, `p`, `radius`, `query`, `skip`, `sort`, `to`, `from`, `fields`, `format` |
| Filters | `all`, `d0`, `d1`, `d2`, `d3`, `d4` |
| Query props | `id`, `type`, `name`, `code` |
| Sort fields | `id`, `type`, `name`, `code` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/droughts-monitor

## `/earthquakes`

Global earthquake data including magnitude, depth, and type.

*Coverage: global · Range: 1568 to now · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search`, `affects` |
| Params | `p`, `limit`, `filter`, `query`, `radius`, `minradius`, `sort`, `fields`, `from`, `to`, `skip`, `format` |
| Filters | `mini`, `minor`, `light`, `moderate`, `strong`, `major`, `great`, `shallow`, `mmi` |
| Query props | `id`, `mag`, `depth`, `state`, `name`, `country` |
| Sort fields | `dt`, `id`, `mag`, `depth`, `state`, `country`, `region` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/earthquakes

## `/energy/farm`

The energy farm endpoint provides energy output data for energy producing sites.

*Coverage: conus · Range: -24 hours · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `from`, `to`, `plimit`, `pskip` |
| Filters | — |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/energy-farm

## `/fires`

Wildfires across the U.S. and Canada with data including type, cause, area, and percent contained.

*Coverage: us, canada · Range: Latest · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `p`, `limit`, `radius`, `minradius`, `query`, `sort`, `skip`, `fields`, `format` |
| Filters | `geo`, `hasperimeter`, `hasnoperimeter` |
| Query props | `id`, `dt`, `area`, `name`, `state`, `country`, `conf` |
| Sort fields | `id`, `dt`, `area`, `name`, `state`, `country`, `conf` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/fires

## `/fires/outlook`

SPC's outlook for weather conditions that will promote the spread of fires.

*Coverage: conus · Range: +8 days · Updates: 2x/day · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `affects`, `contains`, `search`, `within` |
| Params | `p`, `filter`, `from`, `limit`, `query`, `radius`, `skip`, `sort`, `to`, `fields` |
| Filters | `firewx`, `dryltg`, `all`, `elevated`, `critical`, `extreme`, `isodryt`, `sctdryt`, `day1`, `day2`, `day3`, `day4`, `day5`, `day6`, `day7`, `day8` |
| Query props | `id`, `cat`, `day`, `type`, `name`, `code` |
| Sort fields | `id`, `cat`, `day`, `type`, `name`, `code`, `bdt`, `edt`, `idt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/fires-outlook

## `/forecasts`

Future weather conditions around the globe. We support daily, hourly, and many other forecast intervals.

*Coverage: global · Range: +15 days · Updates: 1 hour · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `limit`, `filter`, `from`, `to`, `skip`, `plimit`, `pskip`, `fields`, `lang` |
| Filters | `day`, `daynight`, `mdnt2mdnt`, `#hr`, `#min`, `precise`, `centroid` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/forecasts

## `/hail/archive`

Historical data providing hail occurrence and severity insight

*Coverage: US, Canada, Japan, Europe, Australia · Range: 2024-01-01 (US), 2024-03-08 (Europe), and 2025-02-01 (Other Regions) · Updates: Hourly · Cost: x12*

| | |
|---|---|
| Actions | `:id` |
| Params | `limit`, `fields`, `from`, `to` |
| Filters | — |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/hail-archive

## `/hail/threats`

Hail threats derived from Xweather's nowcast data

*Coverage: us, europe, canada, japan, australia · Range: Now to +60 minutes · Updates: Real-time · Cost: x12*

| | |
|---|---|
| Actions | `:id`, `closest`, `contains`, `route` |
| Params | `p`, `radius`, `fields`, `filter`, `plimit`, `psort`, `format` |
| Filters | `severe`, `notsevere`, `test` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/hail-threats

## `/impacts/:activity`

Global assessment of suboptimal weather conditions for a variety of business needs and activities.

*Coverage: global · Range: Latest · Updates: Real-time · Cost: x25*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `fields`, `filter` |
| Filters | `minseverity0`, `minseverity1`, `minseverity2`, `minseverity3`, `minseverity4`, `minseverity5` |
| Query props | — |
| Sort fields | — |

`:activity` is part of the path and required — `/impacts/general/55403`:
`general` (most outdoor activity: fire weather, severe, wind, lightning, air quality, temperature,
snow, rain) · `roadway_trucking` (severe, wind, lightning, snow, visibility, rollover risk,
temperature) · `maritime_small_craft` (wind, severe, lightning, waves) ·
`maritime_large_vessel` (waves, temperature, visibility, snow, wind).

Docs: https://www.xweather.com/docs/weather-api/endpoints/impacts

## `/indices/:type`

Indices for health and outdoor activities as based on common weather observations and forecasts.

*Coverage: global · Range: +15 days · Updates: Real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `limit`, `fields`, `filter`, `from`, `to` |
| Filters | `day`, `daynight`, `#hr` |
| Query props | — |
| Sort fields | — |

`:type` is part of the path and required — `/indices/migraine/55403`. Health indices:
`arthritis`, `coldflu`, `migraine`, `sinus`. Activity indices: `outdoors`, `golf`, `biking`,
`swimming`, `campfires`, `bees`.

Docs: https://www.xweather.com/docs/weather-api/endpoints/indices

## `/lightning`

Global lightning data based on location queries. Endpoint provides data such as location, amperage, and type of strike.

*Coverage: global · Range: 2016 to now · Updates: Real-time · Cost: x10*

| | |
|---|---|
| Actions | `:id`, `closest`, `route`, `within` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `filter`, `sort`, `skip`, `from`, `to`, `format` |
| Filters | `cg`, `all` |
| Query props | — |
| Sort fields | `dt`, `type`, `peakamp`, `numsensors` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning

## `/lightning/analytics`

An extension of the global lightning endpoint which includes damage potential and an error ellipse for each strike.

*Coverage: global · Range: 2016 to now · Updates: Real-time · Cost: x12*

| | |
|---|---|
| Actions | `:id`, `closest`, `route`, `within` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `filter`, `sort`, `skip`, `from`, `to`, `format` |
| Filters | `cg`, `all`, `ellipse50`, `ellipse80`, `ellipse90`, `ellipse99` |
| Query props | — |
| Sort fields | `dt`, `type`, `peakamp`, `numsensors` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning-analytics

## `/lightning/archive`

Global lightning data based on location queries. Endpoint provides data such as location, amperage, and type of strike. Archive data is available from Jan 2016 through the current date/time.

*Coverage: global · Range: 2016 to now · Updates: Real-time · Cost: x10*

| | |
|---|---|
| Actions | `:id`, `closest`, `route` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `filter`, `sort`, `skip`, `from`, `to`, `format` |
| Filters | `cg`, `ic`, `all` |
| Query props | — |
| Sort fields | `dt`, `type`, `peakamp`, `numsensors` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning-archive

## `/lightning/density`

Provides long-term lightning climatology by returning the 10-year average annual lightning strike density for a specific location, measured as strikes per square kilometer per year.

*Coverage: global · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `p` |
| Filters | — |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning-density

## `/lightning/flash`

Global lightning flash data based on location queries.

*Coverage: global · Range: -5 minutes · Updates: Real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `route` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `sort`, `skip`, `from`, `to`, `format` |
| Filters | — |
| Query props | — |
| Sort fields | `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning-flash

## `/lightning/summary`

A summary of lightning strikes that took place across the globe. Search can be limited by intracloud, cloud-to-ground, or both.

*Coverage: global · Range: -5 minutes · Updates: Real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `filter`, `sort`, `skip`, `from`, `to` |
| Filters | `cg`, `all`, `negative`, `positive` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning-summary

## `/lightning/threats`

Lightning nowcasts providing global potential thunderstorm activity.

*Coverage: global · Range: +1 hour · Updates: 2 minutes · Cost: x10*

| | |
|---|---|
| Actions | `:id`, `closest`, `contains`, `affects`, `route` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `filter`, `from`, `to`, `format`, `for`, `query`, `sort`, `plimit`, `pskip`, `psort`, `skip` |
| Filters | `severe`, `notsevere`, `forceutc` |
| Query props | `stormid`, `issued`, `minvalidtime`, `maxvalidtime`, `speed`, `added`, `created` |
| Sort fields | `stormid`, `minvalidtime`, `maxvalidtime` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning-threats

## `/lightning/turbinerisk`

Estimates the expected annual lightning strike frequency for a wind turbine at a specific location using long-term lightning climatology and turbine height.

*Coverage: global · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `p`, `height` |
| Filters | — |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/lightning-turbinerisk

## `/maritime`

The maritime API provides essential global marine weather data for navigation, offshore operations, coastal monitoring, and recreational activities, with flexible hourly or other intervals.

*Coverage: global · Range: -48 hours to +15 days · Updates: 6 hours · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `filter`, `from`, `to`, `for`, `pskip`, `psort`, `plimit`, `format` |
| Filters | `#hr` |
| Query props | — |
| Sort fields | `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/maritime

## `/maritime/archive`

Historical maritime data available around the globe.

*Coverage: global · Range: 2024 to now · Updates: 1 hour · Cost: x5*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `filter`, `from`, `to`, `for`, `plimit`, `psort`, `pskip`, `format` |
| Filters | `#hr` |
| Query props | — |
| Sort fields | `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/maritime-archive

## `/models/:model`

Returns raw forecast model data for a single forecast model at a requested location. Each response is a time series of forecast periods drawn from one model run. Use the Models Catalog endpoint to discover which models, run times, and datasets are available before making a request.

*Coverage: Global · Range: Varies by model · Updates: Per model run cycle · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `fields`, `p` |
| Filters | `skipnulls` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/models

## `/models/catalog`

Returns a catalog of the forecast models available through the API, including each model's accessible run times, forecast coverage, and the datasets (variables) it produces. Use this endpoint to discover what's available before requesting raw forecast data for a specific model from the /models/:model endpoint.

*Coverage: Global · Range: +15 days · Updates: Per model run cycle · Cost: x1*

| | |
|---|---|
| Actions | `:all` |
| Params | `fields` |
| Filters | — |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/models-catalog

## `/normals`

The normals endpoint provides access to the 30-year climate normals for US locations. This endpoint allows the receipt of up to one month of information per request.

*Coverage: conus, alaska, hawaii · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search`, `route` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `filter`, `query`, `sort`, `skip`, `from`, `to`, `plimit`, `psort`, `pskip`, `pfilter`, `format` |
| Filters | `daily`, `monthly`, `annual`, `hastemp`, `hasprecip`, `hassnow` |
| Query props | `id`, `state`, `country`, `md`, `mon`, `day`, `tmax`, `tmin`, `tavg`, `hdd`, `cdd`, `pmtd`, `smtd`, `sytd`, `name` |
| Sort fields | `id`, `md`, `mon`, `day`, `name`, `state`, `country`, `tmax`, `tmin`, `tavg`, `hdd`, `cdd`, `pmtd`, `mytd`, `smtd`, `sytd` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/normals

## `/normals/stations`

The normals/stations dataset provides access to the complete co-op/station information that normals are available for.

*Coverage: conus, alaska, hawaii · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search`, `route` |
| Params | `p`, `limit`, `radius`, `minradius`, `fields`, `filter`, `query`, `sort`, `skip`, `format` |
| Filters | `hastemp`, `hasprcp`, `hassnow` |
| Query props | `id`, `state`, `country`, `name` |
| Sort fields | `id`, `state`, `country`, `name` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/normals-stations

## `/observations`

The observations data set provides access to current weather observations from a variety of reporting stations.

*Coverage: global · Range: Latest · Updates: 1-60+ minutes (varies by station) · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search`, `route` |
| Params | `p`, `limit`, `radius`, `minradius`, `mindist`, `fields`, `filter`, `query`, `sort`, `skip`, `from`, `to`, `format`, `lang` |
| Filters | `metar`, `allstations`, `pws`, `madis`, `hfmetar`, `ausbom`, `envca`, `allownosky`, `wxrain`, `wxsnow`, `wxice`, `wxfog`, `qcok`, `strict`, `centroid`, `precise` |
| Query props | `temp`, `wind`, `dewpt`, `rh`, `pressure`, `winddir`, `gust`, `name`, `state`, `country`, `id`, `datasource`, `elev`, `qccode`, `trustfactor`, `dt`, `adt` |
| Sort fields | `temp`, `dewpt`, `rh`, `pressure`, `wind`, `winddir`, `gust`, `name`, `state`, `country`, `id`, `datasource`, `trustfactor`, `dt`, `adt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/observations

## `/observations/archive`

Historical observations by day are available through 2011.

*Coverage: global · Range: 2011-08-02 to now · Updates: 1-60+ minutes (varies by station) · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within` |
| Params | `p`, `limit`, `radius`, `filter`, `query`, `sort`, `skip`, `for`, `plimit`, `psort`, `pskip`, `fields`, `lang` |
| Filters | `allstations`, `official`, `pws`, `mesonet`, `hasprecip`, `hassky`, `centroid`, `precise` |
| Query props | `temp`, `dewpt`, `rh`, `pressure`, `wind`, `winddir`, `gust`, `name`, `hasprecip` |
| Sort fields | `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/observations-archive

## `/observations/summary`

Daily summaries based on previously recorded observations. Daily summaries are available through 2011.

*Coverage: global · Range: 2011-08-02 to now · Updates: 20 minutes · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within` |
| Params | `p`, `limit`, `radius`, `filter`, `query`, `sort`, `skip`, `from`, `to`, `for`, `plimit`, `pskip`, `fields`, `psort`, `lang` |
| Filters | `allstations`, `official`, `metar`, `pws`, `mesonet or madis`, `hfmetar`, `hasprecip`, `hassky`, `qcok`, `strict`, `centroid`, `precise` |
| Query props | `id`, `datasource`, `count`, `maxt`, `mint`, `avgt`, `maxdewpt`, `mindewpt`, `avgdewpt`, `maxrh`, `minrh`, `avgrh`, `maxv`, `minv`, `avgv`, `wind`, `gust`, `maxp`, `minp`, `avgp`, `precip`, `precipc`, `elev`, `name`, `state`, `country`, `dt`, `hasprecip`, `qc`, `minqc`, `maxqc`, `mintrustfactor`, `maxtrustfactor` |
| Sort fields | `maxt`, `mint`, `avgt`, `maxdewpt`, `mindewpt`, `avgdewpt`, `maxrh`, `minrh`, `avgrh`, `maxv`, `minv`, `avgv`, `wind`, `gust`, `maxp`, `minp`, `avgp`, `precip`, `mintrustfactor`, `maxtrustfactor` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/observations-summary

## `/phrases/summary`

Phrase related to the current and expected conditions for the next several hours.

*Coverage: global · Range: Latest · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `p`, `filter`, `radius`, `fields`, `format`, `limit`, `skip` |
| Filters | `metar`, `pws`, `mesonet`, `allstations`, `noob` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/phrases-summary

## `/places`

Geographical information for a given location. Including elevation, population, region, country, continent, etc.

*Coverage: global · Updates: Monthly · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `p`, `radius`, `minradius`, `limit`, `filter`, `query`, `sort`, `fields`, `skip`, `format` |
| Filters | `airport`, `amusement`, `bridge`, `camp`, `church`, `county`, `divisions`, `feature`, `fort`, `golf`, `lake`, `neighborhood`, `parish`, `park`, `poi`, `port`, `ppl`, `reserve`, `school`, `stadium`, `temple`, `trail`, `tunnel`, `university`, `worship`, `complex`, `simple` |
| Query props | `name`, `altname`, `state`, `country`, `pop` |
| Sort fields | `name`, `pop` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/places

## `/places/airports`

Geographical information about airports around the world.

*Coverage: global · Updates: Near Real Time · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `p`, `limit`, `radius`, `minradius`, `filter`, `query`, `sort`, `skip`, `fields`, `format` |
| Filters | `airport`, `smallairport`, `medairport`, `largeairport`, `heliport`, `balloonport`, `sea`, `all`, `closed` |
| Query props | `id`, `name`, `city`, `state`, `country`, `type`, `iata` |
| Sort fields | `id`, `name`, `type`, `iata` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/places-airports

## `/places/postalcodes`

Provides geographical information for US and Canadian postal codes.

*Coverage: us, canada · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `p`, `limit`, `radius`, `minradius`, `filter`, `query`, `sort`, `skip`, `fields`, `format` |
| Filters | `us`, `ca, canada`, `standard` |
| Query props | `id`, `zip`, `postalcode`, `name`, `city`, `state`, `country`, `type` |
| Sort fields | `id`, `zip`, `postalcode`, `name`, `city`, `type` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/places-postalcodes

## `/renewables/irradiance/archive`

Retrieve historical solar irradiance data for any location and date range, including detailed time series of solar energy measurements to analyze past solar potential or validate solar performance.

*Coverage: europe, africa · Range: 2004-01-20 to 2025-09-30 · Updates: Hourly · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `fields`, `filter`, `from`, `to`, `tilt`, `azimuth`, `panel_mode`, `horizon`, `preset` |
| Filters | `#hr` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/renewables-irradiance-archive

## `/renewables/irradiance/summary`

Retrieve historical irradiance averages for a specific location at monthly, annual, and overall resolutions. The fullYears summary provides daily average kWh m/2 and annual average kWh m/2.

*Coverage: Africa, Central America, North America, South America, Europe · Range: 2004-01-20 to 2025-09-30 · Cost: x10*

| | |
|---|---|
| Actions | `:id` |
| Params | `fields`, `filter`, `from`, `to`, `tilt`, `azimuth`, `panel_mode`, `horizon`, `preset` |
| Filters | `ghi`, `dni`, `dif`, `annual`, `monthly`, `climatologymonth`, `fullperiod`, `fullyears` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/renewables-irradiance-summary

## `/renewables/irradiance/tmy`

Retrieve historical solar irradiance data for a specific location and resolution represented as a typical meteorogical year (TMY)

*Coverage: Africa, Europe, Central America, North America, South America · Range: - · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `fields`, `filter`, `tilt`, `azimuth`, `horizon`, `panel_mode`, `format`, `preset` |
| Filters | — |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/renewables-irradiance-tmy

## `/rivers`

U.S. lake and river gauges collected and distributed by NOAA's AHPS department.

*Coverage: conus, alaska, hawaii · Range: Latest · Updates: 1 hour · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `p`, `limit`, `radius`, `minradius`, `skip`, `filter`, `query`, `sort`, `fields`, `from`, `to`, `format` |
| Filters | `outofservice`, `inservice`, `obsnotcurrent`, `notdefined`, `lowthreshold`, `noflooding`, `action`, `flood`, `minor`, `moderate`, `major`, `allflood`, `heighttype`, `flowtype` |
| Query props | `id`, `dt`, `status`, `statuscode`, `hasimpacts`, `name`, `waterbody`, `state`, `country` |
| Sort fields | `id`, `dt`, `status`, `statuscode`, `hasimpact`, `name`, `waterbody`, `state`, `country` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/rivers

## `/rivers/gauges`

Enhanced data from rivers and lake gauges per the /rivers endpoint. Data includes recent crests, historical crests, and flood impacts.

*Coverage: conus, alaska, hawaii · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `search`, `within` |
| Params | `p`, `limit`, `skip`, `query`, `filter`, `sort`, `radius`, `fields`, `format` |
| Filters | `impacts`, `recentcrests`, `historiccrests`, `lowwaterrecords` |
| Query props | `id`, `place`, `waterbody`, `state`, `country` |
| Sort fields | `id`, `place`, `waterbody`, `state`, `country` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/rivers-gauges

## `/roadweather`

The roadweather endpoint offers real-time, accurate road condition insights powered by Vaisala Xweather forecasts, enhancing user safety and decision-making for optimal driving experiences.

*Coverage: us, europe, japan, canada, australia, new-zealand · Range: +24 hours · Updates: 6 hours; 15 min the first +2 hours · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `for`, `from`, `to`, `plimit`, `pskip`, `psort`, `fields` |
| Filters | `primary`, `secondary`, `bridge`, `noroadcheck` |
| Query props | — |
| Sort fields | `dt`, `summary`, `summaryindex` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/roadweather

## `/roadweather/analytics`

The roadweather/analytics endpoint offers real-time, accurate road condition insights powered by Vaisala Xweather forecasts, enhancing user safety and decision-making for optimal driving experiences.

*Coverage: us, canada, europe, japan, new-zealand, australia · Range: +24 hours · Updates: 6 hours; 15 min the first +2 hours · Cost: x10*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `for`, `from`, `to`, `plimit`, `pskip`, `psort`, `fields` |
| Filters | `primary`, `secondary`, `bridge`, `noroadcheck`, `addweather` |
| Query props | — |
| Sort fields | `dt`, `summary`, `summaryindex`, `condition`, `temp`, `truckrollover`, `hydroplane`, `lowvisfog`, `lowvisblowingsnow` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/roadweather-analytics

## `/roadweather/conditions`

The roadweather/conditions endpoint offers real-time, accurate road condition insights powered by Vaisala Xweather forecasts, enhancing user safety and decision-making for optimal driving experiences.

*Coverage: us, canada, japan, europe, australia, new-zealand · Range: +24 hours · Updates: 6 hours; 15 min the first +2 hours · Cost: x5*

| | |
|---|---|
| Actions | `:id`, `route` |
| Params | `p`, `from`, `for`, `to`, `plimit`, `pskip`, `psort`, `fields` |
| Filters | `primary`, `secondary`, `bridge`, `noroadcheck` |
| Query props | — |
| Sort fields | `dt`, `summary`, `summaryindex`, `condition`, `temp` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/roadweather-conditions

## `/stormcells`

Observed storm cells and their forecast tracks per the NEXRAD radar system in the U.S. Data will include general, hail, rotating, and tornadic storm cells.

*Coverage: us, puerto-rico, guam · Range: Latest · Updates: 2-3 Minutes · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search`, `affects` |
| Params | `p`, `limit`, `radius`, `mindist`, `minradius`, `filter`, `fields`, `query`, `skip`, `sort`, `format` |
| Filters | `hail`, `rotating`, `tornado`, `threat`, `rainmoderate`, `rainheavy`, `rainintense`, `conus` |
| Query props | `hailprob`, `hailsevere`, `hailsize`, `tvs`, `mda, rotation`, `dbz`, `type`, `isgeneral`, `ishail`, `isrotating`, `istornado`, `isthreat`, `name`, `state`, `country` |
| Sort fields | `hailprob`, `hailsevere`, `hailsize`, `tvs`, `mda, rotation`, `dbz`, `isgeneral`, `ishail`, `isrotating`, `istornado`, `isthreat`, `name`, `state`, `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/stormcells

## `/stormcells/summary`

A summary of active storm cells per the /stormcells endpoint.

*Coverage: us, puerto-rico, guam · Range: Latest · Updates: 2-3 minutes · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `affects`, `search`, `within` |
| Params | `p`, `filter`, `query`, `radius`, `limit`, `fields`, `format` |
| Filters | `hail`, `rotating`, `tornado`, `threat`, `rainmoderate`, `rainheavy`, `rainintense`, `conus`, `geo`, `noforecast` |
| Query props | `hail, hailprob`, `hailsevere`, `hailsize`, `tvs`, `mda, rotation`, `dbz`, `name`, `state`, `country`, `pop*` |
| Sort fields | `pop*` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/stormcells-summary

## `/stormreports`

Local storm reports transmitted by the National Weather Service in the U.S.

*Coverage: us · Range: 1950-01-03 to now · Updates: 15 minutes · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `p`, `limit`, `radius`, `filter`, `query`, `sort`, `skip`, `fields`, `to`, `from` |
| Filters | `avalanche`, `blizzard`, `dust`, `flood`, `fog`, `ice`, `hail`, `lightning`, `marine`, `rain`, `snow`, `tides`, `tornado`, `tropical`, `wind` |
| Query props | `code`, `type`, `state`, `name`, `detail` |
| Sort fields | `code`, `type`, `state`, `name`, `detail`, `dt` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/stormreports

## `/stormreports/summary`

A summary of storm reports derived from the /stormreports endpoint.

*Coverage: us · Range: 1950-01-03 to now · Updates: 15 minutes · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `within`, `search` |
| Params | `p`, `fields`, `filter`, `from`, `to`, `radius`, `query` |
| Filters | `avalanche`, `blizzard`, `dust`, `flood`, `fog`, `ice`, `hail`, `lightning`, `marine`, `rain`, `snow`, `tides`, `tornado`, `tropical`, `wind` |
| Query props | `code`, `type`, `state`, `name`, `detail` |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/stormreports-summary

## `/sunmoon`

Global sun and moon rise / set data.

*Coverage: global · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `limit`, `filter`, `from`, `to`, `fields`, `skip`, `sort` |
| Filters | `sun`, `twilight`, `moon`, `moonphase` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/sunmoon

## `/sunmoon/moonphases`

Current phase of the moon.

*Coverage: global · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `search`, `contains` |
| Params | `p`, `limit`, `filter`, `from`, `to` |
| Filters | `new`, `first`, `full`, `third` |
| Query props | `type`, `code` |
| Sort fields | `dt`, `code`, `type` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/sunmoon-moonphases

## `/threats`

Localized threat summary based on the location provided.

*Coverage: global · Range: Latest · Updates: Near real-time · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `p`, `radius`, `fields`, `query` |
| Filters | — |
| Query props | `hailprob`, `hailsevere`, `hailsize`, `isgeneral`, `ishail`, `isrotating`, `istornado`, `isthreat`, `tvs` |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/threats

## `/tides`

Current and forecast tide levels for US coasts.

*Coverage: us · Updates: 1 month · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `limit`, `p`, `radius`, `minradius`, `filter`, `query`, `sort`, `skip`, `from`, `to`, `plimit`, `psort`, `pskip`, `fields` |
| Filters | `highlow`, `high`, `low` |
| Query props | `id`, `state`, `country`, `type`, `height`, `heightM` |
| Sort fields | `id`, `name`, `state`, `country`, `dt`, `type`, `height` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/tides

## `/tides/stations`

General information about a specific tides station.

*Coverage: us, guam, puerto-rico · Cost: x1*

| | |
|---|---|
| Actions | `:id`, `closest`, `within`, `search` |
| Params | `p`, `limit`, `radius`, `filter`, `query`, `sort`, `skip`, `fields` |
| Filters | — |
| Query props | `id`, `state`, `country`, `type` |
| Sort fields | `id`, `name`, `state`, `country`, `type` |

Docs: https://www.xweather.com/docs/weather-api/endpoints/tides-stations

## `/tropicalcyclones`

Provides information on active tropical cyclones across the globe.

*Coverage: global · Range: Latest · Updates: 6 hours; NHC storms up to 1-3 hours near landfall · Cost: x1*

| | |
|---|---|
| Actions | `:all`, `closest`, `search`, `within`, `affects` |
| Params | `p`, `fields`, `filter`, `format`, `limit`, `query`, `radius`, `minradius`, `skip`, `sort` |
| Filters | `atlantic`, `al`, `eastpacific`, `ep`, `centralpacific`, `cp`, `westpacific`, `wp`, `pacific`, `indian`, `io`, `southern`, `sh`, `position`, `track`, `forecast`, `windfield`, `geo`, `test`, `invests`, `dateline` |
| Query props | `id`, `basin`, `origin`, `currentbasin`, `year`, `event`, `name`, `startdate`, `enddate`, `maxtype`, `maxcat`, `maxwindspeed`, `minpressure`, `test`, `stormtype`, `stormcat`, `windspeed`, `pressure`, `stormdir`, `stormspeed`, `trackstormtype`, `trackstormcat`, `trackwindspeed`, `trackpressure`, `trackstormdir`, `trackstormspeed`, `fcststormtype`, `fcststormcat`, `fcstwindspeed` |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/tropicalcyclones

## `/tropicalcyclones/archive`

Provides archive information on global tropical cyclones.

*Coverage: global · Range: 1851-06-25 to now · Updates: 6 hours; NHC storms up to 1-3 hours near landfall · Cost: x1*

| | |
|---|---|
| Actions | `closest`, `search`, `within`, `affects` |
| Params | `p`, `fields`, `filter`, `format`, `limit`, `query`, `radius`, `minradius`, `skip`, `sort`, `from`, `to` |
| Filters | `atlantic`, `al`, `eastpacific`, `ep`, `centralpacific`, `cp`, `westpacific`, `wp`, `pacific`, `indian`, `io`, `southern`, `sh`, `position`, `track`, `forecast`, `geo`, `test`, `active`, `notactive` |
| Query props | `id`, `basin`, `origin`, `year`, `event`, `name`, `startdate`, `enddate`, `maxtype`, `maxcat`, `maxwindspeed`, `minpressure`, `test`, `stormtype`, `stormcat`, `windspeed`, `pressure`, `stormdir`, `stormspeed`, `trackstormtype`, `trackstormcat`, `trackwindspeed`, `trackpressure`, `trackstormdir`, `trackstormspeed`, `fcststormtype`, `fcststormcat`, `fcstwindspeed`, `active` |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/tropicalcyclones-archive

## `/xcast/forecasts`

Hyperlocal forecast data derived from Xcast sensors

*Coverage: global · Range: +15days · Updates: 1 hour · Cost: x1*

| | |
|---|---|
| Actions | `:id` |
| Params | `limit`, `fields`, `filter`, `from`, `to`, `skip` |
| Filters | `1hr`, `10min` |
| Query props | — |
| Sort fields | — |

Docs: https://www.xweather.com/docs/weather-api/endpoints/xcast-forecasts
