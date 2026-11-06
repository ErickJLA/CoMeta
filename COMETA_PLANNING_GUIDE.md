# Planning a meta-analysis with CoMeta: a guide for Claude

This file is for an AI assistant (written by and for Claude). A user gives you
**this file and a dataset**; your job is to help them **plan a meta-analysis
that can be run in CoMeta 1.0**. Inspect the data, decide what is possible,
and write a step-by-step plan with the exact CoMeta steps and settings.

Rules for you:
- **Plan only with the tools listed here.** If the user needs something
  CoMeta cannot do (section 8), say so plainly and suggest the closest CoMeta
  option or an outside tool (usually R: metafor, clubSandwich, orchaRd).
- **Inspect the data before recommending anything** (section 3). Every
  recommendation should rest on something you saw in the data: numbers of
  studies, levels, missing values.
- **Explain choices in plain language.** CoMeta users are often not
  statisticians; give the reason behind each setting in one sentence.
- **Separate confirmatory from exploratory analyses.** Ask the user for their
  questions and hypotheses; anything chosen after looking at results is
  exploratory.
- **Do not invent features, defaults or thresholds.** The numbers in this file
  come from CoMeta 1.0.0. If the user's CoMeta is a later version, its README
  is the authority.

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
  coefficients use the approximate Hotelling's T² test (AHZ, Tipton &
  Pustejovsky 2015).
- Every analysis gives: a plain-language **Results** dashboard with warnings;
  a **Detailed Statistics** tab (every number, with a plain-text copy for an
  AI assistant); **Methods/Results text with references**; an Excel report;
  publication-ready figures with captions and plot recipes.
- Analyses are saved to a **project file** (data + named analyses with their
  settings and key results) and can be restored and rerun.
- A **validation suite** (28 validations) recomputes the user's own results
  in R (metafor, clubSandwich, MetaUtility).

Step map:

| Step | What it does |
|---|---|
| 2 | Load data (Google Sheets, Excel/CSV upload, a project file, built-in examples) and map columns |
| 3 | Global filters (subset) and an optional common row set |
| 4 | Cleaning (automatic): applies filters, removes unusable rows, reports them |
| 5 | Choose the effect size (CoMeta recommends one) |
| 6 | Compute effect sizes and sampling (co)variances; missing/zero SD handling |
| 7 | **Overall model** (the main result) |
| 8, 9 | Subgroup analysis: configure, run |
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
   - continuous: any zero or negative means (rules out lnRR/lnCVR for those
     rows)? Missing SDs (how many, in how many studies)? Zero SDs? Very small
     n?
   - binary: zero cells, double-zero studies (dropped for log OR / log RR)?
   - lnRR: means close to zero relative to SD (Geary's test will flag them).
4. **Shared controls**: within a study, do several rows have identical control
   n, mean and SD? (Then CoMeta builds their covariance automatically.) Is
   there a column that labels control groups?
5. **Moderators**, for each candidate:
   - type (categorical or continuous); number of levels; effect sizes **and
     studies** per level;
   - **missing values** (how many rows each analysis would lose);
   - **within- or between-study**: does it vary within any study? Within-study
     moderators give sharper comparisons; between-study ones are confounded
     with other study differences;
   - **confounding between moderators**: cross-tabulate categorical pairs;
     correlate continuous ones. Two moderators that move together cannot be
     separated.
6. `year`, coordinates or country present?
7. Duplicates, inconsistent labels (e.g. "Forest" vs "forest" vs "forests":
   ask the user to unify spellings in the sheet before loading; CoMeta does
   not merge variants), outliers in the inputs.

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
- *Zero SDs*: treat as missing (then impute) or drop.
- **Sensitivity check**: results with imputed SDs vs complete cases only.
- **Geary's test** (lnRR, raw data): flags effect sizes whose normal
  approximation is doubtful; they stay in, and Step 7 refits without them as a
  sensitivity analysis.
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
  - two-factor: main effects and interaction tests; if the cells are not fully
    crossed, a sensitivity refit on the largest fully crossed subgrid;
  - **Variance Check**: refits with a τ² and σ² **per subgroup**
    (separate-variance model) and flags changed conclusions, a mean outside
    the shared CI, or τ² + σ² differing by more than ×4 (groups with ≥ 5
    studies); for between-study moderators, an LRT of equal variances. Use it
    when groups are unbalanced or differ in heterogeneity;
  - optional **wild cluster bootstrap** (Detailed Statistics tab) for
    borderline tests (AHZ df < 4 or 0.01 ≤ p ≤ 0.10);
  - warnings: groups with < 5 studies, tests with < 4 df.

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
  size (sized by precision), CI and prediction interval; it can use the
  separate-variance estimates.

### Steps 12–13 – Meta-regression
- One or more moderators, each continuous or categorical (choose the reference
  level). **Additive only: no interaction terms** (for a categorical ×
  categorical interaction use the two-factor subgroup analysis).
- Continuous moderators are centred; CR2 tests per coefficient and AHZ
  omnibus; pseudo-R²; predictions with CI and prediction intervals (kept in
  the observed range); optional wild cluster bootstrap.
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

### Steps 17–20 – Publication bias (all as sensitivity analyses)
- 17: **multilevel Egger's test** (CR2) and **trim-and-fill** (L0/R0; assumes
  independence, so a sensitivity analysis only).
