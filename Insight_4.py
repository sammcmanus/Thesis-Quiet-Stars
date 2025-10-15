import pandas as pd

def insight_4_Load_Data():
    
    global player_stats_DF, team_df
    
    player_stats_DF = pd.read_csv("Data/Processed/player_stats_cleaned.csv")
    team_df  = pd.read_csv("Data/Processed/team_results.csv")


def insight_4_Stats():

    rp = player_stats_DF[(player_stats_DF['role'] == 'R') & (player_stats_DF['usg_percent'].between(10, 15, inclusive='both'))]

    print(rp)
        

if __name__ == "__main__":
    insight_4_Load_Data()
    insight_4_Stats()

'''# 2) Minutes-weighted team-season aggregation ---------------------------------
def minutes_weighted_team_agg(role_df: pd.DataFrame, min_team_role_minutes: float = 0.0) -> pd.DataFrame:
    """Aggregate to team-season level with minutes-weighted averages.
    Output columns:
      - role_ts_w: minutes-weighted TS% of selected role players
      - role_a2t_w: minutes-weighted A2T% of selected role players
      - role_min_sum: total minutes of selected role players
      - role_players_count: number of selected role-player rows
    Group key: ['season','abv'].
    """
    _require_cols(role_df, REQUIRED_COLS)

    def wavg(x: pd.Series, w: pd.Series) -> float:
        x = x.astype(float); w = w.astype(float)
        m = (~x.isna()) & (~w.isna())
        if m.any() and w[m].sum() > 0:
            return float(np.average(x[m], weights=w[m]))
        return np.nan

    grouped = (
        role_df
        .groupby(['season','abv'], as_index=False)
        .apply(lambda g: pd.Series({
            'role_ts_w': wavg(g['ts_percent'], g['mp']),
            'role_a2t_w': wavg(g['a2t_perc'], g['mp']),
            'role_min_sum': float(g['mp'].sum()),
            'role_players_count': int(g.shape[0]),
        }))
        .reset_index(drop=True)
    )
    if min_team_role_minutes > 0:
        grouped = grouped[grouped['role_min_sum'] >= min_team_role_minutes].copy()
    return grouped

# 3) Descriptive stats ---------------------------------------------------------
def describe_metrics(team_df: pd.DataFrame) -> pd.DataFrame:
    """Return mean, median, IQR, and N for role_ts_w and role_a2t_w.
    Requires the output of minutes_weighted_team_agg.
    """
    for c in ['role_ts_w','role_a2t_w']:
        if c not in team_df.columns:
            raise KeyError(f"Expected column '{c}' in team_df.")
    def desc(s: pd.Series) -> Dict[str, float]:
        s = s.dropna()
        if len(s) == 0:
            return {'Mean': np.nan, 'Median': np.nan, 'IQR': np.nan, 'N_teams': 0}
        return {
            'Mean': float(s.mean()),
            'Median': float(s.median()),
            'IQR': float(np.percentile(s, 75) - np.percentile(s, 25)),
            'N_teams': int(len(s))
        }
    rows = []
    for m in ['role_ts_w','role_a2t_w']:
        r = desc(team_df[m])
        r['Metric'] = m
        rows.append(r)
    out = pd.DataFrame(rows)[['Metric','Mean','Median','IQR','N_teams']]
    return out

# 4) Correlation helper (optional target) -------------------------------------
def correlate_with_target(team_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Compute Pearson r between each role metric and a target column you provide.
    Example target: 'team_win_perc' or 'w'.
    Returns a tidy 2-row table for role_ts_w and role_a2t_w.
    """
    for c in ['role_ts_w','role_a2t_w', target_col]:
        if c not in team_df.columns:
            raise KeyError(f"Expected column '{c}' in team_df.")
    rows = []
    for m in ['role_ts_w','role_a2t_w']:
        r = team_df[m].corr(team_df[target_col])
        rows.append({'Metric': m, 'Target': target_col, 'r': float(r) if pd.notna(r) else np.nan, 'N': int(team_df[[m, target_col]].dropna().shape[0])})
    return pd.DataFrame(rows)[['Metric','Target','r','N']]

# 5) Simple quartile comparison (optional) ------------------------------------
def quartile_compare(team_df: pd.DataFrame, metric: str, target_col: str) -> pd.DataFrame:
    """Compare Top vs Bottom quartile of 'metric' on the provided target.
    Returns a 2-row summary (Bottom 25%, Top 25%) with average metric and average target.
    """
    if metric not in team_df.columns or target_col not in team_df.columns:
        raise KeyError("Columns missing in team_df for quartile comparison.")
    df = team_df.dropna(subset=[metric, target_col]).copy()
    if df.empty:
        return pd.DataFrame(columns=['Group','Avg Metric','Avg Target','N teams'])
    q1, q3 = np.percentile(df[metric], [25, 75])
    low = df[df[metric] <= q1]
    high = df[df[metric] >= q3]
    return pd.DataFrame({
        'Group': ['Bottom 25%', 'Top 25%'],
        'Avg Metric': [float(low[metric].mean()), float(high[metric].mean())],
        'Avg Target': [float(low[target_col].mean()), float(high[target_col].mean())],
        'N teams': [int(len(low)), int(len(high))]
    })
'''