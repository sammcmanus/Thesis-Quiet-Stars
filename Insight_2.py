import os
import matplotlib.pyplot as plt
import pandas as pd

# Set your working directory here

set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_2_data_load():
    global top_half_df, bottom_half_df

    top_half_df = pd.read_csv("Data/Processed/top_half.csv")
    bottom_half_df = pd.read_csv("Data/Processed/bottom_half.csv")


def insight_2_Top_Half():
    # Create PER buckets
    bins = [0, 10, 15, 20]  # adjust ranges as needed
    labels = [" > 10","10 to 15", "15+"]

    # Safe assignment with .loc
    top_half_df.loc[:, "per_bucket"] = pd.cut(top_half_df["per"], bins=bins, labels=labels)

    # Count teams per bucket
    bucketed = top_half_df.groupby("per_bucket", observed=True).size().reset_index(name="team_count")

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
    bottom_half_df.loc[:, "per_bucket"] = pd.cut(bottom_half_df["per"], bins=bins, labels=labels)

    # Count teams per bucket
    bucketed = bottom_half_df.groupby("per_bucket", observed=True).size().reset_index(name="team_count")

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
    insight_2_data_load()
    insight_2_Top_Half()
    insight_2_Bottom_Half()
    