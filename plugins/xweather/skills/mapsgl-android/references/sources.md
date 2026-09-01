# Custom data sources - MapsGL Android

Verified against SDK source descriptors + `MapController.addSource` (1.6.x).
Docs are secondary:
https://www.xweather.com/docs/mapsgl-android-sdk/advanced/sources

## Vector tiles

URL templates support `{z}`, `{x}`, `{y}`, `{s}`. When `authenticator` is null,
`addSource` wires the controller's WeatherService authenticator so
`[CLIENT_ID]_[CLIENT_SECRET]` / `{accessKey}` expand per request.

```kotlin
val alertsSource = VectorSourceDescriptor(id = "alerts").apply {
    url = "https://maps{s}.aerisapi.com/[CLIENT_ID]_[CLIENT_SECRET]/alerts/{z}/{x}/{y}/0.pbf"
    minZoom = 4f
    maxZoom = 8f
}
controller.addSource(alertsSource)

// Later: change tile template on the runtime source
(controller.getSource("alerts") as? VectorTileSource)?.let {
    it.tileURL = "https://maps{s}.aerisapi.com/[CLIENT_ID]_[CLIENT_SECRET]/alerts/{z}/{x}/{y}/20220506111000.pbf"
}
```

## GeoJSON (remote URL)

```kotlin
val earthquakesSource = GeoJSONSourceDescriptor(id = "earthquakes").apply {
    url =
        "https://data.api.xweather.com/earthquakes/search?query=mag:1&limit=200&format=geojson&client_id=[CLIENT_ID]&client_secret=[CLIENT_SECRET]"
}
controller.addSource(earthquakesSource)
```

## GeoJSON (in-memory)

Descriptor has no inline JSON field. Register, then set `data` on `GeoJSONSource`:

```kotlin
controller.addSource(GeoJSONSourceDescriptor(id = "earthquakes"))
val geoSource = controller.getSource("earthquakes") as GeoJSONSource
geoSource.data = FeatureCollection.fromJson(geoJSONString)
```

Update later via `geoSource.url` or `geoSource.data`.

## Then add a layer

```kotlin
controller.addLayer(
    CircleLayerDescriptor(
        id = "earthquake-circles",
        source = "earthquakes",
        sourceLayer = null,
    ),
    beforeID = null,
)
```

See `custom-layers.md` for fill/line/symbol examples.
