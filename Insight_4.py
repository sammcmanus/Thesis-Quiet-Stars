import os
import numpy as np
import pandas as pd


set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

PROCESSED = "Data/Processed"
BENCH_IN  = os.path.join(PROCESSED, "bench_core_min.csv")
TEAM_OUT  = os.path.join(PROCESSED, "team_outcomes.csv")

def _wmean(x, w):
    x = pd.to_numeric(x, errors="coerce")
    w = pd.to_numeric(w, errors="coerce")
    m = x.notna() & w.notna() & (w > 0)
    if m.sum() == 0 or w[m].sum() == 0:
        return np.nan
    return float(np.average(x[m], weights=w[m]))

def _safe_ratio(num, den):
    num = pd.to_numeric(num, errors="coerce")
    den = pd.to_numeric(den, errors="coerce")
    m = den.notna() & (den != 0)
    out = pd.Series(np.nan, index=num.index)
    out[m] = num[m] / den[m]
    return out

def _assign_seed_and_tiers(df):
    """
    Seed within each (season, conference) by descending win% (ties broken by wins).
    If 'conference' missing, seed is within season only.
    Tiers:
      - seed_tier: Top 4, 5-8, 9-15
      - wpct_tier: High/Mid/Low by win_pct terciles (season-wise)
    """
    d = df.copy()

    # Seed
    grp_cols = ["season"] + (["conference"] if "conference" in d.columns else [])
    d = d.sort_values(grp_cols + ["win_pct","w"], ascending=[True]*len(grp_cols) + [False, False])
    d["seed"] = d.groupby(grp_cols).cumcount() + 1

    # Seed tiers
    def seed_tier(s):
        if s <= 4:  return "Top 4"
        if s <= 8:  return "5-8"
        return "9-15"
    d["seed_tier"] = d["seed"].apply(seed_tier)

    # Win% terciles by season
    d["wpct_rank"] = d.groupby("season")["win_pct"].rank(pct=True, method="average")
    d["wpct_tier"] = pd.cut(d["wpct_rank"], bins=[0, 1/3, 2/3, 1], labels=["Low","Mid","High"], include_lowest=True)

    # Playoffs flag (pre-play-in): seed <= 8
    d["made_playoffs"] = d["seed"] <= 8

    return d.drop(columns=["wpct_rank"])

def run():
    bench = pd.read_csv(BENCH_IN)
    team  = pd.read_csv(TEAM_OUT)

    # Aggregate bench efficiency to team-season (minutes-weighted)
    # Build AST/TOV ratio from percentages (proxy)
    bench["ts_percent"]  = pd.to_numeric(bench.get("ts_percent"), errors="coerce")
    bench["ast_percent"] = pd.to_numeric(bench.get("ast_percent"), errors="coerce")
    bench["tov_percent"] = pd.to_numeric(bench.get("tov_percent"), errors="coerce")
    bench["mp"]          = pd.to_numeric(bench.get("mp"), errors="coerce")
    bench["ast_tov_ratio_pct"] = _safe_ratio(bench["ast_percent"], bench["tov_percent"])

    grp = ["season","abv"]
    bench_team = bench.groupby(grp).apply(lambda g: pd.Series({
        "bench_ts_wmean":      _wmean(g["ts_percent"], g["mp"]),
        "bench_asttov_wmean":  _wmean(g["ast_tov_ratio_pct"], g["mp"]),
        "bench_mp_sum":        pd.to_numeric(g["mp"], errors="coerce").fillna(0).sum(),
        "bench_count":         g.shape[0]
    })).reset_index()

    # Merge outcomes (season, abv) -> add seed, tiers, playoffs
    keep = ["season","abv","w","l","games","win_pct"]
    if "conference" in team.columns: keep.append("conference")
    merged = bench_team.merge(team[keep], on=["season","abv"], how="left")
    merged = _assign_seed_and_tiers(merged)

    # Segment summaries: means by conference and tier
    seg_cols = []
    if "conference" in merged.columns: seg_cols.append("conference")
    seg_cols += ["seed_tier","wpct_tier"]

    summaries = []
    for c in seg_cols:
        s = merged.groupby(["season", c]).agg(
            teams=("abv","nunique"),
            bench_ts_wmean=("bench_ts_wmean","mean"),
            bench_asttov_wmean=("bench_asttov_wmean","mean"),
            win_pct=("win_pct","mean"),
            made_playoffs_rate=("made_playoffs", "mean")
        ).reset_index()
        s.insert(1, "segment", c)
        summaries.append(s)
    seg_summary = pd.concat(summaries, ignore_index=True)

    # Simple association tests: difference in means of bench metrics between made_playoffs True/False within segments
    diffs = []
    for c in seg_cols:
        for level, g in merged.groupby([c, "season"]):
            if isinstance(level, tuple): level = level[0]
            if g["made_playoffs"].nunique() < 2:  # need both True/False present
                continue
            gp = g.groupby("made_playoffs").agg(
                ts=("bench_ts_wmean","mean"),
                at=("bench_asttov_wmean","mean"),
                n=("abv","nunique")
            ).reset_index()
            if gp.shape == (2,4):
                row = {
                    "season": g["season"].iloc[0],
                    "segment": c,
                    "level": level,
                    "ts_diff_playoff_minus_non": float(gp.loc[gp["made_playoffs"],"ts"].values[0] - gp.loc[~gp["made_playoffs"],"ts"].values[0]),
                    "at_diff_playoff_minus_non": float(gp.loc[gp["made_playoffs"],"at"].values[0] - gp.loc[~gp["made_playoffs"],"at"].values[0]),
                    "n_playoff": int(gp.loc[gp["made_playoffs"],"n"].values[0]),
                    "n_non": int(gp.loc[~gp["made_playoffs"],"n"].values[0]),
                }
                diffs.append(row)
    seg_diffs = pd.DataFrame(diffs).sort_values(["season","segment","level"])

    # Save outputs
    os.makedirs(PROCESSED, exist_ok=True)
    merged.to_csv(os.path.join(PROCESSED, "bench_postseason_joined.csv"), index=False)
    seg_summary.to_csv(os.path.join(PROCESSED, "bench_postseason_segment_summary.csv"), index=False)
    seg_diffs.to_csv(os.path.join(PROCESSED, "bench_postseason_segment_diffs.csv"), index=False)

    print("Bench postseason (segmented) done.")
    print(seg_summary.head(6))
    print(seg_diffs.head(6))

if __name__ == "__main__":
    run()
