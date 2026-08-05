#!/usr/bin/env python3
"""Regenerate the skill reference files that are derived from live Xweather catalogs.

Six reference files are generated rather than hand-written, and drift out of date as Xweather
ships changes:

    plugins/xweather/skills/weather-api/references/endpoints.md   from docs/api/weather-api/endpoints + doc pages
    plugins/xweather/skills/weather-api/references/examples.md    from each endpoint doc page's exampleRequests
    plugins/xweather/skills/weather-api/references/filters.md     from each endpoint doc page's filter/query tables
    plugins/xweather/skills/raster-maps/references/layers.md      from docs/api/maps/layers
    plugins/xweather/skills/mapsgl/references/layers.md           from docs/api/mapsgl/layers
    plugins/xweather/skills/mapsgl-apple/references/layers.md     from the Apple SDK's DocC symbol index

Three more files embed generated content inside hand-written prose, so they are checked rather than
rewritten; the script reports when their groupings no longer match the live catalogs:

    plugins/xweather/skills/weather-api/references/access-cost.md
    plugins/xweather/skills/raster-maps/references/map-units.md
    plugins/xweather/skills/mapsgl/references/weather-layers.md

Usage:
    python3 scripts/regenerate_references.py            # rewrite in place
    python3 scripts/regenerate_references.py --check    # exit 1 if anything would change

--check is what CI runs. It writes nothing.

The Apple SDK has no public layer catalog endpoint — its supported set is the
`WeatherService.LayerCode` enum, which is a subset of the JS catalog and uses Swift case names rather
than the JS string codes (`air-quality-pm2p5` is `.particulateMatter2p5Micron`). The two cannot be
mapped mechanically, so that file is generated from the SDK's published DocC symbol index instead.

The endpoint doc pages render their parameter tables client-side, so the useful data lives in the
Next.js RSC payload embedded in the HTML rather than in the rendered DOM. That is what `_payload`
extracts. If Xweather migrates off Next.js this script breaks loudly (no endpoints parsed) rather
than silently producing empty files — see _fail_if_empty.
"""

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

DOCS = "https://www.xweather.com/docs"
WX_CATALOG = f"{DOCS}/api/weather-api/endpoints"
MAPS_CATALOG = f"{DOCS}/api/maps/layers"
MGL_CATALOG = f"{DOCS}/api/mapsgl/layers"
RELEASES = f"{DOCS}/api/releases/versions"
APPLE_DOCC = "https://cdn.aerisapi.com/sdk/ios/mapsgl/docs/v%s/index/index.json"

ROOT = pathlib.Path(__file__).resolve().parent.parent
WX_REF = ROOT / "plugins/xweather/skills/weather-api/references"
RM_REF = ROOT / "plugins/xweather/skills/raster-maps/references"
MGL_REF = ROOT / "plugins/xweather/skills/mapsgl/references"
APPLE_REF = ROOT / "plugins/xweather/skills/mapsgl-apple/references"

