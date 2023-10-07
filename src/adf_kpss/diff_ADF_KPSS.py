# -------------------------------
# IMPORTS
# -------------------------------
# Standard Libraries
import os
import sys
sys.path.append("C:\\Users\\user\\Desktop\\preprocesamiento")
import pandas as pd
import numpy as np
import sqlite3
from config import DATA_BASE_PATH
import time
import warnings
import datetime as dt
import math
import numbers
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
from src.decomposition.differentiation import *
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
# Retrieve the DataFrames from database
#############################################
d1_12_ipc_idx, d1_12_ext_idx, d1_12_comp_idx = load_and_process_data()
ipc_idx=d1_12_ipc_idx
ext_idx=d1_12_ext_idx
comp_idx=d1_12_comp_idx

# Create a dictionary of DataFrames for easy iteration
dfs = {
    'ipc_idx': ipc_idx,
    'ext_idx': ext_idx,
    'comp_idx': comp_idx
}
print("################################ TESTS ADF based on p-value <= alpha ###########################################")
# Iterate over each DataFrame
for df_name, df in dfs.items():
    print(f"############################################")
    print(f"##### ADF test con p-value for {df_name} ####")
    print(f"############################################")
    adf_model = ModelsADF(df)
    results = adf_model.perform_adf_test(trends=['ct', 'c', 'n'])
    for trend, results in results.items():
        print(f"Results for model {trend}:")
        
        # Display the entire DataFrame results
        print(results['df_results'])
        print("--------------------------")
        
        # Display RU results
        print(f"RU Results for model {trend}:")
        print(results['Stationary_series'])
        print("--------------------------")
        
        # Display not_RU results
        print(f"Not RU Results for trend {trend}:")
        print(results['Non_stationary_series'])
        print("--------------------------")
        
        # Display counts
        print(f"RU Count for trend {trend}: {results['Stationary_count']}")
        print(f"Not RU Count for trend {trend}: {results['Non_stationary_count']}")
        print("--------------------------")
        
        # Display series names
        print(f"RU Series for trend {trend}: {results['Stationary_series']}")
        print(f"Not RU Series for trend {trend}: {results['Non_stationary_series']}")
        print("\n======================================\n")
    
# For each dataframe, perform the KPSS analysis

print("################################ TESTS KPSS #########################################################")

for df_name, df in dfs.items():
    print("######################################################################################")
    print(f"################################ TESTS KPSS for {df_name} ###########################")
    print("######################################################################################")
    print(f'\n')
    kpss_analysis = KPSSAnalysis(df)

    # Performing the test
    kpss_analysis.perform_test()

    # Restricting the loop to only 'c' trend
    trends = ['ct', 'c']

    for trend in trends:
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
            
print("################################ TESTS ADF de lo general a lo particular: para modelos (b) y (a) ######################################")  
# Define your dataframes
df_ce = {
    'ext_idx': ext_idx,
    'comp_idx': comp_idx
}

# For each dataframe, perform the ADF test process
for df_name, df in df_ce.items():
    print(f"\n\nRunning ADF tests for {df_name}\n")
    print("#################################################################################")
    print('######### Primer paso: se usa tau_mu para testear la $H0) \gamma=0$ #############')
    print("#################################################################################")

    results_tau_mu = TestStatistics.tau_mu(df)
    print(f'Cantidad de secuencias que $RH0)\gamma=0$ entonces no contienen RU:   {results_tau_mu[3]}') 
    print(f'Secuencias que no contienen RU: {results_tau_mu[5]}')
    print(f'Cantidad de secuencias que $RH0)\gamma=0$ entonces no contienen RU:   {results_tau_mu[3]}') 
    print('=====> No hay necesidad de continuar con el prodecimiento para las mismas.')
    print(f'Secuencias que contienen RU:{results_tau_mu[6]}')
    print(f'Cantidad de secuencias que contienen RU:  {results_tau_mu[4]}')
    print('=====> Van al segundo paso')
    
    print("\n#################################################################################")
    print('######### Segundo paso: se usa phi_1 para testear la $H0) a_0=gamma=0$ ##########')
    print("#################################################################################")

    results_phi1 = TestStatistics.phi_1(df, cols_norho=results_tau_mu[6])
    print(f'Cantidad de secuencias que rH0: {results_phi1[3]}')
    print(f'Secuencias que rH0:{results_phi1[5]}')
    print('=====> Presencia de constante entonces de los resultados del paso 1, las series son RU y de phi_1 que gamma y/o a_0 son distintos de cero.')
    print("=====> Se gana conocimiento adicional estimando delta y_t=a_0 + sum beta_i delta y_{t-i} + varepsilon_t y testear H0) a_0=0 con distribucion t.")
    print(f'Cantidad de secuencias que no rH0: {results_phi1[4]}')
    print(f'Secuencias que no rH0:{results_phi1[6]}')
    print('=====>Ausencia de constante determinística entonces estas series pasan al paso 3.')

    print("\n#############################################################################################")
    print('######### Tercer paso: se usa tau para testear la H0) gamma=0 para las series con a_0 = 0 ###')
    print("#############################################################################################")

    results_tau = TestStatistics.tau(df, cols_no_rho=results_phi1[6])
    print(f'Secuencias que no contienen RU:{results_tau["rho_list"]} ====> estacionarias en modelo (a)')
    print(f'Secuencias que contienen RU:{results_tau["no_rho_list"]} ====> no estacionarias en modelo (a)')
    print(f'\n')

    # At the end of the loop's iteration for one dataframe, insert a separator for clarity
    print("\n===================================================================================")
    print(f"End of ADF tests for {df_name}")
    print("===================================================================================\n\n")
 