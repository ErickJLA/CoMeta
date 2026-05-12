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
