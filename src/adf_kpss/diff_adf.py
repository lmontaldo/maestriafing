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
ipc_idx = d1_12_ipc_idx
ext_idx = d1_12_ext_idx
comp_idx = d1_12_comp_idx

# Create a list of DataFrame names and their corresponding data for ease of processing
dfs = {
    "ipc_idx": ipc_idx,
    "ext_idx": ext_idx,
    "comp_idx": comp_idx
}

# Loop through each DataFrame, perform the ADF test, and print the results
for df_name, df_data in dfs.items():
    print("========================================\n")
    print(f"Procesando datos para: {df_name}\n{'='*50}")
    print("========================================\n")
    
    # Initialize the class with the current DataFrame
    adf_model = ModelsADF(df_data, alpha=0.05)

    # Perform ADF test and get the results
    results = adf_model.perform_adf_test()

    # Print results
    for trend, trend_results in results.items():
        print("========================================\n")
        print(f"Resultados para la tendencia: {trend}\n")
        print("========================================\n")
        #print(trend_results['df_results'])
        print(f"Cantidad series estacionarias: {trend_results['Stationary_count']}\n")
        print(f"Cantidad series no estacionarias:{trend_results['Non_stationary_count']}\n")
        print(f"Series estacionarias:\n {trend_results['Stationary_series']}\n")
        print(f"Series no estacionarias:\n {trend_results['Non_stationary_series']}\n")
    
    print("\n")





        
