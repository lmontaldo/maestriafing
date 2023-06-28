import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from config import image_path
from utils import data_loader 
from utils.ADF_tests import adf_test 
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
from utils.eda_decomposition import *
from utils.plot_saver import PlotSaver
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Specify the database path
DATA_BASE_PATH
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['EXTERNAL', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df_ext = df_dict['EXTERNAL']
df_clases=df_dict['CLASES_IPC']
df_gral = df_dict['IPC_gral']
############################################
# IPC GENERAL EDA
############################################
df_gral = to_datetime_str(df_gral, 'ymd')
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



