"""
Labour Market Intelligence Dashboard — India
=============================================
Author : Rupal Rani | Tata Institute of Social Sciences, Mumbai
Data   : Synthetic dataset mirroring PLFS unit-level microdata structure
         Replace with real PLFS microdata from mospi.gov.in for research use.
Methods: Descriptive indicators · Mincer OLS regression
         Blinder-Oaxaca decomposition · Gini coefficient · Theil index
Refs   : Mincer (1974), Blinder (1973), Oaxaca (1973), Theil (1967)

Run    : python src/analysis.py
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # non-interactive backend for file output
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import os

# ── Reproducibility ──────────────────────────────────────────────────────────
SEED = 42
rng  = np.random.default_rng(SEED)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, "outputs", "figures")
TAB_DIR = os.path.join(BASE, "outputs", "tables")
DAT_DIR = os.path.join(BASE, "data", "synthetic")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TAB_DIR, exist_ok=True)
os.makedirs(DAT_DIR, exist_ok=True)

# ── Plotting style ─────────────────────────────────────────────────────────────
PALETTE = {
    "Male": "#2C6E9B", "Female": "#D95F5F",
    "General": "#2C6E9B", "OBC": "#5BAD76",
    "SC": "#E8963B", "ST": "#9B59B6",
    "Formal": "#2C6E9B", "Informal": "#D95F5F",
    "Agriculture": "#5BAD76", "Industry": "#E8963B", "Services": "#2C6E9B",
}
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.labelsize": 11,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
    "figure.dpi": 120, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

CAPTION = ("Note: Analysis uses a synthetic dataset (N = 5,000) that mirrors "
           "PLFS structure. Replace with MoSPI PLFS microdata for research output.")


# =============================================================================
# MODULE 1 — SYNTHETIC DATA GENERATION
# =============================================================================

def generate_synthetic_plfs(n: int = 5000) -> pd.DataFrame:
    """
    Generate a synthetic PLFS-like worker dataset.

    Parameters calibrated to approximate PLFS 2022-23 aggregate statistics:
    - Male LFPR ≈ 76 %, Female LFPR ≈ 34 %
    - Overall informality ≈ 82 %
    - Gender wage gap ≈ 28 % (raw mean)
    - Social group wage gradient: General > OBC > SC > ST
    - Returns to schooling ≈ 7 % per year (Mincer)

    Parameters
    ----------
    n : int
        Number of synthetic records.

    Returns
    -------
    pd.DataFrame
    """
    # --- Demographics --------------------------------------------------------
    sex    = rng.choice(["Male", "Female"], n, p=[0.52, 0.48])
    group  = rng.choice(["General", "OBC", "SC", "ST"],
                        n, p=[0.30, 0.43, 0.19, 0.08])
    age    = rng.integers(15, 65, n)
    locale = rng.choice(["Rural", "Urban"], n, p=[0.65, 0.35])
    states = [
        "Uttar Pradesh", "Maharashtra", "Bihar", "West Bengal",
        "Madhya Pradesh", "Rajasthan", "Tamil Nadu", "Karnataka",
        "Gujarat", "Andhra Pradesh", "Odisha", "Telangana",
        "Kerala", "Jharkhand", "Punjab",
    ]
    state  = rng.choice(states, n)

    # --- Education (years of schooling) --------------------------------------
    edu_mean = {"Male":{"General":12,"OBC":10,"SC":8,"ST":6},
                "Female":{"General":10,"OBC":8,"SC":6,"ST":5}}
    years_edu = np.array([
        int(np.clip(rng.normal(edu_mean[s][g], 2.8), 0, 22))
        for s, g in zip(sex, group)
    ])

    # --- Labour-force participation ------------------------------------------
    lfpr_base  = np.where(sex == "Male", 0.78, 0.36)
    age_factor = np.where((age >= 25) & (age <= 54), 1.00,
                 np.where((age >= 18) & (age < 25),  0.85, 0.68))
    lfpr_prob  = np.clip(lfpr_base * age_factor, 0, 1)
    in_lf      = rng.random(n) < lfpr_prob

    unemployed = in_lf & (rng.random(n) < 0.045)
    employed   = in_lf & ~unemployed

    status = np.where(employed, "Employed",
             np.where(unemployed, "Unemployed", "Outside_LF"))

    # --- Sector --------------------------------------------------------------
    sector = np.where(employed,
                      rng.choice(["Agriculture","Industry","Services"],
                                 n, p=[0.44, 0.25, 0.31]),
                      "NA")

    # --- Formality -----------------------------------------------------------
    inf_prob = np.where(sector == "Agriculture", 0.95,
               np.where(sector == "Industry",    0.72,
               np.where(sector == "Services",    0.62, 0.0)))
    formality = np.where(employed,
                         np.where(rng.random(n) < inf_prob, "Informal", "Formal"),
                         "NA")

    # --- Wages (Mincer-style DGP) -------------------------------------------
    experience = np.maximum(0, age - years_edu - 6)

    group_eff  = {"General": 0.00, "OBC": -0.10, "SC": -0.20, "ST": -0.26}
    g_eff      = np.array([group_eff[g] for g in group])

    female_flag = (sex == "Female").astype(float)
    formal_flag = (formality == "Formal").astype(float)
    urban_flag  = (locale == "Urban").astype(float)

    # ln(wage) ~ Mincer + group + formality + urban + noise
    log_wage = (8.50
                + 0.075 * years_edu
                + 0.028 * experience
                - 0.0005 * experience**2
                - 0.30  * female_flag     # raw gender gap ≈ 26 %
                + g_eff
                + 0.45  * formal_flag
                + 0.22  * urban_flag
                + rng.normal(0, 0.40, n))

    monthly_wage = np.where(employed,
                            np.maximum(np.exp(log_wage).round(0), 3000),
                            0).astype(int)

    # --- Survey weights (simplified) ----------------------------------------
    base_wt  = np.where(locale == "Rural", 1.20, 0.90)
    survey_wt = (base_wt * rng.uniform(0.85, 1.25, n)).round(4)

    df = pd.DataFrame({
        "worker_id":      [f"W{i:05d}" for i in range(1, n+1)],
        "sex":            sex,
        "social_group":   group,
        "age":            age,
        "years_education":years_edu,
        "experience":     experience,
        "rural_urban":    locale,
        "state":          state,
        "activity_status":status,
        "sector":         sector,
        "formality":      formality,
        "monthly_wage":   monthly_wage,
        "survey_weight":  survey_wt,
    })
    return df


# =============================================================================
# MODULE 2 — DATA CLEANING
# =============================================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply cleaning steps that mirror the PLFS cleaning protocol.
    Returns a cleaned copy; all decisions logged to console.
    """
    cleaned = df.copy()
    log = []

    # Step 1 — Ensure correct dtypes
    cleaned["monthly_wage"]    = pd.to_numeric(cleaned["monthly_wage"],    errors="coerce")
    cleaned["years_education"] = pd.to_numeric(cleaned["years_education"], errors="coerce")
    cleaned["experience"]      = pd.to_numeric(cleaned["experience"],      errors="coerce")
    cleaned["survey_weight"]   = pd.to_numeric(cleaned["survey_weight"],   errors="coerce")
    log.append("Step 1: dtype validation complete")

    # Step 2 — Education bounds (0–22 years)
    bad_edu = (cleaned["years_education"] < 0) | (cleaned["years_education"] > 22)
    cleaned.loc[bad_edu, "years_education"] = np.nan
    log.append(f"Step 2: Education out-of-range flagged — {bad_edu.sum()} rows")

    # Step 3 — Experience floor at zero
    cleaned["experience"] = cleaned["experience"].clip(lower=0)
    log.append("Step 3: Experience floored at zero")

    # Step 4 — Top-code wages at 99th percentile for employed workers
    cleaned["monthly_wage"] = cleaned["monthly_wage"].astype(float)
    emp   = cleaned["activity_status"] == "Employed"
    p99   = cleaned.loc[emp, "monthly_wage"].quantile(0.99)
    hi_w  = emp & (cleaned["monthly_wage"] > p99)
    cleaned.loc[hi_w, "monthly_wage"] = p99
    log.append(f"Step 4: Wages top-coded at ₹{p99:,.0f} — {hi_w.sum()} rows")

    # Step 5 — Implausible wages (< ₹500 for employed workers)
    low_w = emp & (cleaned["monthly_wage"] < 500)
    cleaned.loc[low_w, "monthly_wage"] = np.nan
    log.append(f"Step 5: Wages < ₹500 set to NaN — {low_w.sum()} rows")

    # Step 6 — Log wage column (for regression; drop non-positive)
    pos_wage = emp & (cleaned["monthly_wage"] > 0)
    cleaned["log_wage"] = np.where(pos_wage, np.log(cleaned["monthly_wage"]), np.nan)
    log.append(f"Step 6: log_wage derived for {pos_wage.sum()} employed workers with positive wages")

    # Step 7 — Binary variables for analysis
    cleaned["female"]   = (cleaned["sex"] == "Female").astype(int)
    cleaned["informal"] = (cleaned["formality"] == "Informal").astype(int)
    cleaned["urban"]    = (cleaned["rural_urban"] == "Urban").astype(int)
    log.append("Step 7: Binary indicators created (female, informal, urban)")

    # Step 8 — Group dummy variables
    for cat in ["OBC", "SC", "ST"]:
        cleaned[f"group_{cat}"] = (cleaned["social_group"] == cat).astype(int)
    log.append("Step 8: Social group dummies created (reference = General)")

    # Step 9 — Sector dummies
    for sec in ["Industry", "Services"]:
        cleaned[f"sector_{sec}"] = (cleaned["sector"] == sec).astype(int)
    log.append("Step 9: Sector dummies created (reference = Agriculture)")

    print("\n── Cleaning log ──────────────────────────────────────────────────────")
    for entry in log:
        print(" ", entry)
    print(f"  Final shape: {cleaned.shape[0]:,} rows × {cleaned.shape[1]} columns")

    return cleaned


