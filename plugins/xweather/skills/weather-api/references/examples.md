# Documented example requests, by endpoint

Copied verbatim from each endpoint's documentation page. Paths are relative to
`https://data.api.xweather.com`; append `&client_id=…&client_secret=…` to every one.

These are the highest-signal reference for URL shape — when a request resembles one of these,
copy its structure rather than inventing parameters.

---

## `/airquality`

- `/airquality/beijing,cn`  
  Returns the estimated air quality information for Beijing, China.
- `/airquality/55403`  
  Returns the estimated air quality information for zip code 55403 (Minneapolis, MN).
- `/airquality/44.9778,-93.265`  
  Returns the estimated air quality information for the specified latitude, longitude.
- `/airquality/beijing,cn?filter=china`  
  Returns the estimated air quality information for Beijing, China using the China defines air quality categories.

## `/airquality/archive`

- `/airquality/archive/phoenix,az?from=2024-03-23`  
  Provides an hourly air quality data for Phoenix on March 23rd, 2024.
- `/airquality/archive/55428?filter=3hr`  
  Provides archive data in 3 hour intervals for today in the 55428 zip code.
- `/airquality/archive/london,uk?filter=uk&from=2024-02-01`  
  Provides a full day of air quality data on Feb 1, 2024 in London utilizing the UK air quality categories and calculations.

## `/airquality/forecasts`

- `/airquality/forecasts/55403`  
  Returns the estimated daily air quality forecast for Minneapolis, MN
- `/airquality/forecasts/beijing,cn?filter=1hr&limit=24`  
  Returns the next 24 hour estimated air quality forecast in hourly intervals for Beijing, China
- `/airquality/forecasts/44.9778,-93.265?filter=3hr&limit=16`  
  Returns the estimated air quality forecast for the specified latitude, longitude in 3 hour intervals for the next 48 hours
- `/airquality/forecasts/beijing,cn?filter=1hr&limit=24&filter=china`  
  Returns the estimated air quality forecast for Beijing, China using the China defined air quality categories.

## `/airquality/index`

- `/airquality/index/beijing,cn`  
  Returns the air quality index for Beijing, China
- `/airquality/index/55403`  
  Returns the air quality index for zip code 55403 (Minneapolis, MN)
- `/airquality/index/44.9778,-93.265`  
  Returns the air quality index for the specified latitude, longitude.

## `/alerts`

- `/alerts/55403`  
  Returns data for zip code 55403.
- `/alerts/45.25,-95.25`  
  Returns the alerts that affect the specified latitude/longitude.
- `/alerts/?p=55403&query=type:TO.W`  
  Return tornado warnings affecting zip code 55403
- `/alerts/minneapolis,mn?filter=flood`  
  Return flood related alerts affecting Minneapolis,MN

## `/alerts/summary`

- `/alerts/summary`  
  Return a summary for all active alerts.
- `/alerts/summary/minneapolis,mn`  
  Return a summary for all active alerts within a 50 mile radius of Minneapolis, MN
- `/alerts/summary/minneapolis,mn?radius=100miles`  
  Return a summary for all active alerts within a 100 mile radius of Minneapolis, MN
- `/alerts/summary/?filter=severe`  
  Return a summary for all severe thunderstorm and tornado watches/warnings.
- `/alerts/summary/?filter=severe;flood`  
  Return a summary for all alerts for severe or flood related events. Note the semicolon is used to represent a logical 'OR'.

## `/conditions`

- `/conditions/55403`  
  Returns current conditions for zip code 55403
- `/conditions/45.25,-95.25`  
  Returns current conditions for the specified latitude/longitude
- `/conditions/minneapolis,mn?for=now`  
  Returns the current conditions for Minneapolis, MN. **NOTE**: from=now is the same as providing no for parameter.
- `/conditions/minneapolis,mn?for=-4hours`  
  Returns the weather conditions for Minneapolis, MN for 4 hours ago.
- `/conditions/minneapolis,mn?for=2020-05-09 13:46:00`  
  Returns the weather conditions for Minneapolis, MN for May 9th, 2020 at 1:46pm local time for the requested location. NOTE: The historical addon maybe required to access dates in the past.
- `/conditions/paris,france?from=-12hours&to=now&plimit=12`  
  Returns hourly conditions for the past 12 hours for Paris, France
- `/conditions/minneapolis,mn?filter=minutelyprecip`  
  Returns the next hour of precipitation rate in 1 minute intervals.
- `/conditions/minneapolis,mn?filter=minutelyprecip&limit=30`  
  Returns the next 30 minutes of precipitation rate in 1 minute intervals.
- `/conditions/minneapolis,mn?filter=minutelyprecip,5min`  
  Returns the next hour of precipitation rate in 5 minute intervals (vs the default 1 minute)
- `/conditions/paris,france?from=now&to=+1hour&filter=1min`  
  Returns the next hour of conditions in 1 minute intervals.
- `/conditions/seoul,kr?from=2024-01-01&to=+1month`  
  Returns hourly conditions in Seoul start on January 1st, 2024 at midnight (local time) through the end of the month. Note: this will count as 31 API accesses.

## `/conditions/summary`

- `/conditions/summary/55403`  
  Returns today's summary of the weather conditions for zip code 55403
- `/conditions/summary/45.25,-95.25`  
  Return to today's summary of weather conditions for the specified latitude/longitude
- `/conditions/summary/paris,france?from=yesterday`  
  Return yesterday's daily weather condition summary for Paris, France
- `/conditions/summary/minneapolis,mn?from=today midnight&to=now&filter=4hr`  
  Return 6 hour weather condition summaries from midnight today through the current time.
- `/conditions/summary/tokyo,jp?from=2024-02-01&to=+1month`  
  Returns a daily conditions summary for the entire month of February 2024. Note: this will cost 29 API accesses.

## `/convective/outlook`

- `/convective/outlook/search?filter=conhazo`  
  Return the convective categorical outlooks for today. Since no from parameter provided, defaults to today.
