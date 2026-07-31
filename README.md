# Xweather plugin marketplace for Claude Code

A Claude Code marketplace distributing the **`xweather`** plugin — four skills covering the
Xweather Weather API, Raster Maps, the MapsGL JS SDK, and Webhooks.

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
| `/xweather:webhooks` | Pushed data delivery — receiver design, securing the endpoint, available data sets, retry and idempotency behaviour, registration details |

Installing prompts for nothing and configures nothing — the skills work immediately, and the two
commands below activate once you export your credentials.

Xweather also hosts an **MCP server** for answering weather questions directly. It isn't bundled here
(a bundled MCP server can't be conditionally disabled, so it would show a permanent connection error
for anyone without MCP access); the `weather-api` skill documents how to connect it in one command.

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
.github/workflows/                  weekly reference refresh
scripts/regenerate_references.py    regenerates the generated reference files
plugins/xweather/                   the plugin
├── .claude-plugin/plugin.json      manifest
├── bin/                            xwrequest, xwmap — added to PATH
└── skills/
    ├── weather-api/
    ├── raster-maps/
    ├── mapsgl/
    └── webhooks/
```

`scripts/` sits at the repo root, not inside the plugin: installing copies only the plugin directory
to a cache, so maintenance tooling there would ship to every user for no reason.

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

Four reference files are generated from live Xweather catalogs rather than hand-written, so they go
stale as the products change:

| File | Source |
|---|---|
| `weather-api/references/endpoints.md` | `docs/api/weather-api/endpoints` + each endpoint's doc page |
| `weather-api/references/examples.md` | each endpoint doc page's `exampleRequests` |
| `weather-api/references/filters.md` | each endpoint doc page's filter and query tables |
| `raster-maps/references/layers.md` | `docs/api/maps/layers` |

```bash
python3 scripts/regenerate_references.py           # rewrite in place
python3 scripts/regenerate_references.py --check   # exit 1 on drift, writes nothing
```

`.github/workflows/refresh-references.yml` runs the regeneration weekly and opens a PR when anything
drifts, and runs `--check` on any PR touching a generated file so a hand-edit fails loudly.

Two further files — `weather-api/references/access-cost.md` and `raster-maps/references/map-units.md`
— embed multiplier tables inside hand-written prose. The script **reports** drift in those but won't
rewrite them, since regenerating would destroy the surrounding explanation. Fix them by hand when the
script flags one.

Endpoint doc pages render their parameter tables client-side, so the script reads the Next.js RSC
payload out of the HTML rather than the rendered DOM. That's inherently coupled to Xweather's docs
stack; if it changes, the script refuses to write near-empty files and fails loudly instead of
quietly emptying a reference. The MapsGL layer catalog
(`curl -s https://www.xweather.com/docs/api/mapsgl/layers`) is fetched live by the `mapsgl` skill at
use time, so there's nothing to regenerate for it.

Each skill's `SKILL.md` tells Claude to refetch the relevant catalog when a request fails or when the
bundled reference doesn't cover something, so the skills degrade gracefully as the products evolve.
