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

---

## Section 4. Data Cleaning and Pre-processing

Cell 4, titled **⚙️ 4. Data Cleaning & Pre-processing**, performs three operations that are required before effect sizes can be computed: (i) it removes records that are structurally unusable (missing essential values, sample sizes below one), (ii) it resolves missing or zero standard deviations through a user-selected imputation strategy, and (iii) it detects effect-size records that share a common control group within the same primary study, tagging them with an internal `shared_group_id` that is consumed by the variance-covariance matrix construction routine in Cell 6 (Gleser & Olkin, 2009; Lajeunesse, 2011). The cell also applies the global pre-filter saved in Cell 3 and renders a tabbed summary of the resulting clean dataset together with a record of every removed row.

The cell is executed by clicking its **▶ Run** button. Depending on the contents of the dataset, the cell either completes automatically (Path A, §4.5) or presents an imputation interface that requires user input (Path B, §4.5).

### 4.1 When the cell is skipped

If the data-type selected in Cell 2 is *Pre-calculated (Effect/SE)*, Cell 4 is bypassed automatically and renders a grey informational banner:

> ⏭️ **Skip This Step (Pre-calculated Mode)** — Data cleaning and SD imputation are bypassed because you imported pre-calculated effect sizes. *N* observations ready for analysis. **Please proceed directly to Cell 5 (Effect Size Selection).**

Because pre-calculated effect sizes already incorporate the user's decisions about missing or implausible variances, no further cleaning is performed on them. Any record-level filtering of a pre-calculated dataset must be carried out upstream.

For raw-continuous and raw-binary modes, the cell performs the operations described in §4.2–§4.6 below.

### 4.2 Unconditional cleaning steps

Before any user-controllable imputation is offered, Cell 4 unconditionally performs the following operations on the dataset received from Cell 3:

1. **Identifier normalisation.** The `id` column is coerced to string and whitespace-trimmed.
2. **Numeric coercion.** Each of `xe`, `sde`, `ne`, `xc`, `sdc`, `nc` (continuous mode) or `events_e`, `nonevents_e`, `events_c`, `nonevents_c` (binary mode) is coerced to numeric; non-parseable entries are treated as missing.
3. **Removal of records missing essential values.** Rows in which any of the essential statistics (means and sample sizes for continuous mode; event and non-event counts for binary mode) is missing are removed and tagged with the reason *"Missing Essential Data (Mean or N)"*.
4. **Removal of records with invalid sample sizes.** Rows in which `ne < 1` or `nc < 1` are removed and tagged with the reason *"Invalid Sample Size (N < 1)"*.
5. **Application of the global pre-filter.** If a *Filter Variable:* and a non-empty set of retained values were saved in Cell 3, rows whose value of that column is not in the retained set are removed and tagged with the reason *"Filtered by User ('\<column\>')"*.

These five operations apply to every dataset that passes through Cell 4 and are not user-configurable.

### 4.3 Shared-control detection

After the unconditional cleaning steps, CoMeta searches for effect-size records that share a common control group within the same primary study. Two records are considered to share a control group when:

- they belong to the same study (identical `id`), and
- for continuous data, they share identical values of `nc`, `xc`, and `sdc` (rounded to six decimal places); or
- for binary data, they share identical values of `events_c` and `nonevents_c`.

Each detected group is assigned a unique `shared_group_id` of the form `<study_id>_shared_grp_<k>`. This column is appended to the cleaned dataset and is consumed by the variance-covariance matrix construction routine in Cell 6, which uses the Gleser & Olkin (2009) closed-form expressions for Hedges' *g* and the Lajeunesse (2011) delta-method expressions for the log response ratio to populate the off-diagonal entries of the per-study **V**ᵢ block. Records that do not share a control group with any other record retain a null `shared_group_id` and are treated as having independent sampling variances.

Shared-control detection is fully automatic; no user intervention is required, and the number of records found to share controls is reported in the *Data Summary* tab (§4.6). Manual override of the detection result is not exposed in the widget interface — if a shared-control structure is to be suppressed, the user should ensure that the relevant control-group statistics differ in the source dataset.

### 4.4 Variance imputation strategies

Once the unconditional steps have completed, Cell 4 inspects the cleaned dataset for missing or zero standard deviations in the `sde` or `sdc` columns. The cell's behaviour from this point onward depends on whether any such values are present.

#### 4.4.1 Missing standard deviations

When one or more rows have a missing `sde` or `sdc`, the user selects a strategy from the *Missing SDs:* dropdown. The four options are:

| Option label | Internal code | Description |
|---|---|---|
| **Impute from nearest study (by sample size)** | `nearest` | For each missing SD, the SD of the row with the closest sample size that has a valid SD is borrowed. Recommended when variability is expected to scale with sample size rather than with the outcome mean. |
| **Impute using median CV from available data** | `median_cv` | The median coefficient of variation, CV = SD ⁄ mean, is computed across all valid rows, and the missing SD is replaced by mean × median CV. This is the default strategy and is the convention most frequently adopted in ecological meta-analysis (cf. Lajeunesse, 2013). |
| **Impute using a custom CV (enter below)** | `custom_cv` | The user supplies a coefficient of variation (e.g., based on prior domain knowledge or a published benchmark), and the missing SD is replaced by mean × CV. Selecting this option reveals an additional *Custom CV:* numeric input (default 0.10; range 0.001 – 10.0; step 0.01). |
| **Drop rows with missing SD** | `drop` | Rows with a missing SD in either group are removed from the analysis. Tagged with the reason *"Missing Standard Deviation"*. |

Below the dropdown, a short explanatory note is displayed for the currently selected strategy. The default selection is *Impute using median CV from available data*.

#### 4.4.2 Zero standard deviations

A reported SD of exactly zero would, if taken at face value, assign infinite weight to that record in the meta-analysis. Cell 4 therefore requires the user to choose one of three strategies via the *Zero SDs:* dropdown:

| Option label | Internal code | Description |
|---|---|---|
| **Replace with smallest nonzero SD in dataset** | `global_min` | Each zero SD is replaced with the smallest strictly positive SD observed in the dataset. The affected records retain a finite but conservatively low weight. This is the default. |
| **Apply same method as missing SDs** | `same_as_missing` | Zero SDs are first converted to missing, after which the strategy selected in §4.4.1 is applied uniformly to all missing entries. |
| **Drop rows with zero SD** | `drop` | Rows in which either SD equals zero are removed from the analysis. Tagged with the reason *"Zero Standard Deviation"*. |

As with the missing-SD dropdown, a short explanatory note for the currently selected strategy is shown beneath the widget.

