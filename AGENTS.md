# Xweather API & Maps — agent skills

This repository packages five [Agent Skills](https://agentskills.io) for the Xweather developer
platform. They are provider-neutral: any skills-compatible agent can load them, and the same content
also ships as plugins for Claude Code and OpenAI's ChatGPT and Codex plugin surfaces.

## The skills

| Skill | Use it for |
|---|---|
| `plugins/xweather/skills/weather-api/` | Building `data.api.xweather.com` request URLs — 59 endpoints, 8 actions, filters, query syntax, and access-cost reporting |
| `plugins/xweather/skills/raster-maps/` | Building `maps.api.xweather.com` URLs — static map images and XYZ tile templates across 159 layers, with map-unit cost reporting |
| `plugins/xweather/skills/mapsgl/` | The MapsGL JavaScript SDK (`@xweather/mapsgl`) — controllers, weather layers, styling, expressions, legends, timeline animation, session cost |
| `plugins/xweather/skills/mapsgl-apple/` | The MapsGL SDK for Apple platforms — install channels, `MapboxMapController`/`MapLibreMapController`, `WeatherService.LayerCode` layers, SwiftUI and UIKit setup, paint, expressions, legends, timeline, session cost |
| `plugins/xweather/skills/webhooks/` | Pushed data delivery — receiver design, securing the endpoint, retry and idempotency behaviour, registration |

Each skill is a directory with a `SKILL.md`, plus `references/` for detail loaded on demand and
`scripts/` for the two helper programs. Read a skill's `SKILL.md` when a task matches its
`description`; pull in `references/` files only as needed — several are large.

## Working in this repository

**Never hand-edit the generated reference files.** Six are derived from live Xweather sources:

```
plugins/xweather/skills/weather-api/references/endpoints.md
plugins/xweather/skills/weather-api/references/examples.md
plugins/xweather/skills/weather-api/references/filters.md
plugins/xweather/skills/raster-maps/references/layers.md
plugins/xweather/skills/mapsgl/references/layers.md
plugins/xweather/skills/mapsgl-apple/references/layers.md
```

The Apple SDK one is the odd case: there is no public layer catalog endpoint for it, so it is generated
from the SDK's published DocC symbol index at
`cdn.aerisapi.com/sdk/ios/mapsgl/docs/v<version>/index/index.json`, with the version resolved from the
releases endpoint. The Swift `WeatherService.LayerCode` case names are not mechanical transforms of the
JS layer codes (`air-quality-pm2p5` is `.particulateMatter2p5Micron`), so the two catalogs cannot be
cross-derived.

Regenerate them instead:

```bash
python3 scripts/regenerate_references.py           # rewrite in place
python3 scripts/regenerate_references.py --check   # exit 1 on drift, writes nothing
```

CI runs `--check` on any pull request touching a generated file, so a hand-edit fails the build.

The script also pins the **MapsGL CDN version** in `plugins/xweather/skills/mapsgl/SKILL.md` to whatever
`docs/api/releases/versions` reports for the `mapsgl` product key, rewriting every
`cdn.aerisapi.com/sdk/js/mapsgl/<version>/` URL and the sentence naming the fallback. That in-file
version is only a fallback — the skill instructs agents to fetch the current release at generation
time. Don't hand-edit it.

**The releases endpoint outranks npm.** `@xweather/mapsgl` on npm has carried a higher version than
the releases endpoint reports, and `cdn.aerisapi.com` serves those newer paths too, so a URL
resolving proves nothing about what's released. Never bump a version from npm or from a successful
`curl`.

Three further files embed generated content inside hand-written prose —
`plugins/xweather/skills/weather-api/references/access-cost.md`, `plugins/xweather/skills/raster-maps/references/map-units.md`, and
`plugins/xweather/skills/mapsgl/references/weather-layers.md`. The script reports drift in those but won't rewrite
them; fix them by hand when it flags one.

## Conventions

- **Skill frontmatter follows the Agent Skills spec**: `name` and `description` required, `name`
  matching the directory name, `version` under `metadata` rather than at the top level. Validate with
  `skills-ref validate ./plugins/xweather/skills/<name>` if you have it.
- **Keep skill content provider-neutral.** Don't name a specific agent's tools (`WebFetch`,
  `AskUserQuestion`, `Grep`) or client-specific variables in `SKILL.md` or `references/`. Say what to
  do ("fetch the catalog", "ask the user"), not which tool to do it with.
- **Reference bundled files by relative path** from the skill root — `references/foo.md`,
  `scripts/bar.py` — and keep them one level deep.
- **All Python scripts are standard-library Python 3** with no dependencies. Keep them that way; a
  dependency install would break the zero-setup property that makes them portable.
- **Credentials come from the environment** (`XWEATHER_CLIENT_ID`, `XWEATHER_CLIENT_SECRET`) and are
  never echoed. Printed URLs always show `{client_id}` / `{client_secret}` placeholders. Preserve
  this in any change to the scripts.
- **Every skill states the attribution requirement.** Xweather requires a "Powered by Vaisala
  Xweather" credit wherever its data or imagery is displayed, so each `SKILL.md` carries an
  "Attribution is required" section, and `mapsgl` and `raster-maps` build it into their generated
  markup. Keep it in all five — skills install independently, so none can rely on another to carry it.
- **Descriptions are long prose in a YAML scalar.** A `: ` sequence inside one silently breaks the
  frontmatter and the skill then loads with no metadata. Use an em dash instead of a colon.

## Bumping the version

Both `plugins/xweather/.claude-plugin/plugin.json` and
`plugins/xweather/.codex-plugin/plugin.json` set an explicit `version`; bump both on every release.
Keep `metadata.version` in each `SKILL.md` in step. Never change the plugin's `name` (`xweather`) —
it keys installs and namespaces the skills. Run `python3 scripts/validate_packaging.py` after any
marketplace, manifest, or skill-version change; CI runs the same comparison.
