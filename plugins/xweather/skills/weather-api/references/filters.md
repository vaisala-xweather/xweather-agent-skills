# Filter and query-property meanings, by endpoint

`filter=` selects *which* records / intervals come back; `query=` filters on record values
(see `parameters.md` → Advanced queries for the operator syntax). Multiple filters are combined
with `,` for AND and `;` for OR.

Only endpoints that document filters or query properties appear here. For the complete token list
per endpoint — including endpoints with no prose descriptions — see `endpoints.md`.

---

## `/airquality`

**Filters**

- `airnow` — Default - Utilize the US EPA AirNow AQI categories and calculations.
- `cai` — Utilize the South Korean Comprehensive Air-quality Index (CAI) categories and calculations in place of the default AirNow categories.
- `caqi` — Utilize the CAQI (Common Air Quality Index) categories and calculations, in place of the default AirNow categories.
- `china` — Utilize the Chinese Government AQI categories, in place of the default AirNOW categories  For more information on various Air Quality Index standards, please visit the wiki page.
- `eaqi` — Utilize the EAQI (European Air Quality Index) categories and calculations, in place of the default AirNow categories.
- `germany` — Utilize the German categories and calculations in place of the default AirNow categories.
- `india` — Utilize the India AQI categories in place of the default AirNOW categories  For more information on various Air Quality Index standards, please visit the wiki page.
- `uk` — Utilize the UK categories and calculations in place of the default AirNow categories. Please visit the wiki page.

## `/airquality/archive`

**Filters**

- `#hr` — Returns forecast air quality information for the specified interval starting at the locale's current time. Supports values: 1hr, 2hr, 3hr, 4hr, 6hr, 12hr, 24hr.  Default behavior is 1hr
- `airnow` — (default) Utilize the US EPA AirNow AQI categories and calculations.      Name  Range  Color      Good  0 - 50  #00E400      Moderate  51 - 100  #FFFF00      Unhealthy for Sensitive Groups  101 - 150  #FF7E00      Unhealthy  151 - 200  #FF0000      Very Unhealthy  201 - 300  #8F3F97      Hazardous  301 - 500  #7E0023
- `cai` — Utilize the South Korean Comprehensive Air-quality Index (CAI) categories and calculations in place of the default AirNow categories.      Name  Range  Color      Good  0 - 50  #0000FF      Moderate  51 - 100  #00FF00      Unhealthy  101 - 250  #FFFF00      Very Unhealthy  251 - 500  #FF0000
- `caqi` — Utilize the CAQI (Common Air Quality Index) categories and calculations, in place of the default AirNow categories.      Name  Range  Color      Very Low  0 - 25  #79BC6A      Low  26 - 50  #BBCF4C      Medium  51 - 75  #EEC20B      High  76 - 100  #F29305      Very High  101 - 200  #E8416F
- `china` — Utilize the Chinese Government AQI categories, in place of the default AirNOW categories      Name  Range  Color      Excellent  0 - 50  #00FF00      Good  51 - 100  #FFFF00      Lightly Polluted  101 - 150  #FF9900      Moderately Polluted  151 - 200  #FF0000      Heavily Polluted  201 - 300  #540099      Severely Polluted  301 - 500  #800000     For more information on various Air Quality Index standards, please visit the wiki page.
- `eaqi` — Utilize the EAQI (European Air Quality Index) categories and calculations, in place of the default AirNow categories.      Name  Range  Color      Good  0 - 25  #50F0E6      Fair  26 - 50  #50CCAA      Moderate  51 - 75  #F0E641      Poor  76 - 100  #FF5050      Very Poor  101 - 125  #960032      Extremely Poor  126 - 150  #7D2181
- `germany` — Utilize the German categories and calculations in place of the default AirNow categories.      Name  Range  Color      Very Good  0 - 25  #50F0E6      Good  26 - 50  #50CCAA      Moderate  51 - 75  #F0E641      Poor  76 - 100  #FF5050      Very Poor  125  #960032
- `india` — Utilize the India AQI categories, in place of the default AirNOW categories      Name  Range  Color      Good  0 - 50  #00CC00      Satisfactory  51 - 100  #66CC00      Moderate  101 - 200  #FFFF00      Poor  201 - 300  #FF9900      Severe  301 - 400  #FF0000      Hazardous  401 - 500  #A52A2A     For more information on various Air Quality Index standards, please visit the wiki page.
- `uk` — Utilize the UK categories and calculations in place of the default AirNow categories.       Name  Range  Color      Low  1  #009900      Moderate  2 - 4  #FF9900      High  5 - 7  #FF0000      Very High  8 - 10  #990099     For more information on various Air Quality Index standards, please visit the wiki page.

## `/airquality/forecasts`

**Filters**

- `day` — (default) Returns daily forecast air quality information
- `daynight` — Returns forecast data in a daily 12-hour format in which day and night forecasts are separated.
- `#hr` — Returns forecast air quality information for the specified interval starting at the locale's current time. Supports values: 1hr, 2hr, 3hr, 4hr, 6hr, 12hr, 24hr.
- `airnow` — Default - Utilize the US EPA AirNow AQI categories and calculations.  NameRangeColorGood0 - 50#00E400Moderate51 - 100#FFFF00Unhealthy for Sensitive Groups101 - 150#FF7E00Unhealthy151 - 200#FF0000Very Unhealthy201 - 300#8F3F97Hazardous301 - 500#7E0023
- `cai` — Utilize the South Korean Comprehensive Air Quality Index (CAI) categories and calculations in place of the default AirNow categories.  NameRangeColorGood0 - 50#0000FFModerate51 - 100#00FF00Unhealthy101 - 250#FFFF00Very Unhealthy251 - 500#FF0000
- `caqi` — Utilize the CAQI (Common Air Quality Index) categories and calculations, in place of the default AirNow categories.  NameRangeColorVery Low0 - 25#79BC6ALow26 - 50#BBCF4CMedium51 - 75#EEC20BHigh76 - 100#F29305Very High101 - 200#E8416F
- `china` — Utilize the Chinese Government AQI categories, in place of the default AirNOW categories  NameRangeColorExcellent0 - 50#00FF00Good51 - 100#FFFF00Lightly Polluted101 - 150#FF9900Moderately Polluted151 - 200#FF0000Heavily Polluted201 - 300#540099Severely Polluted301 - 500#800000   For more information on various Air Quality Index standards, please visit the wiki page.
- `eaqi` — Utilize the EAQI (European Air Quality Index) categories and calculations, in place of the default AirNow categories.  NameRangeColorGood0 - 25#50F0E6Fair26 - 50#50CCAAModerate51 - 75#F0E641Poor76 - 100#FF5050Very Poor101 - 125#960032Extremely Poor126 - 150#7D2181
- `germany` — Utilize the German categories and calculations in place of the default AirNow categories.  NameRangeColorVery Good0 - 25#50F0E6Good26 - 50#50CCAAModerate51 - 75#F0E641Poor76 - 100#FF5050Very Poor125#960032
- `india` — Utilize the India AQI categories, in place of the default AirNOW categories  NameRangeColorGood0 - 50#00CC00Satisfactory51 - 100#66CC00Moderate101 - 200#FFFF00Poor201 - 300#FF9900Severe301 - 400#FF0000Hazardous401 - 500#A52A2A   For more information on various Air Quality Index standards, please visit the wiki page.
- `uk` — Utilize the UK categories and calculations in place of the default AirNow categories.   NameRangeColorLow1#009900Moderate2 - 4#FF9900High5 - 7#FF0000Very High8 - 10#990099   For more information on various Air Quality Index standards, please visit the wiki page.

## `/alerts`

**Filters**

