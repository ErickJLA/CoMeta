# Planning a meta-analysis with CoMeta: a guide for Claude

Guide version 2 (November 2026), written for **CoMeta 1.0.0**. Every
statement about CoMeta's behaviour was checked against the 1.0.0 code. The
practical advice (run lists, figure checks, validation workflow) comes from
using CoMeta on a real project.

This file is for an AI assistant (written by and for Claude). A user gives you
**this file and a dataset**; your job is to help them **plan a meta-analysis
that can be run in CoMeta**. Inspect the data, decide what is possible, and
write a step-by-step plan with the exact CoMeta steps, settings and filters.
You can also help while they run it: checking results against the plan,
writing text from the Detailed Statistics, and checking figures.

Rules for you:
- **Plan only with the tools listed here.** If the user needs something
  CoMeta cannot do (section 8), say so plainly and suggest the closest CoMeta
  option, a data-preparation workaround (section 8b), or an outside tool
  (usually R: metafor, clubSandwich, orchaRd, wildmeta).
- **Inspect the data before recommending anything** (section 3). Every
  recommendation should rest on something you saw in the data: numbers of
  studies, levels, missing values.
- **Spell out every analysis as a run**: an ID, the CoMeta step, the Step 3
  filter written as `column = value` conditions, and the expected number of
  effect sizes / studies (section 9). This is the most useful part of a plan:
  it lets the user check every result and every figure against it.
- **Explain choices in plain language.** CoMeta users are often not
  statisticians; give the reason for each setting in one sentence.
- **Separate confirmatory from exploratory analyses.** Ask for the questions
  and hypotheses first (section 11); anything chosen after seeing results is
  exploratory.
- **Report from unrounded values.** Take numbers for the text from the
  Detailed Statistics tab (full precision) and round once. Never round a
  number that was already rounded (25.845 → "25.85" → "25.9" is wrong; it is
  25.8).
- **Do not invent features, defaults or thresholds.** If the user's CoMeta is
  newer than 1.0.0, its README is the authority; say which parts of this guide
  may be out of date.

---

## 1. CoMeta in one page

- A Google Colab notebook, used point-and-click: each step is a cell with a
  form. Run **Cell 1** and **Cell 1b** first in every session, then the steps
  in order. Steps 2–7 are the core; Steps 8–26 are optional, in any order
  after Step 7 (a plot step needs its analysis step first).
- **Default model: three-level random effects** (effect sizes nested in
  studies) fitted by REML, with the full sampling variance–covariance matrix
  (including covariances from **shared control groups**).
- **Default inference: CR2 cluster-robust standard errors** (clustered by
  study) with Satterthwaite degrees of freedom and t tests; tests of several
  coefficients use the approximate Hotelling's T² test (AHZ; Tipton &
  Pustejovsky 2015).
- Every analysis gives: a plain-language **Results** dashboard with warnings;
  a **Detailed Statistics** tab (every number, with a plain-text copy meant
  for an AI assistant); **Methods/Results text with references**; an Excel
  report; publication-ready figures with captions and plot recipes.
- Analyses are saved to a **project file** (data + named analyses with their
  settings and key results) and can be restored and rerun.
- A **validation suite** (28 validations) recomputes the user's own results
  in R (metafor, clubSandwich, MetaUtility, wildmeta).
- **One active dataset at a time.** The Step 3 filter applies to every later
  step, so analyses on different subsets mean changing the filter and
  rerunning Steps 4–7 before the analysis. Plan the run order to group runs
  that share a filter.

Step map:

| Step | What it does |
|---|---|
| 2 | Load data (Google Sheets, Excel/CSV upload, a project file, built-in examples) and map columns |
| 3 | Global filters (subset) and an optional common row set |
| 4 | Cleaning (automatic): applies filters, removes unusable rows, reports them |
| 5 | Choose the effect size (CoMeta recommends one) |
| 6 | Compute effect sizes and sampling (co)variances; missing/zero SD handling; Geary's test |
| 7 | **Overall model** (the main result) |
| 8, 9 | Subgroup analysis: configure, run (includes the Variance Check) |
| 9b | Proportion of meaningful effects |
| 10, 11 | Forest plot, orchard plot (of Steps 7 and 9) |
| 12, 13 | Meta-regression, bubble plot |
| 14, 15 | Non-linear spline meta-regression, its plot |
| 16 | Exploratory meta-forest (moderator importance) |
| 17, 18 | Egger's test and trim-and-fill, trim-and-fill plot |
| 19 | PET-PEESE |
| 19b | Time-lag (decline effect) test |
| 19c | Publication-bias overview |
| 20 | Contour-enhanced funnel plot |
| 21, 22 | Leave-one-out (by study), its plot |
| 23 | Baujat plot |
| 24, 26 | Cumulative meta-analysis, its trend plot |
| 25 | Map of studies |
| 27 | Project file manager, warnings log |
| 🧪 cells | Validation suite (needs R; runs in Colab) |

