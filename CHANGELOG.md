# Changelog

All notable changes to CoMeta. Versions follow [semantic versioning](https://semver.org/):
MAJOR for changes that alter results or break saved project files, MINOR for new
features, PATCH for fixes. The version is set once in Cell 1 (`COMETA_VERSION`)
and recorded in project files, Excel reports and validation exports.

## [1.0.0] - 2026-10-24

First public release.

### Analyses
- Derived columns (Step 2b, optional): new columns from rules instead of edits
  in the spreadsheet. A rule transforms a column (logarithm, square, rescale,
  centre overall or within a group, standardise, cut into categories), splits
  a moderator into its between- and within-group parts, combines columns into
  a label, flags rows by a condition, harmonises labels, or computes a formula
  from several columns. Rules are applied in order, never change an existing
  column, are saved with the data in the project file, are listed in every
  Detailed Statistics table and can be applied again to a new version of the
  data. Formulas are read by a restricted parser, not run as code. The formula can be
  built with buttons and is checked while it is written (result of the first
  rows, or what is still wrong); combined labels take any two to four
  columns, in the order chosen.
- Three-level random-effects meta-analysis (REML) with the full sampling
  variance–covariance matrix, including covariances from shared control groups.
  Inference uses cluster-robust CR2 standard errors with Satterthwaite degrees of
  freedom. The two-level model is available as a sensitivity analysis, with
  REML, ML, DL, PM and SJ τ² estimators.
- Effect sizes: lnRR, Hedges' g, Cohen's d, mean difference, lnCVR, log odds
  ratio, log risk ratio, risk difference and logit proportion, or
  pre-calculated effect sizes. Missing SDs can be imputed, with a complete-case
  sensitivity check. For lnRR, Geary's test (Lajeunesse 2015) flags effect sizes
  whose normal approximation is doubtful, and the overall model is refitted
  without them as a sensitivity analysis.
- Subgroups (one or two moderators), with all pairwise differences
  (Holm-adjusted) and a shared-variance check: the model refitted with a τ²
  and a σ² per subgroup (metafor's `struct = "DIAG"`, CR2 by study), with its
  subgroup means, test of subgroup differences, pairwise differences and
  two-way terms next to the shared model's, and a likelihood-ratio test of
  equal variance components for between-study moderators. Meta-regression with predictions. Natural cubic splines,
  optionally adjusted for other moderators. An exploratory meta-forest.
- Proportion of meaningful effects (parametric and calibrated, with
  cluster-bootstrap BCa intervals), overall and per subgroup.
- Optional cluster wild bootstrap tests (Joshi et al. 2022; the algorithm of
  R's wildmeta) for the subgroup tests (shared and separate-variance models)
  and the meta-regression tests, from a panel in Detailed Statistics that
  lists the borderline tests and estimates the run time; re-estimating or
  fast mode, Rademacher or Webb six weights, raw or CR2-adjusted residuals.
- Publication bias: multilevel Egger's test, a time-lag test, and PET-PEESE and
  trim-and-fill (sensitivity analyses), with an overview.
- Sensitivity and complementary analyses: leave-one-out, Baujat plot,
  cumulative meta-analysis, map of studies.

### Results for every analysis
- A plain-language **Results** dashboard explains what the numbers mean, with
  warnings when the data are thin. A yellow *Stale Results* box appears when
  an earlier step was run again after this one.
- A **Detailed Statistics** tab gives every number with its method, and a
  plain-text copy for reports or AI assistants. `DETAILED_STATS_DIGITS` sets
  the significant digits (default 6), e.g. 12 to compare with R.
- Methods and Results text cites the published sources of each method.

### Figures
- Forest, orchard, meaningful-effects, bubble, spline, trim-and-fill,
  time-lag, funnel, leave-one-out, Baujat, cumulative-trend and map plots,
  each with a generated caption and a plot recipe (one file per figure) that
  redraws it exactly without re-running the analysis.
- Size presets as shares of a page (full page width, two-thirds, half page or
  one column, full page tall, 16:9 slide). Each sets every font of the plot to
  sizes balanced for that size and scales marker and bubble sizes; changing
  the width by hand rebalances them too.
- In every plot cell: one font choice for all figures (Arial and Times New
  Roman fall back to the metric-compatible Liberation fonts when missing), a
  panel letter for multi-panel figures, manual axis ranges, and PDF/EPS text
  kept editable (TrueType).
- For lnRR, the effect axis of the forest, orchard, bubble, spline,
  leave-one-out, cumulative and time-lag plots can be labelled in percent
  change.
- Colour-blind-safe defaults where colours carry meaning (the Step 9b plot and
  dashboard; Okabe-Ito and Paul Tol palettes in the bubble plot), and a custom
  colour per group in the orchard and bubble plots.
- The orchard plot can show the subgroups from the separate-variance model
  (own τ² and σ² per subgroup) and hide the Overall row; the bubble plot's
  stats box can show the slope with CI, p, bootstrap p and k, or custom text.

### Saving and reproducing
- A **project file** keeps the work of several days in one file: the data
  (each version once, with a fingerprint) and every analysis saved with
  **💾 Save analysis** (in the *Export & Save* or *Save* tab of every analysis
  step, 7 to 24), with its name, a note, all its settings (Steps 2–7, plus the
  step's own options) and its key results. Each save downloads a new revision
  (`<project>_project_r012.json`) with a log of the changes.
- Step 2 (tab *Project*) and Step 27 list the saved analyses to restore,
  rename, annotate or delete. A restored analysis reruns its steps without
  clicking (Step 9b waits for *Compute Proportions*). Restoring is strict: a
  saved setting that is not available stops the step with a message instead
  of running a different analysis.
- Session files of pre-release versions open as a project with one analysis.

### File names
- Every file is named `<Analysis>_<settings>_<k>ES-<studies>st[_F-<filters>]`
  (e.g. `Subgroups_meth_95ES-27st_F-hab-mar.xlsx`), ready to upload as
  supplementary material: the analysis, its moderators and non-default
  settings, the effect sizes and studies it used, and the Step 3 filters. No
  timestamp; a repeated name gets `_v2`, `_v3`. A figure and its plot recipe
  share the name. Names typed in a plot cell still take precedence.

### Validation
- 28 validations compare CoMeta with R (metafor, clubSandwich, MetaUtility) on
  the user's own analysis, with optional reference datasets. They also include
  101 unit tests. R packages are pinned to a dated CRAN snapshot.
- Validation 27 checks the proportion of meaningful effects on simulated
  three-level data (bias and CI coverage, with Quick / Standard / Publication
  presets).
- Validation 28 checks the cluster wild bootstrap tests of Steps 9 and 12
  against an R implementation of wildmeta's algorithm with the same auxiliary
  weights (every bootstrap statistic, every setting), and against
  `wildmeta::Wald_test_cwb` when that package installs. Main tests first,
  a progress line with the time left, and a time budget (`V28_MAX_MINUTES`);
  a model R cannot fit is reported, not a crash. The R reference uses sparse
  matrices on large data, starts its fits near CoMeta's estimates and keeps
  the best REML fit over several starts, and orders the separate-variance
  model's subgroups as CoMeta does (σ² fixed at 0 for the right subgroup).

### Changes that affect results compared with pre-release versions
- Missing SDs, pooled CV: the "Pooled CV (Nakagawa et al. 2023)" options now
  compute the pooled CV as in that paper (the sample-size-weighted mean CV
  within each study, averaged across studies weighted by each study's mean
  sample size, then squared). Before, they averaged the squared,
  small-sample-corrected CVs over all rows with weights n − 1, which gives a
  larger CV. That method is kept as "Pooled CV² across effect sizes (earlier
  CoMeta method)" to reproduce earlier results; session files that used the
  pooled CV now get the new estimator. Validation 20 recomputes the pooled CVs
  in R.
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
- The built-in BCG example uses author and year as the study ID, so its 13
  trials are 13 studies (two Rosenthal et al. and two Comstock et al. trials
  were merged before) and it reproduces the published estimates.
- Leave-one-out refits follow the inference settings of Step 7 (CR2 on or off,
  t or z); before, they always used CR2 with a t distribution.

### Other changes compared with pre-release versions
- Columns derived from the effect size (e.g. `fold_change`, `Response_Ratio`,
  CI bounds) are no longer offered as moderators.
- Plot recipes saved with the funnel-plot shade "Gray (dark to light)" still
  load, under the new internal name.
- Trim-and-fill reports the number of missing *effect sizes* (it was called
  "missing studies"), and its text no longer calls agreement with Egger's test
  "convergent evidence".
- Cumulative meta-analysis text: confidence intervals of log ratios are
  back-transformed like the estimate (they were left on the log scale).
- The figures were reviewed: the leave-one-out plot draws the no-effect line
  only near the estimates; the funnel plot draws the pseudo-confidence region
  as dashed lines over the significance contours (they made extra stripes);
  the trim-and-fill legend says where its funnel is centred; the bubble-plot
  equation has no scientific notation; spline points are sized by weight;
  legends no longer cover the data at the default size. Plot recipes saved
  earlier load and draw as before.
- Google Sheets import: numeric columns whose name contains "id" inside a
  word (e.g. `lnRR_lipidfree`) were left as text and shown as categorical;
  identifier columns are now recognised by whole words of the name
  (`id`, `study_id`, `StudyID`, ...). Cells with only spaces count as empty
  and the Unicode minus sign (−) is read as a minus.
- Steps 8 and 12 no longer offer `shared_group_id` (the internal key of the
  shared-control groups) as a moderator; Step 8 skips columns with a single
  level and shows one short summary instead of a console-style log.
- Error messages of Steps 6, 8, 9, 19, 21 and 24 appear in the same red box as
  in the other steps.
- The session file of Step 27 and the "Download Settings JSON" buttons of
  Steps 7 and 9 are replaced by the project file.
- Funnel plot: the Egger's-test box is placed beside the plot by default
  (inside the plot it could hide the least precise effect sizes). The corner
  positions are still available, and recipes saved earlier keep theirs.
- Step 7 stops with a clear message when all effect sizes come from a single
  study, instead of reporting a result (the cluster-robust standard error is
  not defined with one study).
- Step 9b warns about subgroups with fewer than 10 studies, and its Results
  text says so and states when the calibrated shares have no confidence
  interval.
- Publication-bias overview (Step 19c): the PET slope is called "the same
  regression as Egger's test" only when both use the standard error, and the
  summary says that Egger's test, trim-and-fill and the PET slope read the
  same funnel asymmetry and count as one piece of evidence.
- Non-significant tests are worded as "no evidence of" or "not detected" in
  the spline dashboard and the publication-bias overview (they said "No" and
  "no change").
- One reference list for all generated texts (`COMETA_REFERENCES`, Cell 1):
  a paper is written the same way in every step, journal articles carry
  their DOI, Step 9b uses numbered citations like the other steps, and the
  references of Step 16 are numbered in order of citation.
- Meta-regression Results name the omnibus test as the Methods do
  (approximate Hotelling's T², AHZ); the subgroup Results table shows small
  p-values as "< 0.001", like the text.
- Excel reports: the first sheet of every report is now the step's
  *Detailed Statistics* table, exactly as shown on screen, so the file and
  the screen give the same numbers. This replaces two sheets that were
  wrong: *Overall Results* listed the two-level estimates even when the
  three-level model was reported, and *Regression Results* listed only the
  intercept and the first moderator. The settings sheet of the
  meta-regression report names every moderator and the fitted model.
- Excel reports: the *Report Text* sheet no longer loses the words after a
  "<" (as in "p < 0.001").
- Project file: a file saved again by an editor that adds a byte-order mark
  (e.g. Notepad) opens; a file that is not a project, or a project whose
  analyses lost their settings by hand editing, is refused with a plain
  message instead of a technical one.
- Reproducibility Mode can be left: while it is on, every step cell shows a
  blue bar with a **Leave Reproducibility Mode** button (also under the
  restore message). Leaving keeps the restored data and settings and stops
  the cells from setting saved settings and running by themselves. Loading
  other data in Step 2 ends the mode as well. Step 2, tab *Project*, now
  explains how the mode works and what to do next.
- Project file: the summary of a saved Egger / trim-and-fill analysis reads
  "Egger slope …, p = …" (it labelled the intercept with the p-value of the
  slope); the slope is stored with the key results. Analyses saved earlier
  show "Egger's test p = …".

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
