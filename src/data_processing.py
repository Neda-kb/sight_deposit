import pandas as pd
import numpy as np
from datetime import datetime
from src.utils import log_current_time

def data_cleaning(df_sight):
    """
    Cleans and filters the df_sight DataFrame.

    """
    df_sight["condition"] = df_sight[""] / 100
    df_sight["Valid_from"] = pd.to_datetime(df_sight["Valid_from"], errors='coerce')
    df_sight["Valid_until"] = pd.to_datetime(df_sight["Valid_until"], errors='coerce')
    df_sight["Valid_from"] = df_sight["GValid_from"].fillna(datetime(1900, 1, 1))
    df_sight["Valid_until"] = df_sight["Valid_until"].fillna(datetime(2262, 4, 11))
    df_sight = df_sight[(df_sight["AUSWDAT"] >= df_sight["Valid_from"]) & (df_sight["AUSWDAT"] <= df_sight["Valid_from"])]
    return df_sight


def gültig_bis_max(df_sight):
    """
    Selects the necessary columns from the DataFrame, groups by them, and calculates the max value for Gültig bis.

    """
    cols_to_group = ["", "", ""]
    cols_to_value = ["Valid until"]
    df_sight_max = df_sight[cols_to_group + cols_to_value].groupby(cols_to_group).max()
    df_sight = pd.merge(left=df_sight, right=df_sight_max.add_suffix("_max"), left_on=cols_to_group, right_index=True, how="left")
    df_sight = df_sight[df_sight["Valid until"] == df_sight["Valid until_max"]]
    return df_sight

def create_double_zero_list(df_sight):
    """
    Creates a double zero list by updating and filtering the DataFrame.

    """
    df_sight["max_condition"] = df_sight.groupby(["", ""])[""].transform('sum')
    df_sight["max_condition_kond"] = df_sight.groupby(["", "", ""])[""].transform('sum')
    df_sight_double_zero=df_sight[df_sight[""]==0]
    df_sight_double_zero=df_sight_double_zero[df_sight_double_zero[""]==""]
    df_sight_double_zero[""]=""
    df_sight=df_sight[df_sight[""]!=0]
    df_sight=pd.concat([df_sight, df_sight_double_zero])
    return df_sight

def adjust_custody_fee(df_sight):
    """
    Adjusts the customer interest rate on the custody fee to be negative.

    """
    cond = (df_sight[""] == "")
    df_sight.loc[cond, ""] = -df_sight[""]
    return df_sight

def set_key_interest_rate(df_sight):
    """
    Sets the key interest rate for specific conditions.

    """
    common_cond = df_sight["interest_rate"].isin(["", "", "", "USD"])
    df_sight.loc[common_cond & (df_sight["condition_description"] == "custody_fee"), "customer_interest"] = \
        np.minimum(df_sight["key_interest_rate"] - df_sight["Zu-/Abschlag"] / 100, 0)
    df_sight.loc[common_cond & (df_sight["condition_description"] == "credit_interest"), "customer_interest"] = \
        np.maximum(df_sight["key_interest_rate"] + df_sight[""] / 100, 0)
    return df_sight

def handle_missing_key(df_sight):
    """
    Handles missing key interest rates.

    """
    common_cond = df_sight["interest_rate"].isin(["", "", "", "USD"])
    missing_leitzinsen = df_sight[(df_sight["key_interest_rate"].isna()) & common_cond]
    missing_leitzinsen = missing_leitzinsen.reset_index(drop=True)
    if not missing_leitzinsen.empty:
        print("!!! Key interest rates are missing!!!")
    return  missing_leitzinsen