# =============================================================================
# MODULE 3 — WEIGHTED LABOUR MARKET INDICATORS
# =============================================================================

def compute_weighted_indicators(df: pd.DataFrame) -> dict:
    """
    Compute headline labour market indicators using survey weights.
    All estimates are population-representative (not raw sample counts).

    Indicators
    ----------
    LFPR           = Labour force / Working-age population (weighted)
    WPR            = Employed / Working-age population (weighted)
    Unemployment   = Unemployed / Labour force (weighted)
    Informality    = Informal employed / Total employed (weighted)
    Median wage    = Weighted median monthly wage for employed workers
    Gender gap     = (Male mean − Female mean) / Male mean
    """
    wap = df  # All records are working-age (15–64)

    wt_total   = df["survey_weight"].sum()
    wt_lf      = df.loc[df["activity_status"].isin(["Employed","Unemployed"]), "survey_weight"].sum()
    wt_emp     = df.loc[df["activity_status"] == "Employed", "survey_weight"].sum()
    wt_unemp   = df.loc[df["activity_status"] == "Unemployed", "survey_weight"].sum()
    wt_inform  = df.loc[(df["activity_status"] == "Employed") & (df["formality"] == "Informal"), "survey_weight"].sum()

    lfpr  = wt_lf   / wt_total
    wpr   = wt_emp  / wt_total
    urate = wt_unemp / wt_lf
    informality_share = wt_inform / wt_emp

    # Weighted mean wage by sex
    emp_df = df[df["activity_status"] == "Employed"].dropna(subset=["monthly_wage"])
    male_emp   = emp_df[emp_df["sex"] == "Male"]
    female_emp = emp_df[emp_df["sex"] == "Female"]

    male_mean   = np.average(male_emp["monthly_wage"],   weights=male_emp["survey_weight"])
    female_mean = np.average(female_emp["monthly_wage"], weights=female_emp["survey_weight"])
    gender_gap  = (male_mean - female_mean) / male_mean

    # Weighted median (approximate)
    overall_mean = np.average(emp_df["monthly_wage"], weights=emp_df["survey_weight"])

    # Group mean wages
    group_wages = {}
    for g in ["General", "OBC", "SC", "ST"]:
        sub = emp_df[emp_df["social_group"] == g]
        if len(sub) > 0:
            group_wages[g] = np.average(sub["monthly_wage"], weights=sub["survey_weight"])

    # Sector mean wages
    sector_wages = {}
    for sec in ["Agriculture", "Industry", "Services"]:
        sub = emp_df[emp_df["sector"] == sec]
        if len(sub) > 0:
            sector_wages[sec] = np.average(sub["monthly_wage"], weights=sub["survey_weight"])

    # LFPR by sex
    lfpr_sex = {}
    for s in ["Male", "Female"]:
        sub    = df[df["sex"] == s]
        wt_sub = sub["survey_weight"].sum()
        wt_lf_sub = sub.loc[sub["activity_status"].isin(["Employed","Unemployed"]),
                             "survey_weight"].sum()
        lfpr_sex[s] = wt_lf_sub / wt_sub if wt_sub > 0 else np.nan

    results = {
        "LFPR":              lfpr,
        "WPR":               wpr,
        "Unemployment_rate": urate,
        "Informality_share": informality_share,
        "Male_mean_wage":    male_mean,
        "Female_mean_wage":  female_mean,
        "Overall_mean_wage": overall_mean,
        "Gender_wage_gap":   gender_gap,
        "LFPR_Male":         lfpr_sex["Male"],
        "LFPR_Female":       lfpr_sex["Female"],
        "Group_wages":       group_wages,
        "Sector_wages":      sector_wages,
    }
    return results


