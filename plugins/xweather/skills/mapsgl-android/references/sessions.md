# Sessions & cost - MapsGL (shared with JS)

MapsGL (including Android) measures usage in **sessions**, not tiles, layers, or
HTTP requests. This matches the JS MapsGL product model.

## Rules

1. A **session** is continuous interaction with a MapsGL map for **up to 5
   minutes**.
2. Sessions align to the **wall clock** at `:00`, `:05`, `:10`, `:15`, ... - not a
   rolling window from first interaction.
3. On Weather API + Maps, **1 session = 150 accesses** (150- multiplier).
4. **At least one session per data request** - no proration below 150 accesses.
5. **Inside a session, interaction is free**: pan, zoom, animate, refresh,
   toggle layers. **Layer count does not change cost.**

## Worked example

Viewing radar from **8:03-8:07** straddles `:05` -> **2 sessions = 300 accesses**.  
The same four minutes from **8:05-8:09** -> **1 session = 150 accesses**.

## Agent guidance

- When asked how usage is measured, show buckets -> sessions -> accesses.
- Cost lever: **when** weather layers are on the map (`addWeatherLayer` /
  `removeWeatherLayer`), not how many layers or whether animation runs.
- Short visits get little discount vs five-minute views because of clock
  alignment.

For longer tables and Raster Maps comparisons, the JS skill's
`references/sessions.md` in
https://github.com/vaisala-xweather/xweather-agent-skills is authoritative for
the shared billing story.
