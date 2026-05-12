# CoMeta — User Guide and Data Formats

*A reference manual for ecologists and conservation researchers conducting three-level meta-analyses through the CoMeta widget interface.*

---

## Section 1. Getting Started

CoMeta is distributed as a single Google Colaboratory notebook, `CoMeta_1.ipynb`, and is operated entirely through a sequence of widget interfaces. This section describes how to open the notebook, initialise the runtime environment, and navigate the notebook's cell-based workflow. Subsequent sections of this guide assume that the environment has been initialised as described below.

### 1.1 Requirements

To run CoMeta, the user requires:

- A Google account, used solely for authenticating with Google Colaboratory.
- A current version of a standard web browser (Chrome, Firefox, Safari, or Edge).
- An active internet connection. All computation is executed on Google's remote runtime; local hardware specifications are therefore not a limiting factor.

No local installation of Python, R, or any scientific computing environment is required. All dependencies are resolved at runtime by Cell 1 (Section 1.3).

### 1.2 Opening the notebook in Google Colab

The notebook may be opened by either of the following routes:

**Option A.** Click the *Open in Colab* badge displayed in the project README on GitHub.

**Option B.** Navigate directly to the following URL:

```
https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb
```

Both routes load the canonical version of `CoMeta_1.ipynb` into the Google Colab editor.

> **Saving a working copy.** The notebook opened from GitHub is a read-only view. To preserve widget selections, uploaded datasets, and computed results across sessions, the user should select **File → Save a copy in Drive** from the Colab menu bar. This creates a private, editable copy in the user's Google Drive (under the `Colab Notebooks` folder) and redirects the active session to it. Subsequent edits are then auto-saved to Drive. A local copy may also be retained at any time via **File → Download → Download .ipynb**.

The notebook is organised as a linear sequence of 38 *cells*, each corresponding to one self-contained step of the analytical pipeline. Cells are numbered and titled in the order in which they should be executed, e.g.:

- **⚙️ 1. Environment Setup & Core Functions**
- **⚙️ 2. Data Ingestion**
- **⚙️ 3. Global Filtering**

The remaining cells implement data cleaning, effect size calculation, model fitting, subgroup and meta-regression analyses, publication bias diagnostics, sensitivity analyses, and report generation, in that order. Each cell exposes its functionality through a dedicated widget interface; no inspection or modification of the underlying source code is required for any analytical task.

### 1.3 Initialising the environment (Cell 1)

Cell 1, titled **⚙️ 1. Environment Setup & Core Functions**, prepares the Colab runtime for analysis. It verifies that the required versions of CoMeta's scientific dependencies (NumPy, pandas, SciPy, matplotlib, ipywidgets, statsmodels, patsy, and related packages) are installed, installs any that are missing or version-mismatched, and loads CoMeta's statistical engine into memory. Cell 1 is the only cell in the notebook that does not present a widget interface, and is executed once per Colab session.

To execute Cell 1:

1. Position the cursor over the left-hand margin of the cell. A circular **▶ Run** button appears.
2. Click the button. Alternatively, with the cell selected, press **Shift + Enter**.

Initial execution typically completes in 30–90 seconds. During execution, a spinner is displayed in place of the run button, and an elapsed-time counter is shown alongside the cell. On successful completion, the cell output is replaced with the following confirmation banner:

> 🟢 **Environment Verified** — *Core engine initialised*

Display of this banner indicates that the statistical engine and widget framework are loaded and that the user may proceed to Cell 2.

> **Recovering from initialisation errors.** If Cell 1 returns a Python traceback or other error in place of the confirmation banner — most commonly the result of an intermittent network failure during package installation — the runtime should be reset via **Runtime → Restart session** (or **Runtime → Restart runtime**) from the Colab menu bar, after which Cell 1 should be re-executed. Reopening the notebook is not necessary.

### 1.4 Executing subsequent cells

From Cell 2 onward, the operational pattern is uniform across the notebook:

