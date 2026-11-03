# CoMeta: working guide for Claude

Written by Claude for a future Claude session (state as of **November 2026**,
release 1.0.0 plus the work since; last commit described here: `d3b7a64`,
"Tidy-ups: red error boxes everywhere, dead code removed, 9b dashboard
colours", on branch `claude/youthful-pasteur-hm1pmf`, not yet merged to `main`
by the user when this was written). Since November
2026 the user keeps this file **in the repository root** (they asked for it;
an earlier copy had been removed because it was added by mistake). Update it
at the end of a working session when the user asks. **Read it first, then
verify against the code**: the notebook changes, and anything here can be
stale. Run `git log --oneline` and compare with the history in section 10 to
see what changed since.

---

## 0. Start-of-session checklist

1. Read this file. Then `git log --oneline | head -20` and `git status`.
2. Rebuild the test harness (section 9). It lives only in the scratchpad, so it
   is gone in a new session. Recreate the scripts from section 9 verbatim.
   The scratchpad can also become unavailable in the middle of a session;
   then work in a folder outside the repo (e.g. `~/cometa_work`), never in
   the repo. Section 9.7 has a light harness for the plot cells that needs
   only Cells 1 and 1b.
3. Install R packages if validations are needed (section 9.1); that takes a
   few minutes, so start it in the background early.
4. Dump the cells to files (`mine/c{i}.py`) so `grep`/`sed` work on them.
   `nbpatch.py` (9.2) re-dumps them after every patch, and `drive.py` runs
   cells from these dumps, so they must stay current.
5. `pip install` what the sandbox lacks: scipy, pandas, patsy, statsmodels,
   ipywidgets, matplotlib, seaborn, xlsxwriter, scikit-learn, pycountry,
   **tqdm** (Step 21 needs it). `plotly` is usually missing, so the map
   (cell 29) cannot be tested headless.
6. Before editing a cell, read the relevant part: line numbers in this file
   are approximate, but function names are stable.

---

## 1. The project and the user

- **CoMeta** is a single Google Colab notebook, `CoMeta.ipynb`, for multilevel
  (three-level) meta-analysis aimed at ecologists. It is being prepared for
  *Methods in Ecology and Evolution* (Applications paper).
- **The "glass box" design is deliberate**: all code stays visible in the
  notebook cells. Do **not** propose moving it into a library or package; the
  user decided this.
- **Validation suite** (cells 32–61): every validation runs on the user's own
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
- **The user's own paper** uses CoMeta: lnRR, about 970 effect sizes from
  75 studies, a year moderator (meta-regression) and a site moderator whose
  levels have very different variances. Several recent features answer it
  or its reviewers: the subgroup variance check and separate-variance model,
  the wild bootstrap, the Nakagawa et al. (2023) pooled CV, Geary's test,
  percent-change axes, the orchard "own variances" option and the bubble
  plot's editable stats box. The user also asks for help with the paper's
  Methods text and reviewer replies.
- **"If it is risky, don't do it"**: the user prefers a low-risk subset of a
  feature (and answering a reviewer differently) over a risky change. Say
  which parts are low risk, do those, and explain what was left out.
- **Release 1.0.0 is prepared** (section 2b) on the development branch. The
  user chose to keep it off `main` for now and will merge it themselves.
  The steps still theirs: author names, a Colab run, the merge, Zenodo and
  the DOI.
