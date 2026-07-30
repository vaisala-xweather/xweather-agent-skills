# URL formats

Host: `maps.api.xweather.com`. The legacy `maps.aerisapi.com` still resolves — always emit the
current host. Tile requests may also use the sharded subdomains `maps1.` … `maps4.`
(`maps1.api.xweather.com`), which exist to raise browser per-host connection limits.

Credentials are **path segments joined by an underscore**, not query parameters:
`/{client_id}_{client_secret}/`. This is the biggest structural difference from the Weather API.

## Static map — center point

```
https://maps.api.xweather.com/{client_id}_{client_secret}/{layers}/{width}x{height}/{place},{zoom}/{offset}.{format}
```

| Segment | Required | Notes |
|---|---|---|
| `layers` | yes | One or more layer codes, comma-separated, composited left to right. Max 10. |
| `width` x `height` | yes | Pixels. Max 5000x5000 on paid plans, 2000x2000 on the free developer trial. |
| `place` | yes | `lat,lon`, US ZIP, Canadian postal code, `city,state`, or any Weather API supported place. US and Canadian locations require the `city,state` form. |
| `zoom` | yes | Between the base map's and overlays' `minzoom`/`maxzoom`; 2–19 is normally supported. Defaults to 6 if omitted. |
| `offset` | yes | Time offset or valid time — see below. |
| `format` | yes | Image quality extension — see below. |

Note the place and zoom share one path segment, comma-joined: `minneapolis,mn,7` is
place=`minneapolis,mn`, zoom=`7`. A `lat,lon` place makes three comma-separated numbers:
`44.96,-93.27,7`.

```
https://maps.api.xweather.com/{client_id}_{client_secret}/radar/300x300/44.96,-93.27,7/current.png
https://maps.api.xweather.com/{client_id}_{client_secret}/flat,radar,admin/300x300/55415,7/current.png
https://maps.api.xweather.com/{client_id}_{client_secret}/sat,radar:75/300x300/minneapolis,mn,7/current.jpg
```

## Static map — bounding box

```
https://maps.api.xweather.com/{client_id}_{client_secret}/{layers}/{width}x{height}/{south},{west},{north},{east}/{offset}.{format}
```

Center and zoom are derived so the box fits the requested dimensions; some scaling may occur to hit
the exact pixel size. Corner order is **south, west, north, east** — bottom latitude, left longitude,
top latitude, right longitude.

```
https://maps.api.xweather.com/{client_id}_{client_secret}/radar/320x320/30.1010,-85.9578,33.0948,-82.4421/current.png
https://maps.api.xweather.com/{client_id}_{client_secret}/flat,radar,admin/320x320/30.1010,-85.9578,33.0948,-82.4421/current.png
```

Four comma-separated numbers = bounding box; three = `lat,lon,zoom`. That count is the only thing
distinguishing the two static forms, so a dropped coordinate silently changes the request's meaning.

## Map tiles

```
https://maps.api.xweather.com/{client_id}_{client_secret}/{layers}/{z}/{x}/{y}/{offset}.{format}
```

256×256 PNG tiles in Spherical Mercator (EPSG:3857) — the scheme Google Maps, Apple Maps, Mapbox,
Leaflet, and OpenStreetMap all use. Zoom is normally 1–21. `x` is the tile column, `y` the row.

```
https://maps.api.xweather.com/{client_id}_{client_secret}/radar/8/41/23/current.png
```

For a mapping library, leave the placeholders in and let the library substitute them:

```
https://maps{s}.api.xweather.com/{client_id}_{client_secret}/radar/{z}/{x}/{y}/current.png
```

### Leaflet

```javascript
var map = L.map('map').setView([44.96, -93.27], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

L.tileLayer('https://maps{s}.api.xweather.com/{client_id}_{client_secret}/radar/{z}/{x}/{y}/current.png', {
  subdomains: '1234',
  attribution: '&copy; Xweather'
}).addTo(map);
```

Xweather layers can also serve as the base map, removing the OSM layer entirely — use a base map
layer code first in the list: `flat,radar,admin`.

### Mapbox GL JS