1. Execute the cell by clicking its **▶ Run** button (or pressing **Shift + Enter**).
2. The associated widget interface is rendered immediately below the cell. Interfaces consist of standard controls — dropdowns, radio buttons, checkboxes, sliders, file-upload dialogs, and labelled action buttons such as *Confirm*, *Apply Filters*, *Calculate Effect Sizes*, and *Fit Model*.
3. Configure the desired options. Settings may be changed freely before triggering an action; no computation is performed until the corresponding action button is pressed.
4. Inspect the cell's output (tables, figures, diagnostic text, or generated report material) and proceed to the next cell.

> **Cells must be executed in order.** CoMeta implements a strictly linear pipeline: each cell consumes objects produced by upstream cells. On a first pass, all cells should therefore be executed from top to bottom. When an upstream cell is subsequently re-executed (for example, to re-import a dataset in Cell 2 or change an imputation strategy in Cell 4), CoMeta displays a *staleness banner* on every downstream cell whose results are no longer consistent with the new upstream configuration. The user re-executes each flagged cell in order, and the banners are cleared as the corresponding outputs are refreshed.

> **Colab session lifetime.** Google Colab terminates idle runtimes after a period of inactivity (typically two to three hours), and may also disconnect long-running sessions. When this occurs, the widget interfaces become unresponsive but the notebook itself is preserved in Google Drive. The session is restored by clicking **Connect** in the upper-right of the Colab interface and re-executing Cell 1; analyses can then be reproduced from this point. CoMeta additionally provides a session export facility (described in a later section) that serialises the complete analytical configuration to a JSON file, enabling exact one-click restoration of an analysis in a fresh runtime.

### 1.5 Summary

Launching CoMeta consists of three steps: opening `CoMeta_1.ipynb` in Google Colab, optionally saving a copy of the notebook to Google Drive, and executing Cell 1 to initialise the environment. Once the *Environment Verified* banner is displayed, the user may proceed to Cell 2 (Data Ingestion), which is described in Section 2.

---

## Section 2. Data Ingestion and Supported Data Formats

Cell 2, titled **⚙️ 2. Data Ingestion**, is the entry point for the user's dataset. It provides four mutually exclusive ingestion pathways, performs an automated column-mapping step that translates the user's column names into CoMeta's internal schema, and validates the resulting table before passing it to the downstream pipeline. This section first describes the four ingestion pathways and the column-mapping interface (§2.1–§2.3), and then documents the data formats that CoMeta expects in detail (§2.4–§2.6).

After Cell 1 has rendered the *Environment Verified* banner, the user clicks the **▶ Run** button on Cell 2. The cell renders a header reading **Step 1: Import Data Source**, followed by a tabbed interface containing the four ingestion pathways described below.

### 2.1 Ingestion pathways

The four tabs at the top of the Cell 2 interface are labelled, from left to right:

| Tab | Label | Use case |
|---|---|---|
| 1 | **Google Sheets** | Load data directly from a Google Sheets spreadsheet to which the user's Google account has access. |
| 2 | **Upload Excel/CSV** | Upload a local `.csv`, `.xlsx`, or `.xls` file from the user's computer. |
| 3 | **Restore Session** | Reload a previously exported CoMeta session (`analysis_settings.json`) for exact reproduction of an earlier analysis. |
| 4 | **Built-in Examples** | Load one of five pre-packaged example datasets that ship with CoMeta. |

Only one tab is used per session. The chosen pathway populates an internal DataFrame that subsequent cells consume; switching tabs after data have been loaded overwrites the previous selection.

#### 2.1.1 Google Sheets

The Google Sheets pathway authenticates the user against Google's API and reads a worksheet directly from Google Drive. It comprises three sequential buttons:

1. **1. Connect Google Account.** Opens a Google authentication pop-up. Once the user grants access, the button switches to "Connected ✓" and a green confirmation banner is displayed.
2. **2. Find Worksheets.** Resolves the spreadsheet whose title is entered in the *Sheet Name:* text field. On success, the *Worksheet:* dropdown is populated with the titles of all sheets in the spreadsheet.
3. **3. Load Data.** Downloads the selected worksheet, drops fully empty rows and columns, coerces predominantly numeric columns to numeric type (identifier-like columns such as `id`, `study`, `paper`, and `author` are protected from coercion), and stores the resulting table in memory.

A green banner stating "**Data successfully loaded!**" with row and column counts indicates that the pathway has completed. The interface for Step 2 (Section 2.3) then appears below.

#### 2.1.2 Upload Excel/CSV

The local-file pathway accepts a single file via the **Select Data** uploader (filtered to `.csv`, `.xlsx`, and `.xls`). Once a file has been selected:

- For CSV files, the parser attempts UTF-8 encoding first and falls back, in order, to Latin-1, Windows-1252, and UTF-8 with BOM.
- For Excel workbooks with more than one sheet, a *Select Sheet:* dropdown appears, allowing the user to choose the target worksheet.

The **Load Data File** button parses the selected file. Files with duplicate column names, no data rows, or unreadable encodings are rejected with an explicit error message. As with the Google Sheets pathway, success is indicated by the green confirmation banner and the appearance of the Step 2 interface.

#### 2.1.3 Restore Session

The session-restoration pathway accepts a previously exported `analysis_settings.json` file via the **Load Settings JSON** uploader. The file is parsed, the original analytical configuration is hydrated into the global `ANALYSIS_CONFIG` dictionary, and a session summary card is rendered, listing the export date, the dimensions of the hydrated dataset, the original effect size metric, the τ² estimation method, the significance level α, the distribution type, and any subgroup or moderator configuration. When this pathway is used, the user does not interact with the Step 2 column-mapping interface; instead, the remaining notebook cells are executed sequentially, and each will automatically restore its widget state from the loaded configuration. Session export is described in a later section of this guide.

#### 2.1.4 Built-in Examples

The built-in examples pathway loads one of five canonical meta-analysis datasets shipped with the notebook. The dataset is selected from the *Select Data:* dropdown and loaded with the **📥 Load Example Dataset** button. The available datasets are:

| Dataset label | Source | Data type |
|---|---|---|
| Binary (BCG Vaccine — Tuberculosis) | Colditz et al. (BCG trials) | Raw binary |
| Continuous (Normand 1999 — Stroke Rehab) | Normand (1999) | Raw continuous |
| 3-Level Pre-Calculated (Konstantopoulos 2011) | Konstantopoulos (2011) | Pre-calculated |
| Meta-Regression / Splines (Raudenbush 1985) | Raudenbush (1985) | Pre-calculated |
| Ecology Continuous (Curtis 1998 — Plant CO₂) | Curtis & Wang (1998) | Raw continuous |

Built-in datasets are pre-mapped to CoMeta's internal schema; the Step 2 column-mapping interface (Section 2.3) is therefore skipped automatically, and the user may proceed directly to Cell 3 (Global Filtering) or Cell 4 (Data Cleaning).

### 2.2 What CoMeta does to the loaded table before mapping

Regardless of the ingestion pathway, CoMeta performs the following automatic steps on the loaded DataFrame before presenting it to the user:

- Column names are stripped of leading and trailing whitespace.
- Entirely empty rows and entirely empty columns are removed.
- Duplicate column names are detected and rejected with an explicit error listing the offending names; the user is asked to rename them in the source file and re-upload.
- For data loaded from Google Sheets, columns whose non-empty values are at least 80 % numeric are coerced to numeric type. Columns whose names contain the tokens `id`, `name`, `label`, `author`, `study`, `paper`, or `title` (case-insensitive) are exempt from coercion to prevent corruption of identifier fields.

### 2.3 Selecting the data type and mapping columns (Step 2)

For the Google Sheets and Upload Excel/CSV pathways, a second interface — headed **Step 2: Select Data Type & Map Columns** — appears immediately below the import section. The user first selects the input data format via the *Data Type:* radio buttons:

| Option label | Internal type | When to use |
|---|---|---|
| **Raw Data — Continuous (Means/SDs/N)** | `raw_continuous` | Means, standard deviations, and sample sizes are available for both Treatment and Control groups. |
| **Raw Data — Binary (Events/Non-Events)** | `raw_binary` | Event and non-event counts are available for both groups (2 × 2 contingency design). |
| **Pre-calculated (Effect/SE)** | `pre_calculated` | A standardised effect size (e.g., Hedges' *g*, lnRR) and either its variance or its standard error have already been computed. |

A dedicated column-mapping panel — *Map Your Columns (… Mode)* — is rendered below the radio group and updated automatically whenever the data-type selection changes. Each row of the panel pairs a target field with a dropdown listing all columns of the loaded table. CoMeta pre-populates each dropdown with its best guess, derived from a built-in synonym table (Section 2.6) that recognises common ecological and meta-analytic column-name conventions; the user adjusts any dropdown whose default selection is incorrect.

The fields exposed for each data type are listed below. Identifier-style synonyms (`id`, `study`, `study_id`, `paper`, `author`) are recognised across all three modes.

**Raw continuous mode** — all seven fields are required:

| Field | Widget label | Description |
|---|---|---|
| `id` | Study ID / Label | Unique identifier for the study or paper. |
| `xe` | Experimental Mean (xe) | Mean outcome in the Treatment group. |
| `sde` | Experimental SD (sde) | Standard deviation of the Treatment group. |
| `ne` | Experimental N (ne) | Sample size of the Treatment group. |
| `xc` | Control Mean (xc) | Mean outcome in the Control group. |
| `sdc` | Control SD (sdc) | Standard deviation of the Control group. |
| `nc` | Control N (nc) | Sample size of the Control group. |

**Raw binary mode** — all five fields are required:

| Field | Widget label | Description |
|---|---|---|
| `id` | Study ID / Label | Unique identifier for the study or paper. |
| `events_e` | Treatment Events (a) | Number of events in the Treatment group. |
| `nonevents_e` | Treatment Non-Events (b) | Number of non-events in the Treatment group. |
| `events_c` | Control Events (c) | Number of events in the Control group. |
| `nonevents_c` | Control Non-Events (d) | Number of non-events in the Control group. |

**Pre-calculated mode** — `id` and `yi` are required; at least one of `variance` or `se` must be mapped:

| Field | Widget label | Description | Status |
|---|---|---|---|
| `id` | Study ID / Label | Unique identifier for the study or paper. | Required |
| `yi` | Effect Size (yi) | The standardised effect size (Hedges' *g*, lnRR, log OR, log RR, etc.). | Required |
| `variance` | Variance (vi) | Sampling variance of the effect size. | Required if `se` is not mapped |
| `se` | Standard Error (SE) | Standard error of the effect size; converted internally to variance. | Required if `variance` is not mapped |
| `n_total` | Sample Size (n_total) | Total sample size; used by some publication-bias diagnostics. | Optional |

**Geographic columns (optional, all modes).** Below the core mapping panel, an optional *🌍 Geographic Columns* section permits the user to map up to three additional fields — *Latitude:*, *Longitude:*, and *Country / Region:* — that enable the geographic-distribution map in Cell 24. Latitude and longitude must be mapped together or omitted together; values outside the ranges [−90, 90] and [−180, 180] respectively are reported as warnings. A field may be left at its default value of *None* to skip it. Geographic columns may not duplicate any column already used as a core mapped field.

**Finalising the mapping.** The user confirms the mapping by clicking **✓ Confirm Mapping & Finalize Data**. CoMeta then:

1. Verifies that every required field has been assigned and that no column has been mapped to two different fields.
2. Coerces each numerically-required column to numeric type. If any required column contains text or missing values, the finalisation is aborted and an error panel lists the offending column, the number of unparseable rows, and the affected study identifiers. The user is asked to correct the source file and re-upload.
3. For pre-calculated mode, coerces the optional `variance`, `se`, and `n_total` columns, issuing a non-blocking warning for any values that cannot be parsed.
4. Validates mapped geographic columns and reports out-of-range or missing entries as warnings.
5. Renames the mapped columns to CoMeta's internal schema and retains all unmapped columns as candidate moderators for downstream analyses.

On success, a green **✅ Data Ready** banner is displayed, summarising the number of rows loaded, the number of mapped columns, the number of moderator columns detected, and (if applicable) the geographic coverage. A table below the banner lists each moderator column with its inferred type (numeric or categorical), the number of unique values, the number of missing entries, and either a range/mean summary (for numeric moderators) or a value-count summary (for categorical moderators). The user may then proceed to Cell 3.

> **Re-running Step 2.** Any change to the data-type radio button, the column-mapping dropdowns, or the source file requires re-clicking **✓ Confirm Mapping & Finalize Data** to take effect. Downstream cells whose results depend on the previous configuration will display a staleness banner until they are re-executed in order.

### 2.4 Supported data formats and minimum schema

CoMeta accepts data in four physical formats and three logical schemas. The physical formats are:

| Physical format | Extension(s) | Notes |
|---|---|---|
| Comma-separated values | `.csv` | UTF-8 preferred; Latin-1, Windows-1252, and UTF-8 BOM also accepted. |
| Microsoft Excel | `.xlsx`, `.xls` | Multi-sheet workbooks supported; the user selects the target sheet. |
| Google Sheets | (online) | First row is treated as the header. |
| CoMeta session file | `.json` | Previously exported analysis configuration; bypasses column mapping. |

The three logical schemas correspond to the three data-type radio options described in Section 2.3. The minimum dataset for a three-level meta-analysis consists of one row per effect-size record, with the columns listed below populated; additional columns may be present and will be retained as candidate moderators.

**Raw continuous schema (per row):**

```
id, xe, sde, ne, xc, sdc, nc
```

**Raw binary schema (per row):**

```
id, events_e, nonevents_e, events_c, nonevents_c
```

**Pre-calculated schema (per row):**

```
id, yi, (variance OR se), [n_total]
```

The square-bracketed `n_total` column is optional. The internal column names shown above are the names used by CoMeta after mapping; the user's original column names may differ, in which case the synonym table (Section 2.6) is applied automatically.

### 2.5 Three-level nesting

CoMeta is designed for three-level meta-analytic models in which multiple effect-size records are nested within primary studies (e.g., several treatment arms, time points, or response variables reported by one paper). The `id` column is the level-3 identifier (the primary study); the *row* of the dataset is the level-1 unit (the effect-size record). When two or more rows share the same `id`, CoMeta automatically treats them as nested observations and fits a three-level random-effects model in Cell 7. Datasets with one row per study are handled correctly as a degenerate (two-level) case; the fallback is reported transparently in the model output.

If a separate level-2 grouping (effect-size groups within studies) is to be modelled explicitly, it should be supplied as an unmapped moderator column with a clear name (e.g., `effect_group`) and selected in the model-configuration interface of Cell 7. The shared-control detection routine (Cell 4) operates independently of this level-2 column and uses treatment/control means and sample sizes to identify effect sizes that share a common control group.

### 2.6 Column-name synonyms

To minimise manual mapping, CoMeta's column-mapping interface pre-fills each dropdown with the first column of the user's table whose name (case-insensitive, whitespace-stripped) matches one of the synonyms listed below. If none of the synonyms is matched, the dropdown is left blank and the user selects the correct column manually.

**Identifiers (all schemas):**

| Internal name | Recognised synonyms |
|---|---|
| `id` | `id`, `study`, `study_id`, `paper`, `author` |

**Raw continuous schema:**

| Internal name | Recognised synonyms |
|---|---|
| `xe` | `xe`, `mean_e`, `mean_exp`, `x_e`, `treatment_mean` |
| `sde` | `sde`, `sd_e`, `sd_exp`, `sigma_e` |
| `ne` | `ne`, `n_e`, `n_exp`, `sample_e` |
| `xc` | `xc`, `mean_c`, `mean_ctrl`, `x_c`, `control_mean` |
| `sdc` | `sdc`, `sd_c`, `sd_ctrl`, `sigma_c` |
| `nc` | `nc`, `n_c`, `n_ctrl`, `sample_c` |

**Raw binary schema:**

| Internal name | Recognised synonyms |
|---|---|
| `events_e` | `events_e`, `events_exp`, `cases_e`, `cases_exp`, `a`, `treatment_events` |
| `nonevents_e` | `nonevents_e`, `nonevents_exp`, `control_e`, `b`, `treatment_nonevents` |
| `events_c` | `events_c`, `events_ctrl`, `cases_c`, `cases_ctrl`, `c`, `control_events` |
| `nonevents_c` | `nonevents_c`, `nonevents_ctrl`, `control_c`, `d`, `control_nonevents` |

**Pre-calculated schema:**

| Internal name | Recognised synonyms |
|---|---|
| `yi` | `yi`, `effect_size`, `es`, `hedges_g`, `lnrr`, `smd`, `effect`, `g`, `d` |
| `variance` | `variance`, `vi`, `var`, `v` |
| `se` | `se`, `standard_error`, `stderr`, `se_es` |
| `n_total` | `n_total`, `n`, `sample_size`, `total_n`, `sample_n` |

**Geographic columns (optional):**

| Internal name | Recognised synonyms |
|---|---|
| `latitude` | `latitude`, `lat` |
| `longitude` | `longitude`, `lon`, `long`, `lng` |
| `country` | `country`, `nation`, `region` |

> **A practical recommendation.** Although the synonym table covers a wide range of conventions, users compiling a new dataset for CoMeta are encouraged to adopt the internal column names directly. Doing so eliminates the mapping step entirely and removes a common source of manual error.

### 2.7 Summary

Cell 2 ingests the user's dataset via one of four pathways — Google Sheets, local file upload, restoration of a previously exported session, or a built-in example dataset — and translates it into one of three internal schemas (raw continuous, raw binary, or pre-calculated). When manual mapping is required, the user selects the data type, confirms the column assignments suggested by the synonym table, and clicks **✓ Confirm Mapping & Finalize Data**. Successful finalisation produces the green *Data Ready* banner together with a moderator summary table. The user may then proceed to Cell 3 (Global Filtering), which is described in Section 3.

---

## Section 3. Global Filtering

Cell 3, titled **⚙️ 3. Global Filtering**, applies a single optional pre-filter that restricts the entire downstream pipeline to a user-specified subset of the dataset. The filter operates on a categorical moderator column — for example, a taxonomic group, biome, experimental design, or study quality flag — and removes all records whose value of that column is not included in the retained set. Because the filter is *global*, every subsequent cell (data cleaning, effect size calculation, model fitting, subgroup analyses, meta-regression, publication-bias diagnostics, and sensitivity analyses) operates exclusively on the filtered subset.

The cell is executed by clicking its **▶ Run** button. Like all cells from Cell 2 onward, no analytical action is taken until the user interacts with the widget interface and presses the save button described below.

### 3.1 When the cell is skipped

If the data-type selected in Cell 2 is *Pre-calculated (Effect/SE)*, Cell 3 is bypassed automatically. In this case, the cell renders a grey informational banner:

> ⏭️ **Skip This Step (Pre-calculated Mode)** — Global pre-filtering is bypassed because you imported pre-calculated effect sizes. **Please proceed directly to Cell 4 (Data Cleaning).**

A minimal `ANALYSIS_CONFIG` record is initialised internally so that downstream cells receive the full dataset unchanged. The user does not need to take any further action in Cell 3 and may move on to Cell 4. Pre-filtering of pre-calculated datasets, if required, should be performed in the source spreadsheet before ingestion in Cell 2.

For raw-continuous and raw-binary modes, the cell renders the full filtering interface described below.

### 3.2 Interface

The interface is preceded by a header reading **Step 3: Global Pre-Filtering** and a one-line summary stating the total number of records loaded from Cell 2 (e.g., *"Loaded dataset contains 102 total records."*). Below this, a panel titled **Global Subset Selection (Optional)** contains the following two controls:

- **Filter Variable:** A dropdown listing every column of the dataset that is not part of the core analytical schema (i.e., not `id` and not one of the means, standard deviations, sample sizes, or event counts). The default value is *None*, which retains the full dataset unchanged.
- **Value-selection checkboxes.** When a column is chosen from the *Filter Variable:* dropdown, a list of checkboxes is generated dynamically — one per unique value of that column — each labelled with the value and its record count in the form `<value> (n=<count>)`. All checkboxes are checked by default. The user unchecks the values that should be *excluded* from the analysis; only records whose value of the filter variable matches one of the checked options are retained.

A header above the checkbox list reminds the user that *the checked values are the ones that will be retained* in the analysis.

Below the panel, a single action button — **▶ Save Configuration** — applies the selection.

### 3.3 Saving the configuration

When **▶ Save Configuration** is clicked, CoMeta writes the filter selection into the global `ANALYSIS_CONFIG` dictionary (specifically, the `prefilter_col` and `prefilter_values` keys, together with the filtered `clean_dataframe`) and renders a green confirmation banner. The banner message depends on the selection:

- If the *Filter Variable:* dropdown is left at *None*, the banner reads:
  > ✅ **Configuration Saved** — No global filters applied. The entire dataset will be retained.
- If a column has been chosen and one or more values have been checked, the banner reads:
  > ✅ **Configuration Saved** — Filtered by **\<column\>**. Retaining *N* selected group(s).

In both cases, the banner concludes with a directive to proceed to Cell 4.

> **Re-saving after a change.** Any change to the *Filter Variable:* dropdown or to the value checkboxes requires re-clicking **▶ Save Configuration** to take effect. Downstream cells display a staleness banner whenever the filter selection is modified and re-saved.

### 3.4 Behaviour under session restoration

When Cell 2 has been populated by uploading a previously exported `analysis_settings.json` file (Restore Session pathway, §2.1.3), Cell 3 displays a blue **🔄 Reproducibility Mode Active** notice at the top of the interface, indicating either the column on which the original session was filtered or that no filter was applied. The *Filter Variable:* dropdown and the value checkboxes are then auto-populated from the saved configuration, and **▶ Save Configuration** is invoked automatically. No manual action is required.

### 3.5 Practical guidance

The global pre-filter is intended for *exclusion criteria that are common to every analysis in the manuscript* — for example, restricting the analysis to a single biome, a single taxonomic clade, or studies that satisfy a quality threshold encoded as a categorical flag. Filters intended to define *subgroup contrasts* (e.g., comparing nitrogen-fixing versus non-nitrogen-fixing species) should not be applied here; instead, the moderator column should be left untouched in Cell 3 and selected as a grouping variable in the subgroup-analysis configuration of Cell 8.

Continuous moderators (numeric columns such as latitude, year of publication, or exposure duration) are not exposed in this interface, because filtering on a continuous variable would require an interval rather than a discrete value selection. Where such a restriction is required, it should be implemented in the source spreadsheet prior to ingestion. Continuous moderators remain fully available to the linear and spline meta-regression modules (Cells 12–15).

### 3.6 Summary

Cell 3 applies a single optional categorical pre-filter that propagates to every downstream cell. In pre-calculated mode the cell is skipped automatically; in raw modes, the user selects a *Filter Variable:* from the dropdown (or leaves it at *None*), unchecks any values that should be excluded, and clicks **▶ Save Configuration**. The green *Configuration Saved* banner confirms the action, after which the user proceeds to Cell 4 (Data Cleaning & Pre-processing), described in Section 4.