### 4.5 Two execution paths

Cell 4 takes one of two paths depending on whether the dataset contains any missing or zero SDs after the unconditional cleaning steps:

- **Path A — no SD issues detected.** The cell runs the full processing pipeline (steps in §4.2 plus shared-control detection from §4.3) immediately, without exposing the imputation widgets, and renders the *Data Summary* and *Removed Data* tabs described in §4.6. No user input is required beyond clicking **▶ Run** on the cell itself.
- **Path B — SD issues detected.** Cell 4 first renders a yellow ⚠️ ***Variance Data Action Required*** panel listing the affected columns and their counts (e.g., *"Experimental SD (sde): 12 missing"*, *"Control SD (sdc): 3 equal to zero"*). Below this panel, the *Standard Deviation Imputation Settings* section exposes the *Missing SDs:* and/or *Zero SDs:* dropdowns described in §4.4 (only the dropdowns relevant to the detected issues are shown), followed by a **▶ Process Data** button. The pipeline runs only after the user clicks this button.

In both paths, downstream cells are marked stale when Cell 4 completes, so that any subsequent re-execution of Cell 4 with new imputation choices is propagated correctly.

### 4.6 Output

On successful completion, Cell 4 displays a tabbed interface with two tabs:

- **📊 Data Summary.** A green ✅ ***Data Successfully Prepared*** card showing three top-line counts — *Rows for Analysis*, *Unique Studies*, and *Total Removed* — followed by a three-row table summarising:
  - the pre-filter status (column and number of rows dropped, if any);
  - the variance imputation log, listing each imputation step performed together with the relevant numerical summary (e.g., the median CV applied, or the global minimum SD used to replace zeros);
  - a hand-off directive instructing the user to proceed to Cell 5.
- **🗑️ Removed Data.** Either a table of every removed row, with the reason for removal and the original means, sample sizes, and SDs, or a green confirmation that no rows were removed. The table is intended to support manuscript-level reporting of inclusion/exclusion decisions and should be inspected before proceeding.

The processed dataset is stored internally as `data_filtered` together with the `shared_group_id` column and the imputation metadata, all of which are consumed by Cells 5 and 6.

### 4.7 Behaviour under session restoration

When the session has been restored from an exported `analysis_settings.json` file (§2.1.3), a blue **🔄 Reproducibility Mode Active** notice is displayed at the top of Cell 4, listing the missing-SD and zero-SD strategies recorded in the saved configuration. If the dataset contains SD issues, the *Missing SDs:* and *Zero SDs:* dropdowns are auto-populated from the saved values (including the *Custom CV:* field where applicable), and the processing pipeline is invoked automatically. No manual action is required.

### 4.8 Practical guidance

Three considerations are worth noting when configuring Cell 4:

- **Disclosure of imputation choices.** All imputation choices made in this cell are recorded in the session configuration and surfaced in the automated *Materials and Methods* text generated by Cell 7. The choice between *median CV* and *custom CV* in particular should be made deliberately, since the resulting figure is reported alongside the model in the generated text.
- **Sensitivity to the imputation strategy.** When a non-negligible proportion of records require SD imputation, the meta-analytic results may be sensitive to the choice of strategy. A standard sensitivity check is to refit the model under at least one alternative strategy (e.g., *median CV* and *drop*) and compare the pooled estimates; the leave-one-out and Baujat diagnostics in Cells 20–22 are complementary tools for this purpose.
- **Shared-control structure.** Because the shared-control detector relies on exact matches in the control-group statistics, datasets in which the same control group has been re-entered with slightly different rounding across rows will fail to be recognised as shared. If the relevant records are known to share a control group, the user should reconcile the control-group entries in the source spreadsheet before ingestion to ensure that the VCV construction in Cell 6 accounts for the induced covariance.

### 4.9 Summary

Cell 4 finalises the analytic dataset. It removes structurally invalid rows, applies the global pre-filter from Cell 3, detects effect-size records sharing a common control group, and resolves missing or zero standard deviations through a user-selected imputation strategy. When no SD issues are present, the cell completes automatically; otherwise the user selects strategies from the *Missing SDs:* and *Zero SDs:* dropdowns and confirms via **▶ Process Data**. The resulting clean dataset, together with the `shared_group_id` column, is passed to Cell 5 (Effect Size Diagnostics), described in Section 5.

---

## Section 5. Effect Size Selection and Diagnostics

Cell 5, titled **🔬 5. Effect Size Selection & Diagnostics**, is the decision point at which the user fixes the effect-size metric that will be computed in Cell 6 and used throughout the rest of the pipeline. The cell operates in two distinct modes depending on the data type chosen in Cell 2:

- In **raw mode** (`raw_continuous` or `raw_binary`), the cell inspects the cleaned dataset, audits its statistical topology, and applies a rule-based scoring engine that produces a recommended effect-size metric together with a stated confidence level. The user accepts the recommendation or selects a different metric from the supported list, subject to data-type compatibility checks.
- In **pre-calculated mode**, the recommendation engine is not available (the raw data are not present); the user instead declares the metric that the supplied effect sizes already represent, so that downstream cells can label and interpret them correctly.

In both modes, the cell's output is a `ANALYSIS_CONFIG['effect_size_type']` entry together with an `es_config` record specifying the internal column names that Cell 6 will create.

### 5.1 Raw mode: the recommendation engine

When the data type is `raw_continuous` or `raw_binary`, Cell 5 first classifies the dataset into one of three topologies:

| Topology | Trigger | Initial recommendation |
|---|---|---|
| **Pure binary** | All four binary columns (`events_e`, `nonevents_e`, `events_c`, `nonevents_c`) are present; continuous columns are absent. | **log Odds Ratio (log OR)** with *High* confidence. |
| **Mixed** | Both binary and continuous columns are present. | A yellow ⚠️ ***Ambiguous Data Types Detected*** panel is displayed, advising the user to confirm the data type manually. Initial recommendation: **Hedges' *g*** with *Low* confidence. |
| **Pure continuous** | Continuous columns (`xe`, `xc`, and at least one SD column) are present. | Output of the rule-based scoring engine (§5.2). |

The cell renders its output in three tabs:

| Tab | Label | Content |
|---|---|---|
| 1 | **💡 Recommendation** | The recommended metric, the rationale, the *Select Type:* radio group, and the **✓ Confirm Selection** button. |
| 2 | **📊 Data Patterns** | A diagnostic audit of the dataset's statistical topology: normalisation, negative values, zero values, scale heterogeneity, SD availability, and distribution shape. |
| 3 | **🧠 Decision Logic** | The row-by-row scoring table produced by the recommendation engine, together with the final per-metric point totals. |

