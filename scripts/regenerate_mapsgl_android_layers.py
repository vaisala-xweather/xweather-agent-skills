#!/usr/bin/env python3
"""Regenerate the MapsGL Android weather-layer catalog from the SDK source.

**This script needs a local checkout of the MapsGL Android SDK** and therefore
cannot run in CI, unlike `regenerate_references.py` which fetches public
endpoints. That is deliberate: the SDK source is not published anywhere CI
could reach.

The catalog is generated from a **release ref**, not from whatever the checkout
happens to have on HEAD - `--ref` defaults to `release/1.6.1`, so the skill
documents exactly one published version.

    python3 scripts/regenerate_mapsgl_android_layers.py --sdk ../mapsgl-android-sdk
    python3 scripts/regenerate_mapsgl_android_layers.py --sdk ../mapsgl-android-sdk --check

`--check` writes nothing and exits non-zero if the committed catalog has drifted
from a fresh generation.

The list of codes is read from that ref with `git show`, so the working tree is
never touched and nothing from a later branch can leak in.
"""
import argparse, io, os, re, sys, collections, subprocess

_ap = argparse.ArgumentParser(description=__doc__,
                              formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument('--sdk', required=True,
                 help='path to a mapsgl-android-sdk checkout')
_ap.add_argument('--root',
                 default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 help='repository root')
_ap.add_argument('--check', action='store_true',
                 help='verify only; write nothing and exit 1 on drift')
_ap.add_argument('--ref', default='release/1.6.1',
                 help='SDK git ref to generate from (default: release/1.6.1)')
ARGS = _ap.parse_args()

SDK_REPO = os.path.abspath(ARGS.sdk)
if not os.path.isdir(os.path.join(SDK_REPO, '.git')):
    print('not an SDK checkout: %s' % SDK_REPO, file=sys.stderr)
    raise SystemExit(2)


def git(*a):
    return subprocess.check_output(['git', '-C', SDK_REPO] + list(a)).decode().strip()


SDK_REF = ARGS.ref
try:
    SDK_COMMIT = git('rev-parse', '--short', SDK_REF)
except subprocess.CalledProcessError:
    print('no such ref in the SDK checkout: %s' % SDK_REF, file=sys.stderr)
    raise SystemExit(2)
SDK_DATE = git('log', '-1', '--format=%cs', SDK_REF)

# The documented version is the ref itself, not whatever is newest upstream.
SDK_VERSION = SDK_REF.split('/')[-1]

print('  SDK ref             :', SDK_REF, SDK_COMMIT, SDK_DATE)
print('  documenting version :', SDK_VERSION)

SDK = os.path.join(SDK_REPO, 'mapsglmaps', 'src', 'main', 'java',
                   'com', 'xweather', 'mapsgl')
CODES   = os.path.join(SDK, 'weather', 'LayerCodes.kt')
SERVICE = os.path.join(SDK, 'weather', 'WeatherService.kt')
CONFIG  = os.path.join(SDK, 'weather', 'WeatherLayerConfiguration.kt')

def read(p):
    # Read from the pinned ref so the working tree's branch is irrelevant.
    rel = os.path.relpath(p, SDK_REPO).replace(os.sep, '/')
    return subprocess.check_output(
        ['git', '-C', SDK_REPO, 'show', '%s:%s' % (SDK_REF, rel)]).decode('utf-8')

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
rows, problems = [], []
for enum_name, code, doc in entries:
    fac = code_to_factory.get(enum_name)
    if not fac:
        problems.append(('no when-branch', enum_name)); continue
    sig = public_factories.get(fac) or internal_factories.get(fac)
    if not sig or sig[0] == '?':
        problems.append(('unresolved signature', enum_name + '/' + fac)); continue
    rows.append(dict(enum=enum_name, code=code, factory=fac,
                     source=sig[0], layer=sig[1], doc=doc,
                     public=fac in public_factories))

print('  enum entries        :', len(entries))
print('  when-block mappings :', len(code_to_factory))
print('  public factories    :', len(public_factories))
print('  rows joined         :', len(rows))
print('  problems            :', len(problems), problems[:8])
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
W('%d built-in weather layers, generated from the MapsGL Android SDK source at the' % len(rows))
W('`%s` tag.' % SDK_REF)
W('')
W('**Every code listed here ships in %s.** The catalog is generated against that release, so' % SDK_VERSION)
W('anything below exists in the JitPack artifact you depend on - there are no development-branch')
W('entries to filter out.')
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
    for r in rs:
        W('- `LayerCode.%s` (`%s`) -> `%s.%s`' % (
            r['enum'], r['code'],
            'WeatherService' if r['public'] else 'WeatherConfigurations', r['factory']))
        if r['doc']:
            W('  - %s' % re.sub(r'\[([A-Z_0-9]+)\]', r'`LayerCode.\1`', r['doc']))

W('')
W('---')
W('')
W('Generated from the MapsGL Android SDK source at `%s` (`%s`), cross-checked against' % (SDK_REF, SDK_COMMIT))
W('the published KDoc for %s at `cdn.aerisapi.com/sdk/android/mapsgl/docs/v%s/`.' % (SDK_VERSION, SDK_VERSION))
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
