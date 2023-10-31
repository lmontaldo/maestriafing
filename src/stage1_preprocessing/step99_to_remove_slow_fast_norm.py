import pandas as pd
import sys
import os
import pickle
from sklearn.decomposition import PCA
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PKL_NORM_PATH = os.path.join(project_root, "data", "prepro", 'data_normalized.pkl')
descriptions_file_path = os.path.join(project_root, "data", "prepro", 'descripciones.txt')


with open(PKL_NORM_PATH, 'rb') as file:
    df = pickle.load(file)
print(df.head())    
#  
descrip = pd.read_csv(descriptions_file_path, sep='\t')
#
def check_columns_in_descrip(df, descrip):
    # Get the column names from df
    df_column_names = df.columns

    # Get the unique values in the 'fred' column of descrip
    descrip_fred_values = descrip['fred'].unique()

    # Check if all column names from df are in descrip's 'fred' column
    missing_columns = set(df_column_names) - set(descrip_fred_values)

    if len(missing_columns) == 0:
        print("All column names from df are in descrip's 'fred' column.")
    else:
        print("The following column names are missing in descrip's 'fred' column:")
        print(list(missing_columns))
        
check_columns_in_descrip(df, descrip)        
df.rename(columns={'IPB51222S': 'IPB51222s', 'HOUTSMW': 'HOUSTMW'}, inplace=True)
# Drop the 'BOGMBASE' column
df.drop(columns='BOGMBASE', inplace=True)    
check_columns_in_descrip(df, descrip)
print(f"After dropping the 'BOGMBASE' column, the shape of df is {df.shape}.")
# split df in xdata and ydata
xdata = df.drop(columns='FEDFUNDS', axis=1)
print(f"Shape xdata: {xdata.shape}")
print(f"Columns in xdata: {xdata.columns}")
rdata=df['FEDFUNDS']
# Filter descrip to keep only 'fred' values that are columns in xdata
valid_fred_values = [col for col in descrip['fred'] if col in xdata.columns]
filtered_descrip = descrip[descrip['fred'].isin(valid_fred_values)]
print(f"Cantidad de filas en filtered_descrip: {filtered_descrip.shape[0]}")
print(f"Cantidad de columns en xdata:{xdata.shape[1]}") 
# Check if xdata.columns are in filtered_descrip["fred"] values
all_columns_in_fred = all(xdata.columns.isin(filtered_descrip["fred"]))
# Print the result
print("All columns in xdata are in filtered_descrip['fred']:")
print(all_columns_in_fred)
# Create empty DataFrames x_slow and x_fast as copies of xdata
x_slow = xdata.copy()
x_fast = xdata.copy()

# Iterate through 'fred' values in filtered_descrip and split columns based on 'slow_1_fast_0'
for index, row in filtered_descrip.iterrows():
    column_name = row['fred']
    is_slow = row['slow_1_fast_0']
    # Check if the column exists in xdata
    if column_name in xdata.columns:
        if is_slow == 1:
            # Remove the column from x_fast if it's slow
            x_fast.drop(columns=column_name, inplace=True)
        else:
            # Remove the column from x_slow if it's fast
            x_slow.drop(columns=column_name, inplace=True)

# Print the resulting DataFrames
print("x_slow shape:")
print(x_slow.shape)
print("x_slow head:")
print(x_slow.head())
column_names_slow = x_slow.columns.tolist()
slow = pd.DataFrame(columns=["slow"])
slow["slow"] = column_names_slow
SLOW_COL_PATH = os.path.join(project_root, "data", "prepro", 'slow_columns.csv')
slow.to_csv(SLOW_COL_PATH, index=False)
print("\nx_fast shape:")
print(x_fast.shape)
print("x_fast head:")
print(x_fast.head())
column_names_fast = x_fast.columns.tolist()
fast = pd.DataFrame(columns=["fast"])
fast["fast"] = column_names_fast
FAST_COL_PATH = os.path.join(project_root, "data", "prepro", 'fast_columns.csv')
fast.to_csv(FAST_COL_PATH, index=False)
# Concatenate x_slow and x_fast horizontally by index to reoder the df
xdata_sf = pd.concat([x_slow, x_fast], axis=1)
ffr_data=rdata.to_frame(name='FEDFUNDS')
print(ffr_data.head())
df_sfr=pd.concat([x_slow, x_fast, ffr_data], axis=1)
print("Datos Y_t=[slow, fast, r] ordenados para identificacion por slow, fast y r: ")
df_sfr_sin_idx=df_sfr.reset_index()
print(df_sfr_sin_idx.head())
print(df_sfr_sin_idx.shape)
print(df_sfr_sin_idx.shape[1])
CSV_Y_PATH = os.path.join(project_root, "data", "prepro", 'sfr.csv')
df_sfr_sin_idx.to_csv(CSV_Y_PATH, index=False)
# pickles
PKL_X_SLOW_PATH = os.path.join(project_root, "data", "prepro", 'x_slow.pkl')
PKL_X_FAST_PATH = os.path.join(project_root, "data", "prepro", 'x_fast.pkl')
PKL_X_SLOW_FAST_PATH = os.path.join(project_root, "data", "prepro", 'x_slow_fast.pkl')
PKL_rDATA_PATH = os.path.join(project_root, "data", "prepro", 'rdata.pkl')
x_slow.to_pickle(PKL_X_SLOW_PATH)
x_fast.to_pickle(PKL_X_FAST_PATH)
xdata_sf.to_pickle(PKL_X_SLOW_FAST_PATH)
rdata.to_pickle(PKL_rDATA_PATH)