---

## 2. Data CoMeta accepts

**One row per effect size.** Rows from the same study share a **study ID**;
this defines the three-level structure. Any other column can be a moderator or
a filter. The user maps columns in Step 2; CoMeta guesses from the names below.

**Raw continuous** (means, SDs, sample sizes):

| Field | Recognised names |
|---|---|
| Study ID | `id`, `study`, `study_id`, `paper`, `author` |
| Treatment mean, SD, n | `xe`, `sde`, `ne` (also `mean_e`, `sd_e`, `n_e`, ...) |
| Control mean, SD, n | `xc`, `sdc`, `nc` (also `mean_c`, `sd_c`, `n_c`, ...) |

**Raw binary** (2×2 tables): study ID; treatment events / non-events
(`events_e`, `nonevents_e`, or `a`, `b`); control events / non-events
(`events_c`, `nonevents_c`, or `c`, `d`). A **single-group proportion** (logit)
uses only the treatment events / non-events.

**Pre-calculated**: study ID; effect size (`yi`, `effect_size`, `es`,
`hedges_g`, `lnrr`, `smd`, `g`, `d`); its variance (`vi`, `variance`, `var`)
**or** standard error (`se`, `standard_error`); optional total n (`n_total`,
`n`, `sample_size`). The user then tells Step 5 which type it is: lnRR,
Hedges' g, Cohen's d, log OR, log RR, Fisher's z, MD, lnCVR, risk difference
or logit proportion.

**Optional columns**:
- `year` (publication year): needed for the cumulative meta-analysis (Steps 24,
  26) and the time-lag test (Step 19b).
- `latitude`/`longitude` (decimal degrees) and/or `country`: the map (Step 25).
- A **control-group column** (opt-in, selected in Step 2): rows of one study
  with the same label share a control group. Without it, CoMeta detects shared
  controls automatically: rows of one study with identical control n, mean and
  SD (or control counts).

Data rules worth checking before the user starts:
- lnRR (and lnCVR) need **positive means** in both groups.
- Text in numeric columns is reported; rows with unusable required values are
  removed and listed (Steps 2, 4, 6).
- Moderator columns: CoMeta treats text columns as categorical; numeric
  columns can be continuous (meta-regression, spline) or, with 2–19 distinct
  values, offered as subgroup moderators in Step 8.
- **Keep a data dictionary** (one row per column: meaning, allowed values,
  units) and a clean-up log next to the data file. Both become supplementary
  material and make the run list unambiguous.

---

## 3. When the user gives you a dataset: inspect it first

If you can run code, profile the data (pandas). Otherwise ask the user for the
column list, a few rows and the counts below.

Check and report:
1. **Size**: number of effect sizes (k) and of studies (m); effect sizes per
   study (min, median, max). Few studies (< 10) limit everything that follows.
2. **Data type**: raw continuous, raw binary or pre-calculated? Which columns
   map to the required fields? Are any required values missing?
3. **Effect-size suitability**:
   - continuous: zero or negative means (rule out lnRR/lnCVR for those rows)?
     Missing SDs (how many, in how many studies)? Zero SDs? Very small n, and
     the share of rows with the smallest n (e.g. n = 3: low power, and
     small-study tests have little to work with)?
   - binary: zero cells, double-zero studies (dropped for log OR / log RR)?
   - lnRR: means close to zero relative to their SD (Geary's test will flag
     them).
4. **Shared controls**: within a study, do several rows have identical control
   n, mean and SD? (Then CoMeta builds their covariance automatically.) Is
   there a column that labels control groups?
5. **Moderators**, for each candidate:
   - type (categorical or continuous); number of levels; effect sizes **and
     studies** per level;
   - **missing values** (how many rows each analysis would lose);
   - **within- or between-study**: does it vary within any study? Within-study
     moderators give sharper comparisons; between-study ones are confounded
     with other study differences. This also decides whether the Variance
     Check's equal-variance LRT is computed (Step 9);
   - **confounding between moderators**: cross-tabulate categorical pairs;
     correlate continuous ones. Two moderators that move together cannot be
     separated.
6. `year`, coordinates or country present?
7. Duplicates, inconsistent labels (e.g. "Forest" vs "forest" vs "forests":
   ask the user to unify spellings in the sheet before loading; CoMeta does
   not merge variants), outliers in the inputs.
8. **Identifier and naming problems** that the label check misses:
   - experiment or control-group IDs reused across studies (e.g. "Exp1" in
     several papers): make them unique, e.g. prefix the study ID;
   - **synonyms** (two names for one species, compound, method...):
     harmonise to one accepted name;
   - derived rows that restate other rows (e.g. a rate computed from two
     other outcomes already in the data, or the same experiment entered from
     two figures): remove them and log the removal.

