# CoMeta: working guide for Claude

Written by Claude for a future Claude session, at the end of a long working
session (state as of **release 1.0.0**, October 2026; last change: the
start-of-notebook cleanup after commit `5a18b93`). The repository owner
(the user) keeps this file outside the repo and attaches it when they need
help. **Read it first, then verify against the code**: the notebook changes,
and anything here can be stale. Run `git log --oneline` and compare with the
history in section 10 to see what changed since.

---

## 0. Start-of-session checklist

1. Read this file. Then `git log --oneline | head -20` and `git status`.
2. Rebuild the test harness (section 9). It lives only in the scratchpad, so it
   is gone in a new session. Recreate the scripts from section 9 verbatim.
3. Install R packages if validations are needed (section 9.1); that takes a
   few minutes, so start it in the background early.
4. Dump the cells to files (`mine/c{i}.py`) so `grep`/`sed` work on them.
5. Before editing a cell, read the relevant part: line numbers in this file
   are approximate, but function names are stable.

---

## 1. The project and the user

- **CoMeta** is a single Google Colab notebook, `CoMeta.ipynb`, for multilevel
  (three-level) meta-analysis aimed at ecologists. It is being prepared for
  *Methods in Ecology and Evolution* (Applications paper).
- **The "glass box" design is deliberate**: all code stays visible in the
  notebook cells. Do **not** propose moving it into a library or package; the
  user decided this.
- **Validation suite** (cells 32–60): every validation runs on the user's own
  analysis in the session and compares it with R (metafor, clubSandwich,
  MetaUtility). Reference datasets are optional (a checkbox).
- **Independence from metafor**: text the user reads (Methods/Results text,
  dashboards, help notes) must describe methods by their published sources,
  not as "like metafor". Developer comments and validation cells may mention
  R packages. "Checked against R" stays as a strength in the README.