### 5.2 The rule-based scoring engine (R1–R6)

For pure-continuous datasets, the recommendation engine compares two candidate metrics — log Response Ratio (lnRR) and Hedges' *g* — by accumulating weighted points across six rules. The dataset's diagnostic features are computed first, and each rule contributes to one or both metric scores. The final winner is the metric with the higher total; the difference in points determines the stated confidence.

| Rule | Diagnostic | Decision threshold | Points awarded | Rationale |
|---|---|---|---|---|
| **R1** | Negative values present in `xe` or `xc` | any negative | Hedges' *g* +10 | Log-ratio metrics are mathematically undefined for negative values. This rule operates as a near-hard constraint. |
|  | All values strictly positive | otherwise | lnRR +2 | Data are compatible with ratio-based metrics. |
| **R2** | Control values clustered at unity | > 50 % of `xc` exactly 1.0 | lnRR +5 | Pre-normalised fold-change data are already a ratio scale. |
|  |  | > 30 % of `xc` in [0.95, 1.05] | lnRR +3 | Strong evidence of normalisation. |
|  |  | mean(`xc`) ∈ (0.8, 1.2) | lnRR +1 | Weak evidence of a unity baseline. |
| **R3** | Scale heterogeneity (ratio of `xe` and `xc` ranges) | ratio > 100 | lnRR +3 | Heterogeneous scales are handled naturally by ratios. |
|  |  | ratio > 10 | lnRR +2 | Moderate scale variance still favours ratios. |
|  |  | otherwise | Hedges' *g* +1 | Comparable scales support standardised mean differences. |
| **R4** | Zero values present in `xe` or `xc` | any zero | Hedges' *g* +2 | log(0) is undefined; lnRR would require an additive constant. |
| **R5** | SD coverage | > 80 % of rows with valid SDs | Hedges' *g* +1 | Hedges' *g* requires complete SDs. |
|  |  | < 20 % | (no points; warning recorded) | SD imputation has unstable consequences. |
| **R6** | Maximum skewness of `xe` and `xc` | skew > 1.5 | lnRR +2 | Strong right-skew typical of multiplicative biological processes. |
|  |  | skew ∈ (−0.5, 0.5) | Hedges' *g* +1 | Approximately symmetric data fit the SMD assumptions. |

**Tie-breaker.** If the two totals are equal after R1–R6, the engine awards one additional point to lnRR when the dataset contains neither negative nor zero values (lnRR is preferred for strictly-positive ecological data because of its direct percentage-change interpretation), and to Hedges' *g* otherwise.

**Confidence level.** Let *Δ* be the absolute difference between the lnRR and Hedges' *g* totals. The reported confidence is:

| Confidence | Condition |
|---|---|
| **High** | *Δ* ≥ 5 |
| **Moderate** | 3 ≤ *Δ* < 5 |
| **Low** | *Δ* < 3 |

The full scoring table — each rule that fired, the metric it favoured, the weight (encoded as plus-signs), and a one-line educational note — is displayed in the **🧠 Decision Logic** tab. The final point totals are shown beneath the table.

### 5.3 The Data Patterns audit

The **📊 Data Patterns** tab is intended both to justify the recommendation and to serve as a record of the dataset's properties for the methods section of a manuscript. For pure-continuous datasets, the audit reports six diagnostics in plain language:

1. **Control group normalisation** — the percentage of control means exactly equal to 1.0.
2. **Negative values** — the total count of negative entries in `xe` and `xc`.
3. **Zero values** — the total count of zero entries in `xe` and `xc`.
4. **Scale heterogeneity** — the ratio of the larger to the smaller of the `xe` and `xc` ranges.
5. **Data completeness** — the percentage of rows with valid SDs in both groups.
6. **Distribution shape (skewness)** — the maximum of skewness(`xe`) and skewness(`xc`).

For pure-binary datasets, the audit instead reports that complete 2 × 2 contingency-table data were detected and notes that the Haldane–Anscombe continuity correction (+ 0.5 to all cells) will be applied automatically by Cell 6 in studies containing a zero cell.

### 5.4 Selecting an effect-size metric

The **💡 Recommendation** tab displays a coloured banner naming the recommended metric and a one-sentence rationale, followed by a *Select Type:* radio group containing the five effect sizes supported in raw mode:

| Option label | Internal code | Compatible data |
|---|---|---|
| **log Response Ratio (lnRR) — for ratio/fold-change data** | `lnRR` | Continuous |
| **Hedges' *g* — for standardized mean differences (corrected)** | `hedges_g` | Continuous |
| **Cohen's *d* — for standardized mean differences (uncorrected)** | `cohen_d` | Continuous |
| **log Odds Ratio (log OR) — for binary outcome data** | `log_or` | Binary |
| **log Risk Ratio (log RR) — for binary outcome data** | `log_rr` | Binary |

The radio button is pre-selected to the engine's recommendation. The user may switch freely between options; CoMeta runs a compatibility check on every change and reacts as follows:

- If the chosen metric is compatible with the dataset's topology, the *About* panel beneath the radio group describes the metric in one short paragraph (e.g., for Hedges' *g*: *"A variation of Cohen's d that includes a correction factor (J) for small sample sizes …"*), and the action button remains enabled and labelled **✓ Confirm Selection**.
- If the chosen metric is incompatible with the dataset (for example, *log OR* selected on a continuous-only dataset, or *Hedges' *g** selected on a pure-binary dataset), a red ❌ ***INCOMPATIBLE DATA*** panel is displayed, the action button is disabled, and its label switches to **✗ Invalid Selection**. The user must choose a compatible metric before proceeding.

Clicking **✓ Confirm Selection** writes the choice to `ANALYSIS_CONFIG['effect_size_type']` together with the corresponding `es_config` record (internal column names that Cell 6 will create — for example, `lnRR`, `var_lnRR`, `SE_lnRR`, `CI_lower_lnRR`, `CI_upper_lnRR`). A green ✅ ***Configuration Saved*** banner confirms the action and directs the user to Cell 6. Downstream cells are marked stale.

### 5.5 Pre-calculated mode: manual declaration

When the data type is `pre_calculated`, the cell does not perform a topology audit. Instead, it renders a yellow informational panel — ***📊 Pre-calculated Effect Size Mode*** — and exposes a single *Effect Size Type:* dropdown containing the five metrics that the pipeline can interpret as already computed:

| Option label | Internal code |
|---|---|
| **Hedges' g (Standardized Mean Difference)** | `hedges_g` |
| **log Response Ratio (lnRR)** | `lnRR` |
| **log Odds Ratio (logOR)** | `log_or` |
| **Fisher's z (Correlation)** | `fisher_z` |
| **Cohen's d (Uncorrected SMD)** | `cohen_d` |

Below the dropdown, an *About* panel describes the currently selected metric. Clicking **✓ Confirm Effect Size Type** writes the user's declaration to `ANALYSIS_CONFIG` (together with the `variance_type` value — `variance`, `se`, or `both` — recorded by Cell 2) and renders the green confirmation banner.

The user is responsible for ensuring that the metric declared here corresponds to the column supplied as `yi` in Cell 2. Mis-declaration of the metric will not be flagged by CoMeta but will lead to incorrect labelling of every subsequent figure, table, and automatically-generated text block.

### 5.6 Behaviour under session restoration

In reproducibility mode, a blue **🔄 Reproducibility Mode Active** notice is displayed at the top of the cell, reporting the metric being restored. The *Select Type:* (raw mode) or *Effect Size Type:* (pre-calculated mode) widget is auto-populated from the saved configuration, and the corresponding confirmation action is invoked automatically. No manual interaction is required.

### 5.7 Practical guidance

Three considerations are worth noting at this step:

- **The recommendation is advisory, not prescriptive.** The rule-based engine encodes a defensible default for ecological datasets, but it does not supersede domain knowledge. When the recommendation conflicts with the conventional metric in the user's literature (for example, when reviewers expect Hedges' *g* despite the data being strongly right-skewed), the user should override the recommendation and proceed with the field-standard metric.
- **Cohen's *d* is exposed for completeness.** Hedges' *g* is the small-sample-corrected analogue of Cohen's *d* and is the appropriate default for meta-analysis. *Cohen's d* is provided primarily for reproducing analyses from earlier literature that pre-dates the widespread adoption of the *J* correction.
- **Mixed data deserve explicit justification.** When the *Ambiguous Data Types Detected* panel appears, the user should decide whether the binary and continuous portions of the dataset can be meaningfully combined under a single metric, or whether they constitute distinct meta-analyses that should be performed separately. CoMeta will compute the chosen metric on every row for which it is mathematically defined, but the interpretability of the pooled estimate is the user's responsibility.

### 5.8 Summary

Cell 5 fixes the effect-size metric for the remainder of the pipeline. In raw mode, a rule-based scoring engine evaluates six topological diagnostics and proposes either lnRR or Hedges' *g* (or, for binary datasets, log OR), with the reasoning surfaced in the **📊 Data Patterns** and **🧠 Decision Logic** tabs; the user accepts or overrides the recommendation via the *Select Type:* radio group, subject to a compatibility check, and clicks **✓ Confirm Selection**. In pre-calculated mode, the user declares the metric via the *Effect Size Type:* dropdown and clicks **✓ Confirm Effect Size Type**. In both cases, successful confirmation hands off to Cell 6 (Effect Size Calculation), described in Section 6.

---

## Section 6. Effect Size Calculation

Cell 6, titled **🧮 6. Effect Size Calculation**, executes the numerical work of the meta-analytical pipeline. It (i) computes the per-record effect size and its sampling variance using the metric chosen in Cell 5, (ii) applies the metric-specific cleaning rules required to keep the calculation mathematically well-defined, (iii) constructs the variance–covariance (VCV) matrices that encode the dependence between effect sizes sharing a common control group within the same study, and (iv) populates a five-tab diagnostic interface that should be inspected before proceeding to the model in Cell 7.

The cell has no user-input widgets. It runs in full when the user clicks its **▶ Run** button, and its output reflects the configuration produced by Cells 2–5 verbatim. If any analytical choice needs to be revised, the user returns to the relevant upstream cell, re-saves, and re-executes Cell 6.

### 6.1 Inputs and execution paths

Cell 6 consumes the cleaned dataset `data_filtered` (from Cell 4) and the configuration dictionary `ANALYSIS_CONFIG` (populated by Cells 3 – 5). Depending on `ANALYSIS_CONFIG['data_type']`, one of two execution paths is taken:

- **Raw path** (`data_type == 'raw'`): the cell computes the effect sizes from the raw means, standard deviations, and sample sizes (or event/non-event counts).
- **Pre-calculated path** (`data_type == 'pre_calculated'`): the cell standardises the user-supplied effect sizes and variances into the internal schema, validates them, and derives the remaining columns (standard errors, confidence intervals, inverse-variance weights, back-transformed quantities).

Both paths conclude by constructing the per-study VCV matrices (§6.4) and rendering the same tabbed output (§6.5).

### 6.2 Metric-specific cleaning (raw path only)

Before any effect size is computed, Cell 6 applies the cleaning rules required by the metric selected in Cell 5. These rules complement, but do not duplicate, the SD imputation already performed in Cell 4.

**Log Response Ratio (lnRR).** lnRR is undefined for non-positive values:

- Rows in which `xe < 0` or `xc < 0` are removed.
- For rows in which `xe == 0` or `xc == 0`, a small additive offset is applied to both means. The offset is set to 1 % of the smallest strictly positive value observed across `xe` and `xc` (or 0.001 if no positive values are available). This data-driven offset preserves the relative ordering of effects across studies of differing scales.

**Log odds ratio (log OR) and log risk ratio (log RR).** For 2 × 2 contingency-table data:

- **Double-zero studies** — studies in which both `events_e == 0` and `events_c == 0` — are uninformative for relative effects and are removed; the reason recorded is *"Double-Zero Event Count (Uninformative)"*.
- **Single-zero studies** — studies in which any one of `events_e`, `nonevents_e`, `events_c`, `nonevents_c` equals zero — are corrected by the standard **Haldane–Anscombe continuity correction**: 0.5 is added to all four cells of the affected 2 × 2 table.

**Hedges' *g*, Cohen's *d***. No additional row-level cleaning is performed; rows that produce NaN effect sizes or non-finite variances after the calculation in §6.3 are removed and tagged with the reason *"Calculation Failed (Missing Data/NaN)"* or *"Zero or Negative Variance"*.

### 6.3 Effect-size and variance formulae

The formulae implemented in Cell 6 are summarised below. All formulae operate row-wise on the cleaned dataset. Symbols: *x̄*ₑ, *x̄*_c are the experimental and control means; *s*ₑ, *s*_c the corresponding standard deviations; *n*ₑ, *n*_c the sample sizes; *a*, *b*, *c*, *d* the cells of the 2 × 2 contingency table (events_e, nonevents_e, events_c, nonevents_c).

**Log Response Ratio (lnRR).**