A minimal profiling snippet (adapt column names):

```python
import pandas as pd, numpy as np
df = pd.read_csv(PATH)                         # or read_excel
k, m = len(df), df['id'].nunique()
print(f"{k} effect sizes, {m} studies; per study:", df.groupby('id').size().describe()[['min','50%','max']].to_dict())
for c in ['xe','xc']:
    if c in df: print(c, '<=0:', int((df[c] <= 0).sum()))
for c in ['sde','sdc']:
    if c in df: print(c, 'missing:', int(df[c].isna().sum()), 'zero:', int((df[c] == 0).sum()))
for c in ['ne','nc']:
    if c in df: print(c, 'distribution:', df[c].value_counts().head(5).to_dict())
for c in df.columns.difference(['id','xe','sde','ne','xc','sdc','nc']):
    s = df[c]
    within = df.groupby('id')[c].nunique(dropna=True).gt(1).any()
    if s.dtype == object or s.nunique() < 20:
        lv = df.groupby(c)['id'].agg(['size', 'nunique']).rename(columns={'size': 'ES', 'nunique': 'studies'})
        print(f"\n{c}: {'within' if within else 'between'}-study, missing {int(s.isna().sum())}\n{lv}")
    else:
        print(f"\n{c}: continuous, range {s.min()}–{s.max()}, missing {int(s.isna().sum())}, {'within' if within else 'between'}-study")
```

---

## 4. The steps in detail (options, defaults, limits)

### Step 2 – Data ingestion
- Tabs: Google Sheets, Upload Excel/CSV, **Project** (open a saved project file),
  Built-in Examples (BCG binary; Normand continuous; Konstantopoulos
  pre-calculated three-level; Raudenbush meta-regression; Curtis ecology lnRR
  with shared controls).
- Choose the data type, map columns (and geography, and optionally the
  control-group column), click **Confirm Mapping & Finalize Data**.

### Step 3 – Global filtering
- *Subset filters*: one or more variables; tick the levels to keep. Every later
  step uses the filtered data. Use for a pre-specified scope (e.g. one outcome
  type), not for exploring results.
- *Common row set*: moderators that must be complete. Rows missing any are
  removed **for all analyses**, so the overall model, subgroups and
  meta-regressions use the same rows and are directly comparable. Recommend it
  when the user will compare models with different moderators.
- **The filter is the most common source of a wrong number.** Write it in the
  plan as `column = value` conditions and check the k / studies CoMeta
  reports against the plan every time.

### Step 4 – Cleaning
- Automatic: applies filters, tidies text categories, checks the inputs;
  *Removed Data* lists every removed row with its reason.

### Step 5 – Effect size
| Data | Options |
|---|---|
| Raw continuous | **lnRR** (log response ratio), **Hedges' g**, Cohen's d, mean difference (MD), **lnCVR** (variability) |
| Raw binary | log odds ratio, log risk ratio, risk difference, logit proportion |
| Pre-calculated | as supplied (declare its type) |
- CoMeta recommends one from the data (signs, zeros, scale) and explains why.
- *Small-sample bias correction* (lnRR, lnCVR; Lajeunesse 2015): on by default.
- Log-scale effects are also reported back-transformed (ratios; percent change
  for lnRR in several plots).

### Step 6 – Effect sizes and sampling variances
- *Missing SDs*: impute with the median CV; impute with the **pooled CV of
  Nakagawa et al. (2023)** (missing cases only; recommended), or use the pooled
  CV for all cases; the earlier "pooled CV²" method; or drop the rows.
  An imputed SD is |mean| × pooled CV.
- The pooled CV is computed from the **rows left after the Step 3 filter**,
  separately for treatment and control groups. The same effect size can
  therefore get a slightly different imputed SD under different filters,
  which explains small differences between "the same" estimate in two runs.
- Imputed SDs are treated as known (their uncertainty is not propagated), so
  imputed rows are slightly over-weighted; CoMeta says so in its log.
- *Zero SDs*: treat as missing (then impute) or drop.
- **Sensitivity check**: results with imputed SDs vs complete cases only.
- **Geary's test** (lnRR, raw data; modified Geary number ≥ 3 in both groups):
  flags effect sizes whose normal approximation is doubtful; they stay in,
  and Step 7 refits without them as a sensitivity analysis. Rows with an
  imputed SD are tested with that SD, so their result depends only on n and
  the pooled CV, not on their own data. The log counts how many failing rows
  have an imputed SD.
- Binary: 0.5 continuity correction for tables with a zero cell (and tables
  sharing their control group); double-zero studies dropped for log OR / log RR.
- **Shared controls**: covariances added to the sampling matrix
  (Gleser & Olkin 2009; Lajeunesse 2011 for lnRR).

