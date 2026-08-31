#!/usr/bin/env python3
"""Issue an Xweather Weather API request without exposing credentials in the command line.

Credentials are read from the environment (XWEATHER_CLIENT_ID / XWEATHER_CLIENT_SECRET) so the
secret never appears in shell history, process listings, or the printed output.

Usage:
    export XWEATHER_CLIENT_ID=...  XWEATHER_CLIENT_SECRET=...
    python3 xwrequest.py '/observations/seattle,wa?filter=allstations'
    python3 xwrequest.py '/forecasts/berlin,de?filter=day&limit=15' --raw
    python3 xwrequest.py '/observations/route' --post route.json

Prints the request URL with credentials replaced by {client_id}/{client_secret}, the accesses this
request was charged (with the multiplier breakdown), the remaining allowance, then the response body
(pretty-printed when it is JSON).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://data.api.xweather.com"


def build(path, client_id, client_secret):
    """Return (real_url, display_url). display_url has credentials as placeholders."""
    if path.startswith(("http://", "https://")):
        parsed = urllib.parse.urlparse(path)
        path = parsed.path + (("?" + parsed.query) if parsed.query else "")
    if not path.startswith("/"):
        path = "/" + path

    base_path, _, query = path.partition("?")
    # Drop any credentials the caller already pasted in, so they can't be double-added or leaked.
    kept = [
        p for p in query.split("&")
        if p and not p.split("=", 1)[0] in ("client_id", "client_secret")
    ]
    prefix = BASE + base_path + "?" + "&".join(kept)
    if kept:
        prefix += "&"
    real = f"{prefix}client_id={urllib.parse.quote(client_id)}&client_secret={urllib.parse.quote(client_secret)}"
    display = f"{prefix}client_id={{client_id}}&client_secret={{client_secret}}"
    return real, display


def report_cost(status, meta):
    """Print what this request cost against the access allowance, and what's left."""
    # The wire header is plural; the Responses doc page lists it singular. Accept either.
    multipliers = meta.get("X-Cost-Multipliers") or meta.get("X-Cost-Multiplier")
    tokens = meta.get("X-Cost-Tokens")

    if not 200 <= status < 300:
        # 4xx and 5xx responses are not charged against the allowance.
        print("Accesses: 0 (errors are not charged)")
        return

    if tokens is not None:
        line = f"Accesses: {tokens}"
        if multipliers:
            line += f"  [{' '.join(multipliers.split())}]"
        print(line)
    elif multipliers:
        print(f"Cost multipliers: {multipliers}")

    if meta.get("X-Cost-Endpoint"):
        print(f"Billed endpoint: {meta.get('X-Cost-Endpoint')}")

    remaining = []
    if meta.get("X-RateLimit-Remaining-Minute"):
        remaining.append(
            f"{meta.get('X-RateLimit-Remaining-Minute')}/{meta.get('X-RateLimit-Limit-Minute', '?')} this minute"
        )
    if meta.get("X-RateLimit-Remaining-Period"):
        period = meta.get("X-RateLimit-Limit-Period-Type", "period")
        remaining.append(
            f"{meta.get('X-RateLimit-Remaining-Period')}/{meta.get('X-RateLimit-Limit-Period', '?')} this {period}"
        )
    if remaining:
        print("Remaining: " + ", ".join(remaining))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="Endpoint path with query string, e.g. '/observations/seattle,wa?limit=5'")
    ap.add_argument("--post", metavar="FILE", help="POST this JSON file as the body (for long /route requests)")
    ap.add_argument("--raw", action="store_true", help="Print the body verbatim instead of pretty-printing JSON")
    ap.add_argument("--timeout", type=float, default=30.0)
    args = ap.parse_args()

    client_id = os.environ.get("XWEATHER_CLIENT_ID")
    client_secret = os.environ.get("XWEATHER_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit(
            "error: set XWEATHER_CLIENT_ID and XWEATHER_CLIENT_SECRET in the environment.\n"
            "       Keys come from the API Keys page at\n"
            "       https://data.portal.xweather.com/account/keys"
        )

    real, display = build(args.path, client_id, client_secret)

    data, headers = None, {}
    if args.post:
        with open(args.post, "rb") as fh:
            data = fh.read()
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(real, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            status, body, meta = resp.status, resp.read().decode("utf-8", "replace"), resp.headers
    except urllib.error.HTTPError as exc:
        status, body, meta = exc.code, exc.read().decode("utf-8", "replace"), exc.headers
    except urllib.error.URLError as exc:
        sys.exit(f"error: request failed: {exc.reason}")

    print(f"URL:  {display}")
    print(f"HTTP: {status}")
    report_cost(status, meta)
    print()

    if args.raw:
        print(body)
        return

    try:
        print(json.dumps(json.loads(body), indent=2))
    except ValueError:
        print(body)


if __name__ == "__main__":
    main()