- `/convective/outlook/search?filter=conhazo&from=today`  
  Return the convective categorical outlooks for today.
- `/convective/outlook/search?filter=conhazo&from=+1day`  
  Return the convective categorical outlooks for tomorrow.
- `/convective/outlook/search?filter=conhazo,geo`  
  Return the convective categorical outlooks for today and include the polygons for the outlooks.
- `/convective/outlook/search?filter=conhazo&sort=code&from=today`  
  Return the convective categorical outlooks for today, sorted by the least significant to the highest.
- `/convective/outlook/search?filter=conhazo&sort=code:-1&from=today`  
  Return the convective categorical outlooks for today, sorted by the highest significant to the lowest.
- `/convective/outlook/atlanta,ga`  
  Return the convective categorical outlooks for today that Atlanta, GA is contained in.
- `/convective/outlook/contains?p=atlanta,ga&filter=conhazo`  
  Return the convective categorical outlooks for today that Atlanta, GA is contained in.
- `/convective/outlook/contains?p=44.96,-93.27&filter=conhazo`  
  Return the convective categorical outlooks for today that contain the specified latitude/longitude
- `/convective/outlook/atlanta,ga?filter=conhazo&from=today&to=+7days&sort=day`  
  Return the convective categorical outlooks for days 1 - 8 that Atlanta, GA is contained within. The results will be sorted by the coverage day
- `/convective/outlook/atlanta,ga?filter=conhazo&from=today&to=+7days&sort=day&fields=details.range,details.risk.type`  
  Return the convective categorical outlooks for days 1 - 8 that Atlanta, GA is contained within. The results will be sorted by the coverage day. The fields parameter will limit the data to the elements needed. This greatly reduces bandwidth and resources.
- `/convective/outlook/ec31f2f9654addad2e4f773522f7b2c3`  
  Return the outlook with id of "ec31f2f9654addad2e4f773522f7b2c3"
- `/convective/outlook/ec31f2f9654addad2e4f773522f7b2c3?filter=geo`  
  Return the outlook with id of "ec31f2f9654addad2e4f773522f7b2c3" and include the polygon(s) data for the outlook
- `/convective/outlook/affects?p=ec31f2f9654addad2e4f773522f7b2c3&pop=50000&limit=10`  
  Return the top 10 locations with at least a population of 50,000 that are within the outlook with id "ec31f2f9654addad2e4f773522f7b2c3"

## `/countries`

- `/countries/us`  
  Return country information for the US.
- `/countries/55403`  
  Returns country information for the country specified by zip code 55403 (Minneapolis, MN, US).
- `/countries?p=45.25,-95.25`  
  Returns country information for the closest location to the specified latitude/longitude.
- `/countries/search?query=pop:30000000&limit=100`  
  Returns up to 100 countries that have a population of at least 30 million.
- `/countries/search?query=area:5000000:10000000&limit=10`  
  Returns up to 10 countries that have an area of 5 - 10 Million square kilometers.

## `/droughts/monitor`

- `/droughts/monitor/search?filter=all`  
  Return all of the drought monitor intensity levels, without the polygons.
- `/droughts/monitor/search?filter=all&sort=code`  
  Return all of the drought monitor intensity levels, without the polygons and sorted by intensity from D0 to D4
- `/droughts/monitor/search?filter=all,geo&sort=code`  
  Return all the drought monitor intensity levels, including polygons and sorted by intensity level from D0 to D4
- `/droughts/monitor/search?filter=all,geo&sort=code&format=geojson`  
  Return all the drought monitor intensity levels, including polygons and sorted by intensity level from D0 to D4. The object will be in GeoJson format.
- `/droughts/monitor/search?filter=D4`  
  Return the drought monitor intensity level D4, without polygons.
- `/droughts/monitor/search?filter=D4,geo`  
  Return the drought monitor intensity level D4, including polygons.
- `/droughts/monitor/san diego,ca`  
  Return the drought monitor information that San Diego, CA is within. This example if useful to quickly check if a location is in a drought and at what level. This query is equivalent to /droughts/monitor/contains?p=san diego,ca
- `/droughts/monitor/contains?p=san diego,ca`  
  Return the drought monitor information that San Diego, CA is within. This example if useful to quickly check if a location is in a drought and at what level.
- `/droughts/monitor/contains?p=44.96,-93.27`  
  Returns the drought monitor information for a specified latitude/longitude
- `/droughts/monitor/ec31f2f9654addad2e4f773522f7b2c3`  
  Return the drought monitor information with id of "ec31f2f9654addad2e4f773522f7b2c3"
- `/droughts/monitor/ec31f2f9654addad2e4f773522f7b2c3?filter=geo`  
  Return the drought monitor information, including polygon, for object id "ec31f2f9654addad2e4f773522f7b2c3"
- `/droughts/monitor/affects?p=ec31f2f9654addad2e4f773522f7b2c3&pop=50000&limit=10`  
  Returns the top 10 locations, with at least a population of 50,000 that are within the intensity level with id "ec31f2f9654addad2e4f773522f7b2c3"

## `/earthquakes`

- `/earthquakes/san diego,ca?radius=100miles`  
  Return nearby earthquakes within 100 miles of San Diego, California.
- `/earthquakes/closest?p=74640`  
  Return closest/nearby earthquake to the specified location.
- `/earthquakes/within?p=:top,:left,:bottom,:right/earthquakes/within?p=45.25,-95.25,35.25,-85.25`  
  Returns all earthquakes within a rectangle defined by the coordinates specified in the point parameter. The points should be: top latitude, left longitude, bottom latitude, right longitude.
- `/earthquakes/within?p=:lat,:lon&radius=:distance /earthquakes/within?p=44,-93&radius=25miles`  
  Returns all earthquakes within a circle with its center at the specified latitude/longitude point and a radius distance from that center. NOTE: This functionality is similar to the closest search, but does not include a distance or sorting. It is a faster query.
- `/earthquakes/us1000edqv`  
  Returns information on the earthquake with USGS id: us1000edqv

