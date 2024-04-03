import pandas as pd
import sys
import os
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_Y_PATH = os.path.join(project_root, "data", "prepro", 'sfr_sin_normalizar.csv') 
# read data  
df= pd.read_csv(CSV_Y_PATH, sep=",")

print(df.columns)
print(df.iloc[:,89:96])
print(df.iloc[:,15])
# List of values to be changed
#values_to_change <- c("S&P 500", "S&P: indust" ,"S&P div yield" ,  "S&P PE ratio", "IPB51222s")
# Define the new column names
new_column_names = {
    'S.P.500': 'S&P 500',
    'S.P..indust': 'S&P: indust',
    'S.P.div.yield': 'S&P div yield',
    'S.P.PE.ratio': 'S&P PE ratio',
    'PB51222S': 'IPB51222s'
}

# Rename the columns
df.rename(columns=new_column_names, inplace=True)
print(df.iloc[:,89:96])
#
# split df into train and test
df_idx=df.set_index('date')
df_idx.index = pd.to_datetime(df_idx.index, format='%Y-%m-%d')
df_idx.index = df_idx.index.date
df_idx.sort_index(inplace=True)
train_size = int(len(df_idx) * 0.8)
train, test = df_idx.iloc[:train_size], df_idx.iloc[train_size:]
print(train.index.min(),train.index.max())
print(test.index.min(),test.index.max())
print(len(test))
print(train.shape)
print(test.shape)
#
train.reset_index(inplace=True)
test.reset_index(inplace=True)
 # save data
train_PATH = os.path.join(project_root, "data", "train_test", 'sfr_train.csv')
train.to_csv(train_PATH, index=False)
test_PATH = os.path.join(project_root, "data", "train_test", 'sfr_test.csv')
test.to_csv(test_PATH, index=False)