- `standard` — (Default). Returns all alerts issued as a warning, watch, or advisory.   Statements and outlooks are not returned by default, though available via the `all` filter or the individual alert type filters.
- `warning` — Returns all warnings.  A warning is issued when a hazardous weather or hydrologic event is occurring, imminent, or likely. A warning means weather conditions pose a threat to life or property. People in the path of the storm need to take protective action.
- `watch` — Returns all watches.  A watch is used when the risk of a hazardous weather or hydrologic event has increased significantly, but its occurrence, location, or timing is still uncertain. It is intended to provide enough lead time so those who need to set their plans in motion can do so. A watch means that hazardous weather is possible. People should have a plan of action in case a storm threatens and they should listen for later information and possible warnings especially when planning travel or outdoor activities.
- `advisory` — Returns all alerts.  An advisory is issued when a hazardous weather or hydrologic event is occurring, imminent, or likely. Advisories are for "less serious" conditions than warnings that may cause significant inconvenience, and if caution is not exercised could lead to situations that may threaten life or property.
- `outlook` — Returns all outlooks.  An outlook is issued daily to indicate that a hazardous weather or hydrologic event may occur in the next several days. The outlook will include information about potential severe thunderstorms, heavy rain or flooding, winter weather, extremes of heat or cold, etc., that may develop over the next 7 days with an emphasis on the first 24 hours of the forecast. It is intended to provide information to those who need considerable lead time to prepare for the event.
- `statement` — Returns all special weather statements. This is typically used when the NWS needs to communicate a non-threatening message, but their message does not fall into the other categories (warning, advisory, outlook, etc.).
- `severe` — Returns all severe-related alerts: - severe thunderstorm - tornado
- `flood` — Returns all flood/hydro-related alerts: - debris flow - flood, flash flood - hydrologic
- `tropical` — Returns all tropical-related alerts: - tropical storm, hurricane, typhoon - tropical storm wind - hurricane wind - extreme wind
- `winter` — Returns all winter-related alerts: - blizzard, winter storm, winter weather - snow, heavy snow - lake effect snow - snow and blowing snow - ice pellets, freezing rain, ice storm - wind chill
- `marine` — Returns all marine/coastal-related alerts: - marine - freezing spray, heavy freezing spray - small craft - small craft for winds - small craft for hazardous seas - small craft for rough bar - gale - hazardous seas - hurricane force winds - lakeshore flood - coastal flood, high surf - tsunami - low water - dense fog, dense smoke, ashfall (marine)
- `nonprecip` — Returns all non-precipitation-related alerts: - blowing dust/dust storm - wind, high wind, lake wind - dense smoke - dense fog, freezing fog - freeze, frost - heat, excessive heat, extreme cold
- `forecast` — Returns forecasts, normally short-term forecasts.
- `all` — Return all warnings, watches, advisories, statements, outlooks and forecasts.
- `wind` — Returns wind-related alerts.
- `fire` — Returns fire-related alerts.
- `tsunami` — Returns tsunami-related alerts.
- `now` — Returns short term forecast alerts as defined by the National Weather Service.
- `synopsis` — Returns a synopsis of the alerts.
- `tornado` — Returns tornado related alerts (Tornado watches/warnings)
- `emergency` — Returns emergency-specific alerts.
- `hassmallpoly` — Returns alerts that have a small polygon (US severe thunderstorm, tornado, flash flood etc)
- `distinct` — Returns only a single copy of a an alert issued for multiple locations.
- `county` — Ignores small polygons within alerts and will return alerts issued for the county or weather zone. USA Only
- `nonmarine` — Returns all warnings, watches, and advisories that are not marine related.
- `geo` — Instructs the API to return the associated polygon with the alert output. Within the US, if the alert has a small polygon, this will be returned, otherwise the county or weather zone the alert was issued for will be returned. Within Canada the polygon will represent the Canadian Location Code (CLC) the alert is issued for. Within Europe the polygon will match the alert polygon as issued by MeteoAlarm. Please note, this feature will only work with a Premium subscription and reduces the maximum limit to 50 results due to the amount of data.

**Query properties**

- `type` — Used to query the alert type. The value should be set to the VTEC Code or the WMO if no VTEC code exists. Review the list of allowed Alert Types.  Examples: /alerts/minneapolis,mn?query=type:TO.W will return only the tornado warnings /alerts/minneapolis,mn?query=type:TO.W;type:NOW will return tornado warnings and short-term forecasts
- `loc` — Used to query by the zone id the alert is issued for. Normally will be a NOAA public weather zone that looks similar to VAZ014 or if issued for a specific county: VAC023. For Canadian alerts, the code will look similar to CLC-086420.
- `sig` — Used to query by the one character coded significance of an alert type. W = Warning A = Watch Y = Advisory S = Statement O = Outlook F = Forecast  Examples: /alerts/minneapolis,mn?query=sig:W;sig:A (returning alerts for Minneapolis, MN that are warnings or watches)
- `sigp` — Used to query by the numeric representation of an alert type. A lower number has higher significance. 1 = Warning 3 = Watch 5 = Advisory 7 = Statement 9 = Forecast (Short term) 11 = Outlook  Examples: /alerts/minneapolis,mn?query=sigp:1;sigp:3 (returns only warnings or watches for Minneapolis, MN)
- `name` — County name or weather zone name (lowercase) of the location the alert has been issued for.
- `active` — Used to query active or inactive alerts.  0 = not active 1 = active By default, the API will not return inactive alerts  Examples: /alerts/minneapolis,mn?query=active:0:0 (returns only alerts that are no longer active for Minneapolis, MN)
- `emergency` — Used to query emergency specific alerts, such as tornado emergencies. true = emergency specific alerts false = non emergency specific alerts
- `id` — Used to query by an alert ID.
- `issued` — Used to query alerts based on the issued time. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=issued:-10minutes&limit=100 (returns alerts issued within the past 10 minutes for Minneapolis, MN)
- `begins` — Used to query alerts based on the begins time of the alert. Some alerts such as winter storm warnings may be issued now, but do not go into effect until several hours later. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=begins:-6hours:6hours&limit=100 (returns active alerts that either went into effect in the past six hours or are set to go live in the next 6 hours for Minneapolis, MN)
- `expires` — Used to query alerts based on the expiration time. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=expires:now:10minutes&limit=100 (returns alerts set to expire within the next 10 minutes for Minneapolis, MN)
- `added` — Used to query alerts based on the time they were added to the API database. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=added:-10minutes&limit=100 (returns alerts received and added within the last 10 minutes for Minneapolis, MN)

## `/alerts/summary`

**Filters**

- `warning` — Returns all warnings.  A warning is issued when a hazardous weather or hydrologic event is occurring, imminent, or likely. A warning means weather conditions pose a threat to life or property. People in the path of the storm need to take protective action.
- `watch` — Returns all watches.  A watch is used when the risk of a hazardous weather or hydrologic event has increased significantly, but its occurrence, location, or timing is still uncertain. It is intended to provide enough lead time so those who need to set their plans in motion can do so. A watch means that hazardous weather is possible. People should have a plan of action in case a storm threatens and they should listen for later information and possible warnings especially when planning travel or outdoor activities.
- `advisory` — Returns all alerts.  An alert is issued when a hazardous weather or hydrologic event is occurring, imminent, or likely. Alerts are for "less serious" conditions than warnings that may cause significant inconvenience, and if caution is not exercised could lead to situations that may threaten life or property.
- `outlook` — Returns all outlooks.  An outlook is issued daily to indicate that a hazardous weather or hydrologic event may occur in the next several days. The outlook will include information about potential severe thunderstorms, heavy rain or flooding, winter weather, extremes of heat or cold, etc., that may develop over the next 7 days with an emphasis on the first 24 hours of the forecast. It is intended to provide information to those who need considerable lead time to prepare for the event.
- `statement` — Returns all special weather statements.
- `severe` — Returns all severe-related alerts: - severe thunderstorm - tornado
- `flood` — Returns all flood/hydro-related alerts: - debris flow - flood, flash flood - hydrologic
- `tropical` — Returns all tropical-related alerts: - tropical storm, hurricane, typhoon - tropical storm wind - hurricane wind - extreme wind
- `winter` — Returns all winter-related alerts: - blizzard, winter storm, winter weather - snow, heavy snow - lake effect snow - snow and blowing snow - ice pellets, freezing rain, ice storm - wind chill
- `marine` — Returns all marine/coastal-related alerts: - marine - freezing spray, heavy freezing spray - small craft - small craft for winds - small craft for hazardous seas - small craft for rough bar - gale - hazardous seas - hurricane force winds - lakeshore flood - coastal flood, high surf - tsunami - low water - dense fog, dense smoke, ashfall (marine)
- `nonprecip` — Returns all non-precipitation-related alerts: - blowing dust/dust storm - wind, high wind, lake wind - dense smoke - dense fog, freezing fog - freeze, frost - heat, excessive heat, extreme cold
- `forecast` — Returns forecasts, normally short-term forecasts.
- `all` — Return all warnings, watches, advisories, statements, outlooks and forecasts.
- `wind` — Returns wind-related alerts.
- `fire` — Returns fire-related alerts.
- `tsunami` — Returns tsunami-related alerts.
- `now` — Returns alerts that are currently in effect.
- `synopsis` — Returns a synopsis of the alerts.
- `tornado` — Returns tornado related alerts (Tornado watches/warnings)
- `emergency` — Returns emergency-specific alerts.
- `canada` — Returns only Canadian alerts. Equivalent to query=country:ca
- `usa` — Returns only USA alerts. Equivalent to query=country:us
- `allcountries` — Returns alerts for all countries (the default).
- `hassmallpoly` — Returns alerts that have a small polygon (US severe thunderstorm, tornado, flash flood etc)
- `distinct` — Returns a summary based on counting alerts issued for multiple locations once.
- `nonmarine` — Returns all warnings, watches, and alerts that are not marine related.

**Query properties**

