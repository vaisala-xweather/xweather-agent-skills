#!/usr/bin/env python3
"""Fetch an Xweather Raster Maps image without exposing credentials.

Credentials are read from the environment (XWEATHER_CLIENT_ID / XWEATHER_CLIENT_SECRET) so the
secret never appears in shell history, process listings, or the printed output.

Usage:
    export XWEATHER_CLIENT_ID=...  XWEATHER_CLIENT_SECRET=...

    # static map, center point
    python3 xwmap.py 'flat,radar,admin/800x600/minneapolis,mn,7/current.png' -o radar.png

    # static map, bounding box
    python3 xwmap.py 'radar/320x320/30.10,-85.96,33.09,-82.44/current.png' -o se.png

    # single tile
    python3 xwmap.py 'radar/8/41/23/current.png' -o tile.png

    # just compute the cost, send nothing
    python3 xwmap.py 'flat,lightning-strikes/800x600/dallas,tx,7/current.png' --estimate-only

Prints the URL with credentials replaced by {client_id}/{client_secret}, the estimated map units,
and where the image was saved.
"""

import argparse
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request

BASE = "https://maps.api.xweather.com"
CATALOG = "https://www.xweather.com/docs/api/maps/layers"

# Fallback multipliers, used only if the live catalog can't be reached.
FALLBACK = {"lightning-all": 10, "lightning-all-15m": 10, "lightning-all-5m": 10,
            "lightning-strikes": 10, "lightning-strikes-15m-icons": 10,
            "lightning-strikes-5m-icons": 10}


def load_multipliers():
    """layer id -> multiplier, from the live catalog; falls back to the ×10/×5 families."""
    try:
        with urllib.request.urlopen(CATALOG, timeout=10) as resp:
            layers = json.loads(resp.read().decode("utf-8"))["layers"]
        return {l["id"]: l.get("multiplier", 1) for l in layers}
    except Exception:
        return None


def parse_path(path):
    """Split a Raster Maps path into (layers, size_or_tile_info). Returns (layers, w, h) where
    w/h are None for tile requests."""
    parts = [p for p in path.strip("/").split("/") if p]
    if len(parts) < 3:
        return None, None, None
    layers = parts[0]
    # Static: layers/WxH/place/offset.fmt   Tile: layers/z/x/y/offset.fmt
    m = re.fullmatch(r"(\d+)x(\d+)", parts[1])
    if m:
        return layers, int(m.group(1)), int(m.group(2))
    return layers, None, None


def strip_modifiers(layer):
    """'radar:70:blur(2)' -> 'radar'. Modifiers attach with ':'."""
    return layer.split(":", 1)[0]


def estimate_units(path, multipliers):
    """(map_units, tiles, [(layer, multiplier)]) or None if the path can't be parsed."""
    layers, w, h = parse_path(path)
    if layers is None:
        return None
    codes = [strip_modifiers(c) for c in layers.split(",") if c]

    weights = []
    for c in codes:
        if multipliers is None:
            weights.append((c, FALLBACK.get(c, 1)))
        elif c in multipliers:
            weights.append((c, multipliers[c]))
        else:
            # Unknown code — could be a legacy alias (sat, cities, frad). Assume ×1 and flag it.
            weights.append((c + " (unrecognised, assumed x1)", 1))

    tiles = 1 if w is None else math.ceil(w / 256) * math.ceil(h / 256)
    return tiles * sum(m for _, m in weights), tiles, weights


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="Everything after the credentials, e.g. 'radar/800x600/seattle,wa,7/current.png'")
    ap.add_argument("-o", "--output", help="Where to save the image (default: derived from the layers and format)")
    ap.add_argument("--estimate-only", action="store_true", help="Print the URL and cost estimate; send no request")
    ap.add_argument("--timeout", type=float, default=60.0)
    args = ap.parse_args()

    path = args.path.strip().lstrip("/")
    if path.startswith(("http://", "https://")):
        # Tolerate a full URL; drop scheme, host, and the credentials segment.
        path = re.sub(r"^https?://[^/]+/", "", path)
        path = re.sub(r"^[^/]*_[^/]*/", "", path)

    display = f"{BASE}/{{client_id}}_{{client_secret}}/{path}"
    print(f"URL:  {display}")

    est = estimate_units(path, load_multipliers())
    if est:
        units, tiles, weights = est
        breakdown = " + ".join(f"{c} x{m}" for c, m in weights)
        scope = f"{tiles} tiles" if tiles != 1 else "1 tile"
        unit_word = "map unit" if units == 1 else "map units"
        print(f"Cost: ~{units} {unit_word}  ({scope} x [{breakdown}])")
    else:
        print("Cost: could not parse the path to estimate map units")

    if args.estimate_only:
        return

    client_id = os.environ.get("XWEATHER_CLIENT_ID")
    client_secret = os.environ.get("XWEATHER_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit(
            "\nerror: set XWEATHER_CLIENT_ID and XWEATHER_CLIENT_SECRET to fetch the image.\n"
            "       Keys come from the API Keys page at\n"
            "       https://data.portal.xweather.com/account/keys\n"
            "       (Use --estimate-only to skip the request.)"
        )

    real = f"{BASE}/{client_id}_{client_secret}/{path}"
    try:
        with urllib.request.urlopen(real, timeout=args.timeout) as resp:
            status, body, ctype = resp.status, resp.read(), resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        print(f"HTTP: {exc.code}")
        print(body)
        sys.exit(1)
    except urllib.error.URLError as exc:
        sys.exit(f"error: request failed: {exc.reason}")

    print(f"HTTP: {status}")

    # A failed Raster Maps request returns JSON with an image-looking URL, so check the type.
    if "application/json" in ctype:
        print(body.decode("utf-8", "replace"))
        sys.exit(1)

    out = args.output
    if not out:
        layers = path.split("/")[0].replace(",", "-").replace(":", "")
        ext = path.rsplit(".", 1)[-1] if "." in path.rsplit("/", 1)[-1] else "png"
        out = f"xwmap-{layers}.{ext}"
    with open(out, "wb") as fh:
        fh.write(body)
    print(f"Saved: {out}  ({len(body):,} bytes, {ctype})")


if __name__ == "__main__":
    main()
