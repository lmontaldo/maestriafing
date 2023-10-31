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
CSV_Y_PATH = os.path.join(project_root, "data", "prepro", 'sfr_sin_normalizar.csv') 
# read data  
df= pd.read_csv(CSV_Y_PATH, sep=",")
# split df into train and test
print(df.columns)




 # save data
#CSV_Y_PATH = os.path.join(project_root, "data", "prepro", 'sfr_sin_normalizar.csv')
#df_sfr_sin_idx.to_csv(CSV_Y_PATH, index=False)







