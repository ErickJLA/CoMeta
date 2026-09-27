#!/usr/bin/env python3
"""Screen a saved Scite citation_graph result by title, locally (no extra Scite calls).

Prints papers in the graph that are NOT already in the pool and whose titles match an include
regex (and not an exclude regex). Pick the promising DOIs from this list and fetch their
abstracts with ONE batched search_literature(dois=[...]) call.

Usage: graph_filter.py <workdir> <graph_result_file> '<include_regex>' ['<exclude_regex>']
"""
import json, os, re, sys

workdir, path, inc = sys.argv[1], sys.argv[2], re.compile(sys.argv[3], re.I)
exc = re.compile(sys.argv[4], re.I) if len(sys.argv) > 4 else None
t = open(path).read(); g = json.loads(t[t.find('{'):])
pp = os.path.join(workdir, 'pool.json')
pool = json.load(open(pp)) if os.path.exists(pp) else {}
print(f"edges={g.get('edge_count')} nodes={g.get('node_count')} truncated={g.get('truncated')} "
      f"low_coverage_seeds={g.get('low_coverage_seeds')}")
out = []
for doi, p in g.get('papers', {}).items():
    title = ' '.join((p.get('title') or '').split())
    title = re.sub(r'<[^>]+>', '', title)
    if doi.lower() in pool or re.search(r'/reviews?/|dryad|zenodo|figshare', doi, re.I):
        continue
    if inc.search(title) and not (exc and exc.search(title)):
        out.append((p.get('year') or 0, doi, title))
for y, d, ti in sorted(out, reverse=True):
    print(y, d, '|', ti[:125])
print('candidates:', len(out))
