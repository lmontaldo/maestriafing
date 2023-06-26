import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from utils import data_loader 
from utils.ADF_KPSS_tests import adf_test 
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
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Specify the database path
path = DATA_BASE_PATH
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
# transform ymd column to datetime
df_gral['ymd'] = pd.to_datetime(df_gral['ymd']).dt.strftime('%Y-%m-%d')
# Create the plot
plt.figure(figsize=(10, 10))  # Adjust figure size to provide more space for labels
sns.lineplot(x='ymd', y='indice', data=df_gral)
plt.xlabel('fecha')
plt.ylabel('valor IPC')
plt.title('Evolución del IPC general mensual')
# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')
# Format x-axis tick labels for readability
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(8))
# Save the plot to an image file
plt.savefig('docs/images/time_series_plot_1.png')

print(df_clases.head())

results = adf_test(df_clases)
for column, result in results.items():
    print(f"Variable: {column}")
    print(result)
    print()







