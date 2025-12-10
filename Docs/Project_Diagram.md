flowchart TD

  subgraph Raw_Data["Raw Data (Data/Raw)"]
    A[Advanced.csv]
    B[Player Per Game.csv]
    C[Team Summaries.csv]
    D[Player Career Info.csv]
    E[NBA Teams.csv]
  end

  subgraph Processing
    P[Process_Raw_Data.py]
  end

  subgraph Processed_Data["Processed Data (Data/Processed)"]
    PS[player_stats_cleaned.csv]
    TR[team_results.csv]
    TH[top_half.csv]
    BH[bottom_half.csv]
  end

  subgraph Insights
    I1[Insight_1.py]
    I2[Insight_2.py]
    I3[Insight_3.py]
    I4[Insight_4.py]
    I5[Insight_5.py]
    I6[Insight_6.py]
  end

  subgraph Outputs["Insight Outputs (img/ & Data/Processed)"]
    O1[Insight 1 plots & tables]
    O2[Insight 2 plots & tables]
    O3[Insight 3 tables]
    O4[Insight 4 plots & tables]
    O5[Insight 5 tables]
    O6[Insight 6 plots & tables]
  end

  subgraph Orchestration
    R[Run_Pipeline.py]
  end

  Raw_Data --> P --> Processed_Data

  Processed_Data --> I1 --> O1
  Processed_Data --> I2 --> O2
  Processed_Data --> I3 --> O3
  Processed_Data --> I4 --> O4
  Processed_Data --> I5 --> O5
  Processed_Data --> I6 --> O6

  R --> P
  R --> I1
  R --> I2
  R --> I3
  R --> I4
  R --> I5
  R --> I6
