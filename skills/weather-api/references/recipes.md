# Common queries cookbook

Sourced from https://www.xweather.com/docs/weather-api/reference/common-queries — the API's own
"common queries by industry" list, reproduced with the credential suffix trimmed. Append
`&client_id={client_id}&client_secret={client_secret}` to every URL. Where the docs show
`{start_date}` / `{end_date}`, substitute a real date (`2026-07-01`) or a relative offset (`-30days`).

Three entries in the published list contain typos, corrected here: a missing `?` before the query
string on the "Current Air Quality", "Hyperlocal Conditions", "Daily Conditions Summary" and
"Moonphases" rows, `mexico%city` → `mexico%20city`, and a duplicated base URL on "Weather Station
Data".

---

## Apps and consumer weather

| Need | URL |
|---|---|
| Current conditions at a coordinate, all station types, selected fields | `https://data.api.xweather.com/observations/39.630661,-105.709282?query=temp:!NULL,wind:!NULL,pressure:!NULL,winddir:!NULL&filter=allstations,hasprecip&fields=id,loc,relativeTo.distanceMI,ob.dateTimeISO,ob.weather,ob.tempF,ob.precipIN,ob.windSpeedMPH,ob.windDir,ob.pressureIN,ob.sunriseISO,ob.sunsetISO` |
| Hyperlocal current conditions | `https://data.api.xweather.com/conditions/paca,panama` |
| Hyperlocal 3-day conditions series | `https://data.api.xweather.com/conditions/7.5344333566393615,-77.52957698454809?to=+3days` |
| Next 6 hours, hourly | `https://data.api.xweather.com/conditions/chicago,il?to=+6hr&filter=1hr` |
| Minute-by-minute precip for the next hour | `https://data.api.xweather.com/conditions/seattle,wa?filter=minutelyprecip,1min` |
| 15-day daily forecast | `https://data.api.xweather.com/forecasts/berlin,de?filter=day&limit=15` |
| Daily conditions summary | `https://data.api.xweather.com/conditions/summary/indianapolis,in` |
| Severe weather alerts | `https://data.api.xweather.com/alerts/denver,co?limit=10` |
| Sunrise / sunset for the next day | `https://data.api.xweather.com/sunmoon/pierre,sd?from=now&to=+1day` |
| Moon phases | `https://data.api.xweather.com/sunmoon/moonphases/berlin,de` |
| Tides, current + forecast | `https://data.api.xweather.com/tides/anchorage,ak?from=now&to=+1day` |
| Named weather station's latest observation | `https://data.api.xweather.com/observations/search?query=id:KORD` |

## Air quality

| Need | URL |
|---|---|
| Current air quality | `https://data.api.xweather.com/airquality/palm%20springs,ca` |
| Current air quality on a national scale (China shown) | `https://data.api.xweather.com/airquality/beijing,cn?filter=china` |
| Nearest 10 air quality observations | `https://data.api.xweather.com/airquality/closest?p=beijing,cn&limit=10` |
| Air quality forecast | `https://data.api.xweather.com/airquality/forecasts/mexico%20city,mx` |
| Air health forecast from a date | `https://data.api.xweather.com/airquality/forecasts/dallas,texas?from={start_date}` |

## Severe weather, storms, and hazards

| Need | URL |
|---|---|
| All active tropical cyclones | `https://data.api.xweather.com/tropicalcyclones?p=&filter=all` |
| Earthquakes inside a bounding box | `https://data.api.xweather.com/earthquakes/within?p=25.425587018544316,-163.64201510020976,15.561843881489148,-151.16154749252362&limit=10` |
| Nearest active wildfire | `https://data.api.xweather.com/fires/closest?p=darwin,au` |
| Lightning strikes within 25 miles | `https://data.api.xweather.com/lightning/closest?p=hyderabad,in&format=json&radius=25miles&filter=all&limit=10` |
| Incoming hail and tornadic threats | `https://data.api.xweather.com/threats/birmingham,al?fields=periods[#].storms.hail,periods[#].storms.tornadic` |
| Storm cell point data as GeoJSON | `https://data.api.xweather.com/stormcells/wauconda,il?format=geojson` |
| All active storm cells with polygons, for emergency ops | `https://data.api.xweather.com/stormcells/summary?filter=geo&format=geojson` |
| Hail damage verification for an insurance claim | `https://data.api.xweather.com/stormreports/search?query=state:pa,detail:1:2&filter=hail&from={start_date}&limit=100` |

