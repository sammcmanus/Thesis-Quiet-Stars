"""
Insight 5 — Role Versatility & Team Success (minimal, fixed columns)

Inputs:
  Data/Processed/player_stats_cleaned.csv  (uses: season, abv, role, ts_percent, usg_percent, ast_per_game, tov_per_game)
  Data/Processed/team_results.csv          (uses: season, abv, win_pct)

Outputs:
  Data/Insights/Insight_5_role_rvs_corr_vs_winpct.csv
  Data/Insights/Insight_5_role_rvs_top_vs_bottom_gap.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path
import os

# Use a raw string for Windows paths to avoid escape issues
set_working_dir = r"C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_5_Load_Data():
    global players, teams
    players = pd.read_csv("Data/Processed/player_stats_cleaned.csv", usecols=["season","abv","role","ts_percent","usg_percent","ast_per_game","tov_per_game"])
    teams   = pd.read_csv("Data/Processed/team_results.csv", usecols=["season","abv","win_pct"])

def _winsorize(s, lo=0.025, hi=0.975):
    ql, qu = s.quantile([lo, hi])
    return s.clip(ql, qu)

def _zscore_by_season(df, col, season_key):
    def _zs(s):
        std = s.std(ddof=0)
        if pd.isna(std) or std == 0:
            return pd.Series(np.zeros(len(s)), index=s.index)
        return (s - s.mean()) / std
    return df.groupby(season_key)[col].transform(_zs)

def insight_5_main():
    # Fixed keys/columns
    season_col = "season"
    team_col   = "abv"
    role_col   = "role"


    players_rb = players[players[role_col].isin(["R","B"])].copy()
    players_rb["__usg_w"] = players_rb.groupby(season_col)["usg_percent"].transform(_winsorize)

    z_ts   = _zscore_by_season(players_rb, "ts_percent", season_col)
    z_usg  = _zscore_by_season(players_rb, "__usg_w",    season_col)
    z_ast  = _zscore_by_season(players_rb, "ast_per_game", season_col)
    z_tov  = -_zscore_by_season(players_rb, "tov_per_game", season_col)  

    stack = np.vstack([z_ts.values, z_usg.values, z_ast.values, z_tov.values])
    players_rb["rvs"] = np.nanmean(stack.T, axis=1)

    team_role = (
        players_rb.groupby([season_col, team_col, role_col], as_index=False)
                  .agg(rvs_mean=("rvs","mean"),
                       n_players=("rvs","count"))
    )

    tr = team_role.merge(
        teams[[season_col, team_col, "win_pct"]],
        on=[season_col, team_col],
        how="left"
    ).dropna(subset=["rvs_mean","win_pct"])

    # Correlation (Role vs Bench)
    corr_rows = []
    for r in ["R","B"]:
        sub = tr[tr[role_col] == r]
        n = sub.shape[0]
        pearson = sub["rvs_mean"].corr(sub["win_pct"]) if n >= 3 else np.nan
        corr_rows.append({
            role_col: r,
            "metric": "rvs_mean",
            "n_teams": int(n),
            "pearson_r": (None if pd.isna(pearson) else round(float(pearson), 3))
        })
    corr_df = pd.DataFrame(corr_rows)

    # Top vs Bottom Quartile Win% Gap
    gap_rows = []
    for r in ["R","B"]:
        sub = tr[tr[role_col] == r].copy()
        if sub.shape[0] >= 12:
            sub["__rvs_q"] = pd.qcut(sub["rvs_mean"], 4, labels=[1,2,3,4])
            q1 = sub.loc[sub["__rvs_q"] == 1, "win_pct"]
            q4 = sub.loc[sub["__rvs_q"] == 4, "win_pct"]
            gap_rows.append({
                role_col: r,
                "q1_avg_winpct": round(q1.mean(), 3),
                "q4_avg_winpct": round(q4.mean(), 3),
                "gap_q4_minus_q1": round((q4.mean() - q1.mean()), 3),
                "n_q1": int(q1.size),
                "n_q4": int(q4.size)
            })
    gap_df = pd.DataFrame(gap_rows)


    Path("Data/Insights").mkdir(parents=True, exist_ok=True)
    corr_df.to_csv("Data/Insights/Insight_5_role_rvs_corr_vs_winpct.csv", index=False)
    gap_df.to_csv("Data/Insights/Insight_5_role_rvs_top_vs_bottom_gap.csv", index=False)

 

if __name__ == "__main__":
    os.chdir(set_working_dir)
    insight_5_Load_Data()
    insight_5_main()
