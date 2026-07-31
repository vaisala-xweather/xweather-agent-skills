# Xweather API & Maps — agent skills

This repository packages four [Agent Skills](https://agentskills.io) for the Xweather developer
platform. They are provider-neutral: any skills-compatible agent can load them, and the same content
also ships as a Claude Code plugin.

## The skills

| Skill | Use it for |
|---|---|
| `skills/weather-api/` | Building `data.api.xweather.com` request URLs — 59 endpoints, 8 actions, filters, query syntax, and access-cost reporting |
| `skills/raster-maps/` | Building `maps.api.xweather.com` URLs — static map images and XYZ tile templates across 159 layers, with map-unit cost reporting |
| `skills/mapsgl/` | The `@xweather/mapsgl` WebGL SDK — controllers, weather layers, styling, expressions, legends, timeline animation, session cost |
| `skills/webhooks/` | Pushed data delivery — receiver design, securing the endpoint, retry and idempotency behaviour, registration |

Each skill is a directory with a `SKILL.md`, plus `references/` for detail loaded on demand and
`scripts/` for the two helper programs. Read a skill's `SKILL.md` when a task matches its
`description`; pull in `references/` files only as needed — several are large.

## Working in this repository

**Never hand-edit the generated reference files.** Five are derived from live Xweather catalogs:

```
skills/weather-api/references/endpoints.md
skills/weather-api/references/examples.md
skills/weather-api/references/filters.md
skills/raster-maps/references/layers.md
skills/mapsgl/references/layers.md
```

Regenerate them instead:

```bash
python3 scripts/regenerate_references.py           # rewrite in place
python3 scripts/regenerate_references.py --check   # exit 1 on drift, writes nothing
```

CI runs `--check` on any pull request touching a generated file, so a hand-edit fails the build.

Three further files embed generated content inside hand-written prose —
`skills/weather-api/references/access-cost.md`, `skills/raster-maps/references/map-units.md`, and
`skills/mapsgl/references/weather-layers.md`. The script reports drift in those but won't rewrite
them; fix them by hand when it flags one.

## Conventions

- **Skill frontmatter follows the Agent Skills spec**: `name` and `description` required, `name`
  matching the directory name, `version` under `metadata` rather than at the top level. Validate with
  `skills-ref validate ./skills/<name>` if you have it.
- **Keep skill content provider-neutral.** Don't name a specific agent's tools (`WebFetch`,
  `AskUserQuestion`, `Grep`) or client-specific variables in `SKILL.md` or `references/`. Say what to
  do ("fetch the catalog", "ask the user"), not which tool to do it with.
- **Reference bundled files by relative path** from the skill root — `references/foo.md`,
  `scripts/bar.py` — and keep them one level deep.
- **The two scripts are standard-library Python 3** with no dependencies. Keep them that way; a
  dependency install would break the zero-setup property that makes them portable.
- **Credentials come from the environment** (`XWEATHER_CLIENT_ID`, `XWEATHER_CLIENT_SECRET`) and are
  never echoed. Printed URLs always show `{client_id}` / `{client_secret}` placeholders. Preserve
  this in any change to the scripts.
- **Descriptions are long prose in a YAML scalar.** A `: ` sequence inside one silently breaks the
  frontmatter and the skill then loads with no metadata. Use an em dash instead of a colon.

## Bumping the version

`.claude-plugin/plugin.json` sets an explicit `version`; Claude Code users only receive updates when
it changes, so bump it on every release. Keep `metadata.version` in each `SKILL.md` in step. Never
change the plugin's `name` (`xweather`) — it keys installs and namespaces the skills.
