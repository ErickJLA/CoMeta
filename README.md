# CoMeta: Three-Level Meta-Analysis in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta.ipynb)

CoMeta is a point-and-click meta-analysis notebook for Google Colab. It fits
**three-level random-effects models** (effect sizes nested within studies) with
cluster-robust (CR2) inference. It covers the whole workflow: data import,
effect-size calculation, subgroups, meta-regression, splines, publication bias,
sensitivity analyses and publication-ready figures. You need no coding: every
step is a form with buttons and drop-downs.

CoMeta is a **glass-box** tool. The statistics are written out in the notebook
cells rather than hidden in a compiled package, so you can read how every
number is computed. Every step reports the settings it used and generates
Methods/Results text you can adapt for a manuscript. During development the
results were checked against the R packages `metafor`, `clubSandwich` and
`MetaUtility`.

**Highlights**
- From raw data to the three-level model: effect sizes, missing-SD imputation
  with a sensitivity check, and automatic detection of shared control groups
  with their sampling covariances.
- **Proportion of meaningful effects** (Step 9b): the share of true effects
  that are meaningful increases, decreases or negligible for a threshold you
  choose, overall and per subgroup, extended to the three-level model.
- Publication bias for dependent effect sizes: multilevel Egger's test,
  PET-PEESE and a time-lag (decline effect) test, with trim-and-fill as a
  sensitivity analysis.
- Reproducibility: a **session file** reruns the analysis, and a **plot
  recipe** (one file per figure) redraws any figure exactly, without
  re-running the analysis.
- Publication-ready figures with journal size presets, and generated
  Methods/Results text with references.

---

## Contents