- **The user maintains the tested package versions** (`REQUIRED_PACKAGES`,
  top of Cell 1) themselves, updating them periodically. Do not change them
  unless asked. (scikit-learn and pycountry were added in the pre-submission
  review at the headless-tested versions.) Differences from the tested set are not shown in Cell 1; they
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
- **Review requests** ("is there something to improve?", "do a last pass"):
  look at the code and the output (render the figures, screenshot the
  dashboards), then give a **numbered list** grouped by risk (fixes /
  additions / bigger pieces / "your call" for anything that changes
  defaults), with a recommendation. The user answers with numbers ("1–7 and
  8–12"); do those, then report per number. Don't implement from a review
  request alone.
- **The user tests in Colab** after each piece and reports back ("it works
  great", or a new request). Say clearly what was only tested headless and
  what to check in Colab (widgets, downloads, fonts).
- The user writes in English with Spanish influence; answer in plain English,
  short sentences, no jargon without a gloss.

---

## 2. Notebook map (62 cells)

| Cell | Title / step | Key functions, classes | Saves to `ANALYSIS_CONFIG` |
|---|---|---|---|
| 0 | markdown header, Colab badge | | |
| 1 | ⚙️ 1. Environment Setup & Core Functions (~4900 lines; blocks "SHARED FIGURE OPTIONS" (4.4) and "PROJECT FILE" (4.5) added November 2026) | GPL notice; release constants `COMETA_VERSION` … (section 2b), `check_and_lockdown`/`package_check_rows`, header banner; CR2 core `_compute_robust_var_betas`, `_run_three_level_reml_regression_v2`, spline engine `_run_robust_spline_analysis`, `spline_prediction_band`, `spline_adjustment_design`, Excel export `export_analysis_report`, `_get_protocol_metadata`, widget helpers, plot-recipe system, **dashboard and Detailed-Statistics helpers**, `effect_derived_columns`, `es_null_value`, `ci_pct_label`, `COMETA_CITATION` | |
| 2 | ⚙️ 1b. Statistical Engine: Multilevel Models, Tests & Checks (~1750; renamed from "Unified Model Engine") | `FitSpec`, `build_fit_spec`, `fit_mv`, `fit_blocks`, `fit_estimates`, `fit_cr2`, `compare_fits`, `pseudo_r2`, `pseudo_r2_report`, `profile_ci`, `tau2_univariate`, `var_components_vcov`, `select_rows`/`RowAccounting`, `attach_vcv_row_pos`, `cluster_vcv`, `slice_vcv_block`, meaningful-effects engine (`MeaningfulModel`, `meaningful_proportions`, `bca_interval`); ends with `cometa_engine_selftest()` (BCG trials, REML: τ² 0.3132433, μ −0.7145323, SE 0.1797815 from metafor, tol 1e-4; plus CR2 computable) → `COMETA_ENGINE_SELFTEST`, sets `COMETA_SETUP_DONE`, shows a green/red status line | |
| 3 | ⚙️ 2. Data Ingestion | upload, column mapping, `CURTIS_DATA` built-in example, opt-in control-group column (`_build_control_mapping_widget`); tab 3 "Project" = `project_open_widget()` (Cell 1) | `shared_control_column` |
| 4 | ⚙️ 3. Global Filtering | | `complete_case_moderators` |
| 5 | ⚙️ 4. Data Cleaning | `run_processing`, `detect_shared_controls`, `user_control_column` | `removed_records`, counts |
| 6 | 🔬 5. Effect Size Selection | effect-size type, bias correction option | `effect_size_type`, `es_config`, `effect_col`, `var_col`, `se_col`, `bias_correction`, `data_type` |
| 7 | 🧮 6. Effect Size Calculation | `run_calculation`, `build_vcv_matrices` (Gleser–Olkin / Lajeunesse covariances), `_expand_to_shared_controls`, SD imputation | `analysis_data`, `vcv_matrices`, `cc_shared_group_rows`, `sd_missing_strategy` … |
| 8 | 📊 7. Overall Meta-Analysis (~3400) | `TwoLevelEngine.calculate_pooled_effect` (GLS with full V), `ThreeLevelEngine`, `OverallEngine`, `OverallController` (`model_selector`, `ci_dist_widget`, `use_kh_widget`, …), `overall_dashboard_html`, `overall_statistics_rows`, `_dash_small_k_html`, `_n_shared_cov_studies` | `global_settings`, `overall_results` (`['reported']` = the model shown), `overall_text` |
| 9 | ⚙️ 8. Subgroup Configuration | `save_configuration`, widgets `moderator1_widget` … | `subgroup_config` |
| 10 | 🔬 9. Subgroup Execution (~4700) | engine, `_pairwise_contrasts` (Holm), `subgroup_variance_check` + `variance_check_html`/`_rows`/`_results_text`/`_summary` (⚖️ Variance Check tab), `subgroup_dashboard_html`, `subgroup_statistics_rows`; tabs include the Processing Log (the user wants it kept); the last tab is "💾 Export & Save" (save bar + Excel) | `subgroup_results`, `subgroup_text` |
| 11 | 📏 9b. Proportion of Meaningful Effects | `_meaningful_effects_cell()`, `meaningful_dashboard_html`, `meaningful_statistics_rows`; plot `palette` (Okabe-Ito default), `_ME_COLORS` (dashboard, Okabe-Ito); stale banner 'meaningful'; save bar in its "💾 Export & Save" tab | `meaningful_config`, `meaningful_results` (`table`, `settings`, `info`), `meaningful_text` |
| 12 | 📊 10. Subgroup forest plot | `_forest_plot_cell()`, plot recipes | |
| 13 | 🍎 11. Orchard plot | `_orchard_cell()`: `build_data` (rows of Overall + Step 9 subgroups; `rows_own` from `subgroup_results['variance_check']['separate_model']['levels']`, PI = μ ± t(df)·√(SE² + τ²_g + σ²_g)), `plot_rows(data, s)` (shared/own, Overall shown or not), `default_colors`, `COL` colour pickers, `percent_change_axis`. Settings: `estimates` ('shared'/'own'), `show_overall`, `percent_axis`, `color::<key>` | |
| 14 | 📈 12. Meta-Regression (~3800) | `RegressionEngine`, `predict_from_fit` (t/z follows Step 7), `default_prediction_grid`, `regression_dashboard_html`, `regression_statistics_rows`, `_regression_controller.run_analysis(moderator_cols, categorical_cols, reference_levels)` | `meta_regression_RVE_results`, `regression_text`; `LAST_REGRESSION_RESULT` global |
| 15 | 📈 13. Meta-Regression plot (bubble plot) | `_meta_regression_plot_cell()`: `build_data` (slopes with `ci` and `boot_p` from `meta_regression_RVE_results['cwb']`), `stats_lines(data, s)`, `copy_auto_text`, `palette_colors`/`FIXED_PALETTES` (Okabe-Ito, Paul Tol bright), `refresh_color_box`. Settings: `percent_axis`, `palette`, `color::<col>::<level>`, `stats_style` ('equation'/'slope'), `show_stars`, `stats_text` (custom, replaces the box), `weight_label`, `show_weight_legend` | |
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
| 31 | 💾 27. Project File | `project_manager_widget()`; log = `_package_versions_html()` (package differences) + warnings summary | |
| 32 | 🧪 Validation: Imports & R Setup | `R_SNAPSHOT_DATE = "2026-10-01"` (Posit snapshot), `record_validation`, `VALIDATION_RESULTS`, `ValidationPrerequisiteError`, `validation_prerequisite_missing`, `validation_user_data`, `validation_sources`, `validation_block_V`, `record_validation_skipped`, `reference_only_validation`, `VALIDATION_INCLUDE_REFERENCE` | |
| 33–60 | Validations 1–28 | V(n) is cell 32+n. V2 (cell 34) and V27 (cell 59) are button-driven Monte Carlo runs. V11 (cell 43) is the pytest unit tests (91; the project and figure tests are at the end). V28 (cell 60) is the cluster wild bootstrap. V22 (cell 54) needs the Baujat cell (27) run first. | |
| 61 | Validation Summary & Export | `N_VALIDATIONS = 28` | |

**Analysis steps and the project file** (section 4.5): Steps 7, 9, 9b, 12,
14, 17, 19b and 24 have the save bar at the top of their "💾 Export & Save"
tab (renamed from "💾 Export"); Steps 16, 19 and 21 have a "💾 Save" tab. Each
of Steps 12–24 has a `restore_and_run(opts)` (or inline code at the end of the
cell) and a stale banner. Every plot cell (11, 12, 13, 15, 17, 20, 22, 24, 26,
27, 30) uses the shared figure options of section 4.4.

**Validation 28 (cluster wild bootstrap).** Takes the test lists the
panels use (`subgroup_cwb_tests(ANALYSIS_CONFIG['subgroup_results'])`,
`regression_cwb_tests(LAST_REGRESSION_RESULT)`); each test dict carries
`inputs` (y/X/V blocks, cluster ids, C, fitter, full fit, two_level, and
grp/s2_fixed for the separate-variance model). Every test: CR0 Rademacher
re-estimated vs `cwb_reference` (cell 32) with the same weights
(`V28_N_REP = 8`); first test of each model also CR2, Webb six, fast mode
(`fixed = TRUE` in R), the panel-closure identity, and F*(w) = F*(−w);
wildmeta's `Wald_test_cwb` p as INFO when `WILDMETA_VERSION` is set (cell 32
tries `install.packages("wildmeta")`, optional; this branch has never run,
because the sandbox can't reach CRAN). Reference datasets: simulated
3-subgroup nested data (shared + DIAG), 3-level and aggregated 2-level
regression. Pairwise/coefficient tests capped at `V28_MAX_PER_KIND = 3`.
Jobs run in priority order (`_v28_jobs`: main test default → its other
settings + Python checks → other tests → wildmeta) under `V28_MAX_MINUTES`
(default 30; skipped jobs are INFO); an `RRuntimeError` is INFO, any other
exception FAIL. `cwb_reference` (cell 32): `sparse` when n ≥ 250 (≈50× faster
at 1000 rows, slower below ~250); full fit started from CoMeta's (τ², σ²)
(`init_tau2/init_sigma2`), null and refits from R's full fit; each REML fit
from two starts (near-0 components at 0.05·mean v, then at 1e-6; plus
metafor's default below 250 rows), highest logLik kept — a single warm start
sometimes stalls near the boundary (log-scale optimizer). Only the first
start falls back to nlminb / Nelder-Mead; the extra starts get BFGS only
(on large data the 1e-6 start makes BFGS stop at once, and Nelder-Mead took
2–3 min per fit: that was the user's 2 h + "Error during the optimization"
in Colab). `grp_levels` passes CoMeta's subgroup order (tests carry
`inputs['grp_levels']`); without it R ordered levels by first appearance,
mismatching `s2_fixed` and starts. Timing at ~1000 effect sizes, 75 studies
(stress test, no budget): 53 min, 102/102 PASS; one separate-variance
comparison ≈ 3.5 min, almost all of it R (CoMeta ≈ 3 s). Fixture + reference
datasets: 186/186 in ≈ 15 min.

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
- `CITATION.cff`: CFF 1.2.0, valid against the official schema. Authors:
  Erick J. Lopez-Arredondo, Karla Y. Ledesma Medina, Hugo V. Perales-Vela
  (filled in November 2026); affiliation, ORCID and `doi:` lines are
  commented out until the user adds them.
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
- **The project file**: `cometa_project.cometa_version`, each analysis's
  `cometa_version`, and `software` (`cometa_version`, `python`,
  `package_check`). (Old session files had `_reproducibility.co_met_version`;
  they still open as projects.)
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
  the project file (`software.package_check`).
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
1. Names are done (`CITATION.cff`, `COMETA_AUTHORS` = "Lopez-Arredondo,
   E. J., Ledesma Medina, K. Y., & Perales-Vela, H. V.", copyright line of
   Cell 1). Left: affiliations and ORCIDs in `CITATION.cff`, and the release
   date (`date-released` and the CHANGELOG `[1.0.0]` heading, both still
   2026-10-24). Also recommended before going public: move this guide out of
   the public repository (it describes the user and their paper; the user
   was told and decides), and replace scikit-learn / pycountry in
   `REQUIRED_PACKAGES` with Colab's versions after a Colab run.
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
- `cometa_error(message, title=None)`: the red error box (since the last
  pass of November 2026 no step prints "❌ ERROR" as plain text).
  `load_reproducibility_config` was removed (dead since the project file);
  `export_config_for_reproducibility` stays (project settings and the V11
  test use it). The Step 9b dashboard colours (`_ME_COLORS`, Cell 11) are
  Okabe-Ito like its plot.
- `make_json_safe`, `ci_pct_label(alpha)`, `_alpha()`, `es_null_value()`,
  `is_text_dtype`, `cometa_save_figure`, `show_figure`, `caption_html`.
- **Shared figure options** (Cell 1, block "SHARED FIGURE OPTIONS", just
  before `cometa_save_figure`; November 2026, user request after a figure
  review): `FIGURE_DEFAULT_PRESET` ('Full page width (16.5 cm)', applied by
  `preset_dropdown` at creation). Presets were replaced (user request) by page
  shares: full page width 6.5×4.6 in 11/10/9 pt, two-thirds 4.33×3.4 9/8/7,
  half page 3.15×2.7 8/7/6, full page tall 6.5×8.66, slide 13.33×7.5 22/18/16;
  `fonts_for_width(w)` interpolates these anchors (`_FONT_BY_WIDTH`) for any
  width. `preset_dropdown(targets)`: 'legend' defaults to the tick size; a
  target can be a list; 'points' (marker areas, × width ratio) and 'markers'
  (marker sizes, × √ratio) are scaled relative to the previous width; changing
  the width by hand sets `fonts_for_width` and rescales markers; while
  `apply_widget_values` runs (`_COMETA_APPLYING_SETTINGS`) nothing is
  rescaled, so recipes restore exactly. Orchard: label → label_fs, grp_fs,
  subtitle_fs; legend → annot_fs, footnote_fs; points pt_size; markers
  fruit_size. Points targets also in 15 (bubble_base/range), 17, 20, 22
  (size_scale), 24, 26, 27. Tooltip: `tooltip` (ipywidgets 8) or
  `description_tooltip` (7). `FIGURE_FONT` (kept across Cell 1 re-runs) with
  `FIGURE_FONT_CHOICES` and `figure_font_name` (Arial → Helvetica / Liberation
  Sans / Arimo …; Times → Liberation Serif / Tinos …; else DejaVu Sans),
  `figure_style(s)` (rc_context with the concrete font name, so saving outside
  the context keeps it), `figure_common_controls(limits, percent)` →
  'panel', 'figure_font', '<a>_range_auto/_min/_max', 'percent_axis';
  `figure_common_box(C, limits)`, `apply_axis_ranges(ax, s, axes, C)` (keeps
  inverted axes inverted; with an automatic range it copies the drawn range
  into C's boxes), `add_panel_label`, `link_percent_label`. `pdf.fonttype` /
  `ps.fonttype` = 42. `percent_change_axis` falls back to MaxNLocator ticks
  when fewer than 3 round ones fit. Wired into cells 11, 12, 13 (panel only;
  its own font list now uses figure_font_name and sets FIGURE_FONT), 15, 17,
  20, 22 (time-lag: `self.c`), 24, 26, 27, 30. Per-plot fixes: LOO
  `null_drawn` (null within a quarter of the CI span, or inside a manual
  range) and x ticks 'bottom' only; funnel fills the pseudo-CI region only
  without contours, legend 'outside', label 'p > 0.10'; trim-and-fill legend
  "(centred on …)", legend 'outside'; bubble `plain()` (no e-notation) and
  p (slope) with 3 decimals; spline `pts['w']` + `size_by_weight` (old
  recipes have no 'w' → equal sizes), `_fmt_p` 3 decimals; cumulative
  `legend_loc` ('below' via ScaledTranslation under the x label; old recipes:
  upper left) and `transparent`; 9b `palette` (okabe_ito default; key placed
  before the colour pickers so recipes restore in the right order). Recipes
  saved with the previous version were loaded headless: all 11 draw. Not done
  (the user may ask later): estimate [CI] column and PI in the forest plot,
  a study-level forest plot, a shared house style.
- Percent-change axis for lnRR plots (just before `cometa_save_figure`):
  `es_is_lnrr(es)`, `percent_change(lnrr)` = 100(e^x − 1),
  `fmt_percent_change(p, digits, fixed)`, `percent_change_axis(ax, 'x'|'y')`
  (round values, roundest first, ≤ ~10 ticks, placed at ln(1 + p/100); the
  data stay on the lnRR scale), `PERCENT_CHANGE_LABEL = 'Change (%)'`. Used
  by the orchard, bubble, forest, spline, leave-one-out, cumulative and
  time-lag plots (each stores `percent_ok` / checks `es_type` in its data
  snapshot, so recipes know whether the option applies).
- Plot colour overrides (orchard, bubble plot): a `ColorPicker` per group
  stored in the settings (`color::...`); a value different from the
  scheme/palette colour overrides it, so recipes need no extra flag; untouched
  pickers follow a scheme change (observer compares with the old scheme's
  colours); a ↺ button resets. Don't add a "custom" checkbox: settings are
  restored in dict order and it would be overwritten.

### 4.5 Project file (replaces the session file; November 2026)

Design agreed with the user after a long discussion: no Drive, no text
"code" strings; one JSON **project** that is downloaded again (as a new
revision) on every save. The user tested that repeated downloads are fine
in Colab, and accepts that people may work on an old revision.

- Cell 1, block "PROJECT FILE" (just before the dashboards block):
  `COMETA_PROJECT` (kept when Cell 1 re-runs), `PROJECT_STEPS`
  (`overall`/`subgroup`/`meaningful`: result key, stale-banner id, settings
  to drop, "run to" text), `project_data_entry` (canonical CSV via one
  reload, 12-hex SHA-256 `id`), `project_add_data` (labels v1, v2…),
  `project_settings` (export_config_for_reproducibility minus `_*` keys and
  later steps' settings), `project_check_ready` (no results / stale banner /
  9b older than Step 7 or 9 by timestamp), `project_key_results`,
  `project_results_text`, `project_settings_text`, `project_add_analysis`
  (raises `ProjectNameExists`; `replace=True`), `project_rename`,
  `project_set_note`, `project_delete`, `project_commit` (revision + log,
  drops unused data), `project_payload` (readable keys first, `datasets`
  last), `project_download` (JS data URL; also sets `PROJECT_LAST_FILE`
  for tests), `project_from_bytes` (+ `_project_from_session` for old
  session files), `project_restore` (sets `ANALYSIS_CONFIG`,
  `raw_data_standardized`, `DATA_TYPE_SELECTED`, `VARIANCE_TYPE_SELECTED`,
  `GEO_COLUMNS_MAPPED`; `is_reproducing = True`), widgets
  `project_save_bar(step)`, `project_manager_widget()`,
  `project_open_widget()`; `_PROJECT_LISTENERS` / `_project_notify()`
  redraw every bar and manager on screen.
- The stored data is `raw_data_standardized` (Step 2 output, **before** the
  Step 3 filters), so analyses on different subsets share one data version.
  (The old session file stored `clean_dataframe`, i.e. the filtered rows.)
- Save bars: at the top of the "💾 Export & Save" tab (renamed from "💾 Export"
  at the user's request) of Step 7 and Step 9 (`render_export_tab`, so a new
  bar after every run) and Step 9b (built with the tabs). The "Download
  Settings JSON" buttons are gone.
- Strict restore: Steps 3 (missing filter / common-row-set column), 5 (effect
  size), 7 (`set_silent` collects `not_restored`; the model is not fitted),
  8 (analysis type / moderators) and 9b (`apply_widget_values` skipped names)
  show a red "Reproducibility Mode stopped" box. Step 6 already refused
  unknown SD strategies.
- Tests: V11 `test_project_*` (4; they isolate session globals with
  `monkeypatch.setitem(globals(), …)`). Headless round trip on the fixture:
  save 4 analyses (overall, filtered overall through Steps 3–7, subgroups,
  9b) → open → restore → rerun → key results equal to 1e-6 (the fixture
  path and the cell path differ by ~1e-9 from the optimiser); also the
  Konstantopoulos pre-calculated example.
- **Steps 12–24 (phase 3, done)**: `PROJECT_STEPS` also has `regression`,
  `spline`, `meta_forest`, `pub_bias` (result key `trimfill_results`, needs
  `funnel_results` too), `pet_peese`, `timelag`, `loo`, `cumulative`
  (`cumulative_metadata`); they drop subgroup/9b settings and keep their
  own options in `analysis['options']` (`project_step_options`, from the
  results; Step 12 now stores `meta_regression_RVE_results['selection']`,
  Step 16 `meta_forest_results['features']`). Key results: `_pr_<step>`
  functions in `_PROJECT_LATER_RESULTS`; text `_project_later_text`,
  options text `_project_options_text`. Stale check: the result's
  `timestamp` older than `overall_results['timestamp']` → refused (plus the
  stale banners of 12, 14, 16). `project_settings` also drops every key
  ending in `_results`, `_text`, `_metadata` (spline_text etc. had leaked
  into settings: 117 KB → 25 KB for 8 analyses). Save tab: wrapped
  `VBox([project_save_bar(step), tab_export])` ("💾 Export & Save") in
  12, 14, 17, 19b, 24; a new "💾 Save" tab in 16, 19, 21. Each cell, after
  building its UI, calls `project_restore_options(step)`; if not None, a
  `restore_and_run(opts)` checks the options against its widgets
  (`project_widget_values`) and runs, or shows
  `project_restore_note_html(step, problems)` (red, nothing runs). Steps 17
  and 21 have no options: they just run. Bootstrap (CWB) is never re-run;
  its p, R and seed are stored in the regression's key results.
- Follow-up fixes (user's request): (1) stale banners registered in 9b
  ('meaningful'), 17 ('pub_bias'), 19 ('pet_peese'), 19b ('timelag'), 21
  ('loo'), 24 ('cumulative'); `ALL_DOWNSTREAM` and Step 7's `mark_stale`
  list now include 'meaningful', 'meta_forest', 'timelag'; Step 9 marks
  'meaningful'; Step 16 now calls `clear_stale('meta_forest')`;
  `PROJECT_STEPS` banners set, so stale results are refused by the banner
  too. (2) `project_restore_options` returns the options only until
  `project_restore_note_html(step)` (no problems) sets
  `_project_restored['options_applied']`. (3) `project_open_widget`
  empties the upload after reading (`reset_upload`: ipywidgets 8 sets
  `value = ()`; ipywidgets 7.7.1, Colab's version, has a read-only value
  rebuilt from `data`/`metadata` when `_counter` changes, so it empties
  those, then `_counter = 0`; tested in a 7.7.1 venv: same file twice →
  opened twice, once each).
- Round trip (fixture → cell path): all 8 later steps reproduce to 1e-6
  except the meta-forest when the first session used the fixture: the
  forest weights use Step 7's T², which differs in the 9th digit between
  the fixture path and the cell path, and the OOB R² moves in the 3rd
  digit. Cell path → cell path is identical (checked in two sessions).
  The forest is that sensitive to tiny numerical differences; tell the user
  if a Verify cell is built (looser tolerance for the meta-forest).
- Agreed phases: (1)–(3) done; (4) "Export for publication" (tick
  analyses, readable table) and a Verify cell that reruns every saved
  analysis and compares with the stored key results.

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
  - Unit tests: 91 passed.
  - V28 passes (84/84 on the fixture, about 6.5 min; 186/186 with the
    reference datasets).
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
- **Figure presets** (replaced in November 2026 by page shares, see 4.4; this note is history): Generic (85/120/175 mm), Elsevier (90/140/190 mm),
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
- **Killing test runs**: `pkill -f run_pre.py` also kills the shell that
  runs it (its own command line matches) and the tool call fails. Use
  `pgrep -f "[p]ython run_pre.py ..."` (the bracket keeps the pattern from
  matching itself) and `kill` the pids.
- **Waiting for background runs**: foreground `sleep` is blocked; use a
  background Bash `until ! pgrep -f "[t]_script.py"; do sleep 10; done`.
- **Plot-cell tests without the fixture**: a synthetic `ANALYSIS_CONFIG`
  with the keys the cell's `build_data` reads is enough (section 9.7).
  `ANALYSIS_CONFIG` is created by Cell 2/3, so assign a new dict rather
  than calling `.clear()` after only Cells 1 and 1b.
- **Screenshots**: use Playwright from Node (`require('playwright')`,
  `chromium.launch()` needs no options); the browser folder name in
  `/opt/pw-browsers` changes between images (1194, 1243, …). Static HTML of
  a dashboard works; ipywidgets have no frontend headless, so render a widget
  tree to HTML yourself (a small recursive VBox/HBox/HTML/Text/Button →
  HTML function was enough for the project manager screenshot).
- **Colab runs ipywidgets 7.7.1; the sandbox has 8.x.** Differences that
  bit us: `FileUpload.value` is a read-only dict rebuilt from
  `data`/`metadata` when `_counter` changes (8.x: a settable tuple of dicts,
  `last_modified` must be a datetime when you fake one); `tooltip` exists
  only in 8 (`description_tooltip` in 7: check `'tooltip' in
  w.trait_names()`). Test 7.7.1 behaviour in a throw-away venv
  (`python3 -m venv venv7 && venv7/bin/pip install ipywidgets==7.7.1`).
  Matplotlib: legend handles are `leg.legend_handles` (new) or
  `leg.legendHandles` (old); use `getattr`.
- **The sandbox's matplotlib default font is Inter**, Colab's is DejaVu
  Sans. Since November 2026 the plots draw with `FIGURE_FONT` (DejaVu Sans
  by default) through `figure_style`, so headless images now match Colab;
  comparisons with images made before that differ by a pixel or so.
- **Settings are restored in dict order** (`apply_widget_values`): a widget
  whose observer changes other widgets (a palette/scheme dropdown) must come
  *before* them in the controls dict, or a recipe's colours get overwritten.
- **Widgets created per run**: Step 7's and Step 9's save bars live in
  `render_export_tab`, so every run makes a new bar; tests must take the
  last widget with a given description, and the bar they click may belong
  to a different step than expected (it happened once: a "stale" test
  saved through Step 7's newest bar).
- **Time-lag plot**: `save_button` saves `last_fig`; click `draw_button`
  first after changing settings. **Step 9b**: re-running the cell resets its
  state; click *Compute Proportions* before *Generate Plot*.
- **Fixture path vs cell path**: `fixture_user.py` skips Steps 3–4, so its
  Step 7 estimates differ from the cell path in the ~9th digit. Compare
  restored analyses with a 1e-6 tolerance; the meta-forest (weights from
  Step 7's T²) can move in the 3rd digit, so for it compare cell path with
  cell path.

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

## 8. Open items and ideas (updated November 2026)

- **Release steps left to the user**: see section 2b.
- **Suggested, not started**:
  1. A combined report: gather every Detailed Statistics tab into one
     Markdown file (Step 27 export). High value for the "tool to learn" goal.
  2. A glossary (τ², σ², I², CR2, Satterthwaite df, PI, …) linked from the
     dashboards and the README.
  3. Navigation markdown cells between groups of steps (Setup, Data,
     Overall, Moderators, Publication bias, Sensitivity, Complementary,
     Project, Validation). The notebook has only one markdown cell. The README
     refers to steps by name, so it stays valid; cell indices in this guide,
     CONTRIBUTING and the harness would shift. Offered, not yet chosen.
  4. A real end-to-end run in Colab, and committing an executed validation
     record (JSON plus the executed notebook) for MEE.
  5. Further spline options: several spline moderators added together, or a
     spline × factor interaction. They need many studies; option 1
     (adjustment) is done.
  6. Project file (section 4.5): phase 4 left — an "Export for
     publication" table (tick analyses, readable table for the supplement)
     and a Verify cell (rerun every saved analysis, compare with the stored
     key results; looser tolerance for the meta-forest; bootstrap p-values
     are not rerun). Also offered: a pre-filled analysis name in the save bar
     (e.g. "Meta-regression: time + method"), and in the manager a mark on
     the restored analysis, the revision log (collapsed) and a filter by step.
  7. Narrow the broad `except Exception` handlers in statistical code
     (`load_reproducibility_config`, the dead session loader, was removed).
  7b. Figures (offered after the figure review, not chosen yet): an estimate
     [CI] column and the prediction interval in the forest plot; a
     study-level forest plot; a shared house style (one palette, bold or
     plain labels); plot titles off by default (journals put them in the
     caption; changes every default figure, so it is the user's call).
  8. **Capture cell for overall analyses** (discussed with the user, not
     built): a cell after Step 7 that snapshots the current overall result
     with a label (e.g. "site = A"), and an orchard data source "Captured
     overall analyses". Guardrails: same effect-size type, warn on different
     CI level / t-z / CR2 / estimator, caption says the rows are separate
     models (no test of differences), saved in the project file and recipes.
     For two levels of one moderator, the orchard's "own variances" option
     (done) is the better answer.
  9. Add Okabe-Ito and Paul Tol bright to the orchard plot's colour schemes
     (the bubble plot has them).
  10. Add to Validation 3: "own variances = separate per-subgroup fits when
     no study spans two subgroups" (checked once on the fixture: μ, CR2 SE,
     Satterthwaite df, τ², σ² equal to 6 decimals; not a permanent check).
  11. Untested paths: the orchard colour pickers in a two-way analysis and
     after a recipe reload; V28's wildmeta comparison (needs CRAN); the map
     cell (plotly missing headless). To confirm in Colab (asked the user):
     the font note says Liberation Sans when Arial is chosen; opening the same
     project file twice; the size presets on a real figure; the
     `cometa_full_height` behaviour.
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
for i, c in enumerate(nb['cells']):        # keep mine/c{i}.py current (drive.py runs these)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mine', f'c{i}.py'), 'w').write(''.join(c['source']))
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
# (for project-file tests also: ANALYSIS_CONFIG['clean_dataframe'] = _raw.copy() after the update below)
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
for i in range(33, 62):
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

### 9.7 Light harness for plot cells (no R, no fixture)

```python
# run_plot.py — run Cells 1 and 1b, a synthetic setup, then a driver script
import json, os, glob
from IPython.testing.globalipapp import start_ipython
ip = start_ipython()
nb = json.load(open('/home/user/CoMeta/CoMeta.ipynb'))
cell = lambda i: ''.join(nb['cells'][i]['source'])
for i in (1, 2):
    print(i, ip.run_cell(cell(i), silent=True).success)
ip.run_cell(open('setup.py').read())          # assigns ANALYSIS_CONFIG = {...}
os.makedirs('out', exist_ok=True); os.chdir('out')
ip.user_ns['cell15'] = cell(15)               # the plot cell to test
print(ip.run_cell(open('../drive.py').read()).success)
```
`setup.py` for the bubble plot: `ANALYSIS_CONFIG = {'es_config': {...,
'type': 'lnRR'}, 'effect_col', 'var_col', 'global_settings': {'alpha',
'dist_type'}, 'analysis_data': reg, 'meta_regression_RVE_results': {'reg_df',
'effect_col', 'term_names', 'moderator_col_name', 'betas',
'var_betas_robust', 'df_robust', 'p_values_all', 'model_type', 'tau_sq',
'sigma_sq', 'k_studies', 'n_obs', 'R_squared_adj', 'cwb': [{'label':
'Coefficient x', 'p_value': ...}]}}`. For the orchard: `overall_results`
(`k`, `k_papers`, `reported` with mu/se/ci/pi/tau_squared/sigma_squared/model)
and `subgroup_results` (`analysis_type`, `moderator1`, `results_df` with
group, k, n_papers, pooled_effect_re, pooled_se_re, ci_*_re, pi_*_re,
model_type). `drive.py`: run the cell, collect widgets from
`ipywidgets.Widget.widgets`, set values, click "Generate…", rename the
newest PNG; read the PNG to check it.

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

### 9.8 Harness for figures, the project file and old recipes (November 2026)

All in `$SP`, run with `python3 run_pre.py 1,2,3,5,7,8 <script>.py` (Steps 12–24
need no R). Patches with awkward quoting are easiest as a pickled list:
build `PATCHES` in a Python heredoc, `pickle.dump` it, and give `nbpatch.py`
a two-line file that loads it.

`figharness.py` (exec it at the top of a test script):

```python
import os, glob, json, sys
exec(open('fixture_user.py').read()); exec(open('mine/drive.py').read())
import ipywidgets as _w
def W(desc, cls=None):
    ws = [w for w in _all_widgets() if getattr(w, 'description', None) == desc and (cls is None or isinstance(w, cls))]
    if not ws: raise KeyError(desc)
    return ws[-1]
def setw(desc, v): W(desc).value = v
def B(desc): return W(desc, _w.Button)
PREP = {   # run the analysis a plot cell needs
 11: lambda: (drive_step8('method'), drive_step9(), drive_step9b()),
 12: lambda: (drive_step8('method'), drive_step9()), 13: lambda: (drive_step8('method'), drive_step9()),
 15: lambda: drive_step12(['time'], []),
 17: lambda: (_cell(16), setattr(_spline_view.mod_dropdown, 'value', 'time'), _spline_view.run_button.click()),
 20: lambda: (_cell(19), B('▶ Run Publication Bias Analysis').click()),
 24: lambda: (_cell(19), B('▶ Run Publication Bias Analysis').click()),
 26: lambda: (_cell(25), _loo_controller.run_analysis()), 27: lambda: (_cell(25), _loo_controller.run_analysis()),
 30: lambda: (_cell(28), _cumulative_controller.run_analysis()), 22: lambda: None}
GEN = {11: '📊 Generate Plot', 12: '📊 Generate Forest Plot', 13: '🌳 Generate Orchard Plot',
       15: '📊 Generate Regression Plot', 17: '📊 Generate Spline Plot', 20: '📊 Generate Trim-and-Fill Plot',
       24: '📊 Generate Funnel Plot', 26: '📊 Generate LOO Plot', 27: '📊 Generate Baujat Plot',
       30: '📊 Generate Cumulative Plot'}
def run_variants(cell, variants):          # variants: [(tag, {widget description: value})]
    PREP[cell](); os.makedirs('figs2', exist_ok=True); base = os.getcwd(); _cell(cell)
    if cell == 22: timelag_controller.on_run()
    os.chdir('figs2'); out = []
    for tag, settings in variants:
        for d, v in settings.items(): setw(d, v)
        before = set(glob.glob('*.png'))
        if cell == 22: timelag_controller.view.draw_button.click(); timelag_controller.view.save_button.click()
        else: B(GEN[cell]).click()
        new = sorted(set(glob.glob('*.png')) - before)
        if new: os.replace(new[0], f"c{cell}_{tag}.png"); out.append(f"c{cell}_{tag}.png")
    os.chdir(base); print('FIGS', out)
```

Then e.g. `run_variants(26, [('default', {}), ('pct', {'X-axis as % change
(lnRR)': True, 'Panel label:': 'B', 'Font (all figures):': 'Arial'})])`, and
paste the PNGs into one contact sheet with PIL (resize each to the same
width; 2 per row for an overview, or half / full / slide side by side to judge
font balance) and look at it with Read. Size presets are set with
`setw('📏 Size:', 'Half page or one column (8 cm)')`.

**Capturing what a cell displays** (to check for red boxes or messages):

```python
_shown = []
_orig = get_ipython().display_pub.publish
def _pub(data, *a, **k):
    _shown.append(str(data.get('text/html', ''))); return _orig(data, *a, **k)
get_ipython().display_pub.publish = _pub
```

**Project file round trips.**
- Session A (`t_e2e1.py`): fixture, then click the save bars (`W(_w.Text,
  'Analysis name:')[-1]`, `B('💾 Save analysis & download project')`; the
  first save also fills `'Project name:'`). For a filtered analysis, set
  `ANALYSIS_CONFIG['prefilters']` and `is_reproducing = True` and run cells
  4–8 (the restore path applies the filter). Write `PROJECT_LAST_FILE[1]`
  to a file.
- Session B (`t_e2e2.py`, pre-run 1,2,3 only): `project_from_bytes(file)`,
  then for each analysis `project_restore(P, id)`, run cells 4–8 and the
  step's cell (Step 9b: also click Compute), and compare
  `project_key_results(ANALYSIS_CONFIG, step)` with the stored `results`
  leaf by leaf (rtol 1e-6) and `project_step_options` with `options`.
- Strict restore: deep-copy the project, break one option or setting
  (unknown column, τ² method, moderator, precision term…), restore, run the
  cell, and check that a "Reproducibility Mode stopped" box was shown and no
  result was written.

**Old plot recipes still load** (`t_oldrec.py`, `t_newload.py`):
`git show HEAD:CoMeta.ipynb > old.ipynb`, dump it to `oldmine/`, and run a
copy of the harness against it (`NB=old.ipynb`, `drive.py` pointing at
`oldmine/`) to save a recipe per plot with
`COMETA_PLOT_PANELS[plot_type]['save']()`. Then, in a fresh session of the
new notebook (cells 1,2,3 only), run each plot cell and call
`COMETA_PLOT_PANELS[plot_type]['load'](bytes, name)`; expect `True`, a PNG,
and no "❌" or "Settings not applied" message. Plot types: meaningful_effects,
forest, orchard, meta_regression, spline, trim_and_fill, timelag, funnel,
leave_one_out, baujat, cumulative_trends (and map).

---

## 10. Collaboration history (what was done, in order)

Most recent first:

- *(session of 2–3 November 2026, branch `claude/youthful-pasteur-hm1pmf`,
  commits `0a435f1` … `d3b7a64`; not merged to `main` yet)*. It started as a
  question about reproducibility for a paper's supplement and ended with a
  figure review:
  1. **Reproducibility design discussion.** The old export wrote one JSON per
     analysis, each with the full data, and covered only Steps 2–9b. Text
     "codes" (a readable string per analysis) were considered; the user
     preferred one JSON. Storage options (download/upload, Google Drive, the
     data's Google Sheet) were compared; the user chose download on every
     save (repeated downloads tested fine in Colab) with a manager in Step 2.
  2. `0a435f1` **Project file** for Steps 7, 9, 9b (section 4.5), strict
     restore in Steps 3, 5, 7, 8, 9b, old session files open as projects.
  3. `c682c84` Save bar moved into the export tab, renamed "💾 Export & Save"
     (user request).
  4. `ea35926` **Steps 12–24** saved and restored (options in
     `analysis['options']`, `restore_and_run` per step); generated texts no
     longer leak into settings.
  5. `fe64f92` After a review the user picked: stale banners in 9b, 17, 19,
     19b, 21, 24 (they had none; Step 7 marked ids nobody registered);
     restored options applied once; the upload box emptied so the same file
     opens twice (ipywidgets 7 and 8).
  6. `a693e3e` **Figure review** (all 11 figures rendered and inspected):
     shared options (font for all figures, panel letter, manual axis ranges,
     editable PDF text), percent-change axis in five more plots, and fixes in
     the LOO, funnel, trim-and-fill, bubble, spline, cumulative and 9b plots
     (section 4.4). Old recipes checked.
  7. `9e07fb0` The user found journal-specific presets a mistake: presets are
     now page shares with balanced fonts, markers follow the width, the
     width typed by hand rebalances both (section 4.4).
  8. `d3b7a64` Last low-risk pass (user picked 1–3 of 7): `cometa_error` red
     boxes instead of 20 printed "❌ ERROR" lines, dead
     `load_reproducibility_config` removed, Okabe-Ito colours in the 9b
     dashboard.
  Unit tests went from 84 to 91. The full R validation suite was not rerun
  (no statistical code changed); the smoke run of every step cell, V11 and
  the project/recipe round trips were.
- *(plots, November 2026, same branch; commits `eee5781` … `4a943a2`)*:
  - **Percent-change axis for lnRR** (shared helpers in Cell 1, section 4.4):
    bubble plot (y axis; equation box adds the slope as % per unit; caption
    explains) and orchard plot (effect axis x or y with the orientation;
    estimate/CI annotations in % with the ES/CI decimals; Min/Max stay in
    lnRR units, a note says so). Default axis label switches to
    "Change (%)" and back unless the user typed one.
  - **Orchard "own variances"** (`estimates` = 'own'): subgroups drawn from
    Step 9's separate-variance model; "Show Overall row" can hide Overall.
    Use case from the user: sites A and B fitted separately because their
    variances differ — the separate-variance model gives the same numbers
    when no study spans two sites, plus a formal A vs B test.
  - **Colours**: orchard colour picker per group (Labels tab); bubble plot
    Palette dropdown (Tab10 default, Okabe-Ito, Paul Tol bright, Viridis,
    Grayscale, Set2, Dark2) and a picker per category of the Color By
    moderator (Labels tab, "Colours" section).
  - **Bubble-plot stats box and legend** (reviewer comment on the user's
    paper): `stats_style` 'slope' = "slope = b per unit of <x label> (95% CI
    lo to hi)" with equal decimals, "p = 0.020; bootstrap p = 0.041" (boot p
    only if Step 12's bootstrap panel ran before the plot cell), "k effect
    sizes, m studies"; stars switch; custom text box replaces the box, with
    a button that copies the automatic text; bubble legend label and on/off.
    Defaults reproduce the old plot.
- *(Validation 28 speed and robustness, November 2026)*: `9577c36`,
  `8d7d0ca`. The user's first Colab run (969 effect sizes, 75 studies) ran
  2 h 20 min and crashed with "Error during the optimization" (an
  unguarded R fit). Fixes: sparse R fits from 250 rows, warm starts,
  best-of-starts REML, fallback optimizers on the first start only,
  per-comparison error handling (R failure = INFO), priority order,
  progress line, `V28_MAX_MINUTES = 30`, `grp_levels`, reference datasets
  only for steps whose cells ran, non-finite bootstrap statistics handled
  explicitly. Where R and CoMeta disagreed, CoMeta always had the higher
  REML log-likelihood (R stalled). Details in section 2 (V28 paragraph).
- *(Validation 28, October 2026)*: `272298d`, dedicated cluster wild
  bootstrap validation (section 2); the test builders carry `inputs`.

- *(file names, October 2026, same branch)*: every saved file is named
  `<Analysis>_<settings>_<k>ES-<studies>st[_F-<filters>].<ext>` (user's design:
  no "CoMeta", no step number, no timestamp). Cell 1 "FILE NAMES" block:
  `_name_part`, `cometa_moderator_tag` (4 letters, `+Nmore` after 2),
  `cometa_filter_tag` (column 3 letters, longer if two columns clash; one kept
  value → 3 letters, several → `2of5`; filters that keep everything ignored),
  `cometa_setting_tags` (`2level`, `noCR2`, `z`, `90CI`), `cometa_analysis_stem(key, name)`
  (knows where each analysis stores its counts), `cometa_plot_stem` (typed name
  > `data['file_stem']` > analysis), `cometa_unique_stem`/`cometa_file_name`
  (`_vN` against `COMETA_FILES_WRITTEN` and the working directory). Plot cells:
  Filename box empty by default (placeholder "automatic…"), `file_stem` stored
  in `state['data']` after `build_data()` so recipes keep the name; Bubble plot
  adds `-<x-axis>` after `BubblePlot`. Add new outputs through these helpers.
- *(subgroup shared-variance check, Stage 1, October 2026, same branch)*:
  - Problem the user hit: the shared τ²/σ² of the unified subgroup model
    pulls a small, very heterogeneous subgroup toward the others' precision.
  - `subgroup_variance_check(fit, levels, L, results_df, alpha, dist_type,
    robust)` (Cell 10, module level, before `_largest_complete_subgrid`):
    rows of each subgroup found by matching design rows to `L`; blocks from
    `fit.spec` (V sliced with `np.ix_`); `fit_blocks` per subgroup (σ² = 0 if
    the shared fit fixed it, or no replication in the subgroup); CR2 via
    `fit_cr2` when the unified fit used CR2, else model-based, df = studies − 1;
    subgroups with < 2 studies are not fitted. Flags: `conclusion`
    (significance differs or opposite signs), `shift` (own mean outside the
    shared CI), `variance` ((τ²+σ²) ratio > 4 or < 1/4, only with ≥ 5 studies,
    `VARIANCE_CHECK_MIN_STUDIES`, `VARIANCE_CHECK_RATIO`). Verdict:
    `estimates differ` / `variances differ` / `consistent`.
  - Equal-variance LRT = 2(Σ ll_separate − ll_shared), REML, df = Σ free
    variance params − shared; only for between-study moderators (additivity
    of REML ll, invariant to the X parametrisation with REMLf). Verified: Σ ll
    equals metafor's `struct = c("DIAG","DIAG")` heteroscedastic model.
  - Called in `analyze_all_subgroups` after the pairwise contrasts (not in the
    fallback); stored in `heterogeneity['variance_check']` and
    `subgroup_results['variance_check']` (plain JSON-safe values).
  - Shown in: new tab 2 "⚖️ Variance Check" (tabs after it shifted by one),
    dashboard (warning for `estimates differ`, a story sentence otherwise),
    Detailed Statistics section, Methods paragraph + refs [5–7]
    (Rubio-Aparicio 2017, 2020; Rodriguez et al. 2023, checked with Scite;
    authors after the third are "et al." — complete them), Results paragraph,
    Excel sheet "Variance Check". README (Step 9, Methods, References),
    CHANGELOG.
  - Validation 3 section 6: per-subgroup rma.mv (free REML) + clubSandwich
    CR2, Σ logLik, the DIAG model and the LRT; unit tests
    `test_variance_check_identical_subgroups` (LRT = 0) and
    `test_variance_check_within_study_moderator_skips_lrt`.
  - **Stage 2 (done, same branch):** `fit_separate_variance_model` (REML of
    Σ_j = V_j + diag(σ²_g) + τ²_g within subgroup; metafor random =
    list(~g|study, ~g|es), struct = "DIAG"), `_diag_loglik` /
    `_diag_loglik_grad` (analytic REML gradient, checked by a unit test;
    L-BFGS-B ftol 1e-12, gtol 1e-8; "converged" = success or projected
    gradient < 1e-3, because the line search ends ABNORMAL at machine
    precision), `_separate_variance_inference` (CR2 with
    `_compute_robust_var_betas(..., phi_blocks=...)`, the new working-model
    argument; AHZ omnibus on eye(p)[1:], pairwise via
    `SubgroupAnalysisEngine._pairwise_contrasts`, two-way via
    `_factorial_wald_tests`). When no study and no sampling covariance spans
    two subgroups, the separate fits are the exact optimum and are used
    directly; otherwise joint REML from three starts. The tab's "Own τ², σ²"
    columns now show this model (not the per-subgroup fits, which remain for
    the LRT: `rows[i]['log_lik_alone']`). `vc['separate_model']`,
    `vc['test_change']`, `vc['n_pairwise_change']`, pairwise rows get
    `shared_p_holm` / `changes`. Verdict 'estimates differ' also when the
    omnibus or a Holm pairwise conclusion changes. Timing: ~8 s for 2200
    effect sizes, 80 studies, 10 subgroups.
  - Validation 3 section 6 now fits metafor DIAG (cell-means, `gamma2` fixed
    at 0 where σ²_g is), clubSandwich CR2 with `cluster = study_id`, HTZ via
    `constrain_equal`, every pairwise contrast and the two-way terms
    (constraints `bases[key].T`); Σ logLik alone vs DIAG for the LRT. Tested
    also with a random 'hgroup' that splits shared-control groups
    (`t_v3c.py`): 71/71.
- *(cluster wild bootstrap, October 2026, same branch)*: engine in Cell 1b
  section 7b: `cwb_test(y_blocks, X_blocks, C, fitter, R, aux, adjust, mode,
  seed, full, eta, progress)`, `cr0_wald_F`, `cr2_adjustment_blocks`,
  `constrain_predictors`, `cwb_weights` (Rademacher, Webb six),
  `cwb_multilevel_fitter(V_blocks, sigma2_fixed)`, `CWB_DEFAULTS` (999,
  Rademacher, CR0, reestimate, seed 2024). Algorithm = wildmeta 0.3.3
  (read from its source: null model by projection, residuals × weight per
  cluster, refit with update(), CR0 Naive-F, p = mean(F* > F)); 'fast' mode
  keeps the full model's Φ (one GLS per replication). Separate-variance refit:
  `cwb_separate_fitter` (Cell 10). Panel `cwb_panel(tests, alpha, on_done)`
  (Cell 1): borderline = AHZ df < 4 or 0.01 ≤ p ≤ 0.10; time estimate from 2
  and 6 replications per model family; results JSON-safe (`ref_test`, `kind`,
  `agree`, ...). Text: `cwb_methods_sentence`, `cwb_results_sentence`,
  `cwb_result_rows`, `CWB_REFERENCE`, Excel `_cwb_sheet`. Step 9:
  `subgroup_cwb_tests(het)`; the view's Detailed Statistics now has
  `stats_out` + `cwb_out` (`refresh_statistics`); controller global
  `_subgroup_controller`; results in `subgroup_results['cwb']`; the
  separate-variance model kept in memory as `separate_model_fit`. Step 12:
  `regression_cwb_tests(result)`, `RegressionResult.cwb_inputs` (the fit, or
  y/v/X of the aggregated two-level model, compared with Knapp-Hartung) and
  `.cwb`; `_run_three_level_reml_regression_v2` now returns 'fit'.
  Validation: Cell 32 defines `CWB_R_REFERENCE` (R `cwb_reference`,
  `cwb_wildmeta`) and `cwb_validation_checks`; V3 section 7 and V4 compare
  every bootstrap F with injected weights (rel. tol 1e-3, p within 1/R; R's
  optim can stop slightly off at boundaries, Python matches the separable
  per-subgroup optimum). wildmeta itself could not be installed in the
  sandbox (installing code from GitHub was refused); its branch is INFO only
  and untested. Speed: ~25 ms/replication at 100 ES (diagonal V), ~70 ms
  with shared-control V, ~0.5 s at 2000 ES with shared controls.
- *(Geary's test, October 2026, same branch)*: `geary_number`, `GEARY_THRESHOLD`
  (Cell 7); Step 6 adds `geary_t`, `geary_c`, `geary_pass` to analysis_data
  (lnRR, raw data; imputed SDs used) and `calc_info['geary']` (n, n_fail,
  n_fail_imputed, n_studies_fail). The columns are in EFFECT_DERIVED_COLUMNS
  (never moderators). Step 7: the SD complete-case refit was moved into
  `OverallController._refit_overall_on_rows(df, vcv, result, alpha, dist,
  use_kh)`; the Geary refit uses it on `geary_pass` rows (VCV rebuilt) and is
  stored in `ANALYSIS_CONFIG['geary_check']` (calc_info geary + 'refit'; in
  RESULT_KEYS). Shown: `_dash_geary_html` (dashboard note, amber when the
  conclusion changes), Step 7 Detailed Statistics section, data-selection row,
  Methods sentence (cites Lajeunesse 2015 via ref_bias), Results paragraph.
  Failing rows are kept (Lajeunesse recommends a sensitivity analysis); no
  exclude option yet. V20 `_geary_rows` recomputes in R with the authors'
  function. Unit test `test_geary_number_lajeunesse_2015`.
- *(pooled CV, October 2026, same branch)*: `calculate_pooled_cv_nakagawa`
  (Cell 7): n-weighted mean CV within study, weighted by the study's mean n
  across studies (the authors' simulation code, `Miss_SD_Sim/R/MLMA_HPC.R`,
  averages within study unweighted; equal when n is constant). Used by
  'nakagawa_missing_cases' / 'nakagawa_all_cases'; the old estimator
  (`calculate_pooled_cv`, CV² averaged over rows, weights n − 1, CV(1+1/4n))
  is 'pooled_cv2_missing_cases'. Methods text describes the formula. V20
  recomputes both pooled CVs in R (`_pooled_cv_rows`, runs even with old
  metafor). The sampling variance stays first order (Hedges 1999); the paper
  adds second-order terms (Lajeunesse 2015) — not implemented.
- *(publication-text review, October 2026, same branch)*:
  - **Data selection** (Cell 1: `data_selection_info`, `data_selection_rows`,
    `_with_data_selection`): `statistics_table_text`/`_html` append a
    "Data selection (Steps 2–6)" section to every Detailed Statistics table.
    Inputs: Step 3 `prefilter_counts`; Step 4 `n_observations_step4_in` (and
    `removed_records` for pre-calculated data); Step 6 `calc_removed_records`
    and `calc_info` (`cc_rows`, `sd`: strategy, n_imputed, pooled CVs). These
    three are in `RESULT_KEYS` (not saved in the session file).
  - **Step 7 Methods** is data-driven: records, filters, exclusions (reason
    map `_REASONS`), SD sentence only when SDs were imputed, continuity
    correction only when applied, shared-control covariances (Gleser & Olkin
    2009; Lajeunesse 2011 for lnRR), inference/heterogeneity/PI sentences
    (Higgins & Thompson 2002; Nakagawa & Santos 2012; Higgins et al. 2009, all
    checked with Scite). `_cite(key)` adds a reference once; a final pass
    renumbers `[n]` and `[n, m]` by first citation and drops uncited ones.
  - Results texts: multilevel I² for the three-level model (the Q-based I² of
    86.8% vs multilevel 88.7% disagreed); subgroup Q_E test replaces the
    Q_M + Q_E "partition"; test name "approximate Hotelling's T² (AHZ)";
    cumulative CIs back-transformed; Step 16 CoMeta reference.
  - **Leave-one-out follows Step 7's CR2 and t/z** (`_LOOModelBased`, Cell 25);
    V22's R side takes `cr2`/`use_t` from the Step 7 settings. The refits are
    always three-level; the text says so when Step 7 reported two-level.
  - Text-review harness: `t_alltext.py` (captures every displayed HTML block
    per step, VARIANT=base/twolevel/z_nocr2) + `strip_caps.py`; strip tags
    with `</?[a-zA-Z][^>]*>` because the HTML contains raw "<" (p < 0.001).
- *(pre-submission review, October 2026, branch `claude/sweet-cori-xqlhn3`)*
  A review for the MEE submission, then the fixes:
  - this guide had been uploaded to the repo by mistake; it was removed
    (it stays in git history). Since November 2026 the user wants it in the
    repo root again (section header);
  - trim-and-fill counts effect sizes, so every user-visible text says
    "missing effect sizes" (Steps 17, 18, 19c); no "convergent evidence";
  - PET-PEESE Results text states the p threshold and why its slope can
    differ in sign from Egger's;
  - `k` = number of effect sizes in the publication texts (Steps 12, 13, 15);
  - Step 7 Methods: references renumbered in order of first citation;
  - meta-regression coefficients use 3 significant digits when |β| and SE
    are < 0.01 (`_coef_strings`, Cell 14);
  - BCG example: `id` = author + year (13 studies; reproduces −0.7145);
    built-in example dicts no longer have `np.str_` keys;
  - session-file wording: restores Steps 2–9b only (README, CHANGELOG, Step 2);
  - `REQUIRED_PACKAGES` gained scikit-learn 1.9.1 and pycountry 26.2.16 (the
    versions tested headless; replace them with Colab's after a Colab run);
    Cells 25 and 32 install pycountry / rpy2 at the pinned versions;
  - README: References subsection (methods + example datasets, checked with
    Scite) and the metadat origin of the examples; CITATION.cff
    `date-released`.
  - An anonymiser for double-anonymous review, `make_review_copy.py`, was
    given to the user (not in the repo).
  - Headless check: 23 validations PASS + 77 unit tests with metafor 4.4.0 /
    clubSandwich 0.5.10 (CRAN was blocked); V12 and V25 need R packages
    that could not be installed there.

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
