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

### A two-minute primer on Google Colab

Google Colab is the cloud environment that runs CoMeta. If you have never used it, you only need to know three things:

- **A notebook is a vertical stack of cells.** Each cell is a self-contained block. You scroll down through the notebook the way you would scroll through a long document.
- **To run a cell, click its ▶ button.** When you hover over the left-hand edge of a cell, a circular play button appears. Click it — or, with the cell selected, press **Shift + Enter** — and the cell executes. A spinning circle and a small timer indicate progress; the spinner disappears and the cell's output appears below it when it finishes.
- **Cells must be run in order, top to bottom.** Each cell of CoMeta depends on the output of the cells above it. On your first pass, run every cell in sequence. If you later go back and change something in an earlier cell, CoMeta will display an **orange staleness banner** on every downstream cell that now needs to be re-run; press ▶ on each flagged cell again, in order, to refresh the analysis.

Colab also disconnects idle sessions after a few hours. If your widgets become unresponsive, click **Connect** in the upper-right of the Colab window, re-run Cell 1, and continue from where you left off. To save your work between sessions, immediately after opening the notebook choose **File → Save a copy in Drive** — your edits then auto-save to Google Drive just like a Google Doc.

### Universal cell pattern in CoMeta

**Click the ▶ Run button on the cell → configure the widgets → click the cell's confirmation button (e.g., *Confirm Mapping*, *Save Configuration*, *Run Analysis*) → inspect the result → move to the next cell.**

That is the entire interaction model. Every cell follows it.

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

---

## 3. Load your data (Cell 2)

**The easiest workflow is Google Sheets.** Keep your dataset in a Google Sheets spreadsheet under the same Google account you use to open Colab. CoMeta then reads the worksheet directly — no file uploads, no version-mismatch confusion, and the data update automatically the next time you re-run the cell.

### Name your columns so CoMeta recognises them

If you use the column names below, CoMeta will detect every column automatically and the mapping step will pre-fill itself with no manual intervention.

**Required — for continuous data (means, SDs, sample sizes):**

| Column name | Meaning |
|---|---|
| `id` | Study identifier (paper, author, or any label shared by all effect-size rows from the same study). |
| `xe` | Mean of the experimental / treatment group. |
| `sde` | Standard deviation of the experimental group. |
| `ne` | Sample size of the experimental group. |
| `xc` | Mean of the control group. |
| `sdc` | Standard deviation of the control group. |
| `nc` | Sample size of the control group. |

**Required — for binary data (2 × 2 contingency-table counts):**

| Column name | Meaning |
|---|---|
| `id` | Study identifier. |
| `events_e` | Events (e.g., deaths, successes) in the treatment group. |
| `nonevents_e` | Non-events in the treatment group. |
| `events_c` | Events in the control group. |
| `nonevents_c` | Non-events in the control group. |

**Required — for pre-calculated effect sizes:**

