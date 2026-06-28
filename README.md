# 🏛️ Labour Market Intelligence Dashboard

> PLFS-based labour market analytics for India — combining Mincer wage regression (returns to schooling) and Blinder-Oaxaca decomposition to quantify the unexplained gender wage gap, visualised in an interactive Tableau dashboard.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Statsmodels](https://img.shields.io/badge/Statsmodels-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

---

## 📌 Overview

This project builds a **Labour Market Intelligence (LMI) system** using India's Periodic Labour Force Survey (PLFS) — the country's primary household survey for employment and wage data.

Two econometric techniques anchor the analysis:

1. **Mincer Earnings Regression** — estimates the private returns to an additional year of schooling, controlling for work experience and other individual characteristics
2. **Blinder-Oaxaca Decomposition** — decomposes the raw gender wage gap into an *explained* component (differences in endowments such as education and experience) and an *unexplained* component (residual discrimination / structural differences)

Results are served through an interactive **Tableau dashboard** and supported by a structured Excel workbook with a full systematic literature review (PRISMA protocol).

---

## 🏆 Key Results

| Metric | Value |
|--------|-------|
| Data source | PLFS (Periodic Labour Force Survey), Government of India |
| Method 1 | Mincer earnings regression — returns to schooling |
| Method 2 | Blinder-Oaxaca decomposition — gender wage gap |
| Literature review | 10 sources included; 8 live-verified references (PRISMA) |
| Workbook | 11-sheet structured research workbook |
| Visualisation | Interactive Tableau dashboard |
| Report | Full DOCX research report with policy implications |

---

## 🔍 Methodology

```
1. Data Acquisition & Cleaning (PLFS)
   ├── Extract individual-level wage, education, employment data
   ├── Handle unit-record survey weights for nationally representative estimates
   └── Construct derived variables: log-wages, experience (proxy), education years

2. Descriptive Labour Market Analysis
   ├── Labour Force Participation Rate (LFPR) by gender, state, sector
   ├── Worker Population Ratio (WPR) and Unemployment Rate (UR)
   └── Wage distribution by education level, occupation, industry

3. Mincer Earnings Regression
   ├── OLS: log(wage) = α + β₁(schooling) + β₂(experience) + β₃(experience²) + ε
   ├── Controls: gender, sector (urban/rural), industry, occupation
   └── Coefficient β₁ = private returns to one additional year of schooling

4. Blinder-Oaxaca Decomposition
   ├── Estimate separate wage equations for men and women
   ├── Decompose gender gap into: explained (endowments) + unexplained (coefficients)
   └── Identify key drivers of the explained and unexplained components

5. Systematic Literature Review (PRISMA)
   ├── 10 studies included after PRISMA screening
   ├── 8 references live-verified
   └── Synthesised across returns to education and gender wage gap literature

6. Visualisation (Tableau)
   └── Interactive dashboard: LFPR maps, wage distributions, decomposition charts
```

---

## 📁 Repository Structure

```
labour-market-intelligence/
│
├── README.md
├── requirements.txt
│
├── scripts/
│   ├── 01_data_cleaning.py          # PLFS data cleaning and feature engineering
│   ├── 02_descriptive_analysis.py   # LFPR, WPR, UR by subgroup
│   ├── 03_mincer_regression.py      # OLS Mincer wage equation
│   ├── 04_oaxaca_decomposition.py   # Blinder-Oaxaca gender wage gap decomposition
│   ├── build_workbook4.py           # Script to build the research Excel workbook
│   ├── verify_workbook.py           # Workbook integrity verification script
│   └── sql_queries.sql              # SQL extraction and aggregation queries
│
├── data/
│   └── README.md                    # PLFS data source info and access instructions
│
└── outputs/
    └── README.md                    # Dashboard screenshots and chart exports
```

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Data Source
This project uses **India's Periodic Labour Force Survey (PLFS)** — available free from the Ministry of Statistics and Programme Implementation (MoSPI):  
🔗 [https://mospi.gov.in/periodic-labour-force-survey-plfs](https://mospi.gov.in/periodic-labour-force-survey-plfs)

Download the unit-level data and place the raw files in the `data/` folder.

### Run the Analysis
```bash
# Step 1: Clean PLFS data
python scripts/01_data_cleaning.py

# Step 2: Descriptive labour market analysis
python scripts/02_descriptive_analysis.py

# Step 3: Mincer regression
python scripts/03_mincer_regression.py

# Step 4: Blinder-Oaxaca decomposition
python scripts/04_oaxaca_decomposition.py

# Step 5: Build research workbook
python scripts/build_workbook4.py
```

---

## 📊 Key Outputs

| Output | Description |
|--------|-------------|
| Tableau Dashboard | Interactive LMI dashboard: LFPR trends, wage distributions, gender gap decomposition |
| Research Report | Full DOCX report with literature review, methodology, results, policy implications |
| Excel Workbook | 11-sheet workbook: PRISMA review, data profile, regression tables, references |
| SQL Scripts | Reproducible data extraction and aggregation queries |

---

## 📚 Systematic Literature Review (PRISMA)

A PRISMA-compliant systematic review was conducted to contextualise findings:

| Stage | Count |
|-------|-------|
| Total records identified | 10 |
| Live-verified references | 8 |
| Final included studies | 10 |
| Consistency check | ✅ MATCH |

---

## 🌍 Policy Relevance

| Insight | Implication |
|---------|-------------|
| Returns to schooling | Informs education investment priorities across gender and sector |
| Unexplained wage gap | Points to labour market discrimination — relevant for equal pay legislation |
| LFPR by state | Highlights geographic disparities in female workforce participation |
| Sectoral wage distribution | Guides targeted skilling and workforce development interventions |

---

## 👩‍💻 About

Developed as **Portfolio Project 4** — part of an end-to-end analytics portfolio built during BS Analytics & Sustainability Studies at TISS Mumbai. Draws on fieldwork experience at Aajeevika Bureau (India LabourLine) and academic training in development economics and labour studies.

📫 [rupalrani2303@gmail.com](mailto:rupalrani2303@gmail.com) · [LinkedIn](https://www.linkedin.com/in/rupal-rani-a23b36257) · [GitHub](https://github.com/rupalrani)