- `type` — Used to query the alert type. The value should be set to the VTEC Code or the WMO if no VTEC code exists. Review the list of allowed Alert Types.  Examples: /alerts/minneapolis,mn?query=type:TO.W will return only the tornado warnings /alerts/minneapolis,mn?query=type:TO.W;type:NOW will return tornado warnings and short-term forecasts
- `wxzone` — Used to query by the zone id the alert is issued for. Normally will be a NOAA public weather zone that looks similar to: VAZ014 or if issued for a specific county : VAC023
- `sig` — Used to query by the one character coded significance of an alert type. W = Warning A = Watch Y = Advisory S = Statement O = Outlook F = Forecast  Examples: /alerts/minneapolis,mn?query=sig:W,sig:A (returns only warnings and alerts for Minneapolis, MN)
- `sigp` — Used to query by the numeric representation of an alert type. A lower number has higher significance. 1 = Warning 3 = Watch 5 = Advisory 7 = Statement 9 = Forecast (Short term) 11 = Outlook  Examples: /alerts/minneapolis,mn?query=sigp:1:3 (returns only warnings and alerts for Minneapolis, MN)
- `name` — County name or weather zone name (lowercase) of the location the alert has been issued for.
- `issued` — Used to query by the date the alert is issued for.
- `expires` — Used to query by the date the alert is scheduled to expire.
- `active` — Used to query active or inactive alerts.  0 = not active 1 = active By default the API will not return inactive alerts  Examples: /alerts/minneapolis,min?query=active:0:0 (returns only alerts that are no longer active for Minneapolis, MN)
- `emergency` — Used to query emergency specific alerts, such as tornado emergencies. true = emergency specific alerts false = non emergency specific alerts
- `issued` — Used to query alerts based on the issued time. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=issued:-10minutes&limit=100 (returns alerts issued within the past 10 minutes for Minneapolis, MN)
- `begins` — Used to query alerts based on the begins time of the alert. Some alerts such as winter storm warnings may be issued now, but do not go into effect until several hours later. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=begins:-6hours:6hours&limit=100 (returns active alerts that either went into effect in the past six hours or are set to go live in the next 6 hours for Minneapolis, MN)
- `expires` — Used to query alerts based on the expiration time. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=expires:now:10minutes&limit=100 (returns alerts set to expire within the next 10 minutes for Minneapolis, MN)
- `added` — Used to query alerts based on the time they were added to the API database. Values can be relative formats or dates. Times are not currently supported.   Examples: /alerts/minneapolis,mn?query=added:-10minutes&limit=100 (returns alerts received and added within the last 10 minutes for Minneapolis, MN)

## `/conditions`

**Filters**

- `minutelyprecip` — Returns the next hour of minutely precipitation forecast. Filter will only return precip related fields and timestamps. Coverage: Global High-Resolution Coverage Regions: US, Canada, Australia, Japan, South Korea, Western Europe
- `#min` — Returns conditions in # minute intervals for up to a 60 minute period. # must be an integer from 1 to 60.  For example: filter=1min : 1 minute intervals filter=5min : 5 minute intervals filter=15min : 15 minute intervals.  This filter should be used in combination with the from and to parameters
- `#hr` — Returns the conditions in # hour intervals for up to a 24 hour period. # must be an integer from 1 to 24. For example: filter=1hr : 1 hour intervals (Default) filter=3hr : 3 hour intervals filter=6hr : 6 hour intervals.  This filter should be used in combination with the from and to parameters

## `/conditions/summary`

**Filters**

- `day` — (Default) Returns a daily summary. The conditions/summary endpoint can return 1 daily summary per API request.
- `#hr` — Returns forecast data for the specified interval starting at the locale's current time. Example values: 1hr, 2hr, 3hr, 4hr, 6hr, 12hr, and 24hr

## `/convective/outlook`

**Filters**

- `cat` — Return outlooks for the SPC categorical convective outlook. Available for Days 1-3
- `prob` — Return the outlooks for the SPC probability outlook. Available for Days 4-8
- `conhazo` — Return outlooks for both categorical and probability outlooks. Most commonly used filter as provides access to days 1-8. The default filter is none provided.
- `torn` — Return SPC tornado outlook. Available for Day 1
- `xtorn, sigtorn` — Return SPC significant tornado outlook. Available for Day 1
- `alltorn` — Returns both the SPC tornado and significant tornado outlook.
- `hail` — Return SPC hail outlook. Available for Day 1
- `xhail, sighail` — Return SPC significant hail outlook. Available for Day 1
- `allhail` — Returns both the SPC hail and significant hail outlook.
- `wind` — Return SPC wind outlook. Available for Day 1
- `xwind, sigwind` — Return SPC significant wind outlook. Available for Day 1
- `allwind` — Returns both the SPC wind and significant wind outlook.
- `all` — Returns all SPC convective outlooks
- `general` — Limit results to the general thunderstorms categorical outlook
- `marginal` — Limit results to the marginal categorical outlook
- `slight` — Limit results to the slight categorical outlook
- `enhanced` — Limit results to the enhanced categorical outlook
- `moderate` — Limit results to the moderate categorical outlook
- `high` — Limit results to the high categorical outlook
- `day#` — Limit results to day "#" outlooks, day can be from 1-8, eg. day1, day2, ..., day8

**Query properties**

- `id` — Query by the outlook ID
- `cat` — Query by outlook category.   Examples: cat prob torn sigtorn hail sighail wind sigwind
- `day` — Valid day of the outlook. Value from 1 - 8
- `type` — The risk type
- `name` — The risk type name from SPC
- `code` — Numeric code for the risk type

## `/countries`

**Query properties**

- `name` — Used to query the country full name. String should be lower case.
- `iso` — Used to query the country 2 letter ISO abbreviation. Should be lower case.
- `iso3` — Used to query the country 3 letter ISO abbreviation. Should be lower case.
- `pop` — Used to query the population.
- `area` — Used to query by the area in square kilometers.
- `altname` — Used to query alternate names for countries

## `/droughts/monitor`

**Filters**

- `all` — All drought monitor intensity levels
- `d0` — Intensity level 0 - Abnormally Dry
- `d1` — Intensity level 1 - Moderate Drought
- `d2` — Intensity level 2 - Severe Drought
- `d3` — Intensity level 3 - Extreme Drought
- `d4` — Intensity level 4 - Exceptional Drought

**Query properties**

- `id` — Query by the object ID
- `type` — Query by the drought intensity level. D0, D1, D2, D3 or D4
- `name` — Query by the drought intensity name
- `code` — Query by the drought intensity code:  0 - D0 - Abnormally Dry 1 - D1 - Moderate Drought 2 - D2 - Severe Drought 3 - D3 - Extreme Drought 4 - D4 - Exceptional Drought

## `/earthquakes`

**Filters**

- `mini` — Return earthquakes with a magnitude of less than 3.0
- `minor` — Return earthquakes with a magnitude between 3.0 and 3.9
- `light` — Return earthquakes with a magnitude between 4.0 and 4.9
- `moderate` — Return earthquakes with a magnitude between 5.0 and 5.9
- `strong` — Return earthquakes with a magnitude between 6.0 and 6.9
- `major` — Return earthquakes with a magnitude between 7.0 and 7.9
- `great` — Return earthquakes with a magnitude of 8.0 or greater
- `shallow` — Return earthquakes with a depth of less than 70km
- `mmi` — Adds intensity values and polygons representing ground shaking severity (Modified Mercalli Intensity) for the event.

**Query properties**

- `id` — Query on the USGS earthquake ID.
- `mag` — Query based on the magnitude of the earthquake.
- `depth` — Query based on the depth of the earthquake in kilometers.
- `state` — Query based on the state the earthquake occurred.
- `name` — Query based on the location name of where the earthquake occurred.
- `country` — Query based on the country the earthquake occurred.

## `/fires`

**Filters**

- `geo` — Include the fire coverage perimeter information and polygon when available. Note fire perimeters are normally available for some, but not all, large US fires.
- `hasperimeter` — Return only fires that have perimeter information.
- `hasnoperimeter` — Return only fires that do not include perimeter information.

**Query properties**

- `id` — The reported fire ID.
- `dt` — The date of the fire.
- `area` — The area of the fire in acres.
- `name` — The closest city to the fire observation.
- `state` — The state of the closest city to the fire observation.
- `country` — The country of the closest city to the fire observation.
- `conf` — The confidence of the fire as a percentage.

## `/fires/outlook`

**Filters**

- `firewx` — Limit results to fire weather outlooks
- `dryltg` — Limit results to dry lightning outlook
- `all` — Return both fire weather can dry lightning outlooks
- `elevated` — Limit results to fire weather outlook that are elevated in significance
- `critical` — Limit results to fire weather outlook that are critical in significance
- `extreme` — Limit results to fire weather outlook that are extreme in significance
- `isodryt` — Limit results to dry lightning outlook that are isolated dry thunderstorms
- `sctdryt` — Limit results to dry lightning outlook that are scattered dry thunderstorms
- `day1` — Limit results to day 1 outlooks
- `day2` — Limit results to day 2 outlooks
- `day3` — Limit results to day 3 outlooks
- `day4` — Limit results to day 4 outlooks
- `day5` — Limit results to day 5 outlooks
- `day6` — Limit results to day 6 outlooks
- `day7` — Limit results to day 7 outlooks
- `day8` — Limit results to day 8 outlooks

**Query properties**

- `id` — Query by the outlook ID
- `cat` — Query by outlook category
- `day` — Valid day of the outlook. Value from 1 - 8
- `type` — The risk type
- `name` — The risk type name from SPC
- `code` — Numeric code for the risk type:  elevated = 2 critical = 4 extreme = 6  isodryt = 20 sctdryt = 22

## `/forecasts`

**Filters**