### Step 7 – Overall meta-analysis (the main result)
- *Model*: **three-level** (recommended, the default) or two-level (sensitivity
  analysis; τ² estimator REML, DL, ML, PM or SJ).
- *CR2 / Knapp-Hartung*: on (default). Off = model-based SE.
- *Inference*: t (default) or z. *Confidence level*: 90, 95 or 99 %.
- Reports: pooled effect, CI, p, **prediction interval**, back-transformed
  effect, Q test, I² and **multilevel I²** (between/within study), τ² and σ²
  with profile-likelihood CIs; model-selection LRT/AIC (for information only;
  the chosen model is reported); Geary and missing-SD sensitivity results.
- Warning when there are fewer than 10 studies.
- These settings (model, CR2, t/z, CI level) are used by every later step.

### Steps 8–9 – Subgroups
- Step 8: single-factor or **two-factor** analysis; moderator(s); thresholds
  *Min Papers* (default 3) and *Min Observations* (default 5) drop small groups.
  Candidates: text/categorical columns, or numeric columns with 2–19 values.
- Step 9: one three-level model with a mean per group and shared τ², σ²:
  - omnibus test of differences (AHZ, CR2); **all pairwise differences**
    (Holm-adjusted); per-group CI and prediction interval; heterogeneity
    explained (pseudo-R²); whether the moderator is within- or between-study;
  - two-factor: main effects and the interaction test; if the cells are not
    fully crossed, a sensitivity refit on the largest fully crossed subgrid;
  - **Variance Check**: refits with a τ² and σ² **per subgroup**
    (separate-variance model: one model on all rows, metafor's
    `struct = c("DIAG", "DIAG")`, CR2 by study), giving each group's mean,
    the test of differences, pairwise differences and, for two factors, main
    effects and interaction. It flags changed conclusions, a mean outside the
    shared CI, or τ² + σ² differing by more than ×4 (groups with ≥ 5 studies).
    When no study spans two groups, its group means equal fitting each group
    on its own. The **LRT of equal variances is computed only for
    between-study moderators**: when a moderator varies within studies the
    models are not nested and the LRT is reported as not computed. Every group
    needs at least 2 studies for the separate-variance model;
  - optional **wild cluster bootstrap** (section 5b);
  - warnings: groups with < 5 studies, tests with < 4 df.
- **Shared or separate variances: the choice can change results.** With
  shared variances, a sparse group borrows the heterogeneity of the large
  groups, which can move its mean a long way (in one project a group of 14
  studies went from about 0% when fitted alone to about +18% in the shared
  model). Rule:
  - for **group means and their plots** when groups differ in size or
    heterogeneity: use the separate-variance estimates (Variance Check and
    the orchard plot's "Own variances per subgroup");
  - for **multi-cell interaction models with sparse cells** (e.g. a 2×2 with
    a cell of 4 studies): keep shared variances, because per-cell variances
    cannot be estimated reliably;
  - for **omnibus tests across many groups**: report the shared-variance test,
    with the separate-variance version as a sensitivity check;
  - state in the Methods which model each result uses, and make tables and
    figures use the same one.
- **Denominator df below 1.** The AHZ denominator df is η − q + 1; with many
  groups and few studies per group it can fall below 1. **CoMeta floors it at
  1.0** (and scales F with the floored value), while R's clubSandwich reports
  the raw value, so the two print different tests (e.g. F(9, 1.0) in CoMeta
  vs F(9, 0.81) in R). A test displayed with df₂ = 1.0 may be such a case:
  do not report it. Use the wild bootstrap, or restrict to groups with enough
  studies (e.g. ≥ 5) and test those.

### Step 9b – Proportion of meaningful effects (Mathur & VanderWeele)
- Share of true effects that are meaningful increases, decreases, or
  negligible, overall and per Step 9 subgroup.
- Thresholds: percent change for log ratios (e.g. 10%), SD units for g/d,
  analysis scale otherwise; same or different in each direction.
  **Set them from biological/practical relevance before seeing results.**
- *True effects of*: individual effect sizes (τ² + σ², default) or study means
  (τ²).
- Parametric (assumes normal true effects) and **calibrated** (no normality
  assumption; prefer it when they disagree).
- CIs: cluster bootstrap; 50–200 resamples to explore (marked exploratory),
  **≥ 1000 for reporting** (BCa). The delta-method CI is poor for shares below
  0.15.

### Steps 10–11 – Forest and orchard plots
- Of the overall and subgroup results; the orchard plot shows every effect
  size (sized by precision), CI and prediction interval.
- Orchard *Elements* tab: **"Own variances per subgroup"** draws the
  separate-variance estimates; the **Overall row can be hidden**.
- See section 10b for which model each plot shows.

### Steps 12–13 – Meta-regression
- One or more moderators, each continuous or categorical (choose the reference
  level). **Additive only: no interaction terms** (for a categorical ×
  categorical interaction use the two-factor subgroup analysis).
- Continuous moderators are centred; CR2 tests per coefficient and AHZ
  omnibus; pseudo-R²; predictions with CI and prediction intervals (kept in
  the observed range); optional wild cluster bootstrap.
- Several continuous columns can enter together, so a **quadratic** works if
  the user adds the squared (centred) column to the data (section 8b).
- Warnings: < 10 studies per coefficient, coefficients with < 4 df,
  categories with < 5 studies.
- Step 13: bubble plot for a continuous moderator (others held at mean /
  reference), colour by another moderator, percent-change axis for lnRR.

### Steps 14–15 – Spline (non-linear) meta-regression
- Natural cubic spline of **one** continuous moderator, df 3–6 (default 3).
- Two tests: does the effect change with the moderator (omnibus AHZ)? is the
  change curved (LRT spline vs linear, ML)?
- *Adjust for*: other moderators held constant (linear or categorical).
- Needs about **10 studies per coefficient** (1 + df + adjustment terms); the
  run stops when studies < coefficients + 2. Warns about sparse ends (few
  studies at the extremes of the moderator).

### Step 16 – Exploratory meta-forest
- Random forest ranking many moderators by permutation importance with
  study-grouped cross-validation (500 trees, fixed seed). Needs **≥ 30 effect
  sizes**. **Exploratory only**: test promising moderators in Steps 9/12 and
  report them as exploratory.

### Steps 17–20 – Publication bias (all sensitivity analyses)
- 17: **multilevel Egger's test** (CR2) and **trim-and-fill** (L0/R0; assumes
  independence, so a sensitivity analysis only).