- **The user**:
  - is a researcher, not a statistician;
  - writes informally, sometimes in Spanish-influenced English;
  - is very appreciative, and gives broad requests ("help me with the spline")
    while trusting your design decisions;
  - wants results that are easy to understand for non-experts (a "tool to
    learn", not just "metafor for Python");
  - uses CoMeta mostly on PCs; phone layouts are not a concern.
- **Release 1.0.0 is prepared** (section 2b) on the development branch. The
  user chose to keep it off `main` for now and will merge it themselves.
  The steps still theirs: author names, a Colab run, the merge, Zenodo and
  the DOI.
- **The user maintains the tested package versions** (`REQUIRED_PACKAGES`,
  top of Cell 1) themselves, updating them periodically. Do not change them
  unless asked. Differences from the tested set are not shown in Cell 1; they
  go to the Step 27 log (section 2b).

### Working conventions with this user

- **Git**:
  - Develop on the branch the session names (e.g. `claude/<name>`).
  - Commit and push after each finished piece; a stop hook complains about
    uncommitted changes.
  - Never open a PR unless asked.
  - Commit messages end with the attribution lines the system gives
    (Co-Authored-By plus Claude-Session).
  - No model names in commits or files.
- **Pace**: the user often says "you can do it at the pace you prefer". Do
  related items in one go, validate, commit, then report.
- **Report shape** (what worked well):
  - a short opening (what's done, pushed, validations pass);
  - then per item: what changed and why, with one concrete number from the
    test data;
  - then what remains;
  - attach screenshots of new dashboards (SendUserFile, `display: render`).
- **When asked "how useful / how hard"**, give an honest assessment with a
  recommendation. The user then decides.
- **Ask only real decisions** (two valid designs with trade-offs). Otherwise
  pick the sensible option and say so.

---

## 2. Notebook map (61 cells)

| Cell | Title / step | Key functions, classes | Saves to `ANALYSIS_CONFIG` |
|---|---|---|---|
| 0 | markdown header, Colab badge | | |
| 1 | ⚙️ 1. Environment Setup & Core Functions (~3160 lines) | GPL notice; release constants `COMETA_VERSION` … (section 2b), `check_and_lockdown`/`package_check_rows`, header banner; CR2 core `_compute_robust_var_betas`, `_run_three_level_reml_regression_v2`, spline engine `_run_robust_spline_analysis`, `spline_prediction_band`, `spline_adjustment_design`, Excel export `export_analysis_report`, `_get_protocol_metadata`, widget helpers, plot-recipe system, **dashboard and Detailed-Statistics helpers**, `effect_derived_columns`, `es_null_value`, `ci_pct_label`, `COMETA_CITATION` | |
| 2 | ⚙️ 1b. Statistical Engine: Multilevel Models, Tests & Checks (~1750; renamed from "Unified Model Engine") | `FitSpec`, `build_fit_spec`, `fit_mv`, `fit_blocks`, `fit_estimates`, `fit_cr2`, `compare_fits`, `pseudo_r2`, `pseudo_r2_report`, `profile_ci`, `tau2_univariate`, `var_components_vcov`, `select_rows`/`RowAccounting`, `attach_vcv_row_pos`, `cluster_vcv`, `slice_vcv_block`, meaningful-effects engine (`MeaningfulModel`, `meaningful_proportions`, `bca_interval`); ends with `cometa_engine_selftest()` (BCG trials, REML: τ² 0.3132433, μ −0.7145323, SE 0.1797815 from metafor, tol 1e-4; plus CR2 computable) → `COMETA_ENGINE_SELFTEST`, sets `COMETA_SETUP_DONE`, shows a green/red status line | |
| 3 | ⚙️ 2. Data Ingestion | upload, column mapping, `CURTIS_DATA` built-in example, opt-in control-group column (`_build_control_mapping_widget`) | `shared_control_column` |
| 4 | ⚙️ 3. Global Filtering | | `complete_case_moderators` |
| 5 | ⚙️ 4. Data Cleaning | `run_processing`, `detect_shared_controls`, `user_control_column` | `removed_records`, counts |
| 6 | 🔬 5. Effect Size Selection | effect-size type, bias correction option | `effect_size_type`, `es_config`, `effect_col`, `var_col`, `se_col`, `bias_correction`, `data_type` |
| 7 | 🧮 6. Effect Size Calculation | `run_calculation`, `build_vcv_matrices` (Gleser–Olkin / Lajeunesse covariances), `_expand_to_shared_controls`, SD imputation | `analysis_data`, `vcv_matrices`, `cc_shared_group_rows`, `sd_missing_strategy` … |
| 8 | 📊 7. Overall Meta-Analysis (~3400) | `TwoLevelEngine.calculate_pooled_effect` (GLS with full V), `ThreeLevelEngine`, `OverallEngine`, `OverallController` (`model_selector`, `ci_dist_widget`, `use_kh_widget`, …), `overall_dashboard_html`, `overall_statistics_rows`, `_dash_small_k_html`, `_n_shared_cov_studies` | `global_settings`, `overall_results` (`['reported']` = the model shown), `overall_text` |
| 9 | ⚙️ 8. Subgroup Configuration | `save_configuration`, widgets `moderator1_widget` … | `subgroup_config` |
| 10 | 🔬 9. Subgroup Execution (~4400) | engine, `_pairwise_contrasts` (Holm), `subgroup_dashboard_html`, `subgroup_statistics_rows`; tabs include the Processing Log (the user wants it kept) | `subgroup_results`, `subgroup_text` |
| 11 | 📏 9b. Proportion of Meaningful Effects | `_meaningful_effects_cell()`, `meaningful_dashboard_html`, `meaningful_statistics_rows` | `meaningful_config`, `meaningful_results` (`table`, `settings`, `info`), `meaningful_text` |
| 12–13 | 10/11 Subgroup forest / orchard plots | plot recipes | |
| 14 | 📈 12. Meta-Regression (~3800) | `RegressionEngine`, `predict_from_fit` (t/z follows Step 7), `default_prediction_grid`, `regression_dashboard_html`, `regression_statistics_rows`, `_regression_controller.run_analysis(moderator_cols, categorical_cols, reference_levels)` | `meta_regression_RVE_results`, `regression_text`; `LAST_REGRESSION_RESULT` global |
| 15 | 📈 13. Meta-Regression plot | | |
| 16 | 📈📈 14. Spline | `SplineMetaRegressionModel` (`run_analysis(mod, df_spline, adjust)`, `_compare_linear_spline`, `_variance_r2_linear`, `get_adjust_candidates`), `spline_dashboard_html`, `spline_statistics_rows`, `_spline_adjust_text`; `_spline_model`, `_spline_view`, `_spline_controller` | `spline_model_results`, `spline_text` |
| 17 | 📈📈 15. Spline plot | `_spline_plot_cell()` | |
| 18 | 🌳 16. Meta-Forest | `ClusterBootstrapForest`, `MetaForestModel`, `metaforest_dashboard_html`, `metaforest_statistics_rows`; `_mf_view.feature_checkboxes`, `_mf_view.run_button` | `meta_forest_results` |
| 19 | 📉 17. Egger & trim-and-fill | `egger_trimfill_statistics_rows` | `funnel_results`, `trimfill_results` |
| 20 | 📉 18. Trim-and-fill plot | | |
| 21 | 📉 19. PET-PEESE | `pet_peese_statistics_rows`; precision term `PETPEESE_ESS_TYPES`, `PETPEESE_PRECISION_LABELS`, `petpeese_precision_terms` (predictors `PET_x`, `PEESE_x` from `prepare_data(precision=)`); `_petpeese_controller.precision_widget` ('ess' default for hedges_g/cohen_d/lnRR/lnCVR with ne, nc — same rule as Step 19b); `run_analysis(p_threshold, precision=)`. Framed as a *sensitivity analysis* (Nakagawa et al. 2022). V19 checks SE and √(1/ñ). | `pet_peese_results` (`precision`, `n_no_precision`), `pet_peese_text` |
| 22 | 📉 19b. Time-lag test | `TimeLagModel`, `timelag_statistics_rows` | `timelag_results` |
| 23 | 📉 19c. Publication-bias Overview | `pubbias_inputs`, `pubbias_overview_html`, `pubbias_overview_rows` (reads 17/19/19b results, refits nothing) | |
| 24 | 📉 20. Funnel plot | contour shades `gray_dark`/`gray`/`blue`; `LEGACY_SHADES` maps old `metafor` key | |
| 25 | 📉 21. Leave-one-out | `_run_three_level_reml_for_subgroup` (any intercept-only refit), `LOOEngine`, `LOO_INFLUENCE_THRESHOLD = 20.0`, `loo_dashboard_html`, `loo_statistics_rows`; `_loo_controller.run_analysis()` | `loo_results` (`data` = per-refit DataFrame, `original`, `threshold`, `alpha`, `null`) |
| 26 | 📉 22. Leave-one-out plot | | |
| 27 | 📊 23. Baujat plot | needs `loo_results` | |
| 28 | 📈 24. Cumulative MA | `CumulativeEngine` (multilevel / study / obs), `cumulative_dashboard_html`, `cumulative_statistics_rows`; `_cumulative_controller` (`agg_method_widget`, `sort_order_widget`, `run_analysis()`) | `cumulative_results` (steps DataFrame), `cumulative_metadata`, `cumulative_text` |
| 29 | 🗺️ 25. Map | | |
| 30 | 📊 26. Cumulative trends plot | | |
| 31 | 💾 27. Export Session | session file; log = `_package_versions_html()` (package differences) + warnings summary | |
| 32 | 🧪 Validation: Imports & R Setup | `R_SNAPSHOT_DATE = "2026-10-01"` (Posit snapshot), `record_validation`, `VALIDATION_RESULTS`, `ValidationPrerequisiteError`, `validation_prerequisite_missing`, `validation_user_data`, `validation_sources`, `validation_block_V`, `record_validation_skipped`, `reference_only_validation`, `VALIDATION_INCLUDE_REFERENCE` | |
| 33–59 | Validations 1–27 | V(n) is cell 32+n. V2 (cell 34) and V27 (cell 59) are button-driven Monte Carlo runs. V11 (cell 43) is the pytest unit tests (77). V22 (cell 54) needs the Baujat cell (27) run first. | |
| 60 | Validation Summary & Export | `N_VALIDATIONS = 27` | |

**Validation 27 (meaningful effects, Monte Carlo).** `_v27_preset`
(Quick 100 reps / 15 bootstrap reps × 200; Standard 500 / 60 × 500;
Publication 1000 / 300 × 1000), `_v27_scen`, `_v27_btn`; result in
`v27_results`. Five scenarios: normal 30 studies, normal 15 studies (INFO),
skewed χ²(3) (parametric share INFO: it assumes normal true effects),
shared controls ρ = 0.5, study-level share. Criteria: |bias| ≤ 0.03 + 2 MC SE;
coverage ≥ 0.90 − 2 MC SE. The delta-method CI is graded only for true shares in
0.15–0.85 (known to undercover outside; Step 9b already points to the bootstrap
CI there). Prototype findings (300 reps): calibrated bias ≤ 0.03 even when
skewed, parametric ~+0.05 when skewed; bootstrap coverage 0.87–0.98; delta
coverage 0.82 for a true share of 0.067. Do not tighten or loosen the criteria
to make a scenario pass; report it.

Effect-size types: `lnRR`, `hedges_g`, `cohen_d`, `MD`, `lnCVR`, `log_or`,
`log_rr`, `risk_diff`, `proportion` (logit), plus pre-calculated data
(`data_type == 'pre_calculated'`). `es_config` holds `effect_col`, `var_col`,
`effect_label`, `effect_label_short`, `type`, `null_value`, `has_fold_change`, …

Other files in the repo:
- `README.md`: the user manual, with a section per step, a "Validation suite
  (for developers)" section and section 9 "Citation, license and contact".
  **Update it with every user-visible change.**
- `CONTRIBUTING.md`: the developer guide, with a cell map, the license of
  contributions and the versioning rule.
- `LICENSE`: GNU GPL v3, the official text from gnu.org (674 lines).
- `CITATION.cff`: CFF 1.2.0, valid against the official schema. Authors are
  placeholders for Erick, Karla and Hugo; the `doi:` line is commented out.
- `CHANGELOG.md`: 1.0.0, including "changes that affect results compared
  with pre-release versions". Add an entry for every release.

---

## 2b. Release 1.0.0: what exists and how to change a version

**One place for release metadata**, at the top of Cell 1 (after the
environment detection):

```python
COMETA_VERSION = "1.0.0"
COMETA_LICENSE = "GPL-3.0-or-later"
COMETA_REPOSITORY = "https://github.com/ErickJLA/CoMeta"
COMETA_DOI = None      # Zenodo DOI once archived
```

These constants feed:
- **`COMETA_AUTHORS` and `COMETA_CITATION`** (Cell 1, near `_alpha`). The
  citation is a software citation: authors (2026), title, (Version x)
  [Software], then the DOI or the repository URL. It appears in every
  generated reference list.
- **The header banner**, printed by Cell 1. It shows the logo, title and
  version badge, the tagline, a description paragraph, a "How to cite" row
  (citation, version, license, repository link) and the green "Environment
  verified" bar. The user asked to remove the yellow "Instruction: execute
  cells sequentially… reproduces the associated manuscript" box; don't add it
  back.
- **The session file** (`_reproducibility.co_met_version`; the key name is
  kept for old files) and `_reproducibility.package_check`.
- **The Excel protocol sheet** (System → CoMeta version).
- **The validation export** (`cometa_version`).

**Status lines (user request)**:
- Cell 1's banner ends with `_cell1_status_html()`: green "Environment ready",
  or amber "Environment incomplete" when packages are missing outside Colab.
  It also shows "Core functions loaded", installed/missing packages, the
  number of versions that differ (pointing to the Step 27 log) and "Next:
  Cell 1b".
- The old static "Environment Verified / Core engine initialised" text was
  inaccurate and is gone.
- Cell 1b ends with the self-test status ("Statistical engine ready" with the
  reproduced BCG values, or red "self-test FAILED"). Keep these honest: they
  must reflect real checks.

**Package check**:
- `COMETA_ENV_CHECK = check_and_lockdown()` near the top of Cell 1.
- `package_check_rows()` at the end of Cell 1 returns
  `(package, installed, tested, note)` rows.
- Cell 1 **no longer displays** the "package versions differ" notice (the
  user asked for this). The list is shown in **Step 27's log**
  (`_package_versions_html()`, above the warnings summary) and recorded in
  the session file.
- Outside Colab, missing packages are still printed by `check_and_lockdown`,
  because the user must act on them.

**GPL notice**: the top of Cell 1 carries the standard GPL "or any later
version" notice, with a copyright line using the author placeholders.

**First (markdown) cell**: the Colab badge (points to
`blob/main/CoMeta.ipynb`), then one line: "CoMeta 1.0.0 · GPL · How to cite ·
Changelog" with links to `main`.

**To release a new version**:
1. Set `COMETA_VERSION` in Cell 1.
2. Change the version in the first markdown cell and in `CITATION.cff`
   (`version:`); the README section 9 text also mentions the version.
3. Add a CHANGELOG entry. Semantic versioning: MAJOR when results change or
   saved sessions break, MINOR for features, PATCH for fixes.
4. Run the full validation suite and V10, V13 and V22 separately
   (section 9.6).

**Remaining release steps (the user's)**:
1. Real names, affiliations and ORCIDs in three places: `CITATION.cff`,
   `COMETA_AUTHORS` in Cell 1, and the copyright line at the top of Cell 1.
2. A Colab run, keeping `cometa_validation_results.json`.
3. Merge the branch to `main` (the user does it; don't open a PR unless asked).
4. Enable the Zenodo–GitHub integration **before** creating the release.
5. Create the GitHub release `v1.0.0`.
6. Put the DOI in `COMETA_DOI` and uncomment `doi:` in `CITATION.cff`.

If the user wants "GPL-3.0-only" instead of "or-later", change it in three
places: `COMETA_LICENSE`, the `CITATION.cff` license line, and the "(at your
option) any later version" wording of the Cell 1 notice. Also update the
README, CONTRIBUTING and CHANGELOG wording.

---

## 3. Statistical conventions (do not break these)

- **Default model: three-level REML.** Effect sizes are nested in studies,
  with the full sampling V (block-diagonal; shared-control covariances).
  - The two-level model is a sensitivity option.
  - τ² estimators for the two-level model: REML, DL, ML, PM, SJ.
- **Two-level model with shared controls**: τ² comes from the chosen estimator
  (diagonal variances). μ is GLS with W_i = (V_i + τ²I)⁻¹, using the same
  weights as its CR2 working model. R equivalent:
  `rma.mv(yi, V, random=~1|es, sigma2=tau2)`. This is checked in V21, and
  mirrored in 9b and V25.
- **Inference: CR2 cluster-robust SE, Satterthwaite df, t distribution**
  (clubSandwich). Settings:
  - "CR2/Knapp-Hartung" off gives model-based SE with df = studies − 1.
  - t/z is a Step 7 setting (`global_settings['dist_type']`: `'t'` or
    `'norm'`). Prediction intervals and meta-regression predictions follow it.
- **Multi-coefficient tests**: HTZ/AHZ Wald test (Tipton & Pustejovsky 2015)
  via the `htz_wald` closure (`htz_fn(C, test='AHZ')`).
- **Pairwise subgroup contrasts**: CR2, contrast-specific AHZ df, Holm adjustment.
- **Variance components**: profile-likelihood CIs (`profile_ci`).
  - R's `confint` can return NA or imprecise bounds when a component sits at 0.
  - Validations compare with `tol=1e-10`, with looser fallbacks, and skip
    R-NA bounds.
- **Likelihood-ratio tests between different fixed effects**: refit by **ML**
  (REML likelihoods are not comparable). Variance components on the boundary
  use a χ̄² 50:50 mixture.
- **Pseudo-R²** = (Σσ²_null − Σσ²_model)/Σσ²_null with the same rows, V and
  random structure. Truncated at 0 overall and per level.
- **Prediction interval** = μ ± crit·√(SE_model² + τ² [+ σ²]), with
  crit = t(studies − 1) or z.
- **Multilevel I²** uses the Higgins–Thompson typical sampling variance.
- **Continuity correction (binary data)**:
  - 0.5 is added to all four cells of a table with a zero cell.
  - It is also added to every table sharing a control group with such a
    table (`_expand_to_shared_controls`), so shared control counts stay
    identical.
  - Double-zero tables are dropped for log OR and log RR, and kept for RD.
- **Rows used**: `select_rows` returns the rows plus `RowAccounting` (every
  dropped row with a reason). Each row carries `_vcv_row_pos`, so V blocks can
  be **sliced by row identity** (`cluster_vcv`) when some of a study's rows
  are dropped.
- **Moderator candidates** must exclude effect-size transforms:
  `effect_derived_columns(df)` (Cell 1). It catches derived names and any
  numeric column with |Spearman ρ| ≥ 0.999 to the effect. Used in Steps 8, 12,
  14 and 16. Bug history: `fold_change` once leaked into the meta-forest
  (out-of-bag R² 0.95).
- **Spline (Step 14)**:
  - Basis: patsy `cr(x, df=k, constraints='center')`.
  - `n_basis` = 1 + k (intercept + spline columns).
  - Adjustment columns come after the basis (`spline_adjustment_design`):
    continuous moderators centred, categorical ones as indicators against a
    reference.
  - The omnibus test covers columns `1:n_basis` only.
  - The curve has adjustment columns at 0; `y_partial` gives the points.
  - Linear-vs-spline LRT: ML, with adjustments in both models,
    df = n_basis − 2.
  - `X_design` stores the exact design matrix.
- **Meaningful effects (9b)**: Mathur & VanderWeele (2019, 2020).
  - Two estimates: parametric and calibrated.
  - CIs: delta method, or cluster bootstrap with BCa (fewer than 500
    resamples gives bias-corrected percentile intervals, marked exploratory).

---

## 4. UI patterns (follow them for anything new)

### 4.1 Result dashboard (the "Results" tab)

- A pure function `xxx_dashboard_html(...) -> str`, built from the **saved
  results** in `ANALYSIS_CONFIG`, so other cells (e.g. the 19c overview) can
  reuse it.
- **Save the results before rendering.**
- The style constants and helpers live in Cell 1, under "RESULT DASHBOARDS
  AND DETAILED-STATISTICS TABLES": `_DASH_CARD`, `_DASH_CTITLE`, `_DASH_CDESC`,
  `_DASH_BOX`, `_DASH_LABEL`, `_DASH_VAL`, `_DASH_SUB`, `_DASH_BADGE`,
  `_DASH_FUNNEL_HEAD`, `_DASH_TRACK`, plus `e_()` (HTML escape),
  `_dash_fmt(x, span)`, `_dash_p(p)`, `_dash_num`, `_dash_ticks(lo, hi)`,
  `_dash_pct`, and `_DASH_ORIGINAL_SCALE` (back-transforms per effect type).
- **Layout**:
  - an outer wrapper div (max-width ~1100px) with a title and a subtitle
    (model · inference · CI level);
  - a verdict badge on the right;
  - warning boxes (amber or red) for exploratory runs, few studies
    (`_dash_small_k_html(K)`), low df, fallbacks, excluded rows;
  - a blue **"In plain words"** box: a narrative with the key numbers, what
    they mean, and caveats;
  - numbered cards in a CSS grid (`repeat(auto-fit, minmax(420px, 1fr))`); the
    first card is often full-width (`grid-column: 1 / -1`).
- **Plots inside dashboards** are inline SVG (viewBox about 1000×300).
  - Use bands for CIs, hover `<title>` for exact numbers, and a red line for
    the null value.
  - Clip extreme intervals with a note rather than letting them squash the
    plot. For example, the leave-one-out plot drops the null line when it is
    far from the data; the cumulative plot sets the axis from steps with ≥ 4
    studies.
- Colours in use: green `#15803d`/`#10b981` for significant/good, slate
  `#475569`, purple `#7c3aed` for heterogeneity, amber `#92400e`/`#fffbeb`,
  red `#991b1b`/`#ef4444`.

### 4.2 Detailed Statistics tab ("🔢 Detailed Statistics", "numbers for nerds")

- `xxx_statistics_rows(cfg) -> List[(section, quantity, value, note)]`.
- Always format numbers with `_st_num(x, sig=6)`, `_st_p`, `_st_peq` ("= 0.0123"
  or "< 1e-16"), `_st_ci(lo, hi)`, never with f"{x:.3f}": they follow the user
  setting `DETAILED_STATS_DIGITS` (Cell 1; None = defaults, an int 1-17 overrides
  every `sig`, e.g. 12 to compare with R). `statistics_table_html` states the
  digits shown under the intro. Only descriptive numbers (counts, run time,
  percent shares) use fixed formats.
- Render it as:
  ```python
  text = statistics_table_text(rows, "CoMeta: <analysis>, detailed statistics", "<intro: scale, what>")
  display(HTML(statistics_table_html(rows, text, "Detailed statistics", "<intro html>")))
  ```
  This gives an HTML table plus a Markdown copy with a Copy button, suitable
  for pasting into an LLM.
- Typical sections: Settings / Data / Model / Inference / Coefficients /
  Tests / Heterogeneity / per-item rows / Methods (formulas) / Software.
- **Tab order**: 📊 Results, 🔢 Detailed Statistics, then the step's own tabs
  (Plot, 📝 Publication Text, 💾 Export, Processing Log …).

### 4.3 Publication text

- Methods and Results as HTML with numbered references (`[n]`) built from a
  `db` dict plus an `active_refs` list. **Append a reference before using its
  number.**
- Cite published sources, never software, as the description of a method.
- A non-significant test reads "no evidence of …", never "the data show no …".
- Check every reference with the Scite MCP tool before adding it (never
  invent one). Already verified: Barendregt et al. 2013 (logit proportion),
  Gleser & Olkin 2009 (shared controls), Pedregosa et al. 2011 (sklearn),
  Peters et al. 2008 (contour funnel), Mathur & VanderWeele 2019/2020,
  Wang & Lee 2019, Tipton & Pustejovsky 2015, Pustejovsky & Tipton 2018,
  Lajeunesse 2015, Sweeting et al. 2004.

### 4.4 Other cross-cutting helpers (Cell 1)

- `widget_values(C)` / `apply_widget_values(C, values)` (skips invalid values
  and returns the skipped names).
- Plot recipes: `build_plot_recipe`, `plot_recipe_bar(plot_type, get_recipe, on_load, filename_fn)`.
  Recipes are JSON; **when you rename an option value, map old values in
  `on_load`.**
- Staleness: `results_token(key)`, `stale_warning_html(step)`,
  `register_banner(module_id, widget)`.
- `make_json_safe`, `ci_pct_label(alpha)`, `_alpha()`, `es_null_value()`,
  `is_text_dtype`, `cometa_save_figure`, `show_figure`, `caption_html`.

---

## 5. Validation suite

- Each validation calls `record_validation(n, title, checks_df_or_list, notes=...)`.
- Check statuses: PASS, FAIL, INFO (shown but not counted).
- A crash counts as FAIL. A missing prerequisite raises
  `ValidationPrerequisiteError` and shows as "not run". A reference-only
  validation with the checkbox off is SKIP.
- Use `validation_user_data()` for the user's rows and settings, and
  `validation_block_V(df, vcv, var_col)` for R's V with exactly those rows.
  **Never** build V from whole cached blocks: rows can be dropped.
- The R side runs through `rpy2`: `ro.globalenv[...] = ...` then `ro.r("""...""")`.
- Tolerances are relative where values scale (`TOL_*` dicts per cell).
- **When a feature changes the math, update its validation's R reference in
  the same commit**, e.g. V21 for the two-level GLS, V25 for 9b, V20 and V24
  for the continuity correction, V14 for t/z, V10 for the adjusted spline.
  Prefer an exact R counterpart over an INFO row.
- **Expected baseline for the full suite on the fixture** (section 9.4):
  - 21 validations record results, all PASS (V6 and V8 SKIP when the
    reference checkbox is off).
  - Unit tests: 77 passed.
  - Cell 54 (V22) fails with "Baujat cell not found" because the harness
    doesn't run the Baujat cell; run it separately (section 9.5).
  - V10, V12 and V13 aren't in the full run (spline, meta-forest, two-way
    subgroups); test them separately.
  - Traceback noise from cell 45 (V13: "only for a TWO-WAY subgroup analysis")
    and from pre-running cell 7 (`data_filtered` not defined) is normal.

---

## 6. Gotchas learned the hard way

- **Cell 1 order**: `from typing import ...` comes late in Cell 1 (around line
  2800). Functions defined earlier must not use `Optional[...]` in annotations
  (use string annotations).
- **Editing**: use exact-match patching (`nbpatch.py`). The notebook JSON is
  written with `indent=2, ensure_ascii=False`, no trailing newline. Keep it
  that way so diffs stay small.
- **f-strings in patches**:
  - Watch for unterminated quotes when a patch splits an f-string across
    lines.
  - Run `python3 -c "import ast; ast.parse(open('mine/cN.py').read())"`
    after every patch.
  - Nested quotes inside triple-quoted f-strings are fine.
- **numpy bools**: `x is True` fails for `np.bool_`; wrap in `bool()`.
- **R `confint` on rma.mv**: strict optimiser settings inherited from the fit
  make profile refits fail. Fit a default-control copy for `confint`.
- **Three-level Cook's distance** was a zero placeholder. Don't claim "no
  influential observations" for three-level models.
- **Global name collisions**: all cells share one namespace. Validation 2
  (cell 34) defines its own `PRESETS` (Monte Carlo settings). The figure-size
  presets are therefore `FIGURE_SIZE_PRESETS` (Cell 1, used by
  `preset_dropdown`). Before adding a module-level name, grep all cells for it.
- **Figure presets**: Generic (85/120/175 mm), Elsevier (90/140/190 mm),
  Nature (89/183 mm, fonts 5–7 pt, height ≤ 170 mm), PLOS (≤ 190.5 mm, fonts
  8–12 pt), thesis, slide. These were checked against the publishers' artwork
  pages in October 2026. The user replaced the old Cell Press / STAR Protocols
  presets with these. There is no MEE preset: MEE doesn't publish
  meta-analyses, so its users wouldn't need one.
- **Headless test**: re-running a cell replaces module-level objects and
  closures. Grab widgets via `_all_widgets()` (last match) after the re-run.
- **Pre-running cells without data** prints errors (cell 7 `data_filtered`).
  These are harmless: the fixture sets the data afterwards.
- **Excel export** builds the file in memory and downloads it via JavaScript.
  To inspect it headless, monkeypatch `display` and decode the base64 (see
  9.6).
- **The meta-forest guard** requires ≥ 30 effect sizes.
- **Splines**: knots are quantiles of the *unique* moderator values (patsy).
  Sparse ends make the curve unstable (dashboard warning when fewer than 3
  studies in the outer 10%).
- **pyplot in headless runs**: `matplotlib.use('Agg')` (run_cells does this).
- **Screenshots**: headless Chromium at
  `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (path may change; look
  in `/opt/pw-browsers`).

---

## 7. How to add things

### 7.1 A new analysis step or a new dashboard

1. Put the computation in a model or engine class; save **everything the
   display needs** (including settings, alpha, null value, model labels) to
   `ANALYSIS_CONFIG['<key>']`.
2. Write `<x>_dashboard_html(cfg)` and `<x>_statistics_rows(cfg)` at module
   level in the cell, reading only saved results.
3. Tabs: Results, Detailed Statistics, then the step's own.
4. Add Methods/Results text with verified references.
5. Update the README (the step's section) and, if the cell map changes,
   CONTRIBUTING.md.
6. Test headless with the fixture, screenshot the dashboard, check the
   Markdown of the Detailed Statistics.
7. Add or extend a validation against R (section 7.2).

### 7.2 A new validation

- New cell: `#@title 🧪 Validation N: <what> on your data (Python vs <R pkg>)`,
  with the standard `COMETA_SETUP_DONE` guard at the top.
- Take the data from `validation_user_data()`; raise
  `ValidationPrerequisiteError` when the step wasn't run.
- Check that "stored results = fresh re-run" (this catches stale results),
  then compare with R.
- Wrap the body in `try/except` and call `record_validation`; a crash
  records FAIL unless `validation_prerequisite_missing(e)`.
- Update the Summary cell if it lists validations, and the README.

### 7.3 Fixing a bug

1. Reproduce it on the fixture (or a small synthetic dataset; see `t_cc.py`
   in 9.6 for a binary shared-control example).
2. Fix it.
3. Re-run the matching validation and the full suite.
4. Check generated text and dashboards for claims that the fix changes. The
   leave-one-out text, for example, asserted unchecked things.

---

## 8. Open items and ideas (as of release 1.0.0)

- **Release steps left to the user**: see section 2b.
- **Suggested, not started**:
  1. A combined report: gather every Detailed Statistics tab into one
     Markdown file (Step 27 export). High value for the "tool to learn" goal.
  2. A glossary (τ², σ², I², CR2, Satterthwaite df, PI, …) linked from the
     dashboards and the README.
  3. Navigation markdown cells between groups of steps. The notebook has
     only one markdown cell.
  4. A real end-to-end run in Colab, and committing an executed validation
     record (JSON plus the executed notebook) for MEE.
  5. Further spline options: several spline moderators added together, or a
     spline × factor interaction. They need many studies; option 1
     (adjustment) is done.
  6. Session file: settings for Step 12 onward aren't saved.
  7. Remove dead code and narrow the broad `except Exception` handlers in
     statistical code; add MEE figure-size presets.
- **Known limitations, documented**:
  - The cumulative "study" and "obs" options ignore within-study
    heterogeneity.
  - The trim-and-fill method assumes independence; it is reported as a
    sensitivity analysis.
  - Spline plug-in fallback: if joint REML fails, it uses the *unadjusted*
    linear model's components.

---

## 9. Headless test harness (recreate in the scratchpad)

Working directory: the scratchpad (call it `$SP`). Replace `$SP` in `drive.py`
with the real path.

### 9.1 R packages

R 4.3 is usually installed. Install the packages into a user library (they
take a few minutes; do it in the background):

```bash
mkdir -p ~/Rlib
R_LIBS_USER=~/Rlib Rscript -e 'install.packages(c("metafor","clubSandwich","metadat","MetaUtility"), lib="~/Rlib", repos="https://cloud.r-project.org")'
```

Versions used: metafor 5.2.1, clubSandwich 0.7.0, metadat 1.6.0,
MetaUtility 2.1.2. Python packages used: numpy 2.5, scipy 1.18, pandas 3.0,
patsy 1.0, statsmodels, scikit-learn, rpy2 3.5, ipywidgets, IPython,
matplotlib, seaborn, xlsxwriter (pip-install what's missing). Always run
with `R_LIBS_USER=~/Rlib`.

### 9.2 `nbpatch.py`: exact-once replacements in cells

```python
"""Apply exact-match replacements to code cells of CoMeta.ipynb.
Usage: python3 nbpatch.py patchfile.py
patchfile defines PATCHES = [(cell_index, old, new), ...]; each old must occur
exactly once in that cell's source."""
import json, sys, runpy, os
NB = '/home/user/CoMeta/CoMeta.ipynb'
DUMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nb.py')
patches = runpy.run_path(sys.argv[1])['PATCHES']
nb = json.load(open(NB, encoding='utf-8'))
for ci, old, new in patches:
    src = ''.join(nb['cells'][ci]['source'])
    n = src.count(old)
    if n != 1:
        sys.exit(f"cell {ci}: expected 1 match, found {n} for:\n{old[:200]}")
    src = src.replace(old, new)
    parts = src.split('\n')
    lines = [p + '\n' for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])
    nb['cells'][ci]['source'] = lines
open(NB, 'w', encoding='utf-8').write(json.dumps(nb, indent=2, ensure_ascii=False))
with open(DUMP, 'w') as out:
    for i, c in enumerate(nb['cells']):
        out.write(f'# ===== CELL {i} ({c["cell_type"]}) =====\n' + ''.join(c['source']) + '\n')
print(f"applied {len(patches)} patch(es)")
```

Patch files can compute `old` text by slicing the cell source (e.g. to
replace a whole function between two markers):

```python
import json
src = ''.join(json.load(open('/home/user/CoMeta/CoMeta.ipynb'))['cells'][25]['source'])
a = src.index("class OldThing:"); b = src.index("# ====\n# NEXT SECTION")
PATCHES = [(25, src[a:b], "new code\n")]
```

After patching, re-dump the cells:
```bash
python3 -c "import json; nb=json.load(open('/home/user/CoMeta/CoMeta.ipynb'))
for i,c in enumerate(nb['cells']): open(f'mine/c{i}.py','w').write(''.join(c['source']))"
```

### 9.3 `run_cells.py` and `run_pre.py`

```python
# run_cells.py
"""Execute selected notebook cells headlessly in one namespace (for testing)."""
import json, sys, os, matplotlib
matplotlib.use('Agg')
from IPython.core.interactiveshell import InteractiveShell
sh = InteractiveShell.instance()
nb = json.load(open(os.environ.get('NB','/home/user/CoMeta/CoMeta.ipynb'), encoding='utf-8'))
def run(i):
    r = sh.run_cell(''.join(nb['cells'][i]['source']), silent=True)
    if not r.success:
        print(f"CELL {i} FAILED: {r.error_in_exec or r.error_before_exec}"); return
    print(f"cell {i} ok")
if __name__ == '__main__':
    for a in sys.argv[1].split(','):
        run(int(a))
    if len(sys.argv) > 2:
        r = sh.run_cell(open(sys.argv[2]).read())
        sys.exit(0 if r.success else 1)
```

```python
# run_pre.py   usage: R_LIBS_USER=~/Rlib python3 run_pre.py 1,2,3,5,7,8 script.py
import sys; sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(open(sys.argv[0].replace('run_pre.py','run_cells.py')).read().split("if __name__")[0])
sh.run_cell("ANALYSIS_CONFIG = {}")
for a in sys.argv[1].split(','): run(int(a))
r = sh.run_cell(open(sys.argv[2]).read()); sys.exit(0 if r.success else 1)
```

Run them from the scratchpad directory (the scripts use relative paths).
Pre-run cells `1,2,3,5,7,8` (setup, engine, ingestion with `CURTIS_DATA`,
cleaning, calculation, Step 7); the script then builds the data.

### 9.4 `fixture_user.py`: the Curtis (1998) lnRR analysis

```python
# Run AFTER notebook cells 1,2,3,5,7,8. Curtis CO2 data: raw continuous, lnRR,
# shared-control groups, synthetic per-study year, two missing SDs (imputed).
import numpy as np, pandas as pd
_raw = pd.DataFrame({k: v for k, v in CURTIS_DATA.items()})
_raw = _raw[['id', 'xe', 'sde', 'ne', 'xc', 'sdc', 'nc', 'method', 'fungrp', 'time']].copy()
_raw['id'] = _raw['id'].astype(str)
_rng = np.random.default_rng(2024)
_years = {s: int(_rng.integers(1985, 1998)) for s in pd.unique(_raw['id'])}
_raw['year'] = _raw['id'].map(_years)
_raw.loc[[3, 17], 'sde'] = np.nan
ANALYSIS_CONFIG.clear()
ANALYSIS_CONFIG.update({
    'data_type': 'raw', 'effect_size_type': 'lnRR',
    'es_config': {'effect_col': 'lnRR', 'var_col': 'var_lnRR', 'se_col': 'SE_lnRR',
                  'ci_lower_col': 'CI_lower_lnRR', 'ci_upper_col': 'CI_upper_lnRR',
                  'effect_label': 'log Response Ratio', 'effect_label_short': 'lnRR',
                  'type': 'lnRR', 'has_fold_change': True, 'null_value': 0, 'scale': 'log',
                  'allows_negative': False},
    'sd_missing_strategy': 'nakagawa_missing_cases', 'sd_zero_strategy': 'drop',
    'bias_correction': True,
})
globals()['raw_data_standardized'] = _raw.copy()
_ok, _res = run_processing(_raw)
globals()['data_filtered'] = _res['data_filtered']
run_calculation()
_oc = OverallController(ANALYSIS_CONFIG)   # Step 7, defaults: 3-level, CR2 on, t, 95%
_oc.run_analysis()
assert ANALYSIS_CONFIG.get('overall_results'), "Step 7 did not store results"
_ad = ANALYSIS_CONFIG['analysis_data']; _v = ANALYSIS_CONFIG['vcv_matrices']
print(f"[fixture] {len(_ad)} effect sizes, {_ad['id'].nunique()} studies, "
      f"{sum(1 for m in _v.values() if np.count_nonzero(m - np.diag(np.diag(m))))} VCV blocks with covariances, "
      f"mu = {ANALYSIS_CONFIG['overall_results']['reported']['mu']:.4f}")
```

Expected fixture output: `102 effect sizes, 29 studies, 1 VCV blocks with
covariances, mu = 0.2564`. Moderators: `method` (GC/GH/OTC), `fungrp`, `time`
(continuous), `year` (synthetic). To rerun Step 7 with other settings, change
`_oc.model_selector.value = TWO_LEVEL_CHOICE`, `_oc.ci_dist_widget.value = 'norm'`
and similar, then call `_oc.run_analysis()`.

### 9.5 `mine/drive.py`: drivers for button-driven steps

```python
import os, ipywidgets as _w
_SP = '$SP/mine/'          # <- scratchpad path; cells dumped as c{i}.py
def _cell(n):
    r = get_ipython().run_cell(open(_SP + f'c{n}.py').read(), silent=True)
    assert r.success, f"cell {n} failed: {r.error_in_exec}"
def _all_widgets():
    reg = getattr(_w.Widget, 'widgets', None) or getattr(_w.Widget, '_active_widgets', {})
    return list(reg.values())
def drive_step8(mod1, mod2=None, atype='single', min_papers=3, min_obs=5):
    _cell(9)
    analysis_type_widget.value = atype; moderator1_widget.value = mod1
    if mod2: moderator2_widget.value = mod2
    min_papers_widget.value = min_papers; min_obs_widget.value = min_obs
    save_configuration(None)
def drive_step9():
    _cell(10); assert ANALYSIS_CONFIG.get('subgroup_results')
def drive_step12(mods, cats, refs=None):
    _cell(14)
    _regression_controller.run_analysis(moderator_cols=mods, categorical_cols=cats, reference_levels=refs or {})
def drive_step9b(**vals):
    ANALYSIS_CONFIG['meaningful_config'] = dict({'mode': 'percent', 'q_increase': 10.0, 'q_decrease': 10.0,
        'same': True, 'level': 'effect', 'bootstrap': False, 'n_boot': 50, 'seed': 2024}, **vals)
    _cell(11)
    [b for b in _all_widgets() if isinstance(b, _w.Button) and b.description == '▶ Compute Proportions'][-1].click()
```

Other steps:
- Step 14: `_cell(16); _spline_view.mod_dropdown.value='time'; _spline_view.adjust_select.value=('method',); _spline_view.run_button.click()`.
- Step 16: `_cell(18)`, tick `_mf_view.feature_checkboxes` values, then `_mf_view.run_button.click()`.
- Step 21: `_cell(25); _loo_controller.run_analysis()`.
- Step 24: `_cell(28); _cumulative_controller.agg_method_widget.value='multilevel'; _cumulative_controller.run_analysis()`.
- Step 22 timelag: `_cell(22); m = TimeLagModel().initialize(); m.run(m.default_precision())`.
- Steps 17 and 19: click '▶ Run Publication Bias Analysis' / '▶ Run PET-PEESE'.

### 9.6 Full suite (`t_full.py`) and other recipes

```python
import os, json, time
exec(open('fixture_user.py').read()); exec(open('mine/drive.py').read())
drive_step8('method'); drive_step9(); drive_step12(['time', 'method'], ['method'])
try: drive_step9b()
except Exception as e: print('[9b driver]', e)
nb = json.load(open('/home/user/CoMeta/CoMeta.ipynb'))
cell = lambda i: ''.join(nb['cells'][i]['source'])
get_ipython().run_cell(cell(32))
VALIDATION_INCLUDE_REFERENCE = os.environ.get('REF') == '1'
for i in range(33, 61):
    if i in (34, 59): continue     # V2 and V27 Monte Carlo are button-driven
    t0 = time.time(); r = get_ipython().run_cell(cell(i))
    print(f"[cell {i}] success={r.success} {time.time()-t0:.0f}s", (repr(r.error_in_exec)[:150] if not r.success else ''))
for n, v in sorted(VALIDATION_RESULTS.items()):
    st = 'SKIP' if v.get('skipped') else ('INFO' if v['passed'] is None else ('PASS' if v['passed'] else 'FAIL'))
    print(f"V{n}: {st} {v['n_pass']}/{v['n_checks'] - v['n_info']} (+{v['n_info']} info) {str(v.get('notes') or '')[:140]}")
```

Run it in the background (takes 10–15 min; with `REF=1`, longer):
```bash
REF=1 R_LIBS_USER=~/Rlib python3 run_pre.py 1,2,3,5,7,8,9,10,11,14,16,18,19,21,22,23,25,28 t_full.py > full.log 2>&1
sed 's/\x1b\[[0-9;]*m//g' full.log | grep -E "^V[0-9]+:|passed|failed|success=False"
```

Single validations:
- After a step, `get_ipython().run_cell(cell(32))`, then `run_cell(cell(32+n))`.
- Then read `VALIDATION_RESULTS[n]` (`n_pass`, `n_checks`, `checks`), or the
  cell's local results DataFrame (`res_df` in V21/V25, `_v14_checks` in V14).
- V22: run `_loo_controller.run_analysis()`, then `run_cell(c27)` (Baujat),
  then cells 32 and 54.

Screenshot a dashboard:
```python
open('dash/x.html','w').write("<html><body style='background:#fff;margin:0'>" + loo_dashboard_html() + "</body></html>")
```
```bash
/opt/pw-browsers/chromium-*/chrome-linux/chrome --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=1200,1600 --screenshot=x.png file://$PWD/dash/x.html
```

Excel export, inspected headless: replace `display` with a collector, call
`export_analysis_report(report_type=..., filename_prefix=...)`, then
regex-extract `base64,(...)` from the Javascript and read it with
`pd.read_excel(io.BytesIO(base64.b64decode(b64)), sheet_name=None)`.

Binary shared-control test (continuity correction): build a small DataFrame
with `id, events_e, nonevents_e, events_c, nonevents_c`. Use two rows of one
study with identical control counts, one with a zero cell. Set `data_type`
`'binary'`, `effect_size_type` `'log_or'` and an `es_config` with `log_or`
columns. Then `run_processing(raw)`, set `data_filtered`, `run_calculation()`
and inspect `analysis_data` and `vcv_matrices`. Pre-run cells `1,2,3,5,7`.

---

## 10. Collaboration history (what was done, in order)

Most recent first, all on one long-running branch:

- *(latest)* Full-height outputs:
  - `cometa_full_height()` (Cell 1) calls Colab's
    `google.colab.output.no_vertical_scroll()`;
  - it is placed right after the setup guard of every step cell (cells
    3–31), not the validation cells;
  - it does nothing outside Colab, when `COMETA_FULL_HEIGHT_OUTPUT = False`,
    or if the function is missing;
  - it was tested only with a simulated Colab module. The user still needs to
    confirm it in real Colab.
- Figure size presets made general (Generic, Elsevier, Nature,
  PLOS, thesis, slide) and renamed `FIGURE_SIZE_PRESETS`. This fixes a clash
  with Validation 2's `PRESETS`.
- Cell 1b renamed "Statistical Engine: Multilevel Models, Tests &
  Checks" (the guard messages of every cell and the docs updated). It gets a
  self-test and a status line; Cell 1's status line is now computed.
- *(after 5a18b93)* Start of the notebook cleaned up:
  - the instruction box was removed from the banner;
  - the package-version notice moved from Cell 1 to Step 27's log;
  - package differences are recorded in the session file.
- `5a18b93` Release 1.0.0 preparation:
  - GPL-3.0 LICENSE, `CITATION.cff`, `CHANGELOG.md`;
  - `COMETA_VERSION` and the other release constants;
  - "How to cite" in the banner;
  - Colab link fixed to `CoMeta.ipynb`;
  - "Co-Meta" renamed "CoMeta" (77 places);
  - README section 9 and CONTRIBUTING licensing.
- `c839bbc` Spline: optional adjustment moderators (engine, UI, plot,
  Validation 10 with the exact design, export).
- `85d51b7` Two-level GLS with full V for shared controls (+V21 exact, 9b,
  V25). Continuity correction extended to shared-control groups (V20, V24).
  Meta-regression predictions follow t/z (V14). Funnel shade key renamed.
- `e5ae1c3` Dashboards and Detailed Statistics for Steps 16, 21 and 24;
  `effect_derived_columns` (the `fold_change` leak); leave-one-out text now
  states whether the conclusion changes; meta-forest references fixed.
- `d8a4e1b` Step 9b dashboard and Detailed Statistics.
- `e1b3c41` Publication bias: Detailed Statistics for 17, 19, 19b; new 19c
  overview.
- Earlier:
  - dashboards and Detailed Statistics for Steps 7, 9 (with pairwise
    contrasts and CIs), 12 and 14;
  - profile CIs and pseudo-R² everywhere;
  - text made independent of metafor;
  - CONTRIBUTING.md;
  - opt-in control-group column;
  - the validation suite reworked to run on the user's data;
  - many statistical fixes (SJ and PM estimators, QM, HTZ df,
    complete-case check, cumulative multilevel, PI t/z).

Design decisions the user approved (don't relitigate):
- glass box;
- validations on the user's data, reference datasets optional;
- the three-level model is always the default, chosen a priori (nested
  comparisons are shown for information only);
- trim-and-fill is a sensitivity analysis;
- keep the subgroup Processing Log tab;
- control-group column is opt-in;
- "numbers for nerds" tab named "🔢 Detailed Statistics".
