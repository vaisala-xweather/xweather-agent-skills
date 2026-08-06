---
name: webhooks
description: This skill should be used to design, build, secure, or debug an Xweather Webhooks receiver — the push alternative to polling the Weather API. Use it whenever a task mentions Xweather webhooks, pushed weather data, a weather webhook receiver or endpoint, subscribing to pushed hail/lightning/alerts/storm-cell data, or asks how to stop polling the Xweather API and receive data in real time instead. Also use it when writing the endpoint handler, choosing a data set to subscribe to, or preparing the registration details Xweather needs. Also covers Xweather's attribution requirement — the 'Powered by Vaisala Xweather' credit and logo rules that apply wherever Xweather data or imagery is displayed.
license: MIT
metadata:
  author: Vaisala Xweather
  version: "0.12.2"
---

# Xweather Webhooks

Xweather pushes data sets to an HTTPS endpoint you own, instead of your application polling
`data.api.xweather.com` on a timer. The payload is **byte-for-byte the same shape the Weather API
returns**, so existing response-parsing code is reusable with almost no change.

**Webhooks are a premium add-on requiring a separate subscription, and endpoints are registered by
Xweather staff — not self-service.** There is no API call or dashboard toggle that turns this on. Say
so early: the work splits into what the user can build today (the receiver) and what needs a
conversation with their account executive (the subscription and registration).

## When webhooks are the right answer

Reach for them when the user is polling frequently for data that changes unpredictably — lightning
strikes, hail threats, new alerts, storm cell updates. Polling that on a short interval burns
accesses continuously and still adds latency; push removes both problems.

Polling via the `weather-api` skill stays the better fit when the data is requested on
demand (a user opens a page), when the update cadence is slow and predictable (daily normals, hourly
temperatures), or when the user can't host a public HTTPS endpoint.

## How a delivery works

Xweather sends an HTTP `POST` to the registered URL.

| | |
|---|---|
| Method | `POST` |
| `Content-Type` | `application/json` |
| `x-api-key` | A client-generated shared secret, proving the delivery came from Xweather. May be a query parameter instead of a header, if preferred. |
| Body | The standard Xweather API response envelope — JSON or GeoJSON, whichever was configured |

The endpoint must answer with a **2xx** status — `202` is the conventional choice — and do it
*immediately*. The response body is ignored.

**Acknowledge first, process second.** Any real work belongs in a background job, queue, or thread
started after the status is written. A handler that parses, matches polygons, and sends notifications
before responding will eventually exceed the delivery timeout, and a timeout is treated as a failed
delivery.

### Retries

A non-2xx status or a connection timeout triggers a retry, **typically no more than two or three
attempts**. After that the delivery is marked failed and is not attempted again — the next
opportunity is the next update for that data set. There is no replay or backfill mechanism, so a
receiver that's down during an event has permanently missed it. Two consequences worth raising:

- Deliveries are effectively at-most-once after retries are exhausted. If gapless history matters,
  pair the webhook with a periodic API query as a reconciliation backstop.
- Handlers should be **idempotent**, because a retry can duplicate a delivery your server actually
  did process but was too slow to acknowledge. Key writes on a stable field — station id, alert id,
  strike timestamp — and upsert rather than insert.

## Available data sets

Common:

| Data set | What arrives |
|---|---|
| Hail Threats | Real-time hail threat polygons with severity ratings |
| Lightning Threats | Predictive lightning threat zones |
| Lightning | Individual strike events as they occur |
| Lightning Analytics | Strike events with enhanced analytical data |
| Lightning Flash | Consolidated cloud-to-ground flash data |
| Alerts | Government watches, warnings, and advisories |
| Fires | Active wildfire perimeters and fire weather |
| Tropical Cyclones | Storm and hurricane track updates |

Also available, less commonly used: Air Quality · Earthquakes · Observations · Rivers · Storm
Reports · Storm Cells.

