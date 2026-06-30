# Data Dictionary — Labour Market Intelligence Dashboard

**Source:** Periodic Labour Force Survey (PLFS), MoSPI, Government of India  
**Demo data:** Synthetic dataset mirroring PLFS 2022–23 structure  
**Author:** Rupal Rani | TISS Mumbai

---

## Variable Definitions

| Variable | Type | Values / Units | Description |
|----------|------|---------------|-------------|
| `worker_id` | String | W00001 – W05000 | Unique record identifier |
| `sex` | Categorical | Male, Female | Sex of respondent |
| `social_group` | Categorical | General, OBC, SC, ST | Social category |
| `age` | Integer | 15–64 (years) | Age in completed years |
| `years_education` | Integer | 0–22 (years) | Total years of formal schooling |
| `experience` | Integer | ≥ 0 (years) | Potential work experience: age − education − 6 |
| `rural_urban` | Categorical | Rural, Urban | Type of area of residence |
| `state` | Categorical | 15 Indian states | State of residence |
| `activity_status` | Categorical | Employed, Unemployed, Outside_LF | Labour force status (usual principal) |
| `sector` | Categorical | Agriculture, Industry, Services, NA | Industry of employment (NA if not employed) |
| `formality` | Categorical | Formal, Informal, NA | Formality of employment (NA if not employed) |
| `monthly_wage` | Float | ₹ (Indian rupees) | Monthly earnings; 0 for non-employed |
| `survey_weight` | Float | > 0 | Survey multiplier for population estimates |

---

## Derived Variables (Created During Cleaning)

| Variable | Formula | Description |
|----------|---------|-------------|
| `log_wage` | ln(monthly_wage) | Natural log of wage; NaN for non-employed or zero wages |
| `female` | 1 if sex == Female, else 0 | Binary sex indicator for regression |
| `informal` | 1 if formality == Informal, else 0 | Binary informality indicator |
| `urban` | 1 if rural_urban == Urban, else 0 | Binary location indicator |
| `group_OBC` | 1 if social_group == OBC, else 0 | OBC dummy (ref = General) |
| `group_SC` | 1 if social_group == SC, else 0 | SC dummy (ref = General) |
| `group_ST` | 1 if social_group == ST, else 0 | ST dummy (ref = General) |
| `sector_Industry` | 1 if sector == Industry, else 0 | Industry dummy (ref = Agriculture) |
| `sector_Services` | 1 if sector == Services, else 0 | Services dummy (ref = Agriculture) |

---

## Activity Status Codes (PLFS Reference)

| PLFS Code | Category Used Here | Description |
|-----------|-------------------|-------------|
| 11–51 (Usual) | Employed | Working or employed (principal + subsidiary) |
| 81 | Unemployed | Seeking or available for work |
| 91–99 | Outside_LF | Not in the labour force |

---

## Education Mapping (PLFS to Years)

| PLFS Education Code | Years Assigned | Level |
|---------------------|---------------|-------|
| Not literate | 0 | None |
| Literate but below primary | 2 | Informal literacy |
| Primary (up to Class V) | 5 | Primary |
| Middle (Class VI–VIII) | 8 | Middle |
| Secondary (Class IX–X) | 10 | Secondary |
| Higher Secondary (Class XI–XII) | 12 | Higher Secondary |
| Diploma/Certificate | 13 | Vocational |
| Graduate | 15 | Under-graduate |
| Post-graduate and above | 17 | Post-graduate |

---

## Formality Classification

A worker is classified as **Formal** if they are in an enterprise that is:
- Registered or licensed, OR
- Employs six or more workers, OR
- Reports provident fund, ESIC, or NPS contributions

All other employed workers are classified as **Informal**, consistent with ILO (2018) definitions.

---

## Survey Weight Guidance

> **Always use survey weights for population estimates.**  
> Unweighted estimates from PLFS are sample proportions, not population proportions, and will be biased if the sample design overrepresents certain groups.

Formula for weighted mean:  
`weighted_mean = Σ(value × weight) / Σ(weight)`

Formula for weighted count:  
`weighted_count = Σ(weight for matching rows)`

---

## Sources

- Ministry of Statistics and Programme Implementation. (2024). *PLFS Annual Report.* Government of India. [mospi.gov.in](https://mospi.gov.in)
- International Labour Organization. (2018). *Women and men in the informal economy* (3rd ed.). ILO.
