# 🏀 Thesis: Quiet Stars – INFO-I 492

The project, Quiet Stars, analyzes NBA player and team performance using historical datasets. It integrates per-game stats, advanced metrics, and team summaries to clean, analyze, and model basketball performance trends.

## Hypothesis Statement:
Teams with deeper, more efficient benches finish with higher win percentages and better seeds than teams that lean heavily on a few high-usage or very young players.

### 📚 Table of Contents

- **[Data Sources](#data-sources)**
- **[Terminology Definitions](Docs/Terminology_Definition.md)**
- **[Data Cleaning](#data-cleaning)**
  - [Row Filtering](#row-filtering)
  - [Column Standardization](#column-standardization)
  - [Impute Values](#impute-values)
  - [Merge](#merge)
  - [Rounding](#rounding)
  - [Derived Fields](#derived-fields)
  - [Row Exclusion After Labeling](#row-exclusion-after-labeling)
  - [Output Files](#output-files)
  - [Insight 2 Data Prep](#insight-2-data-prep)
  - [Columns Used by Table](#columns-used-by-table)
  - [Notes & Implications](#notes--implications)
- **[Insight Summaries]()**
  - [Insight #1: Defensive Metrics and Team Success](Docs/Insight_1.md)
  - [Insight #2: Role Player Efficiency and Team Success](Docs/Insight_2.md)
  - [Insight #3: Player Efficiency and Experience](Docs/Insight_3.md)
  - [Insight #4: Role Player Versatility and Offensive Efficiency](Docs/Insight_4.md)
  - [Insight #5: Bench Strength and End-of-Season Standings](Docs/Insight_5.md)
  - [Insight #6: Role Player Depth and End-of-Season Standings](Docs/Insight_6.md)
- **[Insight Outputs](#insight-output-files)**
- **[Status Log](Docs/Status_Log.md)**
- **[Project Timeline](Docs/Project_Timeline.md)**


<BR>

## Data Sources

| File                     | What it contains (short)                                                                |
| ------------------------ | --------------------------------------------------------------------------------------- |
| `Advanced.csv`           | Advanced player metrics by season/team: TS%, USG%, WS, OBPM/DBPM, BPM, etc.             |
| `Player Per Game.csv`    | Per-game box stats by player/season/team: MP, FG/3P/FT, REB, AST, STL, BLK, TOV, PTS.   |
| `Player Career Info.csv` | Player bio/metadata: birthdate, height, weight, college, draft, position.               |
| `Team Summaries.csv`     | Team-season rollups: wins/losses, pace, ratings, shooting/rebounding rates, attendance. |
| `NBA Teams.csv`          | Team conference and division by season. |

Data Source Link: <a href="https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats">Kaggle – NBA/ABA/BAA Stats (1947-present)</a>

<BR>

# Data Cleaning

<BR>

## Row filtering 

    Keep NBA only: lg == 'NBA'.

    Keep seasons between 2000 and 2025, excluding 2020 and 2021 (due to covid years)

    Drop teams named "2TM" (These represent such as All-Star teams)

    Drop league summary rows: Team Summaries.team != 'League Average'.

<BR>

## Column Standardization

    Rename team columns to a common key abv:

        Advanced.team → abv

        Player Per Game.team → abv

        Team Summaries.abbreviation → abv

    Force types:

        Player Per Game.gs → int

        Team Summaries.w → int

        Team Summaries.l → int

        Advanced.season → int

        Player Career Info.from → int

<BR>

## Impute values

    Player Per Game: all columns are fillna(0) (Setting any missing percentages, rates, and counts in the per-game table to 0)

<BR>

## Merge
    Merge to one player-team-season table

    Keep only the columns below, then inner-join on ["season","player_id","abv"]:

    From Advanced: season, player_id, abv, per, ts_percent, obpm, dbpm, usg_percent, gs, g

    From Player Per Game: season, player_id, abv, ast_per_game, tov_per_game, mp_per_game

    From Team Summaries: season, abv, w, l, playoffs

    From NBA Teams: season, abv, conference, division

<BR>

## Rounding

    Round to 2 decimals: per, ts_percent, obpm, dbpm.

<BR>

## Derived fields

    a2t_perc (Assist-to-turnover ratio): ast_per_game / tov_per_game (if either is set to 0 then a2t_perc is 0), rounded to 2 decimals.   

    Team win % team_win_perc = w / (w + l), rounded to 2 decimals.

<BR>

| Role              | classification                                                            |
| ----------------- | --------------------------------------------------------------------------|
| Starter (S)       | Games started ≥ to 50% and minutes played per game ≥ 24.5 minutes         |
| Role Player (R)   | Games played is ≥ 30 and games started < 50% and minutes per game ≥ 15    |
| Bench Player (B)  | Games played between 15 & 30 and minutes per game >= 10                   |
| Insignificant (I) | All others are considered insignificant and are filtered out.             |

<BR>

    Experience (seasons in league):

    Merge career_info[['player_id','from']] (first season) on player_id (inner).

    experience = season - from (year entered league)

    Drop the temporary from column.

<BR>

## Row exclusion after labeling

    Remove players with role == 'I' (insignificant).

<BR>

## Insight 2 Data Prep

    Input: Data/Processed/player_stats_cleaned.csv

    Keep Role players only: role == 'R'.

    Group by (season, abv) and compute means of: playoffs, per, obpm, dbpm, team_win_perc

    Rename abv → team; round per, obpm, dbpm to 2 decimals.

    Rank teams within each season by team_win_perc (descending).

    Split into top_half and bottom_half by median rank count per season.

    Output:
    Data/Processed/top_half.csv
    Data/Processed/bottom_half.csv

<BR>

## Columns Used By Table

| File                       | Columns Used                                                                            |
| ------------------------   | --------------------------------------------------------------------------------------- |
| `Advanced.csv`             | season, player_id, abv, per, ts_percent, obpm, dbpm, usg_percent, gs, g, mp             |
| `Player Per Game.csv`      | season, player_id, abv, ast_per_game, tov_per_game, mp_per_game                         |
| `Team Summaries.csv`       | season, abv, w, l, playoffs                                                             |
| `Player Career Info.csv`   | player_id, from                                                                         |
| `NBA Teams.csv`            | season, abv, conference, division                                                       |

<BR><BR>

## Output Processed Files

| File                          | Purpose                                                                               |
| ----------------------------- | ------------------------------------------------------------------------------------- |
| `player_stats_cleaned.csv`    | Provide a clean flattened data soure to use for data insights.                        |
| `team_results.csv`            | Provide a clean flattened data soure to use for data insights.                        |
| `top_half.csv`                | Results of insight 2 data prep output, this is the data for role players by top 50% of each <BR> season teams by win percentage.                                                                                                             |
| `bottom_half.csv`             | Results of insight 2 data prep output, this is the data for role players by bottom 50% of each <BR> season teams by win percentage.                                                                                                         |

<BR><BR>

## Insight Output Files

| File                                              | Purpose |
| ------------------------------------------------- | ------- |
| `Insight_1_Starters_DBPM_WINS.png`                | Scatterplot of **Starters** DBPM vs team wins; visual evidence of defensive impact on success. |
| `Insight_1_Role_DBPM_WINS.png`                    | Scatterplot of **Role Players** DBPM vs team wins; supports “quiet stars” hypothesis. |
| `Insight_1_Bench_DBPM_WINS.png`                   | Scatterplot of **Bench** DBPM vs team wins; contextualizes depth contributions. |
| `Insight_2_Top_Half.png`                          | Visualization of role-player efficiency for teams in the **top 50%** of win percentage by season.|
| `Insight_2_Bottom_Half.png`                       | Visualization of role-player efficiency for teams in the **bottom 50%** of win percentage by season.|
| `Insight_3_overall_vets_v_nonvet.csv`             | Summary of veterans (≥7 yrs) vs non-veterans (<7 yrs) across key performance metrics (PER, TS%, DBPM, USG%). Includes both simple and minutes-weighted averages to compare group efficiency. |
| `Insight_3_by_role_and_vet.csv`                   | Efficiency summary broken down by role (Starter, Role, Bench) and veteran status. Shows how experience affects performance within each player category using PER, TS%, DBPM, and usage metrics. |
| `Insight_4_overall_results.csv`                   | Summary table for **role players (USG 10–15)** showing metric distribution and correlations with team win%. |
| `Insight_4_RP_TS_WINS.png`                        | Scatter + fit: **True Shooting % (TS%)** vs **Team Win%** for role players. |
| `Insight_4_RP_A2T_WINS.png`                       | Scatter + fit: **Assist-to-Turnover Ratio (A2T)** vs **Team Win%** for role players. |
| `Insight_5_role_rvs_corr_vs_winpct.csv`           | Two-row table (Role, Bench) with Pearson correlation between role-group RVS and team win%.|
| `Insight_5_role_rvs_top_vs_bottom_gap.csv`	    | Summary of top vs bottom RVS quartile average win% for Role and Bench, plus the Q4–Q1 gap and count. |
| `Insight_6_role_depth_by_team_season.csv`         | Team-season aggregates of role-player depth (R-only): simple means & minutes-weighted means for per, ts_percent, obpm, dbpm, usg_percent, a2t_perc; plus role_mp_total, role_gs_total, role_count, made_playoffs.|
| `Insight_6_correlations.csv`	                    | Correlation coefficients between each role-depth metric and win_pct (league-wide). |
| `Insight_6_dbpm_mean_conference_correlations.csv` | Correlation of the top metric (dbpm_mean) with win_pct by conference. |
| `Insight_6_dbpm_mean_division_correlations.csv`   | Correlation of the top metric (dbpm_mean) with win_pct by division.
| `Insight_6_dbpm_mean_playoff_comparison.csv`	    | Playoff vs Non-Playoff summary (mean/median/count) of the top metric (dbpm_mean).

<br><br>


## Notes & Implications
    
    Excluding the shortened seasons 2020 & 2021 that was caused by covid.
    
    Multi-team seasons: For players traded mid-season, their stats are aggregated on a per-team basis. This means a player will have a separate record for each team they played on within the same season.

    Blanket fillna(0) on Player Per Game: this sets any missing per-game fields (including percent/rate fields) to zero. This is intentional per code; call it out here to avoid confusion.

    A/T ratio when TO=0: the code sets a2t_perc to 0 when tov_per_game == 0 or ast_per_game == 0, this avoids divide-by-zero.




