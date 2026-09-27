#!/usr/bin/env python3
"""Fill missing/placeholder abstracts in <workdir>/pool.json from free sources (no Scite credits).

Scite often returns no abstract for Elsevier journals (and some others). This tries OpenAlex
first, then Semantic Scholar. Records that still have no abstract are left for title-only
judgement. Safe to re-run.

Usage: fill_abstracts.py <workdir>
"""
import json, os, sys, time, urllib.parse, urllib.request

P = os.path.join(sys.argv[1], 'pool.json'); pool = json.load(open(P))
UA = {'User-Agent': 'meta-analysis-screening/1.0'}


def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:               # rate limited: back off and retry
                time.sleep(2 * (attempt + 1)); continue
            return None
        except Exception:
            return None
    return None


def bad(a):
    a = (a or '').lower()
    return len(a) < 250 or 'creative commons' in a or 'open access article' in a


filled = missing = 0
for doi, v in pool.items():
    if not bad(v.get('abstract')):
        continue
    ab, src = '', 'none'
    d = get('https://api.openalex.org/works/doi:' + urllib.parse.quote(doi) + '?select=abstract_inverted_index')
    inv = (d or {}).get('abstract_inverted_index')
    if inv:
        ab = ' '.join(w for _, w in sorted((p, w) for w, ps in inv.items() for p in ps)); src = 'openalex'
    if bad(ab):
        d = get('https://api.semanticscholar.org/graph/v1/paper/DOI:' + urllib.parse.quote(doi) + '?fields=abstract')
        s2 = (d or {}).get('abstract') or ''
        if not bad(s2):
            ab, src = s2, 'semanticscholar'
    if not bad(ab):
        v['abstract'] = ' '.join(ab.split()); v['abstract_src'] = src; filled += 1
    else:
        v['abstract_src'] = 'none'; missing += 1
    time.sleep(0.3)
json.dump(pool, open(P, 'w'), indent=1)
print(f'filled={filled} still_missing={missing} (judge these by title)')
