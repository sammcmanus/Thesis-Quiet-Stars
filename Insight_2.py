import os
import matplotlib.pyplot as plt
import pandas as pd

# Set your working directory here

set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

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

    # Filter for 2023-24 season
    #role_player_stats_playoffs = role_player_stats[role_player_stats['season'] == 2023]
    #role_player_stats_no_playoffs = role_player_stats[role_player_stats['season'] == 2023]
    #playoff_teams = role_player_stats[(role_player_stats['team_win_perc'] >= .6) & (role_player_stats['season'] == 2025)]
    #non_playoff_teams = role_player_stats[(role_player_stats['team_win_perc'] < .6) & (role_player_stats['season'] == 2025)]

    # Sort by season + win percentage
    sorted_df = role_player_stats.sort_values(["season", "team_win_perc"], ascending=[True, False])

    # Rank teams within each season
    sorted_df["rank"] = sorted_df.groupby("season")["team_win_perc"].rank(method="first", ascending=False)

    # Count teams per season
    team_counts = sorted_df.groupby("season")["team_win_perc"].transform("count")

    # Split into top half and bottom half
    top_half = sorted_df[sorted_df["rank"] <= team_counts / 2].copy()
    bottom_half = sorted_df[sorted_df["rank"] > team_counts / 2].copy()


def insight_2_Top_Half():
    # Create PER buckets
    bins = [0, 10, 15, 20]  # adjust ranges as needed
    labels = [" > 10","10 to 15", "15+"]

    # Safe assignment with .loc
    top_half.loc[:, "per_bucket"] = pd.cut(top_half["per"], bins=bins, labels=labels)

    # Count teams per bucket
    bucketed = top_half.groupby("per_bucket", observed=True).size().reset_index(name="team_count")

    # Plot with labels
    fig, ax = plt.subplots()
    bars = ax.bar(bucketed["per_bucket"], bucketed["team_count"], color="orange")
    ax.set_title("Top Half Teams Avg. Role Player Effiency")
    ax.set_xlabel("Role Player Effiency Buckets")
    ax.set_ylabel("Number of Teams")
    ax.bar_label(bars, fmt='{:,.0f}')

    plt.tight_layout()
    plt.grid(axis="y")
    plt.show()

def insight_2_Bottom_Half():
    # Create PER buckets
    bins = [0, 10, 15, 20]  # adjust ranges as needed
    labels = [" > 10","10 to 15", "15+"]

    # Safe assignment with .loc
    bottom_half.loc[:, "per_bucket"] = pd.cut(bottom_half["per"], bins=bins, labels=labels)

    # Count teams per bucket
    bucketed = bottom_half.groupby("per_bucket", observed=True).size().reset_index(name="team_count")

    # Plot with labels
    fig, ax = plt.subplots()
    bars = ax.bar(bucketed["per_bucket"], bucketed["team_count"], color="steelblue")
    ax.set_title("Bottom Half Teams Avg. Role Player Effiency")
    ax.set_xlabel("Role Player Effiency Buckets")
    ax.set_ylabel("Number of Teams")
    ax.bar_label(bars, fmt='{:,.0f}')

    plt.tight_layout()
    plt.grid(axis="y")
    plt.show()

if __name__ == "__main__":
    os.chdir(set_working_dir)
    insight_2_data_prep()
    insight_2_Top_Half()
    insight_2_Bottom_Half()
    