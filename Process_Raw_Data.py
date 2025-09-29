# Set your working directory here
set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

# Library Imports
import os
import numpy as np 
import pandas as pd
from copy import deepcopy
#from pathlib import Path


# Load Datasets
def load_clean_export():
    global player_stats_DF
    advanced = pd.read_csv("Data\Raw\Advanced.csv")
    per_game = pd.read_csv("Data\Raw\Player Per Game.csv")
    team_summaries = pd.read_csv("Data\Raw\Team Summaries.csv")
    career_info = pd.read_csv("Data\Raw\Player Career Info.csv")

# Data Cleaning and Preparation
    # Filtering out:
    # - Non-NBA leagues
    # - Seasons before 2000 and the 2020 & 2021 seasons
    # - Non-seasonal/team entries (e.g., League Leaders, All-Star teams)

    advanced_df_sub = deepcopy(advanced.loc[(advanced['lg'] == 'NBA') & (advanced['season'] >= 2000) & ~advanced['season'].isin([2020, 2021]) & ~(advanced['team'] == '2TM')])
    ppg_df_sub = deepcopy(per_game.loc[(per_game['lg'] == 'NBA') & (per_game['season'] >= 2000) & ~per_game['season'].isin([2020, 2021]) & ~(per_game['team'] == '2TM')])
    ts_df_sub = deepcopy(team_summaries.loc[(team_summaries['lg'] == 'NBA') & (team_summaries['season'] >= 2000) & ~team_summaries['season'].isin([2020, 2021]) & ~(team_summaries['abbreviation'] == '2TM') & ~(team_summaries['team'] == 'League Average')])

    # Standardize team abbreviation column names by renaming to 'abv'

    advanced_df_sub = advanced_df_sub.rename(columns={"team": "abv"})
    ppg_df_sub = ppg_df_sub.rename(columns={"team":"abv"})
    ts_df_sub = ts_df_sub.rename(columns={"abbreviation":"abv"})

    # Converting columns to correct data type.

    ppg_df_sub['gs'] = ppg_df_sub['gs'].astype(int)
    ts_df_sub['w'] = ts_df_sub['w'].astype(int)
    ts_df_sub['l'] = ts_df_sub['l'].astype(int)

    # Populate NaN values with 0 for the following columns as they are percentage fields that did no get calcualted due to the
    # the fields they are calculated from are 0. 
    # Columns being set to 0: fg_percent, x3p_percent, x2p_percent, e_fg_percent, ft_percent
    # ppg_df_sub.isna().sum()  

    ppg_df_sub = ppg_df_sub.fillna(0)

    # Combine nessecary states from team summary, advanced, and per-game stats into a single DataFrame for insights

    # Select only the needed columns from each DataFrame
    advanced_cols = ["season", "player_id", "abv", "per", "ts_percent", "obpm", "dbpm", "usg_percent", "gs", "g"]
    ppg_cols = ["season", "player_id", "abv", "ast_per_game", "tov_per_game", "mp_per_game"]
    ts_cols = ["season", "abv", "w", "l", "playoffs"]

    # Merge DataFrames
    player_stats_DF = (
        advanced_df_sub[advanced_cols]
        .merge(ppg_df_sub[ppg_cols], on=["season", "player_id", "abv"], how="inner")
        .merge(ts_df_sub[ts_cols], on=["season", "abv"], how="inner")
    )

    # Rounding pecents to 2 decimal places.
    player_stats_DF["per"] = player_stats_DF["per"].round(2)
    player_stats_DF["ts_percent"] = player_stats_DF["ts_percent"].round(2)
    player_stats_DF["obpm"] = player_stats_DF["obpm"].round(2)
    player_stats_DF["dbpm"] = player_stats_DF["dbpm"].round(2)

    # Calculate key player metrics:

    # - 'a2t_perc': Assist-to-turnover ratio, set to 0 if AST or TO is 0
    player_stats_DF["a2t_perc"] = np.where(
        (player_stats_DF["ast_per_game"] == 0) | (player_stats_DF["tov_per_game"] == 0),
        0,
        (player_stats_DF["ast_per_game"] / player_stats_DF["tov_per_game"]).round(2)
    )

    # - 'team_win_perc': Team win percentage while player was on the team
    player_stats_DF["team_win_perc"] = (player_stats_DF["w"] / (player_stats_DF["w"] + player_stats_DF["l"])).round(2)

    # - 'Role': Classify player as Starter ('S'), Role player ('R'), Bench ('B'), Insignificant ('I')
    #   based on games started, total games played, and minutes per game
    player_stats_DF["role"] = np.select(
        [
            (player_stats_DF["gs"] / player_stats_DF["g"] >= 0.5) & (player_stats_DF["mp_per_game"] >= 24.5),
            (player_stats_DF["g"] >= 30) & (player_stats_DF["gs"] / player_stats_DF["g"] < 0.5) & (player_stats_DF["mp_per_game"] >= 15),
            (player_stats_DF["g"] >= 15) & (player_stats_DF["mp_per_game"] < 24.5),
        ],
        ["S", "R", "B"],
        default="I"
    )

    # Merge 'from' (Year of First Season) from career_info on player_id
    player_stats_DF = player_stats_DF.merge(
        career_info[['player_id', 'from']], 
        on='player_id', 
        how='inner'
    )
    # Convert columns to int to calculate
    player_stats_DF['season'] = player_stats_DF['season'].astype(int)
    player_stats_DF['from'] = player_stats_DF['from'].astype(int)

    # Calculate experience as the number of seasons played
    player_stats_DF['experience'] = player_stats_DF['season'] - player_stats_DF['from']

    # Drop the 'from' column as it's no longer needed
    player_stats_DF = player_stats_DF.drop(columns=['from'])

    # Remove players with insignificant game time
    # These are marked with Role 'I' in player_stats_DF
    player_stats_DF = player_stats_DF[player_stats_DF["role"] != "I"]


    # Save the cleaned and processed DataFrame to a new CSV file
    player_stats_DF.to_csv("Data/Processed/player_stats_cleaned.csv", index=False)

