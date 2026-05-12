# CoMeta — Truly Quick Start

*A 3-minute, click-through checklist. Open the notebook, hit ▶ on each cell, accept the defaults, and collect your manuscript-ready text from the **📝 Publication Text** tab as you go.*

> For the full guide with theory and rationale, see [`quick_start.md`](quick_start.md) or [`user_guide_and_data_formats.md`](user_guide_and_data_formats.md).

---

## 0. Open & Setup

- Open `CoMeta_1.ipynb` in Google Colab → **File → Save a copy in Drive**.

---

## 1. Data & Prep (Cells 1–6)

- **Run Cell 1** (⚙️ 1. Environment Setup & Core Functions) → wait for the green **🟢 Environment Verified** banner.
- **Run Cell 2** (⚙️ 2. Data Ingestion) → in the **Google Sheets** tab:
  - Click **1. Connect Google Account** → approve the popup.
  - Type your sheet name → click **2. Find Worksheets** → pick worksheet → click **3. Load Data**.
  - Select **Data Type** (*Continuous* / *Binary* / *Pre-calculated*) → click **✓ Confirm Mapping & Finalize Data**.
- **Run Cell 3** (⚙️ 3. Global Filtering) → leave *Filter Variable* on **None** → click **▶ Save Configuration**.
- **Run Cell 4** (⚙️ 4. Data Cleaning & Pre-processing) → accept the default imputation dropdowns → click **▶ Process Data**.
- **Run Cell 5** (🔬 5. Effect Size Selection & Diagnostics) → accept the recommended metric on the **💡 Recommendation** tab → click **✓ Confirm Selection**.
- **Run Cell 6** (🧮 6. Effect Size Calculation) → no widgets, just runs.

---

## 2. The Headline Result (Cell 7)

- **Run Cell 7** (📊 7. Overall Meta-Analysis) → pooled estimate appears on the **📊 Primary Result** tab.
- 🎁 **Open the 📝 Publication Text tab** → copy the auto-generated *Methods* + *Results* paragraphs straight into your manuscript.
- On the **💾 Export** tab → click **📥 Download Settings JSON** (safeguard against Colab timeouts).

---

## 3. Moderators (Cells 8–15) — *Optional*

Skip this whole section if you only need the pooled estimate.

**Categorical moderator (Cells 8–11):**
- **Run Cell 8** → pick a column under **Moderator 1** → click **💾 Save Configuration & Proceed**.
- **Run Cell 9** → results auto-populate. 🎁 Grab the **📝 Publication Text** tab.
- **Run Cell 10** → click **📊 Generate Forest Plot**.
- **Run Cell 11** → click **🌳 Generate Orchard Plot**.

**Continuous moderator (Cells 12–13):**
- **Run Cell 12** → pick a numeric column under **Moderator** → click **▶ Run Meta-Regression**. 🎁 Grab **📝 Publication Text**.
- **Run Cell 13** → click **Generate Plot** (bubble plot).

**Non-linear moderator (Cells 14–15):**
- **Run Cell 14** → pick moderator, leave **Spline df = 3** → click **▶ Run Spline Analysis**. 🎁 Grab **📝 Publication Text**.
- **Run Cell 15** → click **Generate plot**.

---

## 4. Bias & Robustness (Cells 16–22)

Just run through them in order. Accept every default. Collect text from each **📝 Publication Text** tab.

- **Run Cell 16** (Egger's + Trim-and-Fill) → click **▶ Run Publication Bias Analysis**. 🎁 **📝 Publication Text**.
- **Run Cell 17** (Trim-and-Fill plot) → click **Generate Plot**.
- **Run Cell 18** (PET-PEESE) → leave **P-threshold** at 0.10 → click **▶ Run PET-PEESE**.
- **Run Cell 19** (Funnel plot) → click **📊 Generate Funnel Plot**.
- **Run Cell 20** (Leave-One-Out) → click **▶ Run Sensitivity Analysis**. 🎁 **📝 Publication Text**.
- **Run Cell 21** (LOO plot) → click **📊 Generate LOO Plot**.
- **Run Cell 22** (Baujat plot) → click **📊 Generate Baujat Plot**.

---

## ✅ Done

Your manuscript-ready *Methods* and *Results* paragraphs are now sitting in the **📝 Publication Text** tabs of Cells 7, 9, 12, 14, 16, and 20. Concatenate, paste into your draft, ship it.

> Optional extras: Cell 23/25 (cumulative meta-analysis) and Cell 24 (geographic map).