- `day` — Returns forecast data using the industry standard where day = 7am to 7pm and night = 7pm to 7am. Refer to the mdnt2mdnt2 filter for a 12:00am to 11:59:59pm calculation.  By default a 7 day forecast will be returned. If your account supports a longer forecast, include the limit parameter. i.e. "limit=14"
- `daynight` — Returns forecast data in a daily 12-hour format in which day and night forecasts are separated. Similar to the "day" filter above, this filter will include a "day" period (7 am - 7 pm) and a "night" period (7 pm - 7 am) per industry standard.  By default, 7 days of forecast information will be returned. If your account supports a longer forecast, include the limit parameter. i.e. "limit=28"  When using filter=daynight, if the local requested time is from Midnight - 4:59 pm the first period will be the day period. If the local requested time is from 5 pm - 11:59 pm the first periods will be the night period.
- `mdnt2mdnt` — Returns forecast data for the 24hr period. Unlike the day (default) filter above, this data will be calculated from midnight to midnight local time.
- `#hr` — Returns forecast data for the specified interval starting at the locale's current time. Supports values: 1hr, 2hr, 3hr, 4hr, 6hr, 12hr, 24hr, 48hr and 72hr.  NOTE: The day and 24hr filters will not provide the same results. The 24hr filter will return summary data at 24-hour intervals starting from the locale's current time, which may not necessarily be the correct summary for the same days within the range. The 48hr and 72hr filters can be used to return a min, max and total value for the multi-day period.
- `#min` — Returns forecast data in the specified minute interval, for up to 60 minutes maximum. Supports values such as 1min, 2min, 5min, 15min.
- `precise` — Normally, Celsius attributes (tempC, minTempC, maxTempC, dewptC, etc) are rounded to the nearest integer. The precise filter returns Celsius values with 1 decimal place.   NOTE: This filter only affects Celsius temperatures. Fahrenheit values are always rounded to the nearest integer.
- `centroid` — When utilized while passing an US zip code for the location, instructs the API to use the zip code centroid latitude/longitude versus the associated city latitude/longitude.

## `/hail/threats`

**Filters**

- `severe` — Returns data points where the max expected hail size is greater than or equal to 1 inch / 2.54 cm.
- `notsevere` — Returns data points where the max expected hail size is less than 1 inch / 2.54 cm.
- `test` — Will provide test data to allow users to preview responses.

## `/impacts/:activity`

**Filters**

- `minseverity0` — Returns all risk factors even if there is no current impact.
- `minseverity1` — Only returns impacts that have a minimum severity of 1
- `minseverity2` — Only returns impacts that have a minimum severity of 2
- `minseverity3` — Only returns impacts that have a minimum severity of 3
- `minseverity4` — Only returns impacts that have a minimum severity of 4
- `minseverity5` — Only returns impacts that have a minimum severity of 5

## `/indices/:type`

**Filters**

- `day` — Use day only forecast periods. Example: Monday, Tuesday, Wednesday. A day is from ~7am to 7pm
- `daynight` — Use day and night forecast periods. Example: Monday, Monday Night, Tuesday, Tuesday Night
- `#hr` — Use interval based forecast. For hourly use '1hr'. Only supported if your subscription supports hourly/interval based forecasts.

## `/lightning`

**Filters**

- `cg` — Limit to cloud-to-ground strikes (default)
- `all` — Both cloud-to-ground and intracloud lightning

## `/lightning/analytics`

**Filters**

- `cg` — Limit to cloud-to-ground strikes (default)
- `all` — Both cloud-to-ground and intracloud lightning
- `ellipse50` — (default) Return the ellipse based on 50% location confidence.
- `ellipse80` — Return the ellipse based on 80% location confidence.
- `ellipse90` — Return the ellipse based on 90% location confidence.
- `ellipse99` — Return the ellipse based on 99% location confidence.

## `/lightning/archive`

**Filters**

- `cg` — Limit to cloud-to-ground strikes (default)
- `ic` — Intracloud/cloud-to-cloud lightning
- `all` — Both cloud-to-ground and intracloud lightning

## `/lightning/summary`

**Filters**

- `cg` — Filter based on cloud-to-ground strikes. This is the default if no filter or query provided.
- `all` — Filter based on all lightning pulses, cloud-to-ground and intracloud.
- `negative` — Returns negative lightning strikes only.
- `positive` — Returns positive lightning strikes only.

## `/lightning/threats`

**Filters**

- `severe` — Limit to lightning storm threats that are flagged as severe
- `notsevere` — Limit to lightning storm threats that are flagged as not severe
- `forceutc` — Force all ISO dates in the API output to use UTC vs. the localized timezone

**Query properties**

- `stormid` — Query by Lightning Storm threat ID
- `issued` — Query by the issued date/time
- `minvalidtime` — Query by the minimum forecast period date/time for the lightning storm threat
- `maxvalidtime` — Query by the maximum forecast period date/time for the lightning storm threat. Each lightning storm threat may have up to a 60 minute forecast period.
- `speed` — Query by the estimated speed in knots of the lightning storm threat
- `added` — Query by the date/time the lightning threat become available within the API
- `created` — An alias for added

## `/maritime`

**Filters**

- `#hr` — Returns the conditions in # hour intervals for up to a 24 hour period. # must be an integer from 1 to 24. For example: filter=1hr : 1 hour intervals (Default) filter=3hr : 3 hour intervals filter=6hr : 6 hour intervals.  This filter is often be used in combination with the from and to parameters. If no from and to the endpoint returns data for the next 24 hours.

## `/maritime/archive`

**Filters**

- `#hr` — Returns the conditions in # hour intervals for up to a 24 hour period. # must be an integer from 1 to 24. For example: filter=1hr : 1 hour intervals (Default) filter=3hr : 3 hour intervals filter=6hr : 6 hour intervals.  This filter is often be used in combination with the from and to parameters. If no from and to the endpoint returns data for the next 24 hours.

## `/models/:model`

**Filters**

- `skipnulls` — Removes fields with null values from the response. Because not every model produces every weather attribute, responses can otherwise include null fields for variables the model does not carry. Applying skipnulls returns only the fields the model actually provides.

## `/normals`

**Filters**

- `daily` — (default) Return daily normals.
- `monthly` — Return monthly normal summary.
- `annual` — Return annual/yearly normal summary.
- `hastemp` — Return normals that have a temperature. Note that some normal stations could only have precip info.
- `hasprecip` — Return normals that have a precipitation information.
- `hassnow` — Return normals that have a snowfall information.

**Query properties**

- `id` — Query normals for a specific co-op/station ID.
- `state` — Query normals for a specific state.
- `country` — Query normals for a specific country (US only).
- `md` — Query normals for a month/day combination (no leading zeros).
- `mon` — Query normals for a month number (1-12).
- `day` — Query normals for a day of month (1-31).
- `tmax` — Query normals based on the normal maximum temperature (F).
- `tmin` — Query normals based on the normal minimum temperature (F).
- `tavg` — Query normals based on the normal average temperature (F).
- `hdd` — Query normals based on the normal heating degree days.
- `cdd` — Query normals based on the normal cooling degree days.
- `pmtd` — Query normals based on the normal precipitation for the month to date (inches).
- `smtd` — Query normals based on the normal snowfall for the month to date (inches).
- `sytd` — Query normals based on the normal snowfall for the year to date (inches).
- `name` — Query normals based on the co-op/station name.

## `/normals/stations`

**Filters**

- `hastemp` — Returns stations that contain temperature normals.
- `hasprcp` — Returns stations that contain precipitation normals.
- `hassnow` — Returns stations that contain snowfall normals.

**Query properties**

- `id` — Query based on the co-op/station ID.
- `state` — Query based on the 2-letter state abbreviation.
- `country` — Query based on the 2-letter country abbreviation. (US only supported)
- `name` — Query based on the station name.

## `/observations`

**Filters**

- `metar` — (default) Returns records using only METAR observation stations
- `allstations` — Returns observations using all available stations including personal weather stations.
- `pws` — Returns observations using only PWS observation stations from PWSweather.com
- `madis` — Returns observations using only MADIS observation stations
- `hfmetar` — Returns observations using only high frequency METARs. These update frequently but may not provide as much information as the standard METAR
- `ausbom` — Returns Australian observations received from the Australian Bureau of Meteorology (AUSBOM)
- `envca` — Returns Canadian observations received from Environment Canada
- `allownosky` — Includes observations that may not include sky information.
- `wxrain` — Returns observations that have at least one weatherCoded value mentioning snow.
- `wxsnow` — Returns observations that have at least one weatherCoded value mentioning snow.
- `wxice` — Returns observations that have at least one weatherCoded value mentioning ice.
- `wxfog` — Returns observations that have at least one weatherCoded value mentioning fog.
- `qcok` — Ignores observations that have failed one or more Quality Control Screening. This is enabled by default, though can be used with the query parameter.
- `strict` — Returns observations that pass QC, have a temperature, dew point, relative humidity, pressure and cloud / weather information
- `centroid` — When utilized while passing an US zip code for the location, instructs the API to use the zip code centroid latitude/longitude versus the associated city latitude/longitude.
- `precise` — When utilized, the API will include additional decimal precision with imperial and metric attributes

**Query properties**

