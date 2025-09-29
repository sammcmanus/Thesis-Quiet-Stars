import os
from Process_Raw_Data import load_clean_export, insight_2_data_prep
from Insight_1 import insight_1_Load_Data, insight_1_Starters, insight_1_Role, insight_1_Bench
from Insight_2 import insight_2_data_load, insight_2_Top_Half, insight_2_Bottom_Half

# Set your working directory here
set_working_dir = "C:\Development\VSCode\Workspace\Github\Thesis-Quiet-Stars"




if __name__ == "__main__":
    os.chdir(set_working_dir)
    load_clean_export()
    insight_2_data_prep()
    
    insight_1_Load_Data()
    insight_1_Starters()
    insight_1_Role()
    insight_1_Bench()

    insight_2_data_load()
    insight_2_Top_Half()
    insight_2_Bottom_Half()