UA = {"User-Agent": "Mozilla/5.0 (xweather-agent-skills reference regeneration)"}
PUSH = re.compile(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', re.S)


# ---------------------------------------------------------------- fetching


def _get(url, tries=3):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", "ignore")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            last = exc
            time.sleep(1 + attempt * 2)
    raise SystemExit(f"error: could not fetch {url}: {last}")


def _json(url):
    return json.loads(_get(url))


def _payload(url):
    """Concatenate the RSC payload chunks embedded in a Next.js page."""
    return "".join(json.loads(m.group(1)) for m in PUSH.finditer(_get(url)))


def _balanced(text, start, opener, closer):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == opener:
            depth += 1
        elif text[i] == closer:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def _obj(text, key):
    m = re.search(r'"%s":\{' % re.escape(key), text)
    if not m:
        return None
    raw = _balanced(text, m.end() - 1, "{", "}")
    try:
        return json.loads(raw, strict=False)
    except (ValueError, TypeError):
        return None


def _arr(text, key):
    m = re.search(r'"%s":\[' % re.escape(key), text)
    if not m:
        return None
    raw = _balanced(text, m.end() - 1, "[", "]")
    try:
        return json.loads(raw, strict=False)
    except (ValueError, TypeError):
        return None


def _scalar(text, key):
    m = re.search(r'"%s":("(?:[^"\\]|\\.)*"|null|-?\d+)' % re.escape(key), text)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def _clean(value):
    text = re.sub(r"<br\s*/?>", " ", str(value))
    text = re.sub(r"</?[a-zA-Z][^>]*>", "", text)
    return re.sub(r"[ \t]+", " ", text).replace("\n", " ").strip()


def _rows(block):
    if not block:
        return []
    out = []
    for row in block.get("data", []):
        values = list(row.values())
        out.append((
            _clean(values[0] if values else ""),
            _clean(values[1] if len(values) > 1 else ""),
        ))
    return out


def _codes(items):
    return ", ".join("`%s`" % i for i in items) if items else "—"


# ---------------------------------------------------------------- weather api


def fetch_weather_api():
    catalog = _json(WX_CATALOG)
    endpoints = catalog.get("endpoint") or {}
    if not endpoints:
        raise SystemExit(f"error: no endpoints in {WX_CATALOG} — catalog shape may have changed")

    merged = {}
    for slug, meta in endpoints.items():
        text = _payload(f"{DOCS}/weather-api/endpoints/{slug}")
        entry = dict(meta)
        entry["filters_desc"] = _obj(text, "filters")
        entry["queries_desc"] = _obj(text, "queryProps")
        entry["sort_desc"] = _obj(text, "sortableFields")
        entry["examples"] = _arr(text, "exampleRequests")
        entry["dataRange"] = _scalar(text, "dataRange")
        entry["dataCoverage"] = _arr(text, "dataCoverage")
        entry["accessMultiplier"] = _scalar(text, "accessMultiplier")
        merged[slug] = entry
        time.sleep(0.1)
    return merged


def render_endpoints(endpoints):
    out = [
        "# Xweather Weather API — endpoint catalog",
        "",
        "Every endpoint below is a path under `https://data.api.xweather.com`. Full request shape:",
        "`https://data.api.xweather.com/{endpoint}/{action}/{:id}?{params}&client_id=…&client_secret=…`",
        "",
        "`Cost` is the endpoint access multiplier — the base token cost of one request before spatial and",
        "temporal multipliers are applied (see `parameters.md` → Cost headers).",
        "",
        "Filter tokens containing `#` are templates, not literals: `#hr` → `1hr`, `3hr`, `6hr`, `24hr`;",
        "`#min` → `1min`, `5min`, `15min`; `day#` → `day1` … `day8`. A trailing `*` (only `pop*`, on",
        "`/stormcells/summary`) marks a property usable with the `affects` action only.",
        "",
        "Regenerate this list from the live catalog at any time:",
        "`curl -s https://www.xweather.com/docs/api/weather-api/endpoints` (JSON: `{ endpoint: {...}, action: {...} }`).",
        "",
        "---",
        "",
    ]
    for entry in sorted(endpoints.values(), key=lambda e: e["title"]):
        out.append("## `/%s`" % entry["title"])
        out.append("")
        out.append(_clean(entry.get("description") or ""))
        out.append("")
        meta = []
        coverage = entry.get("dataCoverage") or entry.get("region") or []
        if coverage:
            meta.append("Coverage: %s" % ", ".join(coverage))
        if entry.get("dataRange"):
            meta.append("Range: %s" % entry["dataRange"])
        if entry.get("update_interval") and entry["update_interval"] != "N/A":
            meta.append("Updates: %s" % entry["update_interval"])
        mult = entry.get("accessMultiplier")
        if mult is None:
            mult = entry.get("multiplier")
        if mult is not None:
            meta.append("Cost: x%s" % mult)
        if meta:
            out.append("*%s*" % " · ".join(meta))
            out.append("")
        actions = [
            ":id" if a == "id" else (":all" if a == "all" else a)
            for a in (entry.get("actions") or [])
        ]
        out.append("| | |")
        out.append("|---|---|")
        out.append("| Actions | %s |" % _codes(actions))
        out.append("| Params | %s |" % _codes(entry.get("params")))
        out.append("| Filters | %s |" % _codes(entry.get("filters")))
        out.append("| Query props | %s |" % _codes(entry.get("queries")))
        out.append("| Sort fields | %s |" % _codes(entry.get("sort")))
        out.append("")

        # Path-parameter endpoints need their accepted values spelled out; the catalog does not
        # carry them, so these two notes are maintained here by hand.
        if entry["title"] == "impacts/:activity":
            out += [
                "`:activity` is part of the path and required — `/impacts/general/55403`:",
                "`general` (most outdoor activity: fire weather, severe, wind, lightning, air quality, temperature,",
                "snow, rain) · `roadway_trucking` (severe, wind, lightning, snow, visibility, rollover risk,",
                "temperature) · `maritime_small_craft` (wind, severe, lightning, waves) ·",
                "`maritime_large_vessel` (waves, temperature, visibility, snow, wind).",
                "",
            ]
        if entry["title"] == "indices/:type":
            out += [
                "`:type` is part of the path and required — `/indices/migraine/55403`. Health indices:",
                "`arthritis`, `coldflu`, `migraine`, `sinus`. Activity indices: `outdoors`, `golf`, `biking`,",
                "`swimming`, `campfires`, `bees`.",
                "",
            ]

        out.append("Docs: https://www.xweather.com/docs/weather-api/endpoints/%s" % entry["id"])
        out.append("")
    return "\n".join(out)


def render_examples(endpoints):
    out = [
        "# Documented example requests, by endpoint",
        "",
        "Copied verbatim from each endpoint's documentation page. Paths are relative to",
        "`https://data.api.xweather.com`; append `&client_id=…&client_secret=…` to every one.",
        "",
        "These are the highest-signal reference for URL shape — when a request resembles one of these,",
        "copy its structure rather than inventing parameters.",
        "",
        "---",
        "",
    ]
    for entry in sorted(endpoints.values(), key=lambda e: e["title"]):
        examples = entry.get("examples") or []
        if not examples:
            continue
        out.append("## `/%s`" % entry["title"])
        out.append("")
        for ex in examples:
            out.append("- `%s`  " % _clean(ex.get("url", "")).rstrip("&?"))
            out.append("  %s" % _clean(ex.get("description", "")))
        out.append("")
    return "\n".join(out)


def render_filters(endpoints):
    out = [
        "# Filter and query-property meanings, by endpoint",
        "",
        "`filter=` selects *which* records / intervals come back; `query=` filters on record values",
        "(see `parameters.md` → Advanced queries for the operator syntax). Multiple filters are combined",
        "with `,` for AND and `;` for OR.",
        "",
        "Only endpoints that document filters or query properties appear here. For the complete token list",
        "per endpoint — including endpoints with no prose descriptions — see `endpoints.md`.",
        "",
        "---",
        "",
    ]
    for entry in sorted(endpoints.values(), key=lambda e: e["title"]):
        filters = _rows(entry.get("filters_desc"))
        queries = _rows(entry.get("queries_desc"))
        if not filters and not queries:
            continue
        out.append("## `/%s`" % entry["title"])
        out.append("")
        if filters:
            out.append("**Filters**")
            out.append("")
            out += ["- `%s` — %s" % (a, b) for a, b in filters]
            out.append("")
        if queries:
            out.append("**Query properties**")
            out.append("")
            out += ["- `%s` — %s" % (a, b) for a, b in queries]
            out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- raster maps

MAPS_CATEGORY_ORDER = [
    "Base Maps", "Radar + Satellite", "Observations", "Forecasts", "Severe", "Lightning",
    "Air Quality", "Maritime", "Tropical", "Outlooks", "Overlays", "Masks", "Uncategorized",
]


def fetch_maps_layers():
    layers = _json(MAPS_CATALOG).get("layers") or []
    if not layers:
        raise SystemExit(f"error: no layers in {MAPS_CATALOG} — catalog shape may have changed")
    return layers


def _dedupe_coverage(layer):
    """The catalog repeats coverage in Title Case and slug form; keep one of each."""
    seen, out = set(), []
    for item in layer.get("dataCoverage") or []:
        key = item.lower().replace("-", " ")
        if key not in seen:
            seen.add(key)
            out.append(item)
    return ", ".join(out)


def render_layers(layers):
    grouped = {}
    for layer in layers:
        cats = [c for c in (layer.get("categories") or []) if c != "Popular"] or ["Uncategorized"]
        grouped.setdefault(cats[0], []).append(layer)

    out = [
        "# Raster Maps layer catalog",
        "",
        "%d layers. The layer code is what goes in the `{layers}` path segment; combine up to 10 with commas."
        % len(layers),
        "",
        "`x1` / `x5` / `x10` is the layer multiplier — its weight when computing map units (see `map-units.md`).",
        "",
        "**Modifiers** listed on a layer are appended to the code with a dash, one option per modifier group:",
        "`alerts` + Category `severe` → `alerts-severe`; `temperatures` + Source `rtma` → `temperatures-rtma`.",
        "Modifier groups are independent, so a layer with two groups can take one option from each —",
        "`alerts-severe-warnings`. These are different from the *layer modifiers* (`:opacity`, `:blur()`,",
        "`:blend()`) in `modifiers.md`, which attach with a colon.",
        "",
        "Where a modifier below reads *(options not enumerated in the catalog)*, the group exists but the",
        "catalog publishes no values — check that layer's doc page or test the request instead of guessing a",
        "suffix.",
        "",
        "Regenerate from the live catalog: `curl -s https://www.xweather.com/docs/api/maps/layers`",
        "",
        "---",
        "",
    ]

    ordered = MAPS_CATEGORY_ORDER + sorted(set(grouped) - set(MAPS_CATEGORY_ORDER))
    emitted = set()
    for category in ordered:
        items = grouped.get(category)
        if not items:
            continue
        out.append("## %s" % category)
        out.append("")
        for layer in sorted(items, key=lambda l: l["id"]):
            if layer["id"] in emitted:
                continue
            emitted.add(layer["id"])
            out.append("### `%s` — %s" % (layer["id"], layer["title"]))
            out.append("")
            if layer.get("description"):
                out.append(layer["description"])
            meta = ["x%s" % layer.get("multiplier")]
            coverage = _dedupe_coverage(layer)
            if coverage:
                meta.append("Coverage: %s" % coverage)
            if layer.get("dataRange"):
                meta.append("Range: %s" % layer["dataRange"])
            if layer.get("updateInterval"):
                meta.append("Updates: %s" % layer["updateInterval"])
            out.append("")
            out.append("*%s*" % " · ".join(meta))
            for mod in layer.get("modifiers") or []:
                options = mod.get("options") or {}
                required = " **(required)**" if mod.get("required") else ""
                if options:
                    rendered = ", ".join("`-%s` %s" % (k.strip(), v) for k, v in options.items())
                else:
                    rendered = "_(options not enumerated in the catalog — see the layer docs)_"
                out.append("")
                out.append("- Modifier **%s**%s: %s" % (mod.get("name"), required, rendered))
            out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- mapsgl

MGL_CATEGORY_ORDER = [
    "Radar + Satellite", "Conditions", "Forecasts", "Severe", "Lightning", "Tropical",
    "Maritime", "Air Quality", "Climate", "Roads", "Admin", "Other", "Uncategorized",
]


def fetch_mapsgl_layers():
    layers = _json(MGL_CATALOG).get("layers") or []
    if not layers:
        raise SystemExit(f"error: no layers in {MGL_CATALOG} — catalog shape may have changed")
    return layers


def render_mapsgl_layers(layers):
    composite = sorted(l["id"] for l in layers if l.get("type") == "none")
    by_cost = {}
    for layer in layers:
        by_cost.setdefault(layer.get("multiplier", 1), []).append(layer["id"])

    grouped = {}
    for layer in layers:
        cats = [c for c in (layer.get("categories") or []) if c != "Popular"] or ["Uncategorized"]
        grouped.setdefault(cats[0], []).append(layer)

    out = [
        "# MapsGL weather layer catalog",
        "",
        "%d built-in weather layers. The **code** is the string passed to"
        % len(layers),
        "`controller.addWeatherLayer(code)` — and to `getWeatherLayer`, `hasWeatherLayer`,",
        "`removeWeatherLayer`, and `setWeatherLayerVisibility`. It is **not** the resulting"
        " `WebGLLayer`'s",
        "`id`; see `weather-layers.md` for that distinction, which is the most common source of",
        "silently-failing style updates.",
        "",
        "This is a snapshot, regenerated from the live catalog by `scripts/regenerate_references.py`",
        "and refreshed weekly in CI. For **account-specific availability** — what a given",
        "subscription can actually render — call `controller.weatherProvider.getLayerMetadata()` at",
        "runtime instead; this file reflects the public catalog, not entitlements. If a code here is",
        "rejected at runtime, that's a plan question, not a typo.",
        "",
        "Each entry reads: *render type · animatable · cost multiplier · coverage · data range ·"
        " update interval*.",
        "",
        "The **render type** determines which `paint` namespace styles the layer — a `sample` layer",
        "is styled through `paint.sample`, a `line` layer through `paint.stroke`, and so on. See",
        "`styles.md` for the property tables per type.",
        "",
        "---",
        "",
        "## Composite layers",
        "",
        "These %d codes have render type `none`, meaning they expand into **several** sub-layers."
        % len(composite),
        "`addWeatherLayer` and `getWeatherLayer` return an **array** of `WebGLLayer` for them, so",
        "iterate before setting paint properties:",
        "",
        " · ".join("`%s`" % c for c in composite),
        "",
        "## Cost multipliers",
        "",
        "A layer's multiplier weights its contribution to session/access billing. It has no effect on",
        "rendering.",
        "",
    ]
    # List non-x1 codes exhaustively. Summarising them by name pattern reads well but is wrong:
    # plenty of `air-quality-*` and `*road-weather-*` layers (the `-text` label variants and the
    # `*-summary-*` road layers) are x1, so a pattern would overstate their cost.
    for mult in sorted(by_cost, reverse=True):
        ids = sorted(by_cost[mult])
        if mult == 1:
            out.append(
                "- **x1** — the remaining %d layers, i.e. anything not listed above." % len(ids)
            )
        else:
            out.append("- **x%s** (%d):" % (mult, len(ids)))
            out.append("  %s" % " · ".join("`%s`" % i for i in ids))
    out += [
        "",
        "Cost does not follow the layer name. `air-quality-o3` is x5 while `air-quality-o3-text` —",
        "its label variant — is x1, and the per-region `road-weather-risk-*` layers are x5 while",
        "`road-weather-summary-*` are x1. Check the entry rather than inferring from the prefix.",
        "",
        "---",
        "",
    ]

    ordered = MGL_CATEGORY_ORDER + sorted(set(grouped) - set(MGL_CATEGORY_ORDER))
    emitted = set()
    for category in ordered:
        items = grouped.get(category)
        if not items:
            continue
        out.append("## %s" % category)
        out.append("")
        for layer in sorted(items, key=lambda l: l["id"]):
            if layer["id"] in emitted:
                continue
            emitted.add(layer["id"])
            out.append("### `%s` — %s" % (layer["id"], layer["title"]))
            out.append("")
            if layer.get("description"):
                out.append(layer["description"])
                out.append("")
            meta = [layer.get("type") or "?"]
            meta.append("animatable" if layer.get("animatable") else "static")
            meta.append("x%s" % layer.get("multiplier"))
            coverage = ", ".join(layer.get("dataCoverage") or [])
            if coverage:
                meta.append("Coverage: %s" % coverage)
            data_range = (layer.get("dataRange") or "").strip()
            if data_range and data_range != "-":
                meta.append("Range: %s" % data_range)
            interval = (layer.get("updateInterval") or "").strip()
            if interval and interval != "-":
                meta.append("Updates: %s" % interval)
            extra = [c for c in (layer.get("categories") or []) if c != category]
            if extra:
                meta.append("Also: %s" % ", ".join(extra))
            out.append("*%s*" % " · ".join(meta))
            out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- mapsgl apple sdk

# Which `paint` sub-object each layer descriptor exposes, and therefore what an override has to
# reach for. Derived from the descriptors' `paint` types in the same DocC index this file is built
# from; kept here as prose because the paint type names alone don't tell a reader where to write.
APPLE_PAINT_PATHS = {
    "SampleLayerDescriptor": ("sample", "`paint.opacity`, `paint.sample`"),
    "RasterLayerDescriptor": ("raster", "`paint.opacity`, `paint.raster`"),
    "ParticleLayerDescriptor": ("particles", "`paint.opacity`, `paint.sample`, `paint.particle`"),
    "GridLayerDescriptor": (
        "grid",
        "`paint.opacity`, `paint.sample`, `paint.grid`, `paint.fill`, `paint.stroke`, "
        "`paint.icon`, `paint.symbol`",
    ),
    "ContourLayerDescriptor": ("contour", "`paint.opacity`, `paint.sample`, `paint.contour`"),
    "FillLayerDescriptor": ("fill", "`paint.opacity`, `paint.fill`, `paint.stroke`"),
    "LineLayerDescriptor": ("line", "`paint.opacity`, `paint.stroke`"),
    "CircleLayerDescriptor": (
        "circle", "`paint.opacity`, `paint.fill`, `paint.stroke`, `paint.circle`"
    ),
    "SymbolLayerDescriptor": (
        "symbol", "`paint.opacity`, `paint.fill`, `paint.stroke`, `paint.icon`, `paint.text`"
    ),
    "HeatmapLayerDescriptor": ("heatmap", "`paint.opacity`, `paint.heatmap`"),
}

APPLE_TYPE_ORDER = [
    "SampleLayerDescriptor", "RasterLayerDescriptor", "ParticleLayerDescriptor",
    "GridLayerDescriptor", "ContourLayerDescriptor", "FillLayerDescriptor", "LineLayerDescriptor",
    "CircleLayerDescriptor", "SymbolLayerDescriptor", "HeatmapLayerDescriptor",
]


def _docc_find(node, title):
    """Depth-first search of a DocC index tree by node title.

    DocC's index nests children under a symbol but uses flat `groupMarker` entries as section
    headings rather than real parents, so a symbol's members are its *direct* children.
    """
    if node.get("title") == title:
        return node
    for child in node.get("children") or []:
        found = _docc_find(child, title)
        if found is not None:
            return found
    return None


def fetch_apple_layers(version):
    """Weather layer configurations from the Apple SDK's DocC symbol index.

    Returns (codes, configs) where `codes` is the ordered list of `WeatherService.LayerCode` case
    names and `configs` maps each case name to its layer/source descriptor types. A composite layer
    has no single `layer`, so its layer descriptor comes back as None.
    """
    index = _json(APPLE_DOCC % version)
    languages = index.get("interfaceLanguages") or {}
    roots = languages.get("swift") or []
    if not roots:
        raise SystemExit(
            f"error: no swift symbols in {APPLE_DOCC % version} — the DocC index shape may have "
            "changed, or that version was never published"
        )

    service = _docc_find(roots[0], "WeatherService")
    layer_code = _docc_find(roots[0], "WeatherService.LayerCode")
    if service is None or layer_code is None:
        raise SystemExit(
            "error: WeatherService / WeatherService.LayerCode not found in the Apple SDK DocC index "
            "— the SDK's public API may have been restructured"
        )

    codes = [
        child["title"][len("case "):]
        for child in layer_code.get("children") or []
        if child.get("type") == "case"
    ]
    if not codes:
        raise SystemExit("error: no WeatherService.LayerCode cases found in the Apple SDK DocC index")

    configs = {}
    for child in service.get("children") or []:
        title = child.get("title", "")
        if child.get("type") != "struct" or not title.startswith("WeatherService."):
            continue
        entry = {"struct": title, "layer": None, "source": None, "composite": False}
        for member in child.get("children") or []:
            name = member.get("title", "")
            for prefix in ("var layer:", "let layer:"):
                if name.startswith(prefix):
                    entry["layer"] = name.split(":", 1)[1].strip()
            for prefix in ("var layers:", "let layers:"):
                if name.startswith(prefix):
                    entry["composite"] = True
            for prefix in ("var source:", "let source:"):
                if name.startswith(prefix):
                    entry["source"] = name.split(":", 1)[1].strip()
        # `WeatherService.Temperatures` is the config struct for `.temperatures`; the SDK's naming
        # is exactly this consistent, and render_apple_layers() fails loudly if it stops being.
        case = title[len("WeatherService."):]
        configs[case[0].lower() + case[1:]] = entry
    return codes, configs


def render_apple_layers(version, codes, configs):
    missing = [c for c in codes if c not in configs]
    if missing:
        raise SystemExit(
            "error: %d WeatherService.LayerCode cases have no matching configuration struct (%s) — "
            "the SDK no longer names config structs after their layer code, so this generator's "
            "pairing assumption is broken."
            % (len(missing), ", ".join(missing[:5]))
        )

    composite = sorted(c for c in codes if configs[c]["composite"])
    by_type = {}
    for case in codes:
        entry = configs[case]
        if entry["composite"]:
            continue
        by_type.setdefault(entry["layer"] or "unknown", []).append(case)

    unknown = sorted(set(by_type) - set(APPLE_PAINT_PATHS))
    out = [
        "# MapsGL Apple SDK — weather layer catalog",
        "",
        "%d built-in weather layers, generated from the Apple SDK's published DocC symbol index."
        % len(codes),
        "",
        "**In Swift a layer is a `WeatherService.LayerCode` case, not a string.**"
        " `.temperatures`, not `\"temperatures\"`.",
        "The case names are *not* mechanical transforms of the JS/Raster Maps layer codes —"
        " `air-quality-pm2p5`",
        "is `.particulateMatter2p5Micron` and `air-quality-no2` is `.nitrogenDioxide` — so never"
        " convert a code",
        "from the web docs by hand. Look it up here, or let the compiler complete it.",
        "",
        "The Apple SDK also supports **fewer** layers than the JS SDK (%d vs. 283). If a layer exists"
        % len(codes),
        "in the JS catalog and not here, it is not available on Apple platforms — that is a real gap,"
        " not a",
        "naming problem.",
        "",
        "Each entry reads: **`.case`** → its configuration struct. The struct is what you instantiate"
        " to",
        "override defaults:",
        "",
        "```swift",
        "var config = WeatherService.Temperatures(service: controller.service)",
        "config.layer.paint.opacity = 0.5   // opacity is on the layer paint, not on `paint.sample`",
        "try controller.addWeatherLayer(config: config)",
        "```",
        "",
        "Every configuration struct carries the same four members: `code`, `layer` (the descriptor —"
        " paint and",
        "quality live here), `legend`, and `presentation` (the data-inspector formatter). Composite"
        " layers are",
        "the exception; see below.",
        "",
        "For each layer's **description, animatability, coverage, data range, update interval and cost"
        " multiplier**,",
        "see the shared MapsGL layer documentation at https://www.xweather.com/docs/mapsgl/weather-layers"
        " — those",
        "attributes are properties of the data, not of the SDK, and are identical across SDKs. For what"
        " the",
        "authenticated account may actually render, ask at runtime:",
        "",
        "```swift",
        "controller.service.loadLayerMetadata { result in ... }   // -> [WeatherLayerMetadata]",
        "```",
        "",
        "Generated from the DocC index for SDK %s. Regenerate with"
        " `python3 scripts/regenerate_references.py`;" % version,
        "the version is resolved from the releases endpoint, so this list tracks the current release.",
        "",
        "---",
        "",
        "## Composite layers",
        "",
        "These %d cases expand into **several** sub-layers. Their configuration struct exposes"
        % len(composite),
        "`let layers: [any WeatherLayerConfiguration]` instead of a single `layer` — and it is a `let`,"
        " so",
        "**you cannot override paint on a composite through its own config struct**. To restyle one,"
        " add the",
        "constituent layers individually instead (e.g. `.stormcellsTracks` and `.stormcellsPositions`"
        " rather",
        "than `.stormcells`).",
        "",
        " · ".join("`.%s`" % c for c in composite),
        "",
        "---",
        "",
    ]

    ordered = APPLE_TYPE_ORDER + unknown
    for descriptor in ordered:
        cases = by_type.get(descriptor)
        if not cases:
            continue
        kind, paint = APPLE_PAINT_PATHS.get(
            descriptor, ("?", "_(unrecognized descriptor — check the DocC reference)_")
        )
        out.append("## `%s` — render type `%s` (%d)" % (descriptor, kind, len(cases)))
        out.append("")
        out.append("Paint namespaces: %s" % paint)
        out.append("")
        for case in sorted(cases):
            out.append("- `.%s` → `%s`" % (case, configs[case]["struct"]))
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- released versions


def fetch_released_version(product):
    """Current released version for a product id from the releases endpoint.

    This is the release source of truth. It can lag npm: `@xweather/mapsgl` has published a higher
    version than this endpoint reports, and cdn.aerisapi.com serves those newer paths too, so a URL
    resolving is not evidence it's the current release. Always prefer this value.
    """
    products = _json(RELEASES).get("products") or {}
    if product not in products:
        raise SystemExit(
            "error: no %r product in %s — available: %s"
            % (product, RELEASES, ", ".join(sorted(products)) or "none")
        )
    version = (products[product].get("version") or "").strip()
    if not re.fullmatch(r"\d+(\.\d+)*", version):
        raise SystemExit(f"error: unexpected version {version!r} for {product} at {RELEASES}")
    return version


def verify_mapsgl_cdn(version):
    """Confirm the CDN actually serves this version before pinning examples to it.

    The releases endpoint and the CDN are separate systems. If the endpoint ever announces a version
    before the CDN has it, pinning blindly would commit example code whose <script> and <link> tags
    404 — and CI would open a PR containing it. Two HEAD requests are cheap insurance.
    """
    base = "https://cdn.aerisapi.com/sdk/js/mapsgl/%s/aerisweather.mapsgl" % version
    for url in ("%s.js" % base, "%s.css" % base):
        req = urllib.request.Request(url, method="HEAD", headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status != 200:
                    raise SystemExit(
                        "error: %s returned HTTP %s — the releases endpoint reports %s but the CDN "
                        "does not serve it yet. Refusing to pin examples to a broken URL."
                        % (url, resp.status, version)
                    )
        except urllib.error.HTTPError as exc:
            raise SystemExit(
                "error: %s returned HTTP %s — the releases endpoint reports %s but the CDN does not "
                "serve it yet. Refusing to pin examples to a broken URL."
                % (url, exc.code, version)
            )
        except urllib.error.URLError as exc:
            raise SystemExit(f"error: could not reach {url}: {exc.reason}")


def apply_mapsgl_version(version):
    """Point every MapsGL CDN URL in the skill at the released version.

    Only the version segment of cdn.aerisapi.com/sdk/js/mapsgl/<version>/ URLs is touched, plus the
    one sentence that names the pinned fallback. Returns (path, old, new) if anything changed.
    """
    path = MGL_REF.parent / "SKILL.md"
    text = path.read_text()

    found = set(re.findall(r"sdk/js/mapsgl/(\d+(?:\.\d+)*)/", text))
    if not found:
        raise SystemExit(
            "error: no cdn.aerisapi.com/sdk/js/mapsgl/<version>/ URLs found in %s — the skill's CDN "
            "guidance may have been restructured; update apply_mapsgl_version()." % path.name
        )
    if found == {version}:
        return None

    updated = re.sub(r"(sdk/js/mapsgl/)\d+(?:\.\d+)*(/)", r"\g<1>%s\g<2>" % version, text)
    # The prose names the pinned version as the offline fallback; keep it in step.
    updated = re.sub(
        r"^`\d+(?:\.\d+)*` above is the version",
        "`%s` above is the version" % version,
        updated,
        flags=re.M,
    )
    return (path, sorted(found), version, updated)


# ---------------------------------------------------------------- drift checks


def check_mapsgl_prose(mgl_layers):
    """`weather-layers.md` and the MapsGL SKILL.md name specific layers as composite examples, and
    list the render types and categories in prose. Verify those claims still hold."""
    problems = []
    by_id = {l["id"]: l for l in mgl_layers}
    composite = {l["id"] for l in mgl_layers if l.get("type") == "none"}
    types = {l.get("type") for l in mgl_layers}
    categories = {c for l in mgl_layers for c in (l.get("categories") or [])}

    for name in ("weather-layers.md", "../SKILL.md"):
        path = MGL_REF / name
        if not path.exists():
            continue
        text = path.read_text()
        # Layers named near the word "composite" must still be composite. The window is a flat
        # character count, deliberately: sentence-boundary matching doesn't work here because these
        # files are full of "e.g." and `.show()`, and stopping at the first period truncates the
        # window before it ever reaches the list of example codes.
        flat = text.replace("\n", " ")
        for match in re.finditer(r"composite.{0,300}", flat, re.I | re.S):
            for code in re.findall(r"`([a-z0-9][a-z0-9-]{2,})`", match.group(0)):
                if code in by_id and code not in composite:
                    problems.append(
                        "%s names `%s` near a claim about composite layers, but its render type is"
                        " now `%s` — check whether the prose is still accurate"
                        % (path.name, code, by_id[code].get("type"))
                    )
        for kind in sorted(types):
            if kind and kind != "none" and "`%s`" % kind not in text and name == "weather-layers.md":
                problems.append("weather-layers.md does not mention render type `%s`" % kind)
        for cat in sorted(categories):
            if name == "weather-layers.md" and "`%s`" % cat not in text:
                problems.append("weather-layers.md does not mention category `%s`" % cat)
    return sorted(set(problems))


def check_multiplier_prose(endpoints, layers):
    """The two cost references embed multiplier groupings in hand-written prose. Report drift so a
    human can edit them; rewriting prose automatically would destroy the surrounding explanation."""
    problems = []

    ac = (WX_REF / "access-cost.md")
    if ac.exists():
        text = ac.read_text()
        for entry in endpoints.values():
            mult = entry.get("accessMultiplier")
            if mult is None:
                mult = entry.get("multiplier")
            if mult in (5, 10, 12, 25) and "`/%s`" % entry["title"] not in text:
                problems.append(
                    "access-cost.md is missing `/%s` (x%s) from its multiplier tables"
                    % (entry["title"], mult)
                )

    mu = (RM_REF / "map-units.md")
    if mu.exists():
        text = mu.read_text()
        for layer in layers:
            if layer.get("multiplier", 1) > 1 and "`%s`" % layer["id"] not in text:
                problems.append(
                    "map-units.md is missing `%s` (x%s) from its multiplier tables"
                    % (layer["id"], layer["multiplier"])
                )
    return problems


def _fail_if_empty(name, text, minimum=2000):
    if len(text) < minimum:
        raise SystemExit(
            f"error: generated {name} is only {len(text)} bytes — refusing to write. "
            "The docs site structure has probably changed; fix the extractor before regenerating."
        )


# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="Report drift and exit 1 without writing anything")
    args = ap.parse_args()

    print("Fetching Raster Maps layer catalog…", file=sys.stderr)
    layers = fetch_maps_layers()
    print("  %d layers" % len(layers), file=sys.stderr)

    print("Fetching MapsGL layer catalog…", file=sys.stderr)
    mgl_layers = fetch_mapsgl_layers()
    print("  %d layers" % len(mgl_layers), file=sys.stderr)

    print("Fetching released product versions…", file=sys.stderr)
    mgl_version = fetch_released_version("mapsgl")
    print("  mapsgl %s" % mgl_version, file=sys.stderr)
    verify_mapsgl_cdn(mgl_version)
    version_change = apply_mapsgl_version(mgl_version)

    apple_version = fetch_released_version("mapsgl-apple-sdk")
    print("  mapsgl-apple-sdk %s" % apple_version, file=sys.stderr)
    print("Fetching MapsGL Apple SDK DocC symbol index…", file=sys.stderr)
    apple_codes, apple_configs = fetch_apple_layers(apple_version)
    print("  %d weather layer codes" % len(apple_codes), file=sys.stderr)

    print("Fetching Weather API endpoint catalog and doc pages…", file=sys.stderr)
    endpoints = fetch_weather_api()
    print("  %d endpoints" % len(endpoints), file=sys.stderr)

    generated = {
        WX_REF / "endpoints.md": render_endpoints(endpoints),
        WX_REF / "examples.md": render_examples(endpoints),
        WX_REF / "filters.md": render_filters(endpoints),
        RM_REF / "layers.md": render_layers(layers),
        MGL_REF / "layers.md": render_mapsgl_layers(mgl_layers),
        APPLE_REF / "layers.md": render_apple_layers(apple_version, apple_codes, apple_configs),
    }

    for path, text in generated.items():
        _fail_if_empty(path.name, text)

    changed = []
    for path, text in generated.items():
        current = path.read_text() if path.exists() else None
        if current != text:
            changed.append(path)
            if not args.check:
                path.write_text(text)

    if version_change:
        vpath, old, new, updated = version_change
        changed.append(vpath)
        print(
            "  mapsgl CDN version pin: %s -> %s" % ("/".join(old), new),
            file=sys.stderr,
        )
        if not args.check:
            vpath.write_text(updated)

    problems = check_multiplier_prose(endpoints, layers) + check_mapsgl_prose(mgl_layers)

    rel = lambda p: p.relative_to(ROOT)
    if args.check:
        if not changed and not problems:
            print("✔ references are up to date")
            return 0
        for path in changed:
            print("drift: %s would change" % rel(path))
        for problem in problems:
            print("drift: %s" % problem)
        print("\nRun `python3 scripts/regenerate_references.py` to update the generated files.")
        if problems:
            print("The multiplier notes above are inside hand-written prose and need a manual edit.")
        return 1

    if changed:
        for path in changed:
            print("updated %s" % rel(path))
    else:
        print("no changes — references already up to date")
    for problem in problems:
        print("manual edit needed: %s" % problem)
    return 0


if __name__ == "__main__":
    sys.exit(main())