- `temp` — Used to query the temperature. Values are in Celsius.
- `wind` — Used to query the wind speed. Values are in knots.
- `dewpt` — Used to query the dew point. Values are in Celsius.
- `rh` — Used to query the relative humidity.
- `pressure` — Used to query the barometric pressure. Values are in millibars.
- `winddir` — Used to query the wind direction in degrees. 0 being North.
- `gust` — Used to query wind gust speed. Values are in knots.
- `name` — Used to query the observation location's name.
- `state` — Used to query the observation station's state.  Example: /observations/search?query=state:mn&sort=temp:-1 (Returns the observation for the location with the warmest temperature in Minnesota)
- `country` — Used to query the observation station's country.  Example: /observations/search?query=country:us&sort=temp:-1 (Returns the observation for the location with the warmest temperature in the US)
- `id` — Used to query the observation station's ID. Similar to passing the station ID as the :id, but can be used to pull multiple stations at once  Example: /observations/search?query=id:KMSP;id:KROA&limit=2 (Returns the latest observations for both KMSP and KROA)
- `datasource` — used to query observations based on the data source, such as PWS, NOAA_METAR, MADIS_MESONET, etc
- `elev` — Used to query the elevation of the observation.
- `qccode` — The numeric version of the quality control attribute: 0 = failed QC 1 = caution (some observation attributes may be invalid) 10 = OK, passed QC  By default, the API will utilize observations that have passed QC
- `trustfactor` — The trust factor of the observation, 0 - 100. Equivalent to the individual observation QCcode * the station confidence.
- `dt` — Used to query based on the date / time of the observation. Similar to using the from parameter. Example: /observations/search?query=dt:-1hour (returns observations made within the last hour).
- `adt` — Used to query based on the date / time the observation was received and processed.  Example: /observations/search?query=adt:-1hour (returns observations received within the last hour).

## `/observations/archive`

**Filters**

- `allstations` — Returns records using all available stations including personal weather stations.
- `official` — Returns records using official government stations.
- `pws` — Returns records using only PWS observation stations.
- `mesonet` — Returns records using only MESONET observation stations.
- `hasprecip` — Returns observations from stations that have been known to report precipitation.
- `hassky` — Return records that contain sky data in the observation.
- `centroid` — When utilized while passing an US zip code for the location, instructs the API to use the zip code centroid latitude/longitude versus the associated city latitude/longitude.
- `precise` — When utilized, the API will include additional decimal precision with imperial and metric attributes

**Query properties**

- `temp` — Used to query the temperature. Values are in Celsius.
- `dewpt` — Used to query the dew point. Values are in Celsius.
- `rh` — Used to query the relative humidity.
- `pressure` — Used to query the barometric pressure. Values are in millibars.
- `wind` — Used to query the wind speed. Values are in knots.
- `winddir` — Used to query the wind direction in degrees. 0 being North.
- `gust` — Used to query wind gust speed. Values are in knots.
- `name` — Used to query the observation location's name.
- `hasprecip` — Used to query if an observation contains a precipitation record.

## `/observations/summary`

**Filters**

- `allstations` — Returns summaries using all available stations including personal weather stations.
- `official` — Returns summaries using official government stations (alias to metar)
- `metar` — Returns summaries using only METAR observation stations.
- `pws` — Returns summaries using only PWS observation stations.
- `mesonet or madis` — Returns summaries using only MADIS observation stations.
- `hfmetar` — Returns summaries using only High Frequency METAR observations.
- `hasprecip` — Returns summaries from stations that have been known to report precipitation.
- `hassky` — Returns records that contain sky data within the observation.
- `qcok` — Returns records where all observations for the day passed Quality Control.
- `strict` — Returns summaries, where the observation for the day passed QA, included temperatures, dew points, relative humidity, pressure and clouds/weather information
- `centroid` — When utilized while passing an US zip code for the location, instructs the API to use the zip code centroid latitude/longitude versus the associated city latitude/longitude.
- `precise` — When utilized, the API will include additional decimal precision with imperial and metric attributes

**Query properties**

