import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np

def transform_log1(df, index_column):
    """
    Applies the log1p transformation to all series in the dataframe.
    Args:
    - df (pd.DataFrame): The input dataframe.
    - index_column (str): The column name to set as the index.
    
    Returns:
    - pd.DataFrame: Transformed dataframe with the log1p applied and the specified column set as the index.
    """
    df = df.set_index(index_column)
    log1_df = np.log1p(df)
    return log1_df

def normalization(df, index_column):
    """
    Applies z-normalization to all series in the dataframe using StandardScaler.
    Args:
    - df (pd.DataFrame): The input dataframe.
    - index_column (str): The column name to set as the index.
    
    Returns:
    - pd.DataFrame: Transformed dataframe with z-normalization applied and the specified column set as the index.
    """
    
    # Set the specified column as index and store it
    index_values = df[index_column]
    df = df.drop(columns=[index_column])
    
    scaler = StandardScaler()
    normalized_df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    
    # Add back the index
    normalized_df[index_column] = index_values
    normalized_df = normalized_df.set_index(index_column)
    
    return normalized_df