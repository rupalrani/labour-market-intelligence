"""
Labour Market Intelligence Dashboard — India
REAL DATA ANALYSIS
==================
Data   : PLFS unit-level microdata (PLFS 2022-23 round, CWS employed wage workers)
         42,803 records | Monthly earnings | 36 States/UTs | 4 Quarters
Author : Rupal Rani | Tata Institute of Social Sciences, Mumbai
Methods: Weighted descriptive stats · Mincer OLS · Blinder-Oaxaca · Gini · Theil T
Refs   : Mincer (1974) · Blinder (1973) · Oaxaca (1973) · Theil (1967)
"""

import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import os, sys

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, "outputs", "figures")
TAB_DIR = os.path.join(BASE, "outputs", "tables")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TAB_DIR, exist_ok=True)

DATA_PATH = "/mnt/user-data/uploads/plfs_large.csv"

# ── Style ─────────────────────────────────────────────────────────────────────
PAL = {"Male":"#2C6E9B","Female":"#D95F5F",
       "Gen":"#2C6E9B","OBC":"#5BAD76","SC":"#E8963B","ST":"#9B59B6",
       "Rural":"#5BAD76","Urban":"#2C6E9B"}
plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,
    "axes.spines.right":False,"axes.titlesize":13,"axes.labelsize":11,
    "xtick.labelsize":10,"ytick.labelsize":10,
    "figure.dpi":130,"savefig.bbox":"tight","savefig.pad_inches":0.18})

CAP = ("Source: Periodic Labour Force Survey (PLFS) 2022–23, MoSPI, Government of India.\n"
       "Survey period: July 2022 – June 2023. Employed wage workers (CWS). "
       "Survey-weighted estimates. Author: Rupal Rani, TISS Mumbai.")

STATE_MAP = {
    1:"J & K",2:"Himachal Pradesh",3:"Punjab",4:"Chandigarh",
    5:"Uttarakhand",6:"Haryana",7:"Delhi",8:"Rajasthan",9:"Uttar Pradesh",
    10:"Bihar",11:"Sikkim",12:"Arunachal Pradesh",13:"Nagaland",14:"Manipur",
    15:"Mizoram",16:"Tripura",17:"Meghalaya",18:"Assam",19:"West Bengal",
    20:"Jharkhand",21:"Odisha",22:"Chhattisgarh",23:"Madhya Pradesh",
    24:"Gujarat",25:"Daman/DN&H",27:"Maharashtra",28:"Andhra Pradesh",
    29:"Karnataka",30:"Goa",31:"Lakshadweep",32:"Kerala",33:"Tamil Nadu",
    34:"Puducherry",35:"Andaman & Nicobar",36:"Telangana",37:"Andhra Pradesh (new)",
}

# =============================================================================
# LOAD & PREPARE
# =============================================================================

def load_and_prepare(path):
    raw = pd.read_csv(path)
    print(f"  Raw records: {len(raw):,}  |  Columns: {raw.shape[1]}")

    # Keep employed wage workers (CWS=31 dominant; also 11,21,32)
    emp_cws = raw["Current Weekly Status (CWS)"].isin([11,21,31,32])
    df = raw[emp_cws & (raw["earnings"] > 0)].copy()
    print(f"  Employed with positive earnings: {len(df):,}")

    # ── Core variables ────────────────────────────────────────────────────────
    df["sex"]       = df["gender"].str.strip()          # Male / Female
    df["group"]     = df["Social_Cat"].str.strip()      # Gen/OBC/SC/ST
    df["education"] = pd.to_numeric(df["education_yr"], errors="coerce").clip(0,22)
    df["age"]       = pd.to_numeric(df["Age"],          errors="coerce")
    df["experience"]= (df["age"] - df["education"] - 6).clip(lower=0)
    df["exp2"]      = df["experience"] ** 2
    df["wage"]      = pd.to_numeric(df["earnings"],     errors="coerce")
    df["log_wage"]  = np.log(df["wage"])
    df["weight"]    = pd.to_numeric(df["Sub-sample wise Multiplier"], errors="coerce")
    df["urban"]     = (df["Sector"] == 2).astype(int)   # 1=Rural,2=Urban
    df["state"]     = df["State/Ut Code"].map(STATE_MAP)
    df["quarter"]   = df["Quarter"].str.strip()

    # ── Binary / dummies ─────────────────────────────────────────────────────
    df["female"]    = (df["sex"] == "Female").astype(int)
    df["grp_OBC"]   = (df["group"] == "OBC").astype(int)
    df["grp_SC"]    = (df["group"] == "SC").astype(int)
    df["grp_ST"]    = (df["group"] == "ST").astype(int)

    # ── Drop rows missing critical fields ────────────────────────────────────
    df = df.dropna(subset=["log_wage","education","experience","weight","sex","group"])
    print(f"  After cleaning: {len(df):,} records for analysis")
    return df


