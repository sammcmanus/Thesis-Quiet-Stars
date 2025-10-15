'''
•	Bench Strength and End-of-Season Standings
o	Aggregate efficiency metrics (gathered in Bench player efficiency previous insights) per team and correlate with team end of season standings, post season results.
o	Proving bench players are the quiet stars for a team's success.
'''
import numpy as np
import pandas as pd
import os

set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_5_Load_Data():

    global bench, teams_DF, metric_cols
    
    player_stats_DF = pd.read_csv("Data/Processed/player_stats_cleaned.csv")
    teams_DF = pd.read_csv("Data/Processed/team_results.csv")

    bench_cols = ["per", "ts_percent", "obpm", "dbpm", "usg_percent", "a2t_perc", "mp"]
    bench = player_stats_DF.loc[player_stats_DF["role"] == "B", ["season", "abv"] + bench_cols].copy()

    metric_cols = ["bench_per_wmean", "bench_ts_percent_wmean", "bench_obpm_wmean", "bench_dbpm_wmean", "bench_usg_percent_wmean", "bench_a2t_perc_wmean",
                   "bench_per_mean", "bench_ts_percent_mean", "bench_obpm_mean", "bench_dbpm_mean", "bench_usg_percent_mean", "bench_a2t_perc_mean"]

def _weighted_avg(series, weights):
    w = np.asarray(weights)
    x = np.asarray(series)
    if w.sum() == 0 or len(x) == 0:
        return np.nan
    return np.average(x, weights=w)

def _corr_table(frame, y_col="win_pct"):

    out = []
    for m in metric_cols:
        if m in frame.columns and frame[m].notna().sum() > 2 and frame[y_col].notna().sum() > 2:
            r = frame[m].corr(frame[y_col])  # Pearson
        else:
            r = np.nan
        out.append({"metric": m, "pearson_r_vs_" + y_col: r})
    return pd.DataFrame(out).sort_values("metric").reset_index(drop=True)

def _spearman_table(frame, rank_col):
    out = []
    sub = frame.copy()
    for m in metric_cols:
        if m in sub.columns:
            pair = sub[[m, rank_col]].dropna()
            if len(pair) > 2:
                rho = pair[m].rank().corr(pair[rank_col].rank(), method="pearson")
            else:
                rho = np.nan
            out.append({"metric": m, f"spearman_rho_vs_{rank_col}": rho})
    return pd.DataFrame(out).sort_values("metric").reset_index(drop=True)



def insight_5_main():
    
    agg_rows = []
    for (season, abv), g in bench.groupby(["season", "abv"]):
        mp = g["mp"].sum()
        row = {
            "season": season,
            "abv": abv,
            "bench_mp": float(mp),
            "bench_players": int(len(g))
        }
        # Weighted means for efficiency metrics
        for c in ["per", "ts_percent", "obpm", "dbpm", "usg_percent", "a2t_perc"]:
            row[f"bench_{c}_wmean"] = _weighted_avg(g[c], g["mp"])
            row[f"bench_{c}_mean"]  = g[c].mean()
        agg_rows.append(row)

    bench_team = pd.DataFrame(agg_rows)

    df = (bench_team
            .merge(teams_DF, on=["season", "abv"], how="inner")
            .copy())


    df["overall_rank"] = df.groupby("season")["win_pct"].rank(ascending=False, method="min")
    df["conf_rank"]    = df.groupby(["season", "conference"])["win_pct"].rank(ascending=False, method="min")


    # Overall Pearson vs win_pct
    corr_overall = _corr_table(df, "win_pct")
    corr_overall.to_csv("Data/Insights/bench_correlations_overall_vs_winpct.csv", index=False)

    # By conference
    rows_conf = []
    for (conf,), g in df.groupby(["conference"]):
        ctab = _corr_table(g, "win_pct")
        ctab.insert(0, "conference", conf)
        rows_conf.append(ctab)
    corr_by_conf = pd.concat(rows_conf, ignore_index=True)
    corr_by_conf.to_csv("Data/Insights/bench_correlations_by_conference_vs_winpct.csv", index=False)

    # By division
    rows_div = []
    for (div,), g in df.groupby(["division"]):
        ctab = _corr_table(g, "win_pct")
        ctab.insert(0, "division", div)
        rows_div.append(ctab)
    corr_by_div = pd.concat(rows_div, ignore_index=True)
    corr_by_div.to_csv("Data/Insights/bench_correlations_by_division_vs_winpct.csv", index=False)


    spearman_overall = _spearman_table(df, "overall_rank")
    spearman_overall.to_csv("Data/Insights/bench_vs_overall_rank_spearman.csv", index=False)

    df_out_cols = [
    "season","abv","conference","division","w","l","games","win_pct",
    "overall_rank","conf_rank",
    "bench_mp","bench_players"
    ] + [c for c in df.columns if c.startswith("bench_") and c not in ["bench_mp","bench_players"]]
    df[df_out_cols].to_csv("Data/Insights/bench_team_metrics.csv", index=False)


    pd.set_option("display.width", 120)
    pd.set_option("display.max_rows", 200)

    print("\n=== Insight 5: Bench Strength vs Win% (Overall, Pearson) ===")
    print(corr_overall.sort_values("pearson_r_vs_win_pct", ascending=False).to_string(index=False))

    print("\n=== By Conference (Pearson vs Win%) ===")
    for conf, g in corr_by_conf.groupby("conference"):
        print(f"\n-- {conf} --")
        print(g.sort_values("pearson_r_vs_win_pct", ascending=False).to_string(index=False))

    print("\n=== Spearman vs Overall Rank (negative is better) ===")
    print(spearman_overall.sort_values("spearman_rho_vs_overall_rank").to_string(index=False))








    return None

if __name__ == "__main__":

    os.chdir(set_working_dir)
    insight_5_Load_Data()  
    insight_5_main()

