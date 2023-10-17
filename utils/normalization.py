import pandas as pd
from sklearn.preprocessing import StandardScaler

def scale_and_save_to_pickle(input_df, pickle_filename):
    """
    Scale each series in the input DataFrame using StandardScaler and save the scaled DataFrame to a pickle file.

    Args:
        input_df (pd.DataFrame): Input DataFrame with a time index.
        pickle_filename (str): Name of the pickle file to save the scaled DataFrame.
    Returns:
        pd.DataFrame: Scaled DataFrame.
    """
    # Initialize the StandardScaler
    scaler = StandardScaler()

    # Scale each series in the DataFrame
    scaled_data = input_df.copy()
    for col in input_df.columns:
        series = input_df[col].values.reshape(-1, 1)
        scaled_series = scaler.fit_transform(series)
        scaled_data[col] = scaled_series.flatten()

    # Save the scaled DataFrame to a pickle file
    scaled_data.to_pickle(pickle_filename)

    return scaled_data