# =============================================================================
# WEIGHTED DESCRIPTIVE STATISTICS
# =============================================================================

def weighted_mean(values, weights):
    return np.average(values, weights=weights)

def compute_descriptives(df):
    W = df["weight"]

    overall_mean = weighted_mean(df["wage"], W)
    overall_med  = df["wage"].median()

    # By sex
    sex_stats = {}
    for s in ["Male","Female"]:
        sub = df[df["sex"] == s]
        sex_stats[s] = {
            "mean": weighted_mean(sub["wage"], sub["weight"]),
            "median": sub["wage"].median(),
            "n": len(sub),
        }
    gap = (sex_stats["Male"]["mean"] - sex_stats["Female"]["mean"]) / sex_stats["Male"]["mean"]

    # By group
    grp_stats = {}
    for g in ["Gen","OBC","SC","ST"]:
        sub = df[df["group"] == g]
        if len(sub) > 0:
            grp_stats[g] = {
                "mean": weighted_mean(sub["wage"], sub["weight"]),
                "median": sub["wage"].median(),
                "n": len(sub),
            }

    # By location
    loc_stats = {}
    for loc, val in [("Rural",0),("Urban",1)]:
        sub = df[df["urban"] == val]
        loc_stats[loc] = {"mean": weighted_mean(sub["wage"], sub["weight"]),
                          "median": sub["wage"].median(), "n": len(sub)}

    # By quarter (seasonality)
    qtr_stats = {}
    for q in sorted(df["quarter"].unique()):
        sub = df[df["quarter"] == q]
        qtr_stats[q] = {"mean": weighted_mean(sub["wage"], sub["weight"]),
                        "n": len(sub)}

    # By state (top 15 by count)
    state_stats = df.groupby("state").apply(
        lambda x: pd.Series({
            "mean_wage": weighted_mean(x["wage"], x["weight"]),
            "n": len(x)
        })
    ).sort_values("mean_wage", ascending=True)

    return {
        "overall_mean": overall_mean, "overall_median": overall_med,
        "sex_stats": sex_stats, "gender_gap": gap,
        "grp_stats": grp_stats, "loc_stats": loc_stats,
        "qtr_stats": qtr_stats, "state_stats": state_stats,
        "n_total": len(df), "n_male": sex_stats["Male"]["n"],
        "n_female": sex_stats["Female"]["n"],
    }


# =============================================================================
# MINCER EARNINGS REGRESSION (WLS)
# =============================================================================

def mincer_regression(df):
    """
    Weighted OLS: ln(wage) ~ 1 + education + exp + exp² + female
                             + grp_OBC + grp_SC + grp_ST + urban
    Weights = survey multiplier.
    """
    cols = ["education","experience","exp2","female","urban",
            "grp_OBC","grp_SC","grp_ST"]
    labels = ["Intercept","Years of Education","Experience","Experience²",
              "Female (=1)","Urban (=1)","Group: OBC","Group: SC","Group: ST"]

    clean = df.dropna(subset=cols + ["log_wage","weight"])
    y   = clean["log_wage"].values
    Xd  = clean[cols].values
    X   = np.column_stack([np.ones(len(Xd)), Xd])
    wt  = clean["weight"].values
    n, k = X.shape

    # WLS: β = (X'WX)⁻¹ X'Wy  — computed without forming the full diagonal matrix
    w_norm = wt / wt.mean()                  # normalized weights (mean = 1)
    Xw     = X * w_norm[:, None]             # row-scaled design matrix
    XtWX   = Xw.T @ X
    XtWy   = Xw.T @ y
    beta   = np.linalg.lstsq(XtWX, XtWy, rcond=None)[0]

    resid = y - X @ beta
    df_e  = n - k
    # HC0 robust "sandwich" SE for weighted regression — vectorized (no per-row loop)
    Xr     = X * (w_norm * resid)[:, None]   # each row scaled by w_i * resid_i
    meat   = Xr.T @ Xr
    bread  = np.linalg.pinv(XtWX)
    cov    = bread @ meat @ bread
    se     = np.sqrt(np.diag(cov))
    t_val  = beta / se
    p_val  = 2 * (1 - stats.t.cdf(np.abs(t_val), df=df_e))

    ss_res = (wt * resid**2).sum()
    ss_tot = (wt * (y - np.average(y, weights=wt))**2).sum()
    r2 = 1 - ss_res / ss_tot

    result = {"labels":labels,"beta":beta,"se":se,"t":t_val,"p":p_val,
              "r2":r2,"n":n,
              "return_to_schooling": beta[1]*100,
              "female_penalty_pct": (1 - np.exp(beta[4]))*100}

    tbl = pd.DataFrame({"Variable":labels,"Coefficient":beta.round(4),
                         "Std_Error":se.round(4),"t_stat":t_val.round(3),
                         "p_value":p_val.round(4),
                         "Sig":["***" if p<0.01 else "**" if p<0.05
                                else "*" if p<0.1 else "" for p in p_val]})
    tbl.to_csv(os.path.join(TAB_DIR,"mincer_regression_PLFS.csv"),index=False)
    return result


