# Power BI Dashboard Guide
## Labour Market Intelligence Dashboard — India

**Author:** Rupal Rani | TISS Mumbai  
**Purpose:** Step-by-step guide to building the Power BI dashboard layer on top of the Python analysis output

> **Note:** This guide was written against the synthetic-demo schema (`social_group`, `formality`, `rural_urban`, etc. — see `data_dictionary.md`). If you are building the dashboard from the **real PLFS results**, substitute the equivalent real-data tables (`outputs/tables/*_PLFS.csv`) and column names from `data_dictionary_PLFS_real.md` (`grp`, `urban`, `sex`, `state`, `quarter`). The DAX patterns and page layout below apply unchanged either way — only the field names differ.

---

## Overview

The Python script (`src/analysis.py`) produces all the core outputs. Power BI sits on top of those outputs as the **presentation and exploration layer** — it turns the CSV tables and figures into an interactive dashboard that non-technical audiences can navigate.

The dashboard has four pages:

| Page | Title | Contents |
|------|-------|----------|
| 1 | Labour Overview | LFPR, WPR, unemployment, informality KPI cards + bar charts |
| 2 | Group Comparisons | Wage by social group, sex, sector — interactive slicers |
| 3 | Wage Gap | Oaxaca decomposition visual + Mincer coefficient chart |
| 4 | Inequality | Lorenz curve, Gini and Theil index, state-level map |

---

## Step 1: Load Data into Power BI

1. Open Power BI Desktop.
2. Click **Get Data → Text/CSV**.
3. Load `outputs/tables/full_results_summary.csv`.
4. Also load `data/synthetic/plfs_synthetic_clean.csv` — this is the record-level data used for dynamic visuals.
5. Click **Transform Data** → open Power Query Editor.

---

## Step 2: Data Transformations in Power Query

Apply these transformations to `plfs_synthetic_clean`:

| Step | Action |
|------|--------|
| Filter employed workers | Keep rows where `activity_status = "Employed"` (for wage visuals) |
| Change type | Set `monthly_wage`, `survey_weight`, `years_education` as Decimal Number |
| Add column: Education band | Custom column: `= if [years_education] <= 5 then "Primary" else if [years_education] <= 8 then "Middle" else if [years_education] <= 10 then "Secondary" else if [years_education] <= 12 then "Higher Sec" else if [years_education] <= 15 then "Under-grad" else "Post-grad"` |
| Add column: Wage band | Custom column: bins in ₹5,000 steps |

---

## Step 3: DAX Measures

Create the following DAX measures in a dedicated `_Measures` table:

```dax
-- Weighted mean wage
Weighted Mean Wage = 
DIVIDE(
    SUMX(plfs_workers, [monthly_wage] * [survey_weight]),
    SUM(plfs_workers[survey_weight])
)

-- Gender wage gap (%)
Gender Wage Gap % = 
VAR MaleWage = 
    CALCULATE([Weighted Mean Wage], plfs_workers[sex] = "Male")
VAR FemaleWage = 
    CALCULATE([Weighted Mean Wage], plfs_workers[sex] = "Female")
RETURN
    DIVIDE(MaleWage - FemaleWage, MaleWage) * 100

-- LFPR (use summary table)
LFPR % = 
CALCULATE(
    DIVIDE(
        SUMX(FILTER(plfs_workers, [activity_status] IN {"Employed","Unemployed"}), [survey_weight]),
        SUM(plfs_workers[survey_weight])
    )
) * 100

-- Informality share (among employed)
Informality Share % = 
CALCULATE(
    DIVIDE(
        CALCULATE(SUM(plfs_workers[survey_weight]), plfs_workers[formality] = "Informal"),
        SUM(plfs_workers[survey_weight])
    ),
    plfs_workers[activity_status] = "Employed"
) * 100
```

---

## Step 4: Page 1 — Labour Overview

### KPI Cards (top row)
Insert **Card** visuals for:
- `LFPR %` (Male, Female, Overall) — use three separate cards
- `Informality Share %`
- `Gender Wage Gap %`

Format: Bold number, small subtitle label, no border, light background

### Bar Charts
- **LFPR by sex:** Clustered bar, X = sex, Y = `LFPR %`
- **Unemployment by group:** Clustered bar, X = social_group, Y = unemployment rate measure
- **Informality by sector:** Clustered bar, X = sector, Y = `Informality Share %`

### Slicer
Add a **state slicer** (list style) to filter all visuals on the page.

---

## Step 5: Page 2 — Group Comparisons

### Grouped Bar Chart
- X axis: `social_group`
- Values: `Weighted Mean Wage`
- Legend: `sex`
- Sort: descending by wage