## `/fires`

- `/fires/closest?p=minneapolis,mn`  
  Return the active fires near Minneapolis, MN.
- `/fires/within?p=32.53156,-124.409591,42.009518,-114.131211`  
  Return the active fires within a bounding box surrounding California
- `/fires/search?query=state:ca`  
  Return the active fires that are within California
- `/fires/search?filter=hasperimeter&filter=geo`  
  Return only fires with perimeter and include the perimeter polygon.

## `/fires/outlook`

- `/fires/outlook/search?filter=firewx`  
  Return fire weather categorical outlooks for today. Since no **from** parameter provided, defaults to today.
- `/fires/outlook/search?filter=firewx&from=today`  
  Return fire weather categorical outlooks for today.
- `/fires/outlook/search?filter=firewx&from=+1day`  
  Return fire weather categorical outlooks for tomorrow.
- `/fires/outlook/search?filter=firewx,geo`  
  Return fire weather categorical outlooks for today and include the polygons for the outlooks.
- `/fires/outlook/search?filter=firewx&sort=code&from=today`  
  Return the fire weather categorical outlooks for today, sorted by the least significant to the highest.
- `/fires/outlook/search?filter=firewx&sort=code:-1&from=today`  
  Return the fire weather categorical outlooks for today, sorted by the highest significant to the lowest.
- `/fires/outlook/atlanta,ga`  
  Return the fire weather categorical outlooks for today that Atlanta, GA is contained in.  This query is equivalent to /fires/outlook/contains?p=atlanta,ga Note: The endpoint uses a default filter of "firewx" and from=today, since they were not included.
- `/fires/outlook/contains?p=atlanta,ga&filter=firewx`  
  Return the fire weather categorical outlooks for today that Atlanta, GA is contained in.
- `/fires/outlook/contains?p=44.96,-93.27&filter=firewx`  
  Return the fire weather categorical outlooks for today that contain the specified latitude/longitude
- `/fires/outlook/atlanta,ga?filter=firewx&from=today&to=+7days&sort=day`  
  Return the fire weather categorical outlooks for days 1 - 8 that Atlanta, GA is contained within. The results will be sorted by the coverage day
- `/fires/outlook/atlanta,ga?filter=firewx&from=today&to=+7days&sort=day&fields=details.range,details.risk.type`  
  Return the fire weather categorical outlooks for days 1 - 8 that Atlanta, GA is contained within. The results will be sorted by the coverage day. The fields parameter will limit the data to the elements needed. This greatly reduces bandwidth and resources.
- `/fires/outlook/ec31f2f9654addad2e4f773522f7b2c3`  
  Return the outlook with id of "ec31f2f9654addad2e4f773522f7b2c3"
- `/fires/outlook/ec31f2f9654addad2e4f773522f7b2c3?filter=geo`  
  Return the outlook with id of "ec31f2f9654addad2e4f773522f7b2c3" and include the polygon(s) data for the outlook
- `/fires/outlook/affects?p=ec31f2f9654addad2e4f773522f7b2c3&pop=50000&limit=10`  
  Return the top 10 locations with at least a population of 50,000 that are within the outlook with id "ec31f2f9654addad2e4f773522f7b2c3"

## `/forecasts`

- `/forecasts/55415`  
  Return 7 day forecast for the zip code 55415 (Minneapolis).
- `/forecasts/55415?limit=14`  
  Return 14 day forecast for the zip code 55415 (Minneapolis).
- `/forecasts/seattle,wa?filter=daynight`  
  Return 7 days of the day and night forecasts data for Seattle, WA.
- `/forecasts/seattle,wa?filter=daynight&limit=28`  
  Return up to 14 days of the day and night forecasts data for Seattle, WA.
- `/forecasts/seattle,wa?filter=3hr&limit=8`  
  Return the forecasts for the next eight 3-hour intervals for Seattle, WA.
- `/forecasts/seattle,wa?filter=1hr&limit=360`  
  Return up to 15 days of forecast in 1-hour intervals for Seattle, WA.
- `/forecasts/42.25,-95.25`  
  Return forecast data for the coordinate 42.25N, 95.25W.
- `/forecasts/minneapolis,mn?from=today&to=today`  
  Returns the forecast for today only for Minneapolis, MN.
- `/forecasts/minneapolis,mn?from=today&to=+1day&limit=2&filter=daynight`  
  Returns the day/night forecast for the next 24 hours for Minneapolis, MN.
- `/forecasts/minneapolis,mn?from=friday&to=+3days&filter=daynight`  
  Returns the day/night forecast for the weekend (Friday through Sunday) for Minneapolis, MN.

## `/hail/archive`

- `/hail/archive/minneapolis,mn?from=2024-06-05 16:00:00&to=2024-06-05 20:00:00`  
  Provides archive hail data for Minneapolis on June 5th, 2024 between 1600 and 2000 hours.
- `/hail/archive/norman,oklahoma?from=2025-06-01&to=+1day`  
  Provides hourly archive data for Norman, Oklahoma on 2025-06-01 starting at midnight for the next 24 hours.

## `/hail/threats`

- `/hail/threats/minneapolis,mn`  
  Returns hail threats that are currently, or in the near future, affecting Minneapolis.
- `/hail/threats/chico,tx?filter=test`  
  Return the sample data which encompasses Chico, TX.

## `/impacts/:activity`

- `/impacts/general/55403`  
  Provide the general impacts associated with the 55403 zip code.
- `/impacts/roadway_trucking/phoenix,az`  
  Provides weather risks catered to the trucking industry in Phoenix, AZ.

## `/indices/:type`

- `/indices/migraine/55403`  
  Provide the migraine index based on the latest observation.
- `/indices/migraine/55403?to=+5days`  
  Provide the migraine index based on the latest observation, and for the next 5 days.

## `/lightning`

- `/lightning/minneapolis,mn?radius=25miles&limit=100`  
  Return up to 100 recent cloud-to-ground lightning strikes within 25 miles of Minneapolis.
