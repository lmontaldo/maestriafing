import sys
import os

# Append the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, PKL_TRANSF_DATA_PATH
import pandas as pd
from utils.remove_outliers import *

def outliers_removal(df):
    for col in df.columns:
        df[col] = remove_outliers(df[col])
    return df



def main():
    fred = pd.read_pickle(PKL_TRANSF_DATA_PATH)
    df_cleaned = fred.applymap(remove_outliers)
    df_cleaned = df_cleaned.interpolate(method='time')
    output_path = os.path.join(DATA_DIR, "outliers_removed.pkl")
    df_cleaned.to_pickle(output_path)
    # remainding outliers from the cleaned data
    print(df_cleaned.head())
    na_counts = df_cleaned.isna().sum()
    na_counts_sorted = na_counts.sort_values(ascending=False)
    columns_with_na = na_counts_sorted[na_counts_sorted > 0]
    print("Columns with NaN values (Descending Order of NaN Counts):")
    print(columns_with_na[0:10])

if __name__ == "__main__":
    main()

    
        
        
    
    

