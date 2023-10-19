import pickle
import pandas as pd
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
from utils.normalization import scale_dataframe
prepro_data_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
pickle_HOUTSMW_file_path = os.path.join(project_root, "data", "prepro", 'residualsHOUTSMW.pkl')


with open(pickle_HOUTSMW_file_path, 'rb') as pickle_file:
    residualsHOUTSMW= pickle.load(pickle_file)
#    
df = pd.read_csv(prepro_data_file_path, sep=",", index_col='index')
df_drop=df.drop(["HOUSTMW"], axis=1)
#
concatenated_df = pd.concat([df_drop, residualsHOUTSMW], axis=1)
#
df_norm=scale_dataframe(concatenated_df)
PKL_NORM_PATH = os.path.join(project_root, "data", "prepro", 'data_normalized.pkl')
with open(PKL_NORM_PATH, 'wb') as file:
    pickle.dump(df_norm , file)