- `/lightning/minneapolis,mn?radius=25miles&limit=100&sort=dt:-1`  
  Return up to 100 recent cloud-to-ground lightning strikes within 25 miles of Minneapolis, sorting the results so newer strikes are first.
- `/lightning/minneapolis,mn?radius=25miles&limit=100&from=-5minutes`  
  Return up to 100 cloud-to-ground lightning strikes within 25 miles of Minneapolis that have occurred within the last 5 minutes.
- `/lightning/minneapolis,mn?filter=ic&limit=100&radius=25miles`  
  Return up to 100 intracloud (cloud-to-cloud) lighting pulses within 25 miles of Minneapolis.
- `/lightning/minneapolis,mn?filter=all&limit=100&radius=25miles`  
  Return up to 100 lightning pulses (cloud-to-ground and intracloud) within 25 miles of Minneapolis
- `/lightning/within?p=45.25,-95.25,35.25,-85.25&limit=5000`  
  Returns an lightning within the rectangle specified by the coords specified in `p` parameter. The points should be top latitude, left longitude, bottom latitude, right longitude. This feature requires the Lightning Enteprise Add-on.

## `/lightning/analytics`

- `/lightning/analytics/30.33,-101.60?limit=10`  
  Return up to 10 lightning strikes for the 30.33,-101.60 location.
- `/lightning/analytics/rocksprings,tx?&sort=peakamp:-1&limit=20`  
  Return up to 20 lightning strikes near Rocksprings, TX and sort by peakamp descending.
- `/lightning/analytics/within?p=45.25,-95.25,35.25,-85.25&limit=5000`  
  Returns an lightning within the rectangle specified by the coords specified in `p` parameter. The points should be top latitude, left longitude, bottom latitude, right longitude. This feature requires the Lightning Enteprise Add-on since it uses the `within` action.

## `/lightning/archive`

- `/lightning/archive/minneapolis,mn?radius=25miles&limit=100`  
  Return up to 100 recent cloud-to-ground lightning strikes within 25 miles of Minneapolis.
- `/lightning/archive/minneapolis,mn?radius=25miles&limit=100&sort=dt:-1`  
  Return up to 100 recent cloud-to-ground lightning strikes within 25 miles of Minneapolis, sorting the results so newer strikes are first.
- `/lightning/archive/minneapolis,mn?radius=25miles&limit=100&from=2021-07-01&to=+24hours`  
  Return up to 100 lightning strikes within 25 miles of Minneapolis, that occurred on July 1st, 2021.

## `/lightning/density`

- `/lightning/density/norman,ok`  
  Provides the lightning strike density for Norman, Oklahoma.

## `/lightning/flash`

- `/lightning/flash/Minneapolis,MN`  
  Return the closest lightning flash within 25 miles (~42km) of Minneapolis, MN that occurred with in the last 5 minutes.
- `/lightning/flash/Minneapolis,MN?radius=20km&limit=100`  
  Return up to the 100 closest lightning flashes within 20km of Minneapolis, MN that occurred with in the last 5 minutes.
- `/lightning/flash/Minneapolis,MN?radius=20km&limit=100&sort=dt:-1`  
  Return up to the 100 closest lightning flashes within 20km of Minneapolis, MN that occurred with in the last 5 minutes sorted by the date/time of the flash descending.
- `/lightning/flash/Minneapolis,MN?radius=20km&limit=100&from=-3minutes&to=now`  
  Return up to the 100 closest lightning flashes within 20km of Minneapolis, MN that occurred with in the last 3 minutes.
- `/lightning/flash/Minneapolis,MN?minradius=10km&radius=25km&limit=100`  
  Return up to the 100 closest lightning flashes that occurred within the 10km to 25km band from Minneapolis, MN that occurred with in the last 5 minutes.

## `/lightning/summary`

- `/lightning/summary`  
  Return a summary of all lightning strikes worldwide
- `/lightning/summary/atlanta,ga?radius=20miles&filter=cg`  
  Return a summary of all cloud-to-ground lightning strikes within a 20 mile radius of Atlanta, GA
- `/lightning/summary/atlanta,ga?radius=20miles&filter=cg&from=-5minutes&to=now`  
  Return a summary of all cloud-to-ground lightning strikes within a 20 miles radius of Atlanta, GA that occurred within the last 5 minutes.

## `/lightning/turbinerisk`

- `/lightning/turbinerisk/minneapolis,mn?height=100m`  
  Returns the lightning turbine risk at 100m height for Minneapolis, MN.

## `/maritime`

- `/maritime/0,0`  
  Returns the maritime forecast in hourly intervals for the next 24 hours for latitude/longitude 0,0
- `/maritime/0,0?for=now&to=now`  
  Returns the estimated maritime conditions for the current hour at latitude/longitude 0,0
- `/maritime/0,0?for=now&to=+48hours`  
  Returns the maritime forecast in hourly intervals for the next 48 hours for latitude/longitude 0,0
- `/maritime/0,0?for=now&to=+1week&filter=6hours`  
  Returns the maritime forecast in 6 hour intervals for the next 7 days for latitude/longitude 0,0

## `/maritime/archive`

- `/maritime/0,0`  
  Returns the maritime data for today in hourly intervals for latitude/longitude 0,0.
- `/maritime/0,0?from=2024-05-01`  
  Returns hourly maritime data for 2024-05-01 for latitude/longitude 0,0.
- `/maritime/0,0?from=yesterday&filter=3hr`  
  Returns 24 hours of maritime data for the latitude/longitude 0,0 in 3 hour intervals for yesterday.

## `/models/:model`

- `/models/nbm_conus/minneapolis,mn`  
  Returns NBM data for Minneapolis, MN.
- `/models/nbm_conus/minneapolis,mn?filter=skipnulls`  
  Returns NBM data for Minneapolis without any of the null values.

## `/models/catalog`

- `/models/catalog`  
  The response contains an array of model catalog objects. Each object describes one model instance and the run times and datasets available for it.

