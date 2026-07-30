# Xweather plugin marketplace for Claude Code

A Claude Code marketplace distributing the **`xweather`** plugin — three skills covering the
Xweather Weather API, Raster Maps, and the MapsGL JS SDK.

## Install

```
/plugin marketplace add <owner>/xweather-claude-plugin
/plugin install xweather@xweather
/reload-plugins
```

Replace `<owner>/xweather-claude-plugin` with this repository's path once it's hosted. A local path
works too, for testing before publishing:

```
/plugin marketplace add ./xweather-claude-plugin
/plugin install xweather@xweather
```

Keeping the repository private restricts the marketplace to people who can read it — no other
configuration needed.

## What's in it

| Skill | Covers |
|---|---|
| `/xweather:weather-api` | Build and run `data.api.xweather.com` request URLs — 59 endpoints, 8 actions, filters, query syntax, and access-cost reporting |
| `/xweather:raster-maps` | Build `maps.api.xweather.com` URLs — static map images and XYZ tile templates across 159 layers, with map-unit cost reporting |
| `/xweather:mapsgl` | The `@xweather/mapsgl` WebGL SDK — controllers, weather layers, styling, expressions, legends, timeline animation |

Two commands are added to the Bash tool's `PATH` while the plugin is enabled:

- `xwrequest '<path>'` — issue a Weather API request, printing the credential-redacted URL, the
  accesses charged, remaining allowance, and the response.
- `xwmap '<path>' [-o file]` — estimate a Raster Maps request's map units and optionally fetch the
  image.

Both read credentials from `XWEATHER_CLIENT_ID` and `XWEATHER_CLIENT_SECRET` in the environment, so
secrets stay out of shell history and out of the printed output. Keys come from the Apps section of
<https://data.portal.xweather.com/account/keys>.

## Layout

```
.claude-plugin/marketplace.json     the catalog
plugins/xweather/                   the plugin
├── .claude-plugin/plugin.json      manifest
├── bin/                            xwrequest, xwmap — added to PATH
└── skills/
    ├── weather-api/
    ├── raster-maps/
    └── mapsgl/
```

## Development

```bash
claude --plugin-dir ./plugins/xweather     # load without installing
claude plugin validate ./plugins/xweather  # validate before publishing
```

`/reload-plugins` picks up edits without restarting the session.

## Releasing

`plugins/xweather/.claude-plugin/plugin.json` sets an explicit `version`, so **users only receive
updates when that field is bumped**. Bump it on every release. Keep the `version` in
`marketplace.json` (if you add one) in step, or omit it there and let the plugin manifest be the
single source of truth.

## Regenerating the references

Three reference files are generated from live Xweather catalogs and can be refreshed when the
products change:

```bash
# Weather API endpoints, actions, params, filters, query props, sort fields, cost multipliers
curl -s https://www.xweather.com/docs/api/weather-api/endpoints

# Raster Maps layers, modifiers, coverage, data range, update interval, multipliers
curl -s https://www.xweather.com/docs/api/maps/layers

# MapsGL layer catalog
curl -s https://www.xweather.com/docs/api/mapsgl/layers
```

Each skill's `SKILL.md` tells Claude to refetch the relevant catalog when a request fails or when the
bundled reference doesn't cover something, so the skills degrade gracefully as the products evolve.
