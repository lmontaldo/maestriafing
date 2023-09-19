import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from config import image_path
from utils import data_loader 
#from utils.ADF_tests import adf_test 
sys.path.append('../utils')
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
from utils.eda_decomposition import decompose_dataframe, perform_seasonal_adjustment
#from utils.unitroot import *
from utils.pruebas_KPSS import *
from utils.validators import *
#from utils.ADF_tests import *
from utils.eda_decomposition import *
from utils.test_statistics_adf import TestStatistics
from utils.models_ADF import ModelsADF
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
import matplotlib.pyplot as plt
from arch.unitroot import ADF
import warnings
from statsmodels.tools.sm_exceptions import InterpolationWarning
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tabulate import tabulate
import warnings
warnings.simplefilter('ignore', InterpolationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="seaborn")
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['Datosipc', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df=df_dict['CLASES_IPC']
df_raw=df_dict['Datosipc']

############################################
# GRÁFICOS DE LOS COMPONENTES IPC
############################################
df['ymd'] = pd.to_datetime(df['ymd']).dt.normalize()

# from wide to long to make plots
long_df= pd.melt(df, id_vars='ymd', var_name='code', value_name='value')
long_df['groups_codes'] =long_df['code'].str[:3]
# plot components
'''
dfs = {group: data for group, data in long_df.groupby('groups_codes')}
for group, sub_df in dfs.items():
    
    # Convert the 'ymd' column to pandas datetime format
    sub_df["ymd"] = pd.to_datetime(sub_df["ymd"])
    
    g = sns.relplot(data=sub_df, x="ymd", y="value",
                    col="code", hue="code",
                    kind="line", palette="deep",
                    linewidth=4, zorder=5,
                    col_wrap=3, height=3.5, aspect=1.5, legend=False
                   )

    # Adjusting space at the bottom if needed
    g.fig.subplots_adjust(bottom=0.2) 

    # Ensure there's enough spacing between subplots to avoid overlap
    g.fig.tight_layout()

    # Format the x-axis to handle dates
    for ax in g.axes.flat:
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        
    # Show the plot
    plt.show()
'''
# size of each group
unique_codes_per_group = long_df.groupby('groups_codes')['code'].nunique()
latex_table_c = unique_codes_per_group.reset_index().to_latex(index=False, header=["Groups Codes", "Unique Codes Count"])
print(latex_table_c)

# plot
'''
# plot
# underlying trends in ts df
# Use the function to extract the trend
trend_df = STL_extract_trend(df)
# melt the dataframe
long_df_trend = pd.melt(trend_df, id_vars='ymd', var_name='code', value_name='value')
# grouping by code
long_df_trend['groups_codes'] =long_df_trend['code'].str[:3]
# plot trends
dfs = {group: data for group, data in long_df_trend.groupby('groups_codes')}
for group, sub_df in dfs.items():
    
    # Convert the 'ymd' column to pandas datetime format
    sub_df["ymd"] = pd.to_datetime(sub_df["ymd"])
    
    g = sns.relplot(data=sub_df, x="ymd", y="value",
                    col="code", hue="code",
                    kind="line", palette="deep",
                    linewidth=4, zorder=5,
                    col_wrap=3, height=3.5, aspect=1.5, legend=False
                   )

    # Adjusting space at the bottom if needed
    g.fig.subplots_adjust(bottom=0.2) 

    # Ensure there's enough spacing between subplots to avoid overlap
    g.fig.tight_layout()

    # Format the x-axis to handle dates
    for ax in g.axes.flat:
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        
    # Show the plot
    plt.show()
'''  

#############################################################################
# REMOCIÓN DE LA TENDENCIA Y  ESTACIONALIDAD DE LOS COMPONENTES DEL IPC
############################################################################  
df_idx=df.set_index('ymd')
df_idx_diff = df_idx.diff().dropna()
df_idx_diff_sa = STL_seasonal_adjusted(df_idx_diff)
df_idx_sa=STL_seasonal_adjusted(df_idx)

######################################################
# ADF TEST SOBRE LAS SERIES
######################################################

# ADF test ct
# Using the tau_tau method and retrieving only the lists
df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_ct(df_idx_sa)
print(f'lista de series que son no estacionarias en modelo c: {RU_series}')
print(f'lista de series que son estacionarias en modelo c: {not_RU_series}')

df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_c(df_idx_sa)
print(f'lista de series que son no estacionarias en modelo b: {RU_series}')
print(f'lista de series que son estacionarias en modelo b: {not_RU_series}')


df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_n(df_idx_sa)
print(f'lista de series que son no estacionarias en modelo a: {RU_series}')
print(f'lista de series que son estacionarias en modelo a: {not_RU_series}')