def insight_2_data_prep():
    global top_half, bottom_half

    player_stats_DF = pd.read_csv("Data\Processed\player_stats_cleaned.csv")

    # Getting role players
    role_players = player_stats_DF[player_stats_DF["role"] == "R"]

    # Aggregate role player stats by team and season
    role_player_stats = role_players.groupby(['season', 'abv'])[['playoffs', 'per', 'obpm', 'dbpm', 'team_win_perc']].mean().reset_index()

    role_player_stats.columns = ['season', 'team', 'playoffs', 'per', 'obpm', 'dbpm', 'team_win_perc']

    role_player_stats["per"] = role_player_stats["per"].round(2)
    role_player_stats["obpm"] = role_player_stats["obpm"].round(2)
    role_player_stats["dbpm"] = role_player_stats["dbpm"].round(2)

    # Sort by season + win percentage
    sorted_df = role_player_stats.sort_values(["season", "team_win_perc"], ascending=[True, False])

    # Rank teams within each season
    sorted_df["rank"] = sorted_df.groupby("season")["team_win_perc"].rank(method="first", ascending=False)

    # Count teams per season
    team_counts = sorted_df.groupby("season")["team_win_perc"].transform("count")

    # Split into top half and bottom half
    top_half = sorted_df[sorted_df["rank"] <= team_counts / 2].copy()
    bottom_half = sorted_df[sorted_df["rank"] > team_counts / 2].copy()

    # Save the cleaned and processed DataFrame to a new CSV file
    top_half.to_csv("Data/Processed/top_half.csv", index=False)
    bottom_half.to_csv("Data/Processed/bottom_half.csv", index=False)

    
if __name__ == "__main__":
    os.chdir(set_working_dir)
    load_clean_export()
    insight_2_data_prep()
    
    