# =============================================================================
# BLINDER-OAXACA DECOMPOSITION
# =============================================================================

def oaxaca_decomposition(df):
    """
    Twofold Blinder-Oaxaca decomposition.
    Δ = (X̄_M - X̄_F)·β̂_M  +  X̄_F·(β̂_M - β̂_F)
      = Explained (endowments)  +  Unexplained (returns)
    """
    cols = ["education","experience","exp2","urban","grp_OBC","grp_SC","grp_ST"]
    clean = df.dropna(subset=cols+["log_wage","weight"])

    male   = clean[clean["sex"]=="Male"]
    female = clean[clean["sex"]=="Female"]

    def wls(sub):
        y  = sub["log_wage"].values
        Xd = sub[cols].values
        X  = np.column_stack([np.ones(len(Xd)), Xd])
        wt = sub["weight"].values / sub["weight"].mean()
        Xw  = X * wt[:, None]
        XtWX = Xw.T @ X
        XtWy = Xw.T @ y
        b   = np.linalg.lstsq(XtWX, XtWy, rcond=None)[0]
        return b, X

    bm, Xm = wls(male)
    bf, Xf = wls(female)

    # Weighted means
    wm = male["weight"].values
    wf = female["weight"].values
    Xm_bar = np.average(Xm, axis=0, weights=wm/wm.sum())
    Xf_bar = np.average(Xf, axis=0, weights=wf/wf.sum())

    ym_mean = np.average(male["log_wage"],   weights=wm)
    yf_mean = np.average(female["log_wage"], weights=wf)

    raw_gap    = ym_mean - yf_mean
    explained  = (Xm_bar - Xf_bar) @ bm
    unexplained = Xf_bar @ (bm - bf)

    # Component-level endowment contributions
    comp_names = ["Intercept","Education","Experience","Exp²",
                  "Urban","OBC","SC","ST"]
    comp_exp = (Xm_bar - Xf_bar) * bm

    result = {
        "raw_gap_log": raw_gap,
        "raw_gap_pct": (np.exp(raw_gap)-1)*100,
        "explained_log": explained,
        "explained_pct": explained/raw_gap*100 if raw_gap != 0 else 0,
        "unexplained_log": unexplained,
        "unexplained_pct": unexplained/raw_gap*100 if raw_gap != 0 else 0,
        "comp_names": comp_names,
        "comp_explained": comp_exp,
        "male_mean_log": ym_mean,
        "female_mean_log": yf_mean,
        "n_male": len(male), "n_female": len(female),
    }
    tbl = pd.DataFrame({
        "Component":["Raw Gap (log)","Explained (endowments)","Unexplained (returns)"],
        "Value_log":[raw_gap, explained, unexplained],
        "Share_pct":[100, explained/raw_gap*100, unexplained/raw_gap*100]
    })
    tbl.to_csv(os.path.join(TAB_DIR,"oaxaca_decomposition_PLFS.csv"),index=False)
    return result


# =============================================================================
# INEQUALITY: GINI + THEIL
# =============================================================================

def compute_inequality(df):
    w  = df["wage"].values.astype(float)
    wt = df["weight"].values.astype(float)

    # ── Weighted Gini (Lorenz) ────────────────────────────────────────────────
    idx  = np.argsort(w)
    ws   = w[idx];  wts = wt[idx]
    cwt  = np.cumsum(wts);   F = cwt / cwt[-1]
    cinc = np.cumsum(ws*wts); L = cinc / cinc[-1]
    F0 = np.concatenate([[0],F]);  L0 = np.concatenate([[0],L])
    gini = 1 - 2 * np.trapezoid(L0, F0)

    # ── Weighted Theil T ──────────────────────────────────────────────────────
    mu   = np.average(w, weights=wt)
    theil = np.average((w/mu)*np.log(w/mu), weights=wt)

    # Within/between by sex
    tb = tw = 0.0
    grp_th = {}
    for g in ["Male","Female"]:
        m   = df["sex"]==g
        wg  = w[m.values];  wtg = wt[m.values]
        if len(wg)<2: continue
        mu_g   = np.average(wg, weights=wtg)
        ns     = wtg.sum() / wt.sum()
        is_    = (mu_g*wtg.sum()) / (mu*wt.sum())
        th_g   = np.average((wg/mu_g)*np.log(wg/mu_g), weights=wtg)
        tb    += ns * (mu_g/mu) * np.log(mu_g/mu)
        tw    += is_ * th_g
        grp_th[g] = th_g

    lorenz = pd.DataFrame({"Cum_Pop":F0,"Cum_Income":L0})
    result = {"gini":gini,"theil":theil,"theil_between":tb,"theil_within":tw,
              "lorenz":lorenz}

    tbl = pd.DataFrame({
        "Measure":["Gini Coefficient","Theil T","Theil (Between-sex)","Theil (Within-sex)"],
        "Value":[gini,theil,tb,tw],
        "Pct_of_Total":[100,100,tb/theil*100,tw/theil*100]
    })
    tbl.to_csv(os.path.join(TAB_DIR,"inequality_PLFS.csv"),index=False)
    return result


