#!/usr/bin/env python3
"""Regenerate the MapsGL Android weather-layer catalog from the SDK source.

**This script needs a local checkout of the MapsGL Android SDK** and therefore
cannot run in CI, unlike `regenerate_references.py` which fetches public
endpoints. That is deliberate: the mapsgl-android skill documents the SDK's
development branch, whose source is not published anywhere CI could reach.

    python3 scripts/regenerate_mapsgl_android_layers.py --sdk ../mapsgl-android-sdk
    python3 scripts/regenerate_mapsgl_android_layers.py --sdk ../mapsgl-android-sdk --check

`--check` writes nothing and exits non-zero if the committed catalog has drifted
from a fresh generation.

The list of codes comes from the SDK checkout; each is then compared against the
released KDoc so anything present only on the branch is marked *(unreleased)*.
"""
import argparse, io, os, re, sys, json, collections, subprocess, urllib.request

_ap = argparse.ArgumentParser(description=__doc__,
                              formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument('--sdk', required=True,
                 help='path to a mapsgl-android-sdk checkout')
_ap.add_argument('--root',
                 default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 help='repository root')
_ap.add_argument('--check', action='store_true',
                 help='verify only; write nothing and exit 1 on drift')
ARGS = _ap.parse_args()

SDK_REPO = os.path.abspath(ARGS.sdk)
if not os.path.isdir(os.path.join(SDK_REPO, '.git')):
    print('not an SDK checkout: %s' % SDK_REPO, file=sys.stderr)
    raise SystemExit(2)


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def git(*a):
    return subprocess.check_output(['git', '-C', SDK_REPO] + list(a)).decode().strip()


SDK_BRANCH = git('rev-parse', '--abbrev-ref', 'HEAD')
SDK_COMMIT = git('rev-parse', '--short', 'HEAD')
SDK_DATE = git('log', '-1', '--format=%cs')

REL = json.loads(fetch('https://www.xweather.com/docs/api/releases/versions'))
SDK_VERSION = REL['products']['mapsgl-android-sdk']['version']
KDOC = ('https://cdn.aerisapi.com/sdk/android/mapsgl/docs/v%s/mapsglmaps/'
        'com.xweather.mapsgl.weather/-layer-code/index.html' % SDK_VERSION)
PUBLISHED = set(re.findall(r'>([A-Z][A-Z0-9_]{2,})<', fetch(KDOC)))
print('  SDK branch          :', SDK_BRANCH, SDK_COMMIT, SDK_DATE)
print('  latest release      :', SDK_VERSION)
print('  published LayerCodes:', len(PUBLISHED))

SDK = os.path.join(SDK_REPO, 'mapsglmaps', 'src', 'main', 'java',
                   'com', 'xweather', 'mapsgl')
CODES   = os.path.join(SDK, 'weather', 'LayerCodes.kt')
SERVICE = os.path.join(SDK, 'weather', 'WeatherService.kt')
CONFIG  = os.path.join(SDK, 'weather', 'WeatherLayerConfiguration.kt')

def read(p):
    return io.open(p, encoding='utf-8', newline='').read()

def strip_block_comments(s):
    return re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)

codes_raw = read(CODES)
svc_raw   = read(SERVICE)
cfg_raw   = read(CONFIG)

# ---- 1. enum entries ----------------------------------------------------------
enum_start = codes_raw.index('enum class LayerCode(')
enum_body  = codes_raw[enum_start:codes_raw.index('companion object', enum_start)]

entries, pending_doc = [], None
for line in enum_body.split('\n'):
    s = line.strip()
    m_doc = re.match(r'^/\*\*\s*(.*?)\s*\*/$', s)
    if m_doc:
        pending_doc = m_doc.group(1); continue
    m = re.match(r'^([A-Z][A-Z0-9_]*)\("([^"]+)"\),?$', s)
    if m:
        entries.append((m.group(1), m.group(2), pending_doc)); pending_doc = None
    elif s and not s.startswith('*'):
        pending_doc = None