- 19: **PET-PEESE** as multilevel meta-regressions; P-threshold default 0.10;
  precision term √(1/ñ) (effective sample size; default for g, d, lnRR, lnCVR
  with group n) or SE.
- 19b: **time-lag test**: multilevel regression of the effect on centred
  publication year **plus a precision term** (√(1/ñ) by default, or SE, or
  none). The **year-only model is also reported** as a sensitivity analysis,
  on the same rows. The two year slopes answer different questions (year +
  precision: "is the decline more than a small-study effect?"); plan which
  one is the reported result. The plot's line is the primary model with
  precision held at its mean; choose precision "none" for a year-only figure.
  Needs `year`; rows without it are excluded and counted.
- 19c: overview of 17, 19, 19b (how the mean changes under each correction).
- 20: contour-enhanced funnel plot.
- Not available: selection models, Bayesian adjustments, fail-safe N, Begg's
  test (fail-safe N is not recommended anyway).
- Precision tests have little power when most studies use the same small n
  (e.g. triplicates): say so when interpreting them.

### Steps 21–23 – Influence
- 21: **leave-one-study-out** refits (three-level, Step 7 inference); flags
  studies that shift the estimate by more than 20% or change the conclusion.
- 22: plot. 23: **Baujat plot** (contribution to heterogeneity vs influence).

### Steps 24–26 – Complementary
- 24: **cumulative meta-analysis** by publication year (oldest or newest
  first). Default: the Step 7 multilevel model refitted on all effect sizes of
  the studies included so far; a row without a year takes its study's year,
  and only studies with no year at all are dropped. Alternatives (study means,
  or independent effect sizes) are approximations. Reports when the CI first
  excludes no effect and whether the estimate has stabilised (< 10% change
  over the last five steps). Needs `year`.
- 25: map (coordinates and/or country). 26: cumulative trend plot.

### Saving, figures, validation
- **💾 Save analysis** (export/save tab of Steps 7–24) adds an analysis to the
  project file; restore it later from Step 2, tab Project. Name each saved
  analysis with its run ID from the plan.
- Figures: size presets as page shares (full page width, two-thirds, half page
  or one column, full page tall, slide) with balanced fonts; one font for all
  figures; panel letters; manual axis ranges; editable labels, colours and
  scale; plot recipes.
- **Validation suite**: run the 🧪 cells after the analysis; each compares the
  user's own results with R. Recommend it before publication; for large
  projects, see section 7.

---

## 5. Decision guide

**Effect size**
- Continuous, all means positive, interest in proportional change
  (biomass, abundance, growth): **lnRR** (ecology's usual choice; report as
  percent change).
- Means can be zero or negative, or scales differ and are not ratio scales:
  **Hedges' g** (standardized mean difference).
- Same measurement scale everywhere and raw units matter: MD.
- Interest in variability (not the mean): **lnCVR**.
- Binary: log OR (rare events), log RR (common events), RD (absolute risk;
  keeps double-zero studies), logit proportion (single group).
- Correlations: only as **pre-calculated Fisher's z** (z = atanh(r),
  v = 1/(n − 3), computed before loading).

**Model**
- Several effect sizes per study (the usual case): keep the **three-level
  model** and CR2 (defaults). Two-level only as a sensitivity analysis, or when
  nearly every study has one effect size.
