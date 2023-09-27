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
#from utils.eda_decomposition import decompose_dataframe, perform_seasonal_adjustment
#from utils.unitroot import *
from utils.validators import *
from utils.stl_decomposition import STL_procedure
#from utils.ADF_tests import *
from utils.eda_decomposition import *
from utils.test_statistics_adf import TestStatistics
from utils.models_ADF import ModelsADF
from utils.KPSS_tests_arch import KPSSAnalysis
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
#df_idx_diff_sa = perform_seasonal_adjustment(df_idx_diff)

stl = STL_procedure(df_idx_diff, seasonal=13, period=12)
trend, seasonal, residual = stl.decompose_dataframe_stl()
df_idx_diff_sa = stl.STL_seasonal_adjusted()
detrended = stl.STL_detrend()
######################################################
# ADF TEST SOBRE LAS SERIES
######################################################
print(f'\n')
# ADF test over df_idx
print("##################################################################################")
print("################################ TESTS ADF  ######################################")
print("##################################################################################")
print(f'\n')
print('########## Tests ADF sobre las series en log y normalizadas ######################')
print(f'\n')
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_ct(df_idx)
results_1=ModelsADF.adf_ct(df_idx)
print(f'Cantidad de series que son no estacionarias en modelo (c): {results_1[3]}')
print(f'Cantidad de series que son estacionarias en modelo (c): {results_1[4]}')
print(f'Lista de series que son estacionarias en modelo (c): {results_1[6]}')
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_c(df_idx)
print(f'\n')
results_2=ModelsADF.adf_c(df_idx)
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
print("######################################################################################################")
print('############## Test ADF sobre las series en primeras diferencias y desestacionalizadas ##############') 
print("######################################################################################################")
print(f'\n')
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
print("#################################################################################")
print('######### Primer paso: se usa tau_mu para testear la $H0) \gamma=0$ #############')
print("#################################################################################")
print(f'\n')
# rh0, no_rh0, tau_mu, rho_count, no_rho_count, rh0_list, no_rh0_list =TestStatistics.tau_mu(df_idx_diff_sa)
results_tau_mu=TestStatistics.tau_mu(df_idx_diff_sa)
print(f'Cantidad de secuencias que $RH0)\gamma=0$ entonces no contienen RU:   {results_tau_mu[3]}') 
print(f'Secuencias que no contienen RU: {results_tau_mu[5]}')
print(f'Cantidad de secuencias que $RH0)\gamma=0$ entonces no contienen RU:   {results_tau_mu[3]}') 
print('=====> No hay necesidad de continuar con el prodecimiento para las mismas.')
print('\n')
print(f'Secuencias que contienen RU:{results_tau_mu[6]}')
print(f'Cantidad de secuencias que contienen RU:  {results_tau_mu[4]}')
print('=====> Van al segundo paso')


print(f'\n')
print("#################################################################################")
print('######### Segundo paso: se usa phi_1 para testear la $H0) a_0=gamma=0$ ##########')
print("#################################################################################")
print(f'\n')
# rh0, no_rh0, phi_1, rho_count, no_rho_count, rh0_list, no_rh0_list=TestStatistics.phi_1(df_idx_diff_sa, cols_no_rho=no_rh0_list)
results_phi1=TestStatistics.phi_1(df_idx_diff_sa, cols_norho=results_tau_mu[6])
print(f'Cantidad de secuencias que rH0: {results_phi1[3]}')
print(f'Secuencias que rH0:{results_phi1[5]}')
print('=====> Presencia de constante entonces de los resultados del paso 1, las series son RU y de phi_1 que gamma y/o a_0 son distintos de cero.')
print("=====> Se gana conocimiento adicional estimando delta y_t=a_0 + sum beta_i delta y_{t-i} + varepsilon_t y testear H0) a_0=0 con distribucion t.")
print(f'\n')
print(f'Cantidad de secuencias que no rH0: {results_phi1[4]}')
print(f'Secuencias que no rH0:{results_phi1[6]}')
print('=====>Ausencia de constante determinística entonces estas series pasan al paso 3.')

print(f"\n")
print("#################################################################################")
print('Se estima $Delta y_t = a_0 + Sum beta_i Delta y_{t-i} + varepsilon_t$:')
print('Es a_0=0 con t-test?')
print("#################################################################################")
print(f'\n')
#rh0_list, no_rh0_list=TestStatistics.a_0_t(df_idx_diff_sa, cols_rho=rh0_list)
results_a0=TestStatistics.a_0_t_standard(df_idx_diff_sa, cols_rho=results_phi1[5])
print(f'RH0): {results_a0["rho_list"]} =====> Para estas series se vuelve a un paso anterior y se evalúa $gamma=0$ con distribucion t\n')
print(f'No RH0): {results_a0["no_rho_list"]} =====> Para estas series se pasa al modelo (a) y se evalúa tau')
print(f'\n')
print("###############################################################################################")
print('Se vuelve al paso 1, para las series con a_0 neq 0 y se testea H0) gamma=0 con distribucion t')
print("################################################################################################")
print(f'\n')
results_gamma=TestStatistics.gamma_t_distribution(df, cols_rho=results_a0["rho_list"], alpha=0.05, return_values=None)
print(results_gamma)
print(f'\n')
print("#############################################################################################")
print('######### Tercer paso: se usa tau para testear la H0) gamma=0 para las series con a_0 = 0 ###')
print("#############################################################################################")
print(f'\n')
# rh0_tau, no_rh0_tau, rh0_list, no_rh0_list = TestStatistics.tau(df_idx_diff_sa, cols_no_rho=no_rh0_list)
results_tau=TestStatistics.tau(df_idx_diff_sa, cols_no_rho=results_phi1[6])
print(f'Secuencias que no contienen RU:{results_tau["rho_list"]} ====> estacionarias en modelo (a)')
print(f'Secuencias que contienen RU:{results_tau["no_rho_list"]} ====> no estacionarias en modelo (a)')
# return {'rh0': rh0,'no_rh0': no_rh0,'rho_list': rh0_list, 'no_rho_list': no_rh0_list}  
print(f'\n')
# ADF test over df_idx
print("##################################################################################")
print("################################ TESTS KPSS  #####################################")
print("##################################################################################")
print(f'\n')
# Usage:
analysis = KPSSAnalysis(df_idx_diff_sa)
analysis.perform_test()
    # Perform the test
analysis.perform_test()

results_df = analysis.get_result()
print(results_df)

true_columns = analysis.get_RH0_true_columns()
print(true_columns)