# ---- 2. the `when` block, including grouped multi-code branches ----------------
when_start = codes_raw.index('when (code) {', enum_start)
when_body  = strip_block_comments(codes_raw[when_start:codes_raw.index('class WeatherConfigurations', when_start)])
when_body  = re.sub(r'//[^\n]*', '', when_body)          # line comments
flat = re.sub(r'\s+', ' ', when_body)

code_to_factory = {}
# each branch: CODE[, CODE...] -> WeatherConfigurations.Factory(args)
for m in re.finditer(r'((?:[A-Z][A-Z0-9_]*\s*,\s*)*[A-Z][A-Z0-9_]*\s*,?)\s*->\s*WeatherConfigurations\.([A-Za-z0-9]+)\(', flat):
    names = [n.strip() for n in m.group(1).split(',') if n.strip()]
    for n in names:
        code_to_factory[n] = m.group(2)

# ---- 3. factory signatures ----------------------------------------------------
alias_pairs = {}
for m in re.finditer(r'typealias\s+([A-Za-z0-9]+)\s*=\s*WeatherLayerConfiguration<\s*([\w.]+)\s*,\s*([\w.]+)\s*>',
                     re.sub(r'\s+', ' ', cfg_raw + codes_raw + svc_raw)):
    alias_pairs[m.group(1)] = (m.group(2).split('.')[-1], m.group(3).split('.')[-1])

def parse_factories(src):
    src = re.sub(r'\s+', ' ', strip_block_comments(src))
    out = {}
    pat = re.compile(
        r'fun ([A-Za-z0-9]+)\(\s*service: WeatherService\s*(?:,\s*code: LayerCode\s*,?\s*)?\)\s*:\s*'
        r'(?:WeatherLayerConfiguration<\s*([\w.]+)\s*,\s*([\w.]+)\s*>'
        r'|(CompositeWeatherLayerConfiguration)'
        r'|([A-Za-z0-9]+Configuration))')
    for m in pat.finditer(src):
        name, s, l, comp, alias = m.groups()
        if comp:
            out[name] = ('composite', 'composite')
        elif s and l:
            out[name] = (s.split('.')[-1], l.split('.')[-1])
        elif alias in alias_pairs:
            out[name] = alias_pairs[alias]
        else:
            out[name] = ('?', '?')
    return out

public_factories   = parse_factories(svc_raw)     # WeatherService.X
internal_factories = parse_factories(codes_raw)   # WeatherConfigurations.X

# ---- 4. join ------------------------------------------------------------------
rows, problems, unreleased = [], [], []
for enum_name, code, doc in entries:
    if enum_name not in PUBLISHED:
        unreleased.append(enum_name)
    fac = code_to_factory.get(enum_name)
    if not fac:
        problems.append(('no when-branch', enum_name)); continue
    sig = public_factories.get(fac) or internal_factories.get(fac)
    if not sig or sig[0] == '?':
        problems.append(('unresolved signature', enum_name + '/' + fac)); continue
    rows.append(dict(enum=enum_name, code=code, factory=fac,
                     source=sig[0], layer=sig[1], doc=doc,
                     public=fac in public_factories,
                     branch_only=enum_name not in PUBLISHED))

print('  enum entries        :', len(entries))
print('  when-block mappings :', len(code_to_factory))
print('  public factories    :', len(public_factories))
print('  rows joined         :', len(rows))
print('  problems            :', len(problems), problems[:8])
print('  MARKED *(unreleased)* (on branch, not in v%s):' % SDK_VERSION, len(unreleased))
if unreleased:
    print('    ', ', '.join(sorted(unreleased)[:6]), '...')
unused = sorted(set(public_factories) - set(code_to_factory.values()))
print('  public factories not reachable from any LayerCode:', unused)

