# CoMeta — Quick-Start Guide

*A 10-minute read that takes you from opening the notebook to a manuscript-ready meta-analysis. For full technical detail, see [`user_guide_and_data_formats.md`](user_guide_and_data_formats.md).*

---

## What CoMeta is

A no-code, browser-based platform for rigorous three-level meta-analysis in ecology and conservation biology. CoMeta runs as a Google Colaboratory notebook. You interact only with widgets — never with code.

---

## What you need

- A Google account.
- A modern browser.
- An internet connection.
- A dataset in `.csv` or `.xlsx` format (or use one of the built-in examples).

You do **not** need Python, R, or any local installation.

---

## The 30-second tour

CoMeta is one notebook (`CoMeta_1.ipynb`) made up of numbered *cells*. You execute them top-to-bottom, once each. Every cell from Cell 2 onward presents a widget interface — dropdowns, buttons, sliders — that you configure and then confirm with a button click. The output of each cell flows automatically into the next.

**Universal pattern:** click the **▶ Run** button on the cell, configure the widgets, click the cell's confirmation button (e.g., *Confirm Mapping*, *Save Configuration*, *Run Analysis*), inspect the result, move to the next cell.

---

## 1. Open the notebook

Click the *Open in Colab* badge in the project README, or paste this into your browser:

```
https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb
```

Immediately save your own working copy: **File → Save a copy in Drive**.

---

## 2. Initialise the environment (Cell 1)

Click **▶ Run** on **Cell 1 (⚙️ 1. Environment Setup & Core Functions)**. Wait 30 – 90 seconds for the green **🟢 Environment Verified — Core engine initialised** banner.

That's the only cell that has no widget interface; it just prepares the runtime.

---

## 3. Load your data (Cell 2)

Run **Cell 2 (⚙️ 2. Data Ingestion)**. You will see four tabs at the top:

| Tab | When to use |
|---|---|
| **Google Sheets** | Your data is in a Google Sheets spreadsheet. |
| **Upload Excel/CSV** | You have a local `.csv` or `.xlsx` file. |
| **Restore Session** | You are reproducing a previous analysis from a saved `.json` file. |
| **Built-in Examples** | You want to try CoMeta with a canonical dataset (recommended for first use). |

**First-time users — try a built-in example.** Click *Built-in Examples*, choose **Ecology Continuous (Curtis 1998 — Plant CO₂)**, click **📥 Load Example Dataset**, and skip ahead to Cell 3 — built-in datasets are pre-mapped.

**Loading your own data:**

1. Click *Upload Excel/CSV*, choose your file, and click **Load Data File** (for multi-sheet Excel, pick the worksheet first).
2. Below, select the **Data Type:** that matches your dataset:
   - **Raw Data — Continuous (Means/SDs/N)** — you have *x̄*, SD, and *n* for treatment and control.
   - **Raw Data — Binary (Events/Non-Events)** — you have 2 × 2 contingency-table counts.
   - **Pre-calculated (Effect/SE)** — you have already computed effect sizes and their variances.
3. CoMeta will auto-fill the column-mapping dropdowns from a synonym table; correct any wrong guesses.
4. Optionally map *Latitude:*, *Longitude:*, and *Country / Region:* in the **🌍 Geographic Columns** section for the map in Cell 24.
5. Click **✓ Confirm Mapping & Finalize Data**. A green **✅ Data Ready** banner with a moderator summary table appears.

> **Tip.** If CoMeta rejects your data, the error message names the offending column. Common causes are non-numeric values in a numeric field (e.g., `n/a`) and duplicate column names. Fix in the source file and re-upload.

---

## 4. Filter your data (Cell 3)

Run **Cell 3 (⚙️ 3. Global Filtering)**. If you imported pre-calculated effect sizes, this cell is skipped automatically — go to Cell 4.

Otherwise, the cell offers a single optional filter:

- Leave *Filter Variable:* at **None** to keep the entire dataset.
- Or pick a categorical column (e.g., taxonomic clade), uncheck the values you want to **exclude** from the whole analysis, and click **▶ Save Configuration**.