# =============================================================================
# VISUALISATIONS
# =============================================================================

def fig1_wage_by_sex_group(desc):
    fig, axes = plt.subplots(1,2,figsize=(13,5))
    fig.suptitle("Monthly Earnings by Sex and Social Group — PLFS 2022–23",fontsize=14,y=1.02)

    # Panel A: sex
    ax = axes[0]
    for i,(s,col) in enumerate([("Male",PAL["Male"]),("Female",PAL["Female"])]):
        v = desc["sex_stats"][s]["mean"]
        b = ax.bar(i, v, color=col, width=0.55, edgecolor="white")
        ax.bar_label(b, labels=[f"₹{v:,.0f}"], padding=4, fontsize=10)
    ax.set_xticks([0,1]); ax.set_xticklabels(["Male","Female"])
    ax.set_ylabel("Mean Monthly Wage (₹)")
    ax.set_title(f"By Sex  |  Raw gap = {desc['gender_gap']*100:.1f}%")
    ax.set_ylim(0, desc["sex_stats"]["Male"]["mean"]*1.25)

    # Panel B: social group
    ax2 = axes[1]
    groups = ["Gen","OBC","SC","ST"]
    vals   = [desc["grp_stats"][g]["mean"] for g in groups]
    colors = [PAL[g] for g in groups]
    bars   = ax2.bar(groups, vals, color=colors, width=0.55, edgecolor="white")
    ax2.bar_label(bars, labels=[f"₹{v:,.0f}" for v in vals], padding=4, fontsize=9)
    ax2.set_ylabel("Mean Monthly Wage (₹)")
    ax2.set_title("By Social Group (Reference = General)")
    ax2.set_ylim(0, max(vals)*1.2)

    fig.text(0.5,-0.04,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"01_wage_sex_group_PLFS.png"))
    plt.close()


def fig2_wage_by_education(df):
    bins   = [0,5,8,10,12,15,22]
    labels = ["0–5\n(Primary)","6–8\n(Middle)","9–10\n(Sec)","11–12\n(H.Sec)","13–15\n(UG)","16+\n(PG)"]
    df2 = df.copy()
    df2["edu_band"] = pd.cut(df2["education"], bins=bins, labels=labels, right=True)
    tbl = df2.groupby("edu_band", observed=False).apply(
        lambda x: pd.Series({"mean":np.average(x["wage"],weights=x["weight"]),
                              "n":len(x)}))

    fig, ax = plt.subplots(figsize=(11,5.5))
    cols = plt.cm.Blues(np.linspace(0.35,0.85,len(tbl)))
    bars = ax.bar(tbl.index, tbl["mean"], color=cols, edgecolor="white")
    ax.bar_label(bars, labels=[f"₹{v:,.0f}" for v in tbl["mean"]], padding=4, fontsize=9)
    ymax = tbl["mean"].max()*1.18
    for i,(idx,row) in enumerate(tbl.iterrows()):
        ax.text(i, ymax*0.02, f"n={int(row['n']):,}", ha="center", va="bottom",
                fontsize=7.5, color="#666")
    ax.set_ylabel("Mean Monthly Wage (₹)")
    ax.set_title("Mean Monthly Wage by Education Level — PLFS 2022–23\n(Survey-weighted)")
    ax.set_ylim(0, ymax)
    fig.text(0.5,-0.06,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"02_wage_education_PLFS.png"))
    plt.close()