$$ \mathrm{lnRR} = \ln\!\bigl(\bar{x}_e / \bar{x}_c\bigr), \qquad \mathrm{Var}(\mathrm{lnRR}) = \frac{s_e^{2}}{n_e\,\bar{x}_e^{2}} + \frac{s_c^{2}}{n_c\,\bar{x}_c^{2}}. $$

The cell additionally reports the back-transformed *Response Ratio* (exp lnRR), a signed *fold change*, and the *Percent Change* (Response Ratio − 1) × 100, all stored as separate columns for interpretation.

**Hedges' *g*.** The cell computes the pooled standard deviation

$$ s_p = \sqrt{\frac{(n_e - 1)\,s_e^{2} + (n_c - 1)\,s_c^{2}}{n_e + n_c - 2}}, $$

Cohen's *d* = (*x̄*ₑ − *x̄*_c) ⁄ *s*_p, and the exact small-sample correction factor *J* via the gamma function,

$$ J(m) = \frac{\Gamma(m/2)}{\sqrt{m/2}\;\Gamma\!\bigl((m-1)/2\bigr)}, \qquad m = n_e + n_c - 2, $$

so that Hedges' *g* = *J* · *d*. The variance uses the large-sample approximation matching *metafor* and Borenstein et al.,

$$ \mathrm{Var}(g) = \frac{1}{n_e} + \frac{1}{n_c} + \frac{g^{2}}{2\,(n_e + n_c)}. $$

**Cohen's *d* (uncorrected).** Same as Hedges' *g* but without the *J* factor:

$$ d = \frac{\bar{x}_e - \bar{x}_c}{s_p}, \qquad \mathrm{Var}(d) = \frac{n_e + n_c}{n_e\,n_c} + \frac{d^{2}}{2\,(n_e + n_c)}. $$

**Log odds ratio (log OR).**

$$ \mathrm{logOR} = \ln\!\bigl(a\,d / (b\,c)\bigr), \qquad \mathrm{Var}(\mathrm{logOR}) = \tfrac{1}{a} + \tfrac{1}{b} + \tfrac{1}{c} + \tfrac{1}{d}. $$

The back-transformed *Odds Ratio* (exp logOR) and its confidence bounds are stored alongside.

**Log risk ratio (log RR).**

$$ \mathrm{logRR} = \ln\!\Bigl(\tfrac{a/(a+b)}{c/(c+d)}\Bigr), \qquad \mathrm{Var}(\mathrm{logRR}) = \tfrac{1}{a} - \tfrac{1}{a+b} + \tfrac{1}{c} - \tfrac{1}{c+d}. $$

The back-transformed *Risk Ratio* is stored alongside.

**Derived quantities (all metrics).** For every retained row, Cell 6 computes:

| Quantity | Formula | Internal column |
|---|---|---|
| Standard error | $\sqrt{\mathrm{Var}}$ | metric-specific (e.g., `SE_lnRR`, `SE_g`) |
| 95 % Wald confidence interval | effect ± 1.96 · SE | metric-specific `CI_lower_*`, `CI_upper_*` |
| Fixed-effect weight | 1 ⁄ Var | `w_fixed` |

The Wald interval is used for record-level diagnostics only; the pooled estimate reported by Cell 7 uses the appropriate model-based interval (Knapp–Hartung-adjusted, profile-likelihood, or CR2 cluster-robust) and is not the row-wise Wald CI.

### 6.4 Construction of the variance–covariance (VCV) matrices

For each primary study (level-3 unit identified by `id`), Cell 6 constructs a per-study variance–covariance matrix **Σ**ᵢ that encodes the sampling covariance between effect-size records sharing a common control group within that study. The matrix is initialised as the diagonal of sampling variances. For every set of two or more rows sharing the same `shared_group_id` (assigned by Cell 4, §4.3), the corresponding off-diagonal entries are filled using metric-specific closed-form expressions:

| Metric | Shared-control covariance | Source |
|---|---|---|
| **lnRR** | $s_c^{2} / (n_c\,\bar{x}_c^{2})$ | Lajeunesse (2011) delta-method expression. |
| **Cohen's *d*** | $\tfrac{1}{n_c} + \tfrac{d_i\,d_j\,n_c}{2\,N_i\,N_j}$ with $N_k = n_{e,k} + n_c$ | Gleser & Olkin (2009), Table 4. |
| **Hedges' *g*** | $J_i\,J_j\,\bigl[\tfrac{1}{n_c} + \tfrac{d_i\,d_j\,n_c}{2\,N_i\,N_j}\bigr]$, with *d* back-derived from *g* via *J* | Gleser & Olkin (2009); the *J* factor uses exact log-gamma. |
| **log OR** | $\tfrac{1}{c} + \tfrac{1}{d}$ (where *c*, *d* are the control-arm event and non-event counts) | Gleser & Olkin (2009). |
| **log RR** | $\tfrac{1}{c} - \tfrac{1}{n_c}$, with $n_c = c + d$ | Gleser & Olkin (2009). |

The resulting dictionary of matrices is stored as `ANALYSIS_CONFIG['vcv_matrices']` and consumed by the three-level REML engine in Cell 7 to populate the off-diagonal entries of the marginal variance Σᵢ = τ²_between · **J**ᵢ + τ²_within · **I**ᵢ + **V**ᵢ. Studies that contain no shared-control records receive a purely diagonal matrix; their sampling variances are therefore treated as independent, exactly as they would be in a conventional fixed-V meta-analysis. No user action is required to enable the VCV correction — it is applied automatically wherever Cell 4 detected a shared control group.

### 6.5 Output: five diagnostic tabs

On completion, Cell 6 renders a tabbed interface comprising the following five tabs:

- **📊 Summary.** Three top-line counts (Observations, Studies, Removed) are displayed as coloured cards, followed by a descriptive table (mean, median, min, max, standard deviation of the effect-size column) and a histogram of the effect-size distribution with a vertical dashed line at the sample mean and a thin reference line at the null value.
- **📉 Diagnostics.** A processing log enumerates every cleaning step performed (SD handling carried forward from Cell 4, metric-specific cleaning from §6.2, VCV construction). Below the log, an **Outlier Analysis (IQR Method)** identifies effect sizes lying outside the standard 1.5 × interquartile range fences and presents them in a sortable table together with the originating `id`, `xe`, `xc`, `ne`, `nc` (and `year`, where available). The intended use is the detection of transcription errors in the source spreadsheet; biologically extreme but genuine values should be retained.
- **📏 Detailed Stats.** A descriptive table reporting *N*, mean, median, standard deviation, skewness, and kurtosis of the effect size, standard error, and variance; a *Normality Check (Shapiro–Wilk)* card (test omitted for *N* > 5000); a brief *What should I do?* advisory panel that flags small-sample non-normality, high skewness (|skew| > 1), and high kurtosis (|kurt| > 3); a Q–Q plot of the effect-size column against the normal quantiles; and a five-row preview of the analytical dataset.
- **🧠 Interpretation.** Three headline cards report the *Direction* of the typical effect (Favors Treatment / Favors Control / Ambiguous, based on the proportion of studies whose individual 95 % CI excludes the null), the *Significance Rate* (% of records with a 95 % CI excluding the null), and the *Dominant Magnitude* (the most common magnitude bin, see below). A pie chart summarises the vote-counting classification (significant positive / significant negative / non-significant), and a horizontal bar chart reports the count of records in each magnitude bin. A brief automated narrative summarises these results in prose. The magnitude bins follow Cohen's conventional benchmarks for standardised mean differences and approximate benchmarks for ratio-scale metrics:

  | Metric class | Negligible | Small | Medium | Large |
  |---|---|---|---|---|
  | Hedges' *g*, Cohen's *d* | < 0.2 | 0.2 – 0.5 | 0.5 – 0.8 | > 0.8 |
  | lnRR, log OR, log RR | < 0.1 | 0.1 – 0.3 | 0.3 – 0.5 | > 0.5 |

  The vote-counting and magnitude classifications in this tab are *record-level* descriptive aids; they do **not** substitute for the model-based pooled inference reported by Cell 7.
- **🗑️ Removed Data.** A table listing every row removed by Cell 6, together with the reason for removal (*"Double-Zero Event Count (Uninformative)"*, *"Calculation Failed (Missing Data/NaN)"*, *"Zero or Negative Variance"*, *"Missing Effect Size or Variance"*, etc.) and the originating means, sample sizes (or event counts), and effect size / variance columns. A green confirmation banner is shown if no rows were removed.

### 6.6 Pre-calculated path

When the data type is `pre_calculated`, the metric-specific calculations of §6.3 are bypassed. The cell instead performs the following operations:

1. The user-supplied effect size column (`yi`) and variance column are coerced to numeric and renamed to the internal schema (e.g., `lnRR`, `var_lnRR`). When only a standard error was mapped in Cell 2, it is squared to yield the variance; when both `variance` and `se` were mapped, the explicit variance column is preferred.
2. Rows with a missing effect size or variance are removed (reason *"Missing Effect Size or Variance"*); rows with zero variance are removed (reason *"Zero Variance (Infinite Weight)"*); the presence of any negative variance triggers a critical error and the pipeline halts.
3. The standard error, 95 % Wald confidence interval, and inverse-variance weight are derived using the same formulae as the raw path.
4. For ratio-scale metrics (lnRR, log OR, log RR), the back-transformed Response Ratio / Odds Ratio / Risk Ratio and the corresponding confidence-interval columns are computed.
5. The VCV matrices are constructed exactly as in §6.4. Because the raw control-group statistics are not available, only the metrics that require nothing beyond the variance column itself yield a diagonal **Σ**ᵢ; off-diagonal entries can be populated only where the relevant raw columns (`nc`, `xc`, `sdc`, or `events_c`, `nonevents_c`) are present in the pre-calculated dataset and a `shared_group_id` has been assigned.

The same five-tab output is rendered, with the Pre-calculated mode flagged in the Summary tab. The Diagnostics tab reports the validation steps performed; the Detailed Stats and Interpretation tabs apply identically to pre-calculated and raw datasets.

### 6.7 Outputs handed to downstream cells

Cell 6 writes the following keys to `ANALYSIS_CONFIG` for consumption by Cell 7 onwards:

| Key | Contents |
|---|---|
| `analysis_data` | The cleaned, per-record analytical DataFrame, with the effect size, variance, SE, CI bounds, fixed-effect weight, and back-transformed columns. |
| `effect_col`, `var_col`, `se_col`, `ci_lower_col`, `ci_upper_col` | The internal column names for the chosen metric. |
| `vcv_matrices` | A dictionary keyed by `id` containing the per-study VCV matrix. |

These objects, together with the unchanged moderator columns retained from Cell 2, constitute the full input to the three-level REML engine in Cell 7.

### 6.8 Practical guidance

- **Inspect the Removed Data tab before modelling.** Records dropped at this stage do not appear in the model fit. The number and reason for each removal should be reported in the manuscript's Methods section; CoMeta's automated *Materials and Methods* generator in Cell 7 will surface these counts, but the user is responsible for verifying that the removals are scientifically defensible.
- **Outliers are advisory, not prescriptive.** The 1.5 × IQR rule flags candidates for inspection. Ecological data routinely contain genuine extreme values, and silent removal of such records is inappropriate; the cumulative, leave-one-out, and Baujat diagnostics in Cells 20 – 22 are the appropriate tools for assessing the influence of extreme records on the pooled estimate.
- **The record-level Wald CIs are not the model output.** The 95 % CIs displayed in this cell are based on the asymptotic normal approximation around each record and are intended for visualising the per-study distribution. The pooled estimate, the heterogeneity statistics, and the inference reported in Cell 7 use the three-level REML model with CR2 cluster-robust standard errors and Satterthwaite degrees of freedom; these are the values that should be reported.
- **The zero-offset for lnRR is a fallback, not a remedy.** If a non-trivial proportion of records require the zero offset described in §6.2, the appropriateness of lnRR for the dataset should be reconsidered. Hedges' *g* is the appropriate alternative for outcomes that legitimately attain zero values.

### 6.9 Summary

Cell 6 computes, per record, the effect size and sampling variance for the metric chosen in Cell 5, applying the metric-specific cleaning rules required to keep the calculation well-defined (lnRR zero-offset; binary double-zero drop and Haldane–Anscombe correction). For every primary study, it builds the variance–covariance matrix that encodes within-study sampling dependence among effect sizes that share a control group, using the Gleser & Olkin (2009) and Lajeunesse (2011) closed-form expressions. The cell renders a five-tab diagnostic interface — **📊 Summary**, **📉 Diagnostics**, **📏 Detailed Stats**, **🧠 Interpretation**, **🗑️ Removed Data** — that should be inspected before proceeding to Cell 7 (Overall Meta-Analysis), described in Section 7.

---

## Section 7. Overall Meta-Analysis

