#!/usr/bin/env python3
"""Structural checks across every skill in the plugin.

Two independent checks:

  refs    every `references/foo.md` a skill mentions resolves - in that skill, or
          in another skill when the mention explicitly qualifies it ("the `mapsgl`
          skill's `references/sessions.md`"); every reference file is reachable
          from its SKILL.md; and none is orphaned
  links   every non-templated URL resolves

`refs` is deterministic and offline. `links` reaches the network, so it is the
flaky one - run it on a schedule rather than on every pull request.

    python3 scripts/check_skill_links.py --skip-links   # structural only
    python3 scripts/check_skill_links.py                # both

Exits non-zero if any check fails.
"""
import argparse
import io
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# Hosts that appear as identifiers or deliberate placeholders, never as addresses.
SKIP_HOSTS = (
    'schemas.android.com',   # XML namespace URIs
    'example.com',           # placeholder in sample code
    'example.org',
    'localhost',
    '127.0.0.1',
)

# Endpoints that answer 4xx by design and cannot be probed. Keep short and justified:
# every entry here is a place real rot could hide.
EXPECT_UNPROBEABLE = {
    'https://api.mapbox.com/downloads/v2/releases/maven': 'auth-gated Maven repo',
}

TRAILING = '.,;:)]}>"\'`*'
URL_RE = re.compile(r'https?://[^\s<>()\[\]"`]+')

# A bare mention, resolved against the skill that contains it.
REF_RE = re.compile(r'`?references/([A-Za-z0-9._-]+\.md)`?')
# A mention explicitly attributed to another skill, e.g.
#   the `mapsgl` skill's `references/sessions.md`
CROSS_REF_RE = re.compile(
    r'`(?P<skill>[a-z0-9][a-z0-9-]*)`\s+skill(?:\'s|s\')?\s+`?references/(?P<file>[A-Za-z0-9._-]+\.md)`?')


def read(p):
    return io.open(p, encoding='utf-8', newline='').read()


def discover(skills_root):
    """skill name -> {'dir', 'skill_md', 'refs': {filename: path}, 'files': [...]}"""
    out = {}
    for name in sorted(os.listdir(skills_root)):
        d = os.path.join(skills_root, name)
        skill_md = os.path.join(d, 'SKILL.md')
        if not os.path.isfile(skill_md):
            continue
        refdir = os.path.join(d, 'references')
        refs = {}
        if os.path.isdir(refdir):
            for f in sorted(os.listdir(refdir)):
                if f.endswith('.md'):
                    refs[f] = os.path.join(refdir, f)
        out[name] = {'dir': d, 'skill_md': skill_md, 'refs': refs,
                     'files': [skill_md] + [refs[k] for k in sorted(refs)]}
    return out


# --------------------------------------------------------------------------- refs
def check_refs(skills):
    ok = True
    for name, s in skills.items():
        problems = []

        # Which (file, line) mentions resolve where.
        for path in s['files']:
            base = os.path.basename(path)
            for i, line in enumerate(read(path).split('\n'), 1):
                cross = {m.group('file'): m.group('skill') for m in CROSS_REF_RE.finditer(line)}
                for fname in REF_RE.findall(line):
                    owner = cross.get(fname)
                    if owner:
                        target = skills.get(owner, {}).get('refs', {})
                        if fname not in target:
                            problems.append(
                                '%s:%d references/%s attributed to the `%s` skill, which does not have it'
                                % (base, i, fname, owner))
                    elif fname not in s['refs']:
                        problems.append('%s:%d references/%s does not exist in this skill'
                                        % (base, i, fname))

        # Everything on disk should be reachable from SKILL.md.
        indexed = set(REF_RE.findall(read(s['skill_md'])))
        for fname in sorted(set(s['refs']) - indexed):
            problems.append('references/%s exists but SKILL.md never points at it' % fname)

        status = 'ok' if not problems else 'FAIL'
        print('  %-16s %2d reference files  %s' % (name, len(s['refs']), status))
        for p in problems:
            print('      %s' % p)
            ok = False
    return ok


# -------------------------------------------------------------------------- links
def collect_urls(skills):
    found = {}
    for name, s in skills.items():
        for path in s['files']:
            text = read(path)
            for m in URL_RE.finditer(text):
                url = m.group(0).rstrip(TRAILING)
                # A `<version>` placeholder truncates the match at '<', leaving a
                # prefix that is not a real address. Detect it from what follows.
                if text[m.end():m.end() + 1] == '<':
                    continue
                if '{' in url or '}' in url:      # templated pattern, not an address
                    continue
                if '/.../' in url:                # deliberately elided path in an example
                    continue
                if any(h in url for h in SKIP_HOSTS):
                    continue
                found.setdefault(url, set()).add('%s/%s' % (name, os.path.basename(path)))
    return {u: sorted(v) for u, v in found.items()}


def probe(url, timeout=25):
    """(ok, detail). Uses curl for the system trust store and redirect handling.

    401/403 counts as reachable - the host and path exist, they are just gated.
    """
    if url in EXPECT_UNPROBEABLE:
        return True, 'skipped (%s)' % EXPECT_UNPROBEABLE[url]
    try:
        r = subprocess.run(
            ['curl', '-sS', '-L', '-o', os.devnull, '-w', '%{http_code}',
             '--max-time', str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 10)
    except Exception as e:                        # noqa: BLE001
        return False, type(e).__name__
    code = (r.stdout or '').strip()
    if not code.isdigit():
        return False, (r.stderr or 'no response').strip()[:70]
    n = int(code)
    if 200 <= n < 400:
        return True, 'HTTP %d' % n
    if n in (401, 403):
        return True, 'HTTP %d (gated)' % n
    if n == 405:
        # Endpoint exists but refuses GET - MCP servers answer only POST.
        return True, 'HTTP 405 (exists, GET not allowed)' % ()
    return False, 'HTTP %d' % n


def check_links(skills):
    urls = collect_urls(skills)
    print('  checking %d distinct URLs across %d skills' % (len(urls), len(skills)))
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda u: (u, probe(u)), sorted(urls)))
    failures = [(u, d, urls[u]) for u, (ok, d) in results if not ok]
    for url, detail, where in failures:
        print('      FAIL %s  %s' % (url, detail))
        print('           in %s' % ', '.join(where))
    print('  %d ok, %d failed' % (len(urls) - len(failures), len(failures)))
    return not failures


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help='repository root')
    ap.add_argument('--skip-links', action='store_true',
                    help='structural checks only, no network')
    args = ap.parse_args()

    skills_root = os.path.join(args.root, 'plugins', 'xweather', 'skills')
    if not os.path.isdir(skills_root):
        print('no skills directory under %s' % args.root, file=sys.stderr)
        return 2

    skills = discover(skills_root)
    if not skills:
        print('no skills found', file=sys.stderr)
        return 2

    print('references:')
    ok = check_refs(skills)

    if not args.skip_links:
        print('\nlinks:')
        ok = check_links(skills) and ok

    print('\n%s' % ('Skill checks passed' if ok else 'Skill checks FAILED'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