1. [Getting started](#1-getting-started)
2. [Preparing your data](#2-preparing-your-data)
3. [Step-by-step manual](#3-step-by-step-manual)
4. [Saving and reproducing an analysis](#4-saving-and-reproducing-an-analysis)
5. [Statistical methods](#5-statistical-methods)
6. [Outputs](#6-outputs)
7. [Troubleshooting](#7-troubleshooting)
8. [Validation suite (for developers)](#8-validation-suite-for-developers)
9. [Citation, license and contact](#9-citation-license-and-contact)

---

## 1. Getting started

1. Click **Open in Colab** above. You need a Google account. Use
   *File → Save a copy in Drive* if you want to keep your own copy.
2. Run **Cell 1 (Environment Setup & Core Functions)** and then **Cell 1b
   (Statistical Engine)**. These two cells define everything the other cells
   use, and they must run first in every session. Each ends with a status line:
   - Cell 1: **Environment ready**, or amber **Environment incomplete** if a
     package is missing (outside Colab), with how many package versions
     differ from the tested set.
   - Cell 1b: **Statistical engine ready** after a self-test that refits the
     BCG vaccine trials and reproduces the published estimates
     (τ² = 0.3132, μ = −0.7145, SE = 0.1798). If the self-test fails, the line
     turns red: check the package versions before trusting any result.
   - Cell 1 installs missing packages at the tested versions.
   - If a package that is already installed has a different version, Cell 1
     keeps it, so you do not need to restart. The differences are listed in the
     log of Step 27 and recorded in the session file and the validation export.
3. Run the remaining cells **in order** (Step 2, Step 3, ...). Each cell shows
   a form; make your choices and click its button before moving on. Cells that
   depend on an earlier step tell you which step is missing.

If the Colab runtime restarts (or you reconnect after a timeout), all results
are lost: run Cells 1 and 1b again, then continue. You can save a session file
(see [Section 4](#4-saving-and-reproducing-an-analysis)) to avoid redoing the
steps by hand.

**Try it first with a built-in example.** Step 2 has a *Built-in Examples* tab
with five classic datasets:

| Example | Data type | Good for |
|---|---|---|
| Binary (BCG Vaccine, Tuberculosis) | Events / non-events | log OR, log RR, RD |
| Continuous (Normand 1999, Stroke Rehab) | Means / SDs / N | Hedges' g, MD |
| 3-Level Pre-Calculated (Konstantopoulos 2011) | Effect + variance | Three-level model |
| Meta-Regression / Splines (Raudenbush 1985) | Effect + variance | Moderators, splines |
| Ecology Continuous (Curtis 1998, Plant CO₂) | Means / SDs / N | lnRR, subgroups, shared controls |

---

## 2. Preparing your data

Use **one row per effect size** (one comparison or observation). Rows from the
same paper share the same study ID; this is what defines the three-level
structure. Any other columns (species, habitat, method, year, dose, ...) can be
used as moderators and filters.

You choose the data type in Step 2 and map your columns to the fields below.
CoMeta guesses the mapping from common column names (listed in brackets), and
you can change any of them.

**Raw continuous data (means, SDs, sample sizes)**

| Field | Meaning | Recognised names |
|---|---|---|
| Study ID | Paper / study label | `id`, `study`, `study_id`, `paper`, `author` |
| Treatment mean, SD, n | Experimental group | `xe`, `sde`, `ne` (also `mean_e`, `sd_e`, `n_e`, ...) |
| Control mean, SD, n | Control group | `xc`, `sdc`, `nc` (also `mean_c`, `sd_c`, `n_c`, ...) |

**Raw binary data (2×2 tables)**

| Field | Recognised names |
|---|---|
| Study ID | as above |
| Treatment events / non-events | `events_e`, `nonevents_e` (also `a`, `b`) |
| Control events / non-events | `events_c`, `nonevents_c` (also `c`, `d`) |

**Pre-calculated effect sizes**

| Field | Recognised names |
|---|---|
| Study ID | as above |
| Effect size | `yi`, `effect_size`, `es`, `hedges_g`, `lnrr`, `smd`, `g`, `d` |
| Variance **or** standard error | `vi`, `variance`, `var` / `se`, `standard_error` |
| Total sample size (optional) | `n_total`, `n`, `sample_size` |

**Optional columns**

- `year`: publication year, needed for the cumulative meta-analysis (Steps 24
  and 26).
- `latitude` / `longitude` (decimal degrees) and/or `country`: needed for the
  map (Step 25). You map these in Step 2.

Numeric fields are checked when you confirm the mapping: text in a numeric
column is reported, and rows with unusable required values are removed and
listed.

---

## 3. Step-by-step manual

Steps 2–7 are the core workflow. Steps 8 onward are optional and can be run in
any order once Step 7 is done, except that each visualization step needs its
execution step first (e.g. Step 10 needs Step 9). Step 9b uses the overall model
of Step 7 and, if Step 9 was run, the subgroups.

### Data preparation

**Step 2 – Data Ingestion.** Four tabs:
- *Google Sheets*: connect your Google account, type the spreadsheet name, pick
  the worksheet and load it.
- *Upload Excel/CSV*: upload a file and pick the sheet.
- *Restore Session*: load a session file saved earlier (see Section 4).
- *Built-in Examples*: load one of the example datasets.

After loading, choose the data type (raw continuous, raw binary or
pre-calculated), check the column mapping, map the optional geographic columns
and click **Confirm Mapping & Finalize Data**.

**Step 3 – Global Filtering.** Two tabs:
- *Subset filters*: restrict the analysis to part of the data. Add one or more
  filter variables and tick the levels to keep; the counts per level are shown.
  Every later step uses the filtered data.
- *Common row set* (optional): choose moderators that must be complete. Rows
  missing any of them are removed **for all analyses**, so that the overall
  model, subgroups and meta-regressions are all fitted on exactly the same
  rows and can be compared directly. Leave it empty to let each analysis use
  all rows available for its own variables.

Click **Save Configuration**.

**Step 4 – Data Cleaning & Pre-processing.** Runs automatically. It applies the
Step 3 filters, tidies text categories, checks the data for the effect-size
calculation and reports what was kept (*Data Summary*) and what was removed and
why (*Removed Data*).

**Step 5 – Effect Size Selection & Diagnostics.** CoMeta looks at your data
(signs, zeros, sample sizes, spread) and recommends an effect size, explaining
why (*Recommendation*, *Data Patterns* and *Decision Logic* tabs). You can
accept it or pick another:

| Data type | Effect sizes available |
|---|---|
| Raw continuous | log Response Ratio (lnRR), Hedges' g, Cohen's d, Mean Difference (MD), log Coefficient of Variation Ratio (lnCVR) |
| Raw binary | log Odds Ratio, log Risk Ratio, Risk Difference, logit Proportion |
| Pre-calculated | used as supplied |

The **small-sample bias correction** checkbox (lnRR and lnCVR only) is on by
default and applies the second-order corrections of Lajeunesse (2015). For log-scale effect sizes
(lnRR, lnCVR, log OR, log RR) results are also shown back-transformed as ratios
(fold-change).

**Step 6 – Effect Size Calculation.** Computes the effect sizes and their
sampling variances.
- *Missing SDs*: impute with the median CV, impute with the pooled CV (missing
  cases only), replace all SDs with the pooled CV, or drop the rows.
- *Zero SDs*: treat them as missing (then impute) or drop the rows.
- Binary data: 0.5 is added to every cell of a table that has a zero cell
  (only those tables, plus any table that shares a control group with one of
  them, so the shared control counts stay identical). For log OR and log RR, studies with zero events in both
  groups are dropped and listed (they are kept for the risk difference). For
  a logit proportion, 0.5 is added to both counts when either is zero.
- **Shared controls**: rows that share the same control group are detected,
  and the covariance between their effect sizes is built into the sampling
  variance matrix used by all models. Detection is automatic: rows of one
  study with identical control n, mean and SD (or control counts) share a
  control. To set the groups yourself, add a column that gives each row's
  control group (rows of a study with the same label share a control; leave it
  blank for rows with their own control) and select it as **Control-group
  column** in the Step 2 column mapping. It is used only when selected there
  (a column named `control_id` is pointed out but not used on its own);
  otherwise the automatic detection applies.

Click **Calculate & run sensitivity check**. The tabs show a summary, diagnostic
plots, detailed statistics, an interpretation, a sensitivity check (results
with imputed SDs against complete cases only) and the removed rows.

### Overall model

**Step 7 – Overall Meta-Analysis.** The main result.
- *Model*: three-level (recommended) or two-level (as a sensitivity analysis).
  For the two-level model you can choose the τ² estimator: REML, DL, ML, PM or SJ.
  With shared controls, the two-level mean is estimated by generalized least
  squares with weights (V + τ²I)⁻¹, using the full sampling covariance matrix.
  Its CR2 standard error uses the same weights.
- *CR2 / Knapp-Hartung*: cluster-robust small-sample inference (on by default).
- *Inference*: t-distribution (default) or normal (z).
- *Confidence level*: 90, 95 or 99 %.

Results are shown in tabs:
- *Primary Result*: a summary dashboard that explains the result in plain
  language: the pooled effect with its CI, p-value and prediction interval;
  the effect on its original scale (ratio, proportion or correlation); how
  clustering and the CR2 correction change the uncertainty (effect sizes,
  studies, degrees of freedom, model-based vs reported SE); where the
  variation comes from (multilevel I²); whether there is more variation than
  chance (Q test) and how large it is (τ², σ² with CIs). A warning appears
  when there are fewer than 10 studies.
- *Detailed Statistics*: every number of the analysis at full precision, with
  the method behind it: data (effect sizes, studies, effect sizes per study,
  exclusions, sampling covariances), model and estimation, inference settings,
  pooled effect (SE, test statistic, df, p, CI, PI, back-transformed values),
  heterogeneity (Q, I², multilevel I², τ² and σ² with profile-likelihood CIs),
  variance-structure tests, reference models and software versions. A
  plain-text (Markdown) copy with a Copy button is included, for reports or
  for pasting into an AI assistant.
- *Model Selection*: likelihood-ratio test and AIC comparing the nested
  variance structures. This is for information; the model you chose is the one
  reported.
- *Settings*, *Publication Text* and *Export* (Excel audit report and session
  file).

### Moderator analyses

**Step 8 – Subgroup Analysis: Configuration.** Choose single-factor or
two-factor (interaction) analysis and the moderator(s). The thresholds *Min
Papers* (default 3) and *Min Observations* (default 5) exclude groups too small
to estimate. A preview shows how many studies and observations each level has.

**Step 9 – Subgroup Analysis: Execution.** Fits one three-level model with a
mean for each group (and common variance components) and tests whether the
groups differ (HTZ cluster-robust omnibus test).
- *Results Summary*: a dashboard that explains the result in plain language:
  the effect in each subgroup (with CI, prediction interval and the
  back-transformed value), whether the subgroups differ, every pairwise
  difference (with Holm-adjusted p-values), how much heterogeneity the
  moderator explains (τ² and σ² with and without it), and whether the
  comparison is fair (studies per subgroup; between- or within-study
  moderator). Warnings appear for subgroups with fewer than 5 studies, a test
  with fewer than 4 degrees of freedom, excluded subgroups and the fallback
  fit.
- *Detailed Statistics*: every number at full precision with its method
  (subgroup estimates, pairwise differences, omnibus and two-way tests,
  residual τ² and σ² with profile-likelihood CIs, pseudo-R²), with a
  plain-text copy for reports or AI assistants.
- *Processing Log*, *Configuration*, *Publication Text* and *Export* (Excel
  report and session file).

**Step 9b – Proportion of Meaningful Effects.** The pooled mean says how large
the effect is on average; with heterogeneity, the true effects of individual
studies and effect sizes vary around it. This step answers a question the mean
cannot: *what share of true effects is large enough to matter?*

1. *Thresholds*: set what counts as meaningful. For log-ratio effect sizes
   (lnRR, log OR, log RR, lnCVR) enter a percent change, e.g. 10% (an increase
   of 10% is a ratio ≥ 1.10, a decrease of 10% a ratio ≤ 0.90); for Hedges' g
   or Cohen's d use SD units; otherwise the analysis scale. Untick *Same
   threshold in both directions* to set increases and decreases separately.
2. *True effects of*: individual effect sizes (τ² + σ², default) or study
   means (τ² only; three-level model).
3. *Bootstrap resamples*: see below. Click **Compute Proportions**.

CoMeta then estimates, for the overall model and for each subgroup of Step 9,
the share of true effects that are **meaningful increases**, **meaningful
decreases** and **negligible** (Mathur & VanderWeele 2019, 2020):
- *Parametric* estimates assume normally distributed true effects with the
  fitted mean and heterogeneity (τ² + σ² for individual effect sizes, or τ²
  for study means).
- *Calibrated* estimates make no normality assumption: each effect size is
  shrunk toward its model mean and the shares are counted directly. When the
  two disagree, the true effects are probably not normal; prefer the calibrated
  estimate.
- Confidence intervals come from a cluster bootstrap (whole studies resampled,
  the model refitted each time); a quick delta-method CI is also given for the
  parametric estimate. Choose the number of resamples: **50** or **200** to
  explore thresholds quickly (bias-corrected percentile intervals, clearly
  marked as exploratory), **1000** or more for the results you report (BCa
  intervals). A progress bar shows the time left.

The results come as a dashboard, a **🔢 Detailed Statistics** tab, publication
text, a CSV export and a figure. The dashboard explains the shares in plain
words. It shows stacked bars for every group (calibrated and parametric), the
distribution of true effects with the thresholds marked, and the overall shares
with their confidence intervals. It also gives warnings for exploratory runs,
missing bootstrap intervals, T² = 0 and few studies. The Detailed Statistics tab
lists every number at full precision: the thresholds on the analysis scale, the
model, τ², σ², T² and SE(T²), and each share with its bootstrap and
delta-method CIs. It also has a plain-text copy to paste into a report or an AI
assistant. The figure shows stacked bars for all groups with their CIs, or the
distribution of true effects for one group, and has its own plot recipe. Choose the thresholds before
looking at the results, from what is biologically or practically relevant for
your outcome.

**Step 10 – Forest Plot** and **Step 11 – Orchard Plot** visualize the
subgroups. Both have tabs for style, text, annotations (k, number of papers,
fold-change, CI text), axes, labels (rename each group), export and an
auto-generated figure caption. The orchard plot shows the individual effect
sizes (scaled by precision), the CI (thick line) and the prediction interval
(thin line) for each group. In a two-factor analysis both plots group the rows
by the first moderator.

**Step 12 – Meta-Regression.** Choose one or more moderators. For each, choose
whether it is continuous or categorical and, for categorical ones, the
reference level. Click **Run Meta-Regression**.
- *Results*: a dashboard that explains the model in plain language: what each
  moderator does (per unit, or each level vs the reference, with the change
  over the observed range and the ratio scale for log ratios), predicted
  effects (a bubble plot with CI and prediction bands for one continuous
  moderator; otherwise predictions at typical values, kept inside the
  observed range; their CI and prediction intervals follow the t or z choice
  of Step 7), the tests of the moderators, how much heterogeneity they
  explain, and whether the analysis is reliable (studies per coefficient,
  moderator coverage, within- or between-study moderators). Warnings appear
  for fewer than 10 studies per coefficient, coefficients with fewer than 4
  degrees of freedom, categories with fewer than 5 studies and excluded rows.
- *Detailed Statistics*: every number at full precision with its method
  (coefficients, CR2 / Knapp–Hartung tests, residual τ² and σ² with
  profile-likelihood CIs, pseudo-R², predictions, the coefficient covariance
  matrix, diagnostics), with a plain-text copy for reports or AI assistants.
- *Publication Text* and *Export* (Excel report).

**Step 13 – Meta-Regression: Visualization.** Bubble plot of the effect against
a continuous moderator of the model (choose which one for the x-axis), with the
regression line, confidence band, equation, p and R², bubbles sized by their
model weight and optional colouring by another moderator. With several
moderators, the line holds the others at their mean (continuous) or reference
level (categorical).

**Step 14 – Non-Linear Spline Meta-Regression.** Fits a natural cubic spline of
a continuous moderator (choose the spline df, default 3). A likelihood-ratio
test against the linear model shows whether the relationship is non-linear,
and the HTZ omnibus test shows whether the moderator matters at all.
- *Adjust for* (optional): other moderators to hold constant, so the curve
  shows the change with the spline moderator after accounting for them.
  - Numeric moderators enter as straight-line terms, centred at their mean.
  - Text moderators enter as categories, against a reference level you choose
    (the default is the level with the most effect sizes).
  - The curve is the partial effect, drawn at the mean or reference level of
    each adjustment moderator.
  - The plotted points are the effect sizes minus the estimated contribution
    of the adjustment moderators, so they are comparable with the curve.
  - Both tests keep the adjustment terms in every model they compare.
  - The pseudo-R² of the adjustment moderators alone is also reported, so you
    can see what the curve adds.
  - Each adjustment adds parameters: aim for at least 10 studies per
    coefficient. A warning appears below that, and the run stops when there
    are fewer studies than coefficients plus two.
- *Results*: a dashboard that reads the two tests in order (does the effect
  change with the moderator? is the change curved?), draws the fitted curve
  over the effect sizes with its CI and prediction bands, the best straight
  line and the knots, shows how much heterogeneity the spline explains, and
  how reliable the curve is (studies along the moderator range, studies per
  coefficient, sparse ends). Warnings appear for sparse ends, few studies per
  coefficient, a test with fewer than 4 degrees of freedom and fallbacks.
- *Detailed Statistics*: every number with its method (knots, basis
  coefficients, both tests with the ML fits, residual τ² and σ² with
  profile-likelihood CIs, pseudo-R², the predicted curve at the knots,
  diagnostics), with a plain-text copy for reports or AI assistants.

**Step 15** plots the fitted curve
with its confidence band and the non-linearity test. With adjustment
moderators, it plots the adjusted points and the caption says where the curve
is drawn.

**Step 16 – Exploratory Meta-Forest.** A random forest that ranks many
moderators by their importance, with cross-validation by study. Use it to
explore which moderators may matter, then test them with Steps 9 or 12. It is
not a confirmatory test. The **Results** dashboard shows each moderator's
permutation importance on held-out studies. Each moderator is marked
*consistent*, *unstable* or *none* by how it varies across folds. The dashboard
also gives the out-of-bag R² with a reading guide and the step where each
promising moderator should be tested. **🔢 Detailed Statistics** lists the data,
the forest settings, the weights (τ² and its source), the out-of-bag R², and
each importance score with its SD across folds. Columns derived from the effect
size, such as `fold_change`, `Response_Ratio`, `Odds_Ratio` and CI bounds, are
never offered as moderators here or in Steps 8, 12 and 14. Neither is any
numeric column whose ranks match the effect size exactly.

### Publication bias

**Step 17 – Egger's Test & Trim-and-Fill.**
- *Egger's test*: multilevel regression of the effect on its standard error
  with CR2 inference.
- *Trim-and-fill*: estimators L0 and R0 to estimate the missing studies and
  the adjusted effect.
- *Combined Assessment* summarizes both.
- *Detailed Statistics*: every number of both methods with its method, with a
  plain-text copy.
- Also has publication text and an Excel report.

**Step 18 – Trim-and-Fill Plot.** Funnel plot with observed and imputed effect
sizes, pseudo-confidence guides and the original and adjusted means.

**Step 19 – PET-PEESE.** Precision-effect test and precision-effect estimate
with standard error. If the PET intercept is significant (P-threshold, default
0.10 two-sided), the PEESE estimate is used; otherwise the PET estimate.
Tabs: summary, visuals, interpretation, *Detailed Statistics* (both models,
the decision rule and the recommended estimate) and publication text.

**Step 19b – Time-Lag Test (Decline Effect).** Tests whether effect sizes
change with publication year, as expected when large or significant results are
published sooner (time-lag bias). It fits a multilevel meta-regression of the
effect on publication year (centred), with effect sizes nested in studies, the
shared-control covariances and CR2 inference, as in the other steps. A
precision term separates a decline over time from a small-study effect
(Nakagawa et al. 2022). Choose it in *Precision term*: √(1/ñ) (effective sample
size; the default for Hedges' g, Cohen's d, lnRR and lnCVR when the group
sample sizes are in the data, because their SE depends on the effect itself),
the standard error, or none. The year-only model is shown
as a sensitivity analysis. A year slope opposite in sign to the overall mean
means effect sizes move toward zero over time. Needs a `year` column; effect
sizes without one (or without the chosen precision term) are excluded and
counted, and the year-only model uses the same effect sizes. Tabs: results, plot (bubble plot
of effect against year with the fitted line and confidence band, journal
presets, PDF/PNG/SVG, caption and plot recipe), publication text, *Detailed
Statistics* (both models, settings and exclusions) and an Excel report. Unlike the cumulative meta-analysis (Step 24), which shows how
the pooled mean changed as studies accumulated, this is a formal test.

**Step 19c – Publication Bias: Overview.** Brings together the
publication-bias steps run in the session (17, 19, 19b); nothing is refitted.
The dashboard shows how the average effect of Step 7 changes under each
correction (PET, PEESE with the recommended one marked, trim-and-fill), which
signals of small-study effects were found (Egger's slope, trim-and-fill, the
PET slope, a decline over time), whether the conclusion changes (direction,
significance, size), and how to read the results (a signal is not proof of
publication bias; no signal is not proof of none). The verdict is based on the
PET-PEESE estimate the rule recommends. *Detailed Statistics* lists every number
of the three steps, with a plain-text copy. Re-run it after re-running any of
them.

**Step 20 – Funnel Plot.** Contour-enhanced funnel plot: shaded significance
regions (p ≤ 0.10, 0.05, 0.01) around the no-effect value, an optional
pseudo-confidence region around the pooled effect, optional colouring by a
moderator and the result of Egger's test from Step 17.

### Sensitivity analyses

**Step 21 – Leave-One-Out.** Refits the overall model leaving out one study at
a time and reports how much the estimate changes and which studies change its
significance. The **Results** dashboard explains the outcome in plain words. It
shows the pooled effect without each study as a forest, the studies that move
the estimate most (against the 20% threshold), whether removing one study
changes the conclusion (the CI crossing no effect), and whether one study
drives the heterogeneity. **🔢 Detailed Statistics** lists the model with all
studies and every refit (estimate, SE, df, CI, p, shift, τ², σ²). **Step 22** plots the results (sorted by effect, by influence or
by study ID, with significance changers highlighted).

**Step 23 – Baujat Plot.** Each study's contribution to heterogeneity (Q)
against its influence on the pooled effect, (μ − μ₋ᵢ)²/SE²₋ᵢ (Baujat et al.,
2002), with labels for the most outlying studies.

### Complementary analyses

**Step 24 – Cumulative Meta-Analysis.** Adds studies in order of publication
year (oldest first or newest first) and refits the model at each step. The
default (*By Study, multilevel model*) refits the model of Step 7 on all effect
sizes of the studies included so far (effect sizes nested in studies, shared
controls, CR2 when on; at the first steps, while the CR2 degrees of freedom are
below 4, model-based standard errors are used). Two simpler options remain: study means pooled with a
two-level model (approximate: it ignores within-study heterogeneity, so its
intervals can be too narrow) and each effect size as independent. Needs a
`year` column. The **Results** dashboard explains the outcome in plain words. It
plots the cumulative estimate with its CI band and marks from when the CI
excludes no effect. It also shows how precision grew and how I² and τ² evolved,
and says whether the estimate has stabilized (less than 10% change over the
last five steps). **🔢 Detailed Statistics** lists the settings, a summary and
every step (estimate, SE, df, CI, τ², σ², I², inference). **Step 26 –
Cumulative Trends** plots the cumulative effect with its confidence band and,
optionally, the I² trajectory on a second axis.

**Step 25 – Geographic Distribution.** Interactive world map of the studies.
Bubble map from coordinates, choropleth by country, or both side by side. You
can choose the projection, base map, colour scale (centred at the no-effect
value for diverging scales) and what the colour and size represent (effect
size, weight, study count, ...). Country names are matched to ISO codes; names
that could only be guessed are flagged.

**Step 27 – Export Session.** Downloads the session file (see Section 4).

---

## 4. Saving and reproducing an analysis

The **session file** (`.json`) contains the data as loaded in Step 2 and all
settings of Steps 2–9b:
- column mapping, filters and common row set;
- effect size, bias correction and SD handling;
- the overall-model settings and the subgroup configuration;
- the meaningful-effect thresholds of Step 9b.

You can download it from Step 27 (*Download Session File*) or from the
*Download Settings JSON* buttons in Steps 7 and 9.

To reproduce an analysis:

1. Run Cells 1 and 1b.
2. In Step 2, open the *Restore Session* tab and upload the session file.
3. Run Steps 3–9 in order. They pick up the stored settings automatically,
   with no clicking needed. Step 9b fills in the stored thresholds; click
   *Compute Proportions*.
4. For Step 12 onward (meta-regression, splines, publication bias, sensitivity
   and complementary analyses), select the options again; these choices are not
   stored.

This is also a convenient way to share an analysis with co-authors or
reviewers: send them the notebook link and the session file.

### Plot recipes (one file per figure)

Every plot cell has **💾 Save Plot Recipe** and **📂 Load Plot Recipe**
buttons. A plot recipe is a small `.json` file with:
- the numbers the figure draws (already computed, so nothing is refitted);
- every setting of the plot cell, including renamed labels;
- a note of the analysis it came from (for example "Subgroups by habitat",
  the model, the CI level and when it was run).

Loading a recipe in the same plot cell redraws the figure exactly, even in a
new session where only Cells 1 and 1b were run. This is useful when an analysis
needs several subgroup analyses or meta-regressions: save one recipe per
figure, and you can restyle or re-export any of them later without running
Steps 8–9 (or 12, 14, ...) again. Tick **Apply style only** before loading to
take just the settings (sizes, fonts, colours, labels) and keep the data
currently in the session, for example to give all figures the same style.

A plot cell shows which analysis it is plotting at the top. If that analysis is
run again after the plot cell, the plot cell warns that it still shows the
earlier results; re-run the plot cell to plot the new ones.

---

## 5. Statistical methods

**Model.** The three-level model is

  y<sub>ij</sub> = μ + u<sub>j</sub> + w<sub>ij</sub> + e<sub>ij</sub>

for effect size *i* in study *j*:
- *u<sub>j</sub>* ~ N(0, σ²<sub>between</sub>) is the between-study variation;
- *w<sub>ij</sub>* ~ N(0, σ²<sub>within</sub>) is the within-study variation;
- *e<sub>ij</sub>* is the sampling error, with a known (co)variance that
  includes shared-control covariances.

The variance components are estimated by REML (ML for likelihood-ratio tests
between models with different fixed effects). The two-level model is the
standard random-effects model (with shared controls, its weights use the full
sampling covariance matrix).

**Inference.**
- By default, tests and CIs use the CR2 cluster-robust variance estimator with
  Satterthwaite degrees of freedom (clustered by study). This keeps inference
  valid when the variance structure is misspecified or effect sizes are
  correlated within studies.
- Tests of several coefficients (subgroup differences, meta-regression
  omnibus) use the HTZ approximate F test.
- Turning CR2 off gives model-based standard errors with t or z inference.

**Heterogeneity.**
- Cochran's Q.
- Multilevel I² split into between- and within-study parts.
- Profile-likelihood CIs for the variance components.
- Prediction intervals.

**Effect sizes** use the standard formulas (Borenstein et al., 2009; Hedges
et al., 1999 for lnRR; Nakagawa et al., 2015 for lnCVR; Barendregt et al., 2013
for the logit proportion), with the small-sample corrections for lnRR and lnCVR
(Lajeunesse, 2015) and the bias-corrected Hedges' g (Hedges, 1981). They are
checked against R in Validation 20.

**Publication bias.**
- Egger's test and trim-and-fill use the full sampling covariance matrix
  (including shared controls).
- Trim-and-fill chooses the side to fill from the funnel asymmetry: the sign
  of the slope of the effect sizes regressed on their standard errors
  (negative: studies missing on the right).
- PET-PEESE uses the conditional rule described in Step 19.

**Proportion of meaningful effects.** Under the multilevel model the true
effect of an effect size is N(μ, τ² + σ²), and the true mean of a study
N(μ, τ²); with one effect per study both reduce to N(μ, τ²), the setting of
Mathur & VanderWeele (2019). The parametric share is 1 − Φ((q − μ)/T), with a
delta-method SE from SE(μ) and SE(T²), where the covariance of the variance
components comes from the observed information of the REML likelihood.
Calibrated estimates shrink each effect size toward its
model mean by √(T²/(T² + vᵢ)) (Wang & Lee, 2019). Bootstrap CIs resample
studies, refit the model and use BCa intervals with a leave-one-study-out
jackknife for the acceleration (Efron, 1987) (quick
exploratory runs skip the jackknife: bias-corrected percentile intervals). The
resamples start from the full-data estimates, which makes them fast without
changing the result. The shares and calibrated estimates are checked against
R in Validation 25 (one-effect-per-study case). Validation 27 checks the
three-level case by simulation: the bias of both shares and the coverage of
both CIs, on normal and skewed true effects, 15 or 30 studies, shared controls
and study-level shares. In those simulations the calibrated share stayed close
to the truth when the true effects were skewed, while the parametric share
(which assumes normal true effects) was biased by about 0.05. The delta-method
CI covered poorly when the true share was below 0.15; use the bootstrap CI
there. With 15 studies, coverage was slightly below nominal.

---

## 6. Outputs

- **Tables and results** in each step's tabs.
- **Publication text**: Methods and Results paragraphs in the *Publication
  Text* tab of each analysis, with the numbers filled in.
- **Excel reports**: audit report (Step 7) and reports for subgroups,
  meta-regression, splines, publication bias, time-lag test and cumulative analysis; a CSV
  table of the meaningful-effect shares (Step 9b).
- **Figures**: forest, orchard, meaningful-effects, bubble, spline,
  trim-and-fill, time-lag, funnel, leave-one-out, Baujat, cumulative trend and map plots.
  Every plot can be customized (size, fonts, colours, labels, axis limits) and
  saved as PDF, PNG
  (adjustable DPI) and SVG, with an optional transparent background. Each plot
  cell has a **figure size preset** and generates a figure caption. The
  presets set the width, height and font sizes at printed size:
  - **Generic** 1 column (85 mm), 1.5 columns (120 mm) and full width (175 mm),
    which fit most journals;
  - the exact column widths of **Elsevier** (90, 140, 190 mm), **Nature** (89,
    183 mm) and **PLOS** (190 mm);
  - a thesis page and a 16:9 presentation slide.
  Check your target journal's instructions, which take precedence. The map is saved as an interactive HTML file
  (PNG/PDF/SVG too if the `kaleido` package is installed). In Colab, saved files
  appear in the *Files* panel on the left.
- **Session file** and **plot recipes** for reproducibility (Section 4).

---

## 7. Troubleshooting

| Problem | Solution |
|---|---|
| "CoMeta setup not found in this session" | Run Cells 1 and 1b again (the runtime was restarted or the cells were not run). |
| A dashboard shows an inner scroll bar, or you prefer one | In Colab each step's output grows to its full height. To get Colab's scrolling back, set `COMETA_FULL_HEIGHT_OUTPUT = False` in Cell 1 (just above `es_null_value`) and re-run Cell 1. |
| Package versions differ from the tested set (log of Step 27) | Usually harmless; the analysis runs with the installed versions. |
| A step says an earlier step is missing | Run the steps in order. If you change something in an early step, re-run the following steps. |
| "'year' column not found" (cumulative analysis) | Add a `year` column to your data. |
| No map types available | Map latitude/longitude or country in Step 2. |
| A subgroup is missing from the results | It has fewer papers or observations than the Step 8 thresholds; see the processing log in Step 9. |
| Step 9b takes long | Use 50 or 200 bootstrap resamples to explore thresholds, then 1000 for the final run; the progress line shows the time left. |
| Step 9b shows no subgroups | Run Step 9 first. If Step 9 fell back to separate per-group fits, the subgroup shares are not computed (a note says so). |
| "… resamples could not be fitted" (Step 9b) | A small subgroup was missing from some bootstrap resamples; those resamples are skipped. With many skipped, the subgroup CIs are unreliable. |
| "This recipe is for a … plot" | Load a plot recipe in the plot cell that saved it (e.g. a forest-plot recipe in Step 10). |
| The map cannot be saved as PNG/PDF | Install `kaleido` (`pip install kaleido`) or use the interactive HTML file and the camera button on the map. |
| You want to see the warnings | Numerical messages from numpy/scipy while models are fitted (e.g. "invalid value encountered") come from trial values the optimiser rejects; CoMeta checks convergence itself, so they are not printed. CoMeta's own messages appear as a short yellow line. Both are kept in the *Warnings log* in Step 27. |
| Google Sheets does not connect | Allow the Google sign-in pop-up, or download the sheet and use *Upload Excel/CSV*. |

---

## 8. Validation suite (for developers)

CoMeta keeps all its code in the notebook on purpose: you can read how every
number is computed, change it, and try new ideas. The **validation suite**
(the 🧪 cells after Step 27) is the verification system for those changes.
Each validation recomputes a CoMeta result in R (`metafor`, `clubSandwich`,
`MetaUtility`) and checks that the two agree.

**It runs on your analysis.** The validations use the data, the sampling
variance–covariance matrix (including shared controls), the settings and the
results of the steps you ran in this session. Change a cell, re-run your
analysis and the matching validation, and you see right away, on your own
data, whether CoMeta still matches R.

How to use it:
1. Run your analysis (Steps 2–27, or the steps you changed).
2. Run **Validation: Imports & R Setup** (installs/loads the R packages).
3. Run the validations you need, then **Validation Summary & Export**.

Each validation is *PASS*, *FAIL*, *not run* (the analysis step it checks was
not run in this session, e.g. Validation 3 needs Step 9) or *skipped*. A
validation that crashes is recorded as *FAIL*.

**Reference datasets (optional).** Tick *Also run the fixed reference
datasets* in the R setup cell to add fixed benchmarks (`metadat` datasets and
simulated edge cases: shared controls, missing years, singletons, unbalanced
clusters). They reach code paths your data may not use; validations that use
only them (6 and 8) are *skipped* while the box is unticked. The Monte Carlo
validations (2, 5, 9, 27: bias and coverage) and the unit tests (11) use generic
simulated data and do not depend on your analysis.

The summary cell exports the results, with package versions, to
`cometa_validation_results.json`.

---

## 9. Citation, license and contact

**Version.** This is CoMeta **1.0.0**. The version appears in the notebook
header and is recorded in every session file, Excel report and validation
export. [CHANGELOG.md](CHANGELOG.md) lists the changes between versions.

**How to cite.** If you use CoMeta in published work, please cite the software
and the methods papers it relies on (the generated publication text lists
them). Citation details are in [CITATION.cff](CITATION.cff): GitHub's
**Cite this repository** button gives them in APA and BibTeX. The notebook
header shows the same citation.

**License.** CoMeta is free software, released under the
[GNU General Public License v3.0 or later](LICENSE). You may use, study,
change and share it. If you distribute a modified version, it must also be
released under the GPL with its source code.

Questions, bug reports and suggestions are welcome through the
[GitHub issues](https://github.com/ErickJLA/CoMeta/issues) page.
To fix something, add a method or keep your own version of CoMeta, see
[CONTRIBUTING.md](CONTRIBUTING.md).
