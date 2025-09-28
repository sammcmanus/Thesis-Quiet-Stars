
import os
import matplotlib.pyplot as plt
import pandas as pd

# Set your working directory here
set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_1_Load_Data():
    global player_stats_DF
    player_stats_DF = pd.read_csv("Data\Processed\player_stats_cleaned.csv")

def insight_1_Starters():
    # Starters
    plt.scatter(player_stats_DF.loc[player_stats_DF["role"] == "S", "dbpm"],
                player_stats_DF.loc[player_stats_DF["role"] == "S", "w"], 
                color='Red', 
                alpha=0.4)

    plt.title('Starters DBPM and Wins')
    plt.xlabel('DBPM')
    plt.ylabel('Wins')

    plt.grid(True)
    plt.show()

def insight_1_Role():
    # Role Players
    plt.scatter(player_stats_DF.loc[player_stats_DF["role"] == "R", "dbpm"],
                player_stats_DF.loc[player_stats_DF["role"] == "R", "w"], 
                color='green', 
                alpha=0.4)
    plt.title('Role Players DBPM and Wins')
    plt.xlabel('DBPM')
    plt.ylabel('Wins')

    plt.grid(True)
    plt.show()

def insight_1_Bench():
    # Bench Players
    plt.scatter(player_stats_DF.loc[player_stats_DF["role"] == "B", "dbpm"],
                player_stats_DF.loc[player_stats_DF["role"] == "B", "w"], 
                color='blue', 
                alpha=0.4)
    plt.title('Bench Players DBPM and Wins')

    plt.xlabel('DBPM')
    plt.ylabel('Wins')

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    os.chdir(set_working_dir)
    insight_1_Load_Data()
    insight_1_Starters()
    insight_1_Role()
    insight_1_Bench()
    