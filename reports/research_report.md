# Wage Gaps and Earnings Inequality in India: Evidence from PLFS 2022–23 Microdata

**Author:** Rupal Rani  
**Affiliation:** Tata Institute of Social Sciences, Mumbai  
**Data:** Periodic Labour Force Survey (PLFS) 2022–23, MoSPI, Government of India  
**Date:** 2024

---

## Abstract

This study examines wage determination and inequality in India using Periodic Labour Force Survey (PLFS) 2022–23 unit-level microdata covering 41,913 employed wage workers across 36 states and union territories. A survey-weighted Mincer earnings regression finds a return to schooling of approximately 10.3 percent per additional year of education. The raw gender wage gap is 22.5 percent by arithmetic mean and equivalent to a 34.5 percent female wage penalty after controlling for education, experience, social group, and urban/rural location. A Blinder-Oaxaca decomposition produces a striking result: only 0.3 percent of the gender wage gap is attributable to differences in observable worker characteristics between men and women; 99.7 percent reflects differential returns to the same characteristics. This pattern is interpreted with care: because female labour force participation is substantially lower than male participation, the women observed in wage employment are a selected, relatively advantaged subgroup whose characteristics resemble male workers more closely than the female working-age population as a whole. Wage inequality, measured by a Gini coefficient of 0.427, is moderate-to-high, with 98.3 percent of total Theil inequality occurring within rather than between gender groups. These findings carry direct relevance for understanding how wage-setting, not differential human capital accumulation, drives the gender pay gap among India's wage-employed workforce.

**Keywords:** PLFS, wage inequality, gender pay gap, Mincer earnings function, Blinder-Oaxaca decomposition, selection bias, India, labour economics

---

## 1. Introduction

India's labour market is characterised by low female labour force participation, substantial informality, and persistent wage disparities across social groups (International Labour Organization, 2019; National Commission for Enterprises in the Unorganised Sector, 2009). The Periodic Labour Force Survey (PLFS), conducted by the Ministry of Statistics and Programme Implementation (MoSPI) since 2017, is the principal source of systematic data on employment and wages in India, producing quarterly and annual estimates at the national and state level (Ministry of Statistics and Programme Implementation, 2024).

This study uses PLFS 2022–23 unit-level microdata to examine three linked questions. First, what is the return to education in the Indian wage-employed labour force, estimated through a Mincer earnings function (Mincer, 1974)? Second, how large is the gender wage gap, and how much of it reflects differences in worker characteristics versus differences in the returns paid for those characteristics, examined through a Blinder-Oaxaca decomposition (Blinder, 1973; Oaxaca, 1973)? Third, how unequal are wages overall, and how much of that inequality lies between gender groups versus within them, measured using the Gini coefficient and the Theil index (Theil, 1967; Atkinson, 1970)?

The analysis produces a result that departs from a common prior in the literature: differences in observable characteristics between male and female wage workers in this sample are small, so almost the entire wage gap reflects differential treatment for similar workers rather than a gap in qualifications or experience. This paper reports that finding transparently, together with the selection-bias caveat required to interpret it correctly.

---

## 2. Data and Methods

### 2.1 Data Source

The data are drawn from PLFS unit-level microdata for the period July 2022 to June 2023, corresponding to the PLFS 2022–23 annual round (Ministry of Statistics and Programme Implementation, 2024). The working extract used in this study contains 42,803 individual records across 129 variables, including demographic information, education, employment status under both Usual Principal Status and Current Weekly Status, wages, household characteristics, and the survey multiplier required for population-weighted estimation.

The analytic sample restricts to individuals with Current Weekly Status codes indicating employment (wage and salaried work) and strictly positive reported earnings, yielding 41,913 records. All descriptive statistics and regression estimates use the PLFS survey weight (`Sub-sample wise Multiplier`) to produce population-representative estimates, consistent with PLFS documentation guidance that unweighted sample statistics should not be interpreted as population estimates.

**A transparency note on representativeness:** this is a working extract rather than the complete PLFS national file. Readers requiring official national or state-level PLFS indicators should consult MoSPI's published PLFS Annual Report directly. The estimates in this paper are presented as an independent analysis of microdata, not as a restatement of official MoSPI headline figures.

### 2.2 Variable Construction

| Variable | Construction |
|----------|--------------|
| Monthly wage | `earnings` field; employed wage workers with earnings > 0 |
| Years of education | `education_yr`, top-coded at 22 |
| Experience | age − years of education − 6, floored at zero (Mincer proxy) |
| Sex | `gender`: Male / Female |
| Social group | `Social_Cat`: General, OBC, SC, ST |
| Location | `Sector`: Rural (1) / Urban (2) |
| Survey weight | `Sub-sample wise Multiplier` |

