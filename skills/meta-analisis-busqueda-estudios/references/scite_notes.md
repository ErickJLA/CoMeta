# Scite behaviour notes (learned from pilot runs)

Scite credits are limited, so each call has to count. These notes explain the rules in SKILL.md.

## search_literature
- **Payload size:** about 15–20k characters per paper, of which about 75% is `citations` (Smart Citation snippets) that can't be switched off. A 50-result search is about 0.5–1.5 MB and is automatically saved to a file. Parse that file with `scripts/pool.py add`; don't read it directly.
- Because the payload goes to a file anyway, `limit: 50` in one call is cheaper than 5 calls of 10.
- **`term`** searches title, abstract **and full text**. That boosts recall but brings in noise: papers mentioning a keyword in passing, and ambiguous abbreviations (e.g. "SST" pulled in satellite and tuna papers). Prefer spelled-out terms and require two concept blocks joined by AND.
- `term` supports AND, OR, NOT, "phrases" and wildcards (`strip*`).
- **The `abstract` and `title` filters do not accept Boolean OR.** `abstract: "butterflies OR moths"` returned 2 hits instead of hundreds. Use them only with a single word or phrase, or not at all.
- **The `paper_type: "Review"` filter** gave poor relevance. Reviews turn up naturally in normal searches and the citation graph.
- **Fetching metadata by DOI:** `dois: [...]` with no `term` returns abstracts for up to about 50 DOIs in one call. Use this after the citation graph.
- **Missing abstracts:** Elsevier journals (Agriculture, Ecosystems & Environment; Biological Conservation; Basic and Applied Ecology; Crop Protection…) often come back with no abstract. `scripts/fill_abstracts.py` fills most of them from OpenAlex or Semantic Scholar at no Scite cost.
- **Noise records:** PeerJ peer-review reports (`10.7287/peerj.*/reviews/*`), dataset DOIs (Dryad, Zenodo) and book-chapter duplicates. `pool.py` skips the review records automatically; the graph filter skips datasets.
- `editorialNotices` flags retractions and corrections. `pool.py titles` shows "RETRACTED/NOTICE"; such papers should be excluded or noted.

## citation_graph
- Returns only titles and years (compact), so it's the best Scite call for finding more papers. One call with 3–4 seeds and `direction: "both"` returned about 550 papers, over 100 of them relevant by title.
- `max_edges: 600` is a good cap; a larger graph mainly adds off-topic citing papers.
- Seeding with a review and `direction: "out"` gives mostly primary studies (its reference list). Seeding with a primary study and `direction: "in"` gives newer studies that cite it.
- Check `low_coverage_seeds`: if a seed is listed, its graph is incomplete.

## read_fulltext / excerpt checks: not used
- Scite indexes the full text of only about 50% of papers, including only some open-access ones. When the full text isn't indexed, `read_fulltext` returns just the abstract.
- The user screens full texts through institutional access, which is faster and more reliable, so this skill stops at title and abstract.

## report_citations
- Scite's terms of use ask for one call at the end with the cited and excluded decision set. It also gives the user a record of include and exclude decisions for a PRISMA-style screening log. Keep it to one call with about 15–25 representative entries: all High papers and key reviews as `cited`, plus a sample of exclusions with reason codes.

## Call budget per question
| Step | Calls |
|---|---|
| Discovery searches (limit 50) | 2 (3 if a Spanish-language search is needed) |
| Citation graph | 1 |
| Batched abstract fetch for promising graph titles | 1 |
| report_citations | 1 |
| **Total** | **5–6** |
