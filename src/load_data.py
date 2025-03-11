
import os
import pandas as pd
from datetime import datetime
from src.utils import log_current_time

def load_excel_data(file_path, dtype=None, sheet_name=None, columns=None):
    df = pd.read_excel(file_path, dtype=dtype, sheet_name=sheet_name)
    if columns:
        df = df[columns]
    return df

def historie_sichteinlagen(Historie_Sichteinlagen):
    file_path = os.path.join(Historie_Sichteinlagen)
    columns = ["", "", "", "", ""]
    df = load_excel_data(file_path, dtype={'': str}, sheet_name="", columns=columns)
    df[""] = df[""].apply(lambda x: x[2:12])
    return df


def filter_historie_sichteinlagen(df_sight_history, deal_id, filter_dates):
    df_sight_history_filter = df_sight_history[df_sight_history[''] == deal_id]
    df_sight_history_filter = df_sight_history_filter[df_sight_history_filter[""].isin(filter_dates)]
    return df_sight_history_filter

def konditionen(Konditionen_DM):
    file_path = os.path.join(Konditionen_DM)
    columns = ["", "", "", "", "", "", "", "", "", "", "", ""]
    df = load_excel_data(file_path, dtype={'': str}, sheet_name="", columns=columns)
    return df

def historie_onzins(Historie_ONZins):
    file_path = os.path.join(Historie_ONZins)
    columns = ["", ""]
    df_eur = pd.read_excel(file_path, sheet_name="EUR")
    df_eur.columns = columns
    df_eur['Currency'] = 'EUR'
    df_usd = pd.read_excel(file_path, sheet_name="USD")
    df_usd.columns =columns
    df_usd['Currency'] = 'USD'
    df_usd[""] = df_usd[""] / 100
    df = pd.concat([df_eur, df_usd], axis=0)
    return df

def merge_dataframes(df_sight_history, df_sight_cond, df_onzins):
    df_sight = pd.merge(df_sight_history, df_sight_cond, left_on="", right_on="", how="left")
    df_sight = pd.merge(df_sight, df_onzins, left_on=["", ""], right_on=["", "Currency"], how="left")
    return df_sight

def drop_navalues(df_sight):
    df_sight.dropna(subset=[''], inplace=True)
    return df_sight