Cell 7, titled **📊 7. Overall Meta-Analysis**, fits the pooled meta-analytical model. It is the central analytical cell of CoMeta: every subsequent cell — subgroup analysis, meta-regression, publication-bias diagnostics, sensitivity analyses, and the complementary modules — operates on the model fitted here. Cell 7 estimates three candidate models in parallel (fixed-effect, two-level random-effects, and three-level hierarchical), compares them by the Akaike Information Criterion (AIC), reports the pooled effect together with cluster-robust inference and a heterogeneity decomposition, generates a manuscript-ready *Materials and Methods* and *Results* paragraph adapted to the chosen configuration, and exports the complete session to either an Excel audit workbook or a JSON reproducibility file.

The cell is executed by clicking its **▶ Run** button. It performs an initial fit with default settings and renders the six output tabs immediately, so that the user sees a complete result on the first execution. Any change to the analytical settings is applied by editing the widgets in the **⚙️ Settings** tab and clicking **Re-Run Analysis**.

### 7.1 The model

For each primary study *i* with *k*ᵢ effect-size records, CoMeta represents the vector of observed effect sizes **y**ᵢ as

$$ \mathbf{y}_i \;=\; \mathbf{1}_{k_i}\,\mu \;+\; u_i\,\mathbf{1}_{k_i} \;+\; \mathbf{e}_i^{(w)} \;+\; \boldsymbol{\varepsilon}_i, $$

where *μ* is the pooled effect, *u*ᵢ ∼ 𝒩(0, τ²_between) is the between-study random effect, **e**ᵢ⁽ʷ⁾ ∼ 𝒩(**0**, τ²_within **I**) is the between-effect-sizes-within-studies random effect, and **ε**ᵢ ∼ 𝒩(**0**, **V**ᵢ) is the vector of sampling errors with the per-study variance–covariance matrix **V**ᵢ constructed by Cell 6 (Section 6.4). The marginal covariance of **y**ᵢ is therefore

$$ \boldsymbol{\Sigma}_i \;=\; \tau^{2}_{\mathrm{between}}\,\mathbf{J}_i \;+\; \tau^{2}_{\mathrm{within}}\,\mathbf{I}_i \;+\; \mathbf{V}_i, $$

where **J**ᵢ is the *k*ᵢ × *k*ᵢ matrix of ones and **I**ᵢ is the identity. The variance components are estimated by restricted maximum likelihood (REML) by default; profile-likelihood confidence intervals for τ² and σ² are computed by one-dimensional Brent root-finding over the profile log-likelihood. When τ²_within is estimated at the lower boundary (≈ 0), the three-level model is automatically reverted to a two-level random-effects model and the user is informed in the *Model Selection* tab.

Three candidate models are fitted simultaneously: (i) the **fixed-effect** model (τ²_between = τ²_within = 0); (ii) the **two-level random-effects** model (τ²_within = 0, with τ²_between estimated by the user-selected method); and (iii) the **three-level** model. The model with the lower AIC is reported as the *winner* in the **📊 Primary Result** and **⚖️ Model Selection** tabs; the user may override the AIC selection with the *Model Selection:* dropdown (Section 7.4).

### 7.2 Inference

Pooled-effect inference uses the inverse-Σᵢ-weighted least-squares estimator

$$ \hat{\mu} \;=\; \Bigl(\sum_i \mathbf{1}_{k_i}^{\top}\,\boldsymbol{\Sigma}_i^{-1}\,\mathbf{1}_{k_i}\Bigr)^{-1} \sum_i \mathbf{1}_{k_i}^{\top}\,\boldsymbol{\Sigma}_i^{-1}\,\mathbf{y}_i, $$

and reports a **CR2 cluster-robust standard error** (Pustejovsky & Tipton, 2018) with Satterthwaite-approximated degrees of freedom for the *t*-statistic. The CR2 estimator is robust to mis-specification of the working **Σ**ᵢ — in particular to incorrect choices of the within-study correlation structure — and is the default for every coefficient reported by Cells 7, 8, 12, and 14.

A **95 % prediction interval** for the true effect of a future, exchangeable study is reported alongside the confidence interval. For the two-level model it follows Higgins, Thompson, and Spiegelhalter (2009); for the three-level model it incorporates both variance components. The **Knapp–Hartung small-sample adjustment** is applied to the standard error of the pooled estimate when the corresponding checkbox is enabled (default).

Inversion of **Σ**ᵢ uses a Sherman–Morrison path whenever **V**ᵢ is diagonal and a full Cholesky decomposition otherwise; this ensures numerical stability when the user's dataset includes shared control groups and **V**ᵢ contains off-diagonal entries.

### 7.3 Heterogeneity

Cell 7 reports the conventional decomposition: the Cochran *Q* statistic with its degrees of freedom and *p*-value, the Higgins *I* ² index, and the variance components themselves with profile-likelihood confidence intervals. For the three-level model, both τ²_between (between-studies) and σ² ≡ τ²_within (between-effect-sizes-within-studies) are reported with their respective intervals. The narrative interpretation surfaced in the **📉 Heterogeneity** tab follows Higgins et al. (2003): *I* ² < 25 % is labelled negligible, 25–50 % low, 50–75 % moderate, and > 75 % substantial.

### 7.4 Analytical settings

The **⚙️ Settings** tab exposes six widgets that control every user-tunable aspect of the model. The defaults correspond to the convention most frequently adopted in the ecological meta-analysis literature.

| Widget label | Type | Options | Default | Effect |
|---|---|---|---|---|
| **Confidence Level:** | dropdown | *95 % CI (α = 0.05)*, *99 % CI (α = 0.01)*, *90 % CI (α = 0.10)* | 95 % CI | Sets the nominal coverage of every confidence and prediction interval reported in the cell. |
| **Model Selection:** | dropdown | *Auto-Select (Best AIC)*, *Force 2-Level*, *Force 3-Level* | Auto-Select | Determines which model is reported in the *Primary Result* tab. Auto-select compares AIC values and reports the lower; the forced options bypass the comparison. |
| **τ² Method:** | dropdown | *REML*, *DL*, *ML* | REML | Estimator for the between-study variance: restricted maximum likelihood, DerSimonian–Laird, or maximum likelihood. |
| **Knapp-Hartung Correction** | checkbox | — | enabled | Applies the Knapp–Hartung adjustment to the standard error of the pooled effect for improved small-sample inference. |
| **Inference:** | dropdown | *t-distribution (Robust/Small Sample)*, *Normal distribution (z) (Match R)* | *t* | Controls whether *p*-values and confidence intervals are derived from a *t*-distribution with Satterthwaite degrees of freedom or from the standard normal distribution. |
| **Use Full Log-Likelihood** | checkbox | — | disabled | Switches the REML log-likelihood from the restricted form to the full form, which matches certain alternative implementations in R. |