```javascript
map.addSource('xweather-radar', {
  type: 'raster',
  tiles: ['https://maps.api.xweather.com/{client_id}_{client_secret}/radar/{z}/{x}/{y}/current.png'],
  tileSize: 256
});
map.addLayer({ id: 'xweather-radar', type: 'raster', source: 'xweather-radar', paint: { 'raster-opacity': 0.8 } });
```

### Google Maps

```javascript
const radar = new google.maps.ImageMapType({
  getTileUrl: (coord, zoom) =>
    `https://maps.api.xweather.com/{client_id}_{client_secret}/radar/${zoom}/${coord.x}/${coord.y}/current.png`,
  tileSize: new google.maps.Size(256, 256),
  opacity: 0.8
});
map.overlayMapTypes.push(radar);
```

### OpenLayers

```javascript
new ol.layer.Tile({
  source: new ol.source.XYZ({
    url: 'https://maps.api.xweather.com/{client_id}_{client_secret}/radar/{z}/{x}/{y}/current.png'
  })
});
```

## Time offsets

Every request needs a time segment. Two forms.

**Relative offset.** `current` or `latest` for the most recent frame; otherwise a signed integer plus
a unit. The API issues a temporary redirect to the nearest available frame.

| Unit | Accepted spellings |
|---|---|
| Current | `current`, `latest` |
| Seconds | `s`, `second`, `seconds` |
| Minutes | `m`, `min`, `minute`, `minutes` |
| Hours | `h`, `hr`, `hour`, `hours` |
| Days | `d`, `day`, `days` |

```
.../radar/500x500/minneapolis,mn,6/current.png
.../radar/500x500/minneapolis,mn,6/-10minutes.png
.../fradar/500x500/minneapolis,mn,6/+1hour.png
```

The numeric part must be an integer — `-90minutes`, never `-1.5hours`.

**Valid time.** A UTC timestamp as `YYYYMMDDhhiiss`. The API returns the closest available frame at
or before that time.

```
.../radar/500x500/minneapolis,mn,6/20160601174100.png
```

Past reach is per-layer (`Range` in `layers.md`) — radar goes back 30 days, satellite 7. Future reach
depends on the forecast model: HRRR ~18 h, NAM 60 h, GFS 360 h.

## Image quality

The extension controls encoding. Prefix any of these with `@2x` for a retina-DPI version
(`@2x.png`, `@2x.jpg90`).

| Extension | Result |
|---|---|
| `png` | True-color PNG |
| `png32` / `png64` / `png128` / `png256` | Indexed PNG at that colour count (dithered) |
| `jpg70` | 70 % quality JPEG |
| `jpg` / `jpg80` | 80 % quality JPEG — the default |
| `jpg90` / `jpg95` / `jpg100` | Higher-quality JPEG |
| `webp` | WebP |

Transparency matters: **tile overlays must use `png` or `webp`.** JPEG has no alpha channel, so a
JPEG tile renders as an opaque block over the base map. JPEG is fine for a static map that already
includes its own base layer.

Indexed PNGs (`png32`–`png256`) meaningfully cut bandwidth on mobile at some colour-banding cost.

## Layer combination

Comma-separate codes; they composite in order, left to right, so the first is the bottom of the
stack. Maximum **10 layers** per request (subscription may lower this).

```
alerts,radar                                    → radar drawn on top of alerts
flat-dk,alerts,radar,admin                      → dark base, alerts, radar, then borders/cities
```

A conventional stack is: base map → weather layers → admin/overlay labels last, so labels stay
legible above the weather.

Layer codes come from `layers.md` or the live catalog. Older doc examples use short aliases that
still work but are not in the catalog — `sat` for `satellite-geocolor`, `cities` for `admin-cities`,
`frad` for `fradar`. Prefer the catalog codes; recognise the aliases when reading existing URLs.

## Errors

Raster Maps uses a **different error envelope from the Weather API** — and a different status code
for bad credentials:

```
HTTP 403
{"error":{"code":"authorization_error","message":"Invalid client credentials"}}
```

A failed request returns JSON with an `application/json` content type rather than an image, so
anything consuming the response should check the content type before treating the bytes as an image.
