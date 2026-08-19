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

## Checking the skills

Two checks beyond `validate_packaging.py`:

```bash
python3 scripts/check_skill_links.py --skip-links   # references resolve; offline
python3 scripts/check_skill_links.py                # also probe every URL
```

The reference check verifies that every `references/foo.md` a skill mentions
actually exists, that each one is reachable from its `SKILL.md`, and that none is
orphaned. It understands a qualified cross-skill mention - "the `mapsgl` skill's
`references/sessions.md`" resolves against `mapsgl`, not against the skill doing
the mentioning.

`.github/workflows/check-skills.yml` runs the offline half on every change under
`plugins/xweather/skills/`, and the link half weekly. Links are deliberately kept
off pull requests: a third-party outage should not block an unrelated change.

**The `mapsgl-android` layer catalog is generated, but not by CI.**

```bash
python3 scripts/regenerate_mapsgl_android_layers.py --sdk ../mapsgl-android-sdk
python3 scripts/regenerate_mapsgl_android_layers.py --sdk ../mapsgl-android-sdk --check
```

Unlike `regenerate_references.py`, this one reads a local SDK checkout rather than
a public endpoint, so it cannot run in CI. That follows from the skill tracking the
SDK's development branch, whose source is not published anywhere CI could fetch.
Run `--check` by hand after the SDK moves; it writes nothing and exits non-zero on
drift. The set of codes comes from the checkout, and each is compared against the
released KDoc so anything only on the branch is marked *(unreleased)*.

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

## Keep the two plugin manifests in sync

The plugin ships two manifests, and **every property they share must hold the same value** — CI
enforces it:

```
plugins/xweather/.claude-plugin/plugin.json
plugins/xweather/.codex-plugin/plugin.json
```

Shared: `name`, `version`, `description`, `author`, `homepage`, `license`, `keywords`. The
human-facing name also has to agree across three places, despite living at a different path in each —
`displayName` in the marketplace entry and the Claude manifest, `interface.displayName` in the Codex
one.

Check before pushing:

```bash
python3 scripts/validate_packaging.py
```

Enable the pre-push hook once per clone so this can't reach the remote broken:

```bash
git config core.hooksPath .githooks
```

Bumping `version` in one manifest and forgetting the other is the failure that actually happens.

## Bumping the version

Both `plugins/xweather/.claude-plugin/plugin.json` and
`plugins/xweather/.codex-plugin/plugin.json` set an explicit `version`; bump both on every release.
Keep `metadata.version` in each `SKILL.md` in step. Never change the plugin's `name` (`xweather`) —
it keys installs and namespaces the skills. Run `python3 scripts/validate_packaging.py` after any
marketplace, manifest, or skill-version change; CI runs the same comparison.
