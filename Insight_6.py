import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_6_Load_Data():
    global team_results_DF, role_df, metrics

    player_stats_DF = pd.read_csv("Data/Processed/player_stats_cleaned.csv")
    team_results_DF = pd.read_csv("Data/Processed/team_results.csv")

    # Role players only
    role_df = player_stats_DF.loc[player_stats_DF["role"] == "R"].copy()

    # Relevant metrics for role depth
    metrics = ["per", "ts_percent", "obpm", "dbpm", "usg_percent", "a2t_perc"]

def _weighted_avg(df: pd.DataFrame, value_col: str, weight_col: str) -> float:
    
    # Calculate weighted average of value_col using weight_col as weights
    return np.average(df[value_col], weights=df[weight_col])

def insight_6_Build_Role_Depth():
    global role_depth_df

    rows = []
    for (season, abv), g in role_df.groupby(["season", "abv"]):
        row = {"season": season, "abv": abv}

        # Means and minutes-weighted means
        for m in metrics:
            if m in g.columns:
                row[f"{m}_mean"] = g[m].mean()
                
                row[f"{m}_wmean"] = _weighted_avg(g, m, "mp")
            else:
                row[f"{m}_mean"] = np.nan
                row[f"{m}_wmean"] = np.nan

        row["role_mp_total"] = g["mp"].sum() 
        row["role_gs_total"] = g["gs"].sum() 
        row["role_count"] = int(g.shape[0])
        row["made_playoffs"] = bool(g["playoffs"].max())

        rows.append(row)

    role_depth_df = pd.DataFrame(rows).sort_values(["season", "abv"])

    role_depth_df.to_csv("Data/Insights/Insight_6_role_depth_by_team_season.csv", index=False)

def insight_6_Join_Team_Results():
    global team_merged_df
    
    # Merge role-depth metrics with team results
    team_merged_df = team_results_DF.merge(role_depth_df, on=["season", "abv"], how="left")

def insight_6_Correlations():
    global top_metric

    records = []

    for m in metrics:
        for suf in ["mean", "wmean"]:
            col = f"{m}_{suf}"
            if col in team_merged_df.columns:
                temp = team_merged_df[[col, "win_pct"]].dropna()
                if temp.shape[0] >= 3:
                    r = temp.corr().iloc[0, 1]
                    records.append(
                        {
                            "metric": col,
                            "corr_win_pct": round(float(r), 3),
                            "n": int(temp.shape[0]),
                        }
                    )

    corr_df = pd.DataFrame(records).sort_values("corr_win_pct", ascending=False)
    corr_df.to_csv("Data/Insights/Insight_6_correlations.csv", index=False)

    # Choose top metric for breakdowns & plots
    top_metric = corr_df.iloc[0]["metric"] if not corr_df.empty else None

def insight_6_Breakdowns():
    
    # Conference correlations
    conf_rows = []
    for conf, g in team_merged_df.dropna(subset=[top_metric, "win_pct", "conference"]).groupby("conference"):
        if g.shape[0] >= 3:
            r = g[[top_metric, "win_pct"]].corr().iloc[0, 1]
            conf_rows.append({"conference": conf, "corr": float(r), "n": int(g.shape[0])})
    conf_df = pd.DataFrame(conf_rows).sort_values("corr", ascending=False)
    
    conf_df.to_csv(f"Data/Insights/Insight_6_{top_metric}_conference_correlations.csv", index=False)

    # Division correlations
    div_rows = []
    for div, g in team_merged_df.dropna(subset=[top_metric, "win_pct", "division"]).groupby("division"):
        if g.shape[0] >= 3:
            r = g[[top_metric, "win_pct"]].corr().iloc[0, 1]
            div_rows.append({"division": div, "corr": float(r), "n": int(g.shape[0])})
    div_df = pd.DataFrame(div_rows).sort_values("corr", ascending=False)
    
    div_df.to_csv(f"Data/Insights/Insight_6_{top_metric}_division_correlations.csv", index=False)

    # Playoff vs Non-Playoff comparison
    pm = (
        team_merged_df
        .dropna(subset=[top_metric])
        .groupby("made_playoffs")[top_metric]
        .agg(["mean", "median", "count"])
        .reset_index()
    )
    
    pm.to_csv(f"Data/Insights/Insight_6_{top_metric}_playoff_comparison.csv", index=False)


def insight_6_main():
    insight_6_Build_Role_Depth()
    insight_6_Join_Team_Results()
    insight_6_Correlations()
    insight_6_Breakdowns()

if __name__ == "__main__":
    os.chdir(set_working_dir)
    insight_6_Load_Data()
    insight_6_main()
