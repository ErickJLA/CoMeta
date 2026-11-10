# Contributing to CoMeta

CoMeta is never finished. It is a meta-analysis tool, and it is also an open
workbench: all the statistics are written out in the notebook so you can
read them, question them, change them and try new ideas on your own data.
Most people will only use it, and that is fine. This guide is for those who
want to go further: report a problem, fix a bug, add a method, or keep their
own version (a fork).

You do not need to be a professional programmer. A clear bug report with
your data and settings is as valuable as a pull request.

CoMeta is released under the [GNU GPL v3.0 or later](LICENSE). By
contributing, you agree that your contribution is released under the same
license. A fork you distribute must keep the license and make its source code
available. When you change results, add an entry to
[CHANGELOG.md](CHANGELOG.md) and raise the version in three places (`COMETA_VERSION` in Cell 1, the first
notebook cell and `CITATION.cff`): MAJOR for
changes that alter results or break saved project files, MINOR for new features,
PATCH for fixes.

---

## Contents

1. [Ways to contribute](#1-ways-to-contribute)
2. [How CoMeta works](#2-how-cometa-works)
3. [Conventions](#3-conventions)
4. [Checking your change](#4-checking-your-change)
5. [Adding a new method or a new validation](#5-adding-a-new-method-or-a-new-validation)

---

## 1. Ways to contribute

| You want to… | What to do |
|---|---|
| Report a bug or a wrong number | Open an [issue](https://github.com/ErickJLA/CoMeta/issues) (see below what to include). |
| Report a difference between CoMeta and R | Open an issue with the validation results file (`cometa_validation_results.json`). |
| Suggest a method, an option or a plot | Open an issue first, with a reference for the method, so we can agree on the approach before you write code. |
| Fix a bug or improve the text | Fork the repository, make the change on a branch, check it (section 4) and open a pull request describing what changed, why, and what you checked. |
| Improve the documentation | Edit `README.md` or this file and open a pull request. |
| Share a test dataset | A published dataset with known results (e.g. from a paper or an R package) is very useful for the validation suite. |

**A good bug report contains:**
- what you did (the step and the options you chose) and what you expected;
- the message or the number that looks wrong (a screenshot helps);
- the **project file** with the analysis that shows the problem (save it with
  **💾 Save analysis** in Step 7, 9 or 9b): it holds your settings and data, so
  the problem can be reproduced exactly. If the data cannot be
  shared, say so; a small made-up dataset that shows the same problem is
  enough;
- the **Warnings log** from Step 27, if the problem came with warnings.

---

## 2. How CoMeta works

Everything lives in `CoMeta.ipynb`. That is on purpose (a *glass box*):
there is no hidden package, so what you read is what runs. This section
explains how the cells fit together, so you know where a number comes from
and where a change has to go.

To find the code behind something you see, search the notebook (Colab:
**Edit → Find and replace**) for the label in the output. Expand a form cell
(double-click it, or *Show code*) to see its code.

### 2.1 The big picture

The cells run top to bottom. They share their state through one dictionary,
**`ANALYSIS_CONFIG`**: each step reads the keys it needs and writes its
settings and results back. A step never depends on another cell's private
variables, only on `ANALYSIS_CONFIG` and the shared functions of Cells 1 and
1b.

```
Step 2  Data ingestion      → raw_data_standardized (columns renamed: id, xe, sde, ne, xc, sdc, nc
                                                     or events_e, nonevents_e, events_c, nonevents_c)
Step 3  Global filters      → ANALYSIS_CONFIG['clean_dataframe'], ['prefilters'], ['complete_case_moderators']
Step 4  Cleaning            → data_filtered (+ 'shared_group_id' for rows sharing a control)
Step 5  Effect-size choice  → ['es_config'], ['effect_col'], ['var_col'], ['bias_correction'], ...
Step 6  Effect sizes        → ['analysis_data']  (one row per effect size)
                              ['vcv_matrices']   (study id → sampling variance–covariance block)
Step 7  Overall model       → ['global_settings'] (inference choices used by every later step)
                              ['overall_results'], ['overall_text']
Steps 8–26  Analyses        → read analysis_data + vcv_matrices + global_settings,
                              write '<analysis>_results' and '<analysis>_text'
Steps 7–24 "Save analysis" → project file (data versions + named analyses:
                              settings, key results; no full results)
```

| Cells | What they hold |
|---|---|
| **1. Environment Setup & Core Functions** | Imports, the τ² estimators (REML, ML, PM, SJ, DL), CR2 / Satterthwaite inference and the HTZ Wald test (`_compute_robust_var_betas`), the warning router and log, the stale-results banners, figure saving and plot recipes, the project file (`project_*`, save bar, manager). |
| **1b. Statistical Engine** | `FitSpec`, `build_fit_spec`, `fit_mv`, `fit_blocks`, `fit_cr2`, `compare_fits`, `pseudo_r2`, row accounting, VCV slicing, proportion of meaningful effects. |
| **2–6. Data** | Ingestion and column mapping, global filters, cleaning and shared-control detection, effect-size choice, effect sizes and sampling VCVs (`build_vcv_matrices`). |
| **7. Overall model** | Fixed-effect, two-level and three-level models, heterogeneity, prediction interval, Methods/Results text. |
| **8–16. Moderators** | Subgroups, proportion of meaningful effects, meta-regression, splines, meta-forest, with their plots. |
| **17–20. Publication bias** | Egger, trim-and-fill, PET-PEESE, time-lag test, the overview of all of them (19c), funnel plot. |
| **21–26. Sensitivity and complementary analyses** | Leave-one-out, Baujat, cumulative meta-analysis, maps, trends. |
| **27. Project File** | Project manager, warnings log. |
| **🧪 Validation cells** | R setup, Validations 1–28 (Python vs R, and Monte Carlo checks), Validation 11 (unit tests), summary and export. |

### 2.2 The keys in `ANALYSIS_CONFIG`

**Settings** (what the user chose; saved with each analysis in the project file):

| Key | Written by | Content |
|---|---|---|
| `prefilters`, `complete_case_moderators` | Step 3 | Global filters; moderators that define the common row set. |
| `shared_control_column` | Step 2 | Column that labels control groups, or `None` (automatic detection). |
| `data_type`, `effect_size_type`, `es_config` | Step 5 | The effect size and its description: column names, labels, log scale or not, null value. |
| `effect_col`, `var_col`, `se_col`, `ci_lower_col`, `ci_upper_col` | Steps 5–6 | Column names in `analysis_data` (e.g. `lnRR`, `var_lnRR`). Always read them from here; never hard-code `yi`. |
| `bias_correction`, `sd_missing_strategy`, `sd_zero_strategy` | Steps 5–6 | Effect-size options and missing/zero SD handling. |
| `global_settings` | Step 7 | `alpha`, `ci_percent`, `dist_type` (`'t'` or `'norm'`), `tau_method`, `use_kh` (CR2 / Knapp–Hartung on or off), `model_choice` (three-level or two-level). |
| `subgroup_config`, `meaningful_config`, … | each step | That step's own options. |

**Data and results** (rebuilt by running the steps; not saved in the project file, except a few key results per analysis):

| Key | Written by | Content |
|---|---|---|
| `analysis_data` | Step 6 | One row per effect size: `id` (study), the effect, its variance, SE, CI, and all moderator columns. |
| `vcv_matrices` | Step 6 | `{study id: k×k sampling VCV}`; off-diagonals are non-zero only for shared controls. |
| `removed_records`, `complete_case_log` | Steps 4, 6 | Every excluded row and why. |
| `overall_results` | Step 7 | All models; `overall_results['reported']` is the model the user reports (`mu`, `se`, `ci_lower`, `ci_upper`, `pi_lower`, `pi_upper`, `tau_squared`, `sigma_squared`, `df`, …). |
| `subgroup_results`, `meta_regression_RVE_results`, `spline_model_results`, `meta_forest_results`, `funnel_results`, `trimfill_results`, `pet_peese_results`, `timelag_results`, `loo_results`, `cumulative_results`, `meaningful_results` | each analysis | That analysis's numbers, read by its plot cell and by the validations. |
| `overall_text`, `subgroup_text`, `regression_text`, `bias_text`, … | each analysis | Generated Methods/Results text. |

### 2.3 Effect sizes, sampling covariances and row identity

Step 6 computes the effect sizes and builds one sampling VCV block per study
(`build_vcv_matrices`). When rows share a control group, the block has
covariances between their effect sizes (Gleser & Olkin 2009; Lajeunesse
2011). Every model uses this V, so it must stay matched to the rows.

The rule is **row identity, never row position**:
- `analysis_data` keeps its original index. When an analysis uses a subset
  (rows with a moderator value, one subgroup, leave-one-out), keep the index
  (do not `reset_index`), and the engine slices each study's block to the
  rows that remain.
- `attach_vcv_row_pos(df)` adds a `_vcv_row_pos` column (each row's position
  inside its study's block), so the identity survives sorting.
  `cluster_vcv(...)` / `slice_vcv_block(...)` return the right sub-block.
- The **common row set** (Step 3) is applied in Step 6 before the VCVs are
  built, so all analyses can use exactly the same rows.

### 2.4 The model engine (Cell 1b)

All models (overall, subgroups, meta-regression, splines, Egger,
trim-and-fill, leave-one-out, cumulative, time-lag) are fitted by one
engine, so there is one likelihood and one optimiser to validate
(Validation 15 checks it against `rma.mv`).

The model, per study *i*:

  *y*ᵢ = *X*ᵢβ + *u*ᵢ**1** + *e*ᵢ + sampling error,  Var(*y*ᵢ) = *V*ᵢ + τ²**J** + σ²**I**

with τ² the between-study and σ² the within-study variance. Either can be
held fixed (e.g. σ² = 0 gives the two-level model).

The pieces:

| Object | Role |
|---|---|
| `select_rows` / `RowAccounting` | Drops rows in a fixed order (missing id → effect → variance → complete-case columns) and records every dropped row with its reason. `accounting.summary_text()` gives "Used 102 of 102 effect sizes in 29 of 29 clusters". |
| `build_fit_spec(df, X=..., complete_case_cols=...)` | Builds a `FitSpec`: the exact rows, the y, V and X blocks per study, and the row accounting. Reads `effect_col`, `var_col` and `vcv_matrices` from `ANALYSIS_CONFIG` by default. |
| `fit_mv(spec, tau2=None, sigma2=None, method='REML')` | REML/ML fit. `None` = estimated (bounded at 0); a number = held fixed. Searches the interior and every boundary face, so the log-likelihood is the true constrained maximum. Returns an `MVFit` (`betas`, `cov_beta` (model-based), `se`, `tau2`, `sigma2`, `loglik`, `aic`, `converged`, `structure`, `notes`). |
| `fit_blocks(y_blocks, V_blocks, X_blocks, ...)` | The entry point most analysis cells use: same fit from blocks they assembled themselves; picks the two-level model when no study has more than one effect size, and can fall back to a diagonal V (with a note) when a block is not a valid covariance. |
| `fit_cr2(fit)` | CR2 cluster-robust covariance and Satterthwaite df on exactly the blocks and variance components of `fit` (as `clubSandwich::vcovCR(type = "CR2")` / `coef_test`). With `with_wald_helper=True` it also returns the HTZ Wald test used for omnibus tests. |
| `compare_fits(full, reduced)` | AIC/BIC/LRT between two fits. Refuses (`ComparisonError`) when they use different rows or a different V; refits under ML when the fixed effects differ; boundary-corrected p-values for variance components. |
| `pseudo_r2(model, null)` | Share of heterogeneity explained (total, per level), with the null fitted on the same rows and V. |

**Try it.** After running Steps 2–7, a new cell can fit its own models with
the same machinery (this example uses the Curtis 1998 example data and its
`method` moderator):

```python
import numpy as np, pandas as pd
from scipy import stats

cfg = ANALYSIS_CONFIG
df  = cfg['analysis_data']                  # keep the original index
gs  = cfg['global_settings']                # Step 7 choices

# Model 0: intercept only (the overall three-level model)
spec0 = build_fit_spec(df, label='intercept only')
fit0  = fit_mv(spec0)                       # REML, tau² and sigma² estimated

# Model 1: a moderator, on exactly the same rows and the same V
X = pd.get_dummies(df['method'], prefix='method', drop_first=True, dtype=float)
X.insert(0, 'intrcpt', 1.0)
spec1 = build_fit_spec(df, X=X, label='method')
fit1  = fit_mv(spec1)

# Inference as the notebook does it: CR2 + Satterthwaite df
V_cr2, df_cr2 = fit_cr2(fit1)
se = np.sqrt(np.diag(V_cr2))
p  = 2 * stats.t.sf(np.abs(fit1.betas / se), df_cr2)
print(pd.DataFrame({'estimate': fit1.betas, 'SE (CR2)': se, 'df': df_cr2, 'p': p},
                   index=spec1.term_names))

print(pseudo_r2(fit1, fit0)['R2'])          # share of heterogeneity explained
cmp = compare_fits(fit1, fit0)              # refitted under ML (different fixed effects)
print(cmp.delta_aic, cmp.lrt, cmp.p_value)
print(spec1.accounting.summary_text())
```

This is the starting point for a new idea: change the design, fix a
variance component, use a subset, and the rows, V and inference stay
consistent with the rest of the notebook. To use the user's inference
choices, read `gs['use_kh']` (CR2 on/off), `gs['alpha']` and
`gs['dist_type']`, as the time-lag cell (`fit_timelag_model`) does.

### 2.5 Anatomy of an analysis cell

The larger steps share one structure (see Step 7: `OverallDataManager`,
`OverallEngine`, `OverallHTMLTemplates`, `OverallPublicationTextGenerator`,
`OverallResultsView`, `OverallController`):

1. **Setup check** at the top: the cell stops with a clear message if Cells
   1 and 1b have not run in this session.
2. **Data manager**: all reading from and writing to `ANALYSIS_CONFIG`
   (`analysis_data`, `vcv_matrices`, settings), with checks that the data
   are there.
3. **Engine**: the statistics, using the Cell 1b engine; no widgets or HTML
   here, so it can be unit-tested and validated on its own.
4. **Views and text**: HTML tables, plots, and the generated Methods/Results
   text with references.
5. **Controller**: the widgets (forms and buttons); on *Run* it calls the
   engine, stores `<analysis>_results` and `<analysis>_text`, shows the
   views and marks later steps stale.

Smaller steps keep the same order in plain functions (e.g.
`fit_timelag_model` → `timelag_results_html` → `TimeLagController` in
Step 19b). Validations call the engine functions directly, which is why the
statistics must not live inside widget callbacks.

### 2.6 Staleness, plots and reproducibility

- **Stale results.** When an upstream step changes, it calls
  `mark_stale(module_ids, "Step N: …")` (Cell 1); the registered banners of
  the listed modules (`ALL_DOWNSTREAM = ['overall', 'subgroup',
  'regression', 'spline', 'pub_bias', 'pet_peese', 'loo', 'cumulative',
  'plots']`) show "re-run this step". A new step registers its banner with
  `register_banner('my_module', banner_widget)`.
- **Reproducibility Mode.** A restore sets `ANALYSIS_CONFIG['is_reproducing']`;
  a step then sets its saved settings and runs. Every step cell calls
  `show_reproducibility_bar()` right after `cometa_full_height()` (the bar
  with the *Leave Reproducibility Mode* button); a new step cell must do the
  same. `project_leave_reproducibility()` switches the mode off.
- **Plot cells** only draw: they read `<analysis>_results` and never refit.
  `results_token(key)` notices when the analysis was re-run after the plot
  (`stale_warning_html`). `plot_recipe_bar` / `build_plot_recipe` save a
  figure's data and settings in a small file, so the figure can be redrawn
  exactly without the analysis. Every plot cell also adds
  `figure_common_controls()` to its settings (panel label, the font of all
  figures, optional manual axis ranges and the lnRR percent-change checkbox),
  shows `figure_common_box(C)`, draws inside `with figure_style(s):`, and calls
  `apply_axis_ranges(ax, s, ...)` (before `percent_change_axis`) and
  `add_panel_label(fig, s, size)`. `preset_dropdown` starts every cell at
  `FIGURE_DEFAULT_PRESET` (full page width). Pass it every size widget of the
  cell: 'title', 'label', 'tick', 'legend' (lists allowed, e.g. group labels
  with 'label', annotations with 'legend'), 'points' for marker areas and
  'markers' for marker sizes in points; otherwise that size stays fixed when
  the figure gets smaller or larger. New settings must keep old recipes drawing
  as before: read them with `s.get(key, old_default)`.
- **Project file** (Cell 1, "PROJECT FILE"). `COMETA_PROJECT` is the open
  project: `datasets` (each data version once: canonical CSV, column types,
  12-hex SHA-256 fingerprint `id`, label `v1`, `v2`, …), `analyses` (name,
  note, `step` = `overall` / `subgroup` / `meaningful`, `data_id`, `settings`,
  key `results`, a readable `summary`), `log` and `revision`.
  `project_settings` takes the settings from `export_config_for_reproducibility`
  (which skips the results listed in `RESULT_KEYS`) and drops later steps'
  settings the analysis does not use (`PROJECT_STEPS[step]['drop']`).
  `project_save_bar(step)` (save tab of Steps 7–24) adds an analysis and downloads a new
  revision (`project_commit`); `project_manager_widget()` (Steps 2 and 27)
  renames, annotates, deletes and restores. `project_restore` puts the data and
  settings in `ANALYSIS_CONFIG` with `is_reproducing = True`; Steps 3–9b then
  restore their widgets from the saved settings and run. A saved value that is
  not available stops the step with a red "Reproducibility Mode stopped"
  message instead of falling back to a default. Running the cells recomputes
  the results; they are never loaded from the file. Old session files open
  through `_project_from_session`. Steps 12–24 keep their own options in
  `analysis['options']` (`project_step_options`, read from the step's results;
  Step 12 stores its selection in `meta_regression_RVE_results['selection']`).
  On restore, `project_restore_options(step)` returns them only for the
  restored step; the cell checks them against its widgets
  (`project_widget_values`), shows `project_restore_note_html` and runs, or
  stops. To save a new kind of analysis: add it to `PROJECT_STEPS`, write its
  `_pr_<step>` key-results function, its text in `_project_later_text` and
  its options in `project_step_options` / `_project_options_text`, put
  `project_save_bar('<step>')` in its tabs and a `restore_and_run` in its
  cell.

### 2.7 Messages and warnings

- An error that stops a step is shown with `cometa_error(message, title=None)`
  (Cell 1): the red box every step uses. Say what to do ("run Step 4 (Data
  Cleaning) first"), not only what went wrong.
- `warnings.warn("…")` is the way to tell the user something about their
  results (e.g. a fallback was used). The router in Cell 1 shows CoMeta's
  own messages once, compactly, and keeps every warning (CoMeta's and the
  libraries') in `COMETA_WARNING_LOG`, viewable in Step 27.
- Floating-point noise from optimisers (trial points outside the valid
  region) is silenced with the `@_quiet_numerics` decorator (Cell 1b);
  convergence and boundary estimates are checked explicitly instead.
- Errors the user can fix are shown as a short HTML message in the cell
  output (what is missing and which step to run), not as a traceback.

---

## 3. Conventions

These keep CoMeta readable and its results trustworthy.

**Statistics**
- Every method follows a published source; cite it in a comment next to the
  code and in the generated Methods text.
- A result that can be compared with R must be validated against R
  (section 4). If CoMeta deliberately differs from R, say so in the code and
  in the generated text.
- Keep the defaults conservative: a new option starts *off* unless it is the
  recommended practice.
- When the method changes, update the generated Methods/Results text and its
  references in the same change. The text must describe what was computed.
- References live in one dictionary, `COMETA_REFERENCES` (Cell 1). Add a new
  reference there (with its DOI, checked against the publisher's record) and
  use it by key; do not write a reference inside a step. Number citations in
  order of first appearance.

**Code**
- Stay inside the notebook. Do not move code into an external package; a
  new helper goes into the cell where it is used, or into Cell 1 / 1b when
  several steps need it.
- Prefer the libraries already loaded (numpy, scipy, pandas, statsmodels,
  matplotlib, ipywidgets). A new dependency needs a good reason.
- Match the surrounding style: comment density, names, and the way each
  step builds its widgets and HTML output.
- Read settings from and write results to `ANALYSIS_CONFIG`; do not rely on
  global variables from other cells. A step that changes its results should
  call `mark_stale(...)` so later steps show the "re-run" banner.
- Messages for the user: `warnings.warn(...)` for something they should
  know (it is shown once, compactly, and kept in the Step 27 warnings log),
  or a clear HTML message in the cell output. Do not print numerical noise:
  wrap optimiser code with `@_quiet_numerics` (Cell 1b) and report
  convergence yourself.
- User-facing text in plain English, without naming other software unless
  the comparison helps the reader.

**Outputs**
- Commit the notebook **without outputs** (Colab: **Edit → Clear all
  outputs** before saving). Outputs make the file very large and the
  changes impossible to review.
- A deliberate executed record (e.g. a full validation run for a release)
  is the exception; say so in the pull request.

---

## 4. Checking your change

The validation suite (the 🧪 cells after Step 27) is the verification
system for developers. It runs **on your own analysis**: the data, the
sampling VCV (including shared controls), the settings and the results of
the steps you ran in this session. See *Validation suite* in the
[README](README.md#8-validation-suite-for-developers).

1. Run your analysis (Steps 2–27, or the steps you changed).
2. Run **Validation: Imports & R Setup**. For a statistical change, tick
   *Also run the fixed reference datasets*: they reach code paths your data
   may not (singletons, unbalanced clusters, missing years, shared controls).
   The R packages are installed from a dated snapshot so everyone compares
   against the same versions.
3. Run the validations that cover your change, plus **Validation 11 (unit
   tests)**, which runs on every change.
4. Run **Validation Summary & Export** and keep
   `cometa_validation_results.json` for the pull request.

Each validation reports *PASS*, *FAIL*, *not run* (the step it checks was not
run) or *skipped* (it uses only reference datasets and they are off). A
change is ready when nothing that passed before fails now. If a tolerance
has to be loosened, explain why in the pull request.

**Excel reports.** The numbers of a report come from the step's Detailed
Statistics rows: pass `key='<step id>'` to `statistics_table_text` when the
tab is rendered, and `statistics_sheet(writer, '<step id>')` writes them as
the first sheet. Do not build a second table of results for the file.

**Unit tests.** Validation 11 collects every `test_...` function in its cell
with pytest. Add a test for each bug you fix (one that fails before your fix
and passes after) and for each new function. Tests should be small, fast and
use made-up data or published values (e.g. a number taken from R, with the
R call in the docstring).

---

## 5. Adding a new method or a new validation

**A new analysis step**
1. Open an issue describing the method and its reference.
2. Add a cell where it belongs in the workflow, with a `#@title` header in
   the style of the others and the setup check used at the top of every cell.
3. Read the data from `ANALYSIS_CONFIG['analysis_data']` and
   `ANALYSIS_CONFIG['vcv_matrices']`, and the inference settings from
   `global_settings`, so the step agrees with the overall model.
4. Store its results under a new key (e.g. `ANALYSIS_CONFIG['mymethod_results']`)
   and, if they are results rather than settings, add the key to
   `RESULT_KEYS` in `export_config_for_reproducibility` (Cell 1) so the
   project file stays small.
5. Generate Methods/Results text with references, as the other steps do.
6. Add unit tests and, when R can compute the same thing, a validation.
7. Document the step in the README manual.

**A new validation**
1. Copy the closest existing validation cell (e.g. Validation 26) and keep
   its structure: header comment saying what is compared with which R
   function, tolerances in a dictionary at the top.
2. Get the data with `validation_sources(reference=...)`: your analysis
   first, plus fixed reference datasets when the switch is on.
   `validation_user_data()` gives the effect sizes, the VCV and the Step 7
   settings; `validation_block_V()` builds the block-diagonal V for R.
3. If a required step was not run, raise `ValidationPrerequisiteError`
   (recorded as *not run*). A validation that uses only fixed datasets
   starts with `if reference_only_validation(n, title):`.
4. Record the outcome with `record_validation(n, title, checks, notes=...)`,
   where `checks` is a list of `(check, 'PASS'/'FAIL'/'INFO')`.
5. Increase `N_VALIDATIONS` in **Validation Summary & Export** and list the
   new validation in the README.

---

Questions about contributing: open an
[issue](https://github.com/ErickJLA/CoMeta/issues).