## `/normals`

- `/normals/minneapolis,mn`  
  Returns today's normals for the closest station to Minneapolis, MN.
- `/normals/usc00214884`  
  Returns today's normals for co-op station USC00214884.
- `/normals/55403?to=+1week`  
  Returns the next 7 days of normals for zip code 55403 (Minneapolis, MN).
- `/normals/closest?p=55403&limit=5`  
  Returns today's normals for the 5 closest stations to zip code 55403.
- `/normals/closest?p=55403&filter=hassnow`  
  Returns today's normals for the closest station to zip code 55403 that has snowfall information available.
- `/normals/closest?p=55403&limit=5&pfilter=monthly`  
  Returns the current month's summary for the 5 closest locations to zip code 55403.
- `/normals/minneapolis,mn?from=first%20day%20of%20june&to=last%20day%20of%20j`  
  Returns daily normals in Minneapolis, MN for each day of June by passing relevant parameters. For example, passing 'from=first day of june&to=last day of june' will need to be URL encoded as shown below.

## `/normals/stations`

- `/normals/stations/minneapolis,mn`  
  Return the information for the closest station to Minneapolis, MN.
- `/normals/stations/usc00214884`  
  Return the information for co-op station USC00214884.
- `/normals/stations/closest?p=55403&limit=5`  
  Return the information for the closest 5 stations to 55403.
- `/normals/stations/closest?p=55403&filter=hassnow`  
  Return the information for the closest station to 55403 that has snowfall information available.

## `/observations`

- `/observations/55403`  
  Returns data for zip code 55403.
- `/observations/KMSP`  
  Returns the observation for ICAO KMSP.
- `/observations/closest?p=45.25,-95.25`  
  Returns data for the closest observation to the location, specified. If no limit is specified, it defaults to a limit of 1.   If limit = 1, returns a single observation object, otherwise return an array of observation objects.
- `/observations/closest?p=55403&limit=5&radius=50mi`  
  Returns up to 5 observations within 50 miles of zip code 55403 (Minneapolis) . Results will be sorted by distance (ascending) from zip code 55403
- `/observations/closest?p=55403&query=wind:21.7`  
  Returns the closest observation to zip code 55403 (Minneapolis) with a wind speed of 21.7 knots (25 mph) or higher.
- `/observations/within?p=45.25,-95.25,35.25,-85.25`  
  Returns an observation within the rectangle specified by the coords specified in the loc. The points should be top latitude, left longitude, bottom latitude, right longitude. For more than one observation use the limit parameter.
- `/observations/within?p=45.25,-95.25&radius=50mi`  
  Returns an observation within a circle with a center at 45.25, -95.25 and a radius of 50 miles.  Note: This functionality is similar to the closest search but is faster as it does not include a distance or sorting.
- `/observations/within?p=45.25,-95.25,35.25,-85.25,40.5,-92.75,45.25,-95.25`  
  Returns an observation within a polygon specified by a series of comma separated latitude, longitude points. There must be 3 or more points specified.
- `/observations/within?p=45.25,-95.25,35.25,-85.25&limit=10`  
  Returns up to 10 observations within the rectangle specified with the top left corner of 45.25, -95.25 and the bottom right corner of 35.25, -85.25.
- `/observations/within?p=45.25,-95.25,35.25,-85.25&query=wind:21.7`  
  Returns an observation with a wind speed of 21.7knots (25mph) or higher, within the rectangle specified with the top left corner of 45.25, -95.25 and the bottom right corner of 35.25, -85.25.
- `/observations/search?query=id:KMSP&p=55403`  
  Returns the latest KMSP observation within a circle with a center at zip code 55403 (Minneapolis) and a radius of 50 miles (the default).  Note: This functionality is similar to the closest search, thus you can pass radius as needed.

## `/observations/archive`

- `/observations/archive/55403`  
  Returns archived data for zip code 55403.
- `/observations/archive/KMSP`  
  Returns the archived observation for ICAO KMSP.
- `/observations/archive/closest?p=45.25,-95.25`  
  Returns archived data for the closest observation to the specified location. If no limit is specified, it defaults to a limit of 1. If limit equals 1, return a single observation object, otherwise return an array of observation objects.
- `/observations/archive/closest?p=55403&limit=5&radius=50mi`  
  Returns up to 5 archived observations within 50 miles of zip code 55403 (Minneapolis). Results will be sorted by distance (ascending) from zip code 55403.
- `/observations/archive/closest?p=55403&query=wind:21.7`  
  Returns the closest archived observation to zip code 55403 (Minneapolis) with a wind speed of 21.7 knots (25 mph) or higher.
- `/observations/archive/within?p=45.25,-92.25,35.25,-85.25`  
  Returns all archived observations within the rectangle specified by the coords in the loc. The points should be top latitude, left longitude, bottom latitude, right longitude.
- `/observations/within?p=45.25,-95.25&radius=50mi`  
  Returns all archived observations within a circle with a center at 45.25, -95.25 and a radius of 50 miles.
- `/observations/archive/within?p=45.25,-95.25,35.25,-85.25,40.5,-92.75,45.25,-95.25`  
  Returns all archived observations within a polygon specified by a series of comma separated latitude, longitude points. There must be 3 or more points specified.

## `/observations/summary`

- `/observations/summary/KMSP`  
  Return the latest summary for ICAO KMSP.
- `/observations/summary/KMSP?from=yesterday`  
  Returns the daily summary for yesterday for ICAO KMSP.
- `/observations/summary/KMSP?from=-5days&plimit=5`  
  Returns the daily summaries for the last 5 days for ICAO KMSP.
- `/observations/summary/minneapolis,mn?from=yesterday`  
  Returns the daily summary for the closest observation station to Minneapolis, MN that at least reported temperature information.
- `/observations/summary/closest?p=55403&limit=5`  
  Return the current day summary for up to 5 observations near zip code 55403.
- `/observations/summary/closest?p=55403&psort=maxt:-1&&from=-1week`  
  Return the daily summary with the hottest temperature from the past week for the closest observation station to zip code 55403.

