import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from config import image_path
from utils import data_loader 
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from utils.datetime import *
from utils.plot_saver import PlotSaver
from arch.unitroot import ADF
from utils.unitroot import UnitRootTests
from utils.pruebas_KPSS import *
from utils.datetime import *
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['EXTERNAL', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df_ext = df_dict['EXTERNAL']
df_clases=df_dict['CLASES_IPC']
df_gral = df_dict['IPC_gral']
############################################
# IPC GENERAL: EDA
############################################
df_gral['ymd'] = pd.to_datetime(df_gral['ymd'], format='%Y-%m-%d')
df_gral_idx = df_gral.set_index('ymd')
# Plot the IPC general and save in docs/images
#save_line_plot_df(df_gral_idx, image_path, title='Evolución IPC general en logaritmos y normalizado', xlabel='Fecha', ylabel='Valores IPC')
# Differenciate IPC general
df_gral_idx_diff = df_gral_idx.diff().dropna()
# Plot the differenciated IPC general and save in docs/images
#save_line_plot_df(df_gral_idx_diff, image_path, title='Evolución IPC general en primeras diferencias', xlabel='Fecha', ylabel='Valores')
# Deseasonalize IPC general
df_gral_idx_diff_des = perform_seasonal_adjustment(df_gral_idx_diff)
#save_line_plot_df(df_gral_idx_diff_des, image_path, title='Evolución IPC general en primeras diferencias con ajuste estacional', xlabel='Fecha', ylabel='Valores')
df_gral_idx_diff_des
analyzer = KPSSAnalyzer(df_gral_idx_diff_des)
analyzer.kpss_test_c()  # For constant stationarity
analyzer.kpss_test_ct()  # For trend stationarity




############################################
# Clases IPC: EDA
 ############################################
print('\n----------\n')
print('\nThe IPC classes have been detrended and deseasonalized so it is expected to be stationaries.')
print('Performing Unit Root ADF test')
df_clases['ymd'] = pd.to_datetime(df_clases['ymd'], format='%Y-%m-%d')
df_clases_idx=df_clases.set_index('ymd')
