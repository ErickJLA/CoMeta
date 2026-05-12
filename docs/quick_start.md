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

## 8. Run the overall meta-analysis (Cell 7)

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

## 9. Compare subgroups (Cells 8 – 11)

For ecological meta-analyses, the pooled estimate is rarely the end of the story. The more interesting question is usually **does the effect differ across biologically meaningful groups?** — for example, do gymnosperms respond to elevated CO₂ differently from angiosperms, or do tropical sites respond differently from temperate ones? Subgroup analyses answer that question.

### Why this matters: a one-paragraph primer on heterogeneity

When you combine studies, they almost never report exactly the same effect. The variation among study-level effects beyond what sampling error alone would produce is called **heterogeneity**, and Cell 7's **📉 Heterogeneity** tab quantifies it:

- ***I*²** is the percentage of total variation attributable to genuine between-study differences. Higgins et al. (2003) suggest the bins *I*² < 25 % is *negligible*, 25 – 50 % *low*, 50 – 75 % *moderate*, > 75 % *substantial*.
- **τ²** is the absolute variance of the underlying true effects across studies; σ² (in the three-level model) further partitions variance within studies.
- ***Q*** is the formal test statistic; a significant *Q* says the studies are not all estimating the same true effect.

A non-trivial *I*² is a signal that the pooled estimate is an average over meaningfully different study contexts. Subgroup analysis is the natural next step: it asks whether a categorical moderator — clade, biome, experimental design, study quality — *explains* part of that heterogeneity. If it does, the pseudo-*R*² will be appreciable and you have a more nuanced story to tell than "the average effect is X".

### Configure the subgroup analysis (Cell 8)

Run **Cell 8 (⚙️ 8. Subgroup Analysis: Configuration)**. The interface has four tabs; you will mostly use **📋 Configuration** and **📊 Moderator Preview**.

1. In **📋 Configuration**, choose **Single-Factor Analysis** (one moderator) or **Two-Factor Analysis (Interaction)** (two moderators crossed) from the *Analysis Type* radio group. Stick with single-factor unless you have plenty of data — two-way designs need a healthy number of records per cell of the cross-tabulation.
2. Pick the **Moderator 1:** column from the dropdown. CoMeta auto-detects every categorical (or low-cardinality numeric) column from your dataset.
3. Open the **📊 Moderator Preview** tab and confirm that each level of the moderator has enough observations (≥ 5 is a good rule of thumb). Levels with too few records will be excluded automatically — you will see them flagged.
4. *(Optional)* Open **⚙️ Thresholds** to adjust *Min Papers:* (default 3) and *Min Observations:* (default 5). Higher thresholds yield fewer but better-estimated groups; lower thresholds yield more groups but less stable estimates. The live impact panel shows which groups will survive.
5. Back in **📋 Configuration**, click **💾 Save Configuration & Proceed**.

A green **✓ Configuration Saved Successfully** banner confirms that the configuration has been written.

### Execute the analysis (Cell 9)

Run **Cell 9 (🔬 9. Subgroup Analysis: Execution)**. No widgets — it runs automatically using the configuration from Cell 8 and the same statistical settings (CR2 cluster-robust inference, Knapp–Hartung, etc.) as Cell 7.

The result is presented in six tabs. The two you will use most are:

- **📊 Results Summary** — one row per subgroup with the pooled effect, confidence interval, prediction interval, and *p*-value, plus an omnibus *Q*_M test for whether the subgroups differ overall.
- **📉 Heterogeneity** — the variance decomposition: how much of the total heterogeneity *Q*_T is attributable to differences *between* groups (*Q*_M) versus residual heterogeneity *within* groups (*Q*_E), summarised by a pseudo-*R*² (the proportion of heterogeneity explained by the moderator).

**The number to report** is the *Q*_M *p*-value: a significant *Q*_M says the moderator explains part of the heterogeneity. Don't just count which individual subgroups are "significant" in isolation; the omnibus test is what determines whether the moderator matters.

The **📝 Publication Text** tab again contains an autogenerated *Methods* and *Results* paragraph for the subgroup analysis.

### Visualise the subgroups (Cells 10 and 11)

Two complementary figures accompany the subgroup analysis. Both are publication-ready and follow CoMeta's familiar customise-then-generate pattern.

- **Cell 10 — 📊 Forest Plot.** The classical subgroup forest plot: one row per group, with the pooled effect as a marker, the confidence interval as a horizontal line, and the prediction interval as a thinner outer line. Adjust typography, colours (the *Grayscale (Publication)* default is journal-friendly), and per-row annotations in the six tabs, then click **📊 Generate Forest Plot**.
- **Cell 11 — 🍎 Orchard Plot.** The Nakagawa et al. (2021) orchard plot: a forest-plot-style summary with the individual effect-size records drawn as semi-transparent "fruit" alongside the pooled estimate, so the reader sees both the group summary *and* the within-group spread. Click **🌳 Generate Orchard Plot** in the eight-tab interface.

Both cells export to PDF and PNG (Cell 11 also exports SVG). Both auto-generate a figure caption in their **📝 Caption** tab.

> **Which figure to use?** A typical manuscript reports both: the forest plot in the main text for the headline subgroup contrast, and the orchard plot — either in the main text or as a supplement — to show the underlying record-level distribution. They are complementary, not redundant.

### When to skip subgroups

If your *I*² in Cell 7 is below ~25 %, the heterogeneity is negligible and there is little to explain — a subgroup analysis adds little. Likewise, if no biologically meaningful categorical moderator was recorded, the right tool is the linear or spline meta-regression on a continuous moderator (next section, and Cells 14 – 15).

---

## 10. Test continuous predictors with meta-regression (Cells 12 – 13)