- Keep t inference and CR2 on unless there is a specific reason.
- Estimates with Satterthwaite df < 4: report but do not interpret (Tipton
  2015); mark them (e.g. † in tables).

**Missing SDs**: pooled CV of Nakagawa et al. (2023), missing cases only;
report the sensitivity check. If most SDs are missing, say so as a limitation.

**Moderator analyses**
- One categorical moderator: subgroups (Steps 8–9); read the Variance Check
  and decide shared vs separate variances by the rule in Step 9.
- Two categorical moderators and their interaction: two-factor subgroups (needs
  enough crossed cells).
- Continuous moderator: meta-regression (12); if non-linearity is plausible
  and there are enough studies, spline (14) or a quadratic (section 8b).
- Several moderators together: meta-regression with several terms; respect
  ~10 studies per coefficient; avoid moderators that are confounded.
- Many candidate moderators, no clear hypotheses: meta-forest (16) to explore,
  then test a few, labelled exploratory.
- Prefer within-study moderators for causal statements; describe between-study
  ones as associations.
- Comparing models with different moderators: set a **common row set** in
  Step 3.
- Borderline p-values or few studies (df < 4): run the wild cluster bootstrap
  (section 5b).

**How much is "meaningful"** (9b): agree the threshold with the user from the
subject matter (e.g. a 10% or 20% change) before running; report both
directions.

**Publication bias**: Egger (17), PET-PEESE (19), time-lag (19b) if `year` is
available, then the overview (19c); funnel plot (20). Treat all as sensitivity
analyses; no single test proves or rules out bias.

**Sensitivity set** to report with the main result: leave-one-out (21),
two-level model (7), missing-SD complete cases (6), Geary refit (lnRR, 7),
separate-variance subgroups (9), publication-bias overview (19c).

### 5b. Wild cluster bootstrap: planning and reporting

Offered in the Detailed Statistics tab of Steps 9 and 12 (Joshi et al. 2022;
R wildmeta). The panel's settings:

| Setting | Options (default first) |
|---|---|
| Tests | borderline tests (AHZ df₂ < 4 or 0.01 ≤ p ≤ 0.10) or all tests |
| Replications | 999, 1999, 4999 |
| Weights | Rademacher; Webb six (very few studies) |
| Residuals | CR0 (as wildmeta); CR2 ("CWB adjusted") |
| Mode | re-estimate τ², σ² in every replication (as wildmeta); fast (τ², σ² fixed at the full-model values) |
| Seed | 2024 |

An *Estimate time* button predicts the run time. Results show the bootstrap p
(± its Monte Carlo SE) next to the small-sample test, and whether they agree.

- **Fix the list of tests before running**: e.g. every test that carries a
  conclusion with 0.01 ≤ p ≤ 0.10, every interpreted test with df < 4, and any
  pre-specified key comparison regardless of p. Do not add tests after seeing
  results.
- **Weights**: Webb six when about 10 or fewer studies inform the test
  (Rademacher gives only 2^m distinct samples; CoMeta says so).
- **Replications**: 4999 for reported p-values; keep the seed fixed and report
  it. Re-estimate mode is the reference method; fast mode is an approximation
  for long runs; say in the Methods which one was used.
- **Reporting rule**: give the bootstrap p next to the CR2/AHZ p for the
  planned tests; when they fall on opposite sides of 0.05, call the result
  **uncertain** instead of choosing the more favourable one. With df < 4 and
  about 10 studies, the bootstrap can also exceed its nominal error rate for
  single coefficients; read both with caution.

---

## 6. Minimum data and warnings (CoMeta 1.0.0)

| Where | Rule or warning |
|---|---|
| Step 7 | warning when fewer than 10 studies |
| Step 8 | groups dropped below Min Papers (3) or Min Observations (5) |
| Step 9 | warnings: group with < 5 studies; test with < 4 df; variance flag when τ² + σ² differs > ×4 (groups ≥ 5 studies); equal-variance LRT only for between-study moderators; separate-variance model needs ≥ 2 studies per group |
| Step 9b | bootstrap < 1000 resamples = exploratory; delta CI unreliable when share < 0.15 |
| Step 12 | warnings: < 10 studies per coefficient; coefficient df < 4; category with < 5 studies |
| Step 14 | stops when studies < coefficients + 2; warns below 10 studies per coefficient and for sparse ends |
| Step 16 | needs ≥ 30 effect sizes |
| Steps 19b, 24 | need a `year` column |
| Wild bootstrap | borderline = AHZ df₂ < 4 or 0.01 ≤ p ≤ 0.10; Webb weights advised with ≤ 10 studies |
| Step 21 | influence flag: shift > 20% of the estimate, or a changed conclusion |
| Any AHZ test | df₂ is floored at 1.0; a test shown with df₂ = 1.0 may not be estimable: do not report it |

