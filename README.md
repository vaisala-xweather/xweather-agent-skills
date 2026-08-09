# Xweather API & Maps — Agent Skills

Five [Agent Skills](https://agentskills.io) for the Xweather developer platform: build Weather API
request URLs, generate Raster Maps imagery and tile URLs, work with the MapsGL SDKs for the web and for
Apple platforms, and set up pushed data delivery.

Agent Skills is an open standard originally published by Anthropic, so these work in any
skills-compatible agent — **OpenAI Codex, Cursor, GitHub Copilot, VS Code, Gemini CLI, Goose,
OpenHands, JetBrains Junie, Claude Code**, and others. The repository also packages the same skills
as installable plugins for Claude Code and OpenAI's ChatGPT and Codex plugin surfaces.

## The skills

| Skill | Covers |
|---|---|
| `weather-api` | `data.api.xweather.com` request URLs — every endpoint, all 8 actions, per-endpoint filter and query semantics, place and date formats, batch requests, and the access-cost model. Every URL comes with its cost. |
| `raster-maps` | `maps.api.xweather.com` URLs — static map images and XYZ tile templates across the full layer catalog, dash-joined data modifiers, opacity/blur/blend/scale-hsla, time offsets, and map-unit cost reporting. |
| `mapsgl` | The MapsGL JavaScript SDK (`@xweather/mapsgl`) — controllers for Mapbox GL, MapLibre GL, Google Maps and Leaflet, the full layer catalog, styling, expressions, legends, timeline animation, and session-based cost. |
| `mapsgl-apple` | The MapsGL SDK for Apple platforms — Swift Package/CocoaPods/Carthage install, `MapboxMapController` and `MapLibreMapController`, the full `WeatherService.LayerCode` catalog, SwiftUI and UIKit setup, paint properties, expressions, legends, timeline, and session-based cost. |
| `webhooks` | Pushed data delivery — receiver design, securing the endpoint, available data sets, retry and idempotency behaviour, and the registration details Xweather needs. |

## Install

### Claude Code

```
/plugin marketplace add vaisala-xweather/xweather-agent-skills
/plugin install xweather@vaisala-xweather
/reload-plugins
```

In the **Claude app**: Settings → Plugins → Add → `vaisala-xweather/xweather-agent-skills`.

Installing prompts for nothing and configures nothing. When developing, load the plugin directly:
`claude --plugin-dir ./plugins/xweather`.

### OpenAI Codex

Install the plugin from this repository's marketplace:

```bash
codex plugin marketplace add vaisala-xweather/xweather-agent-skills
codex plugin add xweather@vaisala-xweather
```

Start a new Codex thread after installation so the new skills are loaded. The repository retains its
Claude marketplace as the shared catalog because Codex supports the legacy-compatible
`.claude-plugin/marketplace.json` location; `plugins/xweather/.codex-plugin/plugin.json` supplies the
first-class OpenAI plugin metadata.

For a skills-only installation, Codex also discovers skills in `.agents/skills` directories — note
the plural `.agents`:

| Scope | Path |
|---|---|
| Repository | `$REPO_ROOT/.agents/skills` (also `$CWD/.agents/skills` and parent dirs) |
| Personal | `$HOME/.agents/skills` |
| Machine-wide | `/etc/codex/skills` |

```bash
git clone https://github.com/vaisala-xweather/xweather-agent-skills.git
mkdir -p ~/.agents/skills
ln -s "$PWD"/xweather-agent-skills/plugins/xweather/skills/* ~/.agents/skills/
```

Symlinking rather than copying means `git pull` updates a skills-only installation in place. Restart
Codex if a skill doesn't appear. Individual skills can be disabled in `~/.codex/config.toml`:

```toml
[[skills.config]]
path = "/Users/you/.agents/skills/mapsgl/SKILL.md"
enabled = false
```

### Other skills-compatible agents

Cursor, GitHub Copilot, VS Code, Gemini CLI, Goose, OpenHands, JetBrains Junie and others all read
the same `SKILL.md` files but look in different directories. Clone the repo and symlink
`plugins/xweather/skills/*` into whichever location your client documents — <https://agentskills.io/clients> links the
per-tool instructions.

### ChatGPT

ChatGPT can load Agent Skills packaged in an OpenAI plugin. This repository includes the required
`.codex-plugin/plugin.json`; public discovery in ChatGPT and Codex requires a separate submission to
OpenAI's shared plugin directory. The hosted Xweather MCP server remains available when direct
live-data tools are preferred; see [The Xweather MCP server](#the-xweather-mcp-server) below.

## Helper scripts

Two standard-library Python 3 programs, bundled with the skills that use them:

| Script | Purpose |
|---|---|
| `plugins/xweather/skills/weather-api/scripts/xwrequest.py` | Issue a Weather API request. Prints the credential-redacted URL, HTTP status, accesses charged with the multiplier breakdown, remaining allowance, and the response. |
| `plugins/xweather/skills/raster-maps/scripts/xwmap.py` | Issue a Raster Maps request. Prints the redacted URL and map-unit estimate, saves the image. `--estimate-only` computes cost without sending anything. |

Both read credentials from the environment, so secrets stay out of shell history and out of the
printed output:

```bash
export XWEATHER_CLIENT_ID='…' XWEATHER_CLIENT_SECRET='…'

python3 plugins/xweather/skills/weather-api/scripts/xwrequest.py '/observations/seattle,wa?filter=allstations&limit=3'
python3 plugins/xweather/skills/raster-maps/scripts/xwmap.py 'flat,radar,admin/800x600/minneapolis,mn,7/current.png' -o radar.png
python3 plugins/xweather/skills/raster-maps/scripts/xwmap.py 'flat,lightning-strikes/800x600/dallas,tx,7/current.png' --estimate-only
```

Claude Code additionally exposes them as bare `xwrequest` / `xwmap` commands via `bin/`, but the
skills never assume that.

## Credentials

Keys come from the **API Keys** page at <https://data.portal.xweather.com/account/keys>. Each key pair is
bound to a **namespace** — a top-level domain for web, or a reverse-DNS bundle id for mobile. A
request from outside that namespace fails with `unauthorized_namespace` on the Weather API, or a 403
`authorization_error` on Raster Maps, regardless of whether the URL is otherwise correct.

Raster Maps puts credentials in the URL *path*, so a tile URL used in client-side JavaScript exposes
the key pair to anyone viewing the page. The namespace binding is what limits the damage.

## The Xweather MCP server

Xweather hosts an MCP server at `https://mcp.api.xweather.com/mcp` that answers weather questions
directly instead of producing URLs for you to call — useful when direct live-data tools are a better
fit than URL-building guidance.

**It is deliberately not bundled here.** A bundled MCP server can't be conditionally disabled, so
anyone without an MCP-enabled subscription would get a permanent connection error for a feature they
never asked for. Connect it yourself instead.

In every form below, the token is your client id and secret joined by a **single underscore** —
`abc123_def456`, not two separate values.

**Claude Code:**

```bash
claude mcp add --transport http xweather https://mcp.api.xweather.com/mcp \
  --header "Authorization: Bearer CLIENT_ID_CLIENT_SECRET"
```

Add `--scope user` for all projects, or `--scope project` to share it with a repo via `.mcp.json`.

**ChatGPT** (Plus, Pro, Business, Enterprise or Edu — custom connectors need a paid plan): Settings →
Connectors → advanced settings → enable **Developer mode**, then add a connector with this URL.
ChatGPT can't send custom headers, so the token goes in the query string instead:

```
https://mcp.api.xweather.com/mcp?api_key=CLIENT_ID_CLIENT_SECRET
```

**Claude.ai** (Pro or Max): Settings → Connectors → Add custom connector, same URL form as ChatGPT —
the desktop app also can't set headers.

Narrow the loaded tools with `&include_tags=general,forecast,summary` if people have other MCP servers
connected; all six groups at once crowds the model's tool choices. The `weather-api` skill documents
the server in full — all three auth methods, the six tool tag groups, filter precedence, and how to
read a failed connection.

## Layout

```
AGENTS.md                             conventions for agents working in this repo
.claude-plugin/marketplace.json       the Claude marketplace catalog
scripts/regenerate_references.py      regenerates the catalog-derived references
.github/workflows/                    weekly reference refresh
plugins/xweather/                     the plugin
├── .claude-plugin/plugin.json        Claude Code plugin manifest
├── .codex-plugin/plugin.json         ChatGPT and Codex plugin manifest
├── bin/                              xwrequest, xwmap — Claude Code puts these on PATH
└── skills/                           the five skills — the portable payload
    ├── weather-api/
    ├── raster-maps/
    ├── mapsgl/
    ├── mapsgl-apple/
    └── webhooks/
```

The marketplace catalog sits at the repository root and the plugin lives in `plugins/xweather/`, the
layout `anthropics/claude-code` uses. That nesting is required because the Claude app's marketplace
sync resolves relative plugin sources. Codex also recognizes this marketplace location for
compatibility, so a second catalog under `.agents/` would only duplicate release metadata.

There is still exactly one copy of the skills. Both plugin manifests and skills-compatible agents
load `plugins/xweather/skills/` instead of maintaining vendor-specific copies.

## Development

```bash
claude --plugin-dir ./plugins/xweather   # load in Claude Code without installing
claude plugin validate .                 # validate the manifests
python3 scripts/validate_packaging.py    # compare shared marketplace, manifest, and skill metadata
skills-ref validate ./plugins/xweather/skills/weather-api   # validate against the Agent Skills spec
```

`.github/workflows/validate-packaging.yml` runs the metadata comparison for relevant pushes and pull
requests. `skills-ref` comes from <https://github.com/agentskills/agentskills>. `/reload-plugins`
picks up edits without restarting a Claude Code session.

## Local checks before pushing

```bash
git config core.hooksPath .githooks    # once per clone
```

That enables a pre-push hook running `scripts/validate_packaging.py`, which asserts that the Claude
and Codex plugin manifests agree on every shared property, plus `claude plugin validate . --strict`
when the CLI is on PATH. Both are local and instant. `SKIP_PREPUSH=1 git push` bypasses it.

Run the packaging check on its own at any time:

```bash
python3 scripts/validate_packaging.py
```

The reference regeneration is deliberately *not* in the hook — it fetches ~60 doc pages, which is too
slow for a push. CI covers it.

## Regenerating the references

Five reference files are generated from live Xweather catalogs rather than hand-written, so they go
stale as the products change:

| File | Source |
|---|---|
| `plugins/xweather/skills/weather-api/references/endpoints.md` | `docs/api/weather-api/endpoints` + each endpoint's doc page |
| `plugins/xweather/skills/weather-api/references/examples.md` | each endpoint doc page's `exampleRequests` |
| `plugins/xweather/skills/weather-api/references/filters.md` | each endpoint doc page's filter and query tables |
| `plugins/xweather/skills/raster-maps/references/layers.md` | `docs/api/maps/layers` |
| `plugins/xweather/skills/mapsgl/references/layers.md` | `docs/api/mapsgl/layers` |
| the MapsGL CDN version pinned in `plugins/xweather/skills/mapsgl/SKILL.md` | `docs/api/releases/versions`, `mapsgl` key |

```bash
python3 scripts/regenerate_references.py           # rewrite in place
python3 scripts/regenerate_references.py --check   # exit 1 on drift, writes nothing
```

`.github/workflows/refresh-references.yml` runs the regeneration weekly and opens a PR when anything
drifts, and runs `--check` on any PR touching a generated file so a hand-edit fails loudly.

Three further files embed generated content inside hand-written prose:
`access-cost.md` and `map-units.md` carry multiplier tables, and `mapsgl/references/weather-layers.md` documents the catalog's render types, categories,
and which codes are composite. The script **reports** drift in those but won't rewrite them, since
regenerating would destroy the surrounding explanation.

Endpoint doc pages render their parameter tables client-side, so the script reads the Next.js RSC
payload out of the HTML rather than the rendered DOM. That's inherently coupled to Xweather's docs
stack; if it changes, the script refuses to write near-empty files and fails loudly instead of
quietly emptying a reference. The two layer catalogs are plain JSON endpoints and need no scraping.

## Releasing

Both plugin manifests set an explicit `version`, so installed users only receive a new packaged
release when it is bumped. Keep `version` in `plugins/xweather/.claude-plugin/plugin.json` and
`plugins/xweather/.codex-plugin/plugin.json` aligned with `metadata.version` in every `SKILL.md`.
Run `python3 scripts/validate_packaging.py` before releasing; CI rejects drift in names, versions,
display metadata, or the shared marketplace source.

**Never change the plugin's `name`** (`xweather`). It keys `enabledPlugins`, `pluginConfigs`, and
plugin installation state, and it namespaces the skills, so renaming breaks existing installs. To
change the label users see, update the Claude manifest and marketplace entry plus
`interface.displayName` in the Codex manifest.

## Requirements

- An Xweather account with the relevant product access. A free developer account works for
  evaluation, with a 2000×2000 static-map size cap.
- `python3` for the two helper scripts (standard library only — nothing to install).
- Optional: a subscription including MCP access, if you separately connect the Xweather MCP server.
- Optional: the Webhooks premium add-on, to actually receive pushed data. The `webhooks` skill is
  useful before that — you can build and test a receiver against the sample payloads first.