Anything outside both lists needs a support conversation. Each data set corresponds to a Weather API
endpoint. Use the `weather-api` skill when you need the endpoint's response-field reference.

## Building the receiver

The whole contract is: accept POST, verify the secret, return 202, process asynchronously.

```javascript
import express from 'express';
const app = express();
app.use(express.json());

app.post('/webhooks/xweather/a3f8c2d1e5b7', (req, res) => {
  if (req.get('x-api-key') !== process.env.XWEATHER_WEBHOOK_KEY) {
    return res.status(401).end();
  }
  res.status(202).end();        // acknowledge first
  enqueue(req.body);            // then hand off — never process inline
});

app.listen(3000);
```

```python
from flask import Flask, request, abort
import os, threading

app = Flask(__name__)

@app.route('/webhooks/xweather/a3f8c2d1e5b7', methods=['POST'])
def receive_webhook():
    if request.headers.get('X-Api-Key') != os.environ['XWEATHER_WEBHOOK_KEY']:
        abort(401)
    data = request.get_json()
    threading.Thread(target=process_payload, args=(data,)).start()
    return '', 202
```

The docs' own examples use a bare `threading.Thread` and an unguarded handler. That's fine as an
illustration, but for anything real prefer a durable queue (SQS, Celery, BullMQ, a database-backed
job table) over an in-process thread — a thread dies with the process, and the delivery is already
acknowledged, so the data is simply gone. Raise this when the user is writing production code.

Test locally against the **Xweather Postman collection**, which ships sample payloads for the data
sets; no subscription needed to exercise the handler.

## Securing the endpoint

Layer these — no single one is sufficient:

1. **HTTPS only.** Non-negotiable: it encrypts the payload and keeps the URL token off the wire.
2. **A secret token in the URL path** — `https://your-server.com/webhooks/xweather/a3f8c2d1e5b7`.
   This is obscurity, not authentication: it cuts random scanning and accidental discovery. Useful,
   but never the only control.
3. **API key verification.** Xweather includes a client-provided key on every request, as an
   `X-Api-Key` header (recommended) or an `api_key` query parameter. Compare it on every request and
   reject mismatches before parsing anything. Use a constant-time comparison if the language offers
   one.
4. **Payload validation.** Check `Content-Type` is `application/json`, that the body parses, and that
   the top-level structure matches the expected envelope for that data set. **Allow unknown extra
   fields** — Xweather may add fields and commits to never removing them, so a strict schema that
   rejects unrecognised keys will break on a future release. Validate permissively.

Rotating a URL or key is a support request needing **at least two business days' notice** to avoid
dropped deliveries. Worth designing for: have the receiver accept both the old and new key during a
rotation window rather than cutting over atomically.

## Registering

Xweather configures the subscription. The user supplies:

- **The full HTTPS URL** of each receiver. Use a **fully qualified domain name, not a raw IP** —
  DNS-based endpoints survive infrastructure changes.
- **The data set(s)** to subscribe to.
- **The coverage area** — a bounding box or polygon. Keep it a simple rectangle or low-vertex polygon;
  complex geometry causes performance problems.
- **Per-environment URLs and keys.** Up to three environments (dev / staging / production) are
  supported without discussion; more needs a support conversation.
- **Format**: JSON or GeoJSON. GeoJSON is the natural choice for polygon data sets (hail threats,
  alerts, fire perimeters) and for anything heading to a map.

The registration form Xweather expects looks like this:

| Field | Example |
|---|---|
| Client Name | My Weather Company |
| Webhook Endpoint(s) | Hail Threats |
| Coverage Area | CONUS — options include CONUS, AK, HI, Puerto Rico, Guam; specify which |
| Update Interval | Real-time |
| Format | GeoJSON |
| Client Endpoints | staging: `https://example.com/webhooks/staging/kawrejhg8a`<br>production: `https://example.com/webhooks/production/jwer9024hf` |
| Authentication | staging `X-API-KEY: 56c3edd0…`<br>production `X-API-KEY: 2001e097…` |