Used for exclusion criteria common to every analysis — e.g., "restrict to angiosperms". Subgroup *contrasts* (e.g., comparing angiosperms vs. gymnosperms) come later in Cell 8.

---

## 5. Clean the data (Cell 4)

Run **Cell 4 (⚙️ 4. Data Cleaning & Pre-processing)**.

- If your dataset has **no missing or zero SDs**, the cell runs automatically and shows a green **✅ Data Successfully Prepared** card with two tabs (*Data Summary* and *Removed Data*). Move on.
- If it has **missing or zero SDs**, a yellow **⚠️ Variance Data Action Required** panel lists the issue counts. Choose imputation strategies from the two dropdowns:
  - **Missing SDs:** default is *Impute using median CV from available data* (the ecological convention).
  - **Zero SDs:** default is *Replace with smallest nonzero SD in dataset*.
- Click **▶ Process Data**.

Inspect the **🗑️ Removed Data** tab — these rows will not appear in the model, and you'll need to explain them in the manuscript's *Methods*.

---

## 6. Choose an effect size (Cell 5)

Run **Cell 5 (🔬 5. Effect Size Selection & Diagnostics)**.

CoMeta inspects your data and recommends one of: **lnRR**, **Hedges' g**, or **log OR / log RR**. The recommendation appears as a coloured banner on the **💡 Recommendation** tab.

- For most ecological datasets, accept the recommendation.
- If you have a strong reason to use a different metric (journal convention, prior analyses), pick it from the *Select Type:* radio group.
- The button changes to red ❌ *Invalid Selection* if the metric is incompatible with your data type (e.g., log OR on continuous data).

Click **✓ Confirm Selection**.

> **Curious why?** The **📊 Data Patterns** and **🧠 Decision Logic** tabs show what CoMeta saw in your data and how the six scoring rules (R1 – R6) reached the recommendation.

---

## 7. Compute the effect sizes (Cell 6)

Run **Cell 6 (🧮 6. Effect Size Calculation)**. No widgets — it just runs.

Cell 6 computes the per-record effect size and variance, applies any metric-specific cleaning (e.g., the Haldane–Anscombe correction for zero-cell binary studies), constructs the variance–covariance matrices for shared control groups, and renders five diagnostic tabs.

**What to check before moving on:**
- **📊 Summary** — the *Observations*, *Studies*, and *Removed* counts look sensible.
- **🗑️ Removed Data** — every row removed at this stage has a defensible reason.
- **📉 Diagnostics** — the *Outlier Analysis* table flags candidates for inspection; check them in your source data for typos.

---

## 8. Fit the pooled model (Cell 7) — the central cell

Run **Cell 7 (📊 7. Overall Meta-Analysis)**. This is the headline result of your meta-analysis.

The cell fits three candidate models (fixed-effect, two-level random-effects, three-level) and reports the **AIC winner** in the **📊 Primary Result** tab as a single number — the pooled effect size — with its confidence interval, prediction interval, and *p*-value.

**The six tabs:**

| Tab | What to look for |
|---|---|
| **📊 Primary Result** | The pooled estimate. This is the number you report. |
| **📉 Heterogeneity** | *I*², *Q*, τ², σ² with profile-likelihood CIs. |
| **⚖️ Model Selection** | Side-by-side comparison of all three candidate models. Verify the AIC winner is the three-level model in three-level datasets. |
| **⚙️ Settings** | Six widgets to change α, model selection, τ² estimator, Knapp–Hartung, distribution, etc. Defaults are appropriate for most analyses. |
| **📝 Publication Text** | Manuscript-ready *Methods* and *Results* paragraphs. Copy these directly. |
| **💾 Export** | **📥 Download Settings JSON** here — do this now to safeguard against Colab session timeouts. |

If you change any setting in **⚙️ Settings**, click **Re-Run Analysis** to refit.

> **You can stop here** if all you want is the pooled estimate and the autogenerated text. Everything below is optional.

---

## 9. Optional analyses

The remaining cells extend the headline analysis. Run only those relevant to your manuscript.

