#!/usr/bin/env python3
"""Regenerate the skill reference files that are derived from live Xweather catalogs.

Four reference files are generated rather than hand-written, and drift out of date as Xweather
ships changes:

    skills/weather-api/references/endpoints.md   from docs/api/weather-api/endpoints + doc pages
    skills/weather-api/references/examples.md    from each endpoint doc page's exampleRequests
    skills/weather-api/references/filters.md     from each endpoint doc page's filter/query tables
    skills/raster-maps/references/layers.md      from docs/api/maps/layers

Two more files embed generated content inside hand-written prose, so they are checked rather than
rewritten; the script reports when their multiplier groupings no longer match the live catalogs:

    skills/weather-api/references/access-cost.md
    skills/raster-maps/references/map-units.md

Usage:
    python3 scripts/regenerate_references.py            # rewrite in place
    python3 scripts/regenerate_references.py --check    # exit 1 if anything would change

--check is what CI runs. It writes nothing.

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

ROOT = pathlib.Path(__file__).resolve().parent.parent
WX_REF = ROOT / "plugins/xweather/skills/weather-api/references"
RM_REF = ROOT / "plugins/xweather/skills/raster-maps/references"

UA = {"User-Agent": "Mozilla/5.0 (xweather-claude-plugin reference regeneration)"}
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


# ---------------------------------------------------------------- drift checks


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

    print("Fetching Weather API endpoint catalog and doc pages…", file=sys.stderr)
    endpoints = fetch_weather_api()
    print("  %d endpoints" % len(endpoints), file=sys.stderr)

    generated = {
        WX_REF / "endpoints.md": render_endpoints(endpoints),
        WX_REF / "examples.md": render_examples(endpoints),
        WX_REF / "filters.md": render_filters(endpoints),
        RM_REF / "layers.md": render_layers(layers),
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

    problems = check_multiplier_prose(endpoints, layers)

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
