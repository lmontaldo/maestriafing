# -------------------------------
# IMPORTS
# -------------------------------
# Standard Libraries
import os
import sys
sys.path.append("C:\\Users\\user\\Desktop\\preprocesamiento")
from config import DATA_BASE_PATH
path=DATA_BASE_PATH
import pandas as pd
import numpy as np
import sqlite3
import time
import warnings
import datetime as dt
import math
import numbers
from utils import data_loader
from utils.validators import *
from utils.stl_decomposition import STL_procedure
from utils.datetime import *
from utils.test_statistics_adf import TestStatistics
from utils.models_ADF_arch import ModelsADF
from utils.KPSS_tests_arch import KPSSAnalysis
from utils.standarization import Standardization

# -------------------------------
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


    stl_ext = STL_procedure(df_ext_idx , seasonal=13, period=12)
    _, _, residual_ext = stl_ext.decompose_dataframe_stl()
    stl_ipc = STL_procedure(df_ipc_idx , seasonal=13, period=12)
    _, _, residual_ipc = stl_ipc.decompose_dataframe_stl()
    stl_c = STL_procedure(df_comp_idx , seasonal=13, period=12)
    _, _, residual_c = stl_c.decompose_dataframe_stl()
    return residual_c, residual_ipc, residual_ext

if __name__ == "__main__":
    residual_c, residual_ext, residual_ipc = load_and_process_data()

    
    