## `/phrases/summary`

- `/phrases/summary/minneapolis,mn`  
  Obtain the weather summary for Minneapolis, MN
- `/phrases/summary/minneapolis,mn?limit=3`  
  Obtain the weather summary for the next 3 hours instead of the default 6 hours.
- `/phrases/summary/toronto,canada`  
  Obtain the weather summary phrase for Toronto, Canada
- `/phrases/summary/51.50853,-0.12574`  
  Obtain the weather summary phrase for London, UK via a latitude / longitude combination
- `/phrases/summary/minneapolis,mn?radius=0.001mile`  
  Obtain the weather summary for Minneapolis, MN, but since the radius is so small, the phrase will be based on the next 6 hours of forecast only.
- `/phrases/summary/minneapolis,mn?filter=allstations`  
  Obtain the weather summary for Minneapolis, MN and pull any of observations stations types, including Personal Weather Stations, when generating the phrase.

## `/places`

- `/places/closest?p=45.25,-95.25`  
  Return the location closest to the coordinate 42.25N, 95.25W.
- `/places/closest?p=55403&limit=5&radius=50mi`  
  Return up to five places within 50 miles of zip code 55403 (Minneapolis). Results will be sorted by distance (ascending) from the specified zip code.
- `/places/search?query=name:seattle,state:wa`  
  Search for and returns data for Seattle, WA.
- `/places/search?query=name:^seat&limit=10`  
  Return up to 10 locations, with a name starting with "seat". The locations will be sorted by population descending.
- `/places/minneapolis,mn`  
  Return the location information for Minneapolis,MN
- `/places/paris,fr`  
  Return the location information for Paris, France
- `/places/paris,france`  
  Return the location information for Paris, France. Example of using the full country name.
- `/places/search?query=name:paris,country:fr`  
  Return the location information for Paris, France. Example using a search action.

## `/places/airports`

- `/places/airports/MSP`  
  Returns the airport information for Minneapolis - St Paul International Airport by using the 3 character IATA ID.
- `/places/airports/KROA`  
  Returns the airport information for Roanoke Regional Airport by using the 4 character ICAO ID.
- `/places/airports/closest/?p=minneapolis,mn&limit=5`  
  Returns the 5 closest airports of any size to downtown Minneapolis, MN.
- `/places/airports/closest/?p=minneapolis,mn&limit=5&radius=200miles&filter=largeairport`  
  Returns up to 5 of the closest larger airports within a 200 mile radius of Minneapolis, MN.

## `/places/postalcodes`

- `/places/postalcodes/55403`  
  Look up US zip code 55403. (Minneapolis, MN)
- `/places/postalcodes/M4B 1B3`  
  Look up Canadian postal code.
- `/places/postalcodes/M4B1B3`  
  Look up Canadian postal code, note the space after the first three characters is optional.
- `/places/postalcodes/closest?p=42.95,-95.25`  
  Return the location closest US zip code (based on zip code centroid) to the coordinate 42.25N, 95.25W.
- `/places/postalcodes/closest?p=43.65,-76.92&filter=canada`  
  Find the closest Canadian postal code to the coordinate 43.65, -76.92.

## `/renewables/irradiance/summary`

- `https://data.api.xweather.com/renewables/irradiance/summary/stockholm,se?filter=climatologyMonth,ghi`  
  This provides the global horizontal irradiance summary for Stockholm over the last calendar month.

## `/rivers`

- `/rivers/houston,tx?limit=10`  
  Return observations for up to 10 gauges near Houston, Texas.
- `/rivers/houston,tx?filter=allflood&limit=10`  
  Return observations for up to 10 gauges near Houston, Texas that are reporting flood stage
- `/rivers/search?query=state:tx&filter=minor&limit=50`  
  Return observations for up to 50 gauges within the state of Texas that are reporting minor flooding

## `/rivers/gauges`

- `/rivers/gauges/houston,tx?limit=10`  
  Return the 10 closest gauges to Houston, TX
- `/rivers/gauges/houston,tx?limit=10&filter=impacts`  
  Return the 10 closest gauges to Houston, TX that include flood impact information

## `/roadweather`

- `/roadweather/44.9648,-93.2682`  
  Returns the road weather information for a road within 100meters of the specified latitude/longitude. Since no filter is provided, the API will return data for the nearby primary road if one is nearby. Alternatively, it will fall back to a secondary road if one is nearby.
- `/roadweather/44.9648,-93.2682?filter=primary`  
  Returns the road weather information for a primary road within 100 meters of the specified latitude/longitude.
- `/roadweather/44.9648,-93.2682?filter=secondary`  
  Returns the road weather information for a secondary road within 100 meters of the specified latitude/longitude.

## `/roadweather/analytics`

- `/roadweather/44.9648,-93.2682`  
  Returns the road weather information for a road within 100meters of the specified latitude/longitude. Since no filter is provided, the API will return data for the nearby primary road if one is nearby. Alternatively, it will fall back to a secondary road if one is nearby.
- `/roadweather/44.9648,-93.2682?filter=primary`  
  Returns the road weather information for a primary road within 100 meters of the specified latitude/longitude.
- `/roadweather/44.9648,-93.2682?filter=secondary`  
  Returns the road weather information for a secondary road within 100 meters of the specified latitude/longitude.

## `/roadweather/conditions`

- `/roadweather/44.9648,-93.2682`  
  Returns the road weather information for a road within 100meters of the specified latitude/longitude. Since no filter is provided, the API will return data for the nearby primary road if one is nearby. Alternatively, it will fall back to a secondary road if one is nearby.
- `/roadweather/44.9648,-93.2682?filter=primary`  
  Returns the road weather information for a primary road within 100 meters of the specified latitude/longitude.
- `/roadweather/44.9648,-93.2682?filter=secondary`  
  Returns the road weather information for a secondary road within 100 meters of the specified latitude/longitude.

## `/stormcells`

