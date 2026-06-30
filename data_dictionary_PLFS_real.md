# Data Dictionary — PLFS 2022–23 Real Data Analysis

**Applies to:** `src/plfs_real_analysis.py` and all `*_PLFS.csv` / `*_PLFS.png` outputs  
**Source:** Periodic Labour Force Survey (PLFS) 2022–23, MoSPI, Government of India  
**Author:** Rupal Rani | TISS Mumbai

> This dictionary covers the **real PLFS data pipeline**. The synthetic demonstration pipeline (`src/analysis.py`) uses a different, simplified schema documented separately in `data_dictionary.md`. The two are not interchangeable — column names and category labels differ between them (e.g., the real data uses `Gen` for the General category; the synthetic demo uses `General`).

---

## 1. Raw PLFS Columns Used

The source extract (`plfs_large.csv`) contains 129 columns mirroring the official PLFS household and person schedules. The columns actually used in this analysis are listed below; all other columns (daily activity logs, household consumption expenditure, FSU/stratum sampling identifiers, etc.) were left untouched.

| Raw Column | Type | Description |
|------------|------|--------------|
| `Current Weekly Status (CWS)` | Integer code | Employment status in the reference week. Codes 11, 21, 31, 32 indicate employed (wage/salaried, self-employed variants); used to define the analytic sample. |
| `earnings` | Numeric | Reported earnings for the activity (₹). Primary wage variable. |
| `gender` | String | `Male`, `Female`, `Other` |
| `Social_Cat` | String | Social category: `Gen` (General), `OBC`, `SC`, `ST` |
| `education_yr` | Numeric | Total years of formal education completed |
| `Age` | Integer | Age in completed years (16–59 in this extract) |
| `Sector` | Integer | `1` = Rural, `2` = Urban |
| `State/Ut Code` | Integer | Numeric state/UT identifier (mapped to state names in code) |
| `Quarter` | String | PLFS survey quarter label (`Q5`–`Q8` in this extract) |
| `Survey Date` | String (DDMMYYYY) | Date of household visit |
| `Sub-sample wise Multiplier` | Numeric | Survey weight — **required for all population-level estimates** |

---

## 2. Derived Analysis Variables

Created in `load_and_prepare()` in `src/plfs_real_analysis.py`:

| Variable | Formula / Source | Description |
|----------|------------------|--------------|
| `sex` | `gender.strip()` | Cleaned sex label |
| `group` | `Social_Cat.strip()` | Cleaned social group label: `Gen`, `OBC`, `SC`, `ST` |
| `education` | `education_yr`, clipped to [0, 22] | Years of schooling for the Mincer model |
| `age` | `Age` | Age in years |
| `experience` | `age − education − 6`, floored at 0 | Mincer potential-experience proxy |
| `exp2` | `experience²` | Quadratic experience term |
| `wage` | `earnings` | Monthly wage (₹) |
| `log_wage` | `ln(wage)` | Dependent variable for all regressions |
| `weight` | `Sub-sample wise Multiplier` | Survey weight |
| `urban` | 1 if `Sector == 2`, else 0 | Location binary |
| `state` | `State/Ut Code` mapped via `STATE_MAP` | State/UT name |
| `quarter` | `Quarter.strip()` | Survey quarter label |
| `female` | 1 if `sex == "Female"`, else 0 | Regression dummy |
| `grp_OBC` / `grp_SC` / `grp_ST` | 1 if `group == "OBC"/"SC"/"ST"`, else 0 | Social group dummies (reference = General) |

---

## 3. Analytic Sample Definition

Starting sample: 42,803 raw person-records.

| Step | Filter | Resulting N |
|------|--------|-------------|
| 1 | `Current Weekly Status (CWS)` ∈ {11, 21, 31, 32} (employed) | 41,929 |
| 2 | `earnings` > 0 | 41,913 |
| 3 | Drop rows missing `log_wage`, `education`, `experience`, `weight`, `sex`, or `group` | 41,913 (no further loss) |

**Final analytic sample: 41,913 employed wage workers.**

---

## 4. Survey Period

The `Quarter` field (`Q5`–`Q8`) does **not** correspond to calendar-year quarters. Cross-referencing `Survey Date` confirms:

| Quarter Label | Calendar Period |
|---------------|------------------|
| Q5 | July – September 2022 |
| Q6 | October – December 2022 |
| Q7 | January – March 2023 |
| Q8 | April – June 2023 |

This corresponds to the **PLFS 2022–23 annual round** (July 2022 – June 2023), the standard PLFS reporting year used by MoSPI. **Always verify this kind of period mapping directly from `Survey Date` rather than assuming quarter labels match calendar quarters** — this was caught and corrected during this project's own development.

---

## 5. Social Group and State Coding

### Social Group (`Social_Cat`)
| Code in data | Meaning |
|---------------|---------|
| `Gen` | General category |
| `OBC` | Other Backward Classes |
| `SC` | Scheduled Castes |
| `ST` | Scheduled Tribes |

### State/UT Code Mapping
A 36-entry mapping (`STATE_MAP` in code) converts numeric PLFS state codes to state names, following the standard MoSPI state code list. Two codes (28 and 37) both map to "Andhra Pradesh" entries reflecting the undivided/successor coding used across survey rounds — flagged in code comments for any analyst extending this work to merge or compare across years.

---

## 6. Survey Weight Guidance

> **Every estimate in `plfs_real_analysis.py` uses `weight` (the survey multiplier). Never compute an unweighted mean or proportion and present it as a population estimate.**

Weighted mean formula used throughout:
```python
np.average(values, weights=weight)
```

Weighted regression (WLS) scales the design matrix by normalized weights before solving the normal equations — see `mincer_regression()` and `oaxaca_decomposition()` in the source code for the exact implementation.

---

## 7. Known Data Caveats

1. **This is a working extract, not the complete PLFS national file.** It should not be cited as an official MoSPI statistic. Cross-check any headline figure against MoSPI's published PLFS Annual Report before using it outside this portfolio/research context.
2. **Sample composition:** 28,381 of 42,803 raw records (66%) are Urban-sector records, compared with PLFS's typical population urban share of roughly 35%. This may reflect a deliberate urban-oversampled extract rather than a representativeness problem — but it reinforces why survey weights, not raw counts, must drive every estimate.
3. **`total_wages` is largely zero/unused** in this extract (only 38 non-zero values out of 42,803); `earnings` is the populated, reliable wage field and is used throughout instead.
4. **No top-coding applied** to `earnings` in the current pipeline — see Limitations in the research report for the recommended robustness check.

---

## 8. PLFS Official Documentation

For the authoritative PLFS data dictionary, codebooks, and the full national microdata file, see MoSPI's PLFS portal: [mospi.gov.in/web/plfs](https://mospi.gov.in/web/plfs)
