---
name: meta-analisis-busqueda-estudios
description: Takes a meta-analysis question written in Spanish, translates it to English, structures it (PICO/PECO, design type, effect size), and searches the literature with Scite to find candidate primary studies likely to contain extractable data. Screens titles and abstracts only and delivers an English Excel list ranked High/Medium/Low, plus a sheet of reviews and meta-analyses and an RIS file for Zotero or EndNote, while keeping Scite credit use to about 5–6 calls. Use this skill whenever the user gives a meta-analysis or systematic-review question (in Spanish or English) and wants papers, studies, "literatura", "artículos candidatos", "estudios para incluir", a starting reading list or a search strategy for it, even if they only paste the question with a student's name, or say "busca literatura para esta pregunta" or "find papers for this meta-analysis". For writing the results/discussion of a finished meta-analysis, use meta-analisis-resultados-discusion instead.
---

# Meta-analysis literature finder (Spanish question → English candidate list)

The user is a researcher who supervises students' meta-analyses. They paste a question in Spanish (often with a student's name) and want a **ranked list of probable primary studies** to screen themselves through institutional access. The job ends at title/abstract screening. The user reads the full texts, so don't try to read papers or check data inside them.

Two resources are scarce, and the workflow is designed around them:
- **Scite credits.** Aim for about 5–6 Scite calls per question. See `references/scite_notes.md` for why each rule exists.
- **Your context.** Scite results are huge. Parse them with the bundled scripts; don't read them raw.

Run straight through without pausing for approval. The user asked for no checkpoints. All deliverables are in **English**, and references keep their original language.

## Setup

- Scripts are in `scripts/` next to this file. Call them with `python3 <skill_dir>/scripts/<name>.py`.
- Use a work directory in your scratchpad or temp space, e.g. `<scratch>/meta_<slug>/`, where `<slug>` is short, like `q1_flower_strips`. Save final deliverables where the user can open them: the session's outputs folder, or the current working directory if there isn't one.
- Needs `openpyxl` (`pip install openpyxl` if the import fails). `fill_abstracts.py` needs outbound access to api.openalex.org or api.semanticscholar.org. If both are blocked, skip that step; the affected rows are marked "title only".

## Step 1: Understand, translate and structure (no Scite calls)

1. Translate the question into clear English.
2. Break it into **PICO/PECO**: population/system, intervention or exposure, comparator or gradient, outcome(s).
3. Classify the **design**: treatment vs control, binary incidence, correlation/gradient, or single-group values for meta-regression. Read `references/design_types.md` now. It defines what "extractable data" and a "High" candidate mean for each design, and how to handle vague or overly narrow questions.
4. If the question has a primary and a secondary scope (e.g. "Lepidoptera (or pollinators)"), keep both. The primary scope gets its own search and is listed first in the output.
5. If the question fails a check in design_types.md (vague outcome, two outcomes, very narrow scope), don't stop. Choose the most searchable interpretation, and record the choice plus 1–2 alternative formulations (in Spanish) for the search log.

## Step 2: Discovery searches (2 Scite calls; 3 if a Spanish search is needed)

Write **two** `search_literature` queries with `limit: 50`:
- **Search 1, primary scope:** intervention/exposure synonyms AND primary outcome or taxon.
- **Search 2, broader scope:** intervention/exposure synonyms AND broader outcome/taxon AND a comparison word (control, untreated, conventional, without…) or a gradient word (correlat*, gradient, distance…).
- **Search 3, only for Mexico or Latin America scopes:** the same concepts in Spanish.

How to write the terms: put synonyms in OR groups with wildcards (`"flower strip*" OR "wildflower strip*"`), and join concept blocks with AND. Spell out abbreviations: "sea surface temperature", not "SST". **Don't** use the `abstract`, `title` or `paper_type` filters with OR, because they silently return almost nothing.

Each result is too large to show and is saved to a file. Add each saved file to the pool right away:

```
python3 scripts/pool.py <workdir> add <saved_result_file> <label>
python3 scripts/pool.py <workdir> titles
```

## Step 3: Snowball with the citation graph (1–2 Scite calls)

From the title list, pick **3–4 seeds**: the most on-target primary studies plus the most relevant review or meta-analysis if one exists. Then call `citation_graph` with `direction: "both"`, `depth: 1`, `max_edges: 600`. The result is also saved to a file. Screen it locally:

