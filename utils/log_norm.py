import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np

def transform_log1(df):
    """
    Applies the log1p transformation to all series in the dataframe.
    Returns:
    - pd.DataFrame: Transformed dataframe with the log1p applied.
    """
    return np.log1p(df)

def normalization(df):
    """
    Applies z-normalization to all series in the dataframe using StandardScaler.
    Returns:
    - pd.DataFrame: Transformed dataframe with z-normalization applied.
    """
    scaler = StandardScaler()
    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