- `/stormcells/mpx_i9`  
  Returns data for a specific storm cell. In this case Storm Cell ID I9 as reported by Radar station MPX. Returns a single object containing the storm cell information. If no storm cell, then an empty object is returned along with an error code of no data.
- `/stormcells/closest?p=45.25,-95.25`  
  Returns closest single storm cell to the specified point. Result is an array. Empty if no close storm cells.
- `/stormcells/closest?p=55403&limit=5&radius=50mi`  
  Returns up to 5 storms cells within 50 miles of zip code 55403 (Minneapolis). Storm cells will be sorted by distance (ascending) from zip code 55403.
- `/stormcells/closest?p=55403&query=tvs`  
  Returns up to 1 storm cell within 50 miles of zip code 55403 that has a value for “ob.tvs” greater than 0.
- `/stormcells/closest?p=55403&query=hail:70&limit=0`  
  Return all storm cells within 50 miles of zip code 55403 that have a 70%+ probability of hail. Results will be sorted by distance.
- `/stormcells/closest?p=55403&query=hail:70,hail.size:.5:2&limit=0`  
  Return all storm cells within 50 miles of zip code 55403 that have a 70%+ probability of hail with a hail size between .5 and 2 inches. Results sorted by distance.
- `/stormcells/within?p=45.25,-95.25,35.25,-85.25&limit=10`  
  Returns up to 10 storm cells within the rectangle specified with the top left corner of 45.25,-95.25 and the bottom right corner of 35.25,-85.25.
- `/stormcells/within?p=45.25,-95.25,35.25,-85.25&query=ob.tvs`  
  Returns all storm cells that have an 'ob.tvs' value greater than 0 (meaning a tornadic storm cell) within the rectangle specified with the top left corner of 45.25,-95.25 and the bottom right corner of 35.25,-85.25.
- `/stormcells/within?p=45.25,-95.25,35.25,-85.25&filter=tornado,hail`  
  Returns storm cells that show hail and tornadic characteristics within the rectangle specified with the top left corner of 45.25,-95.25 and the bottom right corner of 35.25,-85.25.
- `/stormcells/affects?p=DMX_CO&limit=50`  
  Returns up to 50 cities within the forecast path of stormcell DMX_CO
- `/stormcells/affects?p=DMX_CO&limit=50&pop=50000`  
  Returns up to 50 cities with a population of 50,000 or greater that are within the forecast path of stormcell DMX_CO

## `/stormcells/summary`

- `/stormcells/summary`  
  Return a summary for all storm cells
- `/stormcells/summary/search?filter=conus`  
  Return a summary for only storm cells within the Continental US
- `/stormcells/summary/search?query=state:ga`  
  Return a summary for only storm cells within the state of Georgia.
- `/stormcells/summary/search?query=state:ga;state:al`  
  Return a summary for storm cells that are within the states of Georgia or Alabama.  **Note:** the semicolon is used to represent a logical 'OR'.
- `/stormcells/summary/minneapolis,mn`  
  Return a summary for storm cells within a 50 mile radius of Minneapolis, MN
- `/stormcells/summary/55403?radius=100miles`  
  Return a summary for storm cells within a 100 mile radius of zip code 55403 (Minneapolis, MN)
- `/stormcells/summary/search?filter=conus,hail`  
  Return a summary for storm cells within the Continental US and have a high probability of having hail.
- `/stormcells/summary/search?filter=hail,tornado`  
  Return a summary for storm cells that have a high probability of having hail and contain a tornadic vortex signature (TVS) as determined by NEXRAD radar. **Note:** the comma is used to represent a logical 'AND', meaning only use storm cells that meet both criteria.
- `/stormcells/summary/search?filter=hail;tornado`  
  Return a summary for storm cells that have a high probability of having hail or contain a tornadic vortex signature (TVS) as determined by NEXRAD radar. **Note** the semicolon is used to represent a logical 'OR', meaning only use storm cells that meet both criteria.
- `/stormcells/summary/search?filter=hail,geo`  
  Return a summary for storm cells that have a high probability of having hail. Additionally include the polygons of the storm cell groups.
- `/stormcells/summary/search?filter=threat`  
  Return a summary for storm cells that are threatening in nature.
- `/stormcells/summary/affects?filter=threat&query=state:ga,pop:50000&limit=10`  
  Return up to 10 locations with a population of 50,000 or higher within the state of Georgia, that are currently being affected or within the path of threatening storm cells.
- `/stormcells/summary/affects?filter=threat,noforecast&query=state:ga,pop:50000&limit=10`  
  Return up to 10 locations with a population of 50,000 or higher within the state of Georgia, that are within the immediate vicinity (ignoring storm cell forecasts) of threatening storm cells.

## `/stormreports`

- `/stormreports/minneapolis,mn?from=-24hours&limit=10`  
  Returns the latest 10 storm reports near Minneapolis that were reported within the last 24 hours.
- `/stormreports/51dc1b0e3a751ea17000017c`  
  Returns the storm report information for the storm report with the ID '51dc1b0e3a751ea17000017c'.
- `/stormreports/minneapolis,mn?from=-1year&filter=wind&limit=100`  
  Returns the latest 100 wind related storm reports near Minneapolis that were reported within the last year.
- `/stormreports/within?p=59.3534,-122.9738,25.7960,-63.5597&limit=500&from=-24hours&to=now`  
  Returns up to the latest 500 storm reports within a bounding box that occurred within the past 24 hours. Perfect usage for fetching storm reports to display on an interactive map.

## `/stormreports/summary`

- `/stormreports/summary`  
  Return summary for all storm reports received today
- `/stormreports/summary/search?query=state:ga`  
  Return a summary for only storm reports today within the state of Georgia.
- `/stormreports/summary/search?query=state:ga;state:al`  
  Return a summary for storm reports that are within the states of Georgia or Alabama.   **Note:** the semicolon is used to represent a logical 'OR'.
- `/stormreports/summary/minneapolis,mn`  
  Return a summary for storm reports within a 50 mile radius of Minneapolis, MN today.
