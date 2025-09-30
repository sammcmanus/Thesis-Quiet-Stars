# 🏀 Thesis: Quiet Stars – INFO-I 492

The project, Quiet Stars, analyzes NBA player and team performance using historical datasets. It integrates per-game stats, advanced metrics, and team summaries to clean, analyze, and model basketball performance trends.

## Hypothesis Statement:
Teams with deeper, more efficient benches finish with higher win percentages and better seeds than teams that lean heavily on a few high-usage or very young players.

# Contents

* [Data Sources](#public-dataset)
* [Data Cleaning](#data-cleaning)
    * [Row Filtering](#row-filtering)
    * [Column Standardization](#column-standardization)
    * [Missing values](#missing-values)
    * [Merge](#merge)
    * [Rounding](#rounding)
    * [Derived fields](#derived-fields)
    * [Row exclusion after labeling](#row-exclusion-after-labeling)
    * [Output Files](#output-files)
    * [Insight 2 Data Prep](#insight-2-data-prep)
    * [Columns Used By Table](#columns-used-by-table)
    * [Notes & Implications](#notes--implications)
* [Insight Summaries](#insight-summaries)
    * [#1: Defensive Metrics and How They Support Team Success](#1-defensive-metrics-and-how-they-support-team-success)
    * [#2: Role Player Efficiency and How It Supports Team Success](#2-role-player-efficiency-and-how-it-supports-team-success)
    * [#3: Player Efficiency and Its Correlation to Experience](#3-player-efficiency-and-its-correlation-to-experience)
* [Change Log](#change-log)
* [Project Timeline](Docs/Project_Timeline.md)

<BR>

## Data Sources

| File                     | What it contains (short)                                                                |
| ------------------------ | --------------------------------------------------------------------------------------- |
| `Advanced.csv`           | Advanced player metrics by season/team: TS%, USG%, WS, OBPM/DBPM, BPM, etc.             |
| `Player Per Game.csv`    | Per-game box stats by player/season/team: MP, FG/3P/FT, REB, AST, STL, BLK, TOV, PTS.   |
| `Player Career Info.csv` | Player bio/metadata: birthdate, height, weight, college, draft, position.               |
| `Team Summaries.csv`     | Team-season rollups: wins/losses, pace, ratings, shooting/rebounding rates, attendance. |

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

## Missing values

    Player Per Game: all columns are fillna(0) (Setting any missing percentages, rates, and counts in the per-game table to 0)

<BR>

## Merge
    Merge to one player-team-season table

    Keep only the columns below, then inner-join on ["season","player_id","abv"]:

    From Advanced: season, player_id, abv, per, ts_percent, obpm, dbpm, usg_percent, gs, g

    From Player Per Game: season, player_id, abv, ast_per_game, tov_per_game, mp_per_game

    From Team Summaries: season, abv, w, l, playoffs

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
| `Advanced.csv`             | season, player_id, abv, per, ts_percent, obpm, dbpm, usg_percent, gs, g                 |
| `Player Per Game.csv`      | season, player_id, abv, ast_per_game, tov_per_game, mp_per_game                         |
| `Team Summaries.csv`       | season, abv, w, l, playoffs                                                             |
| `Player Career Info.csv`   | player_id, from                                                                         |    

<BR><BR>

## Output Files

| File                          | Purpose                                                                               |
| ----------------------------- | ------------------------------------------------------------------------------------- |
| `player_stats_cleaned.csv`    | Provide a clean flattened data soure to use for data insights.                        |
| `top_half.csv`                | Results of insight 2 data prep output, this is the data for role players by top 50% of each <BR> season teams by win percentage.                                                                                                             |
| `bottom_half.csv`             | Results of insight 2 data prep output, this is the data for role players by bottom 50% of each <BR> season teams by win percentage.             

<BR><BR>

## Notes & Implications
    
    Excluding the shortened seasons 2020 & 2021 that was caused by covid.
    
    Multi-team seasons: For players traded mid-season, their stats are aggregated on a per-team basis. This means a player will have a separate record for each team they played on within the same season.

    Blanket fillna(0) on Player Per Game: this sets any missing per-game fields (including percent/rate fields) to zero. This is intentional per code; call it out here to avoid confusion.

    A/T ratio when TO=0: the code sets a2t_perc to 0 when tov_per_game == 0 or ast_per_game == 0, this avoids divide-by-zero.


<BR><BR>

# Insight Summaries

<BR>

## #1: Defensive Metrics and How They Support Team Success

    Goal: Show if teams with better defensive performance, particularly from bench role players, better end-of-season standings, emphasizing the defensive contributions of “quiet stars.”

    DBPM (Defensive Box Plus-Minus) is a statistic that measures a player's defensive impact per 100 possessions in basketball. A higher DBPM means a player contributes more to their team's defense, like preventing opponents from scoring.Insight 

<BR>

## #2: Role Player Efficiency and How It Supports Team Success

    Goal: Show that teams with more efficient role players have higher win percentages, emphasizing the efficiency of “quiet stars” in offensive and defensive contributions.

    Player Effiency Rating (PER) is a per-minute rating that quantifies a player's performance by combining various box score statistics, such as points, rebounds, assists, steals, blocks, turnovers, and shooting efficiency, into a single value. It is normalized so that the league average PER is 15.0, with higher values indicating better performance.

<BR>

## #3: Player Efficiency and Its Correlation to Experience

    Goal: Quantify how veteran NBA players with 7+ years of experience demonstrate higher efficiency compared to less experienced players, highlighting their value to team success through optimized roles and production.

<BR>

## Change Log

    1.0 — Initial Transition from Kaggle
    1.1 — Initial Documentation
    