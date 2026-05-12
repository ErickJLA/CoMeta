# CoMeta — User Guide and Data Formats

*A practical companion for ecologists and conservation researchers running rigorous three-level meta-analyses through the CoMeta widget interface. No programming experience is required at any point.*

---

## Section 1. Getting Started

Welcome to CoMeta. If you have ever run a meta-analysis on paper, in a spreadsheet, or with a statistical package and felt that the *statistics* were tractable but the *software* was the barrier, this guide is for you. CoMeta runs entirely in your web browser through Google Colaboratory. You will never need to install anything, type a single line of code, or manage package versions. Everything you do happens through point-and-click widgets — dropdowns, buttons, checkboxes, and sliders.

This first section walks you through the two things you need to do before any analysis begins: **opening the notebook in Google Colab** and **initialising the environment** so that the widget interface comes to life.

### 1.1 What you need before you start

- A free **Google account** (the same kind you would use for Gmail or Google Drive). This is required by Google Colab; CoMeta itself does not collect or store anything.
- A modern web browser (Chrome, Firefox, Safari, or Edge — any recent version is fine).
- An internet connection. Once the notebook is loaded, all computation happens on Google's servers, so the speed of your own computer is irrelevant.

You do **not** need Python, R, conda, Anaconda, Jupyter, a terminal, administrator rights on your machine, or any prior exposure to programming. If you have ever opened a Google Doc, you already know enough to use Colab.

### 1.2 Launching the notebook in Google Colab

There are two equally easy ways to open CoMeta:

**Option A — Click the "Open in Colab" badge.**
On the project's GitHub page (or in the project README), you will see a coloured badge that reads **Open In Colab**. Click it. A new browser tab opens, and a few seconds later you are looking at the CoMeta notebook.

**Option B — Paste the direct link into your browser.**

```
https://colab.research.google.com/github/ErickJLA/CoMeta/blob/main/CoMeta_1.ipynb
```

Either route brings you to the same notebook, titled **CoMeta_1.ipynb**, displayed inside the Google Colab editor.

> **Tip — save your own copy.** The notebook you open from the badge is a *read-only view* of the official version. If you want to keep your widget selections, your uploaded data, and your results between sessions, immediately go to the Colab menu bar and choose **File → Save a copy in Drive**. Colab will create a private, editable copy in your own Google Drive (in a folder called *Colab Notebooks*) and switch you over to it automatically. From that point on, every change you make is saved to your Drive, exactly the way Google Docs saves itself as you type. If you prefer not to use Drive, you can instead use **File → Download → Download .ipynb** at any time to keep a local copy on your computer.

When the notebook first loads you will see a long, vertically-scrolling page made up of *cells*. Each cell is one self-contained step of the analysis pipeline — there are 38 of them in total — and each one is clearly numbered and labelled with a gear icon ⚙️ and a descriptive title, for example:

- **⚙️ 1. Environment Setup & Core Functions**
- **⚙️ 2. Data Ingestion**
- **⚙️ 3. Global Filtering**
- … and so on, in order, all the way through publication-bias diagnostics and sensitivity analyses.

You will work through these cells *from top to bottom*, one at a time. You never need to read the code inside them; you simply need to *run* each one and then interact with the widget interface it reveals.

### 1.3 Running Cell 1 — the one-time initialisation step

The very first cell, **⚙️ 1. Environment Setup & Core Functions**, is the only cell that does not display a widget interface. Its job is to prepare the Colab session: it checks that the correct versions of the underlying scientific libraries (NumPy, pandas, SciPy, matplotlib, ipywidgets, and a handful of others) are installed, and it loads CoMeta's internal statistical engine into memory. You only need to run it **once per session**.

To run Cell 1:

1. Hover your mouse over the left-hand edge of the cell. A small **▶ (Play / Run)** button appears in a circular frame.
2. Click it.
3. *(Equivalent keyboard shortcut: select the cell and press* **Shift + Enter** *.)*

The first time you run Cell 1 in a new Colab session, expect it to take **roughly 30–90 seconds**. Colab is downloading and pinning a small set of packages to known-good versions so that every CoMeta user, on every machine, gets identical numerical results. While this is happening, the play button shows a spinning circle and a small running-time counter ticks up beside the cell.

When Cell 1 finishes, the output area underneath it clears itself and displays a tidy confirmation banner with a small green dot:

> 🟢 **Environment Verified** — *Core engine initialised*

That banner is your green light. The statistical engine is loaded, the widget framework is active, and you are ready to move on.

> **If something looks wrong.** On rare occasions, Colab assigns you a runtime that is missing a dependency or has hit a transient network hiccup. The symptom is usually a red error message instead of the green banner. The fix is almost always the same: in the Colab menu bar, choose **Runtime → Restart session** (or **Runtime → Restart runtime**), and then re-run Cell 1. You do not need to re-open the notebook or do anything else.

### 1.4 Running the rest of the cells

From Cell 2 onward, every cell follows the same simple pattern, and once you have seen one you have seen them all:

1. **Click the ▶ Run button on the cell** (or press **Shift + Enter**).
2. **The widget interface appears** directly beneath the cell — dropdowns, file-upload boxes, radio buttons, sliders, checkboxes, and clearly labelled action buttons such as *Confirm*, *Apply Filters*, *Calculate Effect Sizes*, *Fit Model*, and so on.
3. **Make your selections.** Nothing happens until *you* click an action button — you can change your mind freely, toggle options on and off, and re-select dropdowns without any risk of corrupting the analysis.
4. **Move on to the next cell** when you are satisfied with the results displayed by the current one.

Crucially, **the code inside each cell never has to be edited**. You never type Python. You never edit a configuration file. The play button is the only piece of "code" you ever press.

> **Cells run in order.** CoMeta is a linear pipeline: Cell 3 expects the data that Cell 2 produced, Cell 7 expects the effect sizes that Cell 6 produced, and so on. Always run the cells top-to-bottom on your first pass. If you later go back and change something upstream — say, you re-import your dataset in Cell 2 or change an imputation strategy in Cell 4 — CoMeta will automatically display an orange *staleness banner* on every downstream cell that now needs to be re-run. You simply press ▶ on each flagged cell again, in order, and the banners clear themselves as the analyses refresh.

> **Sessions are temporary.** Google Colab disconnects idle sessions after a period of inactivity (typically a couple of hours). If that happens, your widget interface will go grey and unresponsive. Don't worry — your *notebook* is safe in Google Drive; only the *running session* has ended. Reconnect by clicking the **Connect** button in the top-right of Colab, then re-run Cell 1, and then continue from where you left off. (We will see in a later section how CoMeta's **session export to JSON** feature lets you save your entire analytical configuration and reload it with a single click, so that long analyses never have to be reconstructed from memory.)

### 1.5 You are ready

That is genuinely all there is to launching CoMeta. Open the notebook, click ▶ on Cell 1, wait for the green *Environment Verified* banner, and you are looking at a fully-prepared, no-code meta-analysis environment running on Google's servers. Everything from here on — uploading your data, choosing an effect size, fitting a three-level random-effects model, running publication-bias diagnostics, generating a manuscript-ready Methods paragraph — happens entirely through the widgets you are about to meet.

In the next section, we will pick up where we left off and walk through **Cell 2: Data Ingestion**, where you bring your own dataset into CoMeta (or load one of the built-in example datasets to follow along).