- 19: **PET-PEESE** as multilevel meta-regressions; P-threshold default 0.10;
  precision term √(1/ñ) (effective sample size; default for g, d, lnRR, lnCVR
  with group n) or SE.
- 19b: **time-lag test** (effect vs publication year, with a precision term);
  needs `year`.
- 19c: overview of 17, 19, 19b (how the mean changes under each correction).
- 20: contour-enhanced funnel plot.
- Not available: selection models, Bayesian adjustments, fail-safe N, Begg's
  test (fail-safe N is not recommended anyway).

### Steps 21–23 – Influence
- 21: **leave-one-study-out** refits (three-level, Step 7 inference); flags
  studies that shift the estimate by more than 20% or change the conclusion.
- 22: plot. 23: **Baujat plot** (contribution to heterogeneity vs influence).

### Steps 24–26 – Complementary
- 24: **cumulative meta-analysis** by publication year (multilevel by default;
  study means or independent effect sizes as approximations); needs `year`.
- 25: map (coordinates and/or country). 26: cumulative trend plot.

### Saving, figures, validation
- **💾 Save analysis** (export/save tab of Steps 7–24) adds an analysis to the
  project file; restore it later from Step 2, tab Project.
- Figures: size presets as page shares (full page width, two-thirds, half page
  or one column, full page tall, slide) with balanced fonts; one font for all
  figures; panel letters; manual axis ranges; plot recipes.
- **Validation suite**: run the 🧪 cells after the analysis; each compares the
  user's own results with R. Recommend it before publication.

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

**Missing SDs**: pooled CV of Nakagawa et al. (2023), missing cases only;
report the sensitivity check. If most SDs are missing, say so as a limitation.

**Moderator analyses**
- One categorical moderator: subgroups (Steps 8–9); check the Variance Check.
- Two categorical moderators and their interaction: two-factor subgroups (needs
  enough crossed cells).
- Continuous moderator: meta-regression (12); if non-linearity is plausible
  and there are enough studies, spline (14).
- Several moderators together: meta-regression with several terms; respect
  ~10 studies per coefficient; avoid moderators that are confounded.
- Many candidate moderators, no clear hypotheses: meta-forest (16) to explore,
  then test a few, labelled exploratory.
- Prefer within-study moderators for causal statements; describe between-study
  ones as associations.
- Comparing models with different moderators: set a **common row set** in
  Step 3.
- Borderline p-values or few studies (df < 4): run the wild cluster bootstrap.

**How much is "meaningful"** (9b): agree the threshold with the user from the
biology (e.g. a 10% or 20% change) before running; report both directions.

**Publication bias**: Egger (17), PET-PEESE (19), time-lag (19b) if `year` is
available, then the overview (19c); funnel plot (20). Treat all as sensitivity
analyses; no single test proves or rules out bias.

**Sensitivity set** to report with the main result: leave-one-out (21),
two-level model (7), missing-SD complete cases (6), Geary refit (lnRR, 7),
separate-variance subgroups (9), publication-bias overview (19c).

