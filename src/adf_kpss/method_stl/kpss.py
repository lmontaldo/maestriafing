# -------------------------------
# IMPORTS
# -------------------------------
# Standard Libraries
import os
import sys
sys.path.append("C:\\Users\\user\\Desktop\\preprocesamiento")
from config import DATA_BASE_PATH
import pandas as pd
import numpy as np
import sqlite3
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
from src.decomposition.stl_loess import *
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
residual_c, residual_ext, residual_ipc = load_and_process_data()
ipc_idx=residual_ipc
ext_idx=residual_ext
comp_idx=residual_c

# Create a dictionary of DataFrames for easy iteration
dfs = {
    'ipc_idx': ipc_idx,
    'ext_idx': ext_idx,
    'comp_idx': comp_idx
}

print("################################ TESTS KPSS #########################################################")

for df_name, df in dfs.items():
    print("######################################################################################")
    print(f"################################ TESTS KPSS for {df_name} ###########################")
    print("######################################################################################")
    print(f'\n')

    # Create an instance of KPSSAnalysis with current dataframe
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