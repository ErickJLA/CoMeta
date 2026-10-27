# Changelog

All notable changes to CoMeta. Versions follow [semantic versioning](https://semver.org/):
MAJOR for changes that alter results or break saved sessions, MINOR for new
features, PATCH for fixes. The version is set once in Cell 1 (`COMETA_VERSION`)
and recorded in session files, Excel reports and validation exports.

## [1.0.0] - 2026-10-24

First public release.

### Analyses
- Three-level random-effects meta-analysis (REML) with the full sampling
  variance–covariance matrix, including covariances from shared control groups.
  Inference uses cluster-robust CR2 standard errors with Satterthwaite degrees of
  freedom. The two-level model is available as a sensitivity analysis, with
  REML, ML, DL, PM and SJ τ² estimators.
- Effect sizes: lnRR, Hedges' g, Cohen's d, mean difference, lnCVR, log odds
  ratio, log risk ratio, risk difference and logit proportion, or
  pre-calculated effect sizes. Missing SDs can be imputed, with a complete-case
  sensitivity check.
- Subgroups (one or two moderators), with all pairwise differences
  (Holm-adjusted) and a shared-variance check: each subgroup refitted with its
  own τ² and σ², compared with the shared model, with a likelihood-ratio test
  of equal variance components for between-study moderators. Meta-regression with predictions. Natural cubic splines,
  optionally adjusted for other moderators. An exploratory meta-forest.
- Proportion of meaningful effects (parametric and calibrated, with
  cluster-bootstrap BCa intervals), overall and per subgroup.
- Publication bias: multilevel Egger's test, a time-lag test, and PET-PEESE and
  trim-and-fill (sensitivity analyses), with an overview.
- Sensitivity and complementary analyses: leave-one-out, Baujat plot,
  cumulative meta-analysis, map of studies.

### Results for every analysis
- A plain-language **Results** dashboard explains what the numbers mean, with
  warnings when the data are thin.
- A **Detailed Statistics** tab gives every number with its method, and a
  plain-text copy for reports or AI assistants. `DETAILED_STATS_DIGITS` sets
  the significant digits (default 6), e.g. 12 to compare with R.
- Methods and Results text cites the published sources of each method.
- Publication-ready figures, with plot recipes that redraw a figure exactly.
- A session file that restores the data and the settings of Steps 2–9b, so
  those steps rerun without clicking (choices from Step 12 onward are selected
  again).

### Validation
- 27 validations compare CoMeta with R (metafor, clubSandwich, MetaUtility) on
  the user's own analysis, with optional reference datasets. They also include
  77 unit tests. R packages are pinned to a dated CRAN snapshot.
- Validation 27 checks the proportion of meaningful effects on simulated
  three-level data (bias and CI coverage, with Quick / Standard / Publication
  presets).

### Changes that affect results compared with pre-release versions
- Two-level model with shared controls: the mean is now the GLS estimate with
  the full sampling covariance matrix, matching its CR2 standard error.
- Binary data: the 0.5 continuity correction is also applied to every table
  sharing a control group with a zero-cell table, so the shared control counts
  stay identical.
- Prediction intervals (overall model and meta-regression) follow the t / z
  choice of Step 7.
- PET-PEESE: for Hedges' g, Cohen's d, lnRR and lnCVR with group sample sizes,
  the precision term is now √(1/ñ) (PET) and 1/ñ (PEESE), the effective sample
  size (Nakagawa et al. 2022), as in the time-lag test. The standard error stays
  available in *Precision term*. PET-PEESE is now described as a sensitivity
  analysis.
- The control-group column is used only when selected in Step 2. Older session
  files that relied on automatic use of a `control_id` column must select it.
- Columns derived from the effect size (e.g. `fold_change`, `Response_Ratio`,
  CI bounds) are no longer offered as moderators.
- Plot recipes saved with the funnel-plot shade "Gray (dark to light)" still
  load, under the new internal name.
- The built-in BCG example uses author and year as the study ID, so its 13
  trials are 13 studies (two Rosenthal et al. and two Comstock et al. trials
  were merged before) and it reproduces the published estimates.
- Trim-and-fill reports the number of missing *effect sizes* (it was called
  "missing studies"), and its text no longer calls agreement with Egger's test
  "convergent evidence".
- Leave-one-out refits follow the inference settings of Step 7 (CR2 on or off,
  t or z); before, they always used CR2 with a t distribution.
- Cumulative meta-analysis text: confidence intervals of log ratios are
  back-transformed like the estimate (they were left on the log scale).

### File names
- Every file is named `<Analysis>_<settings>_<k>ES-<studies>st[_F-<filters>]`
  (e.g. `Subgroups_meth_95ES-27st_F-hab-mar.xlsx`), ready to upload as
  supplementary material: the analysis, its moderators and non-default
  settings, the effect sizes and studies it used, and the Step 3 filters. No
  timestamp; a repeated name gets `_v2`, `_v3`. A figure and its plot recipe
  share the name. Names typed in a plot cell still take precedence.

### Publication text and Detailed Statistics
- Every Detailed Statistics tab ends with a *Data selection (Steps 2–6)*
  section: records loaded, Step 3 filters (values kept and excluded), records
  excluded in Steps 4 and 6 with their reasons, imputed SDs, continuity
  corrections, shared control groups and the analysis data.
- Step 7 Methods: the Data Preparation paragraph reports the records, filters,
  exclusions, imputed SDs (only when some were imputed), continuity
  corrections (only when applied) and shared-control covariances; the
  inference, heterogeneity (Q, I², multilevel I²) and prediction-interval
  methods are described with their references; references are numbered in
  order of citation and uncited ones are left out.
- Step 7 Results: one I² (the multilevel I² for the three-level model), ΔAIC
  defined, plain wording of the SD sensitivity check.
- Subgroups: the test for residual heterogeneity replaces the Q_M + Q_E
  "partition" (the two use different weights).
- Wording fixes in Steps 9b, 12, 14, 16, 17, 21 and 24 (test names, k = number
  of effect sizes, AIC comparison, missing CoMeta reference in Step 16,
  reference order in Step 24).

### License
- Released under the GNU General Public License v3.0 or later (see `LICENSE`).
