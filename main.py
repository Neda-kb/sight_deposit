
import os
import pandas as pd
from datetime import datetime

from src import load_data as ld
from src import data_processing as dp
from src.calculate_NII import calculate_NII
from src.output import template_excel, output
from src.utils import log_current_time


# All input and output pathes
input_path = r''
unterordner_2022 = os.path.join(input_path, '2022','2022.xlsx')
unterordner_2023 = os.path.join(input_path, '2023')
ordner_einlagen = os.path.join(unterordner_2023, '','2023_History.xlsx')
ordner_konditionen = os.path.join(unterordner_2023, 'condition DM',"2023_condition_DM.xlsx")
output_path_ML=r'.\Output\missing.xlsx'
output_path_output_SV= r'.\Output\output_SightDepo_Aggregation.xlsx'
output_path_SF= r'.\Output\output_SightDepo_Final.xlsx'
log_current_time("let\'s go!")

#%%

# Read and Prepare Data

## Read Data from "2024_History.xlsx"
df_sight_history = ld.historie_sichteinlagen(ordner_einlagen)
log_current_time("History of demand deposits read")

## Read Data from "2023_condition_DM.xlsx"
df_sight_cond =ld.konditionen(ordner_konditionen)
log_current_time("Conditions read")

## Read Data from "2022.xlsx"
df_onzins =ld.historie_onzins(unterordner_2022)
if 0.05 < max(abs(df_onzins["key interest rate"].min()), abs(df_onzins["key interest rate"].max())):
    print("!!! Extraordinarily high key interest rates - does the 100 factor for USD still apply?")
log_current_time("raw data read")

## Merge Data
df_sight =ld.merge_dataframes(df_sight_history, df_sight_cond, df_onzins)

## Drop Nan values
df_sight = ld.drop_navalues(df_sight)
log_current_time("Dataframes merged")

#%%

# Process sight data

## Cleans and filters df_sight
df_sight = dp.data_cleaning(df_sight)
## Calculates the max value for Gültig bis
df_sight = dp.gültig_bis_max(df_sight)
## Creates a double zero list
df_sight = dp.create_double_zero_list(df_sight)
##  Adjusts the customer interest rate
df_sight = dp.adjust_custody_fee(df_sight)
## Sets the key interest rate for specific conditions
df_sight = dp.set_key_interest_rate(df_sight)
## Handles missing key interest rates
missing_leitzinsen =dp. handle_missing_key(df_sight)
log_current_time("Data processing completed")
## Export missing key interest rates to Excel
if not missing_leitzinsen.empty:
   template_excel(missing_leitzinsen,output_path_ML, 'missing_Leitzinsen')

#%%

# Calculate Net Interest Income (NII)

df_sight_with_NII = calculate_NII(df_sight)
## Export Data to Excel
template_excel(df_sight_with_NII , output_path_output_SV, 'output_SightDepo_vorAggregation',merge_cells=False)
log_current_time("vorAgg written to Excel")

#%%

# Generate final output
df_sight_final = output(df_sight_with_NII)
template_excel(df_sight_final, output_path_SF, 'output_SightDepo_Final')
log_current_time("Ready")
