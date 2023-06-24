import data_loader
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
# Specify the database path
path = 'C:/Users/Transitorio/Desktop/tesis2023/tesis2023-1/data/mydatabase.db'
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['EXTERNAL', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(path, tables_list)
# to df
df_ext = df_dict['EXTERNAL']
df_clases=df_dict['CLASES_IPC']
df_gral = df_dict['IPC_gral']
############################################
# IPC GENERAL EDA
############################################
print('\n IPC general información de los datos: \n ------------------------------ \n')
print(df_gral.info())
# transform ymd column to datetime


