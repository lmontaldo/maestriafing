

import pandas as pd
from scipy.stats import *
import numpy as np


def validate_df(df):
    # Check if there is exactly one datetime64[ns] column
    datetime_columns = df.select_dtypes(include=['datetime64[ns]']).columns
    if len(datetime_columns) != 1:
        return False, 'DataFrame must contain exactly one datetime64[ns] column'
    
    # Check if all other columns are float64
    non_datetime_columns = df.columns.difference(datetime_columns)
    non_float_columns = df[non_datetime_columns].select_dtypes(exclude=['float64']).columns
    if len(non_float_columns) > 0:
        return False, 'All columns other than the datetime64[ns] column must be float64'
    
    return True, 'DataFrame is valid: contains 1 datetime64[ns] column and all other columns are float64'
def validate_format(df):
    # Check the number of columns
    if df.shape[1] < 2:
        return 'Cannot determine format from a single column'
    
    # Check the data types of the columns
    dtypes = df.dtypes
    
    # If there is exactly one non-numeric column, assume the DataFrame is in wide format
    if (dtypes != 'object').sum() == df.shape[1] - 1:
        return 'wide'
    
    # If there are multiple non-numeric columns, assume the DataFrame is in long format
    return 'long'