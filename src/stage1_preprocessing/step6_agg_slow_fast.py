import pandas as pd
import sys
import os
import pickle
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PKL_NORM_PATH = os.path.join(project_root, "data", "prepro", 'data_normalized.pkl')
descriptions_file_path = os.path.join(project_root, "data", "prepro", 'descripciones.txt')
print(descriptions_file_path)

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
# drop aggregates variables
columns_to_drop = descrip.loc[descrip['drop_aggregate_1'] == 1, 'fred']
df.drop(columns=columns_to_drop, inplace=True)
print(f"After dropping columns that are aggregates, the shape of df is {df.shape}.")
# split df in xdata and ydata
xdata = df.drop(columns='FEDFUNDS', axis=1)
print(f"Shape xdata: {xdata.shape}")
print(f"Columns in xdata: {xdata.columns}")
ydata=df['FEDFUNDS']
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


print("\nx_fast shape:")
print(x_fast.shape)
print("x_fast head:")
print(x_fast.head())
# Concatenate x_slow and x_fast horizontally by index to reoder the df
xdata_sf = pd.concat([x_slow, x_fast], axis=1)
print("Datos X_t ordenados para identificacion por slow y fast: ")
print(xdata_sf.head())

PKL_X_SLOW_FAST_PATH = os.path.join(project_root, "data", "prepro", 'x_slow_fast.pkl')
PKL_YDATA_PATH = os.path.join(project_root, "data", "prepro", 'ydata.pkl')
xdata_sf.to_pickle(PKL_X_SLOW_FAST_PATH)
ydata.to_pickle(PKL_YDATA_PATH)






