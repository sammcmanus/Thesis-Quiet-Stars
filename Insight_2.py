import os
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import chi2_contingency

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
    plt.savefig('img/Insight_2_Top_Half.png')
    plt.close()

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
    plt.savefig('img/Insight_2_Bottom_Half.png')
    plt.close()

def insight_2_stats():
    
    # Mean PER comparison
    mean_top = top_half_df["per"].mean()
    mean_bottom = bottom_half_df["per"].mean()

    print("\nMean PER Comparison")
    print(f"Top Half Teams: {mean_top:.2f}")
    print(f"Bottom Half Teams: {mean_bottom:.2f}")

    # Proportion of teams with role player PER > 15
    top_high = (top_half_df["per"] > 15).sum()
    top_total = len(top_half_df)
    bottom_high = (bottom_half_df["per"] > 15).sum()
    bottom_total = len(bottom_half_df)

    # Create contingency table
    table = [[top_high, top_total - top_high],
             [bottom_high, bottom_total - bottom_high]]

    chi2, p, dof, ex = chi2_contingency(table)

    print("\nProportion Test (Chi-Square)")
    print(f"Top Half with PER > 15: {top_high}/{top_total}")
    print(f"Bottom Half with PER > 15: {bottom_high}/{bottom_total}")
    print(f"Chi-Square p-value: {p:.4f}")

    if p < 0.05:
        print("\nResult: Statistically significant difference (p < 0.05).\n")
    else:
        print("\nResult: No statistically significant difference (p >= 0.05).\n")

if __name__ == "__main__":
    os.chdir(set_working_dir)
    insight_2_data_load()
    insight_2_Top_Half()
    insight_2_Bottom_Half()
    insight_2_stats()