### 2.3 Mincer Earnings Regression

Following Mincer (1974), log monthly wages are modelled as:

```
ln(wageᵢ) = α + β₁·educationᵢ + β₂·experienceᵢ + β₃·experienceᵢ²
            + β₄·femaleᵢ + β₅·urbanᵢ + γ·social_groupᵢ + εᵢ
```

The model is estimated by weighted least squares (WLS) using PLFS survey weights, with heteroskedasticity-robust ("sandwich") standard errors computed directly rather than assuming homoskedastic errors.

### 2.4 Blinder-Oaxaca Decomposition

Separate weighted regressions are estimated for male and female sub-samples using the regressors education, experience, experience-squared, urban location, and social group dummies. The twofold decomposition splits the mean log-wage gap as:

```
Δ = (X̄_M − X̄_F)·β̂_M  +  X̄_F·(β̂_M − β̂_F)
   ───────────────────    ──────────────────────
   Explained (endowments)  Unexplained (differential returns)
```

where X̄_M and X̄_F are survey-weighted mean characteristic vectors for male and female workers, and β̂_M and β̂_F are their respective estimated coefficients (Blinder, 1973; Oaxaca, 1973).

### 2.5 Inequality Measures

The Gini coefficient is computed from the survey-weighted Lorenz curve using the trapezoidal-area method. The Theil T index is computed as the weighted mean of (wage/mean wage) × ln(wage/mean wage), and is decomposed into within-sex and between-sex components following the standard additive decomposition (Theil, 1967; Atkinson, 1970).

---

## 3. Results

### 3.1 Descriptive Wage Patterns

**Table 1: Mean Monthly Wage by Sex and Social Group (Survey-weighted, ₹)**

| Group | Male | Female |
|-------|------|--------|
| General | 25,038 | 21,975 |
| OBC | 19,969 | 15,353 |
| SC | 17,474 | 11,074 |
| ST | 18,779 | 12,438 |

The overall weighted mean monthly wage is ₹20,010, with a male mean of ₹21,136 and a female mean of ₹16,388 — a raw arithmetic gender gap of 22.5 percent. Wages rise sharply with education: workers with 0–5 years of schooling earn a weighted mean of ₹10,554 per month, compared with ₹38,948 for workers with 16 or more years of schooling — an almost four-fold difference. Urban workers earn substantially more than rural workers (₹23,135 versus ₹15,975 per month).

### 3.2 Mincer Earnings Regression

**Table 2: Mincer Earnings Regression (Weighted Least Squares)**

| Variable | Coefficient | Std. Error | t | p |
|----------|-------------|------------|---|---|
| Intercept | 8.010 | 0.032 | 249.4 | < 0.001 |
| Years of Education | 0.103 | 0.0015 | 68.3 | < 0.001 |
| Experience | 0.033 | 0.0019 | 17.5 | < 0.001 |
| Experience² | −0.0003 | 0.00004 | −7.1 | < 0.001 |
| Female (= 1) | −0.423 | 0.0156 | −27.1 | < 0.001 |
| Urban (= 1) | 0.241 | 0.0163 | 14.8 | < 0.001 |
| Group: OBC | −0.058 | 0.0191 | −3.0 | 0.002 |
| Group: SC | −0.114 | 0.0220 | −5.2 | < 0.001 |
| Group: ST | −0.034 | 0.0287 | −1.2 | 0.234 |

*R² = 0.421, N = 41,913. Full table in `outputs/tables/mincer_regression_PLFS.csv`.*

The estimated **return to schooling is 10.3 percent per additional year**, holding experience, sex, social group, and location constant. This is on the higher end of returns typically reported for India but within plausible range, and is consistent with the steep observed wage-education gradient in Table 1. The experience profile is concave, as predicted by human capital theory: wages rise with experience but at a diminishing rate.

The coefficient on **Female equals −0.423**, implying a 34.5 percent wage penalty for women relative to observably similar men. This conditional estimate is larger than the unconditional 22.5 percent raw gap, because women in this sample are not, on average, disadvantaged on the observable characteristics in the model — meaning the raw gap understates how much less women are paid for the same measured qualifications. The OBC and SC coefficients are negative and statistically significant, indicating lower wages relative to the General category after controlling for education and experience; the ST coefficient, while negative, is not statistically significant at conventional levels in this specification.

### 3.3 Blinder-Oaxaca Decomposition

**Table 3: Blinder-Oaxaca Decomposition of the Gender Wage Gap**

| Component | Log-wage difference | Share of gap |
|-----------|---------------------|--------------|
| Raw gap (male mean log wage − female mean log wage) | 0.426 | 100.0% |
| Explained (endowments) | 0.001 | 0.3% |
| Unexplained (differential returns) | 0.425 | 99.7% |

