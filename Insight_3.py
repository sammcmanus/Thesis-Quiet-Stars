import os
import pandas as pd
import numpy as np

# Set your working directory here
set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_3_Load_Data():
    
    global player_stats_DF
    
    player_stats_DF = pd.read_csv("Data/Processed/player_stats_cleaned.csv")
    
    # Create a new column 'is_vet' to indicate if a player is a veteran (7 or more years of experience)
    player_stats_DF["is_vet"] = player_stats_DF["experience"] >= 7


def _available(df: pd.DataFrame, cols):
    return [c for c in cols if c in df.columns]

def _agg_by_group(gb, metrics, weight_col=None):
    """
    Build a table with mean/median/IQR and minutes-weighted mean (if weight_col given).
    """
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

def insight3_efficiency_tables(player_stats_DF: pd.DataFrame) -> dict:
    """
    Build efficiency comparison tables for vets vs non-vets.

    Returns:
      {
        "overall": DataFrame of vets vs non-vets,
        "by_role": DataFrame of (role, vet split) if 'role' column exists
      }
    """
    df = player_stats_DF.copy()
    if "is_vet" not in df.columns:
        raise ValueError("Missing 'is_vet'. Add it first with: df['is_vet'] = df['experience'] >= 7")

    # compute minutes per season for weighting if columns exist
    weight_col = None
    if "mp_per_game" in df.columns and "g" in df.columns:
        df["minutes_weight"] = df["mp_per_game"] * df["g"]
        weight_col = "minutes_weight"

    # use only metrics that are present in your file
    candidate_metrics = ["per", "ts_percent", "obpm", "dbpm", "usg_percent"]
    metrics = _available(df, candidate_metrics)
    if not metrics:
        raise ValueError("No efficiency metrics found. Expected one or more of: " + ", ".join(candidate_metrics))

    # drop rows with unknown vet status (NaN experience)
    d = df.dropna(subset=["is_vet"]).copy()

    # overall vets vs non-vets
    overall = _agg_by_group(d.groupby("is_vet"), metrics, weight_col=weight_col)

    # by role (if present)
    if "role" in d.columns:
        by_role = _agg_by_group(d.groupby(["role", "is_vet"]), metrics, weight_col=weight_col)
        by_role["segment"] = by_role["segment"].apply(lambda s: f"{s[0]}|{s[1]}")
    else:
        by_role = pd.DataFrame(columns=["segment"] + [f"{m}_{t}" for m in metrics for t in ["mean","median","iqr","wmean"]])

    return {"overall": overall, "by_role": by_role}


if __name__ == "__main__":
    os.chdir(set_working_dir)
    insight_3_Load_Data()

    tables = insight3_efficiency_tables(player_stats_DF)
    overall_df = tables["overall"]
    by_role_df = tables["by_role"]

    print("Overall (vets vs non-vets):")
    print(overall_df)

    print("\nBy Role (e.g., 'R|True' = Role Player & Veteran):")
    print(by_role_df)