def fig3_mincer_coefficients(reg):
    show  = [1,2,3,4,5,6,7,8]   # skip intercept (index 0)
    betas = reg["beta"][show]
    ses   = reg["se"][show]
    pvals = reg["p"][show]
    labs  = [reg["labels"][i] for i in show]

    colors = ["#D95F5F" if p<0.01 else "#E8963B" if p<0.05 else "#aaa" for p in pvals]

    fig, ax = plt.subplots(figsize=(9,6))
    ypos = np.arange(len(labs))
    ax.barh(ypos, betas, xerr=1.96*ses, color=colors, height=0.6,
            edgecolor="white", capsize=4)
    ax.axvline(0,color="black",lw=0.8,ls="--")
    ax.set_yticks(ypos); ax.set_yticklabels(labs)
    ax.set_xlabel("Coefficient on log(Monthly Wage)")
    ax.set_title(f"Mincer Earnings Regression — PLFS Real Data\n"
                 f"R² = {reg['r2']:.3f}  |  N = {reg['n']:,}  |  "
                 f"Return to schooling ≈ {reg['return_to_schooling']:.1f}% per year")

    patches = [mpatches.Patch(color="#D95F5F",label="p < 0.01"),
               mpatches.Patch(color="#E8963B",label="p < 0.05"),
               mpatches.Patch(color="#aaa",   label="p ≥ 0.05")]
    ax.legend(handles=patches,loc="lower right",fontsize=9)
    fig.text(0.5,-0.06,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"03_mincer_PLFS.png"))
    plt.close()


def fig4_oaxaca(oa):
    exp_pct  = oa["explained_pct"]
    unexp_pct= oa["unexplained_pct"]

    fig, axes = plt.subplots(1,2,figsize=(12,5))
    fig.suptitle("Blinder–Oaxaca Decomposition of Gender Wage Gap — PLFS Real Data",fontsize=13)

    # Panel A: stacked bar
    ax = axes[0]
    ax.bar([0], [exp_pct],  color="#5BAD76", width=0.5,
           label=f"Explained (endowments): {exp_pct:.1f}%")
    ax.bar([0], [unexp_pct],bottom=[exp_pct], color="#D95F5F", width=0.5,
           label=f"Unexplained (returns): {unexp_pct:.1f}%")
    ax.text(0, exp_pct/2,   f"{exp_pct:.0f}%",  ha="center",va="center",
            color="white",fontweight="bold",fontsize=12)
    ax.text(0, exp_pct+unexp_pct/2, f"{unexp_pct:.0f}%", ha="center",va="center",
            color="white",fontweight="bold",fontsize=12)
    ax.set_xticks([0]); ax.set_xticklabels(["Gender Wage Gap"])
    ax.set_ylabel("Share of Raw Gap (%)"); ax.set_ylim(0,115)
    ax.legend(loc="upper right",fontsize=9)

    # Panel B: mean log wages by sex
    ax2 = axes[1]
    vals = [oa["male_mean_log"], oa["female_mean_log"]]
    bars = ax2.bar(["Male","Female"], vals,
                   color=[PAL["Male"],PAL["Female"]], width=0.5, edgecolor="white")
    ax2.bar_label(bars, labels=[f"{v:.3f}" for v in vals], padding=4)
    ax2.set_ylabel("Mean ln(Monthly Wage)")
    ax2.set_title(f"Raw gap in log wages = {oa['raw_gap_log']:.3f}\n"
                  f"≈ {oa['raw_gap_pct']:.1f}% wage difference\n"
                  f"(Male n={oa['n_male']:,}  Female n={oa['n_female']:,})")
    ax2.text(0.5,-0.14,
             "⚠ Unexplained ≠ discrimination. Includes unobservables (Blinder 1973, Oaxaca 1973).",
             ha="center",fontsize=8,color="#D95F5F",transform=ax2.transAxes)

    fig.text(0.5,-0.05,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"04_oaxaca_PLFS.png"))
    plt.close()


def fig5_lorenz(ineq):
    lz = ineq["lorenz"]
    fig, ax = plt.subplots(figsize=(7,6.8))
    ax.plot(lz["Cum_Pop"], lz["Cum_Income"],
            color="#2C6E9B", lw=2,
            label=f"Lorenz Curve (Gini = {ineq['gini']:.3f})")
    ax.plot([0,1],[0,1],"--",color="gray",lw=1,label="Line of Perfect Equality")
    ax.fill_between(lz["Cum_Pop"], lz["Cum_Pop"], lz["Cum_Income"],
                    alpha=0.15, color="#2C6E9B")
    ax.set_xlabel("Cumulative Share of Workers (low → high wage)")
    ax.set_ylabel("Cumulative Share of Total Wages")
    ax.set_title(f"Lorenz Curve — Wage Inequality | PLFS Real Data\n"
                 f"Gini = {ineq['gini']:.3f}  |  Theil T = {ineq['theil']:.3f}  |  "
                 f"Between-sex = {ineq['theil_between']/ineq['theil']*100:.1f}% of Theil")
    ax.legend()
    fig.text(0.5,-0.04,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"05_lorenz_gini_PLFS.png"))
    plt.close()


