-- ============================================================
-- Labour Market Intelligence — SQL Analysis Script
-- Author : Rupal Rani | TISS Mumbai
-- Data   : PLFS-structure table loaded into a SQL database
--          (PostgreSQL / SQLite syntax; minor adjustments for
--           MySQL or BigQuery noted in comments)
-- Usage  : Load plfs_synthetic_clean.csv into a table named
--          `plfs_workers`, then run queries in sequence.
-- ============================================================


-- ── 0. Setup: Create and inspect the table ──────────────────────────────────

-- PostgreSQL: use COPY; SQLite: use .import or sqlite3 Python API
-- CREATE TABLE IF NOT EXISTS plfs_workers (
--     worker_id       TEXT,
--     sex             TEXT,
--     social_group    TEXT,
--     age             INTEGER,
--     years_education INTEGER,
--     experience      INTEGER,
--     rural_urban     TEXT,
--     state           TEXT,
--     activity_status TEXT,
--     sector          TEXT,
--     formality       TEXT,
--     monthly_wage    REAL,
--     survey_weight   REAL,
--     female          INTEGER,
--     informal        INTEGER,
--     urban           INTEGER
-- );

-- Quick record count and column check
SELECT
    COUNT(*)          AS total_records,
    COUNT(DISTINCT sex)           AS n_sex_values,
    COUNT(DISTINCT social_group)  AS n_groups,
    COUNT(DISTINCT state)         AS n_states,
    COUNT(DISTINCT activity_status) AS n_status_values
FROM plfs_workers;


-- ── 1. Weighted Labour Force Indicators ─────────────────────────────────────
-- NOTE: Survey weights are essential for PLFS. All counts use SUM(survey_weight).

-- 1A. Overall LFPR, WPR, and unemployment rate
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN activity_status IN ('Employed','Unemployed') THEN survey_weight ELSE 0 END)
               / SUM(survey_weight), 1
    ) AS lfpr_pct,

    ROUND(
        100.0 * SUM(CASE WHEN activity_status = 'Employed' THEN survey_weight ELSE 0 END)
               / SUM(survey_weight), 1
    ) AS wpr_pct,

    ROUND(
        100.0 * SUM(CASE WHEN activity_status = 'Unemployed' THEN survey_weight ELSE 0 END)
               / NULLIF(SUM(CASE WHEN activity_status IN ('Employed','Unemployed') THEN survey_weight ELSE 0 END), 0),
    1) AS unemployment_rate_pct

FROM plfs_workers;


-- 1B. LFPR by sex
SELECT
    sex,
    ROUND(
        100.0 * SUM(CASE WHEN activity_status IN ('Employed','Unemployed') THEN survey_weight ELSE 0 END)
               / SUM(survey_weight), 1
    ) AS lfpr_pct,
    ROUND(SUM(survey_weight), 0) AS weighted_pop
FROM plfs_workers
GROUP BY sex
ORDER BY sex;


-- 1C. Informality share (among employed)
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN formality = 'Informal' THEN survey_weight ELSE 0 END)
               / NULLIF(SUM(survey_weight), 0), 1
    ) AS informality_share_pct
FROM plfs_workers
WHERE activity_status = 'Employed';


-- ── 2. Wage Analysis by Group ────────────────────────────────────────────────

-- 2A. Weighted mean wage by sex (employed workers only)
SELECT
    sex,
    ROUND(
        SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0), 0
    ) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
GROUP BY sex
ORDER BY weighted_mean_wage DESC;


-- 2B. Raw gender wage gap
SELECT
    ROUND(
        100.0 * (
            SUM(CASE WHEN sex = 'Male'   THEN monthly_wage * survey_weight ELSE 0 END) /
            NULLIF(SUM(CASE WHEN sex = 'Male' THEN survey_weight ELSE 0 END), 0)
          -
            SUM(CASE WHEN sex = 'Female' THEN monthly_wage * survey_weight ELSE 0 END) /
            NULLIF(SUM(CASE WHEN sex = 'Female' THEN survey_weight ELSE 0 END), 0)
        )
        /
        NULLIF(
            SUM(CASE WHEN sex = 'Male' THEN monthly_wage * survey_weight ELSE 0 END) /
            NULLIF(SUM(CASE WHEN sex = 'Male' THEN survey_weight ELSE 0 END), 0),
        0),
    1) AS gender_wage_gap_pct
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0;


-- 2C. Mean wage by social group
SELECT
    social_group,
    ROUND(
        SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0), 0
    ) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
GROUP BY social_group
ORDER BY weighted_mean_wage DESC;


-- 2D. Mean wage by social group AND sex (intersectional)
SELECT
    social_group,
    sex,
    ROUND(
        SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0), 0
    ) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
GROUP BY social_group, sex
ORDER BY social_group, sex;


-- 2E. Mean wage by sector
SELECT
    sector,
    ROUND(
        SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0), 0
    ) AS weighted_mean_wage,
    ROUND(
        100.0 * SUM(CASE WHEN formality = 'Informal' THEN survey_weight ELSE 0 END)
               / NULLIF(SUM(survey_weight), 0), 1
    ) AS informality_pct,
    COUNT(*) AS sample_n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
  AND sector <> 'NA'
GROUP BY sector
ORDER BY weighted_mean_wage DESC;


-- 2F. Formal vs. informal wage premium
SELECT
    formality,
    ROUND(
        SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0), 0
    ) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
  AND formality <> 'NA'
GROUP BY formality
ORDER BY weighted_mean_wage DESC;


-- ── 3. Education and Wage ────────────────────────────────────────────────────

