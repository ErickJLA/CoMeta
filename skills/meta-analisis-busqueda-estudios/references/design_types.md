# Question review and design types

Read this during Step 1 to classify the question. The design decides which abstracts look "extractable".

## 1. Is the question searchable as written?

Check four things. If one fails, don't stop. Pick the most searchable interpretation, state it in the search log, and list 1–2 alternative formulations (in Spanish, since the question came in Spanish) under "Question notes".

| Check | Fails when… | Typical fix |
|---|---|---|
| Measurable outcome | Outcome is a vague construct ("adaptación", "salud", "éxito") | Pick the measurable proxy the literature actually reports (occupancy, relative abundance, capture rate, body weight, survival…) |
| Defined comparison or predictor | No control group, or no continuous predictor | Name the comparator (untreated, ambient, primary forest…) or the gradient (distance, % cover, temperature) |
| One outcome per analysis | Two outcomes in one question ("peso corporal y corticosterona") | Keep both, but tag each candidate with which outcome(s) it likely reports; they will be separate meta-analyses |
| Feasible scope | Very narrow (one species × one country × one habitat) | Search the stated scope first, then widen one dimension (whole species range, the region, related habitats) and say so in the log |

Geographic restriction to Mexico or Latin America: add one search with Spanish terms, because much of that literature is in Spanish-language journals. Also note in the limitations that theses and regional journals (UNAM repositories, Revista Mexicana de Biodiversidad, Acta Zoológica Mexicana…) need a manual check.

## 2. Design types

### A. Treatment vs control (two groups)
Examples: flower strips vs no strips, heat stress vs thermoneutral, gibberellic acid (GA₃) vs untreated seeds, selective logging vs primary forest.
- **Extractable data:** mean, SD or SE, and n per group (or a test statistic convertible to d).
- **Effect size:** lnRR or Hedges' g.
- **Abstract signals for "High":** an explicit control or comparator group; reported direction or size ("30% higher", "significantly increased", "did not differ", means); replicated design (n sites, plots, birds, pens).
- **Red flags:** comparison only among treatments with no control; comparator is a different habitat type than the question asks (e.g. semi-natural meadow instead of crop), which makes it **Medium**; outcome is a proxy (e.g. crop visitation instead of abundance), which also makes it **Medium**.

### B. Binary / incidence outcome
Examples: pruning-wound protectants vs untreated (infected wounds), disease incidence, mortality.
- **Extractable data:** events / total per group, or % with n.
- **Effect size:** log RR or log OR.
- **Abstract signals:** "% recovery", "incidence", "% disease control", "mortality", inoculated vs untreated control.
- **Red flags:** only in-vitro assays (e.g. mycelial inhibition), which make it **Low** unless the question includes in-vitro work; only "% control relative to control" without the raw control incidence. Keep those as **Medium**, since raw data are often in the tables.

### C. Correlation / gradient
Examples: sea surface temperature (SST) vs breeding success, distance to protected-area edge vs bird abundance, forest cover vs deer density or dispersal distance.
- **Extractable data:** r, R², slope ± SE, F or t with df, n (years, sites, individuals). Alternatively, raw paired values (a yearly series, site-level values).
- **Effect size:** Fisher's z (from r), or standardized slopes.
- **Abstract signals:** "correlated", "regression", "declined with", "predicted by", n years or sites.
- **Red flags:** the statistic refers to a different predictor (e.g. body condition instead of SST) → **Medium** with "verify predictor"; several papers reusing the same long-term series (same colony, same monitoring program) → note possible non-independence in "Why probable / caveats"; categorical edge-vs-interior studies can still be used, so mark them "convertible" rather than excluding them.

### D. Single-group values across studies (meta-regression)
Examples: mean dispersal distance per population, compared across landscapes with different forest cover.
- **Extractable data:** mean ± SD and n per population, plus the study-level covariate (e.g. % forest cover, which may have to come from the paper's site description).
- **Effect size:** raw mean (log-transformed) with a meta-regression on the covariate.
- **Abstract signals:** telemetry or GPS collars, genetic dispersal estimates, reported distances with n animals, study-area description.

## 3. Tier rules (all designs)

- **H: High.** A primary study whose abstract matches the population, intervention/exposure, comparison and outcome (PICO/PECO) and the design, with signs of quantitative results.
- **M: Medium.** Relevant, but one element needs checking (comparator, outcome proxy, design, or which predictor), or the record has no abstract and the title is strongly relevant.
- **R: Review or meta-analysis.** Not included as data, but its study list is the fastest source of more primary studies. Flag existing meta-analyses on the same question, because the student's meta-analysis then needs a novelty angle (newer studies, a different region, taxon or moderator).
- **L: Low.** Topic-adjacent, but wrong outcome, no comparison, wrong setting (e.g. urban when the question is agricultural), modelling only, or methods only.
- **X: Excluded.** Off-topic, duplicate (book chapter or preprint of an included paper), or opinion.

Duplicates: when a preprint and the journal version both appear, keep the journal version. When two papers clearly report the same experiment (same sites and years), keep both but note "possible same dataset as <doi>" so the user avoids double counting.