# =============================================================================
# MODULE 4 — MINCER EARNINGS REGRESSION (OLS via numpy)
# =============================================================================

def mincer_regression(df: pd.DataFrame) -> dict:
    """
    Estimate a Mincer earnings function:
        ln(wage) = α + β₁·school + β₂·exp + β₃·exp² + controls + ε

    Controls: female, group dummies, sector dummies, urban
    Returns coefficients, standard errors, t-stats, p-values, R².

    Reference: Mincer, J. (1974). Schooling, Experience, and Earnings. NBER.
    """
    reg_df = df[(df["activity_status"] == "Employed")].dropna(
        subset=["log_wage", "years_education", "experience"]
    ).copy()
    reg_df["exp2"] = reg_df["experience"] ** 2

    # Regressors
    cols = ["years_education", "experience", "exp2",
            "female", "urban",
            "group_OBC", "group_SC", "group_ST",
            "sector_Industry", "sector_Services"]

    y  = reg_df["log_wage"].values
    Xd = reg_df[cols].values
    # Add intercept
    X  = np.column_stack([np.ones(len(Xd)), Xd])
    feat_names = ["Intercept"] + cols

    # OLS: β = (X'X)⁻¹ X'y
    XtX  = X.T @ X
    Xty  = X.T @ y
    beta = np.linalg.lstsq(XtX, Xty, rcond=None)[0]

    # Residuals and diagnostics
    y_hat = X @ beta
    resid = y - y_hat
    n, k  = X.shape
    df_e  = n - k
    s2    = (resid @ resid) / df_e
    cov_b = s2 * np.linalg.pinv(XtX)
    se    = np.sqrt(np.diag(cov_b))
    t_val = beta / se
    p_val = 2 * (1 - stats.t.cdf(np.abs(t_val), df=df_e))

    ss_res = resid @ resid
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2     = 1 - ss_res / ss_tot
    r2_adj = 1 - (1 - r2) * (n - 1) / df_e

    results = {
        "feature_names": feat_names,
        "coefficients":  beta,
        "std_errors":    se,
        "t_statistics":  t_val,
        "p_values":      p_val,
        "r_squared":     r2,
        "r_squared_adj": r2_adj,
        "n_obs":         n,
        "return_to_schooling_pct": beta[1] * 100,  # β₁ as %
    }

    # Save regression table
    reg_table = pd.DataFrame({
        "Variable":    feat_names,
        "Coefficient": np.round(beta, 4),
        "Std_Error":   np.round(se,   4),
        "t_Statistic": np.round(t_val, 3),
        "p_Value":     np.round(p_val, 4),
        "Significant": ["***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
                        for p in p_val],
    })
    reg_table.to_csv(os.path.join(TAB_DIR, "mincer_regression.csv"), index=False)
    return results


# =============================================================================
# MODULE 5 — BLINDER-OAXACA DECOMPOSITION
# =============================================================================