## Agriculture

| Need | URL |
|---|---|
| Historical growth analysis over a date range | `https://data.api.xweather.com/conditions/summary/minneapolis,mn?from={start_date}&to={end_date}` |
| Irrigation analytics, yesterday's summary | `https://data.api.xweather.com/conditions/summary/minneapolis,mn?from=-1day` |
| In-field 7-day hourly forecast with agronomy fields | `https://data.api.xweather.com/forecasts/minneapolis,mn?filter=1hr&limit=168&fields=periods.dateTimeISO,periods.maxTempF,periods.maxTempC,periods.pop,periods.precipIN,periods.precipMM,periods.humidity,periods.sky,periods.solradWM2,periods.dewpointF,periods.dewpointC,periods.windDir,periods.windSpeedMaxMPH,periods.windSpeedMaxKPH,periods.weather` |
| Irrigation 72-hour hourly forecast | `https://data.api.xweather.com/forecasts/minneapolis,mn?filter=1hr&limit=72&fields=periods.dateTimeISO,periods.maxTempF,periods.maxTempC,periods.pop,periods.precipIN,periods.precipMM,periods.humidity,periods.sky,periods.solradWM2,periods.dewpointF,periods.dewpointC,periods.windDir,periods.windSpeedMaxMPH,periods.windSpeedMaxKPH,periods.weather` |

## Energy and utilities

| Need | URL |
|---|---|
| Hourly energy analytics for a past day | `https://data.api.xweather.com/conditions/minneapolis,mn?from={start_date}&to=+1day&limit=24` |
| Grid load / production forecast including 80 m wind | `https://data.api.xweather.com/forecasts/minneapolis,mn?filter=1hr&limit=72&fields=periods.dateTimeISO,periods.maxTempF,periods.maxTempC,periods.pop,periods.precipIN,periods.precipMM,periods.humidity,periods.sky,periods.solradWM2,periods.dewpointF,periods.dewpointC,periods.windDir,periods.windSpeedMaxMPH,periods.windSpeedMaxKPH,periods.windDir80m,periods.windSpeedMax80mMPH,periods.windSpeedMax80mKPH,periods.weather` |

## Logistics and other

| Need | URL |
|---|---|
| Packaging recommendations from a 72-hour hourly forecast | `https://data.api.xweather.com/forecasts/minneapolis,mn?filter=1hr&limit=72&fields=periods.dateTimeISO,periods.maxTempF,periods.maxTempC,periods.pop,periods.precipIN,periods.precipMM,periods.humidity,periods.dewpointF,periods.dewpointC,periods.weather` |
| Machine-learning training window at a coordinate | `https://data.api.xweather.com/conditions/31.43799,121.186?from={start_date}&to=+1day&limit=24` |
| Historical analysis from a start date | `https://data.api.xweather.com/conditions/summary/minneapolis,mn?from={start_date}` |

---

## Patterns worth reusing

**Trim the payload before anything else.** Every agriculture/energy recipe above leads with
`fields=` — an hourly 7-day forecast is a large document, and naming the ~12 properties you actually
consume is the difference between a usable response and a wall of JSON.

**`filter=1hr&limit=N` is the hourly idiom.** `limit` counts intervals, not days: 24 for a day, 72
for three days, 168 for a week, 360 for the full 15-day forecast range.

**`closest` needs both `radius` and `limit`.** Without `limit` you get exactly one record; without a
generous `radius` you often get none. `radius=25miles&limit=10` is a sane starting point for
point-event data (lightning, fires, earthquakes).

**Point-in-polygon questions use `contains`, not `within`.** "Is Denver in a drought area / severe
outlook?" → `/droughts/monitor/contains?p=denver,co`, `/convective/outlook/contains?p=denver,co`.
The place must go in `p=` — an action in the path leaves no room for it. On these polygon endpoints
the bare `:id` form is a documented shorthand for the same query: `/droughts/monitor/denver,co`.
`within` is for "what's inside this shape I'm describing".

**`format=geojson` for anything going onto a map.** Storm cells, alert polygons, fire perimeters,
and every `route` response are geometry-first.

**Historical vs. summary.** `/conditions/summary` and `/observations/summary` give daily aggregates
(max/min/total). `/observations/archive` and `/conditions?from=…&to=…` give the underlying time
series. Pick summary when the user says "the high that day", archive when they say "hour by hour".
