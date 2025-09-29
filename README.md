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
    * [Output](#output)
    * [Insight 2 Data Prep](#insight-2-data-prep)
    * [Columns Used By Table](#columns-used-by-table)
    * [Notes & Implications](#notes--implications)
* [Insight Summaries](#insight-summaries)
    * [#1: Defensive Metrics and How They Support Team Success](#1-defensive-metrics-and-how-they-support-team-success)
    * [#2: Role Player Efficiency and How It Supports Team Success](#2-role-player-efficiency-and-how-it-supports-team-success)
    * [#3: Player Efficiency and Its Correlation to Experience](#3-player-efficiency-and-its-correlation-to-experience)
* [Change Log](#change-log)

## Data Sources

| File                     | What it contains (short)                                                                |
| ------------------------ | --------------------------------------------------------------------------------------- |
| `Advanced.csv`           | Advanced player metrics by season/team: TS%, USG%, WS, OBPM/DBPM, BPM, etc.             |
| `Player Per Game.csv`    | Per-game box stats by player/season/team: MP, FG/3P/FT, REB, AST, STL, BLK, TOV, PTS.   |
| `Player Career Info.csv` | Player bio/metadata: birthdate, height, weight, college, draft, position.               |
| `Team Summaries.csv`     | Team-season rollups: wins/losses, pace, ratings, shooting/rebounding rates, attendance. |

Data Link: <a href="https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats">Kaggle – NBA/ABA/BAA Stats (1947-present)</a>

<BR><BR>
# <Center>Data Cleaning</Center>
<BR>

## Row filtering 

    Keep NBA only: lg == 'NBA'.

    Keep seasons ≥ 2000, exclude 2020 and 2021 (due to covid years)

    Drop multi-team aggregate rows coded as '2TM':

    Advanced.team != '2TM'

    Player Per Game.team != '2TM'

    Team Summaries.abbreviation != '2TM'

    Drop league summary rows: Team Summaries.team != 'League Average'.

<BR>

## Column Standardization

    Rename team columns to a common key abv:

    Advanced.team → abv

    Player Per Game.team → abv

    Team Summaries.abbreviation → abv

    Force integer types:

    Player Per Game.gs → int

    Team Summaries.w → int

    Team Summaries.l → int

<BR>

## Missing values

    Player Per Game: all columns are fillna(0) (one blanket call on the filtered frame).

    This sets any missing percentages, rates, and counts in the per-game table to 0.

    Other input tables are not filled (left as-is).

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

    Assist-to-turnover ratio a2t_perc

    If ast_per_game == 0 or tov_per_game == 0 → set to 0

    Else a2t_perc = ast_per_game / tov_per_game, rounded to 2 decimals.

    Team win % team_win_perc = w / (w + l), rounded to 2 decimals.

    Role classification role (string in {'S', 'R', 'B', 'I'}):

    Starter 'S': gs/g ≥ 0.5 and mp_per_game ≥ 24.5

    Role 'R': g ≥ 30 and gs/g < 0.5 and mp_per_game ≥ 15

    Bench 'B': g ≥ 15 and mp_per_game < 24.5

    Else: 'I' (insignificant)

    Experience (seasons in league):

    Merge career_info[['player_id','from']] (first season) on player_id (inner).

    experience = season - from (year entered league)

    Drop the temporary from column.

<BR>

## Row exclusion after labeling

    Remove players with role == 'I' (insignificant).

<BR>

## Output

    Write Data/Processed/player_stats_cleaned.csv (no index).

<BR>

## Insight 2 Data Prep

    Input: Data/Processed/player_stats_cleaned.csv

    Keep Role players only: role == 'R'.

    Group by (season, abv) and compute means of:

    playoffs, per, obpm, dbpm, team_win_perc

    Rename abv → team; round per, obpm, dbpm to 2 decimals.

    Rank teams within each season by team_win_perc (descending).

    Split into top_half and bottom_half by median rank count per season.

    Save:

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

## Notes & Implications
    
    Excluding the shortened seasons 2020 & 2021 that was caused by covid.
    
    Multi-team seasons: rows with '2TM' are dropped, so you keep per-team splits and do not use season-total rows. When later aggregating to team-season, a traded player’s impact is naturally isolated to each team stint (no double-counting within a team, but a player can appear for two teams in the same season).

    Blanket fillna(0) on Player Per Game: this sets any missing per-game fields (including percent/rate fields) to zero. That makes downstream code simpler but can understate rates when the true value is “not applicable” rather than 0. (This is intentional per code; call it out here to avoid confusion.)

    A/T ratio when TO=0: the code sets a2t_perc to 0 when tov_per_game == 0 or ast_per_game == 0. This avoids divide-by-zero but treats those cases as zero rather than NaN/∞. Results using A/T should be interpreted with that rule in mind.

    Experience: computed as season - from from Player Career Info.csv after an inner merge (players missing from are implicitly dropped at this step).

<BR><BR>
# <center>Insight Summaries</center>
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
<<<<<<< HEAD
=======

>>>>>>> 2070c0fc11dcd8611baadb5c8cd97d88e9fc08bd
