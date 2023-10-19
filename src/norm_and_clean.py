import pandas as pd
import sys
import os
import pickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, DATA_BASE_PATH, PKL_HOUTSMW_PATH
#PKL_HOUTSMW_PATH = os.path.join(DATA_DIR, 'residualsHOUTSMW.pkl')
from utils.normalization import scale_dataframe
with open(PKL_HOUTSMW_PATH, 'rb') as pickle_file:
    residualsHOUTSMW= pickle.load(pickle_file)
#    
df = pd.read_csv(DATA_BASE_PATH, sep=",", index_col='index')
df_drop=df.drop(["HOUSTMW"], axis=1)
#
concatenated_df = pd.concat([df_drop, residualsHOUTSMW], axis=1)
#
df_norm=scale_dataframe(concatenated_df)
PKL_NORM_PATH = os.path.join(DATA_DIR, 'data_normalized.pkl')
with open(PKL_NORM_PATH, 'wb') as file:
    pickle.dump(df_norm , file)
