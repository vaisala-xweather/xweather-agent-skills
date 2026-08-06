# Android gotchas - MapsGL (1.6.x)

## Requirements

- **minSdk 28** (Android 9+)
- **OpenGL ES 3.0** for encoded sample / particle / contour / grid GLES paths
- **Mercator** projection on the Mapbox map before weather layers

## Dependencies

- MapsGL JitPack AAR **does not** replace Mapbox - always add Mapbox Maps SDK
- Configure Mapbox Maven + `MAPBOX_DOWNLOADS_TOKEN` or builds fail resolving Mapbox
- Don't double-depend on `mapsglmaps` via classic and groupId coordinates

## Constructor

Use `MapboxMapController(mapView, account)`.  
The `(mapView, baseContext, account, lifecycleOwner)` overload is **deprecated**.

## LayerCode vs layer id

Styling / `beforeId` / Mapbox queries need the **resolved** layer id from the
weather config / returned `TileLayer`, not `LayerCode.value` (e.g. not
`"temperatures"`).

## R8 / ProGuard

The library ships `consumerProguardFiles` and keeps the public API. Consumer apps
should not need custom keep rules for normal `addWeatherLayer` usage. Prefer
public APIs over reflecting into internals.

## Rendering paths (1.6.x mental model)

- **Encoded** sample / particles / contours / grids -> GLES custom layers on Mapbox
- **Many vector** fill/line/circle/symbol/heatmap weather layers -> Mapbox style
  layers (plus GLES for stencil masks where used)

## Permissions

Location is optional (demo UX). Network must work for tiles/auth. Demo README
historically typos `ACCESS_COURSE_LOCATION` - use `ACCESS_COARSE_LOCATION` if you
copy permissions.

## Compose

SDK demos are View/`MapView`-centric. Only produce Compose wrappers when the
user asks; Mapbox's Compose map APIs are a separate integration surface.