```
python3 scripts/graph_filter.py <workdir> <saved_graph_file> '<include_regex>' '<exclude_regex>'
```

Build the include regex from the intervention/exposure words and the exclude regex from obvious off-topic themes (e.g. `aphid|pest|weed` for a pollinator question). From the printed titles, choose the **≤50 most promising DOIs** that aren't already in the pool. Fetch all their abstracts with **one** call: `search_literature(dois=[...], limit=50)` with no `term`. Then add that result to the pool with the label `snowball`.

This step usually finds the key reviews and meta-analyses, and is typically the richest source of candidates.

## Step 4: Fill missing abstracts (0 Scite calls)

```
python3 scripts/fill_abstracts.py <workdir>
```

Scite often has no abstract for Elsevier journals. This script fills most of them from OpenAlex or Semantic Scholar.

## Step 5: Screen titles and abstracts

1. Run `pool.py titles` and make a first pass on titles. Mark clearly off-topic records mentally (pest control, other taxa, other settings, peer-review records) and don't read their abstracts. This keeps context use low.
2. Read abstracts only for plausible records, in batches: `pool.py abstracts <i> <j> ...`.
3. Assign a tier to each plausible record using the rules in `references/design_types.md` (H, M, R, L, X). Records you don't list get "Excluded, off-topic" automatically.
4. Write `<workdir>/decisions.json`, keyed by DOI:

```json
{
  "10.1007/s10841-023-00469-9": {
    "tier": "H",
    "system": "Moths",
    "comparison": "Wildflower-enriched margin vs plain grass margin (control)",
    "data": "Abundance, richness, Shannon (up to 1.4x, 1.8x, 3.5x)",
    "why": "Lepidoptera-specific experiment with explicit control"
  }
}
```

Keep `why` to one line a supervisor can act on: why the paper is likely to have data, and what to check (comparator mismatch, possible duplicate dataset, title-only judgement, a different predictor). For reviews and meta-analyses, say what they cover and whether one already answers the question, which is a novelty warning worth stating.

## Step 6: Build the deliverables

Write `<workdir>/search_log.json` as an object whose fields appear in this order: *Question (original, Spanish)*, *Question (English)*, *PICO/PECO*, *Design / effect size* (data to extract, effect size, moderators worth recording), *Question notes* (interpretation choices and alternative formulations, if any), *Search 1…3* (exact term plus total hits, e.g. "1,194 hits, top 50 screened"), *Snowballing* (seed DOIs, direction, number of titles), *Abstract sources*, *Screening basis*, *Limitations* (Scite only, no Web of Science/Scopus, top 50 per search, no grey literature, plus any Spanish-literature caveat), *Date*. Then run:

```
python3 scripts/build_outputs.py <workdir> <workdir>/decisions.json <workdir>/search_log.json <output_dir>/<Slug>_candidates [--focus '<primary-scope regex>']
```

This produces the `.xlsx` file (Candidates with a "Your decision" dropdown, Reviews & meta-analyses, Low & excluded, Search log) and the `.ris` file (High, Medium and Reviews, built from stored metadata, so no Scite call). Use `--focus` so primary-scope studies are listed first within each tier.

## Step 7: Record decisions with Scite (1 call)

Call `report_citations` **once**. Include all High papers and the key reviews as `cited`, and a sample of exclusions with `reason_code` (off_topic, out_of_scope, duplicate) and `stage: "title_abstract"`. Scite's terms ask for this, and it also leaves a screening record for the user.

## Step 8: Reply to the user

Send or link both files. Then give a short summary in chat (English):
- counts per tier, and the 3–5 strongest candidates (primary scope first);
- existing meta-analyses or large reviews, and whether they threaten the question's novelty;
- interpretation choices made in Step 1, if any;
- limitations in one line, and the number of Scite calls used.

## What not to do, and why

- **Don't read papers' full text**, run excerpt checks, or call `read_fulltext`. The user screens full texts with institutional access, and Scite indexes only about half of them anyway.
- **Don't page through searches** (offset) or run many narrow searches. Two broad searches plus the citation graph found more, for fewer credits, in pilot runs.
- **Don't print raw Scite results** into the conversation. Use the scripts.
- **Don't cite or list papers that weren't retrieved** through Scite, OpenAlex or Semantic Scholar in this run. Every row must trace to a real DOI.