RENDER = {'SampleLayerDescriptor':'sample','RasterLayerDescriptor':'raster',
          'ParticleLayerDescriptor':'particles','GridLayerDescriptor':'grid',
          'ContourLayerDescriptor':'contour','FillLayerDescriptor':'fill',
          'LineLayerDescriptor':'line','CircleLayerDescriptor':'circle',
          'SymbolLayerDescriptor':'symbol','HeatmapLayerDescriptor':'heatmap',
          'DataQueryLayerDescriptor':'query'}
PAINT = {'sample':'`paint.opacity`, `paint.sample`','raster':'`paint.opacity`, `paint.raster`',
         'particles':'`paint.opacity`, `paint.particle`','grid':'`paint.opacity`, `paint.grid`',
         'contour':'`paint.opacity`, `paint.contour`','fill':'`paint.opacity`, `paint.fill`',
         'line':'`paint.opacity`, `paint.line`','circle':'`paint.opacity`, `paint.circle`',
         'symbol':'`paint.opacity`, `paint.icon`, `paint.text`','heatmap':'`paint.opacity`, `paint.heatmap`',
         'query':'`paint.opacity`, `paint.text`'}

by_layer, composites = collections.OrderedDict(), []
for r in sorted(rows, key=lambda r: r['code']):
    (composites if r['layer'] == 'composite' else by_layer.setdefault(r['layer'], [])).append(r) \
        if r['layer'] != 'composite' else composites.append(r)

order = ['SampleLayerDescriptor','RasterLayerDescriptor','ParticleLayerDescriptor','GridLayerDescriptor',
         'ContourLayerDescriptor','FillLayerDescriptor','LineLayerDescriptor','CircleLayerDescriptor',
         'SymbolLayerDescriptor','HeatmapLayerDescriptor','DataQueryLayerDescriptor']
order += [k for k in by_layer if k not in order]

out = []
W = out.append
W('# MapsGL Android SDK - weather layer catalog')
W('')
W('%d built-in weather layers, generated from the MapsGL Android SDK source on the' % len(rows))
W('`%s` branch.' % SDK_BRANCH)
W('')
W('**%d of these are not in the latest release (%s) yet** and are marked *(unreleased)* below. They' % (len(unreleased), SDK_VERSION))
W('compile only against the development branch - on a released artifact from JitPack they do not')
W('exist. Everything unmarked is in %s.' % SDK_VERSION)
W('')
W('**In Kotlin a layer is a `LayerCode` enum constant, not a string.** `LayerCode.TEMPERATURES`, not')
W('`"temperatures"`. The enum names are *not* mechanical transforms of the wire codes -')
W('`air-quality-co` is `LayerCode.CARBON_MONOXIDE`, `wind-dir` is `LayerCode.WIND_DIR` but its factory')
W('is `WindDirectionArrows` - so never convert a code from the web docs by hand. Look it up here, or')
W('let the IDE complete it. Each entry lists the wire code in parentheses.')
W('')
W('Two ways to add any of them:')
W('')
W('```kotlin')
W('controller.addWeatherLayer(LayerCode.TEMPERATURES)               // defaults')
W('')
W('val config = WeatherService.Temperatures(controller.service)     // to override paint first')
W('config.layer.paint.opacity = 0.5f')
W('controller.addWeatherLayer(config)')
W('```')
W('')
W('The first form calls `LayerCode.getConfigurationForLayerCode(code, service)` internally, so the two')
W('are equivalent apart from the chance to mutate the configuration before it is added.')
W('')
W('For each layer\'s **description, animatability, coverage, data range, update interval and cost')
W('multiplier**, see the shared MapsGL layer documentation at')
W('https://www.xweather.com/docs/mapsgl/weather-layers - those are properties of the data, not of the')
W('SDK, and are identical across SDKs.')
W('')
W('Sections are grouped by layer descriptor, which determines the paint namespace available. See')
W('`references/weather-styling.md` for what each paint type exposes.')
W('')
W('---')
W('')
W('## Composite layers')
W('')
W('These %d codes expand into **several** sub-layers. Their configuration is a' % len(composites))
W('`CompositeWeatherLayerConfiguration`, which carries a list of sub-configurations rather than a')
W('single `layer`, so **paint cannot be set on a composite through its own configuration**. To')
W('restyle one, add the constituent layers individually instead - e.g. `LayerCode.STORMCELLS_TRACKS`')
W('and `LayerCode.STORMCELLS_POSITIONS` rather than `LayerCode.STORMCELLS`.')
W('')
W(' · '.join('`LayerCode.%s`' % r['enum'] for r in sorted(composites, key=lambda r: r['enum'])))
W('')
W('---')

