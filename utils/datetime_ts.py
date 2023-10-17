

import pandas as pd
def set_datetime_to_monthly(pickle_file_path: str) -> pd.DataFrame:
    # 1. Read the pickle file into a DataFrame
    df = pd.read_pickle(pickle_file_path)

    # 2. Convert the first column to a datetime type with monthly frequency
    first_col_name = df.columns[0]
    df[first_col_name] = pd.to_datetime(df[first_col_name], format='%Y-%m-%d')

    return df