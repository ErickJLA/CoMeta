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

**Raw binary mode** — `id`, `events_e`, and `nonevents_e` are required; `events_c` and `nonevents_c` are required for two-group comparisons but may be omitted for single-group prevalence/incidence data (see note below):

| Field | Widget label | Description | Status |
|---|---|---|---|
| `id` | Study ID / Label | Unique identifier for the study or paper. | Required |
| `events_e` | Treatment Events (a) | Number of events in the Treatment group. | Required |
| `nonevents_e` | Treatment Non-Events (b) | Number of non-events in the Treatment group. | Required |
| `events_c` | Control Events (c) | Number of events in the Control group. | Required for two-group designs; omit for single-group data |
| `nonevents_c` | Control Non-Events (d) | Number of non-events in the Control group. | Required for two-group designs; omit for single-group data |

> **Single-group binary data.** CoMeta supports *single-group* binary designs in which only the treatment-arm (or single-group) event and non-event counts are available — for example, prevalence, incidence, or single-arm proportion meta-analyses. When the source dataset contains `events_e` and `nonevents_e` but no control event or non-event columns, Cell 5 automatically classifies the dataset as single-group binary and recommends the **Logit Proportion** metric (§5). The control-column dropdowns may be left empty in this case, or the corresponding columns may simply be absent from the source file.

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
id, events_e, nonevents_e, [events_c], [nonevents_c]
```

The control-arm columns `events_c` and `nonevents_c` are required for conventional two-group binary comparisons (log OR, log RR, Risk Difference). They may be omitted for *single-group* prevalence or incidence designs, in which case Cell 5 will recommend the Logit Proportion metric automatically.

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
| **Pure binary (two-group)** | All four binary columns (`events_e`, `nonevents_e`, `events_c`, `nonevents_c`) are present; continuous columns are absent. | **log Odds Ratio (log OR)** with *High* confidence; **log Risk Ratio (log RR)** and **Risk Difference (RD)** are reported as compatible alternatives. |
| **Single-group binary** | Only the treatment-arm binary columns (`events_e`, `nonevents_e`) are present; the control-arm columns (`events_c`, `nonevents_c`) are absent. | **Logit Proportion** with *Moderate* confidence. The data are logit-transformed to ensure that confidence intervals remain within the [0, 1] interval. |
| **Mixed** | Both binary and continuous columns are present. | A yellow ⚠️ ***Ambiguous Data Types Detected*** panel is displayed, advising the user to confirm the data type manually. Initial recommendation: **Hedges' *g*** with *Low* confidence. |
| **Pure continuous** | Continuous columns (`xe`, `xc`, and at least one SD column) are present. | Output of the weighted scoring engine (§5.2). |

The cell renders its output in three tabs:

| Tab | Label | Content |
|---|---|---|
| 1 | **💡 Recommendation** | The recommended metric, the rationale, the *Select Type:* radio group, and the **✓ Confirm Selection** button. |
| 2 | **📊 Data Patterns** | A diagnostic audit of the dataset's statistical topology: normalisation, negative values, zero values, scale heterogeneity, SD availability, and distribution shape. |
| 3 | **🧠 Decision Logic** | The row-by-row scoring table produced by the recommendation engine, together with the final per-metric point totals. |

### 5.2 The weighted scoring engine (R1–R6)

For pure-continuous datasets, the recommendation engine implements a **Weighted Scoring System** that compares four candidate continuous metrics — log Response Ratio (lnRR), Hedges' *g*, Mean Difference (MD), and log Coefficient of Variation Ratio (lnCVR) — by accumulating weighted points across six rules. The dataset's diagnostic features are computed first, and each rule contributes points to one or more metric scores. The metric with the highest total is reported as the recommendation; the difference in points between the top two contenders determines the stated confidence.

The scoring engine focuses on the dataset properties that govern the mathematical safety of each metric: data skewness, the presence of zeros or negative values, the proportion of exact 1.0 entries (indicative of pre-normalised fold-change data), SD coverage (which is essential for the *g*/MD/lnCVR variance formulae), and scale heterogeneity across studies. The intent is not to identify a single "correct" metric but to recommend the safest mathematical choice given the dataset's empirical features.

| Rule | Diagnostic | Decision threshold | Points awarded | Rationale |
|---|---|---|---|---|
| **R1** | Negative values present in `xe` or `xc` | any negative | Hedges' *g* +10; MD +3 | Log-ratio metrics (lnRR, lnCVR) are mathematically undefined for negative values. This rule operates as a near-hard constraint. |
|  | All values strictly positive | otherwise | lnRR +2; lnCVR +1 | Data are compatible with ratio-based metrics. |
| **R2** | Control values clustered at unity | > 50 % of `xc` exactly 1.0 | lnRR +5 | Pre-normalised fold-change data are already a ratio scale. |
|  |  | > 30 % of `xc` in [0.95, 1.05] | lnRR +3 | Strong evidence of normalisation. |
|  |  | mean(`xc`) ∈ (0.8, 1.2) | lnRR +1 | Weak evidence of a unity baseline. |
| **R3** | Scale heterogeneity (ratio of `xe` and `xc` ranges) | ratio > 100 | lnRR +3; lnCVR +1 | Heterogeneous scales are handled naturally by ratios; MD is *not* recommended in this regime. |
|  |  | ratio > 10 | lnRR +2 | Moderate scale variance still favours ratios. |
|  |  | otherwise | Hedges' *g* +1; MD +2 | Comparable scales support standardised and raw mean differences alike. |
| **R4** | Zero values present in `xe` or `xc` | any zero | Hedges' *g* +2 | log(0) is undefined; lnRR would require an additive constant. |
| **R5** | SD coverage | > 80 % of rows with valid SDs | Hedges' *g* +1; lnCVR +2 | Both metrics require complete SDs; lnCVR specifically requires SDs to compute the CV ratio. |
|  |  | < 20 % | Hedges' *g* −2; MD −2; lnCVR −5 (warning recorded) | SD imputation is unstable for variance-based metrics; the strong negative penalty for lnCVR reflects its direct dependence on the SD term. |
| **R6** | Maximum skewness of `xe` and `xc` | skew > 1.5 | lnRR +2 | Strong right-skew typical of multiplicative biological processes. |
|  |  | skew ∈ (−0.5, 0.5) | Hedges' *g* +1 | Approximately symmetric data fit the SMD assumptions. |

**Scale-dependence caveat.** When the recommender identifies MD or Hedges' *g* / Cohen's *d* (any *standardised* or *absolute* mean-difference metric) as the leading candidate, a **Scale Dependence Warning** is displayed beneath the recommendation. The warning advises the user that MD and SMD-class metrics implicitly assume that all studies were conducted at comparable *spatial and temporal* scales (e.g., plot size, experiment duration); if the constituent studies span vastly different scales, the pooled estimate may be biased and the user should consider including scale as a moderator in Cell 8 or Cell 12, or aggregating studies separately by scale stratum. The warning is purely advisory and does not alter the score.

**Tie-breaker.** If two totals are equal after R1–R6, the engine prefers lnRR when the dataset contains neither negative nor zero values (lnRR is preferred for strictly-positive ecological data because of its direct percentage-change interpretation), and Hedges' *g* otherwise.

**Confidence level.** Let *Δ* be the absolute difference between the top two metric totals. The reported confidence is:

| Confidence | Condition |
|---|---|
| **High** | *Δ* ≥ 5 |
| **Moderate** | 3 ≤ *Δ* < 5 |
| **Low** | *Δ* < 3 |

The full scoring table — each rule that fired, the metric it favoured, the weight (encoded as plus-signs), and a one-line educational note — is displayed in the **🧠 Decision Logic** tab. The final per-metric point totals are shown beneath the table.

For **pure-binary** topologies, a parallel scoring routine evaluates the three binary candidates (log OR, log RR, Risk Difference) and reports log OR as the default high-confidence recommendation, with log RR and RD listed as compatible alternatives. For **single-group binary** topologies, the engine bypasses competitive scoring and recommends Logit Proportion directly.

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

The **💡 Recommendation** tab displays a coloured banner naming the recommended metric and a one-sentence rationale, followed by a *Select Type:* radio group containing the nine effect sizes supported in raw mode:

| Option label | Internal code | Compatible data |
|---|---|---|
| **log Response Ratio (lnRR) — for ratio/fold-change data** | `lnRR` | Continuous (strictly positive) |
| **Hedges' *g* — for standardized mean differences (corrected)** | `hedges_g` | Continuous |
| **Cohen's *d* — for standardized mean differences (uncorrected)** | `cohen_d` | Continuous |
| **Mean Difference (MD) — for raw, unstandardized differences** | `MD` | Continuous, identical units across studies |
| **log Coefficient of Variation Ratio (lnCVR) — for variability** | `lnCVR` | Continuous (strictly positive), full SDs available |
| **log Odds Ratio (log OR) — for binary outcome data** | `log_or` | Binary (two-group) |
| **log Risk Ratio (log RR) — for binary outcome data** | `log_rr` | Binary (two-group) |
| **Risk Difference (RD) — absolute risk change** | `risk_diff` | Binary (two-group) |
| **Logit Proportion — for single-group prevalence** | `proportion` | Binary (single-group) |

**Definitions of the Mean Difference, lnCVR, Risk Difference, and Logit Proportion metrics.**

- **Mean Difference (MD)** — the raw, unstandardised difference between the treatment and control means, $\hat{\mu} = \bar{x}_e - \bar{x}_c$. MD is directly interpretable in the units of the original measurement and does not standardise by within-study variability. **User note:** MD is only appropriate when *all* constituent studies measure the outcome on the exact same scale and unit (e.g., grams of biomass, °C of temperature change); a meta-analysis of MDs across heterogeneous units is not meaningful. If the user is unsure whether their dataset satisfies this assumption, Hedges' *g* is the safer default.
- **log Coefficient of Variation Ratio (lnCVR)** — the natural log of the ratio of the coefficients of variation of the treatment and control groups (Nakagawa et al., 2015). Whereas lnRR detects changes in the mean, lnCVR detects whether a treatment alters the *variability* of an outcome relative to its mean. **User note:** lnCVR is particularly useful for ecological and evolutionary studies in which a treatment may stabilise or destabilise a response without changing its central tendency. The small-sample bias correction of Nakagawa et al. (2015) is applied automatically.
- **Risk Difference (RD)** — the absolute difference in event probabilities, $\hat{\mu} = p_e - p_c$, where $p_e = a/(a+b)$ and $p_c = c/(c+d)$. RD is highly interpretable (e.g., "a 5 % absolute reduction in mortality") but its sampling variance is unstable when probabilities approach the boundaries 0 or 1. **User note:** prefer log OR or log RR for rare outcomes; reserve RD for outcomes in the moderate-prevalence range (0.1 – 0.9).
- **Logit Proportion** — the logit transformation of a single-group event probability, $\hat{\mu} = \ln(\hat p / (1 - \hat p))$, with the Haldane–Anscombe continuity correction applied to zero or one-valued cells. **User note:** the data are logit-transformed (rather than analysed on the proportion scale directly) to ensure that the model-implied confidence intervals remain within the [0, 1] interval after back-transformation. Logit Proportion is the appropriate metric for single-group prevalence, incidence, or single-arm proportion meta-analyses; the back-transformed proportion and its CI are reported alongside the logit estimate in Cell 6.

The radio button is pre-selected to the engine's recommendation. The user may switch freely between options; CoMeta runs a compatibility check on every change and reacts as follows:

- If the chosen metric is compatible with the dataset's topology, the *About* panel beneath the radio group describes the metric in one short paragraph (e.g., for Hedges' *g*: *"A variation of Cohen's d that includes a correction factor (J) for small sample sizes …"*), and the action button remains enabled and labelled **✓ Confirm Selection**.
- If the chosen metric is incompatible with the dataset (for example, *log OR* selected on a continuous-only dataset, or *Hedges' *g** selected on a pure-binary dataset), a red ❌ ***INCOMPATIBLE DATA*** panel is displayed, the action button is disabled, and its label switches to **✗ Invalid Selection**. The user must choose a compatible metric before proceeding.

Clicking **✓ Confirm Selection** writes the choice to `ANALYSIS_CONFIG['effect_size_type']` together with the corresponding `es_config` record (internal column names that Cell 6 will create — for example, `lnRR`, `var_lnRR`, `SE_lnRR`, `CI_lower_lnRR`, `CI_upper_lnRR`). A green ✅ ***Configuration Saved*** banner confirms the action and directs the user to Cell 6. Downstream cells are marked stale.

### 5.5 Pre-calculated mode: manual declaration

When the data type is `pre_calculated`, the cell does not perform a topology audit. Instead, it renders a yellow informational panel — ***📊 Pre-calculated Effect Size Mode*** — and exposes a single *Effect Size Type:* dropdown containing the metrics that the pipeline can interpret as already computed:

| Option label | Internal code |
|---|---|
| **Hedges' g (Standardized Mean Difference)** | `hedges_g` |
| **log Response Ratio (lnRR)** | `lnRR` |
| **Mean Difference (MD)** | `MD` |
| **log Coefficient of Variation Ratio (lnCVR)** | `lnCVR` |
| **log Odds Ratio (logOR)** | `log_or` |
| **log Risk Ratio (logRR)** | `log_rr` |
| **Risk Difference (RD)** | `risk_diff` |
| **Logit Proportion** | `proportion` |
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

Cell 5 fixes the effect-size metric for the remainder of the pipeline. In raw mode, a weighted scoring engine evaluates six topological diagnostics and proposes one of nine supported metrics — lnRR, Hedges' *g*, Cohen's *d*, Mean Difference, lnCVR, log OR, log RR, Risk Difference, or Logit Proportion — with the reasoning surfaced in the **📊 Data Patterns** and **🧠 Decision Logic** tabs; the user accepts or overrides the recommendation via the *Select Type:* radio group, subject to a compatibility check, and clicks **✓ Confirm Selection**. In pre-calculated mode, the user declares the metric via the *Effect Size Type:* dropdown and clicks **✓ Confirm Effect Size Type**. In both cases, successful confirmation hands off to Cell 6 (Effect Size Calculation), described in Section 6.

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

**Log Coefficient of Variation Ratio (lnCVR).** lnCVR is undefined for non-positive means and for zero standard deviations:

- Rows in which `xe <= 0` or `xc <= 0` are removed.
- Rows in which `sde == 0` or `sdc == 0` after the imputation performed in Cell 4 are removed; the reason recorded is *"Zero SD After Imputation (lnCVR Undefined)"*.

**Log odds ratio (log OR), log risk ratio (log RR), and Risk Difference (RD).** For 2 × 2 contingency-table data:

- **Double-zero studies** — studies in which both `events_e == 0` and `events_c == 0` — are uninformative for relative effects and are removed; the reason recorded is *"Double-Zero Event Count (Uninformative)"*.
- **Single-zero studies** — studies in which any one of `events_e`, `nonevents_e`, `events_c`, `nonevents_c` equals zero — are corrected by the standard **Haldane–Anscombe continuity correction**: 0.5 is added to all four cells of the affected 2 × 2 table. The same correction is applied to RD to stabilise the variance estimate at the boundaries.

**Logit Proportion.** For single-group binary data:

- Rows in which either `events_e == 0` or `nonevents_e == 0` are corrected by adding 0.5 to both cells (Haldane–Anscombe), so that the logit is finite and its asymptotic variance is well-defined.
- Rows with missing event or non-event counts are removed and tagged *"Missing Essential Data (Single-Group Binary)"*.

**Mean Difference (MD), Hedges' *g*, Cohen's *d***. No additional row-level cleaning is performed; rows that produce NaN effect sizes or non-finite variances after the calculation in §6.3 are removed and tagged with the reason *"Calculation Failed (Missing Data/NaN)"* or *"Zero or Negative Variance"*.

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

**Mean Difference (MD).** The raw, unstandardised mean difference and its sampling variance are

$$ \mathrm{MD} = \bar{x}_e - \bar{x}_c, \qquad \mathrm{Var}(\mathrm{MD}) = \frac{s_e^{2}}{n_e} + \frac{s_c^{2}}{n_c}. $$

The MD has the same units as the original outcome and is reported on the natural scale; no back-transformation is applied.

**Log Coefficient of Variation Ratio (lnCVR).** Following Nakagawa et al. (2015), the bias-corrected lnCVR and its variance are

$$ \mathrm{lnCVR} = \Bigl[\ln\!\bigl(s_e / |\bar{x}_e|\bigr) + \tfrac{1}{2(n_e - 1)}\Bigr] - \Bigl[\ln\!\bigl(s_c / |\bar{x}_c|\bigr) + \tfrac{1}{2(n_c - 1)}\Bigr], $$

$$ \mathrm{Var}(\mathrm{lnCVR}) = \frac{s_e^{2}}{n_e\,\bar{x}_e^{2}} + \frac{1}{2(n_e - 1)} + \frac{s_c^{2}}{n_c\,\bar{x}_c^{2}} + \frac{1}{2(n_c - 1)}. $$

The additive $1/[2(n-1)]$ terms are the small-sample bias correction for log-CVs derived by Nakagawa et al. (2015). The back-transformed Coefficient of Variation Ratio (exp lnCVR) is stored alongside as an interpretive aid.

**Risk Difference (RD).** Let $p_e = a/(a+b)$ and $p_c = c/(c+d)$ be the event probabilities in the two arms. Then

$$ \mathrm{RD} = p_e - p_c, \qquad \mathrm{Var}(\mathrm{RD}) = \frac{p_e\,(1 - p_e)}{a + b} + \frac{p_c\,(1 - p_c)}{c + d}. $$

RD is reported on its natural scale (an absolute probability difference); no back-transformation is applied.

**Logit Proportion (single-group binary).** Let $a$ and $b$ denote the event and non-event counts in the single group (with the Haldane–Anscombe correction of $+0.5$ applied when either cell is zero). Then

$$ \mathrm{logit\_p} = \ln\!\bigl(a / b\bigr), \qquad \mathrm{Var}(\mathrm{logit\_p}) = \frac{1}{a} + \frac{1}{b}. $$

The back-transformed proportion $\hat p = \mathrm{expit}(\mathrm{logit\_p}) = a / (a + b)$ and its confidence interval (obtained by transforming the logit-scale CI endpoints) are stored alongside, ensuring that the reported interval lies entirely within [0, 1].

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
| **lnCVR** | $s_c^{2} / (n_c\,\bar{x}_c^{2}) + 1 / [2\,(n_c - 1)]$ | Nakagawa et al. (2015); adds the log-CV bias-correction covariance to the lnRR shared-control term. |
| **Cohen's *d*** | $\tfrac{1}{n_c} + \tfrac{d_i\,d_j\,n_c}{2\,N_i\,N_j}$ with $N_k = n_{e,k} + n_c$ | Gleser & Olkin (2009), Table 4. |
| **Hedges' *g*** | $J_i\,J_j\,\bigl[\tfrac{1}{n_c} + \tfrac{d_i\,d_j\,n_c}{2\,N_i\,N_j}\bigr]$, with *d* back-derived from *g* via *J* | Gleser & Olkin (2009); the *J* factor uses exact log-gamma. |
| **MD** | $s_c^{2} / n_c$ | Standard expression for the shared-control component of a raw mean difference. |
| **log OR** | $\tfrac{1}{c} + \tfrac{1}{d}$ (where *c*, *d* are the control-arm event and non-event counts) | Gleser & Olkin (2009). |
| **log RR** | $\tfrac{1}{c} - \tfrac{1}{n_c}$, with $n_c = c + d$ | Gleser & Olkin (2009). |
| **Risk Difference (RD)** | $p_c\,(1 - p_c) / n_c$, with $p_c = c/(c+d)$ | Standard expression for the shared-control component of a risk difference. |

Single-group binary designs (Logit Proportion) do not contain a control arm and therefore admit no shared-control covariance; the per-study **Σ**ᵢ for these datasets is purely diagonal.

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
  | lnRR, lnCVR, log OR, log RR | < 0.1 | 0.1 – 0.3 | 0.3 – 0.5 | > 0.5 |
  | MD, RD, Logit Proportion | (interpreted on the natural scale of the outcome or probability; no fixed benchmarks are applied) | | | |

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

Cell 6 computes, per record, the effect size and sampling variance for the metric chosen in Cell 5 — one of nine supported metrics: lnRR, Hedges' *g*, Cohen's *d*, Mean Difference, lnCVR, log OR, log RR, Risk Difference, or Logit Proportion — applying the metric-specific cleaning rules required to keep the calculation well-defined (lnRR zero-offset; lnCVR positivity and SD checks; binary double-zero drop and Haldane–Anscombe correction; single-group binary continuity correction for Logit Proportion). For every primary study, it builds the variance–covariance matrix that encodes within-study sampling dependence among effect sizes that share a control group, using the Gleser & Olkin (2009), Lajeunesse (2011), and Nakagawa et al. (2015) closed-form expressions. The cell renders a five-tab diagnostic interface — **📊 Summary**, **📉 Diagnostics**, **📏 Detailed Stats**, **🧠 Interpretation**, **🗑️ Removed Data** — that should be inspected before proceeding to Cell 7 (Overall Meta-Analysis), described in Section 7.

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

---

## Section 8. Subgroup Analysis Configuration

Cell 8, titled **⚙️ 8. Subgroup Analysis: Configuration**, sets up — but does **not** execute — the subgroup analyses to be run by Cell 9. It exposes a four-tab interface in which the user (i) chooses between a single-factor and a two-factor subgroup design, (ii) selects the moderator (or pair of moderators) on which the groups are defined, (iii) specifies the minimum-data thresholds that each group must satisfy in order to be included, and (iv) inspects the distribution of records across groups before committing to the configuration. The cell validates the user's selections and writes them to `ANALYSIS_CONFIG['subgroup_config']`; Cell 9 then fits a separate three-level REML model for each retained group, using exactly the same inference machinery as Cell 7 (CR2 cluster-robust standard errors, Satterthwaite degrees of freedom, Knapp–Hartung adjustment where enabled).

The cell is executed by clicking its **▶ Run** button. It initialises by reading the analytical dataset from `ANALYSIS_CONFIG['analysis_data']`, auto-detecting the columns that may serve as moderators, and rendering the four tabs.

### 8.1 Moderator auto-detection

CoMeta searches the analytical dataset for columns that can plausibly act as categorical moderators. A column is recognised as a moderator when any of the following conditions is true:

- the column has dtype `object` (i.e., free-text or string values);
- the column has a pandas `Categorical` dtype;
- the column is numeric but has fewer than 20 unique values and more than one unique value (e.g., publication year, study quality grade, or an ordinal habitat code).

Core analytical columns (`xe`, `sde`, `ne`, `xc`, `sdc`, `nc`, `id`, the chosen effect-size column, its variance, standard error, confidence-interval bounds, and any auxiliary columns added by Cells 4 – 6 such as `sde_imputed`, `Response_Ratio`, `Odds_Ratio`, `Percent_Change`, `df`, `J`, etc.) are excluded automatically. The detected list is reported in the **📝 Details** tab and used to populate the moderator dropdowns described in §8.2. If no moderator columns are detected, the cell renders a red initialisation-error panel instructing the user to verify that the dataset contains categorical columns; in that case, the subgroup pipeline cannot be used and the analysis should proceed directly to Cell 12 (Meta-Regression).

### 8.2 Tab 1 — 📋 Configuration

The first tab is the principal configuration panel. It presents four numbered sections:

1. **Select Analysis Type.** A radio group with two options:

   | Option label | Internal value | Description |
   |---|---|---|
   | **Single-Factor Analysis** | `single` | One moderator partitions the dataset into mutually exclusive groups; an independent three-level REML model is fitted within each group. Recommended for primary hypotheses with ≥ 10 observations per group. |
   | **Two-Factor Analysis (Interaction)** | `two_way` | Two moderators are crossed; an independent model is fitted in each non-empty cell of the resulting contingency table. Recommended only when 3 – 5 studies are available per cell and ≥ 20 observations are available overall. |

2. **Select Moderator(s).** A *Moderator 1:* dropdown listing every auto-detected moderator. When the analysis type is *two-way*, a *Moderator 2:* dropdown appears below; its first option is *None*, and the two moderators must be distinct.

3. **Set Quality Thresholds.** A read-only summary of the *Min Papers:* and *Min Observations:* slider values, with a pointer to the **⚙️ Thresholds** tab where they may be adjusted (see §8.4).

4. **Save Configuration.** The **💾 Save Configuration & Proceed** button writes the configuration to memory and triggers the validation described in §8.5.

Every change to the analysis-type, moderator, or threshold widgets is observed: the **📊 Moderator Preview** and **⚙️ Thresholds** tabs are updated automatically so that the user can iterate on the configuration before committing.

### 8.3 Tab 2 — 📊 Moderator Preview

This tab summarises the empirical distribution of records across the selected moderator categories *before* the quality thresholds are applied. For the primary moderator, the cell reports a per-category table with four columns:

| Column | Description |
|---|---|
| **Category** | Distinct value of the moderator. |
| **Observations** | Number of effect-size records in the category. |
| **Papers** | Number of primary studies (distinct `id` values) contributing to the category. |
| **Percent** | Observations as a percentage of the analytical dataset. |

Rows for categories with fewer than five observations are shaded yellow to flag potentially under-powered groups. A coloured banner beneath the table summarises whether all categories meet the conventional five-observation rule of thumb.

When the analysis type is *two-way*, the per-category table is repeated for the secondary moderator and is followed by a *Combination Matrix: Moderator 1 × Moderator 2* — a colour-graded cross-tabulation of observation counts. The cell counts empty combinations (which will be dropped), flags any combination with fewer than three records, and warns when the minimum-cell count is below five. These visual checks are the principal safeguard against fitting a two-way subgroup model to a sparse contingency table.

### 8.4 Tab 3 — ⚙️ Thresholds

This tab exposes the two minimum-data sliders that determine which groups are retained:

| Widget label | Type | Range | Default |
|---|---|---|---|
| **Min Papers:** | IntSlider | 1 – 10 (step 1) | 3 |
| **Min Observations:** | IntSlider | 2 – 20 (step 1) | 5 |

A group (or, in two-way mode, a cell of the combination matrix) is retained in the analysis only if it contains **at least *Min Papers* distinct primary studies *and* at least *Min Observations* effect-size records**. Setting either threshold higher yields fewer but better-estimated groups; setting either lower yields more groups but increases the risk of unstable estimates.

Below the sliders, an *Impact on Data Retention* section reports, in real time, the consequence of the current thresholds:

- A green panel headed **✓ Groups Meeting Criteria** lists every group that would be retained, with its observation count and paper count.
- A red panel headed **✗ Groups Excluded** lists every group that would be dropped, together with the reason (fewer than *Min Papers* studies, fewer than *Min Observations* records, or both).

The user is therefore able to choose threshold values with full visibility of which groups will and will not survive, without having to refit the model.

### 8.5 Saving the configuration

Clicking **💾 Save Configuration & Proceed** triggers the following sequence:

1. **Validation.** The configuration is rejected, with a red ❌ ***Validation Failed*** panel listing the offending conditions, if any of the following hold:
   - the analysis type is *two-way* but *Moderator 2:* is left at *None*;
   - *Moderator 1:* and *Moderator 2:* are the same column;
   - fewer than two groups satisfy the quality thresholds, in which case a subgroup analysis is not well-defined.
2. **Persistence.** On successful validation, the configuration is written to `ANALYSIS_CONFIG['subgroup_config']` as a dictionary recording: the analysis type, the names of the chosen moderator(s), the number of categories in each moderator (and their values), the threshold values, the list of valid groups, the count and percentage of records retained, and (in two-way mode) the number of empty cells in the combination matrix.
3. **Confirmation.** A green ✓ ***Configuration Saved Successfully*** panel summarises the saved configuration (analysis type, primary moderator, secondary moderator if applicable, number of valid groups, and the proportion of the analytical dataset retained) and directs the user to Cell 9. The **📝 Details** tab is simultaneously updated with a timestamped record of the saved configuration.
4. **Staleness propagation.** The subgroup-analysis and plotting downstream cells (Cells 9 – 11) are marked stale; they will need to be re-executed to reflect the new configuration.

### 8.6 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, the analysis-type radio group, the *Moderator 1:* and *Moderator 2:* dropdowns, and the two threshold sliders are auto-populated from the saved configuration, and **💾 Save Configuration & Proceed** is invoked automatically. A blue **🔄 Reproducibility Mode Active** notice at the top of the cell reports the analysis type and the moderator(s) being restored. No manual interaction is required.

### 8.7 Practical guidance

- **Use the Moderator Preview tab before adjusting thresholds.** Small categories — those that the *⚠️ Smallest group* warning flags — should be inspected case-by-case. They may represent legitimate but under-sampled levels of a factor (in which case higher thresholds will appropriately exclude them) or coding errors in the source spreadsheet (in which case they should be reconciled upstream in Cell 2 before re-running this configuration).
- **Two-way subgroup analyses are demanding.** Cell 9 fits a separate three-level REML model per cell of the contingency table. In typical ecological datasets — even relatively well-resourced ones — many cells will contain too few records to support a stable estimate. The *Combination Matrix* in the **📊 Moderator Preview** tab and the *Groups Excluded* list in the **⚙️ Thresholds** tab should both be consulted before committing to a two-way design. When the resulting valid-group count is small, the conclusions of the analysis are driven by the few populated cells and should be reported with explicit caveats.
- **Subgroups versus meta-regression.** A subgroup analysis is appropriate for categorical moderators whose levels are of intrinsic substantive interest (e.g., taxonomic clade, biome, experimental design). For continuous moderators, or for moderators with many levels, meta-regression (Cell 12) and spline meta-regression (Cell 14) are the appropriate tools.
- **The cell saves but does not fit.** No model is estimated in Cell 8. The Cell 9 execution, with the corresponding per-group estimates, heterogeneity statistics, between-group tests, and automatic interpretation, is described in Section 9.

### 8.8 Summary

Cell 8 configures the subgroup analysis without executing it. The user selects the analysis type from the *Analysis Type* radio group, the moderator(s) from the *Moderator 1:* and (when applicable) *Moderator 2:* dropdowns, and the minimum-data thresholds (*Min Papers:* and *Min Observations:*) from the IntSliders in the **⚙️ Thresholds** tab. The **📊 Moderator Preview** and *Impact on Data Retention* panels report, in real time, which categories or combinations will be retained under the current configuration. Clicking **💾 Save Configuration & Proceed** validates the selection, persists it to `ANALYSIS_CONFIG['subgroup_config']`, and hands off to Cell 9 (Subgroup Analysis Execution), described in Section 9.

---

## Section 9. Subgroup Analysis Execution

Cell 9, titled **🔬 9. Subgroup Analysis: Execution**, fits the subgroup analysis configured in Cell 8. For a single-factor design it fits one three-level REML model per level of the chosen moderator; for a two-factor design it fits one model per non-empty cell of the cross-tabulation of the two moderators. The cell additionally computes the omnibus Wald test of subgroup differences (*Q*_M), partitions the total heterogeneity *Q*_T into between- and within-group components (*Q*_M and *Q*_E), reports the proportion of total heterogeneity explained by the moderator (pseudo-*R* ²), and generates a manuscript-ready paragraph adapted to the configuration. As in Cell 7, the per-group inference uses the CR2 cluster-robust standard error with Satterthwaite degrees of freedom, and applies the Knapp–Hartung adjustment when the corresponding option was enabled in Cell 7.

Cell 9 has no user-input widgets beyond the two export buttons described in §9.6. It is executed by clicking its **▶ Run** button, and the analysis runs against (i) the configuration saved by Cell 8 (`ANALYSIS_CONFIG['subgroup_config']`) and (ii) the global analytical settings recorded by Cell 7 (`ANALYSIS_CONFIG['global_settings']`: α, distribution type, τ² estimator, Knapp–Hartung flag, model-selection rule). To change either of these inputs, the user returns to the relevant upstream cell, re-saves, and re-executes Cell 9.

### 9.1 Per-group model and the fallback hierarchy

For each retained group, CoMeta first attempts to fit a full three-level REML model. When the within-group dataset includes records that share a control group (carrying a non-trivial `shared_group_id` from Cell 4), the corresponding off-diagonal entries of the per-study **V**ᵢ block are populated from the VCV matrices constructed by Cell 6; this is reported in the results table as the model type **3L-VCV**. When no shared controls are present within the group, the model uses a diagonal **V**ᵢ and is reported as **3L-Diag**. If the optimisation does not converge, or if the estimated τ²_within collapses to the lower boundary, the engine falls back to a two-level random-effects model (reported as **2L**) and proceeds without raising an error. The model type that was actually fitted for each group is therefore visible in the right-hand column of the results table (§9.2).

If the joint three-level model — in which all groups share a common variance structure with group-specific means — fails to converge, the engine reverts to fitting an independent model per group and sets the `fallback_used` flag. The use of the fallback is reported transparently both as a yellow notice in the **📝 Publication Text** tab and in the autogenerated *Materials and Methods* paragraph.

### 9.2 Tab 1 — 📊 Results Summary

The first tab displays the headline result of the subgroup analysis in two parts:

**Summary card.** A single block reports the moderator (or pair of moderators) on which the analysis was run, the number of subgroups analysed, the **Test for Subgroup Differences** as a Wald statistic *Q*_M with its degrees of freedom and *p*-value, the **Variance Explained (Pseudo-*R*²)** as a percentage of the total heterogeneity that the moderator accounts for, and the residual heterogeneity components τ² and σ² of the joint model.

**Results table.** One row per subgroup, with the following columns:

| Column | Content |
|---|---|
| **Subgroup** | Category label of the moderator (or pair of categories for two-way designs). |
| **k** | Number of effect-size records in the subgroup. |
| **Studies** | Number of distinct primary studies (`id` values) in the subgroup. |
| **Effect** | Pooled effect size for the subgroup, with conventional significance asterisks (*** *p* < 0.001, ** *p* < 0.01, * *p* < 0.05). |
| **CI** | Confidence interval at the level selected in Cell 7 (default 95 %). |
| **PI** | Prediction interval for a future exchangeable study within the subgroup. |
| ***p*-value** | *p*-value for the test that the subgroup mean equals the null value. |
| **Model** | Model type actually fitted: **3L-VCV** (three-level with shared-control correction), **3L-Diag** (three-level with diagonal sampling variance), or **2L** (two-level fallback). |

Two legends — a significance legend (the meaning of the asterisks and *ns*) and a model-type legend (the meaning of 3L-VCV, 3L-Diag, 2L) — are displayed beneath the table.

### 9.3 Tab 2 — 📉 Heterogeneity

The second tab decomposes the heterogeneity across the subgroup structure. A short explanatory block describes the four quantities reported, after which a table presents the decomposition:

| Component | Notation | Interpretation |
|---|---|---|
| **Total** | *Q*_T | Overall heterogeneity across all retained records. |
| **Between-Groups** | *Q*_M | Heterogeneity attributable to the moderator. Reported with df and *p*-value; significance asterisks are applied when *p* < 0.05. |
| **Within-Groups** | *Q*_E | Residual heterogeneity within subgroups, after accounting for the moderator. |

Below the decomposition table, a coloured card reports the pseudo-*R* ² and its qualitative interpretation, which CoMeta classifies into one of three bins:

| Pseudo-*R* ² | Label |
|---|---|
| < 25 % | Low explanatory power |
| 25 % – 50 % | Moderate explanatory power |
| ≥ 50 % | High explanatory power |

The pseudo-*R* ² is a description of the variance partition for the present moderator, not a measure of out-of-sample predictive accuracy; it should be reported in those terms.

### 9.4 Tab 3 — ⏱️ Processing Log

The third tab streams the real-time diagnostic output of the per-group optimisation engine: convergence status, the chosen variance estimator, the activation of any fallback path, and any numerical warnings encountered during the fits. The log is intended for diagnostic inspection when an unexpected result appears in the **📊 Results Summary** tab and is the appropriate place to identify groups whose fits triggered a fallback.

### 9.5 Tab 4 — ⚙️ Configuration

The fourth tab records the configuration under which the present analysis was run, for traceability. It reports the timestamp; the analysis type; the moderator(s); the number of subgroups; the internal effect-size and variance column names; the α level and the corresponding confidence-interval percentage; the distribution used for inference (*t* or *z*); and the total number of observations and primary studies that entered the analysis. A green confirmation note states that all prerequisites have been met.

### 9.6 Tab 5 — 📝 Publication Text

The fifth tab contains the automatically generated *Materials and Methods* and *Results* paragraphs describing the subgroup analysis. The text adapts to the chosen design (single- vs. two-factor), to the model type actually fitted, and — when the per-group joint-model fallback was triggered — to the use of independent group-wise models. In the latter case, a yellow ⚠️ notice precedes the text:

> ⚠️ **Note:** The text below has been automatically adjusted to reflect that independent models were used due to convergence constraints.

As elsewhere in CoMeta, the generated text is intended for direct copy-and-paste into a manuscript draft but should be read carefully and edited for substantive narrative.

### 9.7 Tab 6 — 💾 Export

The sixth tab exposes two download buttons:

- **📥 Download Subgroup Report** writes an Excel workbook containing the subgroup table, the heterogeneity decomposition, and the per-group analytical data.
- **📥 Download Settings JSON** writes the same `analysis_settings.json` file as in Cell 7, with the subgroup configuration now included; restoring this file via Cell 2's *Restore Session* pathway reproduces the present subgroup analysis verbatim.

### 9.8 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, Cell 9 executes automatically using the restored configuration. No manual interaction is required, and the six tabs are populated as if the user had just configured and run the analysis interactively.

### 9.9 Practical guidance

- **Report the Q_M test, not the per-group p-values.** The test of subgroup differences in a meta-analysis is *Q*_M, not the collection of within-group *p*-values. A subgroup mean that is statistically significant in isolation does not imply that the moderator explains heterogeneity in the pooled effect; the conclusion that subgroups differ is supported by a significant *Q*_M (preferably interpreted alongside the pseudo-*R* ²) rather than by counting which subgroups are individually "significant".
- **Inspect the model-type column.** When a substantial proportion of groups fell back to **2L** or triggered the joint-model fallback (yellow notice in the publication tab), the conclusions of the analysis are conditional on those fallbacks. The manuscript should report the model type per subgroup and acknowledge the convergence behaviour.
- **Pseudo-*R*² is a descriptive partition.** The reported pseudo-*R* ² is a within-sample summary; values close to 100 % do not imply that the moderator would predict the effect of a future study to that precision. The prediction-interval column in the results table is the relevant device for that purpose.
- **Two-way designs require explicit caveats.** When a two-factor analysis was selected in Cell 8, the per-cell estimates frequently rest on a small number of records. The PI column will widen accordingly. The conclusions should be framed in terms of the populated cells of the design, not in terms of an unobserved factorial structure.

### 9.10 Summary

Cell 9 fits one three-level REML model per subgroup defined in Cell 8, using the CR2 cluster-robust inference machinery of Cell 7. The cell tries the full 3L-VCV / 3L-Diag specification first and falls back transparently to a 2L model when convergence fails; the model type actually fitted for each subgroup is reported in the results table. The omnibus test of subgroup differences (*Q*_M), the heterogeneity decomposition (*Q*_M / *Q*_E), and the pseudo-*R* ² are reported in dedicated tabs alongside per-subgroup pooled estimates, confidence intervals, prediction intervals, and an autogenerated *Materials and Methods* / *Results* paragraph. Excel and JSON exports are provided. The fitted subgroup result is consumed by the forest- and orchard-plot renderers in Cells 10 and 11, described in Section 10.

---

## Section 10. Subgroup Visualisation: Forest and Orchard Plots

Cells 10 and 11 produce the two complementary publication-ready visualisations of the subgroup analysis fitted in Cell 9:

- **Cell 10 — 📊 *10. Subgroup Analysis: Visualization - Forest Plot*** renders a conventional forest plot with one row per retained subgroup. Each row displays the pooled effect size as a marker, the confidence interval as a horizontal line, the prediction interval as a thinner outer line, and a textual annotation listing the number of observations, the number of contributing papers, and (optionally) the back-transformed fold change.
- **Cell 11 — 🍎 *11. Subgroup Analysis: Visualization - Orchard Plot*** renders the orchard plot of Nakagawa et al. (2021): one column (or row) per retained subgroup, with the per-record effect sizes drawn as semi-transparent "fruit" — sized in proportion to the inverse-variance weight — alongside the pooled estimate (the central marker), the confidence interval (the inner thick line), and the prediction interval (the outer thinner line acting as the "trunk"). The orchard plot supplements the pooled estimates of the forest plot with a visualisation of the within-subgroup distribution of records.

Both cells are pure renderers: they read the configuration and results saved by Cell 9, expose a multi-tab customisation interface for the plot's typographic and aesthetic properties, and produce the final image only when the user clicks the corresponding **Generate Plot** button. Neither cell modifies the fitted model.

### 10.1 Common architecture

Both cells follow the same operational pattern:

1. On execution, the cell reads `ANALYSIS_CONFIG['subgroup_results']` (and the upstream effect-size configuration) and renders a *Tab* widget containing the customisation panels described below.
2. The user adjusts the widgets to suit the journal's typographic conventions and the manuscript's narrative. All customisations are queued — no re-rendering occurs while the user is editing.
3. Clicking the **📊 Generate Forest Plot** (Cell 10) or **🌳 Generate Orchard Plot** (Cell 11) button renders the figure in the cell's output area using the current settings.
4. If the corresponding *Save …* checkboxes are enabled in the **💾 Export** tab, the figure is simultaneously written to disk in the requested formats (PDF, PNG, and — for Cell 11 — SVG). The image files are saved to the active Colab session's local filesystem and can be downloaded via the Files pane in the Colab side-bar.
5. A dynamically generated figure caption is produced in the **📝 Caption** tab and updates automatically with every plot regeneration; it is intended for direct copy-paste into the manuscript.

The cells are independent — the user may generate one, both, or neither — but they share the same fitted result and so will always agree numerically. Because both cells are downstream of Cell 9, any change to the subgroup configuration (Cell 8) or the overall analytical settings (Cell 7) requires Cell 9 to be re-executed before either visualisation will reflect the new model.

### 10.2 Cell 10 — Forest Plot

The forest plot is the conventional summary figure for a subgroup meta-analysis. Cell 10 exposes seven tabs:

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Choice of model (Random-Effects / Fixed-Effects), plot dimensions, typography sizes, colour scheme, marker style, and confidence-interval line style. |
| 2 | **📝 Text** | Plot title, *x*-axis label, *y*-axis label, and toggles for whether each label is displayed. |
| 3 | **🏷️ Annotations** | Row-level annotations: *k* (observations), number of papers, fold-change (lnRR only); annotation position (right / above / below) and offsets; group-label placement for two-way designs. |
| 4 | **📏 Axes** | *x*-axis auto-scaling (or explicit minimum and maximum), gridline visibility and style, null-effect reference line, and the optional fold-change top axis for log-scale metrics. |
| 5 | **💾 Export** | *Save as PDF* and *Save as PNG* checkboxes, PNG DPI (default 300), transparent-background toggle, and a filename prefix. |
| 6 | **✏️ Labels** | A label-editor pane in which the user may override the display name of every retained subgroup (and of the *Overall* row) without modifying the source dataset. Useful for converting machine-readable codes (e.g., `GYMNO`) into manuscript labels (e.g., *Gymnosperms*). |
| 7 | **📝 Caption** | The dynamically generated figure caption, refreshed on every plot regeneration. |

**Key widgets in the 🎨 Style tab.**

| Widget | Type | Options / range | Default |
|---|---|---|---|
| **Model:** | dropdown | *Random-Effects*, *Fixed-Effects* | Random-Effects |
| **Plot Width (in):** | FloatSlider | 6.0 – 14.0 | 8.0 |
| **Height per Row (in):** | FloatSlider | 0.2 – 1.0 | 0.4 |
| **Title Font Size:** | IntSlider | 8 – 18 | 12 |
| **Axis Label Size:** | IntSlider | 8 – 16 | 11 |
| **Tick Label Size:** | IntSlider | 6 – 14 | 9 |
| **Annotation Size:** | IntSlider | 6 – 12 | 8 |
| **Color Scheme:** | dropdown | *Grayscale (Publication)*, *Color (Presentation)*, *Black & White Only* | Grayscale |
| **Marker Style:** | dropdown | *Circle/Diamond*, *Square/Diamond*, *Circle/Star* | Circle/Diamond |
| **CI Line Style:** | dropdown | *Solid Line*, *Dashed Line*, *Solid with Caps* | Solid Line |

The default *Grayscale (Publication)* colour scheme and *Circle/Diamond* marker style follow the convention adopted by the major ecological journals; the *Color (Presentation)* scheme is intended for conference slides.

**Annotations.** By default, every row displays the *k* and paper count as a parenthesised annotation. For ratio-scale metrics (lnRR, log OR, log RR), the *Show Fold-Change* checkbox additionally prints the back-transformed fold change. The annotation position can be set to *right*, *above*, or *below* the CI line, and offsets are exposed in case multi-line rows would otherwise overlap.

**Two-way designs.** When the subgroup configuration is two-way, additional widgets (*Group H-Offset:*, *Group V-Offset:*, *Group Fontsize:*) control the positioning and typography of the bracket labels that delimit the levels of the first moderator across rows.

**Generation.** Clicking **📊 Generate Forest Plot** produces the figure. When the export checkboxes are enabled, the corresponding files are written to the Colab filesystem using the supplied filename prefix.

### 10.3 Cell 11 — Orchard Plot

The orchard plot of Nakagawa et al. (2021) is a visual complement to the forest plot: rather than collapsing each subgroup to a single row, the orchard plot draws every per-record effect size as a semi-transparent "fruit" — sized by the inverse-variance weight — alongside the pooled estimate, confidence interval, and prediction interval. This makes the within-subgroup distribution of records visible, which is particularly informative when the *Q*_E component of heterogeneity (within-group residual heterogeneity, §9.3) is non-trivial.

Cell 11 exposes eight tabs:

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Plot dimensions, orientation (horizontal / vertical), colour scheme (eight choices), marker style, font family, and the colour reserved for the overall pooled estimate. |
| 2 | **📝 Text** | Title, optional subtitle, *x*- and *y*-axis labels, optional footnote, and the typographic sizes of each element. |
| 3 | **🍎 Orchard** | Fruit (per-record point) size, alpha, edge width and colour, optional weight-scaling; PI ("trunk") line width and alpha; CI line width, style, and colour; jitter to disperse coincident fruit. |
| 4 | **💬 Annot.** | Row-level annotations: *k*, paper count, ES value, CI text, with configurable prefixes, suffixes, decimals, and formats (e.g., `[{lo}, {hi}]` for the CI), plus annotation position and offsets. |
| 5 | **📏 Axes** | Auto-scale toggle (with explicit *Min:* / *Max:* fallback), grid visibility / style / alpha, null-effect line (position, style, line width, colour), separator lines between groups, and group-label placement (position, rotation, optional background box, colour, bold). |
| 6 | **💾 Export** | *Save PDF*, *Save PNG*, *Save SVG* checkboxes, PNG DPI, filename, transparent background, and an optional timestamp suffix on the filename. |
| 7 | **✏️ Labels** | The same label-editor functionality as Cell 10. |
| 8 | **📝 Caption** | The dynamically generated figure caption. |

**Key widgets in the 🎨 Style tab.**

| Widget | Type | Options / range | Default |
|---|---|---|---|
| **Plot Width (in):** | FloatSlider | 6 – 20 | 10 |
| **Plot Height (in):** | FloatSlider | 4 – 30 | auto, ≥ 6 |
| **Font Family:** | dropdown | DejaVu Sans, Arial, Times New Roman, Courier New, Georgia | DejaVu Sans |
| **Color Scheme:** | dropdown | Viridis, Plasma, Coolwarm, Grayscale, Tab10, Set2, Dark2, B & W Only | Viridis |
| **Marker Style:** | dropdown | Circle/Diamond, Square/Diamond, Circle/Star, Circle/Circle | Circle/Diamond |
| **Orientation:** | dropdown | Horizontal, Vertical | Horizontal |
| **Overall Color:** | dropdown | Black, Dark Red, Dark Blue, Dark Green | Black |

**Fruit, CI, and PI controls (🍎 Orchard tab).** The orchard plot is dense by design; the relevant controls allow the user to balance legibility and information content:

| Widget | Type | Range | Default | Effect |
|---|---|---|---|---|
| **Point Alpha:** | FloatSlider | 0.05 – 1.0 | 0.5 | Transparency of individual fruit. |
| **Point Size:** | IntSlider | 10 – 250 | 50 | Base marker size, scaled by weight if *Scale by Weight* is enabled. |
| **Jitter:** | FloatSlider | 0.01 – 0.5 | 0.10 | Random offset applied to each fruit to disperse coincident points. |
| **Scale by Weight** | checkbox | — | enabled | When checked, fruit area scales with the inverse-variance weight. |
| **Show PI (Trunk)** | checkbox | — | enabled | Draws the prediction interval as the outer "trunk" line. |
| **PI Width:** | FloatSlider | 1 – 10 | 4.0 | Line width of the prediction interval. |
| **PI Alpha:** | FloatSlider | 0.05 – 1.0 | 0.3 | Transparency of the prediction interval. |
| **Show CI** | checkbox | — | enabled | Draws the confidence interval as the inner thick line. |
| **CI Width:** | FloatSlider | 0.5 – 6 | 2.0 | Line width of the confidence interval. |
| **CI Style:** | dropdown | Solid, Dashed, Caps | Solid | Style of the confidence-interval line. |
| **Fruit Size (pt):** | IntSlider | 4 – 30 | 12 | Size of the pooled-estimate marker. |
| **Overall Scale:** | FloatSlider | 1.0 – 2.5 | 1.4 | Size multiplier for the *Overall* row's marker. |

**Generation.** Clicking **🌳 Generate Orchard Plot** produces the figure with the current settings. As in Cell 10, the export checkboxes drive file output to the Colab session's filesystem.

### 10.4 The autogenerated figure caption

Both cells render a **📝 Caption** tab containing a publication-ready figure caption that is regenerated automatically every time the plot is rendered. The caption describes the displayed quantities (markers, intervals, annotations), the model used (random-effects vs. fixed-effects, or the orchard-plot conventions of Nakagawa et al. 2021), the metric (e.g., lnRR, Hedges' *g*), the sample-size conventions used in the annotation, and the moderator(s) on which the subgroups are defined. The caption is provided as a starting point and should be edited for substantive narrative consistent with the rest of the manuscript.

### 10.5 Practical guidance

- **Forest and orchard plots are complementary, not redundant.** The forest plot is the appropriate device for reporting *between-subgroup* differences and for embedding the pooled estimates in the main text of a manuscript. The orchard plot is the appropriate device for reporting the *within-subgroup* distribution of records — particularly when the residual heterogeneity is non-trivial — and for justifying the use of a three-level model. Manuscripts that report a subgroup analysis typically benefit from including both.
- **Grayscale is the publication default.** Both cells default to journal-friendly conventions: the forest plot uses *Grayscale (Publication)* and the orchard plot uses *Viridis*. Where the destination journal mandates greyscale figures, the orchard plot's *Grayscale* and *B & W Only* options should be selected before export.
- **Match the metric to the axis label.** The default *x*-axis label is set from the effect-size configuration of Cell 5 (e.g., "log Response Ratio"); when a back-transformed scale is preferred for interpretation, both cells offer a fold-change axis (Cell 10) or can be edited directly in the **📝 Text** tab.
- **Use the Labels editor before exporting.** Group labels in CoMeta default to the raw values found in the dataset (e.g., `GYMNO`, `ANGIO`, `N2FIX`). The **✏️ Labels** tab is the appropriate place to rename them to manuscript-friendly forms (*Gymnosperms*, *Angiosperms*, *N₂-fixing*). The renaming is purely a display change and does not modify the analytical dataset; the analysis can therefore be re-run without re-renaming.
- **Regenerate the caption before submitting.** The caption tab updates only when the plot is regenerated. If the figure has been edited externally (e.g., letter labels added in a vector editor), the caption should be copied immediately after the last in-CoMeta render to ensure consistency with the version of the figure that appears in the manuscript.

### 10.6 Summary

Cells 10 and 11 produce the two principal visualisations of the subgroup analysis: a conventional forest plot of the pooled per-subgroup estimates (Cell 10) and the orchard plot of Nakagawa et al. (2021) showing the per-record distribution within each subgroup (Cell 11). Both cells share a common architecture: a multi-tab customisation interface (*🎨 Style*, *📝 Text*, annotation, axes, *💾 Export*, *✏️ Labels*, *📝 Caption*, plus the orchard-specific *🍎 Orchard* tab in Cell 11), a single **Generate Plot** action button, automatic export to PDF / PNG (and SVG, for Cell 11) when the corresponding checkboxes are enabled, and a dynamically generated figure caption. Both cells read the fitted subgroup result of Cell 9 without modifying it, so users may iterate freely on aesthetic choices without affecting the model. The next analytical step, meta-regression on continuous moderators, is described in Section 11.

---

## Section 11. Linear Meta-Regression

Cells 12 and 13 implement linear meta-regression on a single continuous moderator. Cell 12 fits the regression model and reports the slope, the test of its significance, and a battery of model-quality diagnostics; Cell 13 produces the publication-ready bubble plot of the fitted relationship. Together, they extend the categorical subgroup analysis of Cells 8 – 11 to moderators whose values lie on a continuous scale (e.g., latitude, year of publication, mean exposure duration, body mass) and to ordinal moderators whose levels carry meaningful numerical distance.

The inferential engine is the same three-level REML framework used throughout the pipeline: the regression coefficients are estimated by inverse-Σᵢ-weighted least squares with Σᵢ = τ²_between **J**ᵢ + τ²_within **I**ᵢ + **V**ᵢ, and the standard errors and *p*-values are based on the CR2 cluster-robust estimator (Pustejovsky & Tipton, 2018) with Satterthwaite-approximated degrees of freedom. The Knapp–Hartung adjustment is applied where it was enabled in Cell 7. As elsewhere in CoMeta, when the fitted τ²_within collapses to the lower boundary, the engine reverts transparently to a two-level random-effects regression.

### 11.1 Cell 12 — 📈 12. Meta-Regression: Configuration & Execution

Cell 12 exposes a minimal configuration interface and a single action button. After Cell 7 has been executed, the user clicks **▶ Run** on Cell 12, selects the moderator of interest from the *Moderator:* dropdown, and clicks **▶ Run Meta-Regression**. The cell fits the model and renders five output tabs.

#### 11.1.1 Moderator detection

Cell 12 automatically populates the *Moderator:* dropdown with every column of `ANALYSIS_CONFIG['analysis_data']` that satisfies all of the following:

- the column is **not** one of the core analytical columns (`id`, the chosen effect-size column, its variance, its standard error, the fixed-effect weight `w_fixed`, or the random-effects weight `w_random`);
- the column is either numeric *or* parses to numeric with at least three non-missing values; and
- the column has at least two distinct numeric values.

Categorical moderators (which would be analysed by Cells 8–11) are excluded automatically; an ordinal column coded numerically (e.g., a 1–5 disturbance severity index) is detected and treated as continuous. If the dataset contains no columns satisfying these conditions, the dropdown reads *No numeric moderators found* and the analysis cannot be run; the user should return to Cell 2 and ensure that the relevant continuous variable was retained as a moderator column.

#### 11.1.2 The interface

The configuration panel contains exactly two widgets:

| Widget | Type | Description |
|---|---|---|
| **Moderator:** | Dropdown | The continuous moderator to regress the effect size on. |
| **▶ Run Meta-Regression** | Button | Executes the regression with the current moderator selection. |

The two widgets are deliberately minimal: all other settings (α, distribution type, τ² estimator, Knapp–Hartung adjustment) are inherited from the global configuration saved by Cell 7, ensuring that the regression is consistent with the pooled model.

#### 11.1.3 The model and the columns reported

CoMeta fits the model

$$ y_{ij} \;=\; \beta_0 \;+\; \beta_1 \, x_{ij} \;+\; u_i \;+\; \nu_{ij} \;+\; \varepsilon_{ij}, $$

where *y*ᵢⱼ is the effect size for record *j* in study *i*, *x*ᵢⱼ is the moderator value, *u*ᵢ ∼ 𝒩(0, τ²_between), *ν*ᵢⱼ ∼ 𝒩(0, τ²_within), and *ε*ᵢⱼ is the sampling error with the per-study **V**ᵢ from Cell 6. Inference on the regression coefficients (*β*₀, *β*₁) uses CR2 cluster-robust standard errors and Satterthwaite degrees of freedom. The pseudo-*R* ² is computed as the relative reduction in the residual variance components from the intercept-only model fitted in Cell 7.

#### 11.1.4 Output: five tabs

| Tab | Title | Contents |
|---|---|---|
| 1 | **📊 Results** | The headline slope estimate $\hat{\beta}_1$ together with its confidence interval and *p*-value; an automatic plain-language interpretation paragraph (e.g., *"For every 1-unit increase in latitude, the effect size decreases by 0.0123 units. This relationship is statistically significant."*); a coefficient table reporting *β*₀ and *β*₁ with their standard errors, *p*-values, confidence intervals, and the residual degrees of freedom; and a model summary box reporting the model type, *k*, the number of studies, the residual degrees of freedom, τ², σ², pseudo-*R* ², and the residual *I* ². |
| 2 | **🔍 Diagnostics** | A residual-analysis card reporting the residual range, mean, and standard deviation; influence diagnostics flagging observations with Cook's *D* exceeding the conventional 4 / *n* threshold (the indices of any flagged points are listed); the residual *I* ² and pseudo-*R* ², with a brief interpretation note; and an assumption table summarising the regression assumptions and their applicability to the fitted model. |
| 3 | **⚙️ Model Details** | The model specification, the moderator column name, the effect-size and variance columns used, the estimation method, the convergence status, and the timestamp. |
| 4 | **📝 Publication Text** | Manuscript-ready *Materials and Methods* and *Results* paragraphs describing the regression, the inference machinery (CR2, Satterthwaite, Knapp–Hartung as applicable), the coefficient estimates, the test of the slope, and the heterogeneity decomposition. |
| 5 | **💾 Export** | An export button that writes an Excel workbook containing the coefficient table, the residuals and influence diagnostics, and the model summary. |

When the analysis completes, downstream cells dependent on the regression (Cell 13 — plotting; Cells 14 – 15 — spline meta-regression as an alternative non-linear specification) are marked stale.

### 11.2 Cell 13 — 📈 13. Meta-Regression: Visualization

Cell 13 produces the bubble plot of the fitted regression. Each record is drawn as a point whose horizontal coordinate is the moderator value, whose vertical coordinate is the effect size, and whose area is proportional to the inverse-variance weight (so that small-variance records are visually weighted in proportion to their statistical contribution). The regression line and an optional confidence band are overlaid. Cell 13 follows the same generate-on-click architecture as the subgroup plotting cells (Section 10) and exposes six customisation tabs.

#### 11.2.1 Tabs

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Plot title (with show/hide toggle), *x*- and *y*-axis labels, plot width and height in inches. |
| 2 | **⚫ Points** | *Color By:* — an optional categorical moderator on which the bubble colour is conditioned (defaults to *None*); fall-back single colour (gray / blue / red / green / purple / orange); minimum and maximum bubble sizes; bubble transparency. |
| 3 | **📈 Regression** | Show 95 % confidence band; regression-line colour and width; CI band transparency; show / hide the regression equation and *p*-value annotation; show / hide the pseudo-*R* ² annotation. |
| 4 | **💾 Layout/Export** | Grid visibility; null-effect reference line (*y* = 0); legend location and font size; *Save as PDF* and *Save as PNG* checkboxes; PNG DPI (default 300); filename prefix (default *MetaRegression_Plot*); transparent background. |
| 5 | **✏️ Labels** | A label-editor pane for renaming the levels of the *Color By:* moderator without modifying the source data, exactly as in the subgroup-plotting cells. |
| 6 | **📝 Caption** | The dynamically generated figure caption, refreshed on every plot regeneration. |

#### 11.2.2 Key widgets

| Widget | Type | Range | Default |
|---|---|---|---|
| **Plot Width (in):** | FloatSlider | 5.0 – 14.0 | 8.0 |
| **Plot Height (in):** | FloatSlider | 4.0 – 12.0 | 6.0 |
| **Color By:** | Dropdown | *None* + any auto-detected categorical column | *None* |
| **Min Bubble Size:** | IntSlider | 0 – 200 | 20 |
| **Max Bubble Size:** | IntSlider | 100 – 2000 | 800 |
| **Transparency:** | FloatSlider | 0.1 – 1.0 | 0.6 |
| **Show 95% Confidence Band** | Checkbox | — | enabled |
| **Line Width:** | FloatSlider | 0.5 – 5.0 | 2.0 |
| **CI Transparency:** | FloatSlider | 0.1 – 0.8 | 0.3 |
| **Show Regression Equation & P-value** | Checkbox | — | enabled |
| **Show R² Value** | Checkbox | — | enabled |
| **PNG DPI:** | IntSlider | 150 – 600 | 300 |

Clicking **Generate Plot** renders the bubble plot in the cell's output area. When the export checkboxes are enabled, PDF and PNG files are written to the Colab session's filesystem with the configured filename prefix.

#### 11.2.3 The autogenerated caption

The **📝 Caption** tab in Cell 13 produces a figure-legend draft describing the bubble convention (size proportional to inverse-variance weight), the moderator and effect-size metric, the model used, the meaning of the confidence band, and — when the *Color By:* widget is set — the colouring scheme. The caption is regenerated on every plot render and should be copied immediately after the final render.

### 11.3 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, Cell 12's *Moderator:* dropdown is auto-populated from the saved configuration and the regression is fitted automatically; Cell 13's customisation widgets are likewise restored and the plot is rendered without user intervention. The blue **🔄 Reproducibility Mode Active** notice is displayed at the top of each cell during restoration.

### 11.4 Practical guidance

- **Choose the moderator deliberately.** The regression fitted by Cell 12 is *univariate*: each call to the cell tests a single moderator. When several candidate moderators are of substantive interest, the recommended workflow is to refit the regression once per moderator and to interpret the resulting coefficients in the light of the corresponding pseudo-*R* ² values. Naive multiple testing across moderators is the user's responsibility; CoMeta does not adjust *p*-values for it.
- **Check the Diagnostics tab before interpreting the slope.** A non-trivial residual *I* ² indicates that the moderator does not fully explain the heterogeneity; Cook's *D* values exceeding 4 / *n* identify records that exert undue leverage on the fitted slope. Both quantities should be inspected before the slope is reported.
- **Consider the spline alternative for non-linear relationships.** Cells 14 and 15 fit a restricted-cubic-spline meta-regression of the same moderator on the same effect-size column. When the bubble plot of Cell 13 displays curvature that the linear fit fails to capture — a common finding for dose-response, threshold, and saturation relationships — the spline regression is the appropriate non-linear extension and is described in Section 12.
- **Categorical moderators belong in Cells 8 – 11.** Cell 12 deliberately refuses to operate on a column that is not numeric, because treating a nominal variable as continuous is rarely defensible. When the moderator of interest has a small number of unordered levels, the subgroup analysis described in Sections 8 – 10 is the appropriate device.

### 11.5 Summary

Cell 12 fits a univariate linear meta-regression of the chosen effect-size metric on a single continuous moderator, using the same three-level REML framework, the same CR2 cluster-robust inference, and the same global settings as Cell 7. The user selects the moderator from the *Moderator:* dropdown and clicks **▶ Run Meta-Regression**; the resulting slope, confidence interval, *p*-value, residual diagnostics (Cook's *D*, residual *I* ²), pseudo-*R* ², and autogenerated manuscript text are presented across five tabs. Cell 13 then produces the corresponding bubble plot with inverse-variance-weighted point sizing, an overlaid regression line and optional confidence band, and an autogenerated caption, exported on demand as PDF or PNG. The non-linear extension of the same analysis — restricted-cubic-spline meta-regression — is described in Section 12.

---

## Section 12. Non-Linear Spline Meta-Regression

Cells 14 and 15 implement the non-linear extension of the linear meta-regression of Section 11. Cell 14 fits a restricted-cubic-spline (natural cubic spline) meta-regression of the effect size on a single continuous moderator, performs an omnibus test for non-linearity, and reports the model-quality diagnostics; Cell 15 produces the publication-ready spline-curve plot with its 95 % confidence band. Together, they are the appropriate tools for moderators that may exhibit dose-response, threshold, saturation, or non-monotone relationships with the effect size — relationships that the linear specification of Cell 12 cannot capture.

The spline basis is constructed by `patsy`'s `cr()` function with the user-specified number of degrees of freedom, applied to the standardised moderator. The spline coefficients are estimated by inverse-variance-weighted least squares using a *plug-in* τ² obtained from the overall model fitted in Cell 7; this fixed-τ² strategy ensures stable convergence on the often-flat profile likelihoods that arise when the spline basis introduces multiple correlated columns. The omnibus test of non-linearity is a Wald χ² statistic on the joint significance of the spline terms.

### 12.1 Cell 14 — 📈📈 14. Non-Linear Spline Model Meta-Regression: Configuration & Execution

Cell 14 exposes a minimal configuration interface and a single action button. After Cell 7 has been executed, the user clicks **▶ Run** on Cell 14, selects the moderator and the number of spline degrees of freedom from the two widgets, and clicks **▶ Run Spline Analysis**. The cell fits the model and renders five output tabs.

#### 12.1.1 The interface

| Widget | Type | Range / options | Default | Effect |
|---|---|---|---|---|
| **Moderator:** | Dropdown | Numeric (or numeric-coercible) columns of the analytical dataset | first available | The continuous moderator on which the spline is constructed. The detection rule is the same as in Cell 12 (Section 11.1.1): numeric or parse-to-numeric columns with at least three non-missing values and more than one unique value. |
| **Spline df:** | IntSlider | 3 – 6 | 3 | Degrees of freedom of the restricted cubic-spline basis. *df* = 3 corresponds to four knots (the practical minimum for a non-trivial spline); *df* = 6 corresponds to seven knots and is the upper bound supported in CoMeta. |
| **▶ Run Spline Analysis** | Button | — | — | Fits the spline model with the current moderator and *df* selection. |
| **📥 Download Spline Report** | Button | — | — | Writes an Excel workbook containing the omnibus test, the coefficient table, the knot locations, and the residual diagnostics. |

The Knapp–Hartung adjustment, the τ² estimator, the α level, and the distribution used for inference are inherited from the global configuration saved by Cell 7, so that the spline analysis is consistent with the pooled and linear-regression results.

#### 12.1.2 The model

For each effect-size record, let *x* be the value of the selected moderator. Cell 14 standardises *x* to *z* = (*x* − μ̂) ⁄ σ̂, constructs the *df*-dimensional natural-cubic-spline basis **B**(*z*) = `patsy.cr(z, df=df_spline)`, and fits

$$ y_{ij} \;=\; \beta_0 \;+\; \mathbf{B}(z_{ij})^{\top}\,\boldsymbol{\beta} \;+\; \varepsilon_{ij}, $$

by inverse-variance-weighted least squares with weights *w*ᵢⱼ = (Vᵢⱼ + τ̂²)⁻¹, where τ̂² is the plug-in variance component carried over from Cell 7. The omnibus test of non-linearity is a Wald χ² statistic on the joint significance of the spline terms in **β**, with degrees of freedom equal to the number of basis columns. Standardisation of the moderator is purely a numerical convenience and does not affect the omnibus test or the predicted curve.

The choice of natural-cubic splines (rather than ordinary cubic splines) ensures that the fitted curve is linear beyond the boundary knots, which substantially reduces the well-known instability of polynomial fits at the extremes of the moderator range.

#### 12.1.3 Output: five tabs

| Tab | Title | Contents |
|---|---|---|
| 1 | **📊 Results** | A gradient card displaying the omnibus *p*-value (with the conventional significance asterisks); an information grid reporting the Wald χ² statistic with its degrees of freedom and *p*-value; a plain-language interpretation paragraph that adapts to the test outcome (e.g., *"The relationship between exposure_duration and effect sizes exhibits significant non-linear patterns. A flexible spline model fits the data better than a simple straight line. Examine the Spline Plot tab to identify thresholds or plateaus."*); a model-comparison table relative to the linear specification; and a model-summary box. |
| 2 | **🔍 Diagnostics** | A residual-analysis card reporting the residual mean, standard deviation, and range. A **Boundary Diagnostics** card reports whether the lower and upper 10 % deciles of the moderator range each contain at least three records: when they do, a green ✅ *Boundary Data Sufficient* notice is displayed; when they do not, a yellow ⚠️ ***Sparse Data at Boundaries*** notice warns that the fitted curve may "whip" upwards or downwards at the tails and should be interpreted with caution. |
| 3 | **⚙️ Model Details** | The method label (*Restricted (Natural) Cubic Splines*), the explicit list of knot locations on the standardised moderator scale, a note on the plug-in τ² treatment, and a *Raw Coefficients* table reporting the intercept and each spline-term coefficient with its standard error and *t*-value. The table is followed by an explicit reminder that *individual spline coefficients lack direct biological interpretation; the omnibus test is the correct device for assessing non-linearity*. |
| 4 | **📝 Publication Text** | Manuscript-ready *Materials and Methods* and *Results* paragraphs describing the spline specification, the omnibus test, and (when significant) a pointer to the spline-plot figure. |
| 5 | **💾 Export** | The **📥 Download Spline Report** button described above. |

When the analysis completes, the spline-plot cell (Cell 15) is marked stale and should be re-executed to reflect the new fit.

### 12.2 Cell 15 — 📈📈 15. Non-Linear Spline Model Meta-Regression: Visualization

Cell 15 produces the publication-ready spline-curve plot. Each effect-size record is drawn as a point at its (moderator, effect-size) coordinates; the fitted spline curve is overlaid, optionally with a 95 % confidence band; and the plot is annotated with the omnibus *p*-value where requested. Cell 15 follows the same generate-on-click architecture as Cells 10, 11, and 13.

#### 12.2.1 Tabs

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Plot title (with show / hide toggle), *x*- and *y*-axis labels, plot width and height in inches, PNG DPI for the export. |
| 2 | **⚫ Points** | Show / hide the data points; *Color By:* — an optional categorical moderator on which the point colour is conditioned; fall-back single colour, point size, and point opacity. |
| 3 | **🌊 Curve** | Curve colour and line width; show / hide the 95 % confidence band and its opacity; show / hide the omnibus-*p* statistical annotation. |
| 4 | **💾 Layout** | Grid visibility; null-effect (*y* = 0) reference line; legend location; *Save as PDF* and *Save as PNG* checkboxes; filename prefix (default *Spline_Plot*). |
| 5 | **✏️ Labels** | A label-editor pane for renaming the levels of the *Color By:* moderator without modifying the source dataset. |
| 6 | **📝 Caption** | The dynamically generated figure caption, refreshed on every plot regeneration. |

#### 12.2.2 Key widgets

| Widget | Type | Range | Default |
|---|---|---|---|
| **Width (in):** | FloatSlider | 5.0 – 16.0 | 10.0 |
| **Height (in):** | FloatSlider | 4.0 – 12.0 | 6.0 |
| **Color By:** | Dropdown | *None* + auto-detected categorical columns | *None* |
| **Size:** | IntSlider | 10 – 150 | 40 |
| **Opacity:** | FloatSlider | 0.1 – 1.0 | 0.5 |
| **Line Color:** | Dropdown | blue, red, black, green, purple | blue |
| **Line Width:** | FloatSlider | 0.5 – 6.0 | 2.5 |
| **Show 95% Confidence Band** | Checkbox | — | enabled |
| **CI Opacity:** | FloatSlider | 0.05 – 0.5 | 0.15 |
| **Show Stats (P-value)** | Checkbox | — | enabled |
| **PNG DPI:** | IntText | — | 300 |

Clicking **Generate plot** renders the figure with the current settings; when the *Save as PDF* and *Save as PNG* checkboxes are enabled, the corresponding files are written to the Colab session's filesystem with the configured filename prefix.

#### 12.2.3 The autogenerated caption

The **📝 Caption** tab in Cell 15 produces a figure-legend draft describing the spline specification (number of degrees of freedom, knot count, natural-cubic basis), the moderator, the effect-size metric, the meaning of the confidence band, the use of inverse-variance-weighted estimation, and — where the *Color By:* widget has been set — the colour-coding scheme. The caption is regenerated on every plot render and should be copied immediately after the final render.

### 12.3 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, Cell 14's *Moderator:* and *Spline df:* widgets are auto-populated from the saved configuration and **▶ Run Spline Analysis** is invoked automatically; Cell 15's customisation widgets are likewise restored and the plot is rendered without user intervention.

### 12.4 Practical guidance

- **Choose the degrees of freedom deliberately.** *df* = 3 (the default) is the conservative choice and provides enough flexibility to reveal monotone non-linearities, plateaus, and single thresholds. Higher *df* values increase flexibility at the cost of additional spline coefficients and a wider confidence band; *df* > 4 is rarely justified unless the dataset is large and the underlying relationship is genuinely complex (e.g., a multi-modal dose-response curve).
- **Inspect the boundary diagnostics before reporting the curve shape.** When the **🔍 Diagnostics** tab displays the yellow ⚠️ *Sparse Data at Boundaries* notice, the extreme tails of the fitted curve are essentially driven by the natural-cubic linearity constraint at the boundary knots and by very few records. The curve interior is unaffected, but interpretive claims about the moderator's behaviour at extreme values should be qualified accordingly.
- **Do not interpret individual spline coefficients.** The spline basis columns are correlated by construction and individually lack a substantive interpretation; the *Raw Coefficients* table in **⚙️ Model Details** is provided for completeness and reproducibility, not for interpretation. The substantive findings are the omnibus *p*-value, the shape of the fitted curve in Cell 15, and (where reported) the locations of any plateaus or thresholds visible in the curve.
- **Report the spline analysis as a pre-specified extension of the linear regression.** When both Cells 12 and 14 are run on the same moderator, the spline analysis is most defensibly reported as a pre-specified non-linear sensitivity check on the linear model, rather than as an alternative selected post hoc on the basis of fit. Both fits should be reported, with the linear fit as the primary specification when the omnibus test is non-significant and the spline fit as the primary specification when it is.

### 12.5 Summary

Cell 14 fits a restricted-cubic-spline (natural cubic spline) meta-regression of the effect size on a single continuous moderator, with the user selecting the moderator from the *Moderator:* dropdown and the basis dimension from the *Spline df:* slider (range 3 – 6, default 3). The spline basis is constructed by `patsy.cr()` on the standardised moderator and fitted by inverse-variance-weighted regression with a plug-in τ² from Cell 7. An omnibus Wald χ² test for the joint significance of the spline terms is reported in the **📊 Results** tab; the **🔍 Diagnostics** tab includes a boundary-sparsity check that flags unstable curve tails. Cell 15 produces the spline-curve plot with an optional 95 % confidence band and an autogenerated caption. Both cells share a single underlying fit; iterating on aesthetic choices in Cell 15 does not require Cell 14 to be re-executed.

---

## Section 13. Publication-Bias Diagnostics

Publication bias — the systematic under-reporting of studies whose results do not align with expectations — distorts pooled estimates by an amount that is rarely small in ecology and conservation biology. CoMeta implements three complementary tests of small-study effects and a dedicated funnel plot, distributed across four cells:

| Cell | Title | Purpose |
|---|---|---|
| 16 | **📉 16. Publication Bias: Diagnostics: Egger's & Trim-Fill** | Egger's regression test for asymmetry and the Duval & Tweedie trim-and-fill adjusted estimate, with a combined interpretation. |
| 17 | **📉 17. Publication Bias: Trim-and-Fill Plot** | A dedicated funnel-style plot showing observed and trim-and-fill-imputed studies alongside the original and bias-adjusted pooled estimates. |
| 18 | **📉 18. Publication Bias: PET-PEESE** | The Stanley & Doucouliagos (2014) PET-PEESE bias-corrected pooled estimate. |
| 19 | **📉 19. Publication Bias: Funnel Plot** | A publication-ready funnel plot of the analytical dataset, with optional significance contours and Egger's-test annotation. |

The four tests are deliberately complementary rather than redundant: Egger's regression is the conventional inferential test for small-study effects; trim-and-fill produces a *what-if* estimate that adjusts the pooled effect under the assumption of missingness symmetry; PET-PEESE produces a model-based, bias-corrected estimate that is robust to heterogeneity but rests on different assumptions; and the funnel plot is the appropriate visual summary that should accompany the manuscript. No single diagnostic is decisive; a defensible publication-bias assessment combines the inferential outcomes with the funnel plot.

All four cells are downstream of Cell 7 and operate on `ANALYSIS_CONFIG['analysis_data']`. They do not modify the model fitted by Cell 7.

### 13.1 Cell 16 — Egger's test and trim-and-fill

Cell 16 runs the two most widely cited inferential tests in a single execution. The interface contains a single action button — **▶ Run Publication Bias Analysis** — and renders five output tabs.

#### 13.1.1 Egger's regression test

Egger's test (Egger, Smith, Schneider, & Minder, 1997) regresses the standardised effect size on its standard error, weighted by the inverse variance:

$$ \frac{y_i}{\mathrm{SE}_i} \;=\; \beta_0 \;+\; \beta_1 \cdot \frac{1}{\mathrm{SE}_i} \;+\; \varepsilon_i. $$

A non-zero intercept (*β*₀ ≠ 0) is the operational definition of funnel-plot asymmetry. The **📊 Egger's Test** tab reports the intercept estimate, its standard error, the *t* statistic, the degrees of freedom, and the two-sided *p*-value, with the conventional significance asterisks. A *p* < 0.05 is the conventional threshold for declaring small-study effects detectable; values above this threshold should be interpreted as "no evidence of asymmetry under this test", not as evidence of the absence of bias.

#### 13.1.2 Trim-and-fill

Trim-and-fill (Duval & Tweedie, 2000) is a non-parametric imputation procedure that iteratively trims asymmetrically located studies, re-estimates the pooled effect, and then "fills" the missing side of the funnel with symmetrically imputed studies until symmetry is achieved. The pooled effect re-estimated on the augmented dataset is the bias-adjusted estimate. The **📉 Trim-and-Fill** tab reports the number of studies imputed, the original pooled estimate (from Cell 7) with its confidence interval, the adjusted pooled estimate with its confidence interval, and the absolute change. A non-trivial gap between the two estimates indicates that, *under the symmetry assumption of trim-and-fill*, publication bias may be inflating the pooled effect.

#### 13.1.3 Combined Assessment

The **🔍 Combined Assessment** tab synthesises the two diagnostics into a single qualitative summary, distinguishing the cases (i) Egger's significant and trim-and-fill non-trivial, (ii) one significant and the other not, and (iii) neither significant. The tab is intended as a starting point for the manuscript's *Results* paragraph on publication bias.

#### 13.1.4 Other tabs

- **📝 Publication Text.** Manuscript-ready *Materials and Methods* and *Results* paragraphs describing both diagnostics, including the imputed-study count and adjusted estimate.
- **💾 Export.** A **📥 Download Bias Report** button writes an Excel workbook containing the Egger's-test statistics, the trim-and-fill table, and the underlying per-record data.

### 13.2 Cell 17 — Trim-and-Fill Plot

Cell 17 produces a publication-ready funnel-style figure in which the observed studies and the trim-and-fill-imputed studies are overlaid, with markers distinguishing the two, and with vertical reference lines at the original and adjusted pooled estimates. The visual gap between the two reference lines is the principal device by which the magnitude of the trim-and-fill adjustment is communicated to the reader; a figure of this type is conventional in ecological meta-analyses that disclose a non-trivial trim-and-fill outcome.

Cell 17 follows the generate-on-click architecture used elsewhere in CoMeta. It exposes seven customisation tabs:

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Plot dimensions, typographic sizes (title, axis labels, ticks, legend). |
| 2 | **📝 Text** | Show / hide and edit the plot title, *x*-axis label, and *y*-axis label. |
| 3 | **⚫ Points** | Observed-point colour, shape, edge width; imputed-point colour, shape, edge width and edge style (used to make the imputed studies visually distinguishable); point size and alpha. |
| 4 | **📐 Lines** | Show / hide the original-pooled-effect reference line and the adjusted-pooled-effect reference line, each with configurable colour, width, and style; show / hide the funnel envelope; funnel fill and line width. |
| 5 | **📏 Axes** | *x*-axis auto-scaling (or explicit *X-Min:* / *X-Max:*), invert *y*-axis (the conventional orientation for funnel plots), grid visibility and style, legend location and frame. |
| 6 | **💾 Export** | *Save as PDF* and *Save as PNG* checkboxes, PNG DPI (default 300), transparent-background toggle, filename prefix, optional timestamp suffix. |
| 7 | **📝 Caption** | Dynamically generated figure caption, refreshed on every plot regeneration. |

Clicking the **Generate Plot** button renders the figure with the current settings.

### 13.3 Cell 18 — PET-PEESE

Cell 18 implements the two-stage PET-PEESE procedure of Stanley & Doucouliagos (2014). The procedure fits two related models — the *Precision-Effect Test* (PET), in which the effect size is regressed on its standard error, and the *Precision-Effect Estimate with Standard Error* (PEESE), in which the effect size is regressed on its *squared* standard error — and uses the significance of the PET intercept to decide which model's intercept estimate is reported as the bias-corrected pooled effect:

- if the PET intercept is statistically significant at the chosen threshold, the PEESE intercept is reported as the bias-corrected estimate;
- if the PET intercept is non-significant, the PET intercept itself is reported.

#### 13.3.1 The interface

Cell 18 exposes one widget and one action button:

| Widget | Type | Range | Default | Effect |
|---|---|---|---|---|
| **P-threshold:** | FloatSlider | 0.01 – 0.20 | 0.10 | The *α* level at which the PET intercept is judged to be significant for the purposes of selecting between PET and PEESE. The 0.10 default follows the convention of Stanley & Doucouliagos (2014); higher or lower thresholds shift the PET → PEESE switch towards or away from PEESE. |
| **▶ Run PET-PEESE** | Button | — | — | Executes the procedure. |

#### 13.3.2 Output: four tabs

| Tab | Title | Contents |
|---|---|---|
| 1 | **📊 Summary** | The PET intercept and its *p*-value; the PEESE intercept and its *p*-value; the bias-corrected pooled estimate selected by the procedure; and the threshold at which the selection was made. |
| 2 | **📈 Visuals** | The PET and PEESE fitted lines overlaid on the per-record (SE, effect-size) scatter, together with the original and bias-corrected pooled estimates. |
| 3 | **📝 Interpretation** | A plain-language interpretation of the procedure's outcome, including a note when the selected estimate differs substantially from the Cell 7 pooled estimate. |
| 4 | **📝 Publication Text** | Manuscript-ready *Materials and Methods* and *Results* paragraphs describing the procedure and the bias-corrected estimate. |

### 13.4 Cell 19 — Funnel Plot

Cell 19 produces the canonical funnel plot of the analytical dataset: a scatter of every effect-size record's value against its standard error (or precision, depending on the orientation conventions of the destination journal), with optional significance contours and an Egger's-test annotation overlay. The funnel plot is the most frequently reported visual diagnostic in published ecological meta-analyses and is the appropriate accompaniment to whichever inferential tests are reported from Cells 16 and 18.

Cell 19 follows the generate-on-click pattern. It exposes five tabs:

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Title (text and font), *x*- and *y*-axis labels, plot width and height, PNG DPI. |
| 2 | **⚫ Points** | *Color By:* — an optional categorical moderator on which the point colour is conditioned; fall-back single colour; point size; point opacity. |
| 3 | **▼ Funnel** | *Show Significance Contours (1 %, 5 %, 10 %)* — draws the three contour lines that demarcate the regions of the funnel within which records of given standard error would or would not be individually significant; *Fill Confidence Region* and *Fill Opacity:* — visually fill the conventional 95 % funnel envelope; *Show Egger's Test Stats* — annotates the figure with the intercept estimate and *p*-value computed in Cell 16. |
| 4 | **💾 Export** | *Save as PDF* and *Save as PNG* checkboxes; filename (default *Funnel_Plot*). |
| 5 | **📝 Caption** | The dynamically generated figure caption. |

Clicking **📊 Generate Funnel Plot** renders the figure. When the *Show Egger's Test Stats* checkbox is enabled, the figure draws its annotation from the result of Cell 16; if Cell 16 has not been run, the annotation falls back to "not computed".

### 13.5 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, Cell 16's **▶ Run Publication Bias Analysis** is invoked automatically, Cell 18's *P-threshold:* slider is restored to the saved value and **▶ Run PET-PEESE** is invoked automatically, and Cells 17 and 19 are rendered with their customisation widgets restored. No manual action is required.

### 13.6 Practical guidance

- **Report all four diagnostics or justify the omission.** The three inferential procedures rest on different assumptions and may disagree. Reporting only the test that yields the most favourable outcome is the most common form of selective reporting in published meta-analyses. The accepted convention is to report Egger's regression as the primary test (Cell 16), the trim-and-fill adjusted estimate as a sensitivity check (Cells 16 and 17), and PET-PEESE as an additional bias-corrected estimate when the heterogeneity is non-trivial (Cell 18). The funnel plot of Cell 19 should accompany all three.
- **Funnel asymmetry has many causes besides publication bias.** Genuine sources of small-study effects — including true heterogeneity correlated with sample size (e.g., small studies tend to use different methods), poor methodological quality of small studies, and chance — produce the same visual signature as publication bias. The *Results* paragraph should not declare publication bias on the basis of a significant Egger's test alone; the discussion should explicitly acknowledge the competing explanations.
- **Trim-and-fill rests on a strong symmetry assumption.** The trim-and-fill adjusted estimate is the pooled effect that would obtain *if* the missingness mechanism produces exact left–right symmetry in the funnel. Under heterogeneity, this assumption is rarely met and the adjusted estimate should be reported as a sensitivity bound rather than a corrected estimate.
- **PET-PEESE is a model-based correction with its own assumptions.** The PET-PEESE procedure assumes that the true effect is well approximated by an intercept term in either the SE or SE² metric; in datasets with substantial residual heterogeneity, both PET and PEESE intercepts may be biased. The PET-PEESE estimate is most defensible as one of several complementary bias diagnostics, not as a stand-alone replacement for the pooled estimate of Cell 7.
- **The funnel plot should be in the manuscript.** The funnel plot of Cell 19 is the most informative single artifact for a reader assessing the plausibility of the bias diagnostics; manuscripts that report the inferential tests without the figure are appreciably harder to evaluate.

### 13.7 Summary

Cells 16, 17, 18, and 19 implement CoMeta's publication-bias diagnostic suite. Cell 16 runs Egger's regression test and the Duval & Tweedie trim-and-fill adjustment in a single call, presents both in dedicated tabs together with a combined-assessment summary, and exports the result. Cell 17 produces a dedicated trim-and-fill figure that overlays the observed and imputed studies on a funnel and shows the original and adjusted pooled estimates as reference lines. Cell 18 runs the Stanley & Doucouliagos (2014) PET-PEESE procedure under a user-tunable *P-threshold:* (default 0.10), reports the PET and PEESE intercepts, and selects the bias-corrected estimate accordingly. Cell 19 produces the canonical funnel plot with optional significance contours, an Egger's-test annotation, and a user-controlled categorical *Color By:* dimension. The four cells are complementary: a defensible publication-bias assessment combines the inferential outcomes of Cells 16 and 18 with the visual evidence of Cells 17 and 19. The next analytical step, sensitivity analysis (leave-one-out and Baujat influence diagnostics), is described in Section 14.

---

## Section 14. Sensitivity Analysis: Leave-One-Out and Baujat Diagnostics

Cells 20 – 22 implement CoMeta's per-study influence diagnostics. The leave-one-out analysis (Cells 20 and 21) refits the pooled model with each study removed in turn, exposing the sensitivity of the headline estimate to the inclusion of any single primary study. The Baujat plot (Cell 22) summarises, for every study, the joint pattern of its contribution to total heterogeneity and its influence on the pooled effect, identifying records that are simultaneously outlying and pivotal.

Both diagnostics operate on the same fitted model as Cell 7 and are routinely reported together in ecological meta-analyses. They are downstream of Cells 4, 6, and 7; any change to the imputation strategy, the effect-size calculation, or the analytical settings requires the upstream cells to be re-saved and these diagnostics to be re-executed.

### 14.1 Cell 20 — Leave-One-Out Execution

Cell 20, titled **📉 20. Sensitivity Analysis: Leave-One-Out: Execution**, refits the pooled model *k* times (where *k* is the number of primary studies in the analytical dataset), removing one study on each pass and recording the resulting pooled estimate, confidence interval, *p*-value, and the magnitude of the change relative to the all-studies baseline. The cell uses the same three-level REML engine and the same global settings (α, distribution type, τ² estimator, Knapp–Hartung flag) as Cell 7, so that each leave-one-out fit is directly comparable to the headline estimate.

#### 14.1.1 Interface

Cell 20 exposes a single action button — **▶ Run Sensitivity Analysis** — together with a progress bar that fills as the *k* refits are completed. No other configuration is required; the analysis inherits its inferential setup from Cell 7.

#### 14.1.2 Output: two tabs

| Tab | Title | Contents |
|---|---|---|
| 1 | **📊 Sensitivity Summary** | A baseline panel restating the all-studies pooled estimate from Cell 7; a *Most Influential Studies* table listing the studies that produce the largest change in the pooled estimate when removed, with columns for the excluded study identifier, the recomputed pooled estimate (`mu`), the absolute change (`diff`), and the percentage change (`pct_change`); a plain-language interpretation note that distinguishes the *robust* case (no individual study produces an influential change) from the *non-robust* case (one or more studies produce changes exceeding the conventional 20 % threshold); and a *Next Steps* panel pointing the user to the leave-one-out plot (Cell 21) for the full per-study sequence. |
| 2 | **📝 Publication Text** | Manuscript-ready *Materials and Methods* and *Results* paragraphs describing the leave-one-out procedure, the threshold used to declare influence (20 % by default), the number of studies flagged, and — where applicable — the identifiers of those studies. |

The full per-study table — one row per excluded study, with its recomputed estimate and *p*-value — is stored internally for consumption by Cell 21. Cell 20 itself displays only the *Most Influential* subset to keep the summary tab readable; manuscripts reporting a leave-one-out analysis typically reproduce the full table as supplementary material.

### 14.2 Cell 21 — Leave-One-Out Visualization

Cell 21 produces the publication-ready forest-style figure of the leave-one-out result. Each row of the figure corresponds to one study being omitted; the recomputed pooled estimate and its confidence interval are plotted on the row, together with reference lines for the all-studies pooled estimate and (optionally) its confidence band. Records whose omission flips the statistical significance of the pooled effect can be highlighted in colour, drawing the reader's eye to the pivotal studies.

Cell 21 follows CoMeta's generate-on-click pattern and exposes five customisation tabs:

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Plot title (with show / hide toggle), *x*- and *y*-axis labels, plot width, and either auto-determined height or a manually specified height. |
| 2 | **📊 Data** | *Sort By:* — the row order of the figure, choosing among *Effect Size (Low to High)*, *Influence (Diff from Original)*, and *Study ID*; *Highlight Significance Changers (Red)* — colours the rows whose recomputed pooled estimate has a different significance status from the all-studies baseline; point colour and point size for the recomputed estimates. |
| 3 | **📐 Lines** | Show / hide and style the original-pooled-effect reference line; show / hide the original 95 % confidence band (with adjustable transparency); show / hide the null-effect line. |
| 4 | **💾 Export** | *Save as PDF* / *Save as PNG* checkboxes; PNG DPI (default 300); filename prefix (default *LOO_Plot*). |
| 5 | **📝 Caption** | Dynamically generated figure caption, refreshed on every plot regeneration. |

The action button is **📊 Generate LOO Plot**. Default settings produce a manuscript-ready figure: rows sorted by effect size, significance changers highlighted in red, the all-studies estimate and its 95 % CI band shown as reference lines, and the null line marked at *y* = 0.

### 14.3 Cell 22 — Baujat Influence Plot

Cell 22, titled **📊 22. Sensitivity Analysis: Baujat Plot**, produces the Baujat (2002) diagnostic: a two-dimensional scatter in which each study is plotted at coordinates (*x*ᵢ, *y*ᵢ), where *x*ᵢ is the study's contribution to the total heterogeneity statistic *Q* and *y*ᵢ is the study's influence on the pooled estimate. The plot identifies four qualitatively distinct regions:

- **High Q-contribution, low influence:** studies that diverge from the pooled effect but carry little weight; they drive heterogeneity but not the headline estimate.
- **Low Q-contribution, high influence:** studies that are consistent with the pooled effect but carry sufficient weight to move the estimate; they pin down the pooled value.
- **High Q-contribution, high influence:** studies that are both outlying and pivotal; these warrant the closest scrutiny.
- **Low Q-contribution, low influence:** the majority of records in a well-behaved dataset.

The plot is conventionally annotated with the identifiers of the most extreme studies, sorted by a user-selected method.

#### 14.3.1 Interface

Cell 22 follows the generate-on-click pattern and exposes five tabs:

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Plot width, height, point size, point colour, opacity, and an optional pair of median reference lines that quadrant the plot. |
| 2 | **📝 Labels** | Title, *x*-axis label (default *"Contribution to Heterogeneity (Q)"*), *y*-axis label (default *"Influence on Pooled \<effect label\>"*), and font sizes for the title and the axis labels. |
| 3 | **🏷️ Labels** | *Show Study Labels* — toggles the per-point study-ID labels; *Labeling Method:* — selects which studies receive a label (*Top Outliers (Combined Score)* [default], *Top by Heterogeneity Only*, *Top by Influence Only*, or *All Studies*); *Max Labels:* — limits the number of labelled points (default 5); *Label Position:* — *Auto (Best)*, *Right*, *Left*, *Top*, or *Bottom*; and the label font size. |
| 4 | **💾 Export** | *Save as PDF* / *Save as PNG* checkboxes; PNG DPI (default 300); filename prefix (default *Baujat_Plot*); optional timestamp suffix. |
| 5 | **📝 Caption** | Dynamically generated figure caption, refreshed on every plot regeneration. |

The action button is **📊 Generate Baujat Plot**. With the default *Top Outliers (Combined Score)* labelling method and *Max Labels:* set to 5, the figure annotates the five studies whose joint Q-contribution and influence rank place them furthest from the origin — exactly the records that warrant closer inspection in the manuscript's narrative.

### 14.4 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, **▶ Run Sensitivity Analysis** is invoked automatically in Cell 20, and Cells 21 and 22 are rendered with their customisation widgets restored. No manual action is required.

### 14.5 Practical guidance

- **Choose an influence threshold before running.** The default 20 % threshold for flagging an influential study in the leave-one-out summary is a conservative convention; the appropriate threshold depends on the size of the pooled effect and on the precision with which the manuscript intends to communicate it. Pre-specifying the threshold (and reporting it explicitly in the *Materials and Methods*) is the recommended practice.
- **Sort the leave-one-out plot by influence for reporting.** The default *Sort By: Effect Size (Low to High)* produces a forest-plot-like ordering that is most useful when scanning for outlying recomputed estimates. For the figure that accompanies a manuscript-level claim of robustness, *Sort By: Influence (Diff from Original)* places the most influential studies at the extremes of the plot, which more directly communicates the magnitude of the largest perturbation.
- **Combine leave-one-out with Baujat.** The two diagnostics are designed to be read together. A study flagged as influential by the leave-one-out procedure should appear in the upper-right region of the Baujat plot; a study that the Baujat plot identifies as both outlying and pivotal should be among the largest |diff| entries in the leave-one-out table. When the two diagnostics disagree, the discrepancy itself is informative and should be discussed.
- **Influential studies are not necessarily errors.** A single study that perturbs the pooled estimate may reflect a transcription mistake, but it may equally reflect a genuine but under-replicated experimental finding. The pertinent action is to inspect the study and to report the analysis with and without it; silent removal is inappropriate.
- **Cell 20 is computationally proportional to *k*.** Datasets with several hundred primary studies will take longer to run than the model fit of Cell 7, and the progress bar is intended to provide reassurance during this wait. The leave-one-out result is cached in `ANALYSIS_CONFIG`, so subsequent renders of Cell 21 do not trigger refits.

### 14.6 Summary

Cells 20 – 22 provide the per-study influence diagnostics that accompany the pooled analysis in any rigorous meta-analytical manuscript. Cell 20 executes the leave-one-out procedure under the same inferential settings as Cell 7 and produces a two-tab summary highlighting the studies whose removal materially changes the pooled estimate. Cell 21 renders the corresponding forest-style figure with configurable row ordering, optional significance-flipping highlights, and reference lines for the all-studies estimate and its confidence band. Cell 22 produces the Baujat (2002) influence plot, identifying records that are simultaneously high contributors to total heterogeneity and high influencers on the pooled effect, with a four-option labelling method that controls which studies are annotated. The three cells share their input with Cell 7 and do not modify the underlying model, so customisation choices may be iterated freely. The complementary analyses described in Section 15 — cumulative meta-analysis, geographic distribution, and temporal trends — extend the diagnostic picture beyond per-study influence.

---

## Section 15. Complementary Analyses: Cumulative Meta-Analysis and Geographic Distribution

Cells 23, 24, and 25 implement CoMeta's *complementary* analyses — analyses that supplement the pooled, subgroup, and meta-regression results with additional perspectives on the evidence base. The three cells fall into two functional pairs:

- **Cumulative meta-analysis** (Cells 23 and 25). Cell 23 refits the pooled model after the cumulative addition of each study in chronological order; Cell 25 visualises the resulting trajectory of the pooled estimate (with its confidence band) and of the *I*² statistic across the temporal sequence. The pair is the appropriate device for assessing whether the literature has "stabilised" around the present pooled estimate or whether recent additions are still materially shifting it.
- **Geographic distribution** (Cell 24). Cell 24 renders an interactive Plotly map of the studies, either as latitude/longitude bubbles, as a country-level choropleth, or both side-by-side, depending on which geographic columns were mapped in Cell 2. The map is the appropriate device for reporting the geographic representativeness of the synthesis.

Like the diagnostic cells of Sections 13 and 14, the three complementary cells operate downstream of Cell 7 and do not modify the fitted model. They are independent of each other; the user may run any subset.

### 15.1 Cell 23 — Cumulative Meta-Analysis

Cell 23, titled **📈 23. Complementary: Cumulative Meta-Analysis**, refits the pooled REML model after sequentially adding studies in chronological order (or in reverse-chronological order). The *k*-th refit pools the first *k* studies; the trajectory of the *k* pooled estimates exposes how the synthesis has accumulated evidence over time. The cell uses the same inferential machinery as Cell 7 (REML estimation, CR2 cluster-robust inference, Satterthwaite degrees of freedom, optional Knapp–Hartung adjustment).

#### 15.1.1 Interface

Cell 23 exposes two configuration widgets and a single action button:

| Widget | Type | Options | Default | Effect |
|---|---|---|---|---|
| **Sort Order:** | Dropdown | *Chronological (Oldest → Newest)*, *Reverse Chronological (Newest → Oldest)* | Chronological | The order in which studies are accumulated. Reverse-chronological accumulation, less commonly reported, can highlight the residual contribution of recent studies. |
| **Aggregation:** | Dropdown | *By Study (Recommended)*, *By Observation (Ignore nesting)* | By Study | Whether each step of the cumulative sequence adds an entire primary study (one row per `id`, the recommended approach for three-level datasets) or a single effect-size record (one row at a time, ignoring the within-study nesting). |
| **▶ Run Cumulative Analysis (REML)** | Button | — | — | Executes the cumulative refits. |

The temporal ordering requires a publication-year column. CoMeta searches the analytical dataset for a column named `year`, `Year`, or any common synonym; if no such column is found, the cell reports a configuration error and the analysis cannot be run.

#### 15.1.2 Output: four tabs

| Tab | Title | Contents |
|---|---|---|
| 1 | **📊 Analysis Summary** | A baseline panel restating the all-studies pooled estimate; a discussion of whether the cumulative trajectory has stabilised, with a quantitative comparison between the early and late portions of the sequence; and a *Next Step* pointer to Cell 25 for the corresponding figure. |
| 2 | **📋 Step-by-Step Data** | The full cumulative table: one row per step of the sequence, with the added study's identifier, the recomputed pooled estimate, its confidence interval, the running heterogeneity statistics (*Q*, *I* ², τ²), and the *k* studies included up to that step. This table is the appropriate object to include as a supplementary item in a manuscript reporting a cumulative analysis. |
| 3 | **📝 Publication Text** | Manuscript-ready *Materials and Methods* and *Results* paragraphs describing the cumulative procedure, the sort order, the aggregation choice, and the principal qualitative finding (stabilisation, trend, or oscillation). |
| 4 | **💾 Export** | An export button that writes the step-by-step table to an Excel workbook. |

### 15.2 Cell 25 — Cumulative Trend Plot

Cell 25, titled **📊 25. Complementary: Cumulative Trends**, renders the publication-ready figure that visualises the trajectory produced by Cell 23. The *x*-axis is the cumulative number of studies (or, equivalently, the running publication year); the left *y*-axis is the cumulative pooled effect size with its confidence band; an optional right-hand *y*-axis displays the trajectory of the *I*² statistic. The figure is the standard companion to a cumulative meta-analysis and is widely reproduced in published syntheses.

Cell 25 follows CoMeta's generate-on-click pattern and exposes five tabs:

| Tab | Title | Contents |
|---|---|---|
| 1 | **🎨 Style** | Plot width and height, title and label font sizes, grid visibility. |
| 2 | **📝 Text** | Show / hide the plot title; edit the title, *x*-axis label, and *y*-axis label. |
| 3 | **📈 Effect** | Line colour and width for the cumulative-effect trajectory; marker style (*Circle*, *Square*, *Diamond*, or *None*); show / hide the 95 % confidence band and its opacity; show / hide the null-effect (*y* = 0) reference line. |
| 4 | **📉 I²** | Show / hide the *I*² trajectory on the right-hand axis; line colour, style (*Dashed*, *Dotted*, *Solid*), and opacity. The default is to show the *I*² trajectory in dashed orange. |
| 5 | **💾 Export** | *Save as PDF* / *Save as PNG* checkboxes, PNG DPI (default 300), filename (default *Cumulative_Trend_Plot*). |

The action button is **📊 Generate Cumulative Plot**. The default settings produce a figure showing the cumulative effect with a 95 % confidence band, the *I*² trajectory in dashed orange on the right axis, and the null-effect reference line at *y* = 0 — the four elements most frequently reproduced in published cumulative figures.

### 15.3 Cell 24 — Geographic Distribution of Studies

Cell 24, titled **🗺️ 24. Complementary: Geographic Distribution of Studies**, renders an interactive Plotly map of the analytical dataset. The cell adapts to the geographic columns mapped in Cell 2 (Section 2.3): when latitude and longitude are present, a bubble map is offered; when a country column is present, a country-level choropleth is offered; when both are present, the user may render the two side-by-side. The figure is the appropriate device for the *Geographic representativeness* paragraph of a manuscript's *Methods* section.

Cell 24 follows the generate-on-click pattern and exposes five tabs:

#### 15.3.1 Tab 1 — 🗺️ Map Type

The **Map Type:** radio group exposes only the options that are compatible with the geographic columns available:

| Option | Available when |
|---|---|
| **Bubble Map (Coordinates)** | Latitude and longitude were mapped in Cell 2. |
| **Choropleth Map (Country)** | A country/region column was mapped in Cell 2. |
| **Both (Side by Side)** | Both coordinate and country columns were mapped. |

The user additionally selects the cartographic **Projection:** from eight standard options: *Robinson (recommended)*, *Natural Earth*, *Equirectangular*, *Mollweide*, *Winkel Tripel*, *Eckert IV*, *Mercator*, and *Orthographic (Globe)*. The **Base Map:** dropdown controls the visual style — *Light Gray Land* (default), *White Land*, *Blue Ocean*, or *Minimal (Outlines Only)* — and three checkboxes (*Show Coastlines*, *Show Country Borders*, *Show Map Frame*) toggle the corresponding cartographic elements.

#### 15.3.2 Tab 2 — 🎨 Style

The Style tab controls the dimensions of the rendered map (default 900 × 500 px, configurable up to 1600 × 1000 px) and the visual encoding of the data:

| Widget | Type | Options / range | Default |
|---|---|---|---|
| **Color Scale:** | Dropdown | RdBu (diverging, recommended), Viridis, Plasma, Cividis, RdYlGn, Spectral, Blues (sequential), YlOrRd (sequential), Grays (B & W) | RdBu_r |
| **Center Color at Zero (diverging)** | Checkbox | — | enabled |
| **Bubble Opacity:** | FloatSlider | 0.1 – 1.0 | 0.80 |
| **Max Bubble Size:** | IntSlider | 5 – 50 | 22 |
| **Bubble Edge Width:** | FloatSlider | 0 – 2 | 0.5 |
| **Edge Color:** | Dropdown | Black, Dark Gray, White, None | Black |
| **Jitter (°):** | FloatSlider | 0.0 – 2.0 | 0.0 |

The *RdBu_r* diverging colour scale centred at zero is the default because, for log-scale and standardised effect-size metrics, the meaningful axis runs from negative (study favours control) through zero (null) to positive (study favours treatment). The jitter widget displaces overlapping coordinate bubbles in degrees of latitude/longitude, which is useful when many studies cluster at the same nominal location (e.g., a single field station).

#### 15.3.3 Tab 3 — 📝 Text

The Text tab controls the figure's textual elements: title, optional subtitle (with an *Auto-generate subtitle* toggle that emits a description such as *"n = 87 studies across 14 countries"*), the colour-bar label and length, an optional study-count annotation with configurable position, and the font family and base font size.

#### 15.3.4 Tab 4 — 📊 Data

The Data tab controls how the analytical data are mapped to the visual encoding:

| Widget | Effect |
|---|---|
| **Color By:** | The column whose value determines the bubble or country colour. The default is the chosen effect-size column. |
| **Size By:** | The column whose value determines the bubble size. The default is the inverse-variance weight, which sizes bubbles by their statistical contribution. |
| **Size Transform:** | A transformation applied to *Size By* before mapping to bubble area (linear, log, square root). |
| **Choropleth aggregation:** | When a choropleth is selected, the statistic aggregated per country (mean, median, weighted mean, count). |

#### 15.3.5 Tab 5 — 💾 Export

PDF, PNG, and HTML export of the Plotly figure with a configurable filename (default *Geographic_Map*). The HTML export preserves the interactivity (zoom, pan, tooltips on each bubble) and is useful for supplementary online material; the PDF and PNG exports are the appropriate artefacts for the printed manuscript.

The action button is **Generate Map**; rendering takes a few seconds because the map is a fully interactive Plotly figure rather than a static matplotlib image.

### 15.4 Behaviour under session restoration

When the session has been restored from an `analysis_settings.json` file, Cell 23's *Sort Order:* and *Aggregation:* widgets are auto-populated and **▶ Run Cumulative Analysis (REML)** is invoked automatically; Cells 24 and 25 are rendered with their customisation widgets restored. As elsewhere in CoMeta, no manual action is required.

### 15.5 Practical guidance

- **The cumulative analysis is not a temporal trend in the moderator sense.** A non-flat trajectory of the cumulative pooled estimate need not imply that the *true* effect has changed over time; it can equally reflect changes in the methodology, the precision, or the topical focus of the literature. A formal test of a time-trend in the effect size is the linear meta-regression of Cells 12 – 13 with the publication-year column as the moderator; the cumulative figure of Cell 25 is the appropriate visual companion but is not itself a hypothesis test.
- **Choose "By Study" aggregation when in doubt.** For three-level datasets, accumulating an entire primary study per step is the convention; accumulating one effect-size record at a time tends to produce visually noisier trajectories that are harder to interpret in narrative form.
- **Map type follows the data mapping in Cell 2.** When neither coordinates nor a country column were mapped in Cell 2, Cell 24 cannot render any map and reports a configuration error. The pertinent action is to return to Cell 2, re-finalise with the geographic columns enabled in the *Geographic Columns* section (Section 2.3), and re-execute the downstream cells.
- **Diverging colour scales align with effect-size convention.** The default *RdBu_r* scale centred at zero is appropriate for the four effect-size metrics centred at zero (Hedges' *g*, Cohen's *d*, lnRR, log OR, log RR). For sequential outcomes (counts, percentages) a sequential scale (Viridis, Blues) is more appropriate; the user should set this consciously rather than relying on the diverging default.
- **Export the HTML map.** For online supplementary material, the interactive HTML export of Cell 24 is substantially more informative than the static PDF/PNG renderings, because the reader can inspect each study's identifier, coordinates, and effect-size value via the Plotly tooltips. The static formats remain appropriate for the printed manuscript figure.

### 15.6 Summary

Cells 23, 24, and 25 provide CoMeta's complementary analyses. Cell 23 refits the pooled model cumulatively in chronological (or reverse-chronological) order, using either *By Study* or *By Observation* aggregation, and reports the step-by-step trajectory in four output tabs; Cell 25 then renders the corresponding cumulative trend figure with configurable effect-size and *I*² overlays. Cell 24 renders an interactive Plotly map — bubble, choropleth, or both — of the geographic distribution of the studies, with five customisation tabs covering map type, style, text, data encoding, and export. The three cells operate independently of each other and downstream of Cell 7, and may be run in any combination.

This concludes the cell-by-cell tour of the CoMeta analytical pipeline. The *Materials and Methods* text generated by Cell 7 and the *analysis_settings.json* file produced by Cell 7's export tab together provide a complete record of the analysis, which — when deposited as supplementary material alongside a manuscript — enables one-click reproduction of every figure, table, and numerical claim in the present user guide.
