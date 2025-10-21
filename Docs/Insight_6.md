# Insight 6: Role Player Depth and End-of-Season Standings

## Type of Finding:
Quantitative/correlation analysis with conference & division breakdowns.

---

### Details

Using only players labeled `role == 'R'`, I aggregated team-season role-player efficiency with both simple means and minutes-weighted means for: `per`, `ts_percent`, `obpm`, `dbpm`, `usg_percent`, `a2t_perc`. I then joined these to team results (`win_pct`, `conference`, `division`) to evaluate relationships between role-player depth and team success.

**Top correlations vs team win_pct (n = 716 team-seasons):**

| Metric | Corr with Win% | n |
|---|---:|---:|
| dbpm_mean | 0.610 | 716 |
| dbpm_wmean | 0.605 | 716 |
| obpm_mean | 0.358 | 716 |
| obpm_wmean | 0.351 | 716 |
| ts_percent_mean | 0.304 | 716 |
| ts_percent_wmean | 0.302 | 716 |
| a2t_perc_wmean | 0.262 | 716 |
| a2t_perc_mean | 0.242 | 716 |
| per_mean | 0.208 | 716 |
| per_wmean | 0.207 | 716 |

Among role-player metrics, defensive impact (DBPM) shows the strongest association with team winning. Both simple team averages and minutes-weighted averages of role-player DBPM correlate best with win percentage.

**Conference breakdown (top metric: `dbpm_mean`):**

| conference | corr | n |
|---|---:|---:|
| Eastern | 0.628895 | 360 |
| Western | 0.589860 | 356 |

**Division breakdown (top metric: `dbpm_mean`):**

| division | corr | n |
|---|---:|---:|
| Central | 0.666632 | 132 |
| Atlantic | 0.615865 | 128 |
| Pacific | 0.602425 | 128 |
| Southeast | 0.589976 | 100 |
| Southwest | 0.587661 | 100 |
| Northwest | 0.584067 | 100 |
| Midwest | 0.541882 | 28 |

**Playoffs vs Non-Playoffs (top metric: `dbpm_mean`):**

| made_playoffs | mean | median | count |
|---|---:|---:|---:|
| False | -0.455495 | -0.45 | 327 |
| True  |  0.244665 |  0.20 | 389 |

Teams that reached the postseason had substantially higher role-player DBPM on average than those that missed the playoffs.

---

## Why It Matters

This supports the project hypothesis: teams with stronger contributions from role players (quiet stars) achieve higher end-of-season standings. In particular, deeper defensive contributions from role players (higher DBPM) align with higher win percentages and increase likelihood of making the playoffs. Role-player depth isn’t just about filling minutes; it raises the team’s defensive floor and stabilizes performance over the season across conferences and divisions.

---

- **Outputs:**
  - Aggregated role depth by team-season — `Data/Insights/Insight_6_role_depth_by_team_season.csv`

  - Correlation table of role-depth metrics vs `win_pct` — `Data/Insights/Insight_6_correlations.csv`
  
  - Conference correlation table for `dbpm_mean` — `Data/Insights/Insight_6_dbpm_mean_conference_correlations.csv`  
  
  - Division correlation table for `dbpm_mean` — `Data/Insights/Insight_6_dbpm_mean_division_correlations.csv`  
  
  - Playoff vs non-playoff summary for `dbpm_mean` — `Data/Insights/Insight_6_dbpm_mean_playoff_comparison.csv`  
  