Where subgroup analysis (Section 9) asks *does the effect differ between categories?*, meta-regression asks the parallel question for continuous variables: **does the effect change systematically along a numerical gradient?** Common examples in ecology are latitude, elevation, mean annual temperature, exposure duration, body mass, soil moisture, or year of publication. If your dataset contains a moderator like these and you suspect it drives part of the across-study variation in your effect size, this is the cell to use.

### Why this matters

Like a subgroup analysis, meta-regression is a tool for *explaining* the heterogeneity you saw in Cell 7's **📉 Heterogeneity** tab. A high *I*² is rarely a defect — it is a hint that studies disagree because they were conducted under different conditions. Linear meta-regression formally tests whether one of those conditions (the continuous moderator you choose) tracks the differences in the reported effect, and reports the pseudo-*R*² as the proportion of heterogeneity the moderator accounts for. A significant slope means you have a more nuanced story than "the average effect is X" — you have a *rate of change* of the effect with the moderator.

### Configure and run (Cell 12)

Run **Cell 12 (📈 12. Meta-Regression: Configuration & Execution)**. The interface is minimal:

1. From the **Moderator:** dropdown, choose your continuous predictor. CoMeta automatically lists every numeric (or numeric-coercible) column in the dataset.
2. Click **▶ Run Meta-Regression**.

The model uses the same statistical machinery as Cell 7 — three-level REML, CR2 cluster-robust inference, Knapp–Hartung where enabled — so the result is directly comparable to the pooled estimate.

### Read the result

Five tabs are populated. The two you will rely on most are:

- **📊 Results** — the slope **β₁** with its confidence interval and *p*-value, displayed as a large gradient card. A significant slope means the moderator explains variation in the effect size. CoMeta also writes a plain-language interpretation paragraph (e.g., *"For every 1-unit increase in latitude, the effect size decreases by 0.0123 units. This relationship is statistically significant."*) and a coefficient table.
- **🔍 Diagnostics** — the **residual *I*²** (how much heterogeneity remains unexplained *after* including the moderator), the **pseudo-*R*²** (how much the moderator explained), and the **Cook's *D*** influence diagnostics that flag records with outsized leverage on the slope. Inspect these before reporting the slope.

The **📝 Publication Text** tab again writes adaptive *Methods* and *Results* paragraphs ready for the manuscript.

> **One moderator at a time.** CoMeta's meta-regression is univariate by design — re-run Cell 12 once per candidate moderator. The convenience makes it tempting to try many moderators in succession; if you do, be conservative about reporting and discuss the multiple-testing issue explicitly.

### Visualise (Cell 13)

Run **Cell 13 (📈 13. Meta-Regression: Visualization)**. The classical companion figure is a **bubble plot**:

- Each effect-size record is drawn at its (moderator, effect-size) coordinates.
- The **bubble area is proportional to the inverse-variance weight**, so high-precision studies visually dominate — just as they statistically dominate the fit.
- The fitted regression line is overlaid, optionally with a 95 % confidence band.
- The optional **Color By:** dropdown lets you condition bubble colours on a *categorical* moderator (e.g., functional group), which is useful for showing that the continuous trend holds — or not — across qualitative categories.

Customise across six tabs (🎨 Style, ⚫ Points, 📈 Regression, 💾 Layout/Export, ✏️ Labels, 📝 Caption), then click **Generate Plot**. The figure is exported as PDF and PNG, and the **📝 Caption** tab provides a publication-ready figure legend.

### When to skip linear meta-regression

- **Non-linear relationships** (threshold, plateau, dose-response, saturation) are not captured by a straight line; use the **spline meta-regression (Cells 14 – 15)** instead. If your bubble plot in Cell 13 shows obvious curvature, the spline cells are the right next step.
- **Categorical moderators** belong in the **subgroup analysis (Section 9)**, not here.
- **Very small datasets** (~10 studies or fewer) yield unstable slopes; in that regime, report only the pooled estimate from Cell 7.

---

## 11. Other optional analyses

The remaining cells extend the analysis further. Run only those relevant to your manuscript.

| Cells | Module | When to run |
|---|---|---|
| **14 – 15** | **Spline meta-regression** | You have a continuous moderator and expect a non-linear relationship (threshold, dose-response, saturation). |
| **16 – 19** | **Publication-bias diagnostics** | You should run all four (Egger, trim-and-fill, PET-PEESE, funnel plot) for any manuscript reporting a meta-analysis. |
| **20 – 22** | **Sensitivity analysis** | Strongly recommended — leave-one-out and Baujat influence plots demonstrate that the pooled estimate is robust to any single study. |
| **23, 25** | **Cumulative meta-analysis** | Optional. Shows the trajectory of the pooled estimate over publication time. |
| **24** | **Geographic map** | If your dataset has coordinates or country labels (mapped in Cell 2), this produces the geographic-representativeness figure. |

Each of these cells follows the same pattern: run, configure widgets, click the corresponding *Run* or *Generate* button, inspect tabs, optionally export.

---

## 12. Export your session

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

**For most manuscripts:** the minimum reportable pipeline is **Cells 1 – 7** for the pooled estimate, **Cells 16 – 19** for publication-bias diagnostics, and **Cells 20 – 22** for the sensitivity analysis. That covers the core numerical claims any reviewer will look for.

**When heterogeneity is non-trivial** (the typical ecological case): use the **subgroup analysis (Cells 8 – 11)** for categorical moderators or the **linear meta-regression (Cells 12 – 13)** for continuous moderators. Both turn a flat "average effect" into a substantive ecological story by explaining *why* studies disagree. For non-linear relationships along a continuous gradient, the **spline meta-regression (Cells 14 – 15)** is the right tool.

**For additional descriptive figures:** the cumulative analysis (Cells 23, 25) and the geographic map (Cell 24).

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
