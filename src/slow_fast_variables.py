import pandas as pd
import numpy as np
import sys
import os
import pickle
from sklearn.decomposition import PCA
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, DATA_BASE_PATH,  PICKLE_NORM_DF_FILE_PATH, DESCRIPTIONS_PATH
with open(PICKLE_NORM_DF_FILE_PATH, 'rb') as file:
    df = pickle.load(file)
# filter by aggregated variables as un Stock and watson   
descrip = pd.read_csv(DESCRIPTIONS_PATH, sep='\t')
print(descrip.shape)
columns_to_keep = df.columns
filtered_descrip = descrip[descrip['fred'].isin(columns_to_keep)]
print(filtered_descrip.shape)
print(df.shape)