- `/stormreports/summary?from=-1week&to=now`  
  Return a summary for all storm reports received over the past week.
- `/stormreports/summary?filter=tornado`  
  Return a summary for all tornado, funnel cloud and waterspout related storm reports
- `/stormreports/summary?filter=tornado&from=-1week&to=now`  
  Return a summary for all tornado, funnel cloud and waterspout related storm reports over the past week
- `/stormreports/summary?filter=tornado&from=2016-08-17&to=+1day`  
  Return a summary for all tornado, funnel cloud and waterspout related storm reports on Aug 17, 2016 (UTC)
- `/stormreports/summary?filter=rain;snow`  
  Return a summary of rain and snow related storm reports today.  **Note:** the semicolon is used to represent a logical 'OR'.

## `/sunmoon`

- `/sunmoon/minneapolis,mn`  
  Obtain the sun/moon information for today for Minneapolis, MN.
- `/sunmoon/minneapolis,mn?from=now&to=+1week&limit=7`  
  Obtain the next weeks information for Minneapolis, MN.
- `/sunmoon/minneapolis,mn?from=2012-01-01&to=2012-01-31&limit=31`  
  Obtain the sun/moon information for Minneapolis, MN for the month of January, 2012.
- `/sunmoon/10001?filter=sun,moon`  
  Obtain only the sunrise/set and moon rise/set information for New York. Excludes the twilight and moon phase information.

## `/sunmoon/moonphases`

- `/sunmoon/moonphases?limit=4`  
  Fetch the next four moon phases, with times in UTC.
- `/sunmoon/moonphases/minneapolis,mn?limit=4`  
  Fetch the next four moon phases, with times localized to Minneapolis, MN.
- `/sunmoon/moonphases/minneapolis,mn?from=2012-01-01&to=2012-12-31&limit=100`  
  Fetch the moon phases for the all of 2012, with times localized to Minneapolis, MN.
- `/sunmoon/moonphases/search?query=type:new&limit=4`  
  Fetch the next four new moons, with times in UTC.
- `/sunmoon/moonphases/search?query=type:new;type:full&limit=4`  
  Fetch the next four new or full moons, with times in UTC.

## `/threats`

- `/threats/minneapolis,mn`  
  Find the threats affecting Minneapolis, MN
- `/threats/55403?radius=200miles`  
  Find the threats within a 200 mile radius that may affect zip code 55403 (Minneapolis, MN)

## `/tides`

- `/tides/miami,fl`  
  Return today's predicted tides for the closest tide location to Miami, FL.
- `/tides/miami,fl?to=+1week`  
  Return the next week of predicted tides for the closest tide location to Miami, FL.
- `/tides/8723165`  
  Return the today's predicted tides for tide location with id '8723165'.
- `/tides/closest?p=miami,fl&limit=5`  
  Return today's predicted tides for the 5 closest tide locations to Miami, Fl.
- `/tides/closest?p=miami,fl&limit=5&plimit=1`  
  Return the next predicted tide today, for the 5 closest tide locations to Miami, Fl. Here, plimit=1 limits the tides in the periods section of each station object.

## `/tides/stations`

- `/tides/stations/miami,fl`  
  Return the information for the closest station to Miami, FL.
- `/tides/stations/8723165`  
  Return the information for the closest station to tide location with id '8723165'.
- `/tides/stations/closest?p=miami,fl&limit=5`  
  Return the information for the closest 5 stations to Miami, FL.

## `/tropicalcyclones`

- `/tropicalcyclones`  
  Return the currently active tropical systems
- `/tropicalcyclones?filter=al`  
  Return the currently active tropical systems within the Atlantic basin
- `/tropicalcyclones?filter=al;ep;cp`  
  Return the currently active tropical cyclones that are in the atlantic or eastern pacific or the central pacific basins. Note that a semicolon separator is used to denote a logical OR.
- `/tropicalcyclones?filter=al&filter=geo`  
  Return the currently active tropical systems within the Atlantic basin and include the error cone information.
- `/tropicalcyclones/2017-AL-16`  
  Return information on tropical system with ID 2017-AL-16 (Hurricane Nate)
- `/tropicalcyclones/miami,fl?radius=300miles`  
  Return information on currently active tropical systems that are currently located within 300 miles of Miami, Florida
- `/tropicalcyclones/?filter=invests`  
  Return information on the active Invests. Invests are areas under investigation for potential future tropical development.
- `/tropicalcyclones/?filter=invests,al`  
  Return information on the active Invests within the atlantic.

## `/tropicalcyclones/archive`

- `/tropicalcyclones/archive/search?filter=al&limit=20`  
  Return up to 20 tropical cyclones that occurred in the Atlantic basin over the past year (the default if no from/to provided)
- `/tropicalcyclones/archive/2017-AL-16`  
  Return information on tropical system with ID 2017-AL-16 (Hurricane Nate)
- `/tropicalcyclones/archive/miami,fl?radius=300miles&from=-5years&to=now&limit=10`  
  Return information on up to 10 tropical systems that tracked within 300 miles of Miami, FL over the past 5 years.
- `/tropicalcyclones/archive/miami,fl?radius=300miles&filter=track&query=year:1992:1992`  
  Return information on all tropical systems that the historic track came within 300 miles of Miami, Florida during the 1992 tropical season.
- `/tropicalcyclones/archive/search?query=year:2017:2017&sort=maxwindspeed:-1&limit=1`  
  Return information on the tropical system that had the maximum winds reported in the 2017 tropical season, as reported by the NHC or JTWC.

## `/xcast/forecasts`

- `/xcast/forecasts/{xcast_device_id}`  
  Returns hourly forecast data based on your specific Xcast device ID provided.
- `/xcast/forecasts/helsinki,fi`  
  Returns hourly forecast data for Helsinki, FI.
- `/xcast/forecasts/seattle,wa?filter=10min`  
  Returns subhourly forecast data for Seattle, WA in 10 minute intervals.
