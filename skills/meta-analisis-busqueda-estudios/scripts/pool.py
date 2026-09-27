#!/usr/bin/env python3
"""Candidate pool for meta-analysis literature screening.

Scite search results are huge (~75% of each record is Smart Citation snippets that are useless
for screening). This script keeps only what screening needs and stores it in <workdir>/pool.json.

Usage:
  pool.py <workdir> add <scite_result_file> <label>   merge a saved search_literature result
  pool.py <workdir> titles [--from N]                 compact numbered title list
  pool.py <workdir> abstracts <i> [<i> ...] | ALL     print abstracts for screening (by list number)
  pool.py <workdir> missing                           list records whose abstract is missing/placeholder
"""
import json, os, re, sys

NOISE_DOI = re.compile(r'/reviews?/\d|/v\d+/reviews|peerj\.\d+v\d', re.I)   # peer-review records etc.


def load(workdir):
    p = os.path.join(workdir, 'pool.json')
    return (json.load(open(p)) if os.path.exists(p) else {}), p


def read_result(path):
    t = open(path).read()
    d = json.loads(t[t.find('{'):])
    if isinstance(d, dict) and 'text' in d and 'hits' not in d:   # wrapped MCP payload
        d = json.loads(d['text'])
    return d


def bad_abstract(a):
    a = (a or '').lower()
    return len(a) < 250 or 'creative commons' in a or 'open access article' in a


def main():
    workdir, cmd = sys.argv[1], sys.argv[2]
    os.makedirs(workdir, exist_ok=True)
    pool, P = load(workdir)
    keys = list(pool)

    if cmd == 'add':
        d = read_result(sys.argv[3]); label = sys.argv[4]
        new = skipped = 0
        for h in d.get('hits', []):
            doi = (h.get('doi') or '').lower()
            if not doi or NOISE_DOI.search(doi):
                skipped += 1; continue
            if doi not in pool:
                new += 1
                pool[doi] = dict(
                    doi=doi, title=' '.join((h.get('title') or '').split()), year=h.get('year'),
                    journal=h.get('journal') or h.get('publisher'),
                    authors=[a.get('authorName') for a in h.get('authors') or []],
                    abstract=' '.join((h.get('abstract') or '').split()),
                    abstract_src='scite', notices=h.get('editorialNotices'),
                    volume=h.get('volume'), issue=h.get('issue'), page=h.get('page'), found_by=[])
            if label not in pool[doi]['found_by']:
                pool[doi]['found_by'].append(label)
        json.dump(pool, open(P, 'w'), indent=1)
        print(f"query_total={d.get('total')} returned={len(d.get('hits', []))} new={new} "
              f"noise_skipped={skipped} pool_size={len(pool)}")

    elif cmd == 'titles':
        start = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == '--from' else 0
        for i, k in enumerate(keys):
            if i < start: continue
            v = pool[k]
            flag = '-' if bad_abstract(v['abstract']) else 'A'
            ret = ' RETRACTED/NOTICE' if v.get('notices') else ''
            print(f"{i:3d} {v['year']} {flag} {k} | {v['title'][:115]}{ret}")

    elif cmd == 'abstracts':
        idx = range(len(keys)) if sys.argv[3] == 'ALL' else [int(i) for i in sys.argv[3:]]
        for i in idx:
            v = pool[keys[i]]
            ab = v['abstract'] if not bad_abstract(v['abstract']) else 'NO ABSTRACT (judge by title)'
            print(f"\n[{i}] {v['year']} {keys[i]} | {v['title'][:120]}\n  {ab[:1400]}")

    elif cmd == 'missing':
        m = [f"{i} {k}" for i, k in enumerate(keys) if bad_abstract(pool[k]['abstract'])]
        print(len(m), 'records without a usable abstract'); print('\n'.join(m))


if __name__ == '__main__':
    main()
