# CoMeta User Manual

*A step-by-step guide for ecologists conducting meta-analysis with no programming required.*

---

## Table of Contents

| Section | Cells | Topic |
|---|---|---|
| [Introduction](#introduction) | — | What CoMeta is and how to start |
| [Phase 1: Getting Started](#phase-1-getting-started) | 1 | Environment setup |
| [Phase 2: Loading Your Data](#phase-2-loading-your-data) | 2 | Data ingestion and column mapping |
| [Phase 3: Preparing Your Data](#phase-3-preparing-your-data) *(Round 2)* | 3–4 | Filtering and cleaning |
| [Phase 4: Effect Sizes](#phase-4-effect-sizes) *(Round 2)* | 5–6 | Selection and calculation |
| [Phase 5: Overall Meta-Analysis](#phase-5-overall-meta-analysis) *(Round 3)* | 7 | Main synthesis |
| [Phase 6: Subgroup Analysis](#phase-6-subgroup-analysis) *(Round 3)* | 8–11 | Subgroups and visualization |
| [Phase 7: Meta-Regression](#phase-7-meta-regression) *(Round 4)* | 12–15 | Linear and spline models |
| [Phase 8: Publication Bias](#phase-8-publication-bias) *(Round 5)* | 16–19 | Bias diagnostics and plots |
| [Phase 9: Sensitivity Analysis](#phase-9-sensitivity-analysis) *(Round 6)* | 20–22 | Leave-one-out and Baujat |
| [Phase 10: Complementary Analyses](#phase-10-complementary-analyses) *(Round 6)* | 23–25 | Cumulative, geographic, trends |

---

## Introduction

### What is CoMeta?

CoMeta is an open-source platform for conducting rigorous ecological meta-analysis entirely through point-and-click widgets — no programming knowledge is required. It runs inside Google Colaboratory (Colab), a free browser-based environment provided by Google, so nothing needs to be installed on your computer.

At its core, CoMeta fits **three-level hierarchical random-effects models**, which correctly account for the common ecological situation where a single primary study contributes multiple, non-independent effect sizes (for example, biomass measured on multiple species from the same greenhouse experiment). The platform automates variance-covariance correction for shared control groups, robust cluster-based standard errors, and several publication bias diagnostics — methods that are state-of-the-art but have historically required custom R or Python code.

### Opening CoMeta

1. Go to [https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb](https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb) or click the **Open in Colab** badge on the GitHub repository page.
2. Sign in with a Google account when prompted (a free Gmail account is sufficient).
3. The notebook opens in your personal Colab session — you are the only person who can see and edit your copy. Nothing is shared unless you explicitly share it.

> **Tip — save your own copy first.** Go to **File → Save a copy in Drive** before doing any work. This creates a permanent copy in your Google Drive that persists across sessions.

### How CoMeta is organized

The notebook consists of **25 numbered analytical cells** (1–25) that form a linear pipeline, plus a separate block of validation cells (26 onward) intended for developers. You should run the analytical cells in order, from Cell 1 to whichever cell represents the last analysis you need.

Each cell is a self-contained unit with a title bar. To run a cell, click the **▶ play button** on the left side of the cell, or press **Shift + Enter** with the cell selected. The cell executes and displays its output (widgets, tables, or plots) directly below it.

```
Cell 1 → Cell 2 → Cell 3 → Cell 4 → Cell 5 → Cell 6 → Cell 7 → ...
Setup     Data     Filter   Clean    ES type   ES calc   Overall   ...
```

You do not need to run every cell. The complementary cells (23–25) and the visualization cells (10, 11, 13, 15, 17, 19, 21, 22, 25) are always optional. The sensitivity and publication bias cells (Cells 16–22) are recommended but can be omitted if your dataset is very small.

### Stale-result warnings

If you change a setting in an early cell (for example, apply a new filter in Cell 3), CoMeta automatically displays a yellow warning banner in any downstream cell whose results are now out of date:

> ⚠️ **Stale Results Detected** — Upstream settings for **Step 3: Global Filters Changed** have been modified. Please re-run this cell.

This is a safety feature. Whenever you see this banner, click the **Run** button inside that cell to refresh the results before interpreting them. The banner disappears once the cell has been successfully re-run.

### Session files and reproducibility

At the end of most analytical cells you will find a **📥 Download** button. This exports a complete record of every widget setting you have chosen — your analytical configuration — as a JSON file. Keep this file alongside your manuscript data: any collaborator (or a future version of yourself) can restore the exact analysis by uploading the JSON file in Cell 2 (the session restore pathway described below).

---

## Phase 1: Getting Started

### Cell 1 — Environment Setup & Core Functions

**Purpose.** Cell 1 prepares the computing environment. It checks that all required packages (NumPy, pandas, SciPy, matplotlib, and others) are installed at the correct versions, installs or updates any that are missing, and loads every statistical function and helper utility used by downstream cells. Cell 1 produces **no interactive widgets** of its own — its only visible output is the CoMeta welcome card described below.

**Prerequisites.** None — this is always the first cell to run.

#### What happens when you run Cell 1

Running Cell 1 takes 30–90 seconds the first time in a new Colab session (package installation) and only a few seconds on subsequent runs within the same session. Any installation messages are cleared automatically once the setup completes, so the output stays tidy.

If you are running CoMeta **locally** (outside Colab), the cell will instead print a warning listing any package versions that differ from the locked versions. The analysis will still proceed, but numerical results may differ slightly from a Colab run if there are major version mismatches.

#### What Cell 1 displays

After running, Cell 1 shows a single styled **CoMeta welcome card**. The card contains:

- **CoMeta v1.0** — the platform name and version.
- **"From data to report — a no-code platform for rigorous three-level meta-analysis in ecology"** — the platform description.
- A brief description of the statistical approach (VCV matrices, three-level mixed-effects models).
- An instruction reminder: *"Execute cells sequentially."*
- A citation placeholder for the associated manuscript.
- A status footer: **Environment Verified · Core engine initialised** — confirming that the environment check passed and all core functions are loaded.

No interaction is required. If the status footer reads "Environment Verified", Cell 1 is complete and you can proceed to Cell 2.

#### The figure-size preset (appears in visualization cells, not here)

Cell 1 also defines a global **📏 Preset** dropdown widget that pre-fills plot dimensions and font sizes across several visualization cells. This dropdown is **not visible in Cell 1's output** — it appears inside the style panel of the visualization cells that use it (Cells 10, 17, and 25). You do not need to do anything in Cell 1 to use the preset; simply select the desired format from the dropdown when you reach one of those cells.

Available presets:

| Preset | Width × Height | Intended use |
|---|---|---|
| Custom | (unchanged) | Adjust each plot individually |
| Cell Press 1-Col (85 mm) | 3.35 × 3.35 in | Single-column figure in Cell/Current Biology/iScience |
| Cell Press 1.5-Col (114 mm) | 4.49 × 4.00 in | 1.5-column figure in Cell Press journals |
| Cell Press Full (174 mm) | 6.85 × 5.50 in | Full-width figure in Cell Press journals |
| STAR Protocols 1-Col (134 mm) | 5.28 × 5.00 in | Single-column figure in STAR Protocols |
| STAR Protocols Full (172 mm) | 6.77 × 6.00 in | Full-width figure in STAR Protocols |
| Cell 3-Col Layout (55 mm) | 2.17 × 2.50 in | Narrow three-column layout |
| Thesis (A4 Portrait) | 6.30 × 8.00 in | Thesis chapter figures |
| Presentation (16:9) | 13.3 × 7.50 in | Slides and posters |

> **Tip.** Selecting a preset does not lock sizes permanently. Each visualization cell has its own width and height sliders that you can adjust after applying the preset. Think of the preset as a starting point, not a constraint.

> **Important.** Colab sessions disconnect after approximately 90 minutes of inactivity and after a maximum of 12 hours. When a session is disconnected, all in-memory data is lost. To continue your work after reconnecting, run **all cells from Cell 1 onward** in sequence, or load a previously exported session JSON in Cell 2 to restore your configuration automatically.

---

## Phase 2: Loading Your Data

### Cell 2 — Data Ingestion

**Purpose.** Cell 2 loads your dataset into CoMeta and maps your column names to the internal naming scheme the platform expects. It supports four ingestion pathways — Google Sheets, local file upload, built-in example datasets, and session JSON restore — and presents an interactive column-mapping interface that handles a wide range of column name conventions automatically.

**Prerequisites.** Cell 1 must have been run in the current session.

#### Choosing a data type

For file upload and Google Sheets pathways, CoMeta asks you to specify what kind of data you have before mapping columns:

| Data type | When to use | Required raw columns |
|---|---|---|
| **Raw Data — Continuous** | You have group means, standard deviations, and sample sizes for treatment and control arms | Mean, SD, and *n* for both groups |
| **Raw Data — Binary** | You have event counts (e.g., presence/absence, survived/died) for treatment and control arms | Events and non-events for both groups |
| **Pre-calculated** | Effect sizes and their variances (or standard errors) have already been computed in another program | Effect size (*yi*) and variance (*vi*) or SE |

If you are unsure, check the column headers of your spreadsheet. If you see columns like `mean_treatment`, `sd_control`, `n_exp` — choose **Continuous**. If you see `cases_treatment`, `controls_control` — choose **Binary**. If you have a column of Hedges' *g* or lnRR values already — choose **Pre-calculated**.

> **Note — Pre-calculated mode.** When using pre-calculated effect sizes, Cell 3 (Global Filtering) is automatically bypassed because its filtering logic operates on raw group-level columns that do not exist in this mode. Cell 4 (Data Cleaning) is also simplified. You will be taken directly to Cell 5 (Effect Size Selection) after Cell 2.

---

#### Pathway A — Google Sheets

Use this pathway if your data lives in a Google Sheets spreadsheet and you want changes in the sheet to be reflected immediately without re-uploading a file.

> **Note.** Google Sheets integration is only supported when running inside Google Colaboratory. It will not work in a local Jupyter environment.

**Step-by-step:**

1. Run Cell 2. A tabbed interface appears. Click the **Google Sheets** tab if it is not already selected.
2. Click **1. Connect Google Account**. A popup window will ask you to sign in to Google and grant Colab permission to read your Sheets. Follow the instructions in the popup.
3. In the **Sheet Name** text field, type the name of your Google Sheet exactly as it appears in your Google Drive (the file name, not the URL). The default is `tesis`; replace it with your sheet name.
4. Click **2. Find Worksheets**. A dropdown will populate with all the tabs (worksheets) inside that file.
5. Select the worksheet that contains your data from the dropdown.
6. Click **3. Load Data**. The data will be imported and the column-mapping interface will appear (see [Column mapping](#column-mapping) below).

---

#### Pathway B — Local file upload

Use this pathway to upload a CSV or Excel file from your computer.

**Accepted formats:** `.csv`, `.xlsx`, `.xls`

**Step-by-step:**

1. Run Cell 2. Click the **File Upload** tab.
2. Click **Select Data** and choose your file from your computer's file browser. Files up to approximately 100 MB are supported.
3. If you upload an Excel workbook with multiple sheets, a sheet-selector dropdown will appear. Choose the sheet containing your data.
4. A **Data Type** selector will appear with three radio buttons. Choose the option that matches your data (see [Choosing a data type](#choosing-a-data-type) above).
5. Click **Load Data File**. The column-mapping interface will appear (see [Column mapping](#column-mapping) below).

> **Tip — file encoding issues.** If your CSV file contains special characters (accented letters, unusual punctuation in species names), CoMeta will attempt several encodings automatically (UTF-8, Latin-1, Windows-1252). If loading fails, try re-saving the file from Excel as **CSV UTF-8 (comma delimited)** before uploading.

---

#### Pathway C — Built-in example datasets

Five datasets are pre-loaded into CoMeta for practice, benchmarking, and onboarding. These are accessible without any file upload.

**Step-by-step:**

1. Run Cell 2. Click the **Example Data** tab (or equivalent tab label).
2. Select a dataset from the dropdown.
3. Click **Load Example Data**.

| Dataset | Data type | What it contains | Typical use |
|---|---|---|---|
| **Ecology Continuous (Curtis 1998 — Plant CO₂)** | Raw continuous | 102 effect sizes from 26 woody plant studies comparing elevated vs. ambient CO₂; moderators include genus, functional group, CO₂ exposure duration, and experimental method | The canonical starting point for new CoMeta users; reproduces Curtis & Wang (1998) *Oecologia* |
| **3-Level Pre-Calculated (Konstantopoulos 2011)** | Pre-calculated | 56 effect sizes (Hedges' *g*) nested in 11 school districts; demonstrates the three-level structure | Testing the three-level model and understanding the `id` / `school_id` nesting |
| **Meta-Regression / Splines (Raudenbush 1985)** | Pre-calculated | 19 teacher-expectancy studies with a continuous moderator (weeks of contact); ideal for linear and spline meta-regression | Practising Cells 12–15 (meta-regression) |
| **Continuous (Normand 1999 — Stroke Rehab)** | Raw continuous | 9 stroke rehabilitation studies with means, SDs, and *n* | Small-sample testing; demonstrating Cell 7 with a two-level dataset |
| **Binary (BCG Vaccine — Tuberculosis)** | Raw binary | 13 BCG vaccine trials with 2×2 event tables; includes latitude as a moderator | Practising binary effect sizes (log OR, log RR) and subgroup analysis |

> **Recommendation for first-time users.** Load the **Ecology Continuous (Curtis 1998)** dataset and run through the entire pipeline before loading your own data. This gives you a reference point for what each cell's output should look like with a well-behaved ecological dataset.

---

#### Pathway D — Session JSON restore

If you (or a collaborator) previously exported a CoMeta session file (a `.json` file downloaded via a **📥 Download Settings** button), you can restore the complete analytical configuration in a fresh session.

**Step-by-step:**

1. Run Cell 2. Click the **Session Restore** tab.
2. Click the file upload button and select your `.json` session file.
3. CoMeta will re-load the original dataset (which is embedded in the JSON) and restore all widget settings from the saved session.

After a successful restore, you can re-run any downstream cell in sequence and obtain identical results to the original analysis. The session file also serves as supplementary material for a manuscript submission, providing a fully reproducible record of every analytical decision.

> **Note.** The JSON session file contains a copy of the processed data, not the raw uploaded file. If you change the raw source data and want to re-run the analysis, use Pathway A or B to reload it fresh rather than restoring from the old JSON.

---

#### Column mapping

After loading data through Pathway A or B (and for some pre-calculated files), CoMeta presents a **column-mapping interface**. Its purpose is to translate your spreadsheet's column names into the internal variable names CoMeta uses for calculations.

CoMeta recognizes a wide range of common synonyms automatically and will pre-select the most likely match for each required field. You should review every mapping and correct any mismatches before proceeding.

**How to use the mapping interface:**

- Each required internal variable is shown as a labelled row.
- Beside each row is a dropdown listing all columns detected in your file.
- CoMeta pre-selects the most likely match. If the correct column is already selected, leave it as is.
- If the automatic match is wrong, open the dropdown and choose the correct column.
- Once all required fields are mapped, click **✓ Confirm Mapping** (or equivalent) to commit the data.

##### Required columns — Raw continuous data

| Internal name | What it represents | Recognized synonyms |
|---|---|---|
| `id` | Study identifier (groups effect sizes from the same primary study) | `study`, `study_id`, `paper`, `author` |
| `xe` | Experimental group mean | `mean_e`, `mean_exp`, `x_e`, `treatment_mean` |
| `sde` | Experimental group standard deviation | `sd_e`, `sd_exp`, `sigma_e` |
| `ne` | Experimental group sample size | `n_e`, `n_exp`, `sample_e` |
| `xc` | Control group mean | `mean_c`, `mean_ctrl`, `x_c`, `control_mean` |
| `sdc` | Control group standard deviation | `sd_c`, `sd_ctrl`, `sigma_c` |
| `nc` | Control group sample size | `n_c`, `n_ctrl`, `sample_c` |

##### Required columns — Raw binary data

| Internal name | What it represents | Recognized synonyms |
|---|---|---|
| `id` | Study identifier | `study`, `study_id`, `paper`, `author` |
| `events_e` | Number of events in experimental group | `events_exp`, `cases_e`, `a`, `treatment_events` |
| `nonevents_e` | Number of non-events in experimental group | `nonevents_exp`, `b`, `treatment_nonevents` |
| `events_c` | Number of events in control group | `events_ctrl`, `cases_c`, `c`, `control_events` |
| `nonevents_c` | Number of non-events in control group | `nonevents_ctrl`, `d`, `control_nonevents` |

##### Required columns — Pre-calculated effect sizes

| Internal name | What it represents | Recognized synonyms |
|---|---|---|
| `id` | Study identifier | `study`, `study_id`, `paper`, `author` |
| `yi` | Effect size value | `effect_size`, `es`, `hedges_g`, `lnrr`, `g`, `d` |
| `variance` | Sampling variance of the effect size | `vi`, `var`, `v` |
| `se` | Standard error *(alternative to variance)* | `standard_error`, `stderr` |
| `n_total` | Total sample size *(optional but recommended)* | `n`, `sample_size`, `total_n` |

> **Note — variance vs. standard error.** You need to provide either `variance` (= SE²) or `se`, not both. If your spreadsheet contains only standard errors, map the `se` column and leave `variance` as "None"; CoMeta will square the SE internally.

##### Optional geographic columns

If your dataset contains location information for studies, CoMeta can detect it automatically for use in Cell 24 (Geographic Distribution Map). No action is required during column mapping — the columns are detected silently if they are present.

| Internal name | Recognized synonyms |
|---|---|
| `latitude` | `lat` |
| `longitude` | `lon`, `long`, `lng` |
| `country` | `nation`, `region` |

##### Moderator columns

Any column in your dataset that is not a required statistical field or the study identifier is treated as a potential **moderator** — a categorical or continuous variable that may explain variation in effect sizes. These columns do not need to be mapped explicitly; they are carried through the pipeline automatically and will appear as options in Cells 3, 8, 12, 14, and 24.

Common examples: `biome`, `ecosystem_type`, `treatment_duration_days`, `latitude`, `year_published`, `taxa`, `experimental_method`.

---

#### What Cell 2 produces

After you confirm the column mapping, Cell 2 validates the data (checking that numeric columns can be parsed, that the study identifier column is present, and that there are no critical structural issues) and writes the cleaned, mapped dataframe to the pipeline's internal memory. A preview table of the first few rows is displayed so you can verify the data loaded correctly.

**Signs of a successful load:**
- A green confirmation message appears ("✓ Data successfully loaded: *N* records from *k* studies").
- A preview table shows your data with the internal column names.
- Any moderator columns detected are listed.

**Signs of a problem:**
- A red error message ("❌ Error: column `xe` could not be coerced to numeric") — this usually means the mapped column contains text in some rows. Check for units in the cells (e.g., "5.3 g"), merged header rows, or stray commas in your spreadsheet.
- A yellow warning about missing values — this is expected if some rows lack SDs; Cell 4 will handle these.

> **Important.** Every time you change the column mapping (by returning to Cell 2 and reconfirming a different mapping), CoMeta will display a yellow stale banner in all downstream cells (Cells 3–25). This is intentional: a change in how columns are mapped can affect every downstream result. Re-run each downstream cell in sequence after any mapping change.

---

#### Tips and common mistakes

**Duplicate column names.** If your spreadsheet has two columns with the same name, CoMeta will report an error. Rename one of them before uploading.

**Study identifier as a number.** CoMeta treats the `id` column as a text label. If your study IDs are pure numbers (1, 2, 3…), they will be converted to strings ("1", "2", "3") automatically — this does not affect the analysis.

**Three-level nesting.** For a genuine three-level analysis, you need two separate identifier columns: one for the **primary study** (e.g., `paper_id`) and one for the **within-study unit** (e.g., `experiment_id` or `species_id`). Map the primary-study column to `id`. The within-study unit column should be left as a moderator column; CoMeta's model detects the nesting structure automatically from repeated values of `id`.

**Large Excel files.** Files larger than approximately 50 MB may be slow to upload over a network connection. Consider converting to CSV first, which is typically much smaller for tabular data.

**Google Sheets and special characters.** Google Sheets returns all cell values as text strings. CoMeta applies automatic numeric conversion to the required statistical columns after loading. If a column that should be numeric contains even one text value (e.g., "N/A"), that entire column will fail conversion. Clean such cells in the spreadsheet before loading.
