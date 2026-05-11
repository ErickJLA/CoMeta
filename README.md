# CoMeta: A No-Code Platform for Rigorous Three-Level Meta-Analysis in Ecology and Evolution

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Platform: Google Colab](https://img.shields.io/badge/platform-Google%20Colab-orange)](https://colab.research.google.com/)

---

## Overview

Meta-analysis has become central to evidence synthesis in ecology and conservation biology, yet state-of-the-art methods — including three-level hierarchical models, variance-covariance correction for shared control groups, and robust publication bias diagnostics — remain underutilized because their implementation barriers exceed what many research workflows can accommodate.

**CoMeta** is an open-source, no-code platform for rigorous ecological meta-analysis, deployed as an interactive [Google Colaboratory](https://colab.research.google.com/) notebook that requires no installation or programming expertise. Users control the complete analytical pipeline through widget interfaces; every line of the underlying statistical implementation remains directly inspectable, modifiable, and extensible by any researcher who opens the notebook. This *glass-box* design distinguishes CoMeta from compiled GUI platforms: the code is not merely open in principle but navigable in practice.

CoMeta is released in two configurations sharing an identical statistical engine:

| Configuration | Description |
|---|---|
| **CoMeta** (standard) | Full analytical pipeline through the widget interface |
| **CoMeta-dev** | Extends the standard release with validation cells in which every core statistical operation is independently verified through Monte Carlo simulation and reimplemented in R via `metafor` and `clubSandwich`, with side-by-side numerical comparisons |

---

## Key Features

### Statistical Engine

- **Three-level hierarchical random-effects models** fitted by Restricted Maximum Likelihood (REML), correctly partitioning variance into within-study (σ²), between-effect-sizes-within-studies (τ²_within), and between-studies (τ²_between) components
- **Exact variance-covariance (VCV) matrices** for shared control groups using the Gleser & Olkin (2009) and Lajeunesse (2011) closed-form expressions, preventing the artificial inflation of precision that occurs when shared controls are treated as independent
- **CR2 cluster-robust variance estimation** with per-coefficient Satterthwaite degrees of freedom (Pustejovsky & Tipton, 2018), providing valid inference under model misspecification without requiring knowledge of the true within-study correlation structure
- **Non-linear spline meta-regression** via restricted cubic splines (implemented through `patsy`), enabling continuous dose-response and threshold modelling without arbitrary categorical binning of moderators
- **Multiple publication bias diagnostics**: Egger's regression test, trim-and-fill (Duval & Tweedie, 2000), and PET-PEESE (Stanley & Doucouliagos, 2014)
- **Knapp-Hartung adjustment** for improved small-sample inference on pooled effects
- **Optional two-level model fallback** with automatic detection of degenerate three-level structures (τ²_within ≈ 0), transparent notification, and reversion to the appropriate two-level model

### Effect Size Support

| Effect size | Symbol | Typical use case |
|---|---|---|
| Log response ratio | lnRR | Continuous outcomes with a natural ratio interpretation (e.g., biomass, growth rate) |
| Hedges' *g* | *g* | Standardized mean difference, continuous outcomes, unequal variances |
| Log odds ratio | log OR | Binary outcomes |
| Log risk ratio | log RR | Binary outcomes, rare events |
| Pre-calculated | — | User-supplied effect sizes and variances |

A rule-based recommendation engine (Cell 5) evaluates data topology and applies six weighted scoring rules (R1–R6) to guide effect size selection, including detection of pure-binary, mixed, and continuous outcome structures.

### Workflow and Reproducibility

- **Session export/import**: the complete analytical configuration is encoded in a shareable JSON file; any collaborator can reproduce the exact analysis with a single click
- **Automated report generator**: dynamically produces manuscript-ready *Materials and Methods* and *Results* text adapted to the model selected, the bias diagnostics run, and the moderators tested, reducing transcription errors and improving consistency between reported methods and executed analyses
- **Staleness propagation**: a banner system notifies downstream cells when upstream configuration has changed, preventing silent inconsistencies in iterative analyses
- **Built-in example datasets**: including the Curtis & Wang (1998) CO₂ dataset for onboarding and benchmarking

---

## Getting Started

### Open in Google Colab

Click the badge at the top of this page, or navigate directly to:

```
https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb
```

No installation is required. All dependencies are managed automatically at runtime.

### Supported data formats

| Format | Notes |
|---|---|
| CSV / Excel (`.csv`, `.xlsx`) | Direct upload via Colab file dialog |
| Google Sheets | Authenticate with your Google account; paste the sheet URL |
| JSON session file | Load a previously exported CoMeta session for exact reproduction |
| Built-in datasets | Select from the dropdown in Cell 2 |

### Required columns

The minimum dataset for a three-level analysis requires, per effect size record:

| Column | Description |
|---|---|
| Study identifier | Groups effect sizes within the same primary study |
| Effect size group identifier | Nested within study; identifies the level-2 unit |
| Mean (experimental), SD, *n* | Or equivalent pre-calculated effect size and variance |
| Mean (control), SD, *n* | Required for lnRR and Hedges' *g* from raw data |

CoMeta applies a synonym-table column-mapping step (Cell 2) that accepts a wide range of common column names and coerces them to the internal schema automatically.

---

## Analytical Pipeline

CoMeta implements a linear pipeline of 44 notebook cells. The standard analytical cells are numbered sequentially; validation cells are labelled separately and are only present in CoMeta-dev.

| Cell(s) | Module | Description |
|---|---|---|
| 1 | Environment Setup | Dependency lock, core utilities, staleness-banner system |
| 2 | Data Ingestion | Four ingestion pathways; column mapping; synonym tables |
| 3 | Global Filtering | Pre-analysis subsetting by categorical or numeric column values |
| 4 | Data Cleaning & Pre-processing | Missing-SD imputation (four strategies); shared-control detection; VCV triggers |
| 5 | Effect Size Diagnostics | Rule-based effect size recommendation; data-topology audit |
| 6 | Effect Size Calculation | Computation of effect sizes and sampling variances; exact VCV matrix construction |
| 7 | Overall Meta-Analysis | Three-level REML model; CR2 inference; heterogeneity statistics (*I*², *Q*); automated text |
| 8–9 | Subgroup Analysis | Configuration and execution of subgroup REML models with CR2 per group |
| 10–11 | Subgroup Visualization | Forest plot and orchard plot renderers |
| 12–13 | Meta-Regression | Linear meta-regression with CR2 cluster-robust inference; coefficient plots |
| 14–15 | Spline Meta-Regression | Non-linear restricted cubic spline model; spline curve visualization |
| 16–19 | Publication Bias | Egger's test; trim-and-fill; PET-PEESE; funnel plot |
| 20–22 | Sensitivity Analysis | Leave-one-out meta-analysis; Baujat influence plot |
| 23–25 | Complementary Analyses | Cumulative meta-analysis; geographic distribution map; temporal trends |

---

## Statistical Methods in Detail

### Three-Level REML Optimisation

The core estimator (`ThreeLevelEngine.fit`, Cell 7) maximises the restricted log-likelihood over the variance-component space (τ²_within, τ²_between) using a deterministic six-start L-BFGS-B optimiser. The marginal variance matrix for study *i* is:

```
Σᵢ = τ²_between · Jᵢ + τ²_within · Iᵢ + Vᵢ
```

where **V**ᵢ is the block of sampling variances (and covariances, when shared controls are present), **J**ᵢ is a matrix of ones, and **I**ᵢ is the identity matrix. Profile-likelihood confidence intervals are computed by one-dimensional Brent root-finding over the profile log-likelihood surface. The prediction interval follows Higgins et al. (2009).

Inversion of Σᵢ follows a Sherman-Morrison path for diagonal **V**ᵢ and a full Cholesky decomposition when off-diagonal covariances are non-zero.

### Exact VCV Construction for Shared Controls

When multiple treatment arms share a single control group, the sampling covariances between their effect sizes are non-zero and must be modelled explicitly. CoMeta constructs per-study VCV blocks using the Gleser & Olkin (2009) expressions for Hedges' *g* and the Lajeunesse (2011) delta-method expressions for lnRR. The `detect_shared_controls` function (Cell 4) identifies shared control groups automatically and tags them with a `shared_group_id` column that is consumed by `build_vcv_matrices` (Cell 6).

### CR2 Cluster-Robust Variance Estimation

Cluster-robust standard errors are computed by `_compute_robust_var_betas` (Cell 7 / 12) following the CR2 estimator of Pustejovsky & Tipton (2018):

```
V̂_CR2(β̂) = (X'WX)⁻¹ · Σᵢ Aᵢ eᵢ eᵢ' Aᵢ' · (X'WX)⁻¹
```

where *e*ᵢ are the working residuals, **A**ᵢ are the CR2 bias-correction matrices, and degrees of freedom for each coefficient are obtained by the Satterthwaite approximation. This produces valid *t*-based inference even when the working model for Σᵢ is misspecified.

### Non-Linear Spline Meta-Regression

Continuous moderators are modelled with restricted cubic splines (`patsy` `cr()` basis), fitted within the three-level REML framework. This approach captures monotone, dose-response, and threshold relationships without the information loss inherent in categorical binning of a continuous variable. The number and placement of knots are user-configurable through the widget interface.

### Publication Bias Assessment

CoMeta implements three complementary diagnostics:

| Method | Implementation | Reference |
|---|---|---|
| Egger's regression test | Weighted regression of standardized effect on standard error | Egger et al. (1997) |
| Trim-and-fill | Iterative imputation of missing studies; pooled estimate under imputed symmetry | Duval & Tweedie (2000) |
| PET-PEESE | Precision-effect test and precision-effect estimate with standard error | Stanley & Doucouliagos (2014) |

---

## Validation

CoMeta's statistical engine was validated against `metafor` (Viechtbauer, 2010) and `clubSandwich` (Pustejovsky, 2022) via direct compatibility tests and Monte Carlo simulations. Validation cells (CoMeta-dev) implement each core operation independently in R via `rpy2` and compare outputs numerically.

### Summary of Validation Results

| Test | Method | Result |
|---|---|---|
| Overall model | Direct Python vs R comparison (real data) | Pooled effects, τ² components, CIs match to ≥ 4 decimal places |
| Overall model | Monte Carlo simulation (1 000 replications, multiple heterogeneity scenarios) | Empirical Type I error ≈ nominal α; CI coverage ≈ nominal level |
| Subgroup analysis | Direct Python vs R comparison | Subgroup estimates and heterogeneity statistics match to ≥ 4 decimal places |
| CR2 robust SEs | Direct Python vs `clubSandwich` R comparison | Coefficient SEs and Satterthwaite d.f. match to ≥ 4 decimal places |
| Linear meta-regression | Direct Python vs R comparison + Monte Carlo | Coefficients, SEs, and model-fit statistics match; empirical coverage ≈ nominal |
| Spline meta-regression | Curve-matching test and curve-recovery simulation | Predicted spline curves match R `metafor` + `patsy` output; signal recovered under simulation |
| Publication bias diagnostics | Direct Python vs R comparison | Egger's, trim-and-fill, and PET-PEESE outputs match reference implementations |

Validation cells are available in `CoMeta_1.ipynb` (Cells 26–43) and are executable by any user who opens the notebook.

---

## Worked Example: Curtis & Wang (1998) CO₂ Dataset

CoMeta ships with the canonical Curtis & Wang (1998) elevated CO₂ dataset as a built-in example. The demonstration analysis:

1. Replicates the original biomass effect size estimates
2. Extends the analysis with a continuous spline meta-regression of exposure duration — a moderator the original authors binned categorically due to software limitations
3. Demonstrates automated VCV construction, which correctly attributes within-study variance to shared control groups rather than a distinct hierarchical component

This example is accessible from the data ingestion dropdown in Cell 2 without any data upload.

---

## Session Reproducibility

Every analytical decision made through the widget interface is encoded in a single `ANALYSIS_CONFIG` dictionary and can be exported to a JSON session file via the export button in any results cell. The session file captures:

- All widget selections (effect size type, model configuration, moderators, knot placement, publication bias settings)
- Global settings (`α`, distribution type, τ² estimation method, Knapp-Hartung flag)
- Optimiser configuration and convergence metadata
- Provenance flags (data source, imputation decisions)

Loading the session file in a fresh Colab runtime restores the complete configuration and enables exact one-click reproduction of the analysis. The JSON schema is human-readable and version-controlled, making it suitable for deposition as supplementary material alongside a manuscript.

---

## Automated Report Generation

After each analysis module executes, CoMeta generates dynamically adapted *Materials and Methods* and *Results* text. The generator:

- Selects the correct model narrative based on the three-level vs two-level decision and the τ²_within boundary collapse outcome
- Conditionally includes or omits disclosures for SD imputation, Knapp-Hartung adjustment, and shared-control VCV correction depending on which procedures were applied
- Applies Cohen (1988) and Higgins et al. (2003) interpretation bins to effect sizes and *I*² statistics
- Formats all numerical results according to journal conventions (e.g., *d* = 0.42, 95% CI [0.18, 0.66], *p* = .003)

The generated text is displayed in a copyable widget and is also included in the session JSON export, providing a complete record of the reported statistics alongside the configuration that produced them.

---

## Dependencies

All dependencies are installed automatically in Google Colab. The core environment is locked by `check_and_lockdown()` (Cell 1) to the versions listed below.

| Package | Version | Role |
|---|---|---|
| `numpy` | 2.0.2 | Array operations, linear algebra |
| `pandas` | 2.2.2 | Tabular data management |
| `scipy` | 1.16.3 | Optimization (L-BFGS-B, Brent), statistical distributions |
| `matplotlib` | 3.10.0 | All figure rendering |
| `ipywidgets` | — | Widget GUI layer |
| `patsy` | — | Spline basis construction |
| `statsmodels` | — | Egger's regression, auxiliary GLMs |
| `rpy2` *(dev only)* | — | R bridge for validation cells |

---

## Citation

If you use CoMeta in published research, please cite:

> [Author et al.] (*in preparation*). CoMeta: From data to report — a no-code platform for rigorous three-level meta-analysis in ecology and evolution. *Methods in Ecology and Evolution*.

And the core methodological references:

- Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*, 36(3), 1–48.
- Pustejovsky, J. E., & Tipton, E. (2018). Small-sample methods for cluster-robust variance estimation and hypothesis testing in fixed effects models. *Journal of Business & Economic Statistics*, 36(4), 672–683.
- Nakagawa, S., Lagisz, M., O'Dea, R. E., Rutkowska, J., Yang, Y., Noble, D. W. A., & Senior, A. M. (2021). The orchard plot: Cultivating a forest plot for use in ecology, evolution, and beyond. *Research Synthesis Methods*, 12(1), 4–12.

---

## References

- Curtis, P. S., & Wang, X. (1998). A meta-analysis of elevated CO₂ effects on woody plant mass, form, and physiology. *Oecologia*, 113(3), 299–313.
- Duval, S., & Tweedie, R. (2000). Trim and fill: A simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*, 56(2), 455–463.
- Egger, M., Smith, G. D., Schneider, M., & Minder, C. (1997). Bias in meta-analysis detected by a simple, graphical test. *BMJ*, 315(7109), 629–634.
- Gleser, L. J., & Olkin, I. (2009). Stochastically dependent effect sizes. In H. Cooper, L. V. Hedges, & J. C. Valentine (Eds.), *The Handbook of Research Synthesis and Meta-Analysis* (2nd ed., pp. 357–376). Russell Sage Foundation.
- Higgins, J. P. T., Thompson, S. G., Deeks, J. J., & Altman, D. G. (2003). Measuring inconsistency in meta-analyses. *BMJ*, 327(7414), 557–560.
- Koricheva, J., Gurevitch, J., & Mengersen, K. (Eds.). (2013). *Handbook of Meta-Analysis in Ecology and Evolution*. Princeton University Press.
- Lajeunesse, M. J. (2011). On the meta-analysis of response ratios for studies with correlated and multi-group designs. *Ecology*, 92(11), 2049–2055.
- Nakagawa, S., & Santos, E. S. A. (2012). Methodological issues and advances in biological meta-analysis. *Evolutionary Ecology*, 26(5), 1253–1274.
- Pustejovsky, J. E. (2022). *clubSandwich: Cluster-robust (sandwich) variance estimators with small-sample corrections* (R package version 0.5.8).
- Stanley, T. D., & Doucouliagos, H. (2014). Meta-regression approximations to reduce publication selection bias. *Research Synthesis Methods*, 5(1), 60–78.
- Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*, 36(3), 1–48.

---

## License

CoMeta is released under the [MIT License](LICENSE). The statistical engine is open source and may be adapted for new analytical modules following the extension guide in [`docs/architecture_and_data_flow.md`](docs/architecture_and_data_flow.md).

---

## Contributing

Bug reports, feature requests, and pull requests are welcome via the [GitHub issue tracker](https://github.com/ErickJLA/CoMeta/issues). When reporting a numerical discrepancy, please include the session JSON file and the CoMeta version string printed by Cell 1.