for lyr in order:
    rs = by_layer.get(lyr)
    if not rs:
        continue
    rt = RENDER.get(lyr, '?')
    W('')
    W('## `%s` - render type `%s` (%d)' % (lyr, rt, len(rs)))
    W('')
    if rt in PAINT:
        W('Paint namespaces: %s' % PAINT[rt])
        W('')
    if lyr == 'DataQueryLayerDescriptor':
        W('**These have no `WeatherService` factory.** They all share one configuration built by')
        W('`WeatherConfigurations.DataQueryText(service, code)`, which takes the code as a second')
        W('argument - so there is no `WeatherService.TemperaturesText(...)` and writing one will not')
        W('compile. Add them by `LayerCode`, or call `DataQueryText` directly if you need to override')
        W('paint:')
        W('')
        W('```kotlin')
        W('controller.addWeatherLayer(LayerCode.TEMPERATURES_TEXT)')
        W('')
        W('val config = WeatherConfigurations.DataQueryText(controller.service, LayerCode.TEMPERATURES_TEXT)')
        W('```')
        W('')
        W('They render city labels sampled from their parent data layer, and are the `query` layer type.')
        W('')
    for r in rs:
        W('- `LayerCode.%s` (`%s`) -> `%s.%s`%s' % (
            r['enum'], r['code'],
            'WeatherService' if r['public'] else 'WeatherConfigurations', r['factory'],
            ' *(unreleased)*' if r['branch_only'] else ''))
        if r['doc']:
            W('  - %s' % re.sub(r'\[([A-Z_0-9]+)\]', r'`LayerCode.\1`', r['doc']))

W('')
W('---')
W('')
W('Generated from the MapsGL Android SDK source, branch `%s` at `%s` (%s).' % (SDK_BRANCH, SDK_COMMIT, SDK_DATE))
W('*(unreleased)* markers come from diffing against the published KDoc for %s at' % SDK_VERSION)
W('`cdn.aerisapi.com/sdk/android/mapsgl/docs/v%s/`.' % SDK_VERSION)
W('')
W('If a layer appears in the MapsGL JavaScript catalog but not here, it is not available on Android -')
W('a real gap, not a naming problem. Check `LayerCode` in the IDE against the build you actually')
W('depend on before assuming this list matches it.')
W('')
dest = os.path.join(ARGS.root, 'plugins', 'xweather', 'skills',
                    'mapsgl-android', 'references', 'layers.md')
generated = '\n'.join(out)

if ARGS.check:
    # Drift check: write nothing, report whether the committed file still matches.
    try:
        current = io.open(dest, encoding='utf-8', newline='').read()
    except FileNotFoundError:
        print('  CHECK FAIL: %s does not exist' % dest)
        raise SystemExit(1)
    if current == generated:
        print('  CHECK OK: layers.md matches a fresh generation')
        raise SystemExit(0)
    import difflib
    diff = list(difflib.unified_diff(
        current.splitlines(), generated.splitlines(),
        fromfile='committed layers.md', tofile='freshly generated', lineterm='', n=1))
    print('  CHECK FAIL: layers.md has drifted (%d diff lines)' % len(diff))
    for line in diff[:40]:
        print('    ' + line)
    if len(diff) > 40:
        print('    ... %d more' % (len(diff) - 40))
    raise SystemExit(1)

io.open(dest, 'w', encoding='utf-8', newline='\n').write(generated)
print('  wrote:', dest)
print('  sections:', [(k, len(by_layer[k])) for k in order if by_layer.get(k)])
print('  composites:', len(composites))
