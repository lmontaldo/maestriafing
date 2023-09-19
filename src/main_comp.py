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
#print(latex_table_c)

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
df_idx_diff_sa = perform_seasonal_adjustment(df_idx_diff)


######################################################
# ADF TEST SOBRE LAS SERIES
######################################################

# ADF test over df_idx
print("################################ TESTS ADF ######################################")
print("#################################################################################")
print(f'\n')
print('########## Tests ADF sobre las series en log y normalizadas ##################')
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_ct(df_idx)
results_1=ModelsADF.adf_ct(df_idx)
print(f'Cantidad de series que son no estacionarias en modelo (c): {results_1[3]}')
print(f'Cantidad de series que son estacionarias en modelo (c): {results_1[4]}')
print(f'Lista de series que son estacionarias en modelo (c): {results_1[6]}')
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_c(df_idx)
print(f'\n')
results_2=ModelsADF.adf_ct(df_idx)
print(f'Cantidad de series que son no estacionarias en modelo (b): {results_2[3]}')
print(f'Cantidad de series que son estacionarias en modelo (b): {results_2[4]}')
print(f'Lista de series que son estacionarias en modelo (b): {results_2[6]}')
print(f'\n')
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_n(df_idx)
results_3=ModelsADF.adf_n(df_idx)
print(f'Cantidad de series que son no estacionarias en modelo (a): {results_3[3]}')
print(f'Cantidad de series que son estacionarias en modelo (a): {results_3[4]}')
print(f'Lista de series que son estacionarias en modelo (a): {results_3[6]}')

print(f'\n')
print(' ############## Test ADF sobre las series en primeras diferencias y desestacionalizadas ##############') 
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_c(df_idx_diff_sa)
results_4=ModelsADF.adf_ct(df_idx)
print(f'Cantidad de series con RU en modelo (b): {results_4[3]}')
print(f'Lista de series con RU en modelo (b): {results_4[5]}')
print(f'\n')
print(f'# de series con NO RU en modelo (b): {results_4[4]}')
print(f'Lista de series con NO RU en modelo (b): {results_4[6]}')
print(f'\n')
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_n(df_idx_diff_sa)
results_5= ModelsADF.adf_n(df_idx_diff_sa)
print(f'Cantidad de series que son no estacionarias en modelo (a): {results_5[3]}')
print(f'Lista de series que son no estacionarias en modelo (a): {results_5[5]}')
print(f'Cantidad de series que son estacionarias en modelo (a): {results_5[4]}')
print(f'Lista de series que son estacionarias en modelo (a): {results_5[6]}\n')
print(f'\n')
print('Significancia de tau_mu')
# rh0, no_rh0, tau_mu, rho_count, no_rho_count, rh0_list, no_rh0_list =TestStatistics.tau_mu(df_idx_diff_sa)
results_tau_mu=TestStatistics.tau_mu(df_idx_diff_sa)
print(f'Secuencias que no contienen RU:{results_tau_mu[5]}')
print(f'Cantidad de secuencias que no contienen RU:{results_tau_mu[3]}')
print(f'Secuencias que contienen RU:{results_tau_mu[6]}')
print(f'Cantidad de secuencias que contienen RU:{results_tau_mu[4]}')
print(results_tau_mu[6])
print(f'\n')
print('Significancia phi_1:')
# rh0, no_rh0, phi_1, rho_count, no_rho_count, rh0_list, no_rh0_list=TestStatistics.phi_1(df_idx_diff_sa, cols_no_rho=no_rh0_list)
results_phi1=TestStatistics.phi_1(df_idx_diff_sa, cols_norho=results_tau_mu[6])
print(f'Secuencias que rH0:{results_phi1[5]}')
print(f'Cantidad de secuencias que rH0:{results_phi1[3]}')
print(f'Secuencias que no rH0:{results_phi1[6]}')
print(f'Cantidad de secuencias que no rH0:{results_phi1[4]}')
print(f'\n')
print('Significancia de a_0:')
#rh0_list, no_rh0_list=TestStatistics.a_0_t(df_idx_diff_sa, cols_rho=rh0_list)
results_a0=TestStatistics.a_0_t(df_idx_diff_sa, cols_rho=results_phi1[5])
print(f'Reject the null hypothesis: a0 is different from 0: {results_a0["rho_list"]}')
print(f'Fail to reject the null hypothesis: a0 may be 0: {results_a0["no_rho_list"]}')
print(f'\n')
print(f'Modelo (a) sobre NoRH0)\gamma=a_0=0:')
# rh0_tau, no_rh0_tau, rh0_list, no_rh0_list = TestStatistics.tau(df_idx_diff_sa, cols_no_rho=no_rh0_list)
results_tau=TestStatistics.tau(df_idx_diff_sa, cols_no_rho=results_phi1[6])
print(f'Secuencias que no contienen RU:{results_tau["rho_list"]}')
print(f'Secuencias que contienen RU:{results_tau["no_rho_list"]}')
# return {'rh0': rh0,'no_rh0': no_rh0,'rho_list': rh0_list, 'no_rho_list': no_rh0_list}  