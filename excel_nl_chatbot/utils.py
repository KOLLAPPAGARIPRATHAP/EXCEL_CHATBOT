# utils.py

import pandas as pd
import numpy as np
import re

def clean_column_names(df):
    """
    Clean DataFrame column names:
    - strip spaces
    - convert to lowercase
    - replace spaces with underscores
    - remove special characters
    """
    df.columns = df.columns.str.strip().str.lower()
    df.columns = df.columns.str.replace(r'[^a-zA-Z0-9 ]', '', regex=True)
    df.columns = df.columns.str.replace(' ', '_')
    return df

def infer_column_types(df):
    """
    Infer data types of columns in DataFrame.
    Returns a dict with column name as key and type as string.
    """
    return df.dtypes.apply(lambda x: str(x)).to_dict()

def clean_data_for_display(df):
    """Convert NaN/None values to strings and ensure column names are strings"""
    df = df.copy()
    df.columns = df.columns.map(str)  # ensure column names are strings!
    df = df.fillna('N/A').replace([np.nan, pd.NA, None], 'N/A')
    return df

def safe_serialize_dict(d):
    """Convert dict keys/values to strings and replace NaN with 'N/A'"""
    safe_dict = {}
    for k, v in d.items():
        key_str = str(k)
        try:
            value_str = str(v) if v == v else 'N/A'
        except:
            value_str = 'N/A'
        safe_dict[key_str] = value_str
    return safe_dict