---

## 7. Reproducibility, validation and reporting

- Save every reported analysis with **💾 Save analysis**, named with its run
  ID and its place in the paper (e.g. "S2 – Table 2, groups A vs B"); the last
  project file revision is the supplementary file that reproduces them.
- Save each figure's **plot recipe**.
- Copy each step's **Detailed Statistics** (plain-text) for the record; use the
  generated **Methods/Results** text as a starting point (it cites the
  methods). Take numbers for the manuscript from Detailed Statistics, not from
  dashboards or plot labels.
- Run the **validation suite** and keep `cometa_validation_results.json`.
- **Large projects (dozens of analyses)**: point-and-click checking of
  everything is slow and error-prone. A workflow that worked:
  1. write an R script that runs every analysis in the run list (metafor +
     clubSandwich; wildmeta for the bootstrap) and writes one results file
     (run ID, quantity, value);
  2. match a first batch completely (estimates, SEs, df, test statistics,
     variance components, log-likelihoods) between CoMeta and R;
  3. then check a **random sample of about 10 runs** in CoMeta against the
     R results file, and investigate any difference (expect the df₂ < 1 case
     of Step 9 to differ by design);
  4. take every manuscript number from the results file, rounding once.
- Cite CoMeta (`CITATION.cff`) and the method papers the text lists.

---

## 8. What CoMeta cannot do (say so; suggest alternatives)

| Need | Status in CoMeta 1.0.0 | Alternative |
|---|---|---|
| Multivariate models (several correlated outcomes per study) | no | analyse outcomes separately (Step 3 filter), or R metafor `rma.mv` with `vcalc` |
| Phylogenetic non-independence | no | R metafor with a phylogenetic correlation matrix; MetaWin 3 |
| Interactions in meta-regression (continuous × anything) | no (only categorical × categorical via two-factor subgroups) | fit the continuous model within each category (Step 3 filter) and compare; or R metafor |
| Several spline moderators, spline × factor | no | R |
| Correlations from raw r and n | pre-calculated Fisher's z only | compute z and v = 1/(n − 3) first |
| Pre/post or repeated-measures effect sizes (SMCR, ROMC) | pre-calculated only | compute in R `escalc`, load as pre-calculated |
| Bayesian meta-analysis, selection models, RoBMA | no | JASP, R RoBMA / metafor `selmodel` |
| Location-scale models | no (separate-variance subgroups cover categorical cases) | R metafor |
| Network meta-analysis | no | R netmeta |
| Missing-moderator imputation | no (rows with missing moderators are dropped per analysis, or by the common row set) | R mice + metafor |
| Fail-safe N, Begg's test | no (not recommended) | — |
| Functions of coefficients with a CI (e.g. a dose optimum −β₁/2β₂, a share B/(B + C), a ratio of two group means) | no | R: delta method from `coef` and the CR2 `vcov` (clubSandwich `vcovCR`) |
| Custom linear contrasts beyond pairwise and two-factor tests (e.g. a difference-in-differences across four cells with its own Satterthwaite df) | partly: the two-factor interaction test covers the crossed-factor case | R clubSandwich `linear_contrast` / `Wald_test` |
| Effective dose windows (range where the lower CI of the predicted effect exceeds zero) | no (predictions with CIs are given, so it can be read off approximately) | R: predict over a dose grid |
| Offline use / data that cannot go to Google | no (runs in Google Colab) | a local Jupyter install of the notebook, or R |

### 8b. Workarounds by preparing the data first

Several analyses that look impossible become ordinary CoMeta runs once the
user adds a column or builds a second file. Offer these before sending the
user to R.

| Need | Prepare | Then in CoMeta |
|---|---|---|
| Quadratic dose–response | `log10_dose_c` (centred, within class if classes differ) and its square | Step 12 with both as continuous moderators |
| Within- vs between-series dose effects | split centred dose into the series mean (between) and the deviation from it (within), and their squares | Step 12 with the within and between terms |
| A slope between two outcomes of the same unit (e.g. outcome B vs outcome A measured on the same cultures or plots) | a **paired file**: one row per unit with outcome B as the effect size and outcome A's lnRR as a column | load as a separate dataset; Step 12 on that column |
| Decomposing a product (e.g. yield = biomass × content) | a **long file**: one row per component per unit, with a `component × group` column | load separately; Step 9 on that column (the share itself needs R, section 8) |
| Interaction of two categorical moderators as cells | a combined column (e.g. `A1_B1`, `A1_B2`, ...) | Step 9 single-factor on the cell column, or two-factor subgroups |
| Sensitivity without a set of studies or rows (one laboratory, Geary failures, imputed SDs) | a flag column | Step 3 filter on the flag |

When a file is derived, keep its construction rules in the data dictionary
and expect different k / studies from the main file.

---