### Matrix (Pivot Table equivalent)
- Rows: `social_group`
- Columns: `sex`
- Values: `Weighted Mean Wage`
- Conditional formatting: data bars on values

### Slicers
- `sector` (multi-select)
- `rural_urban`
- `formality`

---

## Step 6: Page 3 — Wage Gap

### Oaxaca Decomposition Visual
Power BI does not have a native Oaxaca chart. Use a **100% Stacked Bar Chart**:
- Create a summary table (hard-code or import from `outputs/tables/oaxaca_decomposition.csv`)
- X = "Gap component", Y = Share (%), Legend = Explained vs. Unexplained
- Colours: #5BAD76 (explained) and #D95F5F (unexplained)

Add a **text box** with the interpretive note: *"The unexplained component is not equivalent to discrimination — it also captures unobserved factors (Blinder, 1973; Oaxaca, 1973)."*

### Mincer Coefficient Chart
Import `outputs/tables/mincer_regression.csv` into Power BI.
Create a **horizontal bar chart**:
- Y = Variable (filtered to key regressors)
- X = Coefficient
- Conditional formatting: red bars for negative, blue for positive
- Add error bars using ±1.96 × Std_Error (requires custom visual or DAX)

---

## Step 7: Page 4 — Inequality

### Lorenz Curve
The Lorenz curve requires a line chart with the **Lorenz data** from Python:
- Import `lorenz_curve_data.csv` (add a save step to the Python script)
- X = `Cumulative_Population`, Y = `Cumulative_Income`
- Add a second series: Y = X (the line of perfect equality)
- Title: `"Lorenz Curve — Gini = 0.319"`

### KPI Cards
- Gini coefficient
- Theil T (total)
- Theil within-sex share (91.1%)
- Theil between-sex share (8.9%)

### State Map
- Use Power BI's **Filled Map** visual
- Location: `state`
- Values: `Weighted Mean Wage`
- Colour: blue gradient

---

## Step 8: Formatting and Branding

### Consistent Colour Palette
| Group | Hex |
|-------|-----|
| Male | #2C6E9B |
| Female | #D95F5F |
| Formal | #2C6E9B |
| Informal | #D95F5F |
| SC/ST | #9B59B6 |
| Background | #FAFAFA |
| Text | #222222 |

### Typography
- Title: Segoe UI Semibold, 16pt
- Subtitle / label: Segoe UI, 11pt
- KPI number: Segoe UI Bold, 28pt

### Footer (every page)
> *Analysis uses synthetic data mirroring PLFS structure. Replace with MoSPI PLFS microdata for research estimates. Author: Rupal Rani | TISS Mumbai.*

---

## Step 9: Publish and Share

1. **Save as .pbix** — commit to the GitHub repo in a `/dashboard` folder.
2. **Publish to Power BI Service** — free account works for sharing.
3. **Share the link** on your LinkedIn post and in your GitHub README.
4. **Export as PDF** (File → Export → Export to PDF) for offline portfolios.

---

## Excel Companion (Summary)

Your existing `Project4_Labour_Workbook.xlsx` already has the live engine (Sheet 05) and formula library (Sheet 09). To extend it:

1. **Paste the results CSV** (`full_results_summary.csv`) into a new sheet named `11_PY_Results`.
2. **Create a PivotTable** on `Sheet 05` data → pivot by sex and social_group, value = MonthlyWage.
3. **Create sparklines** in the summary sheet showing wage trends by group.
4. **Add slicers** to the PivotTable for interactive filtering.
5. **Insert PivotChart** (clustered bar) for wage by group — this is your Excel visualisation.

The workbook already demonstrates: SUMIFS, AVERAGEIFS, MEDIAN(IF()), SLOPE, COUNTIF, XLOOKUP, LET, UNIQUE, FILTER, and the Gini formula. These are exactly the Excel skills screened for in entry-level analyst roles.

---

## Portfolio Submission Checklist

- [ ] Python script runs end-to-end with `python src/analysis.py`
- [ ] All 9 figures saved to `outputs/figures/`
- [ ] SQL script reviewed and tested
- [ ] Power BI .pbix file saved and published (or screenshots included)
- [ ] Excel workbook updated with Python results
- [ ] README.md is complete and links to all outputs
- [ ] Research report reviewed for accuracy
- [ ] GitHub repository is public with a proper description and topics
- [ ] LinkedIn post drafted and scheduled
- [ ] Data transparency note visible on every output

---

*Power BI Desktop download: powerbi.microsoft.com (free)*  
*PLFS microdata: mospi.gov.in/web/plfs*
