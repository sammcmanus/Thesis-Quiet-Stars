import os
import pandas as pd
import numpy as np

# Set working directory
set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_3_Load_Data():
    
    global player_stats_DF
    
    player_stats_DF = pd.read_csv("Data/Processed/player_stats_cleaned.csv")
    
def _agg_by_group(gb, metrics, weight_col=None):
    
    # Aggregate metrics by group with mean, median, IQR, and weighted mean if weight_col is provided.
    rows = []
    for segment, chunk in gb:
        row = {"segment": segment}
        for m in metrics:
            x = chunk[m].dropna()
            if x.empty:
                row[f"{m}_mean"] = np.nan
                row[f"{m}_median"] = np.nan
                row[f"{m}_iqr"] = np.nan
                row[f"{m}_wmean"] = np.nan
                continue

            row[f"{m}_mean"] = x.mean()
            row[f"{m}_median"] = x.median()
            row[f"{m}_iqr"] = np.subtract(*np.percentile(x, [75, 25]))

            if weight_col is not None and weight_col in chunk.columns:
                w = chunk.loc[x.index, weight_col].fillna(0)
                row[f"{m}_wmean"] = np.average(x, weights=w) if w.sum() > 0 else np.nan
            else:
                row[f"{m}_wmean"] = np.nan
        rows.append(row)
    return pd.DataFrame(rows)

def insight3_efficiency_tables() -> dict:
    
    df = player_stats_DF.copy()

    # compute minutes per season for weighting if columns exist
    weight_col = None

    df["is_vet"] = df["experience"] >= 7

    df["minutes_weight"] = df["mp_per_game"] * df["g"]
    weight_col = "minutes_weight"

    # Identify available efficiency metrics
    candidate_metrics = ["per", "ts_percent", "obpm", "dbpm", "usg_percent"]

    metrics = [c for c in candidate_metrics if c in df.columns]

    # drop rows with unknown vet status (NaN experience)
    d = df.dropna(subset=["is_vet"]).copy()

    # overall vets vs non-vets
    overall_df = _agg_by_group(d.groupby("is_vet"), metrics, weight_col=weight_col)

    # by role and vet status
    by_role_df = _agg_by_group(d.groupby(["role", "is_vet"]), metrics, weight_col=weight_col)
    by_role_df["segment"] = by_role_df["segment"].apply(lambda s: f"{s[0]}|{s[1]}")
      
    #print("\nOverall (vets vs non-vets):\n")
    #print(overall_df)
    overall_df.to_csv("Data/Insights/Insight_3_overall_vets_v_nonvet.csv", index=False)

    #print("\nBy Role & Vet (e.i. 'R(role)|True(vet)' ):\n")
    #print(by_role_df.sort_values(by='segment', ascending=False))
    by_role_df.to_csv("Data/Insights/Insight_3_by_role_and_vet.csv", index=False)


if __name__ == "__main__":

    os.chdir(set_working_dir)
    insight_3_Load_Data()
    insight3_efficiency_tables()


