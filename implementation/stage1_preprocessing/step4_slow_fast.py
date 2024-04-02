import pandas as pd
import sys
import os
import pickle
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#prepro_data_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
imputed_file_path = os.path.join(project_root, "data", "prepro", "imputed_na_fred_data.csv")
descriptions_file_path = os.path.join(project_root, "data", "prepro", 'descripcion_df.csv')
#
df = pd.read_csv(imputed_file_path, sep=",")
df.set_index('date', inplace=True)
print(f'dims df: {df.shape}')
print("Removing columns HOUSTMW, HOUSTS, PERMITMW")
df=df.drop(['HOUSTMW', 'HOUSTS', 'PERMITMW'], axis=1)
print(f'Dims df after removing HOUSTMW, HOUSTS, PERMITMW: {df.shape}') 
list1=list(df.columns)
#df_fred = pd.read_csv(prepro_data_file_path, sep=",", index_col='index'
#  
descrip = pd.read_csv(descriptions_file_path, sep=";")
print(descrip.head())
print(f"descrip shape: {descrip.shape}")
list2=list(descrip['fred'])
def elements_not_in_second(list1, list2):
    # Convert the second list to a set for faster lookups
    set2 = set(list2)

    # Use list comprehension to find elements in list1 not in set2
    result = [element for element in list1 if element not in set2]
    return result

print(elements_not_in_second(list1, list2))
df.drop(columns='BOGMBASE', inplace=True)
list3=list(df.columns) 
print(elements_not_in_second(list3, list2))
print(f"df shape: {df.shape}")
#
xdata=df.drop(columns='FEDFUNDS', axis=1)
print(xdata.shape)
ffrdata=df['FEDFUNDS'].to_frame(name='FEDFUNDS')
#
x_slow = xdata.copy()
print(f"slow: {x_slow.columns.tolist()}")
x_fast = xdata.copy()
print(f"fast: {x_fast.columns.tolist()}")
for index, row in descrip.iterrows():
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
#
new_df = df.drop('FEDFUNDS', axis=1, inplace=False)           
resulting = descrip[descrip['fred'].isin(new_df.columns)]
path_resulting=os.path.join(project_root, "data", "prepro", 'resulting_table.csv')
resulting.to_csv(path_resulting, index=False)
#
df_sfr=pd.concat([x_slow, x_fast, ffrdata], axis=1)
df_sfr_sin_idx=df_sfr.reset_index()
print(f"shape df_sfr_sin_idx: {df_sfr_sin_idx.shape}")
#
'''
CSV_Y_PATH = os.path.join(project_root, "data", "prepro", 'sfr_sin_normalizar.csv')
df_sfr_sin_idx.to_csv(CSV_Y_PATH, index=False)
#    
list_slow=list(x_slow.columns)
df_slow = pd.DataFrame(list_slow, columns=['slow'])
CSV_slow_PATH = os.path.join(project_root, "data", "prepro", 'slow_variables.csv')
df_slow.to_csv(CSV_slow_PATH, index=False)
'''