# 🇮🇳 Labour Market Intelligence Dashboard — India

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

**Author:** Rupal Rani | Tata Institute of Social Sciences, Mumbai  
**Data:** PLFS 2022–23 unit-level microdata (MoSPI, Government of India) — 41,913 wage workers  
**Status:** Complete analysis on real government survey data. Suitable for portfolio, GitHub, LinkedIn, and research submission.

---

## Project Overview

This project analyses real Periodic Labour Force Survey (PLFS) microdata to answer four questions about India's labour market:

1. **How do wages differ** across gender, social group, education, sector, and state?
2. **What is the return to education?** (Mincer earnings regression)
3. **How much of the gender wage gap reflects different worker characteristics, and how much reflects different returns to those characteristics?** (Blinder–Oaxaca decomposition)
4. **How unequal are wages,** and how much of that inequality is between vs. within gender groups? (Gini + Theil index)

---

## Data

**Source:** Periodic Labour Force Survey (PLFS) 2022–23, Ministry of Statistics and Programme Implementation (MoSPI), Government of India.  
**Coverage period:** July 2022 – June 2023 (four quarters, the official PLFS annual round).  
**Sample:** 41,913 employed wage workers with positive earnings, aged 16–59, across 36 states/UTs.  
**Identification:** Survey weights (`Sub-sample wise Multiplier`) applied to every estimate.

> **Note on representativeness:** This is a working extract of PLFS unit-level records rather than the full national file. All estimates use the supplied survey weights, but readers seeking official national or state PLFS indicators should cross-check against MoSPI's published PLFS Annual Report. This caveat is stated for transparency, consistent with good research practice.

---

## Key Findings

| Metric | Value |
|--------|-------|
| Sample size (wage workers) | 41,913 |
| Overall mean monthly wage | ₹20,010 |
| Male mean wage | ₹21,136 |
| Female mean wage | ₹16,388 |
| **Raw gender wage gap (arithmetic mean)** | **22.5%** |
| Return to schooling (Mincer) | **10.3% per year** |
| Female wage penalty, controlling for education/experience/group/location | 34.5% |
| **Oaxaca — Explained by endowments** | **0.3% of gap** |
| **Oaxaca — Unexplained (differential returns)** | **99.7% of gap** |
| Gini Coefficient (wages) | 0.427 |
| Theil T Index | 0.316 |
| Theil — within-sex share | 98.3% |

---

## Headline Finding: The Gender Wage Gap Is a "Returns" Story, Not a "Characteristics" Story

This is the most important and most carefully checked result in the analysis. Standard expectation in labour economics is that part of a gender wage gap reflects women having, on average, less education or experience than men. **In this sample, that is not what is happening.** Weighted male and female workers have very similar average education (11.1 vs 10.7 years) and a similar urban share (55% vs 59%). Because the two groups look alike on paper, the Blinder–Oaxaca decomposition attributes almost none of the gap (0.3%) to differences in these characteristics. Nearly the entire gap (99.7%) comes from women being paid less than men *for the same measured characteristics*.

**This finding needs a caveat, and the project states it clearly:** female labour force participation in India is much lower than male participation, so the women who do show up in a wage-employment dataset are a selected group — likely more educated and more urban than women overall. This selection can make male and female wage-workers look more similar on paper than the male and female populations as a whole. A Heckman selection correction is the standard next step to address this, and it is listed as a limitation and a future extension, not glossed over.

---

## Methods

### 1. Survey-Weighted Descriptive Statistics
All means, by sex, social group, sector, education, and state, use PLFS survey weights — never simple sample averages.

### 2. Mincer Earnings Regression (Weighted Least Squares)
```
ln(wage) = α + β₁·education + β₂·experience + β₃·experience² + female + urban + group dummies + ε
```
Estimated with WLS using survey weights and heteroskedasticity-robust (sandwich) standard errors. Reference: Mincer (1974).

### 3. Blinder–Oaxaca Decomposition
Separates the mean gender log-wage gap into a part explained by differing characteristics and a part reflecting differing returns to those characteristics. References: Blinder (1973), Oaxaca (1973).

### 4. Inequality Measures
Gini coefficient (Lorenz curve, weighted) and Theil T index (decomposed into within-sex and between-sex components). References: Theil (1967), Atkinson (1970).

---

## Visualisations

| Figure | Description |
|--------|-------------|
| `01_wage_sex_group_PLFS.png` | Mean wage by sex and by social group |
| `02_wage_education_PLFS.png` | Mean wage by education band |
| `03_mincer_PLFS.png` | Mincer regression coefficient plot with 95% CIs |
| `04_oaxaca_PLFS.png` | Oaxaca decomposition — explained vs. unexplained |
| `05_lorenz_gini_PLFS.png` | Lorenz curve with Gini and Theil values |
| `06_wage_state_PLFS.png` | Mean wage by state (states with n ≥ 200) |
| `07_wage_distributions_PLFS.png` | Wage distributions by sex and location |
| `08_gender_gap_heterogeneity_PLFS.png` | Gender gap by social group and education |
| `09_oaxaca_components_PLFS.png` | Variable-by-variable Oaxaca contribution |