This result departs sharply from the common finding in the literature that part of the gender wage gap reflects women's lower average education or experience. **In this sample, male and female wage-employed workers have nearly identical average characteristics:** weighted mean education is 11.1 years for men versus 10.7 years for women, and the urban share is actually higher for women (59.5%) than for men (55.4%). Because the two groups look similar on the variables included in the model, the decomposition attributes almost none of the gap to differing endowments. Practically the entire 22.5–34.5 percent gender wage gap (depending on whether it is expressed as a raw arithmetic difference or as a regression-adjusted log difference) reflects different wages paid for similar measured characteristics, not different characteristics themselves.

**Figure 9 (`09_oaxaca_components_PLFS.png`)** breaks the explained component down by variable. Education and experience-squared push toward a larger explained gap (men have a small education advantage and a different experience-squared profile), while experience itself and urban location push in the opposite direction (women in the sample have, if anything, slightly more favourable values on these dimensions). These offsetting effects are why the net explained share is close to zero rather than substantially positive.

**This finding requires a critical interpretive caveat.** Female labour force participation in India is well below male participation (a well-documented pattern; International Labour Organization, 2019). The women captured in a wage-employment dataset are therefore a selected subset of all working-age women — likely more educated, more urban, and more able to access wage work than women overall. This selection can make male and female *wage workers* look similar on paper even when male and female *populations* differ substantially, because the most disadvantaged women may not appear in wage employment at all. The 99.7 percent unexplained share should accordingly be read as describing the gap *among those who work for wages*, not as a description of gender disparity in the population overall. A Heckman (1979) selection correction, incorporating a labour force participation equation, is the standard next step to address this and is identified as a priority extension in Section 5.

A second, related caveat: the explained share is also constrained by the variables available in this specification. Occupation, industry detail, firm size, hours worked, and job tenure are not included. Richer controls typically raise the explained share of gender wage gaps in the literature, so 0.3 percent should be read as a lower bound on what richer data could explain, not a definitive estimate.

### 3.4 Heterogeneity in the Gender Gap

The gender wage gap varies meaningfully across social group and education level (Figure 8). The gap is smallest in the General category (12.2 percent) and largest among SC workers (36.6 percent), with OBC (23.1 percent) and ST (33.8 percent) in between. By education level, the gap is widest for workers with up to middle-school education (44.2 percent) and narrows substantially among postgraduate workers (22.6 percent), though it does not close even at the highest education level. This pattern suggests that the channels generating the gender wage gap differ by social group and are not fully resolved by higher educational attainment.

### 3.5 Wage Inequality

**Table 4: Inequality Measures**

| Measure | Value |
|---------|-------|
| Gini Coefficient | 0.427 |
| Theil T (total) | 0.316 |
| Theil T (between-sex) | 0.005 (1.7% of total) |
| Theil T (within-sex) | 0.311 (98.3% of total) |

A Gini coefficient of 0.427 indicates moderate-to-high wage inequality among employed workers, consistent with the wide spread between low-education and high-education wage levels documented in Table 1 and Section 3.1. The Theil decomposition shows that **98.3 percent of total wage inequality occurs within gender groups rather than between them.** Even though the gender wage gap itself is large in percentage terms, gender accounts for a small share of overall wage dispersion; the much larger driver of inequality is variation in wages within the male workforce and within the female workforce — most plausibly driven by education, sector, location, and occupation differences that this analysis has only partially captured.

---

## 4. Discussion

### 4.1 Interpreting the Headline Finding

The central empirical contribution of this paper is not simply that a gender wage gap exists in India — that is well documented (International Labour Organization, 2019) — but that, within the wage-employed population captured here, the gap is almost entirely a story of differential pay for similar workers rather than differential qualifications. This has a specific and important policy implication: pay-setting practices, occupational segregation within similar job categories, bargaining power, and possibly unmeasured discrimination, rather than an education or experience gap, appear to be the primary forces sustaining the gender wage gap among formally wage-employed workers in this sample.

At the same time, this finding must not be read in isolation from India's much larger story of female labour force non-participation. The population of women who are *not* in wage employment at all — a far larger group than those captured here — likely faces a different and, in many respects, more severe set of constraints, including unpaid domestic work burdens, social norms, and a lack of suitable formal opportunities. This paper's findings describe the wage-setting gap among those already in wage work; they should not be extrapolated to claims about gender equity in the labour market as a whole.

### 4.2 Policy Implications

Three findings carry direct relevance for policy and further research.