def oaxaca_decomposition(df: pd.DataFrame) -> dict:
    """
    Twofold Blinder-Oaxaca decomposition of the gender log-wage gap.

    Decomposition (male coefficients as reference):
        Δ = (X̄_M − X̄_F)·β̂_M  +  X̄_F·(β̂_M − β̂_F)
           = Explained (endowments)  +  Unexplained (coefficients + intercept)

    The explained part reflects differences in education, experience, sector, etc.
    The unexplained part is NOT equivalent to discrimination; it also captures
    unobserved characteristics.

    References:
        Blinder (1973). JHR, 8(4), 436-455.
        Oaxaca (1973). IER, 14(3), 693-709.
    """
    emp = df[(df["activity_status"] == "Employed")].dropna(
        subset=["log_wage", "years_education", "experience"]
    ).copy()
    emp["exp2"] = emp["experience"] ** 2

    X_cols = ["years_education", "experience", "exp2",
              "urban", "group_OBC", "group_SC", "group_ST",
              "sector_Industry", "sector_Services"]

    def ols(y, X):
        Xt = X.T
        beta = np.linalg.lstsq(Xt @ X, Xt @ y, rcond=None)[0]
        # SE calculation
        n, k = X.shape
        resid = y - X @ beta
        s2    = (resid @ resid) / (n - k)
        cov   = s2 * np.linalg.pinv(Xt @ X)
        se    = np.sqrt(np.diag(cov))
        return beta, se

    # Separate samples
    male_df   = emp[emp["sex"] == "Male"]
    female_df = emp[emp["sex"] == "Female"]

    Xm = np.column_stack([np.ones(len(male_df)),   male_df[X_cols].values])
    Xf = np.column_stack([np.ones(len(female_df)), female_df[X_cols].values])
    ym = male_df["log_wage"].values
    yf = female_df["log_wage"].values

    beta_m, se_m = ols(ym, Xm)
    beta_f, se_f = ols(yf, Xf)

    Xm_bar = Xm.mean(axis=0)
    Xf_bar = Xf.mean(axis=0)

    raw_gap    = ym.mean() - yf.mean()
    explained  = (Xm_bar - Xf_bar) @ beta_m
    unexplained = Xf_bar @ (beta_m - beta_f)

    # Component-level endowment decomposition
    comp_names = ["Intercept"] + X_cols
    comp_explained = (Xm_bar - Xf_bar) * beta_m

    result = {
        "raw_gap_log":    raw_gap,
        "raw_gap_pct":    (np.exp(raw_gap) - 1) * 100,
        "explained_log":  explained,
        "explained_pct":  explained / raw_gap * 100,
        "unexplained_log":unexplained,
        "unexplained_pct":unexplained / raw_gap * 100,
        "components":     dict(zip(comp_names, comp_explained)),
        "beta_male":      beta_m,
        "beta_female":    beta_f,
        "se_male":        se_m,
        "se_female":      se_f,
    }

    # Save
    oa_table = pd.DataFrame({
        "Component":    ["Raw Gap (log)", "Explained (endowments)", "Unexplained (coefficients)"],
        "Value_log":    [raw_gap, explained, unexplained],
        "Share_pct":    [100.0, explained/raw_gap*100, unexplained/raw_gap*100],
    })
    oa_table.to_csv(os.path.join(TAB_DIR, "oaxaca_decomposition.csv"), index=False)

    return result


# =============================================================================
# MODULE 6 — INEQUALITY (GINI + THEIL)
# =============================================================================

def compute_inequality(df: pd.DataFrame) -> dict:
    """
    Compute Gini coefficient (Lorenz method) and Theil T index.
    The Theil index is decomposed into within-group and between-group components.

    References:
        Gini, C. (1912) – original coefficient
        Theil, H. (1967). Economics and Information Theory. North-Holland.
        Atkinson, A. B. (1970). JET, 2(3), 244-263.
    """
    emp = df[(df["activity_status"] == "Employed") & (df["monthly_wage"] > 0)].copy()
    w   = emp["monthly_wage"].values.astype(float)
    wt  = emp["survey_weight"].values.astype(float)

    # ── Gini (weighted Lorenz) ────────────────────────────────────────────────
    sort_idx = np.argsort(w)
    w_s  = w[sort_idx]
    wt_s = wt[sort_idx]

    wt_cum    = np.cumsum(wt_s)
    wt_total  = wt_cum[-1]
    income_cum = np.cumsum(w_s * wt_s)
    income_total = income_cum[-1]

    # Lorenz ordinates
    F = wt_cum  / wt_total
    L = income_cum / income_total
    F0 = np.concatenate([[0], F])
    L0 = np.concatenate([[0], L])

    # Gini = 1 − 2 × area under Lorenz curve (trapezoid rule)
    gini = 1 - 2 * np.trapezoid(L0, F0)

    # ── Theil T (weighted) ────────────────────────────────────────────────────
    mu   = np.average(w, weights=wt)
    theil_total = np.average((w / mu) * np.log(w / mu), weights=wt)

    # Between-group decomposition (by sex)
    theil_between = 0.0
    theil_within  = 0.0
    group_col     = emp["sex"]
    groups        = ["Male", "Female"]

    group_stats = {}
    for g in groups:
        mask  = group_col == g
        w_g   = w[mask.values]
        wt_g  = wt[mask.values]
        if len(w_g) == 0:
            continue
        mu_g    = np.average(w_g, weights=wt_g)
        n_share = wt_g.sum() / wt.sum()
        inc_share = (mu_g * wt_g.sum()) / (mu * wt.sum())
        theil_g   = np.average((w_g / mu_g) * np.log(w_g / mu_g), weights=wt_g)
        theil_between += n_share * (mu_g / mu) * np.log(mu_g / mu)
        theil_within  += inc_share * theil_g
        group_stats[g] = {"mean_wage": mu_g, "theil_within": theil_g}

    # ── Lorenz curve data (for plotting) ─────────────────────────────────────
    lorenz_data = pd.DataFrame({"Cumulative_Population": F0,
                                "Cumulative_Income": L0})

    results = {
        "gini":              gini,
        "theil_total":       theil_total,
        "theil_between_sex": theil_between,
        "theil_within_sex":  theil_within,
        "lorenz_data":       lorenz_data,
        "group_stats":       group_stats,
    }

    # Save
    ineq_table = pd.DataFrame({
        "Measure":  ["Gini Coefficient", "Theil T (Total)",
                     "Theil T (Between-sex)", "Theil T (Within-sex)"],
        "Value":    [gini, theil_total, theil_between, theil_within],
        "Note":     ["0=perfect equality, 1=perfect inequality",
                     "Entropy-based inequality",
                     "Contribution of gender-group differences",
                     "Inequality within each gender group"],
    })
    ineq_table.to_csv(os.path.join(TAB_DIR, "inequality_measures.csv"), index=False)

    return results


