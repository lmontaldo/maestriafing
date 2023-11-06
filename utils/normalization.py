import pandas as pd
from sklearn.preprocessing import StandardScaler

def scale_dataframe(input_df):
    """
    Scale each series in the input DataFrame using StandardScaler.

    Args:
        input_df (pd.DataFrame): Input DataFrame with a time index.

    Returns:
        pd.DataFrame: Scaled DataFrame.
    """
    # Initialize the StandardScaler
    scaler = StandardScaler()

    # Create a new DataFrame for scaled data
    scaled_data = input_df.copy()

    # Scale each series in the DataFrame
    for col in input_df.columns:
        series = input_df[col].values.reshape(-1, 1)
        scaled_series = scaler.fit_transform(series)
        scaled_data[col] = scaled_series.flatten()

    return scaled_data