-- 3A. Mean wage by education bracket
SELECT
    CASE
        WHEN years_education BETWEEN 0  AND 5  THEN '0–5 yrs (Primary)'
        WHEN years_education BETWEEN 6  AND 8  THEN '6–8 yrs (Middle)'
        WHEN years_education BETWEEN 9  AND 10 THEN '9–10 yrs (Secondary)'
        WHEN years_education BETWEEN 11 AND 12 THEN '11–12 yrs (Higher Sec)'
        WHEN years_education BETWEEN 13 AND 15 THEN '13–15 yrs (UG)'
        WHEN years_education >= 16             THEN '16+ yrs (PG)'
        ELSE 'Unknown'
    END AS education_level,
    ROUND(
        SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0), 0
    ) AS weighted_mean_wage,
    COUNT(*) AS sample_n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
  AND years_education IS NOT NULL
GROUP BY education_level
ORDER BY MIN(years_education);


-- ── 4. State-Level Analysis ──────────────────────────────────────────────────

-- 4A. Key indicators by state, ranked by mean wage
SELECT
    state,
    ROUND(
        100.0 * SUM(CASE WHEN activity_status IN ('Employed','Unemployed') THEN survey_weight ELSE 0 END)
               / SUM(survey_weight), 1
    ) AS lfpr_pct,
    ROUND(
        SUM(CASE WHEN activity_status = 'Employed' THEN monthly_wage * survey_weight ELSE 0 END)
        / NULLIF(SUM(CASE WHEN activity_status = 'Employed' AND monthly_wage > 0 THEN survey_weight ELSE 0 END), 0),
    0) AS mean_wage,
    ROUND(
        100.0 * SUM(CASE WHEN formality = 'Informal' AND activity_status = 'Employed' THEN survey_weight ELSE 0 END)
               / NULLIF(SUM(CASE WHEN activity_status = 'Employed' THEN survey_weight ELSE 0 END), 0),
    1) AS informality_pct,
    COUNT(*) AS sample_n
FROM plfs_workers
GROUP BY state
ORDER BY mean_wage DESC;


-- ── 5. Cross-Tabulation Pivot (PostgreSQL syntax) ────────────────────────────
-- Mean wage by social group × formality status

SELECT
    social_group,
    ROUND(AVG(CASE WHEN formality = 'Formal'   THEN monthly_wage END), 0) AS mean_wage_formal,
    ROUND(AVG(CASE WHEN formality = 'Informal' THEN monthly_wage END), 0) AS mean_wage_informal,
    COUNT(*) AS n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
  AND formality <> 'NA'
GROUP BY social_group
ORDER BY mean_wage_formal DESC;


-- ── 6. Data Quality Checks ──────────────────────────────────────────────────

-- 6A. Missing value audit
SELECT
    SUM(CASE WHEN worker_id       IS NULL THEN 1 ELSE 0 END) AS null_worker_id,
    SUM(CASE WHEN sex             IS NULL THEN 1 ELSE 0 END) AS null_sex,
    SUM(CASE WHEN monthly_wage    IS NULL THEN 1 ELSE 0 END) AS null_wage,
    SUM(CASE WHEN years_education IS NULL THEN 1 ELSE 0 END) AS null_education,
    SUM(CASE WHEN survey_weight   IS NULL THEN 1 ELSE 0 END) AS null_weight,
    COUNT(*) AS total_rows
FROM plfs_workers;


-- 6B. Wage distribution sanity check (employed only)
SELECT
    MIN(monthly_wage)                             AS min_wage,
    PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY monthly_wage) AS p10,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_wage) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY monthly_wage) AS median_wage,
    ROUND(AVG(monthly_wage), 0)                   AS mean_wage,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_wage) AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY monthly_wage) AS p90,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY monthly_wage) AS p99,
    MAX(monthly_wage)                             AS max_wage,
    COUNT(*)                                      AS n
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0;
-- NOTE: PERCENTILE_CONT is PostgreSQL/BigQuery syntax.
-- SQLite equivalent: use Python pandas .quantile() instead.


-- 6C. Activity status distribution
SELECT
    activity_status,
    COUNT(*)                            AS raw_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS raw_pct,
    ROUND(SUM(survey_weight), 0)        AS weighted_count,
    ROUND(100.0 * SUM(survey_weight) / SUM(SUM(survey_weight)) OVER (), 1) AS weighted_pct
FROM plfs_workers
GROUP BY activity_status
ORDER BY weighted_count DESC;


-- ── 7. Window Functions — Wage Rank by Group ────────────────────────────────

-- 7A. Wage percentile rank within each social group
SELECT
    worker_id,
    sex,
    social_group,
    monthly_wage,
    ROUND(
        100.0 * RANK() OVER (PARTITION BY social_group ORDER BY monthly_wage)
               / COUNT(*) OVER (PARTITION BY social_group),
    1) AS wage_pctile_in_group
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
ORDER BY social_group, monthly_wage DESC
LIMIT 30;


-- 7B. State wage rank
SELECT
    state,
    ROUND(
        SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0), 0
    ) AS mean_wage,
    RANK() OVER (
        ORDER BY SUM(monthly_wage * survey_weight) / NULLIF(SUM(survey_weight), 0) DESC
    ) AS wage_rank
FROM plfs_workers
WHERE activity_status = 'Employed'
  AND monthly_wage > 0
GROUP BY state
ORDER BY wage_rank;


-- ============================================================
-- END OF SCRIPT
-- Author: Rupal Rani | TISS Mumbai
-- All queries run against plfs_workers table.
-- Replace synthetic data with real PLFS microdata for research.
-- ============================================================
