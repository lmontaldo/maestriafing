# -------------------------------
# IMPORTS
# -------------------------------

# Standard libraries
import os
import sys
import numbers
import time
import math
import datetime as dt
import warnings

# Third-party libraries
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tools.sm_exceptions import InterpolationWarning
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_BASE_PATH, image_path
from utils import data_loader
from utils.validators import *
from utils.stl_decomposition import STL_procedure
from utils.datetime import *
from utils.test_statistics_adf import TestStatistics
from utils.models_ADF_arch import ModelsADF
from utils.KPSS_tests_arch import KPSSAnalysis
from utils.standarization import Standardization

# -------------------------------
# CONFIGURATIONS
# -------------------------------

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
stl = STL_procedure(df_idx_diff, seasonal=13, period=12)
trend, seasonal, residual = stl.decompose_dataframe_stl()
df_idx_diff_sa = stl.STL_seasonal_adjusted()

######################################################
# ADF TEST SOBRE LAS SERIES
######################################################
print(f'\n')
# ADF test over df_idx
print("##################################################################################")
print("################################ TESTS ADF  ######################################")
print("##################################################################################")
print(f'\n')
print("################################ Series normalizadas y estanzarizdadas ##########")
adf_model = ModelsADF(df_idx)
results = adf_model.perform_adf_test(trends=['ct', 'c', 'n'])
for trend, results in results.items():
    print(f"Results for trend {trend}:")
    
    # Display the entire DataFrame results
    print(results['df_results'])
    print("--------------------------")
    
    # Display RU results
    print(f"RU Results for trend {trend}:")
    print(results['RU'])
    print("--------------------------")
    
    # Display not_RU results
    print(f"Not RU Results for trend {trend}:")
    print(results['not_RU'])
    print("--------------------------")
    
    # Display counts
    print(f"RU Count for trend {trend}: {results['RU_count']}")
    print(f"Not RU Count for trend {trend}: {results['not_RU_count']}")
    print("--------------------------")
    
    # Display series names
    print(f"RU Series for trend {trend}: {results['RU_series']}")
    print(f"Not RU Series for trend {trend}: {results['not_RU_series']}")
    print("\n======================================\n")



print(f'\n')
print('############## Test ADF sobre las series en primeras diferencias y desestacionalizadas ##############') 
print(f'\n')
#df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series   = ModelsADF.adf_c(df_idx_diff_sa)
adf_model = ModelsADF(residual)
results = adf_model.perform_adf_test(trends=['c', 'n'])
for trend, results in results.items():
    print(f"Results for trend {trend}:")
    
    # Display the entire DataFrame results
    print(results['df_results'])
    print("--------------------------")
    
    # Display RU results
    print(f"RU Results for trend {trend}:")
    print(results['RU'])
    print("--------------------------")
    
    # Display not_RU results
    print(f"Not RU Results for trend {trend}:")
    print(results['not_RU'])
    print("--------------------------")
    
    # Display counts
    print(f"RU Count for trend {trend}: {results['RU_count']}")
    print(f"Not RU Count for trend {trend}: {results['not_RU_count']}")
    print("--------------------------")
    
    # Display series names
    print(f"RU Series for trend {trend}: {results['RU_series']}")
    print(f"Not RU Series for trend {trend}: {results['not_RU_series']}")
    print("\n======================================\n")
print(f'\n')
print("#################################################################################")
print('######### Primer paso: se usa tau_mu para testear la $H0) \gamma=0$ #############')
print("#################################################################################")
print(f'\n')
# rh0, no_rh0, tau_mu, rho_count, no_rho_count, rh0_list, no_rh0_list =TestStatistics.tau_mu(df_idx_diff_sa)
results_tau_mu=TestStatistics.tau_mu(residual)
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
results_phi1=TestStatistics.phi_1(residual, cols_norho=results_tau_mu[6])
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
results_a0=TestStatistics.a_0_t_standard(residual, cols_rho=results_phi1[5])
print(f'RH0): {results_a0["rho_list"]} =====> Para estas series se vuelve a un paso anterior y se evalúa $gamma=0$ con distribucion t\n')
print(f'No RH0): {results_a0["no_rho_list"]} =====> Para estas series se pasa al modelo (a) y se evalúa tau')
print(f'\n')
print("###############################################################################################")
print('Se vuelve al paso 1, para las series con a_0 neq 0 y se testea H0) gamma=0 con distribucion t')
print("################################################################################################")
print(f'\n')
results_gamma=TestStatistics.gamma_t_distribution(df_idx_diff_sa, cols_rho=results_a0["rho_list"], alpha=0.05, return_values=None)
print(results_gamma)
print(f'\n')
print("#############################################################################################")
print('######### Tercer paso: se usa tau para testear la H0) gamma=0 para las series con a_0 = 0 ###')
print("#############################################################################################")
print(f'\n')
# rh0_tau, no_rh0_tau, rh0_list, no_rh0_list = TestStatistics.tau(df_idx_diff_sa, cols_no_rho=no_rh0_list)
results_tau=TestStatistics.tau(residual, cols_no_rho=results_phi1[6])
print(f'Secuencias que no contienen RU:{results_tau["rho_list"]} ====> estacionarias en modelo (a)')
print(f'Secuencias que contienen RU:{results_tau["no_rho_list"]} ====> no estacionarias en modelo (a)')
# return {'rh0': rh0,'no_rh0': no_rh0,'rho_list': rh0_list, 'no_rho_list': no_rh0_list}  
print(f'\n')
# ADF test over df_idx
print("##################################################################################")
print("################################ TESTS KPSS  #####################################")
print("##################################################################################")
print(f'\n')
# Create an instance of KPSSAnalysis with your data
kpss_analysis = KPSSAnalysis(residual)
# Performing the test
kpss_analysis.perform_test()

# Restricting the loop to only 'c' trend
trend = 'c'
for nlags in kpss_analysis.nlags_list:
    print(f"Results for trend={trend} and nlags method={nlags}:")
    
    # Retrieve and print results
    df_results = kpss_analysis.get_results_for_trend_nlags(trend, nlags)
    stationary_df = kpss_analysis.get_stationary_for_trend_nlags(trend, nlags)
    non_stationary_df = kpss_analysis.get_non_stationary_for_trend_nlags(trend, nlags)

    print(f"\nDataFrame named {trend}_{nlags}:")
    print(df_results)
    
    print(f"\nList of Stationary series for trend={trend} and nlags method={nlags}:")
    print(list(stationary_df.index))  # Get the index (column names) of the stationary DataFrame
    
    print(f"\nList of Non-Stationary series for trend={trend} and nlags method={nlags}:")
    print(list(non_stationary_df.index)) 
    # Fetch and print counts
    stationary_count = kpss_analysis.get_stationary_count_for_trend_nlags(trend, nlags)
    non_stationary_count = kpss_analysis.get_non_stationary_count_for_trend_nlags(trend, nlags)
    
    print(f"Count of Stationary series for trend={trend} and nlags method={nlags}: {stationary_count}")
    print(f"Count of Non-Stationary series for trend={trend} and nlags method={nlags}: {non_stationary_count}")

    print("-------------------------------------------------------------")



