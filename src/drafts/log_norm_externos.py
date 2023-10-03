import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from utils import data_loader
from utils.log_norm import *
from utils import lista_food
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
#############################################
# Retrieve the DataFrames from data_loader
#############################################
path=DATA_BASE_PATH
#path = 'C:/Users/Transitorio/Desktop/tesis2023/tesis2023-1/data/mydatabase.db'
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['Datos_fmi_2022_external']
df_dict = data_loader.get_data(path, tables_list)
df_fmi = df_dict['Datos_fmi_2022_external']

# Create an instance of StandardScaler
scaler = StandardScaler()
#####################################
# IPC general preprocessing
#####################################
#########################################
# IMF data preprocessing- df_fmi
#########################################
cols_px = df_fmi.iloc[:,1:].select_dtypes(exclude=['float']).columns
df_fmi[cols_px] = df_fmi[cols_px].apply(pd.to_numeric, downcast='float', errors='coerce')
df_fmi[['year','month']]=df_fmi.date.str.split('M',expand=True)
df_fmi['ymd'] = pd.to_datetime(df_fmi[['year', 'month']].assign(day=1), format='%d/%b/%Y')
p_usd=df_fmi.drop(['year', 'month','date' ], axis=1)
p_usd = p_usd.sort_values('ymd')
# Truncate the datetime part of fmi prices to match the time span of ipc clases
externos_usd = p_usd[(p_usd['ymd'] >= start_time_clases) & (p_usd['ymd'] <= end_time_clases)]
externos_usd_idx=externos_usd.set_index('ymd')
#########################################
# log transform
log_externos_usd_idx = np.log1p(externos_usd_idx)
# z-score rescaling
# Apply z-score normalization to the DataFrame
normalized_log_fmi_idx = scaler.fit_transform(log_externos_usd_idx)
# Update the DataFrame with the normalized values
log_externos_usd_idx[:] = normalized_log_fmi_idx
# variables associated with food and beverage
# IMPORTAR lista_fb
# creating a df for food and beverages
df_fb=log_externos_usd_idx[lista_fb]
avg_fb=df_fb.mean(axis = 1).to_frame('avg_fb')
# df for external prices to keep: soy, petroleum, beef and average food
lst_external=['PBEEF','POILAPSP','PSOYB']
ext_prices=log_externos_usd_idx.filter(lst_external)
df_external_idx=pd.concat([ext_prices, avg_fb], axis=1)

# logaritmos
log_norm_external=df_external_idx.reset_index()
log_norm_external['ymd'] = log_norm_external['ymd'].astype(str)