---

## 6. Minimum data and warnings (CoMeta 1.0)

| Where | Rule or warning |
|---|---|
| Step 7 | warning when fewer than 10 studies |
| Step 8 | groups dropped below Min Papers (3) or Min Observations (5) |
| Step 9 | warnings: group with < 5 studies; test with < 4 df; variance flag when τ² + σ² differs > ×4 (groups ≥ 5 studies) |
| Step 9b | bootstrap < 1000 resamples = exploratory; delta CI unreliable when share < 0.15 |
| Step 12 | warnings: < 10 studies per coefficient; coefficient df < 4; category with < 5 studies |
| Step 14 | stops when studies < coefficients + 2; warns below 10 studies per coefficient and for sparse ends |
| Step 16 | needs ≥ 30 effect sizes |
| Steps 19b, 24 | need a `year` column |
| Wild bootstrap | offered for AHZ df < 4 or 0.01 ≤ p ≤ 0.10 |
| Step 21 | influence flag: shift > 20% of the estimate |

---

## 7. Reproducibility and reporting

- Save every reported analysis with **💾 Save analysis** (name it as in the
  paper, e.g. "Fig. 3 – subgroups by habitat"); the last project file revision
  is the supplementary file that reproduces them.
- Save each figure's **plot recipe**.
- Copy each step's **Detailed Statistics** (plain-text) for the record; use the
  generated **Methods/Results** text as a starting point (it cites the
  methods).
- Run the **validation suite** and keep `cometa_validation_results.json`.
- Cite CoMeta (`CITATION.cff`) and the method papers the text lists.

---

## 8. What CoMeta cannot do (say so; suggest alternatives)

| Need | Status in CoMeta 1.0 | Alternative |
|---|---|---|
| Multivariate models (several correlated outcomes per study) | no | analyse outcomes separately (Step 3 filter), or R metafor `rma.mv` with `vcalc` |
| Phylogenetic non-independence | no | R metafor with a phylogenetic correlation matrix; MetaWin 3 |
| Interactions in meta-regression (continuous × anything) | no (only categorical × categorical via two-factor subgroups) | R metafor |
| Several spline moderators, spline × factor | no | R |
| Correlations from raw r and n | pre-calculated Fisher's z only | compute z and v = 1/(n − 3) first |
| Pre/post or repeated-measures effect sizes (SMCR, ROMC) | pre-calculated only | compute in R `escalc`, load as pre-calculated |
| Bayesian meta-analysis, selection models, RoBMA | no | JASP, R RoBMA / metafor `selmodel` |
| Location-scale models | no (separate-variance subgroups cover categorical cases) | R metafor |
| Network meta-analysis | no | R netmeta |
| Missing-moderator imputation | no (rows with missing moderators are dropped per analysis, or by the common row set) | R mice + metafor |
| Fail-safe N, Begg's test | no (not recommended) | — |
| Offline use / data that cannot go to Google | no (runs in Google Colab) | a local Jupyter install of the notebook, or R |

---

## 9. Plan template (fill this in for the user)

```markdown
# Meta-analysis plan: <title>

## Data
- Source / file; k effect sizes, m studies (per study: min–median–max)
- Data type and column mapping (Step 2); control-group column?
- Problems found and how they are handled (missing SDs, zeros, labels, ...)

## Questions
1. <confirmatory question> → analysis
2. ...
(Exploratory: ...)

## Settings
- Step 3 filters: ...; common row set: ...
- Step 5 effect size: ... (why); bias correction on
- Step 6 missing SDs: ...; zero SDs: ...
- Step 7: three-level, CR2, t, 95% CI

## Analyses (in order)
| # | Step | What | Settings | Why | Save as |
|---|---|---|---|---|---|
| 1 | 7 | Overall effect | defaults | main result | "Overall" |
| 2 | 9 | Subgroups by ... | min 3 papers, 5 ES | H1 | "..." |
| ... |

## Sensitivity analyses
- ...

## Publication bias
- ...

## Figures (size preset, panels)
- ...

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
- Publication-bias tests with few studies (low power); all are sensitivity
  analyses.