| Cells | Module | When to run |
|---|---|---|
| **8 – 11** | **Subgroup analysis + Forest/Orchard plots** | You have a categorical moderator (e.g., taxonomic clade, biome) whose levels you want to contrast. |
| **12 – 13** | **Linear meta-regression** | You have a continuous moderator (e.g., latitude, year) and expect a monotone relationship. |
| **14 – 15** | **Spline meta-regression** | You have a continuous moderator and expect a non-linear relationship (threshold, dose-response). |
| **16 – 19** | **Publication-bias diagnostics** | You should run all four (Egger, trim-and-fill, PET-PEESE, funnel plot) for any manuscript reporting a meta-analysis. |
| **20 – 22** | **Sensitivity analysis** | Strongly recommended — leave-one-out and Baujat influence plots demonstrate that the pooled estimate is robust to any single study. |
| **23, 25** | **Cumulative meta-analysis** | Optional. Shows the trajectory of the pooled estimate over publication time. |
| **24** | **Geographic map** | If your dataset has coordinates or country labels (mapped in Cell 2), this produces the geographic-representativeness figure. |

Each of these cells follows the same pattern: run, configure widgets, click the corresponding *Run* or *Generate* button, inspect tabs, optionally export.

---

## 10. Export your session

In **Cell 7's 💾 Export tab**, click **📥 Download Settings JSON**. The downloaded `analysis_settings.json` file:

- captures every decision you made through the widget interface;
- can be re-uploaded via *Cell 2 → Restore Session* to reproduce the analysis verbatim in a fresh Colab runtime;
- is the appropriate file to deposit as supplementary material alongside a manuscript.

Also click **📥 Download Excel Audit Report** for a full multi-sheet audit workbook.

---

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Red error on Cell 1 | Transient network failure during dependency install | Colab menu → *Runtime → Restart session*, then re-run Cell 1 |
| "Duplicate column names" | Two columns in your source file share a name | Rename in the source spreadsheet and re-upload |
| Widgets greyed out / unresponsive | Colab session disconnected | Click **Connect** in the upper-right, then re-run Cell 1 |
| Orange staleness banner on a cell | An upstream cell was modified | Re-run the flagged cell |
| "Only N group(s) meet criteria" in Cell 8 | Threshold sliders too high | Lower *Min Papers:* or *Min Observations:* in the *⚙️ Thresholds* tab |
| Spline curve "whips" at the edges | Sparse data at the moderator's tail | See the *⚠️ Sparse Data at Boundaries* warning in Cell 14's *🔍 Diagnostics* tab; interpret the tails with caution |

---

## What to do next

**For most manuscripts:** the minimum reportable pipeline is **Cells 1 – 7** for the pooled estimate plus **Cells 16 – 19** for publication-bias diagnostics and **Cells 20 – 22** for the sensitivity analysis. That covers the four numerical claims that reviewers will look for.

**For richer analyses:** add the subgroup pipeline (Cells 8 – 11), the linear or spline meta-regression (Cells 12 – 15), or both. Add the cumulative analysis (Cells 23, 25) and the geographic map (Cell 24) for additional descriptive figures.

**For full detail on every option, every widget, every formula, and the underlying statistical methods**, see the comprehensive [`user_guide_and_data_formats.md`](user_guide_and_data_formats.md). Section numbers in that guide correspond to the cell groupings used above:

| Cells | User-guide section |
|---|---|
| 1 | §1 Getting Started |
| 2 | §2 Data Ingestion and Supported Data Formats |
| 3 | §3 Global Filtering |
| 4 | §4 Data Cleaning and Pre-processing |
| 5 | §5 Effect Size Selection and Diagnostics |
| 6 | §6 Effect Size Calculation |
| 7 | §7 Overall Meta-Analysis |
| 8 – 9 | §§8 – 9 Subgroup Analysis |
| 10 – 11 | §10 Forest and Orchard Plots |
| 12 – 13 | §11 Linear Meta-Regression |
| 14 – 15 | §12 Non-Linear Spline Meta-Regression |
| 16 – 19 | §13 Publication-Bias Diagnostics |
| 20 – 22 | §14 Sensitivity Analysis |
| 23 – 25 | §15 Complementary Analyses |

---

*Happy meta-analysing. When in doubt, the default settings are the defensible choice.*
