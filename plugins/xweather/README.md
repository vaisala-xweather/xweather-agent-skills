# Xweather API & Maps

Claude Code plugin for the Xweather developer platform: build Weather API request URLs, generate
Raster Maps imagery and tile URLs, work with the MapsGL SDK, and set up pushed data delivery.

Installs and is referenced as **`xweather`** — that identifier is the skill namespace
(`/xweather:weather-api`) and the install target (`/plugin install xweather@xweather`). "Xweather API
& Maps" is the display name shown in the `/plugin` picker.

## Skills

### `/xweather:weather-api`

Turns a plain-language description of wanted weather data into a `data.api.xweather.com` URL, and
runs it when credentials are available. Covers all 59 endpoints, the 8 actions, per-endpoint filter
and query-property semantics, the query operator syntax, place and date formats, batch requests, and
the response/error envelope.

Every URL it produces comes with the **access cost** — the endpoint multiplier as a floor, or the
exact `X-Cost-Tokens` value when the request actually ran. It knows that `route` bills one access per
point and that `batch` bills each sub-request separately.

### `/xweather:raster-maps`

Builds `maps.api.xweather.com` URLs in either of the two shapes the product supports — a static map
image, or an XYZ tile template for Leaflet, Mapbox GL, Google Maps, or OpenLayers. It asks which one
you want when that isn't clear, because the two aren't interchangeable.

Covers all 159 layers with their dash-joined data modifiers, the colon-attached visual modifiers
(opacity, blur, gray, invert, 29 blend modes, `scale-hsla`), time offsets, and image-quality
extensions. Reports map units for every URL: `ceil(w/256) × ceil(h/256) × Σ(layer multipliers)`.

With credentials present it asks before fetching, since fetching spends real map units.

### `/xweather:mapsgl`

The `@xweather/mapsgl` client-side SDK — map controllers for Mapbox GL, MapLibre GL, Google Maps and
Leaflet, adding and styling weather layers, data-driven expressions, color scales, legends, masks,
and timeline animation.

### `/xweather:webhooks`

The push alternative to polling: designing and securing a receiver endpoint, the available data sets,
the acknowledge-then-process contract, retry and idempotency behaviour, and the registration details
Xweather needs. Webhooks are a premium add-on and endpoints are registered by Xweather staff, so the
skill separates what you can build today from what needs an account conversation.

## The Xweather MCP server

Xweather hosts an MCP server at `https://mcp.api.xweather.com/mcp` that answers weather questions
directly instead of producing URLs for you to call.

**This plugin deliberately does not bundle it.** A bundled MCP server can't be conditionally disabled,
so anyone installing the plugin without an MCP-enabled subscription would get a permanent red
connection error for a feature they never asked for. Adding it yourself is one command:

```bash
claude mcp add --transport http xweather https://mcp.api.xweather.com/mcp \
  --header "Authorization: Bearer CLIENT_ID_CLIENT_SECRET"
```

Note the token format: client id and secret joined by a **single underscore**. Add `--scope user` for
all projects, or `--scope project` to share it with a repo. Narrow the loaded tools with
`?include_tags=forecast,summary` if you have other MCP servers connected.

The `weather-api` skill documents the server in full — authentication methods, the six tool tag
groups, filter precedence, and how to read a failed connection — so you can just ask Claude about it.
Whether MCP access is included in your subscription is an account question for your Xweather account
executive.

## Commands added to PATH

| Command | Purpose |
|---|---|
| `xwrequest '<path>'` | Weather API request. Prints the credential-redacted URL, HTTP status, accesses charged with the multiplier breakdown, remaining allowance, and the pretty-printed body. `--post`, `--raw`. |
| `xwmap '<path>'` | Raster Maps request. Prints the redacted URL and map-unit estimate, saves the image. `--estimate-only` computes cost without sending anything. `-o` sets the output path. |

Both require `XWEATHER_CLIENT_ID` and `XWEATHER_CLIENT_SECRET` in the environment:

```bash
export XWEATHER_CLIENT_ID='…' XWEATHER_CLIENT_SECRET='…'

xwrequest '/observations/seattle,wa?filter=allstations&limit=3'
xwmap 'flat,radar,admin/800x600/minneapolis,mn,7/current.png' -o radar.png
xwmap 'flat,lightning-strikes/800x600/dallas,tx,7/current.png' --estimate-only
```

Credentials are never echoed — the printed URL always shows `{client_id}` / `{client_secret}`
placeholders.

## Credentials

Keys come from the Apps section of <https://data.portal.xweather.com/account/keys>. Each key pair is
bound to a **namespace** — a top-level domain for web, or a reverse-DNS bundle id for mobile. A
request from outside that namespace fails with `unauthorized_namespace` on the Weather API, or a 403
`authorization_error` on Raster Maps, regardless of whether the URL is otherwise correct.

Raster Maps puts credentials in the URL *path*, so a tile URL used in client-side JavaScript exposes
the key pair to anyone viewing the page. The namespace binding is what limits the damage.

## Requirements

- An Xweather account with the relevant product access. A free developer account works for
  evaluation, with a 2000×2000 static-map size cap.
- `python3` for the two bundled commands (standard library only — no dependencies to install).
- Optional: a subscription including MCP access, if you separately connect the Xweather MCP server.
- Optional: the Webhooks premium add-on, to actually receive pushed data. The `webhooks` skill is
  useful before that — you can build and test a receiver against the sample payloads first.