Generate **different secrets per environment** — a staging key that also unlocks production defeats
the purpose. When helping fill this in, produce the structure and let the user paste in their own
secrets rather than inventing key values for them.

Xweather sends a **test payload before enabling the full data set**, so the first thing to watch for
after registration is that single delivery landing and being acknowledged.

## Debugging

| Symptom | Likely cause |
|---|---|
| No deliveries at all | Subscription not yet enabled, or still awaiting the test payload. Registration is manual — confirm with the account executive before debugging code. |
| Deliveries stop after a burst | Handler returned non-2xx or timed out, retries exhausted. Check that 202 is written *before* processing. |
| Duplicate records | Handler isn't idempotent and a slow acknowledgement triggered a retry. Upsert on a stable key. |
| Payload parses but fields are missing | Wrong `format` configured (JSON vs GeoJSON), or the data set differs from what was expected. |
| Handler breaks after working for months | Strict schema validation rejecting newly added fields. Validate permissively. |
| Endpoint receiving junk traffic | URL token leaked, or no key check. Add `X-Api-Key` verification and request a rotation. |
| Works locally, not in production | Endpoint not publicly reachable over HTTPS, or a proxy/load balancer stripping the `x-api-key` header. |

Because the payload matches the API response, a fast way to know what to expect is to query the
equivalent Weather API endpoint once via the `weather-api` skill and inspect the response shape.

## Common patterns

- **Severe weather alerting** — subscribe to Alerts, Hail Threats, or Lightning Threats; on delivery,
  test the threat polygon against your asset/customer locations and notify whoever falls inside.
- **Real-time lightning tracking** — subscribe to Lightning or Lightning Analytics; feed strikes into
  a map layer or analytics pipeline. Note the Weather API charges ×10 for lightning; push avoids the
  repeated polling cost entirely.
- **Observation ingestion** — subscribe to Observations with a bounding box and upsert by station id
  to keep a local mirror current.
- **Storm cell monitoring** — subscribe to Storm Cells for position, movement vector, intensity, and
  hail probability; drive dispatch alerts or worksite closures.
- **Fire weather operations** — combine Fires (perimeters) with Alerts (red flag warnings) to
  automate escalation.
- **Flood and river operations** — subscribe to Rivers, compare stage readings against each gauge's
  flood stage, trigger downstream workflows.

## Attribution is required

Xweather requires attribution wherever its data or imagery is displayed. This applies to **all
products** — Weather API, Raster Maps, and MapsGL alike. Build it into anything you produce, and say
so when handing over code or URLs that will end up in front of users.

The minimum is a link to `https://www.xweather.com/` reading "Powered by Vaisala Xweather":

```html
<a href="https://www.xweather.com/" target="_blank" title="Powered by Vaisala Xweather">Powered by Vaisala Xweather</a>
```

The logo may be substituted for the "Xweather" text. Light and dark variants exist in SVG and PNG:

```html
<a href="https://www.xweather.com/" target="_blank" title="Powered by Vaisala Xweather">
  <img src="https://www.xweather.com/assets/logos/vaisala-xweather-logo-dark.svg" alt="Vaisala Xweather" height="40" />
</a>
```

Swap `-dark` for `-light` over a dark background, or `.svg` for `.png`. Using the logo brings rules:
keep it unmodified, leave at least a **10px buffer** of space around it, and only adjust lightness or
opacity in greyscale. Don't rotate it, don't recolour it (monotone black or white excepted), and don't
use the symbol without the Xweather name.

Full guide: https://www.xweather.com/docs/weather-api/resources/attribution

## Related

The `weather-api` skill covers the pull equivalent and is the reference for payload field names —
every webhook data set mirrors an endpoint documented there. Its `access-cost.md` explains the
polling cost that webhooks are often adopted to eliminate.
