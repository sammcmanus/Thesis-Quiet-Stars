
import os
import matplotlib.pyplot as plt
import pandas as pd

# Set your working directory here
set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"

def insight_1_Load_Data():
    global player_stats_DF
    
    player_stats_DF = pd.read_csv("Data/Processed/player_stats_cleaned.csv")


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
    plt.savefig('img/Insight_1_Starters_DBPM_WINS.png')
    plt.close()

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
    plt.savefig('img/Insight_1_Role_DBPM_WINS.png')
    plt.close()

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
    plt.savefig('img/Insight_1_Bench_DBPM_WINS.png')
    plt.close()

def insight_1_Correlation():

    # Calculate correlation between DBPM and Wins by player role
    roles = {
        "S": "Starters",
        "R": "Role Players",
        "B": "Bench Players"
    }
    
    corr_results = []
    
    # Loop through each role and calculate correlation
    for code, name in roles.items():
        subset = player_stats_DF.loc[player_stats_DF["role"] == code]
        corr = subset["dbpm"].corr(subset["w"])
        corr_results.append({"Role": name, "Correlation": round(corr, 3)})
        
    corr_df = pd.DataFrame(corr_results).set_index("Role")

    print("\nCorrelation between DBPM and Wins by Role:\n")
    print(corr_df)


def insight_1_DBPM_Buckets():
    # Group players into DBPM buckets and calculate average team wins by role
    
    bins = [-10, -2, 0, 2, 10]
    labels = ['<-2', '-2 to 0', '0 to 2', '2+']

    roles = {
        "S": "Starters",
        "R": "Role Players",
        "B": "Bench Players"
    }

    bucket_results = []

    for code, name in roles.items():
        subset = player_stats_DF.loc[player_stats_DF["role"] == code].copy()
        subset["DBPM_bucket"] = pd.cut(subset["dbpm"], bins=bins, labels=labels, include_lowest=True)

        bucket_avg = subset.groupby("DBPM_bucket", observed=False)["w"].mean().round(2)

        bucket_results.append(bucket_avg.rename(name))

        results_df = pd.concat(bucket_results, axis=1)

    print("\nAverage Wins by DBPM Bucket and Role:\n")
    print(results_df)



if __name__ == "__main__":
    os.chdir(set_working_dir)
    insight_1_Load_Data()
    insight_1_Starters()
    insight_1_Role()
    insight_1_Bench()
    insight_1_Correlation()
    insight_1_DBPM_Buckets()
    