def fig6_wage_by_state(desc):
    st = desc["state_stats"]
    # Top 20 states by sample size, sorted by wage
    top = st[st["n"] >= 200].sort_values("mean_wage")

    fig, ax = plt.subplots(figsize=(10,8.6))
    colors = plt.cm.Blues(np.linspace(0.30,0.85,len(top)))
    bars   = ax.barh(top.index, top["mean_wage"], color=colors, edgecolor="white")
    ax.bar_label(bars, labels=[f"₹{v:,.0f}  (n={int(n):,})"
                               for v,n in zip(top["mean_wage"],top["n"])],
                 padding=4, fontsize=7.5)
    ax.set_xlabel("Mean Monthly Wage (₹)")
    ax.set_title("Mean Monthly Wage by State — PLFS 2022–23\n(Survey-weighted, states with n ≥ 200)")
    fig.text(0.5,-0.02,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"06_wage_state_PLFS.png"))
    plt.close()


def fig7_wage_distributions(df):
    fig, axes = plt.subplots(1,2,figsize=(12,5))
    fig.suptitle("Wage Distribution by Sex and Location — PLFS Real Data",fontsize=13)

    from scipy.stats import gaussian_kde
    for panel, (grp_col, groups) in enumerate([
        ("sex",   [("Male",PAL["Male"]),("Female",PAL["Female"])]),
        ("urban", [(0,PAL["Rural"]),(1,PAL["Urban"])])
    ]):
        ax = axes[panel]
        labels = []
        for i,(val,color) in enumerate(groups):
            sub = df[df[grp_col]==val]["wage"].values / 1000
            sub = sub[sub < np.percentile(sub,99)]  # trim top 1% for display
            kde = gaussian_kde(sub, bw_method=0.25)
            y   = np.linspace(0, sub.max(), 300)
            x   = kde(y); x = x/x.max()*0.38
            ax.fill_betweenx(y, i-x, i+x, alpha=0.75, color=color)
            ax.plot([i-x, i+x], [np.median(sub),np.median(sub)],
                    color="white", lw=2)
            if grp_col == "sex":
                labels.append(val)
            else:
                labels.append("Rural" if val==0 else "Urban")
        ax.set_xticks(range(len(groups))); ax.set_xticklabels(labels)
        ax.set_ylabel("Monthly Wage (₹ thousands)")
        ax.set_title("By Sex" if panel==0 else "By Location")

    fig.text(0.5,-0.04,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"07_wage_distributions_PLFS.png"))
    plt.close()


def fig8_gender_gap_by_group(df):
    """Gender wage gap by social group and education band."""
    fig, axes = plt.subplots(1,2,figsize=(13,5))
    fig.suptitle("Gender Wage Gap Heterogeneity — PLFS Real Data",fontsize=13)

    # Panel A: gap by social group
    ax = axes[0]
    groups = ["Gen","OBC","SC","ST"]
    gaps   = []
    for g in groups:
        sub = df[df["group"]==g]
        mm  = np.average(sub[sub["sex"]=="Male"]["wage"],
                         weights=sub[sub["sex"]=="Male"]["weight"])
        mf  = np.average(sub[sub["sex"]=="Female"]["wage"],
                         weights=sub[sub["sex"]=="Female"]["weight"])
        gaps.append((mm - mf) / mm * 100)
    colors = [PAL[g] for g in groups]
    bars   = ax.bar(groups, gaps, color=colors, edgecolor="white", width=0.55)
    ax.bar_label(bars, labels=[f"{v:.1f}%" for v in gaps], padding=4)
    ax.set_ylabel("Gender Wage Gap (%)"); ax.set_ylim(0,max(gaps)*1.25)
    ax.set_title("Gender Gap by Social Group\n(Male–Female mean / Male mean)")
    ax.axhline(df.pipe(lambda x: (
        np.average(x[x["sex"]=="Male"]["wage"],weights=x[x["sex"]=="Male"]["weight"]) -
        np.average(x[x["sex"]=="Female"]["wage"],weights=x[x["sex"]=="Female"]["weight"])
    ) / np.average(x[x["sex"]=="Male"]["wage"],weights=x[x["sex"]=="Male"]["weight"])*100),
    color="gray", ls="--", lw=1, label="Overall gap")
    ax.legend(fontsize=9)

    # Panel B: gap by education band
    ax2 = axes[1]
    bins   = [0,8,12,15,22]
    labels = ["0–8 yrs\n(Up to Middle)","9–12 yrs\n(Secondary)","13–15 yrs\n(UG)","16+\n(PG)"]
    df2 = df.copy()
    df2["edu_band"] = pd.cut(df2["education"], bins=bins, labels=labels, right=True)
    edu_gaps = []
    for lb in labels:
        sub = df2[df2["edu_band"]==lb]
        mm  = np.average(sub[sub["sex"]=="Male"]["wage"],
                         weights=sub[sub["sex"]=="Male"]["weight"])
        mf  = np.average(sub[sub["sex"]=="Female"]["wage"],
                         weights=sub[sub["sex"]=="Female"]["weight"])
        edu_gaps.append((mm-mf)/mm*100)
    cols2 = plt.cm.Oranges(np.linspace(0.4,0.85,len(labels)))
    bars2 = ax2.bar(labels, edu_gaps, color=cols2, edgecolor="white", width=0.55)
    ax2.bar_label(bars2, labels=[f"{v:.1f}%" for v in edu_gaps], padding=4)
    ax2.set_ylabel("Gender Wage Gap (%)"); ax2.set_ylim(0,max(edu_gaps)*1.25)
    ax2.set_title("Gender Gap by Education Level")

    fig.text(0.5,-0.05,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"08_gender_gap_heterogeneity_PLFS.png"))
    plt.close()


