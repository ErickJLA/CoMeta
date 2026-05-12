# CoMeta: A No-Code Platform for Rigorous Three-Level Meta-Analysis in Ecology and Evolution

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Platform: Google Colab](https://img.shields.io/badge/platform-Google%20Colab-orange)](https://colab.research.google.com/)

> **CoMeta is a no-code Google Colab notebook that runs publication-grade three-level meta-analyses — including shared-control VCV correction, CR2 cluster-robust inference, and spline meta-regression — in a single afternoon instead of the weeks typically required to assemble an equivalent `metafor` + `clubSandwich` workflow in R.** It is designed for **ecologists and evolutionary biologists** who need rigorous evidence synthesis without writing a line of code, while keeping every statistical step open and inspectable.

---

## 🚀 Getting Started

**One click. No installation. No setup.**

1. Click the **"Open in Colab"** badge above, or open the notebook directly:

   ```
   https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb
   ```

2. In Colab, select **Runtime → Run all** (or run cells sequentially to follow the guided flow).

3. Either upload your own dataset (CSV, Excel, or Google Sheets) or load the **built-in Curtis & Wang (1998) CO₂ dataset** from the Cell 2 dropdown to explore CoMeta without any data of your own.

4. All dependencies install automatically at runtime — there is nothing to configure locally.

> 💡 **Tip:** New users should start with the [Truly Quick Start](docs/truly_quick_start.md) — a 3-minute click-through checklist that gets you from the notebook to manuscript-ready text with no theory upfront.

---

## 📚 Documentation

| Document | What it covers |
|---|---|
| [**Truly Quick Start**](docs/truly_quick_start.md) | A 3-minute, click-through checklist. Run each cell, accept the defaults, and collect manuscript-ready text. |
| [**Quick Start**](docs/quick_start.md) | A longer hands-on walkthrough with the rationale behind each step. |
| [**User Guide & Data Formats**](docs/user_guide_and_data_formats.md) | Detailed reference for supported inputs, required columns, synonym tables, and the widget interface. |
| [**Architecture & Data Flow**](docs/architecture_and_data_flow.md) | Internal design of the statistical engine and an extension guide for developers adding new modules. |

---

## ✨ Key Features

- **Three-level hierarchical REML models** that correctly partition variance into within-study (σ²), between-effect-sizes-within-studies (τ²_within), and between-studies (τ²_between) components.
- **Exact variance-covariance (VCV) correction for shared control groups**, preventing the artificial precision inflation common in ecological meta-analyses.
- **CR2 cluster-robust inference** with per-coefficient Satterthwaite degrees of freedom — valid *t*-based inference even under model misspecification.
- **Non-linear spline meta-regression** for dose-response and threshold modelling, without arbitrary binning of continuous moderators.
- **Multiple publication bias diagnostics**: Egger's regression, trim-and-fill, and PET-PEESE — side by side.
- **Knapp-Hartung adjustment** for improved small-sample inference on pooled effects.
- **Effect size flexibility**: lnRR, Hedges' *g*, log OR, log RR, or user-supplied pre-calculated effects, with a rule-based recommendation engine.
- **One-click reproducibility**: every analytical choice is encoded in a shareable JSON session file.
- **Automated report generator** that produces manuscript-ready *Materials and Methods* and *Results* text adapted to the model actually fitted.
- **Glass-box design**: every line of the statistical engine is directly inspectable, modifiable, and extensible inside the same notebook.

### Two configurations, one statistical engine

| Configuration | Description |
|---|---|
| **CoMeta** (standard) | Full analytical pipeline through the widget interface. |
| **CoMeta-dev** | Adds validation cells in which every core statistical operation is independently verified through Monte Carlo simulation and reimplemented in R via `metafor` and `clubSandwich`, with side-by-side numerical comparison. |

### Supported effect sizes

| Effect size | Symbol | Typical use case |
|---|---|---|
| Log response ratio | lnRR | Continuous outcomes with a natural ratio interpretation (e.g., biomass, growth rate) |
| Hedges' *g* | *g* | Standardized mean difference; continuous outcomes; unequal variances |
| Log odds ratio | log OR | Binary outcomes |
| Log risk ratio | log RR | Binary outcomes; rare events |
| Pre-calculated | — | User-supplied effect sizes and variances |

A rule-based engine (Cell 5) evaluates data topology and applies six weighted scoring rules (R1–R6) to guide effect size selection, with explicit detection of pure-binary, mixed, and continuous outcome structures.

---

## 📊 Analytical Pipeline

CoMeta implements a linear pipeline of **44 notebook cells**. The standard analytical cells are numbered sequentially; validation cells are labelled separately and are only present in CoMeta-dev.

| Cell(s) | Module | Description |
|---|---|---|
| 1 | Environment Setup | Dependency lock; core utilities; staleness-banner system |
| 2 | Data Ingestion | Four ingestion pathways; column mapping; synonym tables |
| 3 | Global Filtering | Pre-analysis subsetting by categorical or numeric column values |
| 4 | Data Cleaning & Pre-processing | Missing-SD imputation (four strategies); shared-control detection; VCV triggers |
| 5 | Effect Size Diagnostics | Rule-based effect size recommendation; data-topology audit |
| 6 | Effect Size Calculation | Effect sizes and sampling variances; exact VCV matrix construction |
| 7 | Overall Meta-Analysis | Three-level REML model; CR2 inference; heterogeneity statistics (*I*², *Q*); automated text |
| 8–9 | Subgroup Analysis | Configuration and execution of subgroup REML models with CR2 per group |
| 10–11 | Subgroup Visualization | Forest plot and orchard plot renderers |
| 12–13 | Meta-Regression | Linear meta-regression with CR2 cluster-robust inference; coefficient plots |
| 14–15 | Spline Meta-Regression | Non-linear restricted cubic spline model; spline curve visualization |
| 16–19 | Publication Bias | Egger's test; trim-and-fill; PET-PEESE; funnel plot |
| 20–22 | Sensitivity Analysis | Leave-one-out meta-analysis; Baujat influence plot |
| 23–25 | Complementary Analyses | Cumulative meta-analysis; geographic distribution map; temporal trends |

---

## 📖 Citation & License

### Citation

If you use CoMeta in published research, please cite:

> [Author et al.] (*in preparation*). CoMeta: From data to report — a no-code platform for rigorous three-level meta-analysis in ecology and evolution. *Methods in Ecology and Evolution*.

### License

CoMeta is released under the [MIT License](LICENSE). The statistical engine is open source and may be adapted for new analytical modules following the extension guide in [`docs/architecture_and_data_flow.md`](docs/architecture_and_data_flow.md).

### Contributing

Bug reports, feature requests, and pull requests are welcome via the [GitHub issue tracker](https://github.com/ErickJLA/CoMeta/issues). When reporting a numerical discrepancy, please include the session JSON file and the CoMeta version string printed by Cell 1.
