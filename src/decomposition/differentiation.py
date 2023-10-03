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

# Third-party Libraries
import dash
from dash import dcc, html
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from tabulate import tabulate

# Utils
from utils import data_loader
from utils.datetime import *
from utils.KPSS_tests_arch import KPSSAnalysis
from utils.models_ADF_arch import ModelsADF
from utils.standarization import Standardization
from utils.stl_decomposition import STL_procedure
from utils.test_statistics_adf import TestStatistics
from utils.validators import *


# -------------------------------
# CONFIGURATIONS
# -------------------------------
warnings.simplefilter('ignore', InterpolationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="seaborn")


def load_and_process_data():
    # Retrieve the DataFrames from data_loader
    tables_list = ['IPC_gral_log_norm', 'externos_log_norm', 'componentes_log_norm']
    df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)

    df_ipc = df_dict['IPC_gral_log_norm']
    df_externos = df_dict['externos_log_norm']
    df_compo = df_dict['componentes_log_norm']

    def to_datetime_str(df, column="ymd"):
        df[column] = pd.to_datetime(df[column]).dt.strftime('%Y-%m-%d')
        return df

    df_ipc_idx = to_datetime_str(df_ipc).set_index("ymd")
    df_ext_idx = to_datetime_str(df_externos).set_index("ymd")
    df_comp_idx = to_datetime_str(df_compo).set_index("ymd")
   

    d1_12_ipc_idx = df_ipc_idx.diff(1).diff(12).dropna()
    d1_12_ext_idx = df_ext_idx.diff(1).diff(12).dropna()
    d1_12_comp_idx = df_comp_idx.diff(1).diff(12).dropna()
    return d1_12_ipc_idx, d1_12_ext_idx, d1_12_comp_idx


if __name__ == "__main__":
    d1_12_ipc_idx, d1_12_ext_idx, d1_12_comp_idx = load_and_process_data()
    print(d1_12_ext_idx.head())
    
    

