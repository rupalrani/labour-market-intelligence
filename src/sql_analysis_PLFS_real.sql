-- ============================================================
-- Labour Market Intelligence — SQL Analysis (REAL PLFS DATA)
-- Author : Rupal Rani | TISS Mumbai
-- Data   : PLFS 2022-23 microdata, cleaned analytic table
--          (41,913 employed wage workers; see
--           data_dictionary_PLFS_real.md for column definitions)
-- Usage  : Load the cleaned analytic extract into a table named
--          `plfs_wages` with the columns below, then run in order.
--          PostgreSQL syntax; SQLite notes included where needed.
-- ============================================================


-- ── 0. Table shape ───────────────────────────────────────────────────────────
-- CREATE TABLE IF NOT EXISTS plfs_wages (
--     sex          TEXT,     -- 'Male' / 'Female'
--     grp          TEXT,     -- 'Gen' / 'OBC' / 'SC' / 'ST'
--     education    REAL,     -- years of schooling
--     age          INTEGER,
--     experience   REAL,
--     wage         REAL,     -- monthly earnings, Rs.
--     log_wage     REAL,
--     weight       REAL,     -- survey multiplier
--     urban        INTEGER,  -- 1 = urban, 0 = rural
--     state        TEXT,
--     quarter      TEXT      -- 'Q5'..'Q8' (Jul 2022 - Jun 2023)
-- );

SELECT
    COUNT(*)                     AS total_records,
    COUNT(DISTINCT sex)          AS n_sex_values,
    COUNT(DISTINCT grp)          AS n_groups,
    COUNT(DISTINCT state)        AS n_states,
    ROUND(SUM(weight))           AS total_weighted_population
FROM plfs_wages;


-- ── 1. Headline Wage Statistics (survey-weighted) ───────────────────────────

-- 1A. Overall and by-sex mean wage
SELECT
    sex,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS weighted_mean_wage,
    COUNT(*)                                              AS sample_n
FROM plfs_wages
GROUP BY sex
ORDER BY weighted_mean_wage DESC;


-- 1B. Raw gender wage gap (arithmetic, survey-weighted)
SELECT
    ROUND(
        100.0 * (
            (SELECT SUM(wage*weight)/SUM(weight) FROM plfs_wages WHERE sex='Male')
          - (SELECT SUM(wage*weight)/SUM(weight) FROM plfs_wages WHERE sex='Female')
        ) / (SELECT SUM(wage*weight)/SUM(weight) FROM plfs_wages WHERE sex='Male'),
    1) AS gender_wage_gap_pct;


-- 1C. Mean wage by social group
SELECT
    grp,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS weighted_mean_wage,
    ROUND(AVG(wage), 0)                                   AS unweighted_mean_wage,
    COUNT(*)                                              AS sample_n
FROM plfs_wages
GROUP BY grp
ORDER BY weighted_mean_wage DESC;


-- 1D. Mean wage by social group AND sex (intersectional — Table 1 in the report)
SELECT
    grp,
    sex,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS weighted_mean_wage,
    COUNT(*)                                              AS sample_n
FROM plfs_wages
GROUP BY grp, sex
ORDER BY grp,
         CASE sex WHEN 'Male' THEN 1 ELSE 2 END;


-- ── 2. Education and Wage ───────────────────────────────────────────────────

SELECT
    CASE
        WHEN education BETWEEN 0  AND 5  THEN '0-5 (Primary)'
        WHEN education BETWEEN 6  AND 8  THEN '6-8 (Middle)'
        WHEN education BETWEEN 9  AND 10 THEN '9-10 (Secondary)'
        WHEN education BETWEEN 11 AND 12 THEN '11-12 (H.Sec)'
        WHEN education BETWEEN 13 AND 15 THEN '13-15 (UG)'
        WHEN education >= 16             THEN '16+ (PG)'
    END AS education_band,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_wages
GROUP BY education_band
ORDER BY MIN(education);


