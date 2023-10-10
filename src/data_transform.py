import sys
import os

# Append the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PKL_RAW_DATA_PATH, PKL_TCODES_PATH
from utils.fred_data_transf import prepare_missing # Import the function

import pandas as pd

def retrieve_and_transform_data():
    # Load data from pkl using the path from config
    fred = pd.read_pickle(PKL_RAW_DATA_PATH)
    print(fred.head())
    fred.set_index('sasdate', inplace=True)
    tcodes = pd.read_pickle(PKL_TCODES_PATH)

    # Call the prepare_missing function from utils
    transformed_data = prepare_missing(fred, tcodes)

    # Define the path to save the resulting DataFrame as a pickle
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'transf_data_fred_conditions.pkl')

    # Save the DataFrame as a pickle file
    transformed_data.to_pickle(output_path)

    return print(transformed_data.index.min(), transformed_data.index.max())

if __name__ == "__main__":
    df_transf = retrieve_and_transform_data()


    

    

    