**First**, the size and statistical robustness of the unexplained gender wage gap (34.5 percent in the regression-adjusted estimate) suggests that interventions focused solely on closing education or experience gaps between men and women are unlikely to close the wage gap on their own, since those gaps are already small in the wage-employed population. Interventions targeting pay transparency, equal-pay audits, and occupational segregation within firms are more directly aligned with what this analysis identifies as the dominant channel.

**Second**, the heterogeneity in the gender gap across social groups — smallest for General category workers, largest for SC workers — indicates that gender and social-group disadvantage compound rather than operate independently. Policy responses that treat gender equity and social-group equity as separate tracks may miss this intersectional pattern.

**Third**, the dominance of within-group inequality (98.3 percent of Theil T) over between-gender inequality means that broad-based wage inequality reduction — through minimum wage policy, sectoral upgrading, and education access — would likely have a larger aggregate effect on inequality than gender-targeted interventions alone, even though both remain independently justified.

### 4.3 Limitations

This analysis has several limitations that bound its conclusions.

**Selection into wage employment.** As discussed in Section 3.3, the near-zero explained share in the Oaxaca decomposition is very likely influenced by positive selection of women into wage employment. This is the most important limitation of the paper and the clearest direction for follow-up work using a Heckman (1979) two-step correction with a labour force participation equation.

**Limited control set.** The regression does not include occupation, industry detail at a fine level, firm size, hours of work, or job tenure — all standard controls in more complete wage-gap studies. Including them would likely increase the explained share of the gap and should be treated as a priority extension before the 99.7 percent unexplained figure is cited without qualification.

**Cross-sectional design.** PLFS is a repeated cross-section, not a panel. The regression results are associational, not causal. The schooling coefficient, in particular, may partly reflect unobserved ability rather than a pure causal return to education (the classical "ability bias" concern in the returns-to-education literature).

**Representativeness of this extract.** As stated in Section 2.1, this is a working extract rather than the complete PLFS national file, and official published indicators should be the reference point for any claim about national or state-level PLFS statistics.

**No wage top-coding.** Extreme wage values were retained as reported. A robustness check that top-codes wages at a high percentile (e.g., the 99th) would help confirm that the Mincer and Oaxaca results are not driven by a small number of very high earners.

**Unexplained ≠ discrimination.** Consistent with the original methodological literature (Blinder, 1973; Oaxaca, 1973), the unexplained component of the wage gap captures differential returns to measured characteristics, but it also absorbs unobserved skill, job quality differences, and any mis-specification of the model. It should be treated as an upper bound on discrimination, not a direct measurement of it.

---

## 5. Conclusion and Future Work

This study finds a gender wage gap of 22.5 percent (raw) to 34.5 percent (regression-adjusted) among PLFS 2022–23 wage-employed workers in India, of which only 0.3 percent is attributable to measured differences in education, experience, and location between male and female workers. Nearly the entire gap reflects different wages for similarly qualified men and women, a finding best interpreted alongside the well-known fact of low female labour force participation, which likely produces a positively selected sample of working women. Returns to schooling are high, at approximately 10.3 percent per year. Wage inequality overall is moderate-to-high (Gini = 0.427), and the large majority of that inequality occurs within rather than between gender groups.

Priority extensions for future work include: a Heckman selection-corrected wage equation incorporating a labour force participation model; richer occupational and industry controls; a robustness check with wage top-coding; and replication using the complete official PLFS national file to validate estimates against MoSPI's published indicators. These extensions would strengthen the causal interpretability of the findings and are the natural next phase of this research programme.

---

## References

Atkinson, A. B. (1970). On the measurement of inequality. *Journal of Economic Theory, 2*(3), 244–263.

Blinder, A. S. (1973). Wage discrimination: Reduced form and structural estimates. *Journal of Human Resources, 8*(4), 436–455.

Heckman, J. J. (1979). Sample selection bias as a specification error. *Econometrica, 47*(1), 153–161.

International Labour Organization. (2018). *Women and men in the informal economy: A statistical picture* (3rd ed.). International Labour Office.

International Labour Organization. (2019). *Global wage report 2018/19: What lies behind gender pay gaps.* International Labour Office.

Mincer, J. (1974). *Schooling, experience, and earnings.* National Bureau of Economic Research.

Ministry of Statistics and Programme Implementation. (2024). *Periodic Labour Force Survey (PLFS) annual report, 2022–23.* Government of India. https://mospi.gov.in

National Commission for Enterprises in the Unorganised Sector. (2009). *The challenge of employment in India: An informal economy perspective.* Government of India.

Oaxaca, R. (1973). Male-female wage differentials in urban labor markets. *International Economic Review, 14*(3), 693–709.

Theil, H. (1967). *Economics and information theory.* North-Holland.

---

*Full reproducible code and data documentation at: github.com/rupalrani/labour-market-intelligence*