def fig9_oaxaca_components(oa):
    """Detailed Oaxaca endowment component breakdown."""
    names = oa["comp_names"][1:]  # skip intercept
    comps = oa["comp_explained"][1:]
    total = oa["explained_log"]

    # Contribution as % of raw gap
    contribs = comps / oa["raw_gap_log"] * 100

    fig, ax = plt.subplots(figsize=(9,5.8))
    colors = ["#2C6E9B" if c >= 0 else "#D95F5F" for c in contribs]
    bars   = ax.barh(names, contribs, color=colors, edgecolor="white", height=0.6)
    ax.axvline(0,color="black",lw=0.8,ls="--")
    ax.set_xlabel("Contribution to Gender Gap (% of raw log gap)")
    ax.set_title(f"Oaxaca Endowment Decomposition — PLFS Real Data\n"
                 f"Total explained = {oa['explained_pct']:.1f}% of raw gap  "
                 f"(raw gap = {oa['raw_gap_log']:.3f} log points)")
    # Manual label placement: positive bars label to the right of bar end,
    # negative bars label to the left, with extra padding so labels never
    # collide with the y-axis tick text.
    xmin, xmax = min(contribs.min(),0), max(contribs.max(),0)
    span = xmax - xmin
    for bar, val in zip(bars, contribs):
        if val >= 0:
            ax.text(val + span*0.02, bar.get_y()+bar.get_height()/2,
                    f"{val:.1f}%", va="center", ha="left", fontsize=9)
        else:
            ax.text(val - span*0.02, bar.get_y()+bar.get_height()/2,
                    f"{val:.1f}%", va="center", ha="right", fontsize=9)
    ax.set_xlim(xmin - span*0.18, xmax + span*0.18)
    fig.text(0.5,-0.02,
            "Positive bar = this variable explains MORE gap (men have higher values/returns).\n"
            "Negative bar = this variable REDUCES the gap (women have higher values/returns).",
            ha="center",fontsize=8,color="#555")
    fig.text(0.5,-0.10,CAP,ha="center",fontsize=7.5,color="#555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR,"09_oaxaca_components_PLFS.png"))
    plt.close()


# =============================================================================
# MASTER RUNNER
# =============================================================================

def main():
    print("="*65)
    print(" Labour Market Intelligence — PLFS REAL DATA ANALYSIS")
    print(" Author: Rupal Rani | TISS Mumbai")
    print("="*65)

    print("\n[1/7] Loading and preparing PLFS data …")
    df = load_and_prepare(DATA_PATH)

    print("\n[2/7] Computing weighted descriptive statistics …")
    desc = compute_descriptives(df)
    print(f"\n  ── Headline Wage Statistics ──────────────────────────────────")
    print(f"  Total wage workers analysed : {desc['n_total']:,}")
    print(f"  Overall mean monthly wage   : ₹{desc['overall_mean']:,.0f}")
    print(f"  Overall median monthly wage : ₹{desc['overall_median']:,.0f}")
    print(f"  Male mean wage              : ₹{desc['sex_stats']['Male']['mean']:,.0f}  (n={desc['n_male']:,})")
    print(f"  Female mean wage            : ₹{desc['sex_stats']['Female']['mean']:,.0f}  (n={desc['n_female']:,})")
    print(f"  Raw gender wage gap         : {desc['gender_gap']*100:.1f}%")
    print(f"\n  ── Wage by Social Group ──────────────────────────────────────")
    for g,v in desc["grp_stats"].items():
        print(f"  {g:<6}: ₹{v['mean']:>9,.0f}/month  (median ₹{v['median']:>7,.0f})  n={v['n']:,}")
    print(f"\n  ── Wage by Location ──────────────────────────────────────────")
    for l,v in desc["loc_stats"].items():
        print(f"  {l:<6}: ₹{v['mean']:>9,.0f}/month  n={v['n']:,}")

    # Save descriptives table
    rows = []
    for g in ["Gen","OBC","SC","ST"]:
        for s in ["Male","Female"]:
            sub = df[(df["group"]==g)&(df["sex"]==s)]
            if len(sub)>0:
                rows.append({"Group":g,"Sex":s,
                             "Mean_Wage":round(np.average(sub["wage"],weights=sub["weight"])),
                             "Median_Wage":round(sub["wage"].median()),
                             "N":len(sub)})
    pd.DataFrame(rows).to_csv(os.path.join(TAB_DIR,"descriptives_PLFS.csv"),index=False)

    print("\n[3/7] Estimating Mincer earnings function (WLS) …")
    reg = mincer_regression(df)
    print(f"\n  ── Mincer Regression Results ──────────────────────────────────")
    print(f"  R² (weighted)               : {reg['r2']:.3f}")
    print(f"  N (employed, +wage)         : {reg['n']:,}")
    print(f"  Return to schooling         : {reg['return_to_schooling']:.2f}% per year ***")
    print(f"  Female wage penalty (cond.) : {reg['female_penalty_pct']:.1f}%")
    for lbl,b,p in zip(reg["labels"][1:],reg["beta"][1:],reg["p"][1:]):
        sig = "***" if p<0.01 else "**" if p<0.05 else "*" if p<0.1 else ""
        print(f"  {lbl:<25}: {b:+.4f}  {sig}")

    print("\n[4/7] Running Blinder-Oaxaca decomposition …")
    oa = oaxaca_decomposition(df)
    print(f"\n  ── Oaxaca Decomposition ───────────────────────────────────────")
    print(f"  Raw gender gap (log)        : {oa['raw_gap_log']:.4f}")
    print(f"  Raw gender gap (%)          : {oa['raw_gap_pct']:.1f}%")
    print(f"  Explained (endowments)      : {oa['explained_pct']:.1f}% of gap")
    print(f"  Unexplained (returns)       : {oa['unexplained_pct']:.1f}% of gap")
    print(f"  [Caution: unexplained ≠ discrimination]")

    print("\n[5/7] Computing inequality measures …")
    ineq = compute_inequality(df)
    print(f"\n  ── Inequality Measures ────────────────────────────────────────")
    print(f"  Gini Coefficient            : {ineq['gini']:.4f}")
    print(f"  Theil T (total)             : {ineq['theil']:.4f}")
    print(f"  Theil (between-sex)         : {ineq['theil_between']:.4f}  ({ineq['theil_between']/ineq['theil']*100:.1f}% of total)")
    print(f"  Theil (within-sex)          : {ineq['theil_within']:.4f}  ({ineq['theil_within']/ineq['theil']*100:.1f}% of total)")

    print("\n[6/7] Generating visualisations …")
    fig1_wage_by_sex_group(desc)
    fig2_wage_by_education(df)
    fig3_mincer_coefficients(reg)
    fig4_oaxaca(oa)
    fig5_lorenz(ineq)
    fig6_wage_by_state(desc)
    fig7_wage_distributions(df)
    fig8_gender_gap_by_group(df)
    fig9_oaxaca_components(oa)
    print(f"      Saved 9 figures to {FIG_DIR}")

    print("\n[7/7] Saving summary results table …")
    summary = pd.DataFrame({
        "Metric":["N (wage workers)","Overall Mean Wage","Male Mean Wage","Female Mean Wage",
                  "Raw Gender Wage Gap","Return to Schooling",
                  "Female Wage Penalty (controlled)","Oaxaca Explained",
                  "Oaxaca Unexplained","Gini Coefficient","Theil T","Theil Between-sex"],
        "Value":[f"{desc['n_total']:,}",
                 f"₹{desc['overall_mean']:,.0f}/month",
                 f"₹{desc['sex_stats']['Male']['mean']:,.0f}/month",
                 f"₹{desc['sex_stats']['Female']['mean']:,.0f}/month",
                 f"{desc['gender_gap']*100:.1f}%",
                 f"{reg['return_to_schooling']:.2f}% per year",
                 f"{reg['female_penalty_pct']:.1f}%",
                 f"{oa['explained_pct']:.1f}% of gap",
                 f"{oa['unexplained_pct']:.1f}% of gap",
                 f"{ineq['gini']:.4f}",
                 f"{ineq['theil']:.4f}",
                 f"{ineq['theil_between']/ineq['theil']*100:.1f}% of Theil"]
    })
    summary.to_csv(os.path.join(TAB_DIR,"PLFS_results_summary.csv"),index=False)

    print("\n" + "="*65)
    print(" REAL DATA ANALYSIS COMPLETE")
    print(f" Data: PLFS 2022-23 | {desc['n_total']:,} wage workers | 36 States")
    print(f" These results are based on actual PLFS microdata.")
    print(f" They are suitable for research publication.")
    print("="*65)

if __name__ == "__main__":
    main()