Every widget is observed: any change is recorded in `ANALYSIS_CONFIG['global_settings']` immediately, but the model is *not* refitted until the user clicks the **Re-Run Analysis** button at the bottom of the tab. This deferred-refit pattern is intentional: it allows the user to adjust several settings together (for example, switching to DL with the *z*-distribution to reproduce a literature analysis) before incurring the cost of refitting.

When **Re-Run Analysis** is clicked, the model is refitted under the new settings, all six tabs are re-rendered, and every downstream cell that depends on the overall model (subgroup analysis, meta-regression, spline regression, publication-bias diagnostics, leave-one-out, cumulative) is marked stale.

### 7.5 Output: six tabs

#### 7.5.1 📊 Primary Result

The first tab displays the headline result of the analysis. It comprises:

- a header naming the winning model (e.g., *"3-Level REML"* or *"Random-Effects (REML)"*), with a green *AIC WINNER 🏆* badge if the AIC selection was used;
- a large gradient card displaying the pooled effect-size estimate $\hat{\mu}$ together with conventional significance asterisks (*** *p* < 0.001, ** *p* < 0.01, * *p* < 0.05, *ns* otherwise);
- a three-element information grid showing the confidence interval (at the user-selected level), the prediction interval for a future exchangeable study, and the *p*-value;
- a short model note stating the model description, the total number of observations *k* and the number of primary studies.

#### 7.5.2 📉 Heterogeneity

The second tab reports the heterogeneity assessment. A coloured badge classifies *I* ² according to the Higgins et al. (2003) bins. A table beneath the badge gives, with profile-likelihood CIs where applicable, *Q*, df(*Q*), *p*(*Q*); *I* ²; the estimated variance components (τ², τ, σ²) of the winning model; and the τ² estimation method (REML / DL / ML).

#### 7.5.3 ⚖️ Model Selection

The third tab supports model comparison and sensitivity. It displays a side-by-side table of the three candidate models — fixed-effect, two-level random-effects, three-level — each with its pooled estimate, confidence interval, and (for the latter two) the AIC. The model whose AIC is lowest is flagged as the AIC winner. Below the table, a small forest-plot-style visual sensitivity panel shows the pooled estimates from each model on a common axis, with the winner highlighted in green; this is the appropriate place to verify that the pooled estimate is not strongly sensitive to the choice of variance structure.

#### 7.5.4 ⚙️ Settings

The fourth tab contains the six configuration widgets described in Section 7.4 and the **Re-Run Analysis** button. An informational box at the bottom of the tab restates the effect-size column, variance column, number of observations, and number of primary studies that the model is operating on.

#### 7.5.5 📝 Publication Text

The fifth tab contains the automatically generated *Materials and Methods* and *Results* paragraphs, formatted to journal conventions (e.g., *d* = 0.42, 95 % CI [0.18, 0.66], *p* = .003). The text is conditional on the configuration: it adapts automatically to the model selected (two-level vs. three-level, including the τ²_within = 0 fallback narrative), the τ² estimator chosen, the use or non-use of the Knapp–Hartung adjustment, the imputation strategy applied in Cell 4 (where relevant), and the presence of shared-control VCV corrections from Cell 6. Cohen (1988) and Higgins et al. (2003) interpretation bins are applied automatically to the effect size and *I* ², respectively.

The generated text is provided for direct copy-and-paste into a manuscript draft. It should nevertheless be read carefully and edited for substantive narrative; CoMeta's responsibility is limited to ensuring numerical and methodological accuracy.

#### 7.5.6 💾 Export

The sixth tab exposes two download buttons:

- **📥 Download Excel Audit Report** writes a multi-sheet Excel workbook containing the full audit trail: the model settings, the heterogeneity statistics, the exclusion log accumulated by Cells 4 and 6, and the row-level effect-size table.
- **📥 Download Settings JSON** writes an `analysis_settings.json` file encoding the complete `ANALYSIS_CONFIG` dictionary. This file may be uploaded to a fresh Colab runtime via the *Restore Session* pathway of Cell 2 (§2.1.3) to reproduce the analysis exactly. Deposition of this file as supplementary material alongside a manuscript provides one-click reproducibility for any reader.

### 7.6 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, the six Settings widgets are auto-populated from the saved configuration on cell load, and **Re-Run Analysis** is invoked automatically. The Primary Result, Heterogeneity, and Model Selection tabs therefore reproduce the original analysis without any manual interaction.

### 7.7 Practical guidance

- **Default settings reflect a defensible convention, not a universal one.** REML with the Knapp–Hartung adjustment and *t*-based inference is the conventional default for ecological meta-analyses with a modest number of studies. Where the user's literature follows a different convention (e.g., DL with *z*-based inference for comparability with older syntheses), the relevant widgets should be adjusted before the result is reported.
- **The AIC winner is the model that the manuscript should report.** When the three-level structure is selected automatically, both τ² components and the prediction interval that incorporates them should be reported; this is done automatically in the generated *Results* text. When the data do not support a non-zero τ²_within, CoMeta reverts to the two-level model transparently and reports only τ²_between.
- **Refit before interpreting.** When any upstream change is made (e.g., a different imputation strategy in Cell 4 or a different effect-size metric in Cell 5), Cell 7 displays a staleness banner. The cell should be re-executed before any of the results in its tabs are read, and the corresponding downstream cells should likewise be refreshed.
- **Export the JSON file.** Regardless of whether the analysis is reported in a manuscript, the JSON session file is the only object that records every analytical decision (imputation, filtering, metric, model, knot placement, etc.) in a single human-readable artefact. Exporting it after every substantive change provides a safeguard against the Colab runtime timing out and losing the configuration.

### 7.8 Summary

Cell 7 fits three candidate meta-analytical models (fixed-effect, two-level random-effects, three-level hierarchical) by REML and reports the AIC-selected model with CR2 cluster-robust inference, Satterthwaite degrees of freedom, profile-likelihood confidence intervals for the variance components, and a prediction interval for a future exchangeable study. The user controls the analysis through six widgets in the **⚙️ Settings** tab (*Confidence Level:*, *Model Selection:*, *τ² Method:*, *Knapp-Hartung Correction*, *Inference:*, *Use Full Log-Likelihood*) and refits the model with **Re-Run Analysis**. Results are presented in six tabs — **📊 Primary Result**, **📉 Heterogeneity**, **⚖️ Model Selection**, **⚙️ Settings**, **📝 Publication Text**, **💾 Export** — and exported either as an Excel audit workbook or as a JSON session file. The fitted model is then consumed by Cells 8 – 25, beginning with the subgroup analyses described in Section 8.
