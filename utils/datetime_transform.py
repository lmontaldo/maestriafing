import pandas as pd

def to_datetime_and_set_index(dfs, column):
    """
    Convert the specified column in multiple dataframes to datetime format,
    set that column as the index, and then return the modified dataframes.

    Args:
    - dfs (list of pd.DataFrame): List of dataframes to process
    - column (str): Column name to convert and set as index

    Returns:
    - list of pd.DataFrame: List of modified dataframes
    """
    modified_dfs = []
    for df in dfs:
        df_copy = df.copy()
        df_copy[column] = pd.to_datetime(df_copy[column])
        df_copy.set_index(column, inplace=True)
        modified_dfs.append(df_copy)
    return modified_dfs