- `id` — Query against the station ID.
- `datasource` — Query based on the data source of the observation.
- `count` — Query against the total number of observations used to create the summary.
- `maxt` — Query against the maximum temperature in Celsius.
- `mint` — Query against the minimum temperature in Celsius.
- `avgt` — Query against the average temperature in Celsius.
- `maxdewpt` — Query against the maximum dew point temperature in Celsius.
- `mindewpt` — Query against the minimum dew point temperature in Celsius.
- `avgdewpt` — Query against the average dew point temperature in Celsius.
- `maxrh` — Query against the maximum relative humidity (percentage).
- `minrh` — Query against the minimum relative humidity (percentage).
- `avgrh` — Query against the average relative humidity (percentage).
- `maxv` — Query against the maximum visibility in meters.
- `minv` — Query against the minimum visibility in meters.
- `avgv` — Query against the average visibility in meters.
- `wind` — Query against the maximum wind speed in knots.
- `gust` — Query against the maximum wind gust speed in knots.
- `maxp` — Query against the maximum pressure in millibars.
- `minp` — Query against the minimum pressure in millibars.
- `avgp` — Query against the average pressure in millibars.
- `precip` — Query against the total precipitation in millimeters (liquid equivalent).
- `precipc` — Query against the total number of observations that reported precipitation.
- `elev` — Query against the observation station elevation in meters.
- `name` — The name of the observation station.
- `state` — The 2-letter state/province abbreviation of the observation station (US & Canada).
- `country` — The 2-letter country abbreviation of the observation station.
- `dt` — Query against the date of the record.
- `hasprecip` — Returns observations that have a recorded precipitation.
- `qc` — Find summaries where the station has at least one observation that matches the value provided.  Quality control: X = failed QC C = caution (some observation attributes may be invalid) P = probation (a station will be on probation if it's new, changed location, or having significant data issues) O = OK, passed QC
- `minqc` — Allows querying against the minimum numeric qc value based on all the obs in the summary.  Quality Control Code is the numerical version of qc (quality control): 0 = failed QC 1 = caution (some observation attributes may be invalid) 3 = probation (a station will be on probation if it's new, changed location, or having significant data issues) 10 = OK, passed QC
- `maxqc` — Allows querying against the maximum numeric qc value based on all the obs in the summary.  Quality Control Code is the numerical version of qc (quality control): 0 = failed QC 1 = caution (some observation attributes may be invalid) 3 = probation (a station will be on probation if it's new, changed location, or having significant data issues) 10 = OK, passed QC
- `mintrustfactor` — Allows querying the minimum trust factor based on the observations within the summary.
- `maxtrustfactor` — Allows querying the maximum trust factor based on the observations within the summary.

## `/phrases/summary`

**Filters**

- `metar` — Will utilize only METAR observation stations when generating the phrase.
- `pws` — Will utilize only PWS observation stations from PWSweather.com when generating the phrase.
- `mesonet` — Will utilize only MESONET observation stations when generating the phrase.
- `allstations` — Will utilize all available stations including personal weather stations when generating the phrase.
- `noob` — Prevents the API from using the latest observation from influencing the phrase, thus returning a forecast only phrase.

## `/places`

**Filters**

- `airport` — Returns all airports, including airbases, airfields and heliports.
- `amusement` — Returns all theme and adventure parks.
- `bridge` — Returns all structures erected across an obstacle, such as a stream, road, etc., in order to carry roads, rail and pedestrians.
- `camp` — Returns all sites occupied by tents, hunts, or other shelters for temporary use.
- `church` — Returns all buildings used for public christian worship.
- `county` — Returns US counties (Parishes in Louisiana).
- `divisions` — Returns smaller US towns, non-incorporation locations such as census divisions.
- `feature` — Returns all natural geological features.
- `fort` — Returns all defensive structures or earthworks.
- `golf` — Returns all golf courses.
- `lake` — Returns all lakes, including crater lakes, salt lakes, oxbow lakes and underground lakes.
- `neighborhood` — Returns smaller US non-incorporation locations such as census divisions, local areas of a city etc.
- `parish` — Alias for the county filter.
- `park` — Returns all parks and other areas maintained as a place of recreation.
- `poi` — Returns all categories of places across all filters.
- `port` — Returns all places that transfer waterborne cargo or passengers, usually in a harbor.
- `ppl` — Returns all populated places, including larger cities, towns and smaller locations and neighborhoods.
- `reserve` — Returns all tracts of public land reserved for future use or restricted use, including agricultural, forest, hunting, nature, reservation and wildlife.
- `school` — Returns all schools, including colleges, military, maritime and technical.
- `stadium` — Returns all facilities used for athletic games and spectators.
- `temple` — Returns all places used for religious worship.
- `trail` — Returns all paths, tracks or routes used by pedestrians, animals, or off-road vehicles.
- `tunnel` — Returns all subterranean passageways used for transportation, including natural caves, road and rail passages.
- `university` — Returns all institutions for higher learning, including prep schools.
- `worship` — Returns all churches and temples.
- `complex` — For improved speed the search action does not include the expanded profile information for locations. The complex filter forces the API to return the expanded profile information, though may lead to a slower response.
- `simple` — Forces the API to not return the expanded profile information for places, leading to faster responses.

**Query properties**

- `name` — Query for a place with the specified name. This queries against the primary name in our database. NOTE: The string to search should be in lowercase.  Example:  /places/search?query=name:austin&limit=10 (returns 10 locations that match the name "Austin")
- `altname` — Query for a place based on the primary or alternate names. Useful for locations that may have multiple names such as "dc, washington, washington dc". NOTE: The string to search should be in lowercase.  Example: /places/search?query=altname:dc&limit=10 (returns 10 locations that match the name "dc")
- `state` — Query for a place with the specified state or province two letter abbreviation. This should be used in conjunction with the name property. NOTE: The string to search should be in lowercase.  Example: /places/search?query=name:austin,state:tx (returns a single location matching the name "Austin" in the state of "TX")
- `country` — Query for a place with the specified country two letter abbreviation.. This should be used in conjunction with the name property. NOTE: The string to search should be in lowercase.   Example: /places/search?query=name:paris,country:fr (returns a single location matching the name "Paris" in the country of "FR")
- `pop` — Query for a place based on it's population.  Example: /places/closest?p=minneapolis,mn&query=pop:75000&limit=10 (returns up to 10 closest locations to Minneapolis that have a population of 75,000 or higher)

## `/places/airports`

**Filters**

- `airport` — Returns all airports.
- `smallairport` — Returns small airports.
- `medairport` — Returns medium-sized airports.
- `largeairport` — Returns large airports.
- `heliport` — Returns heliports.
- `balloonport` — Returns balloon ports (public use balloon airports).
- `sea` — Returns sea bases.
- `all` — Returns all types.
- `closed` — Returns airports marked as closed.

**Query properties**

- `id` — Query by the global recognized ID for the airport.
- `name` — Query by the airport name.
- `city` — Query by the airport's city name.
- `state` — Query by the airport's 2-letter state or province abbreviation (US and Canada only).
- `country` — Query by the airport's 2-letter country abbreviation.
- `type` — Query by the airport type code. Refer to the profile.type property for possible values.
- `iata` — Query based on the airport's 3-letter IATA code.

## `/places/postalcodes`

**Filters**

- `us` — Returns US zip code information.
- `ca, canada` — Returns Canadian postal code information.
- `standard` — Returns only standard location types.

**Query properties**

- `id` — Query by the postal code.
- `zip` — Query by the zip code (alias for id).
- `postalcode` — Query by the postal code (alias for id).
- `name` — Query by the name of the postal code.
- `city` — Query by the city name for the postal code.
- `state` — Query by the 2-letter state abbreviation for the postal code.
- `country` — Query by the 2-letter country abbreviation for the postal code.
- `type` — Query by the postal code type.

## `/renewables/irradiance/archive`

**Filters**

- `#hr` — Returns solar data for the specified interval starting at the locale's current time. Default option is 1hr

## `/renewables/irradiance/summary`

**Filters**

- `ghi` — Global Horizontal Irradiance – total solar power (direct + diffuse) on a flat, horizontal surface (kWh/m²).
- `dni` — Direct Normal Irradiance – direct sunlight power on a surface perpendicular to the sun’s rays (kWh/m²).
- `dif` — Diffuse Horizontal Irradiance – scattered sunlight on a horizontal surface (kWh/m²).
- `annual` — Interval averages over historical years.
- `monthly` — Interval averages over individual historical months.
- `climatologymonth` — Interval averages over calendar months.
- `fullperiod` — Interval averages over the entire requested period.
- `fullyears` — Daily and annual averages over all complete years in the requested period.

## `/rivers`

**Filters**

- `outofservice` — Return observations for gauges marked as out of service
- `inservice` — Return observations for gauges that are not marked as out of service
- `obsnotcurrent` — Return observations for gauges that have not reported updated information recently
- `notdefined` — Return observations for gauges that do not have defined flood categories
- `lowthreshold` — Return observations for gauges that are currently reporting at or below their low water threshold
- `noflooding` — Return observations for gauges that are known not to be flooding
- `action` — Return observations for gauges that are known to be near flood level.
- `flood` — Return observations for gauges that are known to have minor flooding
- `minor` — Return observations for gauges that are known to have minor flooding
- `moderate` — Return observations for gauges that are known to have moderate flooding
- `major` — Return observations for gauges that are known to have major flooding
- `allflood` — Return observations for gauges that are known to have any level of flooding
- `heighttype` — Return observations for gauges that report water height
- `flowtype` — Return observations for gauges that report water flow rate

**Query properties**

- `id` — Query by river gauge ID
- `dt` — Query by the date/time of the observation.   Example: /rivers/search?query=dt:-2hours&limit=1&sort=dt Will return up to 100 river gauge observations that updated within the past two hours, sorted oldest to newest
- `status` — Query based on the gauge status:  out_of_service - Gauge is known to be out of service obs_not_current - Gauge has not reported updated observations recently not_defined - Gauge is reporting observations but has no action/flooding levels defined, thus cannot determine if flooding low_threshold - Gauge is reporting levels below the defined low water threshold no_flooding - Gauge is reporting observations and below flood and action levels action - Gauge is reporting observations at or above action levels. Normally means near flood stage minor - Gauge is reporting levels at or above the minor flood level moderate - Gauge is reporting levels at or above the defined moderate flood level major - Gauge is reporting levels at or above the defined major flood level
- `statuscode` — Query based on the numerical version of the status code:  out_of_service: -1 obs_not_current: 0 not_defined: 1 low_threshold: 3 no_flooding: 5 action: 7 minor: 9 moderate: 11 major: 13
- `hasimpacts` — Query stations that provide impact information based on flood levels.
- `name` — Query by river gauge name
- `waterbody` — Query by the body of water the river gauge is on
- `state` — Query by the two letter state abbreviation the river gauge is within
- `country` — Query by the two letter country abbreviation the river gauge is within

## `/rivers/gauges`

**Filters**

- `impacts` — Limit results to gauges with flood impact information
- `recentcrests` — Limit results to gauges that have recent crest information
- `historiccrests` — Limit results to gauges that have historic crest information
- `lowwaterrecords` — Limit results to gauges that have low water record information

**Query properties**

- `id` — Query by the gauge ID
- `place` — Query by the gauge place name
- `waterbody` — Query by the gauge waterbody name
- `state` — Query by the gauge two letter state abbreviation
- `country` — Query by the gauge two letter country abbreviation

## `/roadweather`

**Filters**

- `primary` — Returns road weather information for primary roads. NOTE: the location must be near a primary road.
- `secondary` — Returns road weather information for secondary roads. NOTE: the location must be near a secondary road.
- `bridge` — Returns road weather information for bridges. NOTE: the location must be near a bridge.
- `noroadcheck` — By default the API ensures the requested location is within 100 meters of a supported road. With this filter, this check is bypassed and the API will return information on the closest supported road within 20km.

## `/roadweather/analytics`

**Filters**

- `primary` — Returns road weather information for primary roads. NOTE: the location must be near a primary road.
- `secondary` — Returns road weather information for secondary roads. NOTE: the location must be near a secondary road.
- `bridge` — Returns road weather information for bridges. NOTE: the location must be near a bridge.
- `noroadcheck` — By default the API ensures the requested location is within 100 meters of a supported road. With this filter, this check is bypassed and the API will return information on the closest supported road within 20km.
- `addweather` — Return the atmospheric weather information for the location.

## `/roadweather/conditions`

**Filters**

- `primary` — Returns road weather information for primary roads. NOTE: the location must be near a primary road.
- `secondary` — Returns road weather information for secondary roads. NOTE: the location must be near a secondary road.
- `bridge` — Returns road weather information for bridges. NOTE: the location must be near a bridge.
- `noroadcheck` — By default the API ensures the requested location is within 100 meters of a supported road. With this filter, this check is bypassed and the API will return information on the closest supported road within 20km.

## `/stormcells`

**Filters**

- `hail` — Returns storm cells that most likely contain hail.
- `rotating` — Returns storm cells that show rotation characteristics.
- `tornado` — Returns storm cells that contain a tornadic vortex signature (TVS) as determined by NEXRAD radar.
- `threat` — Returns storm cells which are potentially threatening
- `rainmoderate` — Returns storm cells showing moderate precipitation potential
- `rainheavy` — Returns storm cells showing heavy precipitation potential
- `rainintense` — Returns storm cells showing intense precipitation potential
- `conus` — Returns storm cells within the Continental US (CONUS) only.  Equivalent to: query=country:us,state:!ak,state:!hi,state:!pr

**Query properties**

- `hailprob` — Used to query the storm cells hail probability. i.e. query=hail:70 will return only if the hail probability is greater than or equal to 70%.
- `hailsevere` — Used to query the storm cells probability of severe hail. Severe hail is defined by the National Weather Service (NWS) as hail that is at least 1" in diameter. This definition was adopted in 2010 where previously it was 3/4" or greater.
- `hailsize` — Used to query the storm cells maximum hail size, in inches.
- `tvs` — Used to query if a storm cell is tornadic.
- `mda, rotation` — Used to query the degree of a storm cells rotation.
- `dbz` — Used to query the precipitation dbz.
- `type` — Used to query based on stormcell type: general, hail, rotating, tornado
- `isgeneral` — Used to query storm cells that are general / garden variety 1 = true, 0 = false
- `ishail` — Used to query storm cells that have at least a 70% probability of hail. 1 = true, 0 = false
- `isrotating` — Used to query storm cells that show major rotation 1 = true, 0 = false
- `istornado` — Used to query storm cells that show potential tornado characteristics 1 = true, 0 = false
- `isthreat` — Used to query storm cells that may be a potential threat 1 = true, 0 = false
- `name` — Used to query based on the closest city to the storm cell.
- `state` — Query the state the storm cell is in.   Example: /stormcells/search?query=state:al&limit=100 (Returns up to 100 storm cells in the state of Alabama)
- `country` — Used to limit results based on country. Currently only 'us' supported.

## `/stormcells/summary`

**Filters**

- `hail` — Returns summary for storm cells that most likely contain hail.
- `rotating` — Returns summary for storm cells that show rotation characteristics.
- `tornado` — Returns summary for storm cells that contain a tornadic vortex signature (TVS) as determined by NEXRAD radar.
- `threat` — Returns summary for storm cells that are potentially threatening, ignoring storm cells that are not currently threatening in nature.
- `rainmoderate` — Returns summary for storm cells that show moderate, heavy or intense rainfall / precipitation
- `rainheavy` — Returns summary for storm cells that show heavy or intense rainfall / precipitation
- `rainintense` — Returns summary for storm cells that show intense rainfall / precipitation
- `conus` — Returns summary for storm cells within the Continental US only.
- `geo` — Indicator for the API to include the polygons of the storm cell groups used with-in the summary
- `noforecast` — Indicator for the API to ignore the storm cell forecasts when creating the storm cell groups used with-in the summary

**Query properties**

- `hail, hailprob` — Used to query the storm cells hail probability. i.e. query=hail:70 will return only if the hail probability is greater than or equal to 70%.
- `hailsevere` — Used to query the storm cells probability of severe hail.
- `hailsize` — Used to query the storm cells maximum hail size, in inches.
- `tvs` — Used to query if a storm cell is tornadic.
- `mda, rotation` — Used to query the degree of a storm cells rotation.
- `dbz` — Used to query the storm cells based on estimated precipitation intensity
- `name` — Used to query based on the closest city to the storm cell.
- `state` — Query the state the storm cell is in.   Example: /stormcells/search?query=state:al&limit=100 (Returns up to 100 storm cells in the state of Alabama)
- `country` — Used to limit results based on country. Currently only 'us' supported.
- `pop*` — Available for use with the affects action only. Utilized to limit results based on population.

## `/stormreports`

**Filters**

- `avalanche` — Returns avalanche-related storm reports.
- `blizzard` — Returns blizzard-related storm reports.
- `dust` — Return dust related storm reports.
- `flood` — Returns flood-related storm reports.
- `fog` — Returns fog-related storm reports.
- `ice` — Returns ice-related storm reports.
- `hail` — Returns hail-related storm reports.
- `lightning` — Returns lightning-related storm reports.
- `marine` — Returns marine related storm reports.
- `rain` — Returns rain-related storm reports.
- `snow` — Returns snow-related storm reports.
- `tides` — Returns tide-related storm reports.
- `tornado` — Returns tornado and waterspout-related storm reports.
- `tropical` — Returns tropical storm / hurricane related storm reports
- `wind` — Returns wind-related storm reports.

**Query properties**

- `code` — Query storm reports based on the coded type.  Code Types:  0 = hurricane 1 = storm surge 2 = dust storm 3 = sprinkles 4 = high astronomical winds 5 = freezing rain 6 = freeze (temperature) 7 = extreme wind chill 8 = wildfire 9 = seiche A = high sustained winds B = downburst C = funnel cloud D = thunderstorm wind damage E = flood F = flash flood G = thunderstorm wind gust H = hail I = excessive heat J = dense fog L = lightning M = marine thunderstorm wind N = non-thunderstorm wind gust None = storm code was not reported O = non-thunderstorm wind damage P = rip currents Q = tropical storm R = heavy rain S = snow / heavy snow T = tornado U = wildfire V = avalanche W = water spout X = wall cloud Z = blizzard a = blowing snow s = sleet t = sneaker wave u = lakeshore flood v = coastal flood x = debris flow z = volcanic ashfall  Example: /stormreports/search?query=code:S&limit=10 (returns 10 storm reports that are of the code "S", which is snow)
- `type` — Query storm reports based on the named type.   Example: /stormreports/search?query=type:snow&limit=10 (returns 10 storm reports that are of the type snow)
- `state` — Query storm reports within a state. The state should be lower case and a two letter abbreviation.  Example: /stormreports/search?query=state:mn&limit=10 (returns 10 storm reports that the state matches Minnesota, "mn")
- `name` — Query storm reports based on the closest location.
- `detail` — Query storm reports based on the reported magnitude. i.e. rain/snow amount, wind speed.

## `/stormreports/summary`

**Filters**

- `avalanche` — Returns avalanche-related storm reports.
- `blizzard` — Returns blizzard-related storm reports.
- `dust` — Return dust related storm reports.
- `flood` — Returns flood-related storm reports.
- `fog` — Returns fog-related storm reports.
- `ice` — Returns ice-related storm reports.
- `hail` — Returns hail-related storm reports.
- `lightning` — Returns lightning-related storm reports.
- `marine` — Returns marine related storm reports.
- `rain` — Returns rain-related storm reports.
- `snow` — Returns snow-related storm reports.
- `tides` — Returns tide-related storm reports.
- `tornado` — Returns tornado and waterspout-related storm reports.
- `tropical` — Returns tropical storm / hurricane related storm reports
- `wind` — Returns wind-related storm reports.

**Query properties**

- `code` — Query storm reports based on the coded type.  Code Types:  0 = hurricane 1 = storm surge 2 = dust storm 3 = sprinkles 4 = high astronomical winds 5 = freezing rain 6 = freeze (temperature) 7 = extreme wind chill 8 = wildfire 9 = seiche A = high sustained winds B = downburst C = funnel cloud D = thunderstorm wind damage E = flood F = flash flood G = thunderstorm wind gust H = hail I = excessive heat J = dense fog L = lightning M = marine thunderstorm wind N = non-thunderstorm wind gust None = storm code was not reported O = non-thunderstorm wind damage P = rip currents Q = tropical storm R = heavy rain S = snow / heavy snow T = tornado U = wildfire V = avalanche W = water spout X = wall cloud Z = blizzard a = blowing snow s = sleet t = sneaker wave u = lakeshore flood v = coastal flood x = debris flow z = volcanic ashfall  Example: /stormreports/search?query=code:S&limit=10 (returns 10 storm reports that are of the code "S", which is snow)
- `type` — Query storm reports based on the named type.   Example: /stormreports/search?query=type:snow&limit=10 (returns 10 storm reports that are of the type snow)
- `state` — Query storm reports within a state. The state should be lower case and a two letter abbreviation.  Example: /stormreports/search?query=state:mn&limit=10 (returns 10 storm reports that the state matches Minnesota, "mn")
- `name` — Query storm reports based on the closest location.
- `detail` — Query storm reports based on the reported magnitude. i.e. rain/snow amount, wind speed.

## `/sunmoon`

**Filters**

- `sun` — Provides sunrise/sunset information.
- `twilight` — Provides sun and twilight information.
- `moon` — Provides moon rise / moon set information.
- `moonphase` — Provides moon phase information for a specific time.

## `/sunmoon/moonphases`

**Filters**

- `new` — Filter on new moons.
- `first` — Filter on first quarter moons.
- `full` — Filter on full moons.
- `third` — Filter on third-quarter moons.

**Query properties**

- `type` — Query based on the type of moon phase abbreviated name.
- `code` — Query based on the numeric representation of the moon phase.

## `/threats`

**Query properties**

- `hailprob` — Used to limit to storms containing storm cells with a specified hail probability. i.e. query=hail:70 will return only if the hail probability is greater than or equal to 70%.
- `hailsevere` — Used to limit to storms containing storm cells with a specified probability of severe hail.
- `hailsize` — Used to limit to storms containing storm cells with a specified maximum hail size, in inches.
- `isgeneral` — Used to limit to storms containing storm cells that are general / garden variety 1 = true, 0 = false
- `ishail` — Used to limit to storms containing storm cells that have at least a 70% probability of hail. 1 = true, 0 = false
- `isrotating` — Used to limit to storms containing storm cells that show major rotation 1 = true, 0 = false
- `istornado` — Used to limit to storms containing storm cells that show potential tornado characteristics 1 = true, 0 = false
- `isthreat` — Used to limit to storms containing storm cells that may be a potential threat 1 = true, 0 = false
- `tvs` — Used to limit to storms containing storm cells that are potentially tornadic.

## `/tides`

**Filters**

- `highlow` — Returns only high and low tidal information.
- `high` — Returns only the high tide information.
- `low` — Returns only the low tide information.

**Query properties**

- `id` — Query tides for a specific tidal location.
- `state` — Query tides for a specific state using the 2-letter state abbreviation (lowercase).
- `country` — Query tides for a specific country using the 2-letter country abbreviation (lowercase).
- `type` — Query tides based on tide type.
- `height` — Query tides based on the tide height in feet.
- `heightM` — Query tides based on the tide height in meters.

## `/tides/stations`

**Query properties**

- `id` — Query based on the station ID.
- `state` — Query based on the station's 2-letter abbreviation (lowercase).
- `country` — Query based on the station's 2-letter country abbreviation (lowercase).
- `type` — Query based on the station type. Refer to the profile.type property for supported values.

## `/tropicalcyclones`

**Filters**

- `atlantic` — Return tropical systems within the Atlantic basin
- `al` — Alias for atlantic
- `eastpacific` — Return tropical systems within the Eastern Pacific basin
- `ep` — Alias for eastpacific
- `centralpacific` — Return tropical systems within the Central Pacific basin
- `cp` — Alias for centralpacific
- `westpacific` — Return tropical systems within the Western Pacific basin
- `wp` — Alias for westpacific
- `pacific` — Return tropical systems within the Eastern, Central and Western Pacific basins
- `indian` — Return tropical systems within the Indian Ocean basin
- `io` — Alias for indian
- `southern` — Return tropical systems within the Southern Hemisphere basin
- `sh` — Alias for southern
- `position` — Used when searching by location, closest and within actions. Search based on system current position
- `track` — Used when searching by location, closest and within actions. Search based on system historical track
- `forecast` — Used when searching by location, closest and within actions. Search based on system forecast track
- `windfield` — Used to force the API to return the 34, 50 and 64 knot wind field polygons for the current position and forecast position of active tropical cyclones.
- `geo` — Used to force the API to return the error cone when available. By default the API does not return the error cone due to the large amount of data.
- `test` — Return Test storm information, useful for development and demonstration
- `invests` — Return information on active invests. Invests are areas under INVESTigation for potential future tropical development.
- `dateline` — When combined with format=geojson, the API will split any polygons into split error cones and line strings into separate features at the anti-merdian / dateline.

**Query properties**

- `id` — Query based on the storm ID. The storm ID will be similar too: 2017-AL-16 or YEAR-BASIN-EVENTNUMBER
- `basin` — Query the storm basin two letter abbreviation: AL = Atlantic EP = Eastern Pacific CP = Central Pacific WP = Western Pacific IO = Indian Ocean SH = Southern Hemisphere
- `origin` — Query the two letter basin abbreviation the storm originated in. See Basin for the potential availables.
- `currentbasin` — Query the two letter basin abbreviation that the storm is currently within. See Basin for the potential availables.
- `year` — Query based on the year of the tropical season the tropical system initiated.
- `event` — Query based on the event number of the tropical system. The event number will start at 1 for each basin and increase consecutively with each tropical system within that basin.
- `name` — Query based on the tropical system name, without the storm type. For example for Hurricane Nate, you would use query=name:nate
- `startdate` — Query based on the date and time the tropical system was initialized and the first advisory issued by the NHC or JWTC.
- `enddate` — Query based on the date and time that the tropical system was deactivated. This will be the date and time of the final advisory issued by the NHC or JWTC.
- `maxtype` — Further details on these definitions are provided at the top of this page.  Query based on the maximum storm type:  I = Invest* WV = Tropical Wave LO = Low Pressure System** TD = Tropical Depression TS = Tropical Storm H = Hurricane TY = Typhoon  * Only seen when passing filter=invests ** Only seen as max when passing filter=invests. Possible to be seen in previous track, but will not be max for a named storm.
- `maxcat` — Further details on these definitions are provided at the top of this page.  Query based on the maximum category of the storm:  I = Invest* DB = Disturbance WV = Tropical Wave LO = Low Pressure System** TD = Tropical Depression TC = Tropical Cyclones SD = Subtropical Depression TS = Tropical Storm SS = Subtropical Storm H1 = Category 1 Hurricane H2 = Category 2 Hurricane H3 = Category 3 Hurricane H4 = Category 4 Hurricane H5 = Category 5 Hurricane TY = Typhoon STY = Super Typhoon  * Only seen when passing filter=invests ** Only seen as max when passing filter=invests. Possible to be seen in previous track, but will not be max for a named storm.
- `maxwindspeed` — Query based on the maximum wind speed, in knots, observed for the system, as reported by the NHC or JWTC.
- `minpressure` — Query based on the minimum pressure, in millibars, observed for the system, as reported by the NHC or JWTC.
- `test` — Query based on if the system is a test storm for development purposes. true = A test tropical system false = An actual tropical system
- `stormtype` — Query based on current storm type (see maxtype codes) for currently active storms.
- `stormcat` — Query based on current storm strength category (see maxcat codes) for currently active storms.
- `windspeed` — Query based on current sustained wind speed, in knots, for currently active storms.
- `pressure` — Query based on current pressure, in millibars, for currently active storms.
- `stormdir` — Query based on current storm direction, in degrees, for currently active storms.
- `stormspeed` — Query based on current storm speed, in knots, for currently active storms.
- `trackstormtype` — Query based on storm type within the historical track of a storm. See maxtype codes.
- `trackstormcat` — Query based on storm category within the historical track of a storm. See maxcat codes.
- `trackwindspeed` — Query based on the wind speed, in knots, within the historical track of a storm
- `trackpressure` — Query based on the pressure, in millibars, within the historical track of a storm
- `trackstormdir` — Query based on the storm direction, in degrees, within the historical track of a storm
- `trackstormspeed` — Query based on the storm speed, in knots, within the historical track of a storm
- `fcststormtype` — Query based on the forecast storm type for currently active storms. See maxtype codes.
- `fcststormcat` — Query based on the forecast storm strength category for currently active storms. See maxcat codes.
- `fcstwindspeed` — Query based on the forecast sustained wind speed, in knots, for currently active storms.

## `/tropicalcyclones/archive`

**Filters**

- `atlantic` — Return tropical systems within the Atlantic basin
- `al` — Alias for atlantic
- `eastpacific` — Return tropical systems within the Eastern Pacific basin
- `ep` — Alias for eastpacific
- `centralpacific` — Return tropical systems within the Central Pacific basin
- `cp` — Alias for centralpacific
- `westpacific` — Return tropical systems within the Western Pacific basin
- `wp` — Alias for westpacific
- `pacific` — Return tropical systems within the Eastern, Central and Western Pacific basins
- `indian` — Return tropical systems within the Indian Ocean basin
- `io` — Alias for indian
- `southern` — Return tropical systems within the Southern Hemisphere basin
- `sh` — Alias for southern
- `position` — Used when searching by location, closest and within actions. Search based on system current position
- `track` — Used when searching by location, closest and within actions. Search based on system historical track
- `forecast` — Used when searching by location, closest and within actions. Search based on system forecast track
- `geo` — Used to force the API to return the error cone when available. By default the API does not return the error cone due to the large amount of data.
- `test` — Return Test storm information, useful for development and demonstration
- `active` — Return information on active systems
- `notactive` — Return information on non active systems

**Query properties**

- `id` — Query based on the storm ID. The storm ID will be similar too: 2017-AL-16 or YEAR-BASIN-EVENTNUMBER
- `basin` — Query the storm basin two letter abbreviation: AL = Atlantic EP = Eastern Pacific CP = Central Pacific WP = Western Pacific IO = Indian Ocean SH = Southern Hemisphere
- `origin` — Query the two letter basin abbreviation the storm originated in. See Basin for the potential availables.
- `year` — Query based on the year of the tropical season the tropical system initiated.
- `event` — Query based on the event number of the tropical system. The event number will start at 1 for each basin and increase consecutively with each tropical system within that basin.
- `name` — Query based on the tropical system name, without the storm type. For example for Hurricane Nate, you would use query=name:nate
- `startdate` — Query based on the date and time the tropical system was initialized and the first advisory issued by the NHC or JWTC.
- `enddate` — Query based on the date and time that the tropical system was deactivated. This will be the date and time of the final advisory issued by the NHC or JWTC.
- `maxtype` — Further details on these definitions are provided at the top of this page.  Query based on the maximum storm type:  I = Invest* WV = Tropical Wave LO = Low Pressure System** TD = Tropical Depression TS = Tropical Storm H = Hurricane TY = Typhoon  * Only seen when passing filter=invests ** Only seen as max when passing filter=invests. Possible to be seen in previous track, but will not be max for a named storm.
- `maxcat` — Further details on these definitions are provided at the top of this page.  Query based on the maximum category of the storm:  I = Invest* WV = Tropical Wave LO = Low Pressure System** TD = Tropical Depression TS = Tropical Storm H1 = Category 1 Hurricane H2 = Category 2 Hurricane H3 = Category 3 Hurricane H4 = Category 4 Hurricane H5 = Category 5 Hurricane TY = Typhoon STY = Super Typhoon  * Only seen when passing filter=invests ** Only seen as max when passing filter=invests. Possible to be seen in previous track, but will not be max for a named storm.
- `maxwindspeed` — Query based on the maximum wind speed, in knots, observed for the system, as reported by the NHC or JWTC.
- `minpressure` — Query based on the minimum pressure, in millibars, observed for the system, as reported by the NHC or JWTC.
- `test` — Query based on if the system is a test storm for development purposes. true = A test tropical system false = An actual tropical system
- `stormtype` — Query based on current storm type (see maxtype codes) for currently active storms.
- `stormcat` — Query based on current storm strength category (see maxcat codes) for currently active storms.
- `windspeed` — Query based on current sustained wind speed, in knots, for currently active storms.
- `pressure` — Query based on current pressure, in millibars, for currently active storms.
- `stormdir` — Query based on current storm direction, in degrees, for currently active storms.
- `stormspeed` — Query based on current storm speed, in knots, for currently active storms.
- `trackstormtype` — Query based on storm type within the historical track of a storm. See maxtype codes.
- `trackstormcat` — Query based on storm category within the historical track of a storm. See maxcat codes.
- `trackwindspeed` — Query based on the wind speed, in knots, within the historical track of a storm
- `trackpressure` — Query based on the pressure, in millibars, within the historical track of a storm
- `trackstormdir` — Query based on the storm direction, in degrees, within the historical track of a storm
- `trackstormspeed` — Query based on the storm speed, in knots, within the historical track of a storm
- `fcststormtype` — Query based on the forecast storm type for currently active storms. See maxtype codes.
- `fcststormcat` — Query based on the forecast storm strength category for currently active storms. See maxcat codes.
- `fcstwindspeed` — Query based on the forecast sustained wind speed, in knots, for currently active storms.
- `active` — Query if the storm is active: true = active false = not active

## `/xcast/forecasts`

**Filters**

- `1hr` — (default) Returns hourly forecast data.
- `10min` — Returns forecast data in 10 min intervals.
