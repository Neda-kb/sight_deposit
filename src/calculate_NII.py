""
import pandas as pd
import numpy as np
from datetime import datetime
import openpyxl as pyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
import logging
from src.utils import log_current_time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_NII(df_sight):
    """
    Calculates the Net Interest Income (NII) for sight deposits based on specific conditions
    and exports the results to an Excel file.

    """
    # Calculate the maximum amount that can be interest-bearing
    df_sight["max_interest_bearing_amount"] = df_sight["upper limit"] - df_sight["B"]

    # Initialize the interest-bearing amount column
    df_sight[""] = 0

    # Apply conditions for interest-bearing amount
    df_sight.loc[(df_sight[""] >= df_sight[""]) &
                     (df_sight[""] >= df_sight[""]), ""] = df_sight[""]

    df_sight.loc[(df_sight[""] >= df_sight[""]) &
                     (df_sight[""] < df_sight[""]), ""] = df_sight[""] - df_sight[""]

    df_sight.loc[(df_sight[""] < df_sight[""]) &
                     (df_sight[""] < df_sight[""]), ""] = 0

    df_sight.loc[df_sight[""] == "", ""] = df_sight[""]

    # Check interest-bearing amount
    df_sight[""] = df_sight.groupby(["", ""])[""].transform('sum')

    # Calculate NII
    df_sight["NII"] = df_sight[""] * df_sight[""]

    # Export to Excel
    df_sight.reset_index(drop=True, inplace=True)
    log_current_time("NII calculation completed")

    return df_sight