---

## Project Structure

```
labour-market-intelligence/
│
├── README.md
├── requirements.txt
├── data_dictionary.md
├── .gitignore
│
├── src/
│   ├── plfs_real_analysis.py     ← Main analysis (real PLFS data) — run this
│   ├── analysis.py               ← Synthetic-data demo version (methodology showcase)
│   └── sql_analysis.sql          ← SQL query library
│
├── data/
│   ├── raw/                      ← Place PLFS microdata CSV here (gitignored — not redistributed)
│   └── synthetic/                ← Synthetic demo data for the methodology showcase
│
├── outputs/
│   ├── figures/                  ← 9 real-data figures + 9 synthetic-demo figures
│   └── tables/                   ← CSV result tables (real data: *_PLFS.csv)
│
├── reports/
│   └── research_report.md        ← Full written research report (real data)
│
└── docs/
    ├── linkedin_post.md
    ├── interview_guide.md
    └── powerbi_excel_guide.md
```

---

## How to Run

```bash
git clone https://github.com/rupalrani/labour-market-intelligence.git
cd labour-market-intelligence
pip install -r requirements.txt

# Place your PLFS microdata extract at data/raw/plfs_large.csv, then:
python src/plfs_real_analysis.py
```

PLFS microdata is not redistributed in this repository (see `.gitignore`). Obtain it directly from [mospi.gov.in/web/plfs](https://mospi.gov.in/web/plfs).

---

## Skills Demonstrated

| Skill | Where Applied |
|-------|--------------|
| **Real government microdata handling** | 129-column PLFS extract, 42,803 raw records |
| **Survey weighting** | Every estimate population-weighted, never raw sample means |
| **Python (pandas, numpy, scipy)** | Cleaning, weighted statistics, custom WLS regression |
| **Statistical modelling** | Mincer WLS regression with robust SEs, Blinder–Oaxaca decomposition |
| **Inequality measurement** | Gini (Lorenz), Theil T (within/between decomposition) |
| **Data visualisation** | 9 publication-grade charts |
| **SQL** | Full query library for the same indicators |
| **Critical interpretation** | Identified and explained a counter-intuitive Oaxaca result rather than hiding it |
| **Research writing** | APA citations, transparent limitations, reproducible code |

---

## Limitations (Honest Assessment)

1. **This is a working extract, not the full PLFS national file.** Estimates should be cross-checked against MoSPI's official published indicators before being cited as national statistics.
2. **Selection into wage employment.** Female labour force participation is much lower than male; the wage-employed women in this sample are not representative of all working-age women. This likely explains the unusually small "explained" share in the Oaxaca decomposition. A Heckman correction is the natural next step.
3. **Limited control set.** The regression controls for education, experience, sex, social group, and urban/rural location, but not occupation, industry detail, firm size, hours worked, or job tenure. Richer controls would likely raise the explained share of the gender gap and should be added before strong causal claims are made.
4. **Cross-sectional design.** PLFS captures a snapshot; the regression shows associations, not causal effects.
5. **Unexplained ≠ discrimination.** The Oaxaca unexplained component captures differential returns to observed characteristics, but also unobserved skill, job characteristics, and model specification. It is an upper bound, not a clean discrimination estimate.
6. **No top-coding applied.** Extreme wage values were retained as reported; no winsorization was applied. A robustness check with top-coding at the 99th percentile is a reasonable extension.

---

## Data Sources & References

- Ministry of Statistics and Programme Implementation. (2024). *Periodic Labour Force Survey (PLFS) Annual Report, 2022–23.* Government of India. [mospi.gov.in](https://mospi.gov.in)
- Mincer, J. (1974). *Schooling, Experience, and Earnings.* NBER.
- Blinder, A. S. (1973). Wage discrimination: Reduced form and structural estimates. *Journal of Human Resources, 8*(4), 436–455.
- Oaxaca, R. (1973). Male-female wage differentials in urban labor markets. *International Economic Review, 14*(3), 693–709.
- Theil, H. (1967). *Economics and Information Theory.* North-Holland.
- Atkinson, A. B. (1970). On the measurement of inequality. *Journal of Economic Theory, 2*(3), 244–263.
- Heckman, J. J. (1979). Sample selection bias as a specification error. *Econometrica, 47*(1), 153–161.
- International Labour Organization. (2018). *Women and men in the informal economy: A statistical picture* (3rd ed.). ILO.
- International Labour Organization. (2019). *Global Wage Report 2018/19: What lies behind gender pay gaps.* ILO.

---

## Licence

Code: MIT Licence.  
PLFS microdata: subject to MoSPI terms of use — not redistributed in this repository.

---

*Part of an Analytics Portfolio prepared by Rupal Rani, Tata Institute of Social Sciences, Mumbai.*