| Column name | Meaning |
|---|---|
| `id` | Study identifier. |
| `yi` | The effect size (e.g., Hedges' *g*, lnRR). |
| `variance` *or* `se` | The sampling variance, **or** the standard error (CoMeta accepts either). |
| `n_total` | *(optional)* Total sample size — helpful for some publication-bias diagnostics. |

**Optional — for the geographic-distribution map (Cell 24):**

| Column name | Meaning |
|---|---|
| `latitude` | Decimal latitude (−90 to 90). |
| `longitude` | Decimal longitude (−180 to 180). |
| `country` | Country or region name. |

**Any other column** in the spreadsheet — taxonomic clade, biome, year, exposure duration, anything — is automatically retained as a candidate *moderator* for the subgroup analyses (Cells 8 – 11) and meta-regressions (Cells 12 – 15). Just give it a clear, machine-readable name (no spaces, no special characters).

> **Don't worry if your existing spreadsheet uses different names.** CoMeta also recognises a wide range of synonyms (`mean_e`, `mean_exp`, `treatment_mean` for `xe`; `study`, `paper`, `author` for `id`; etc.) and will pre-fill its best guesses. You only need to correct the dropdowns where CoMeta got it wrong. The internal names above are simply the most reliable choice.

### Run the cell

Run **Cell 2 (⚙️ 2. Data Ingestion)**, then follow these steps in the **Google Sheets** tab:

1. Click **1. Connect Google Account** and grant access in the popup. The button turns green.
2. Type the *exact* name of your Google Sheets file into the **Sheet Name:** box and click **2. Find Worksheets**.
3. Pick the relevant worksheet from the dropdown and click **3. Load Data**.
4. In the **Step 2** panel that opens below, select the **Data Type:** matching your dataset — *Raw Data — Continuous*, *Raw Data — Binary*, or *Pre-calculated*. Verify the auto-filled column mapping (it will be correct if you used the recommended names).
5. *(Optional)* In the **🌍 Geographic Columns** section, map *Latitude:*, *Longitude:*, and / or *Country / Region:* to enable the map in Cell 24.
6. Click **✓ Confirm Mapping & Finalize Data**.

A green **✅ Data Ready** banner appears with a moderator summary table.

> If your data are in a local `.csv` / `.xlsx` file, in a previously exported CoMeta session, or you want to test CoMeta first on a canonical dataset, Cell 2 offers three additional tabs — **Upload Excel/CSV**, **Restore Session**, and **Built-in Examples**. See [`user_guide_and_data_formats.md`](user_guide_and_data_formats.md) §2 for those workflows; the rest of this quick-start guide applies unchanged.

### Tips and common pitfalls

- **Keep one row per effect-size record.** When a single study contributes several effect sizes (e.g., multiple treatments, multiple time points), give each its own row and use the same `id` value for all of them — CoMeta handles the within-study nesting automatically.
- **Avoid duplicate column names.** Excel and Google Sheets occasionally end up with two columns called *"x"* after copy-paste; CoMeta will reject the load with an explicit error. Rename them in the source.
- **No `n/a`, `N.D.`, or `-` in numeric columns.** Leave those cells empty instead, or CoMeta will count them as non-numeric and drop the rows. Truly missing standard deviations are fine — Cell 4 will offer imputation strategies.
- **Sample sizes must be ≥ 1.** Rows with `ne = 0` or `nc = 0` are dropped automatically with an explicit reason in the *Removed Data* tab.

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
| **📝 Publication Text** | **Auto-generated, manuscript-ready *Methods* and *Results* paragraphs** — see below. |
| **💾 Export** | **📥 Download Settings JSON** here — do this now to safeguard against Colab session timeouts. |

If you change any setting in **⚙️ Settings**, click **Re-Run Analysis** to refit.

### The autogenerated Methods and Results text

The **📝 Publication Text** tab is one of CoMeta's most useful outputs. Every time the model is fitted, CoMeta writes — in plain prose — a *Materials and Methods* paragraph and a *Results* paragraph describing what it just did, formatted to journal conventions (e.g., *g* = 0.42, 95 % CI [0.18, 0.66], *p* = .003). The text is **adaptive**: it changes automatically when you change the configuration. It correctly reflects:

- whether the AIC selected the two-level or three-level model (including the *"τ²_within collapsed to zero, reverted to two-level"* fallback when applicable);
- the τ² estimator you chose (REML / DL / ML);
- whether the Knapp–Hartung adjustment was applied;
- the SD imputation strategy used in Cell 4 (if any);
- the shared-control variance–covariance correction from Cell 6 (if any);
- the Cohen (1988) interpretation bin for the effect size and the Higgins et al. (2003) interpretation bin for *I*².

You can copy the text directly into your manuscript draft. The downstream cells (subgroup analysis, meta-regression, publication-bias diagnostics, sensitivity analysis) each produce their own *Publication Text* tab in the same format, so by the time you finish the pipeline you have a draft *Methods* section and a draft *Results* section assembled from cell-level paragraphs — every numerical claim consistent with the figures and tables in the same notebook.

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