-- ── 3. Gender Gap Heterogeneity by Social Group ─────────────────────────────
-- (Reproduces Figure 8, panel A)

WITH group_sex_wage AS (
    SELECT
        grp,
        sex,
        SUM(wage * weight) / NULLIF(SUM(weight),0) AS mean_wage
    FROM plfs_wages
    GROUP BY grp, sex
)
SELECT
    m.grp,
    ROUND(m.mean_wage, 0) AS male_mean_wage,
    ROUND(f.mean_wage, 0) AS female_mean_wage,
    ROUND(100.0 * (m.mean_wage - f.mean_wage) / m.mean_wage, 1) AS gender_gap_pct
FROM group_sex_wage m
JOIN group_sex_wage f ON m.grp = f.grp AND f.sex = 'Female'
WHERE m.sex = 'Male'
ORDER BY gender_gap_pct DESC;


-- ── 4. State-Level Analysis ──────────────────────────────────────────────────

SELECT
    state,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_wages
GROUP BY state
HAVING COUNT(*) >= 200            -- exclude states with thin samples
ORDER BY weighted_mean_wage DESC;


-- ── 5. Urban / Rural Wage Premium ───────────────────────────────────────────

SELECT
    CASE urban WHEN 1 THEN 'Urban' ELSE 'Rural' END AS location,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_wages
GROUP BY urban
ORDER BY weighted_mean_wage DESC;


-- ── 6. Quarter-over-Quarter Wage Trend (seasonality check) ──────────────────

SELECT
    quarter,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_wages
GROUP BY quarter
ORDER BY quarter;
-- Quarters map to: Q5 = Jul-Sep 2022, Q6 = Oct-Dec 2022,
--                  Q7 = Jan-Mar 2023, Q8 = Apr-Jun 2023


-- ── 7. Data Quality Checks ──────────────────────────────────────────────────

-- 7A. Missing value audit
SELECT
    SUM(CASE WHEN sex        IS NULL THEN 1 ELSE 0 END) AS null_sex,
    SUM(CASE WHEN wage       IS NULL THEN 1 ELSE 0 END) AS null_wage,
    SUM(CASE WHEN education  IS NULL THEN 1 ELSE 0 END) AS null_education,
    SUM(CASE WHEN weight     IS NULL THEN 1 ELSE 0 END) AS null_weight,
    COUNT(*) AS total_rows
FROM plfs_wages;

-- 7B. Wage distribution sanity check (PostgreSQL/BigQuery percentile syntax)
SELECT
    MIN(wage) AS min_wage,
    PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY wage) AS p10,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY wage) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY wage) AS median_wage,
    ROUND(AVG(wage), 0)   AS mean_wage,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY wage) AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY wage) AS p90,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY wage) AS p99,
    MAX(wage) AS max_wage
FROM plfs_wages;
-- SQLite: use Python pandas .quantile() instead of PERCENTILE_CONT.


-- ── 8. Window Functions — Wage Percentile Rank by Group ─────────────────────

SELECT
    sex,
    grp,
    wage,
    ROUND(
        100.0 * RANK() OVER (PARTITION BY grp ORDER BY wage)
               / COUNT(*) OVER (PARTITION BY grp),
    1) AS wage_pctile_in_group
FROM plfs_wages
ORDER BY grp, wage DESC
LIMIT 30;


-- 8B. State wage rank
SELECT
    state,
    ROUND(SUM(wage * weight) / NULLIF(SUM(weight),0), 0) AS mean_wage,
    RANK() OVER (
        ORDER BY SUM(wage * weight) / NULLIF(SUM(weight),0) DESC
    ) AS wage_rank
FROM plfs_wages
GROUP BY state
HAVING COUNT(*) >= 200
ORDER BY wage_rank;


-- ============================================================
-- END OF SCRIPT — REAL PLFS 2022-23 DATA
-- Author: Rupal Rani | TISS Mumbai
-- See data_dictionary_PLFS_real.md for full column documentation
-- and known caveats (working extract, urban-skewed sample, etc.)
-- ============================================================