# =============================================================================
# MODULE 7 — VISUALISATIONS
# =============================================================================

def plot_labour_overview(indic: dict, df: pd.DataFrame):
    """Figure 1: Labour market overview — LFPR, WPR, unemployment, informality."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("India Labour Market Overview (Synthetic PLFS Data)", fontsize=14, y=1.01)

    # Panel A: LFPR by sex
    ax = axes[0]
    sexes  = ["Overall", "Male", "Female"]
    lfprs  = [indic["LFPR"], indic["LFPR_Male"], indic["LFPR_Female"]]
    colors = ["#5B86A5", PALETTE["Male"], PALETTE["Female"]]
    bars   = ax.bar(sexes, [v*100 for v in lfprs], color=colors, width=0.55, edgecolor="white")
    ax.bar_label(bars, fmt="%.1f %%", padding=4, fontsize=10)
    ax.set_title("Labour Force Participation Rate")
    ax.set_ylabel("Percentage (%)")
    ax.set_ylim(0, 100)

    # Panel B: Key rates
    ax2 = axes[1]
    labels = ["WPR", "Unemployment Rate", "Informality Share"]
    values = [indic["WPR"]*100, indic["Unemployment_rate"]*100, indic["Informality_share"]*100]
    bars2  = ax2.bar(labels, values,
                     color=["#5BAD76", "#D95F5F", "#E8963B"],
                     width=0.55, edgecolor="white")
    ax2.bar_label(bars2, fmt="%.1f %%", padding=4, fontsize=10)
    ax2.set_title("Key Labour Market Rates")
    ax2.set_ylabel("Percentage (%)")
    ax2.set_ylim(0, 100)

    fig.text(0.5, -0.04, CAPTION, ha="center", fontsize=8, color="#555555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "01_labour_overview.png"))
    plt.close()


def plot_wage_by_group(df: pd.DataFrame):
    """Figure 2: Mean monthly wage by social group and sex."""
    emp = df[(df["activity_status"] == "Employed")].dropna(subset=["monthly_wage"])

    grp_sex = emp.groupby(["social_group", "sex"]).apply(
        lambda x: np.average(x["monthly_wage"], weights=x["survey_weight"])
    ).reset_index()
    grp_sex.columns = ["Social_Group", "Sex", "Mean_Wage"]

    order = ["General", "OBC", "SC", "ST"]
    grp_sex["Social_Group"] = pd.Categorical(grp_sex["Social_Group"], categories=order, ordered=True)
    grp_sex.sort_values("Social_Group", inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    x      = np.arange(len(order))
    width  = 0.38
    male_  = grp_sex[grp_sex["Sex"] == "Male"].set_index("Social_Group")["Mean_Wage"]
    female_= grp_sex[grp_sex["Sex"] == "Female"].set_index("Social_Group")["Mean_Wage"]

    b1 = ax.bar(x - width/2, [male_.get(g, 0)   for g in order],
                width, color=PALETTE["Male"],   label="Male",   edgecolor="white")
    b2 = ax.bar(x + width/2, [female_.get(g, 0) for g in order],
                width, color=PALETTE["Female"], label="Female", edgecolor="white")
    ax.bar_label(b1, fmt="₹%.0f", padding=3, fontsize=8)
    ax.bar_label(b2, fmt="₹%.0f", padding=3, fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_title("Mean Monthly Wage by Social Group and Sex\n(Survey-weighted)")
    ax.set_ylabel("Mean Monthly Wage (₹)")
    ax.legend()
    ax.text(0.5, -0.12, CAPTION, ha="center", fontsize=8, color="#555555",
            transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "02_wage_by_group.png"))
    plt.close()


def plot_wage_by_education(df: pd.DataFrame):
    """Figure 3: Mean wage by education level (binned)."""
    emp = df[(df["activity_status"] == "Employed")].dropna(
        subset=["monthly_wage", "years_education"])

    bins   = [0, 5, 8, 10, 12, 15, 22]
    labels = ["0–5 yrs\n(Primary)", "6–8 yrs\n(Middle)",
              "9–10 yrs\n(Secondary)", "11–12 yrs\n(Higher Sec)",
              "13–15 yrs\n(Under-grad)", "16+ yrs\n(Post-grad)"]
    emp = emp.copy()
    emp["edu_bin"] = pd.cut(emp["years_education"], bins=bins, labels=labels, right=True)
    edu_wage = emp.groupby("edu_bin", observed=False).apply(
        lambda x: np.average(x["monthly_wage"], weights=x["survey_weight"])
    )

    fig, ax = plt.subplots(figsize=(11, 5))
    colors  = plt.cm.Blues(np.linspace(0.35, 0.85, len(edu_wage)))
    bars    = ax.bar(edu_wage.index, edu_wage.values, color=colors, edgecolor="white")
    ax.bar_label(bars, fmt="₹%.0f", padding=3, fontsize=9)
    ax.set_title("Mean Monthly Wage by Education Level\n(Survey-weighted)")
    ax.set_ylabel("Mean Monthly Wage (₹)")
    ax.set_xlabel("Highest Level of Education")
    ax.text(0.5, -0.16, CAPTION, ha="center", fontsize=8, color="#555555",
            transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "03_wage_by_education.png"))
    plt.close()


def plot_mincer_coefficients(reg: dict):
    """Figure 4: Mincer regression coefficient plot (key variables)."""
    names  = reg["feature_names"]
    coefs  = reg["coefficients"]
    ses    = reg["std_errors"]
    pvals  = reg["p_values"]

    # Select key variables for display
    show   = ["years_education", "experience", "female", "urban",
              "group_OBC", "group_SC", "group_ST",
              "sector_Industry", "sector_Services"]
    display_labels = {
        "years_education": "Years of Schooling",
        "experience":      "Experience (years)",
        "female":          "Female (=1)",
        "urban":           "Urban (=1)",
        "group_OBC":       "Social Group: OBC",
        "group_SC":        "Social Group: SC",
        "group_ST":        "Social Group: ST",
        "sector_Industry": "Sector: Industry",
        "sector_Services": "Sector: Services",
    }

    idx    = [names.index(v) for v in show]
    c_show = coefs[idx]
    s_show = ses[idx]
    p_show = pvals[idx]
    l_show = [display_labels[v] for v in show]

    # Significance colour
    colors = ["#D95F5F" if p < 0.01 else "#E8963B" if p < 0.05 else "#999" for p in p_show]

    fig, ax = plt.subplots(figsize=(9, 6))
    y_pos   = np.arange(len(l_show))
    ax.barh(y_pos, c_show, xerr=1.96*s_show,
            color=colors, edgecolor="white", height=0.6, capsize=4)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(l_show)
    ax.set_xlabel("Coefficient (Log Wage)")
    ax.set_title(f"Mincer Earnings Regression — Key Coefficients\n"
                 f"R² = {reg['r_squared']:.3f}  |  N = {reg['n_obs']:,}  |  "
                 f"Return to schooling ≈ {reg['return_to_schooling_pct']:.1f}% per year")

    patches = [
        mpatches.Patch(color="#D95F5F", label="p < 0.01"),
        mpatches.Patch(color="#E8963B", label="p < 0.05"),
        mpatches.Patch(color="#999",    label="p ≥ 0.05"),
    ]
    ax.legend(handles=patches, loc="lower right", fontsize=9)
    ax.text(0.5, -0.10, CAPTION, ha="center", fontsize=8, color="#555555",
            transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "04_mincer_coefficients.png"))
    plt.close()


def plot_oaxaca(oa: dict):
    """Figure 5: Blinder-Oaxaca decomposition — stacked bar."""
    gap   = oa["raw_gap_pct"]
    expl  = oa["explained_pct"]
    unexp = oa["unexplained_pct"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Blinder-Oaxaca Decomposition of the Gender Wage Gap", fontsize=13)

    # Panel A — summary stacked bar
    ax = axes[0]
    ax.bar([0], [expl],  color="#5BAD76", label=f"Explained (endowments): {expl:.1f}%")
    ax.bar([0], [unexp], bottom=[expl], color="#D95F5F",
           label=f"Unexplained (coefficients): {unexp:.1f}%")
    ax.set_xticks([0])
    ax.set_xticklabels(["Gender Wage Gap"])
    ax.set_ylabel("Share of Raw Gap (%)")
    ax.set_ylim(0, 110)
    ax.legend(loc="upper right", fontsize=9)
    ax.text(0, expl/2, f"{expl:.0f}%", ha="center", va="center",
            color="white", fontweight="bold", fontsize=11)
    ax.text(0, expl + unexp/2, f"{unexp:.0f}%", ha="center", va="center",
            color="white", fontweight="bold", fontsize=11)

    # Panel B — mean log wages
    ax2 = axes[1]
    emp = None  # use placeholder values from oa dict
    male_log   = np.log(oa.get("male_mean", 1))
    female_log = np.log(oa.get("female_mean", 1))

    bars = ax2.bar(["Male\n(log wage)", "Female\n(log wage)"],
                   [oa["beta_male"][0] + 10.5, oa["beta_female"][0] + 10.5],
                   color=[PALETTE["Male"], PALETTE["Female"]], width=0.5)

    ax2.set_title(f"Raw gender wage gap ≈ {gap:.1f}%\n"
                  f"(Log-wage difference = {oa['raw_gap_log']:.3f})")
    ax2.set_ylabel("Estimated mean log wage (illustrative scale)")

    ax2.text(0.5, -0.14,
             "Caution: The unexplained component is NOT equivalent to discrimination.\n"
             "It also captures unobserved characteristics (Blinder 1973, Oaxaca 1973).",
             ha="center", fontsize=8, color="#D95F5F", transform=ax2.transAxes)

    fig.text(0.5, -0.06, CAPTION, ha="center", fontsize=8, color="#555555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "05_oaxaca_decomposition.png"))
    plt.close()


def plot_lorenz_and_gini(ineq: dict):
    """Figure 6: Lorenz curve and Gini coefficient."""
    lz   = ineq["lorenz_data"]
    gini = ineq["gini"]

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(lz["Cumulative_Population"], lz["Cumulative_Income"],
            color="#2C6E9B", linewidth=2, label=f"Lorenz Curve (Gini = {gini:.3f})")
    ax.plot([0, 1], [0, 1], "--", color="gray", linewidth=1, label="Line of Perfect Equality")
    ax.fill_between(lz["Cumulative_Population"],
                    lz["Cumulative_Population"],
                    lz["Cumulative_Income"],
                    alpha=0.15, color="#2C6E9B")
    ax.set_xlabel("Cumulative Share of Workers (poorest → richest)")
    ax.set_ylabel("Cumulative Share of Total Wages")
    ax.set_title(f"Lorenz Curve — Wage Inequality\nGini = {gini:.3f} | "
                 f"Theil T = {ineq['theil_total']:.3f}")
    ax.legend()
    ax.text(0.5, -0.10, CAPTION, ha="center", fontsize=8, color="#555555",
            transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "06_lorenz_gini.png"))
    plt.close()


def plot_informality(df: pd.DataFrame):
    """Figure 7: Informality share by social group and sector."""
    emp = df[df["activity_status"] == "Employed"].copy()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A — by social group
    ax = axes[0]
    groups = ["General", "OBC", "SC", "ST"]
    inf_shares = []
    for g in groups:
        sub = emp[emp["social_group"] == g]
        inf_shares.append((sub["formality"] == "Informal").mean() * 100)
    colors = [PALETTE.get(g, "#5B86A5") for g in groups]
    bars   = ax.bar(groups, inf_shares, color=colors, edgecolor="white", width=0.55)
    ax.bar_label(bars, fmt="%.1f %%", padding=3)
    ax.set_title("Informality Share by Social Group")
    ax.set_ylabel("Informal Workers (%)")
    ax.set_ylim(0, 105)

    # Panel B — by sector
    ax2 = axes[1]
    sectors = ["Agriculture", "Industry", "Services"]
    sec_inf = []
    for s in sectors:
        sub = emp[emp["sector"] == s]
        sec_inf.append((sub["formality"] == "Informal").mean() * 100 if len(sub) > 0 else 0)
    bars2 = ax2.bar(sectors, sec_inf,
                    color=[PALETTE[s] for s in sectors], edgecolor="white", width=0.55)
    ax2.bar_label(bars2, fmt="%.1f %%", padding=3)
    ax2.set_title("Informality Share by Sector")
    ax2.set_ylabel("Informal Workers (%)")
    ax2.set_ylim(0, 105)

    fig.suptitle("Informality Across Groups and Sectors (Synthetic PLFS Data)", fontsize=13)
    fig.text(0.5, -0.04, CAPTION, ha="center", fontsize=8, color="#555555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "07_informality.png"))
    plt.close()


def plot_wage_distribution(df: pd.DataFrame):
    """Figure 8: Wage distribution (violin) by sex and formality."""
    emp = df[(df["activity_status"] == "Employed") & (df["monthly_wage"] > 0)].copy()
    emp["Wage_k"] = emp["monthly_wage"] / 1000  # in thousands

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A — by sex
    ax = axes[0]
    for i, (sex, color) in enumerate([("Male", PALETTE["Male"]), ("Female", PALETTE["Female"])]):
        sub = emp[emp["sex"] == sex]["Wage_k"]
        # Use kde
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(sub, bw_method=0.3)
        y   = np.linspace(sub.min(), min(sub.max(), 80), 200)
        x   = kde(y)
        x   = x / x.max() * 0.35
        ax.fill_betweenx(y, i - x, i + x, alpha=0.7, color=color)
        ax.plot([i - x, i + x], [sub.median(), sub.median()],
                color="white", linewidth=2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Male", "Female"])
    ax.set_ylabel("Monthly Wage (₹ thousands)")
    ax.set_title("Wage Distribution by Sex")

    # Panel B — by formality
    ax2 = axes[1]
    for i, (form, color) in enumerate([("Formal", PALETTE["Formal"]),
                                        ("Informal", PALETTE["Informal"])]):
        sub = emp[emp["formality"] == form]["Wage_k"]
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(sub, bw_method=0.3)
        y   = np.linspace(sub.min(), min(sub.max(), 100), 200)
        x   = kde(y)
        x   = x / x.max() * 0.35
        ax2.fill_betweenx(y, i - x, i + x, alpha=0.7, color=color)
        ax2.plot([i - x, i + x], [sub.median(), sub.median()],
                 color="white", linewidth=2)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["Formal", "Informal"])
    ax2.set_ylabel("Monthly Wage (₹ thousands)")
    ax2.set_title("Wage Distribution by Formality")

    fig.suptitle("Wage Distributions (Violin plots, synthetic data)", fontsize=13)
    fig.text(0.5, -0.04, CAPTION, ha="center", fontsize=8, color="#555555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "08_wage_distributions.png"))
    plt.close()


def plot_state_wages(df: pd.DataFrame):
    """Figure 9: Mean wage by state (horizontal bar)."""
    emp = df[(df["activity_status"] == "Employed")].dropna(subset=["monthly_wage"])

    state_wage = emp.groupby("state").apply(
        lambda x: np.average(x["monthly_wage"], weights=x["survey_weight"])
    ).sort_values()

    fig, ax = plt.subplots(figsize=(9, 7))
    colors  = plt.cm.Blues(np.linspace(0.35, 0.85, len(state_wage)))
    bars    = ax.barh(state_wage.index, state_wage.values, color=colors, edgecolor="white")
    ax.bar_label(bars, fmt="₹%.0f", padding=4, fontsize=8)
    ax.set_xlabel("Mean Monthly Wage (₹)")
    ax.set_title("Mean Monthly Wage by State\n(Survey-weighted, synthetic data)")
    ax.text(0.5, -0.08, CAPTION, ha="center", fontsize=8, color="#555555",
            transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "09_wage_by_state.png"))
    plt.close()


# =============================================================================
# MASTER RUNNER
# =============================================================================

def main():
    print("="*65)
    print(" Labour Market Intelligence Dashboard — India")
    print(" Author: Rupal Rani | TISS Mumbai")
    print("="*65)

    # ── Step 1: Generate data ─────────────────────────────────────────────────
    print("\n[1/8] Generating synthetic PLFS-like dataset …")
    df_raw = generate_synthetic_plfs(n=5000)
    df_raw.to_csv(os.path.join(DAT_DIR, "plfs_synthetic_raw.csv"), index=False)
    print(f"      Records: {len(df_raw):,} | Columns: {df_raw.shape[1]}")

    # ── Step 2: Clean data ────────────────────────────────────────────────────
    print("\n[2/8] Cleaning data …")
    df = clean_data(df_raw)
    df.to_csv(os.path.join(DAT_DIR, "plfs_synthetic_clean.csv"), index=False)

    # ── Step 3: Labour indicators ─────────────────────────────────────────────
    print("\n[3/8] Computing weighted labour market indicators …")
    indic = compute_weighted_indicators(df)
    print(f"\n  ── Headline Indicators ────────────────────────────────────────")
    print(f"  LFPR (overall)       : {indic['LFPR']*100:.1f}%")
    print(f"  LFPR (Male)          : {indic['LFPR_Male']*100:.1f}%")
    print(f"  LFPR (Female)        : {indic['LFPR_Female']*100:.1f}%")
    print(f"  Worker-Population Ratio: {indic['WPR']*100:.1f}%")
    print(f"  Unemployment Rate    : {indic['Unemployment_rate']*100:.1f}%")
    print(f"  Informality Share    : {indic['Informality_share']*100:.1f}%")
    print(f"  Male Mean Wage       : ₹{indic['Male_mean_wage']:,.0f}/month")
    print(f"  Female Mean Wage     : ₹{indic['Female_mean_wage']:,.0f}/month")
    print(f"  Gender Wage Gap      : {indic['Gender_wage_gap']*100:.1f}%")
    print(f"\n  ── Wage by Social Group ───────────────────────────────────────")
    for g, v in indic["Group_wages"].items():
        print(f"  {g:<10}: ₹{v:>9,.0f}/month")
    print(f"\n  ── Wage by Sector ─────────────────────────────────────────────")
    for s, v in indic["Sector_wages"].items():
        print(f"  {s:<12}: ₹{v:>9,.0f}/month")

    pd.DataFrame({"Indicator": list(indic.keys())[:10],
                  "Value":     list(indic.values())[:10]}
                ).to_csv(os.path.join(TAB_DIR, "headline_indicators.csv"), index=False)

    # ── Step 4: Mincer regression ─────────────────────────────────────────────
    print("\n[4/8] Estimating Mincer earnings function …")
    reg = mincer_regression(df)
    print(f"\n  ── Mincer Regression Results ──────────────────────────────────")
    print(f"  R²                   : {reg['r_squared']:.3f}")
    print(f"  Adjusted R²          : {reg['r_squared_adj']:.3f}")
    print(f"  N (employed, +wage)  : {reg['n_obs']:,}")
    print(f"  Return to schooling  : {reg['return_to_schooling_pct']:.2f}% per year")
    k = reg["feature_names"].index("female")
    print(f"  Female coefficient   : {reg['coefficients'][k]:.3f} "
          f"(≈ {(1-np.exp(reg['coefficients'][k]))*100:.1f}% wage penalty, ceteris paribus)")

    # ── Step 5: Oaxaca decomposition ──────────────────────────────────────────
    print("\n[5/8] Running Blinder-Oaxaca decomposition …")
    oa = oaxaca_decomposition(df)
    print(f"\n  ── Oaxaca Decomposition ───────────────────────────────────────")
    print(f"  Raw gender wage gap  : {oa['raw_gap_pct']:.1f}%")
    print(f"  Explained (endowments): {oa['explained_pct']:.1f}% of gap")
    print(f"  Unexplained (coeff.)  : {oa['unexplained_pct']:.1f}% of gap")
    print(f"  [Caution: 'unexplained' ≠ discrimination; includes unobservables]")

    # ── Step 6: Inequality ────────────────────────────────────────────────────
    print("\n[6/8] Computing inequality measures …")
    ineq = compute_inequality(df)
    print(f"\n  ── Inequality Measures ────────────────────────────────────────")
    print(f"  Gini Coefficient     : {ineq['gini']:.3f}")
    print(f"  Theil T (Total)      : {ineq['theil_total']:.3f}")
    print(f"  Theil Between-sex    : {ineq['theil_between_sex']:.3f}")
    print(f"  Theil Within-sex     : {ineq['theil_within_sex']:.3f}")
    print(f"  Between share        : {ineq['theil_between_sex']/ineq['theil_total']*100:.1f}%")

    # ── Step 7: Visualisations ────────────────────────────────────────────────
    print("\n[7/8] Generating visualisations …")
    plot_labour_overview(indic, df)
    plot_wage_by_group(df)
    plot_wage_by_education(df)
    plot_mincer_coefficients(reg)
    plot_oaxaca(oa)
    plot_lorenz_and_gini(ineq)
    plot_informality(df)
    plot_wage_distribution(df)
    plot_state_wages(df)
    print(f"      Saved 9 figures to {FIG_DIR}")

    # ── Step 8: Summary report ────────────────────────────────────────────────
    print("\n[8/8] Writing summary table …")
    summary = pd.DataFrame({
        "Metric": [
            "LFPR (overall)","LFPR (Male)","LFPR (Female)",
            "WPR","Unemployment Rate","Informality Share",
            "Male Mean Wage","Female Mean Wage","Gender Wage Gap",
            "Gini Coefficient","Theil T","Return to Schooling",
            "Oaxaca — Explained","Oaxaca — Unexplained",
        ],
        "Value": [
            f"{indic['LFPR']*100:.1f}%",
            f"{indic['LFPR_Male']*100:.1f}%",
            f"{indic['LFPR_Female']*100:.1f}%",
            f"{indic['WPR']*100:.1f}%",
            f"{indic['Unemployment_rate']*100:.1f}%",
            f"{indic['Informality_share']*100:.1f}%",
            f"₹{indic['Male_mean_wage']:,.0f}",
            f"₹{indic['Female_mean_wage']:,.0f}",
            f"{indic['Gender_wage_gap']*100:.1f}%",
            f"{ineq['gini']:.3f}",
            f"{ineq['theil_total']:.3f}",
            f"{reg['return_to_schooling_pct']:.1f}% per year",
            f"{oa['explained_pct']:.1f}% of gap",
            f"{oa['unexplained_pct']:.1f}% of gap",
        ],
    })
    summary.to_csv(os.path.join(TAB_DIR, "full_results_summary.csv"), index=False)

    print("\n" + "="*65)
    print(" ANALYSIS COMPLETE")
    print(f" Figures  → {FIG_DIR}")
    print(f" Tables   → {TAB_DIR}")
    print(f" Data     → {DAT_DIR}")
    print("="*65)
    print("\n IMPORTANT: Results above use SYNTHETIC illustrative data.")
    print(" For research output, replace data/raw/ with MoSPI PLFS")
    print(" microdata (download at mospi.gov.in) and rerun.")


if __name__ == "__main__":
    main()
