'''
•	Role Player Versatility and Offensive Efficiency
o	Analyze how role players (Usage 10-15%) contribute through shooting %, Assist-to-turnover %, FT %. 
o	Highlights the importance of having versatile role players that are efficient.
'''
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import os

set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_4_Load_Data():
    
    global role_df
    
    player_stats_DF = pd.read_csv("Data/Processed/player_stats_cleaned.csv")

    role_df = player_stats_DF[(player_stats_DF['role'] == 'R') & (player_stats_DF['usg_percent'].between(10, 15, inclusive='both'))]

def _weighted_corr(x: pd.Series, y: pd.Series, w: pd.Series) -> float:
    
    m = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(w) & (w > 0)   
    x, y, w = x[m], y[m], w[m]
    ws = w.sum()
    xm, ym = (w*x).sum()/ws, (w*y).sum()/ws
    cov = (w*((x-xm)*(y-ym))).sum()/ws
    vx  = (w*((x-xm)**2)).sum()/ws
    vy  = (w*((y-ym)**2)).sum()/ws
    
    return cov/np.sqrt(vx*vy)

def _pvalue(r: float, n: int) -> float:
    z = 0.5 * math.log((1 + r) / (1 - r))
    z_stat = z * math.sqrt(n - 3)
    p = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z_stat) / math.sqrt(2))))
    return p

def compute_overall_results():
    
    # Metrics table for TS% and A2T vs team_win_perc (unweighted & minutes-weighted).
    # Columns: metric, mean, median, iqr, corr_team_win_perc, corr_team_win_perc_weighted_by_minutes, n
    
    weight = role_df["mp"].fillna(role_df["mp_per_game"]) if "mp" in role_df.columns else role_df["mp_per_game"]

    rows = []
    for metric in ["ts_percent", "a2t_perc"]:
        rows.append({
            "metric": metric,
            "mean": round(role_df[metric].mean(),3),
            "median": round(role_df[metric].median(),3),
            "iqr": round(role_df[metric].quantile(0.75) - role_df[metric].quantile(0.25),3),
            "corr_team_win_perc": round(role_df[metric].corr(role_df["team_win_perc"]), 3),
            "corr_team_win_perc_weighted_by_minutes": round(_weighted_corr(role_df[metric], role_df["team_win_perc"], weight),3),
            "n": int(role_df[metric].notna().sum())
        })

    cols = ["metric", "mean", "median", "iqr", "corr_team_win_perc", "corr_team_win_perc_weighted_by_minutes", "n"]

    results_df = pd.DataFrame(rows)[cols]
    
    results_df.to_csv("Data/Insights/Insight_4_overall_results.csv", index=False)

def plot_insight4_a2t_vs_wins():

    # Scatter + unweighted trend line for A2T vs team_win_perc (role players; USG 10–15)

    x = role_df["a2t_perc"]
    y = role_df["team_win_perc"]
    n = role_df[["a2t_perc", "team_win_perc"]].dropna().shape[0]
    
    r = x.corr(y)
    w = role_df["mp"] if "mp" in role_df.columns else role_df["mp_per_game"]
    r_w = _weighted_corr(x, y, w)
    p = _pvalue(r, n)


    plt.figure(figsize=(7.5, 5.5))
    plt.scatter(x, y, s=12, alpha=0.6)

    # unweighted least squares line

    xn = x.to_numpy()
    yn = y.to_numpy()
    m = ~np.isnan(xn) & ~np.isnan(yn)

    k, b = np.polyfit(xn[m], yn[m], 1)
    xline = np.linspace(xn[m].min(), xn[m].max(), 100)
    yline = k * xline + b
    plt.plot(xline, yline, linewidth=2)

    plt.xlabel("Assist-to-Turnover Ratio (A2T)")
    plt.ylabel("Team Win %")
    plt.title("Role Players (USG 10–15): A2T vs Team Win%")
    plt.suptitle(f"r = {r:.3f} | minutes-weighted r = {r_w:.3f} | approx p = {p:.4f} | n = {n}", y=0.02, fontsize=9)
    plt.tight_layout()
    plt.savefig('img/Insight_4_RP_A2T_WINS.png')



def plot_insight4_ts_vs_wins():
    
    # Scatter + unweighted trend line for TS% vs team_win_perc (role players; USG 10–15).
    
    x = role_df["ts_percent"]
    y = role_df["team_win_perc"]
    n = role_df[["ts_percent", "team_win_perc"]].dropna().shape[0]

    r = x.corr(y)
    w = role_df["mp"] if "mp" in role_df.columns else role_df["mp_per_game"]
    r_w = _weighted_corr(x, y, w)
    p = _pvalue(r, n)


    plt.figure(figsize=(7.5, 5.5))
    plt.scatter(x, y, s=12, alpha=0.6)
    
    # unweighted least squares line

    xn = x.to_numpy()
    yn = y.to_numpy()
    m = ~np.isnan(xn) & ~np.isnan(yn)
    k, b = np.polyfit(xn[m], yn[m], 1)
    xline = np.linspace(xn[m].min(), xn[m].max(), 100)
    yline = k * xline + b
    plt.plot(xline, yline, linewidth=2)

    plt.xlabel("True Shooting % (TS%)")
    plt.ylabel("Team Win %")
    plt.title("Role Players (USG 10–15): TS% vs Team Win%")
    plt.suptitle(f"r = {r:.3f} | minutes-weighted r = {r_w:.3f} | approx p = {p:.4f} | n = {n}", y=0.02, fontsize=9)
    plt.tight_layout()
    plt.savefig('img/Insight_4_RP_TS_WINS.png')
    

def insight_4_main():
    compute_overall_results()
    plot_insight4_ts_vs_wins()
    plot_insight4_a2t_vs_wins()

if __name__ == "__main__":

    os.chdir(set_working_dir)
    insight_4_Load_Data()  
    insight_4_main()


    