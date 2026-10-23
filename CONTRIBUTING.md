# Contributing to CoMeta

CoMeta is never finished. It is a meta-analysis tool, and it is also an open
workbench: all the statistics are written out in the notebook so you can
read them, question them, change them and try new ideas on your own data.
Most people will only use it, and that is fine. This guide is for those who
want to go further: report a problem, fix a bug, add a method, or keep their
own version (a fork).

You do not need to be a professional programmer. A clear bug report with
your data and settings is as valuable as a pull request.

---

## Contents

1. [Ways to contribute](#1-ways-to-contribute)
2. [Fork, change and propose (the workflow)](#2-fork-change-and-propose-the-workflow)
3. [How the notebook is organised](#3-how-the-notebook-is-organised)
4. [Conventions](#4-conventions)
5. [Checking your change](#5-checking-your-change)
6. [Adding a new method or a new validation](#6-adding-a-new-method-or-a-new-validation)
7. [Pull request checklist](#7-pull-request-checklist)
8. [Keeping your own fork](#8-keeping-your-own-fork)
9. [Conduct and credit](#9-conduct-and-credit)

---

## 1. Ways to contribute

| You want to… | What to do |
|---|---|
| Report a bug or a wrong number | Open an [issue](https://github.com/ErickJLA/CoMeta/issues) (see below what to include). |
| Report a difference between CoMeta and R | Open an issue with the validation results file (`cometa_validation_results.json`). |
| Suggest a method, an option or a plot | Open an issue first, with a reference for the method, so we can agree on the approach before you write code. |
| Fix a bug or improve the text | Fork, change, open a pull request (section 2). |
| Improve the documentation | Edit `README.md` or this file and open a pull request. |
| Share a test dataset | A published dataset with known results (e.g. from a paper or an R package) is very useful for the validation suite. |

**A good bug report contains:**
- what you did (the step and the options you chose) and what you expected;
- the message or the number that looks wrong (a screenshot helps);
- the session file from **Step 27 (Export Session)**: it holds your settings
  and data, so the problem can be reproduced exactly. If the data cannot be
  shared, say so; a small made-up dataset that shows the same problem is
  enough;
- the **Warnings log** from Step 27, if the problem came with warnings.

---

## 2. Fork, change and propose (the workflow)

A *fork* is your own copy of the repository on GitHub. You can change it
freely; nothing reaches the main CoMeta until you propose it and it is
reviewed.

### 2.1 Make your fork

1. Sign in to GitHub and open <https://github.com/ErickJLA/CoMeta>.
2. Click **Fork** (top right). You now have `https://github.com/<your-name>/CoMeta`.
3. In your fork, create a branch for the change (branch menu → type a name
   such as `fix-pi-label` → **Create branch**). One branch per change keeps
   proposals small and easy to review.

### 2.2 Work in Google Colab (no installation)

1. Open your branch's notebook in Colab by changing the address:
   `https://colab.research.google.com/github/<your-name>/CoMeta/blob/<branch>/CoMeta.ipynb`
2. Edit the cells. Expand a form cell (double-click it, or *Show code*) to
   see its code.
3. Re-run the steps you changed on your data, then run the validations
   (section 5).
4. Before saving: **Edit → Clear all outputs** (section 4, *Outputs*).
5. **File → Save a copy in GitHub**: choose your fork, your branch, write a
   short message describing the change and tick nothing else. This makes a
   commit on your branch.

### 2.3 Or work on your computer

```bash
git clone https://github.com/<your-name>/CoMeta.git
cd CoMeta
git checkout -b fix-pi-label
jupyter lab CoMeta.ipynb        # or VS Code, or upload to Colab
```

The notebook installs what it needs in its first cell (it is written for
Colab, so a few Colab-only features, such as Google Sheets import, will not
work locally). The validation suite also needs R and the Python package
`rpy2`; its setup cell installs the R packages.

Commit and push as usual:

```bash
git add CoMeta.ipynb
git commit -m "Prediction interval label: say t or z"
git push -u origin fix-pi-label
```

### 2.4 Propose the change (pull request)

On your fork's GitHub page click **Compare & pull request**. Describe:
- **what** changed and **why** (link the issue if there is one);
- **what you checked**: which validations you ran, on which data, and the
  result (attach `cometa_validation_results.json`);
- for a statistical change, the **reference** it follows.

The change is reviewed, and you may be asked for adjustments; push them to
the same branch and the pull request updates itself.

### 2.5 Stay up to date

When the main CoMeta changes, bring the changes into your fork with
**Sync fork** on your fork's GitHub page, or locally:

```bash
git remote add upstream https://github.com/ErickJLA/CoMeta.git   # once
git fetch upstream
git merge upstream/main
```

---

## 3. How the notebook is organised

Everything lives in `CoMeta.ipynb`. That is on purpose (a *glass box*):
there is no hidden package, so what you read is what runs. The cells run top
to bottom and share their state through one dictionary,
**`ANALYSIS_CONFIG`**: each step reads the keys it needs and writes its
settings and results back.

| Cells | What they hold |
|---|---|
| **1. Environment Setup & Core Functions** | Imports, the τ² estimators, CR2 / Satterthwaite inference, the HTZ Wald test, the warning router and log, `mark_stale` (the "re-run this step" banner) and shared helpers. |
| **1b. Unified Model Engine** | `FitSpec`, `fit_mv`, `compare_fits`: the REML/ML multilevel model used by the overall model, subgroups and meta-regression. |
| **2–6. Data** | Ingestion and column mapping, global filters, cleaning and shared-control detection, effect-size choice and calculation, sampling variance–covariance matrices. |
| **7. Overall model** | Three-level model, heterogeneity, prediction interval, Methods/Results text. |
| **8–16. Moderators** | Subgroups, proportion of meaningful effects, meta-regression, splines, meta-forest, with their plots. |
| **17–20. Publication bias** | Egger, trim-and-fill, PET-PEESE, time-lag test, funnel plot. |
| **21–26. Sensitivity and complementary analyses** | Leave-one-out, Baujat, cumulative meta-analysis, maps, trends. |
| **27. Export Session** | Session file, warnings log. |
| **🧪 Validation cells** | R setup, Validations 1–26 (Python vs R), Validation 11 (unit tests), summary and export. |

Typical keys in `ANALYSIS_CONFIG`: `analysis_data` (the effect sizes used by
all models), `vcv_matrices` (study id → sampling VCV block), `es_config`
(column names and labels of the chosen effect size), `global_settings` (the
Step 7 choices: estimator, CR2, t or z, α) and one `*_results` entry per
analysis (e.g. `overall_results`, `subgroup_results`).

To find where something is computed, search the notebook (Colab: **Edit →
Find and replace**) for the label you see in the output.

---

## 4. Conventions

These keep CoMeta readable and its results trustworthy.

**Statistics**
- Every method follows a published source; cite it in a comment next to the
  code and in the generated Methods text.
- A result that can be compared with R must be validated against R
  (section 5). If CoMeta deliberately differs from R, say so in the code and
  in the generated text.
- Keep the defaults conservative: a new option starts *off* unless it is the
  recommended practice.
- When the method changes, update the generated Methods/Results text and its
  references in the same change. The text must describe what was computed.

**Code**
- Stay inside the notebook. Do not move code into an external package; a
  new helper goes into the cell where it is used, or into Cell 1 / 1b when
  several steps need it.
- Prefer the libraries already loaded (numpy, scipy, pandas, statsmodels,
  matplotlib, ipywidgets). A new dependency needs a good reason.
- Match the surrounding style: comment density, names, and the way each
  step builds its widgets and HTML output.
- Read settings from and write results to `ANALYSIS_CONFIG`; do not rely on
  global variables from other cells. A step that changes its results should
  call `mark_stale(...)` so later steps show the "re-run" banner.
- Messages for the user: `warnings.warn(...)` for something they should
  know (it is shown once, compactly, and kept in the Step 27 warnings log),
  or a clear HTML message in the cell output. Do not print numerical noise:
  wrap optimiser code with `@_quiet_numerics` (Cell 1b) and report
  convergence yourself.
- User-facing text in plain English, without naming other software unless
  the comparison helps the reader.

**Outputs**
- Commit the notebook **without outputs** (Colab: **Edit → Clear all
  outputs** before saving). Outputs make the file very large and the
  changes impossible to review.
- A deliberate executed record (e.g. a full validation run for a release)
  is the exception; say so in the pull request.

---

## 5. Checking your change

The validation suite (the 🧪 cells after Step 27) is the verification
system for developers. It runs **on your own analysis**: the data, the
sampling VCV (including shared controls), the settings and the results of
the steps you ran in this session. See *Validation suite* in the
[README](README.md#8-validation-suite-for-developers).

1. Run your analysis (Steps 2–27, or the steps you changed).
2. Run **Validation: Imports & R Setup**. For a statistical change, tick
   *Also run the fixed reference datasets*: they reach code paths your data
   may not (singletons, unbalanced clusters, missing years, shared controls).
   The R packages are installed from a dated snapshot so everyone compares
   against the same versions.
3. Run the validations that cover your change, plus **Validation 11 (unit
   tests)**, which runs on every change.
4. Run **Validation Summary & Export** and keep
   `cometa_validation_results.json` for the pull request.

Each validation reports *PASS*, *FAIL*, *not run* (the step it checks was not
run) or *skipped* (it uses only reference datasets and they are off). A
change is ready when nothing that passed before fails now. If a tolerance
has to be loosened, explain why in the pull request.

**Unit tests.** Validation 11 collects every `test_...` function in its cell
with pytest. Add a test for each bug you fix (one that fails before your fix
and passes after) and for each new function. Tests should be small, fast and
use made-up data or published values (e.g. a number taken from R, with the
R call in the docstring).

---

## 6. Adding a new method or a new validation

**A new analysis step**
1. Open an issue describing the method and its reference.
2. Add a cell where it belongs in the workflow, with a `#@title` header in
   the style of the others and the setup check used at the top of every cell.
3. Read the data from `ANALYSIS_CONFIG['analysis_data']` and
   `ANALYSIS_CONFIG['vcv_matrices']`, and the inference settings from
   `global_settings`, so the step agrees with the overall model.
4. Store its results under a new key (e.g. `ANALYSIS_CONFIG['mymethod_results']`)
   and, if they are results rather than settings, add the key to
   `RESULT_KEYS` in `export_config_for_reproducibility` (Cell 1) so the
   session file stays small.
5. Generate Methods/Results text with references, as the other steps do.
6. Add unit tests and, when R can compute the same thing, a validation.
7. Document the step in the README manual.

**A new validation**
1. Copy the closest existing validation cell (e.g. Validation 26) and keep
   its structure: header comment saying what is compared with which R
   function, tolerances in a dictionary at the top.
2. Get the data with `validation_sources(reference=...)`: your analysis
   first, plus fixed reference datasets when the switch is on.
   `validation_user_data()` gives the effect sizes, the VCV and the Step 7
   settings; `validation_block_V()` builds the block-diagonal V for R.
3. If a required step was not run, raise `ValidationPrerequisiteError`
   (recorded as *not run*). A validation that uses only fixed datasets
   starts with `if reference_only_validation(n, title):`.
4. Record the outcome with `record_validation(n, title, checks, notes=...)`,
   where `checks` is a list of `(check, 'PASS'/'FAIL'/'INFO')`.
5. Increase `N_VALIDATIONS` in **Validation Summary & Export** and list the
   new validation in the README.

---

## 7. Pull request checklist

- [ ] One topic per pull request; linked issue if there is one.
- [ ] The notebook runs top to bottom in a fresh Colab session.
- [ ] Validation 11 (unit tests) passes; new tests added for the change.
- [ ] Relevant validations pass on your data (and on the reference datasets
      for statistical changes); `cometa_validation_results.json` attached.
- [ ] Generated Methods/Results text and references match what is computed.
- [ ] README updated if the user sees something new or different.
- [ ] Outputs cleared before saving the notebook.

---

## 8. Keeping your own fork

You are welcome to keep a fork for your own research, teaching or method
development: that is part of the idea of CoMeta. If you do:
- keep the reference to the original CoMeta and its citation, and say what
  you changed, so readers of your work know which version produced the
  results;
- run the validation suite after your changes; a modified version that has
  not been checked against R should say so in any publication;
- consider proposing your improvements back (section 2.4): a method that
  helps you probably helps others.

Check the repository's licence file for the terms under which CoMeta may be
reused and redistributed.

---

## 9. Conduct and credit

Be kind and constructive: many users are researchers learning meta-analysis
or programming as they go, and questions are welcome. Critique the code and
the statistics, not the person.

Contributors are credited in the repository history and in the release
notes. If a contribution adds a method of your own, cite your paper in the
generated text and the README, as is done for the other methods.

Questions about contributing: open an
[issue](https://github.com/ErickJLA/CoMeta/issues).
