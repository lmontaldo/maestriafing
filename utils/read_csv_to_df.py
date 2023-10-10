import os
import sys
import pandas as pd

# This gets the directory of the currently executed script.
current_directory = os.path.dirname(os.path.abspath(__file__))

# This gets the parent directory of the current directory, which is the root of your project.
root_directory = os.path.dirname(current_directory)

# Append the root directory to sys.path
sys.path.append(root_directory)

from config import DATA_BASE_PATH , DATA_DIR


def read_csv_to_df(file_path):
    # Read CSV file into a DataFrame
    df = pd.read_csv(file_path)
    df = df.dropna(how='all')
    return df


def transform_dataframe(input_df: pd.DataFrame) -> pd.DataFrame:
    # Extract the first row data (excluding 'sasdate' column if present)
    first_row_data = input_df.iloc[0].drop('sasdate', errors='ignore').values.tolist()

    # Create the new DataFrame using the first row data
    tcodes = pd.DataFrame([first_row_data], columns=input_df.columns.drop('sasdate', errors='ignore'))

    return tcodes

def set_first_column_as_monthly_datetime(input_df: pd.DataFrame) -> pd.DataFrame:
    first_col_name = input_df.columns[0]
    input_df[first_col_name] = pd.to_datetime(input_df[first_col_name], format='%d/%m/%Y')
    return input_df



def main():
    # Define the file path relative to the script's location
    data_file_path = DATA_BASE_PATH 
    
    # Read CSV data into a DataFrame
    df = read_csv_to_df(data_file_path)
    
    # Transform the DataFrame to get the required transf_dfs DataFrame
    tcodes = transform_dataframe(df)
    tcodes = tcodes.T
    tcodes.columns = ['transformations_code'] 
    # Optionally, print the first few rows to check the original data
    df = df.iloc[1:].reset_index(drop=True)
    df = set_first_column_as_monthly_datetime(df)
    
    # Print the transformed DataFrames
    print("\nData fred in ts:\n", df.tail())
    print("\nTransformation codes:\n", tcodes)
    
    # Store the original DataFrame for further processing (either in memory, or to disk)
    # For this example, let's save the DataFrame as a pickle file for later use
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    df.to_pickle(os.path.join(DATA_DIR, "fred_data.pkl"))
    tcodes.to_pickle(os.path.join(DATA_DIR, "tcodes.pkl"))


if __name__ == "__main__":
    main()

