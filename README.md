# Xweather API & Maps — Agent Skills

Four [Agent Skills](https://agentskills.io) for the Xweather developer platform: build Weather API
request URLs, generate Raster Maps imagery and tile URLs, work with the MapsGL WebGL SDK, and set up
pushed data delivery.

Agent Skills is an open standard stewarded by the Linux Foundation's Agentic AI Foundation, so these
work in any skills-compatible agent — **OpenAI Codex, Cursor, GitHub Copilot, VS Code, Gemini CLI,
Goose, OpenHands, JetBrains Junie, Claude Code**, and others. The repository also ships as a Claude
Code plugin for one-command install there.

## The skills

| Skill | Covers |
|---|---|
| `weather-api` | `data.api.xweather.com` request URLs — 59 endpoints, 8 actions, per-endpoint filter and query semantics, place and date formats, batch requests, and the access-cost model. Every URL comes with its cost. |
| `raster-maps` | `maps.api.xweather.com` URLs — static map images and XYZ tile templates across 159 layers, dash-joined data modifiers, opacity/blur/blend/scale-hsla, time offsets, and map-unit cost reporting. |
| `mapsgl` | The `@xweather/mapsgl` WebGL SDK — controllers for Mapbox GL, MapLibre GL, Google Maps and Leaflet, all 283 layers, styling, expressions, legends, timeline animation, and session-based cost. |
| `webhooks` | Pushed data delivery — receiver design, securing the endpoint, available data sets, retry and idempotency behaviour, and the registration details Xweather needs. |

## Install

### Claude Code

```
/plugin marketplace add vaisala-xweather/xweather-agent-skills
/plugin install xweather@vaisala-xweather
/reload-plugins
```

Installing prompts for nothing and configures nothing. A local path works when developing:
`/plugin marketplace add ./xweather-agent-skills`.

### OpenAI Codex

Codex discovers skills in `.agents/skills` directories — note the plural `.agents`:

| Scope | Path |
|---|---|
| Repository | `$REPO_ROOT/.agents/skills` (also `$CWD/.agents/skills` and parent dirs) |
| Personal | `$HOME/.agents/skills` |
| Machine-wide | `/etc/codex/skills` |

```bash
git clone https://github.com/vaisala-xweather/xweather-agent-skills.git
mkdir -p ~/.agents/skills
ln -s "$PWD"/xweather-agent-skills/skills/* ~/.agents/skills/
```

Symlinking rather than copying means `git pull` updates the skills in place. Restart Codex if a skill
doesn't appear. Individual skills can be disabled in `~/.codex/config.toml`:

```toml
[[skills.config]]
path = "/Users/you/.agents/skills/mapsgl/SKILL.md"
enabled = false
```

### Other skills-compatible agents

Cursor, GitHub Copilot, VS Code, Gemini CLI, Goose, OpenHands, JetBrains Junie and others all read
the same `SKILL.md` files but look in different directories. Clone the repo and symlink
`skills/*` into whichever location your client documents — <https://agentskills.io/clients> links the
per-tool instructions.

### ChatGPT (the app, not Codex)

The consumer ChatGPT app reads **neither** Agent Skills nor `AGENTS.md` — only MCP connectors. These
skills won't load there. For live weather data in ChatGPT, connect Xweather's hosted MCP server
instead; see [The Xweather MCP server](#the-xweather-mcp-server) below.

## Helper scripts

Two standard-library Python 3 programs, bundled with the skills that use them:

| Script | Purpose |
|---|---|
| `skills/weather-api/scripts/xwrequest.py` | Issue a Weather API request. Prints the credential-redacted URL, HTTP status, accesses charged with the multiplier breakdown, remaining allowance, and the response. |
| `skills/raster-maps/scripts/xwmap.py` | Issue a Raster Maps request. Prints the redacted URL and map-unit estimate, saves the image. `--estimate-only` computes cost without sending anything. |

Both read credentials from the environment, so secrets stay out of shell history and out of the
printed output:

```bash
export XWEATHER_CLIENT_ID='…' XWEATHER_CLIENT_SECRET='…'

python3 skills/weather-api/scripts/xwrequest.py '/observations/seattle,wa?filter=allstations&limit=3'
python3 skills/raster-maps/scripts/xwmap.py 'flat,radar,admin/800x600/minneapolis,mn,7/current.png' -o radar.png
python3 skills/raster-maps/scripts/xwmap.py 'flat,lightning-strikes/800x600/dallas,tx,7/current.png' --estimate-only
```

Claude Code additionally exposes them as bare `xwrequest` / `xwmap` commands via `bin/`, but the
skills never assume that.

## Credentials

Keys come from the Apps section of <https://data.portal.xweather.com/account/keys>. Each key pair is
bound to a **namespace** — a top-level domain for web, or a reverse-DNS bundle id for mobile. A
request from outside that namespace fails with `unauthorized_namespace` on the Weather API, or a 403
`authorization_error` on Raster Maps, regardless of whether the URL is otherwise correct.

Raster Maps puts credentials in the URL *path*, so a tile URL used in client-side JavaScript exposes
the key pair to anyone viewing the page. The namespace binding is what limits the damage.

## The Xweather MCP server

Xweather hosts an MCP server at `https://mcp.api.xweather.com/mcp` that answers weather questions
directly instead of producing URLs for you to call — useful in agents that consume MCP but not
skills, including the ChatGPT app.

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
AGENTS.md                        conventions for agents working in this repo
skills/                          the four skills — the portable payload
├── weather-api/
├── raster-maps/
├── mapsgl/
└── webhooks/
scripts/regenerate_references.py regenerates the catalog-derived references
bin/                             xwrequest, xwmap — Claude Code puts these on PATH
.claude-plugin/
├── plugin.json                  Claude Code plugin manifest (repo root is the plugin)
└── marketplace.json             Claude Code marketplace catalog
.github/workflows/               weekly reference refresh
```

The repository root *is* the Claude Code plugin, so `skills/` has exactly one canonical copy — no
duplication and no symlinks. Other agents read `skills/` directly.

## Development

```bash
claude --plugin-dir .            # load in Claude Code without installing
claude plugin validate .         # validate the manifests
skills-ref validate ./skills/weather-api   # validate against the Agent Skills spec
```

`skills-ref` comes from <https://github.com/agentskills/agentskills>. `/reload-plugins` picks up edits
without restarting a Claude Code session.

## Regenerating the references

Five reference files are generated from live Xweather catalogs rather than hand-written, so they go
stale as the products change:

| File | Source |
|---|---|
| `weather-api/references/endpoints.md` | `docs/api/weather-api/endpoints` + each endpoint's doc page |
| `weather-api/references/examples.md` | each endpoint doc page's `exampleRequests` |
| `weather-api/references/filters.md` | each endpoint doc page's filter and query tables |
| `raster-maps/references/layers.md` | `docs/api/maps/layers` |
| `mapsgl/references/layers.md` | `docs/api/mapsgl/layers` |

```bash
python3 scripts/regenerate_references.py           # rewrite in place
python3 scripts/regenerate_references.py --check   # exit 1 on drift, writes nothing
```

`.github/workflows/refresh-references.yml` runs the regeneration weekly and opens a PR when anything
drifts, and runs `--check` on any PR touching a generated file so a hand-edit fails loudly.

Three further files embed generated content inside hand-written prose:
`weather-api/references/access-cost.md` and `raster-maps/references/map-units.md` carry multiplier
tables, and `mapsgl/references/weather-layers.md` documents the catalog's render types, categories,
and which codes are composite. The script **reports** drift in those but won't rewrite them, since
regenerating would destroy the surrounding explanation.

Endpoint doc pages render their parameter tables client-side, so the script reads the Next.js RSC
payload out of the HTML rather than the rendered DOM. That's inherently coupled to Xweather's docs
stack; if it changes, the script refuses to write near-empty files and fails loudly instead of
quietly emptying a reference. The two layer catalogs are plain JSON endpoints and need no scraping.

## Releasing

`.claude-plugin/plugin.json` sets an explicit `version`, so **Claude Code users only receive updates
when that field is bumped**. Bump it on every release, and keep `metadata.version` in each `SKILL.md`
in step.

**Never change the plugin's `name`** (`xweather`). It keys `enabledPlugins`, `pluginConfigs`, and
every `/plugin install`, and it namespaces the skills, so renaming breaks existing installs. To change
the label users see, edit `displayName` in both `plugin.json` and the `marketplace.json` entry.

## Requirements

- An Xweather account with the relevant product access. A free developer account works for
  evaluation, with a 2000×2000 static-map size cap.
- `python3` for the two helper scripts (standard library only — nothing to install).
- Optional: a subscription including MCP access, if you separately connect the Xweather MCP server.
- Optional: the Webhooks premium add-on, to actually receive pushed data. The `webhooks` skill is
  useful before that — you can build and test a receiver against the sample payloads first.