## 9. Plan template (fill this in for the user)

```markdown
# Meta-analysis plan: <title>

## Data
- Source / file; k effect sizes, m studies (per study: min–median–max)
- Data type and column mapping (Step 2); control-group column?
- Problems found and how they are handled (missing SDs, zeros, labels,
  reused IDs, synonyms, derived rows, ...)
- Derived files (paired, long format) and how they were built

## Questions
1. <confirmatory question> → run IDs
2. ...
(Exploratory: ...)

## Decisions (settle before running)
- Shared vs separate variances for group means and plots: ...
- Which year model is reported (year + precision vs year alone): ...
- Bootstrap test list, weights, replications, mode, seed: ...
- Handling of df < 4 and df₂ = 1.0 (floored) tests: ...
- Meaningful-effect thresholds (9b): ...

## Settings
- Step 5 effect size: ... (why); bias correction on
- Step 6 missing SDs: ...; zero SDs: ...
- Step 7: three-level, CR2, t, 95% CI

## Run list (every reported analysis; group runs that share a filter)
| ID | Step | What | File | Keep rows where (Step 3) | Expected k / studies | Settings | Why | Saved as |
|---|---|---|---|---|---|---|---|---|
| O1 | 7 | Overall effect, outcome A | main | outcome = A | 400 / 50 | defaults | main result | "O1" |
| S1 | 9 | Groups X vs Y, outcome A | main | outcome = A AND group = X or Y | 360 / 46 | Variance Check; separate variances reported | H2 | "S1" |
| ... |

## Sensitivity analyses
- ... (each with its own run ID and filter)

## Publication bias
- ...

## Figures (one row per panel)
| Figure | Run ID | CoMeta plot | Model shown | Check value | Size preset |
|---|---|---|---|---|---|
| 2a | O1 + S1 | orchard | overall: three-level; groups: own variances | +21.8 (+13.7 to +30.4) | full width |

## Limitations to state
- ...
```

---

## 10. Common pitfalls to check for the user

- Treating several effect sizes per study as independent (CoMeta's three-level
  default handles it; do not switch to two-level without a reason).
- Shared control groups coded inconsistently (identical control values are
  needed for automatic detection, or use a control-group column).
- Subgroups with very few studies, or a moderator that is confounded with
  another (crosstab first).
- Too many moderators for the number of studies (~10 studies per coefficient).
- Choosing thresholds, moderators or filters after seeing results without
  labelling them exploratory.
- Interpreting a non-significant test as "no effect" (CoMeta's text says "no
  evidence of").
- Reporting the mean without the prediction interval when heterogeneity is
  large (Step 7 reports both; Step 9b quantifies it).
- Publication-bias tests with few studies or uniform small n (low power); all
  are sensitivity analyses.
- **A figure and the text showing different numbers for "the same" result.**
  Usual causes: a different Step 3 filter (check k / studies; it also changes
  imputed SDs), a different model (shared vs separate variances, year alone
  vs year + precision), or a value rounded twice. See section 10b.
- **Presenting the same result twice** (a table and a figure of the same
  estimates). Journals discourage it: pick one per result and move the other
  to the Supplement.

### 10b. Which model a plot shows

| Plot | Shows | Watch out |
|---|---|---|
| Forest / orchard of Step 7 | the overall three-level model | — |
| Orchard of Step 9, default | **shared-variance** group means | can differ a lot from separate fits for sparse groups; tick "Own variances per subgroup" when the plan reports those |
| "Overall" row in a Step 9 forest / orchard | the Step 7 model on the current Step 3 filter | includes effect sizes of groups dropped by Min Papers / Min Observations (the caption counts them); if the filter differs from the main overall run, so does this row: check k / studies or hide the row |
| Step 13 bubble plot | the Step 12 meta-regression (other moderators at mean / reference) | its slope is the reported meta-regression slope |
| Step 19b time-lag plot | year + precision model, precision at its mean | its slope differs from year alone; set precision to "none" for a year-only figure |
| Step 22 / Step 26 | leave-one-out / cumulative refits | the last cumulative step equals the Step 7 estimate only when every study has a year (default multilevel option) |

**Figure checklist** (consistent across the paper): no plot titles, a panel
letter on each panel; the same % axis ticks across panels of one figure
(e.g. −50, 0, +50, +100, +200); printed values in the paper's format, e.g.
+21.8 (+13.7 to +30.4) and k / studies; a colour-blind-safe palette used for
the same meaning in every figure (e.g. Okabe–Ito); † on estimates with df < 4;
the caption states the model and the test behind the panel.

---

## 11. Before writing the plan, ask the user

- Their questions and hypotheses, and which were fixed before seeing data.
- Which journal (figure and table limits, supplementary format).
- Whether they will also run R (decides how much to plan around section 8 and
  the validation workflow of section 7).
- Which CoMeta version they have.
