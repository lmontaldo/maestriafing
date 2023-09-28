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
from utils.eda_decomposition import *
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
# Retrieve the DataFrames from database
#############################################
    
tables_list= ['STL_RESIDUALS', 
    'STL_TREND',
    'STL_SEASONAL']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df=df_dict['STL_RESIDUALS']
df['ymd'] = pd.to_datetime(df['ymd']).dt.normalize()
df_idx=df.set_index('ymd')

print("############################################")
print('######### ADF test con p-value #############')
print("############################################")
adf_model = ModelsADF(df_idx)
results = adf_model.perform_adf_test(trends=['ct', 'c', 'n'])
for trend, results in results.items():
    print(f"Results for model {trend}:")
    
    # Display the entire DataFrame results
    print(results['df_results'])
    print("--------------------------")
    
    # Display RU results
    print(f"RU Results for model {trend}:")
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
    
    
############################################
# ADF TEST: from general to specific
############################################
print("#################################################################################")
print('######### Primer paso: se usa tau_mu para testear la $H0) \gamma=0$ #############')
print("#################################################################################")
results_tau_mu=TestStatistics.tau_mu(df_idx)
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
results_phi1=TestStatistics.phi_1(df_idx, cols_norho=results_tau_mu[6])
print(f'Cantidad de secuencias que rH0: {results_phi1[3]}')
print(f'Secuencias que rH0:{results_phi1[5]}')
print('=====> Presencia de constante entonces de los resultados del paso 1, las series son RU y de phi_1 que gamma y/o a_0 son distintos de cero.')
print("=====> Se gana conocimiento adicional estimando delta y_t=a_0 + sum beta_i delta y_{t-i} + varepsilon_t y testear H0) a_0=0 con distribucion t.")
print(f'\n')
print(f'Cantidad de secuencias que no rH0: {results_phi1[4]}')
print(f'Secuencias que no rH0:{results_phi1[6]}')
print('=====>Ausencia de constante determinística entonces estas series pasan al paso 3.')

print(f'\n')
print("#############################################################################################")
print('######### Tercer paso: se usa tau para testear la H0) gamma=0 para las series con a_0 = 0 ###')
print("#############################################################################################")
print(f'\n')
# rh0_tau, no_rh0_tau, rh0_list, no_rh0_list = TestStatistics.tau(df_idx_diff_sa, cols_no_rho=no_rh0_list)
results_tau=TestStatistics.tau(df_idx, cols_no_rho=results_phi1[6])
print(f'Secuencias que no contienen RU:{results_tau["rho_list"]} ====> estacionarias en modelo (a)')
print(f'Secuencias que contienen RU:{results_tau["no_rho_list"]} ====> no estacionarias en modelo (a)')
print(f'\n')


print("##################################################################################")
print("################################ TESTS KPSS  #####################################")
print("##################################################################################")
print(f'\n')
# Create an instance of KPSSAnalysis with your data
kpss_analysis = KPSSAnalysis(df_idx)
# Performing the test
kpss_analysis.perform_test()

# Restricting the loop to only 'c' trend
trend = 'c'
for nlags in kpss_analysis.nlags_list:
    print(f"Results for model={trend} and nlags method={nlags}:")
    
    # Retrieve and print results
    df_results = kpss_analysis.get_results_for_trend_nlags(trend, nlags)
    stationary_df = kpss_analysis.get_stationary_for_trend_nlags(trend, nlags)
    non_stationary_df = kpss_analysis.get_non_stationary_for_trend_nlags(trend, nlags)

    print(f"\nDataFrame named {trend}_{nlags}:")
    print(df_results)
    
    print(f"\nList of Stationary series for model={trend} and nlags method={nlags}:")
    print(list(stationary_df.index))  # Get the index (column names) of the stationary DataFrame
    
    print(f"\nList of Non-Stationary series for model={trend} and nlags method={nlags}:")
    print(list(non_stationary_df.index)) 
    # Fetch and print counts
    stationary_count = kpss_analysis.get_stationary_count_for_trend_nlags(trend, nlags)
    non_stationary_count = kpss_analysis.get_non_stationary_count_for_trend_nlags(trend, nlags)
    
    print(f"Count of Stationary series for model={trend} and nlags method={nlags}: {stationary_count}")
    print(f"Count of Non-Stationary series for model={trend} and nlags method={nlags}: {non_stationary_count}")

    print("-------------------------------------------------------------")