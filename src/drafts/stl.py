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
import sqlite3
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from config import DATA_BASE_PATH
path=DATA_BASE_PATH
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
# 
df['ymd'] = pd.to_datetime(df['ymd']).dt.normalize()
df_idx=df.set_index('ymd')
print(f'La cantidad de observaciones es {df_idx.shape[0]}')
#######################################################
# ENFOQUE DE DETRENDING Y SEASONAL ADJUSTMENT BY LOESS
######################################################
stl = STL_procedure(df_idx, seasonal=13, period=12)
trend, seasonal, residual = stl.decompose_dataframe_stl()
trends=trend.reset_index()
seasonals=seasonal.reset_index()
residuals=residual.reset_index()

print(residuals.head())



dataframes = {
    'STL_RESIDUALS': residuals, 
    'STL_TREND': trends,
    'STL_SEASONAL': seasonals
     
}

# Create tables in the database
def create_tables(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # If the table already exists, replace it
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS STL_RESIDUALS(
            ymd TEXT,
            c0111 FLOAT,
            c0112 FLOAT,
            c0113 FLOAT,
            c0114 FLOAT,
            c0115 FLOAT,
            c0116 FLOAT,
            c0117 FLOAT,
            c0118 FLOAT,
            c0119 FLOAT,
            c0121 FLOAT,
            c0122 FLOAT,
            c0211 FLOAT,
            c0212 FLOAT,
            c0213 FLOAT,
            c0220 FLOAT,
            c0312 FLOAT,
            c0314 FLOAT,
            c0321 FLOAT,
            c0322 FLOAT,
            c0411 FLOAT,
            c0431 FLOAT,
            c0432 FLOAT,
            c0441 FLOAT,
            c0442 FLOAT,
            c0443 FLOAT,
            c0444 FLOAT,
            c0451 FLOAT,
            c0452 FLOAT,
            c0454 FLOAT,
            c0511 FLOAT,
            c0520 FLOAT,
            c0531 FLOAT,
            c0533 FLOAT,
            c0540 FLOAT,
            c0551 FLOAT,
            c0552 FLOAT,
            c0561 FLOAT,
            c0562 FLOAT,
            c0611 FLOAT,
            c0613 FLOAT,
            c0621 FLOAT,
            c0622 FLOAT,
            c0623 FLOAT,
            c0630 FLOAT,
            c0690 FLOAT,
            c0711 FLOAT,
            c0712 FLOAT,
            c0713 FLOAT,
            c0721 FLOAT,
            c0722 FLOAT,
            c0723 FLOAT,
            c0724 FLOAT,
            c0732 FLOAT,
            c0733 FLOAT,
            c0734 FLOAT,
            c0735 FLOAT,
            c0736 FLOAT,
            c0810 FLOAT,
            c0820 FLOAT,
            c0830 FLOAT,
            c0911 FLOAT,
            c0912 FLOAT,
            c0913 FLOAT,
            c0914 FLOAT,
            c0931 FLOAT,
            c0933 FLOAT,
            c0934 FLOAT,
            c0935 FLOAT,
            c0941 FLOAT,
            c0942 FLOAT,
            c0943 FLOAT,
            c0951 FLOAT,
            c0952 FLOAT,
            c0954 FLOAT,
            c0960 FLOAT,
            c1010 FLOAT,
            c1020 FLOAT,
            c1040 FLOAT,
            c1050 FLOAT,
            c1111 FLOAT,
            c1112 FLOAT,
            c1120 FLOAT,
            c1211 FLOAT,
            c1213 FLOAT,
            c1232 FLOAT,
            c1252 FLOAT,
            c1254 FLOAT,
            c1270 FLOAT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STL_TREND (
            ymd TEXT,
            c0111 FLOAT,
            c0112 FLOAT,
            c0113 FLOAT,
            c0114 FLOAT,
            c0115 FLOAT,
            c0116 FLOAT,
            c0117 FLOAT,
            c0118 FLOAT,
            c0119 FLOAT,
            c0121 FLOAT,
            c0122 FLOAT,
            c0211 FLOAT,
            c0212 FLOAT,
            c0213 FLOAT,
            c0220 FLOAT,
            c0312 FLOAT,
            c0314 FLOAT,
            c0321 FLOAT,
            c0322 FLOAT,
            c0411 FLOAT,
            c0431 FLOAT,
            c0432 FLOAT,
            c0441 FLOAT,
            c0442 FLOAT,
            c0443 FLOAT,
            c0444 FLOAT,
            c0451 FLOAT,
            c0452 FLOAT,
            c0454 FLOAT,
            c0511 FLOAT,
            c0520 FLOAT,
            c0531 FLOAT,
            c0533 FLOAT,
            c0540 FLOAT,
            c0551 FLOAT,
            c0552 FLOAT,
            c0561 FLOAT,
            c0562 FLOAT,
            c0611 FLOAT,
            c0613 FLOAT,
            c0621 FLOAT,
            c0622 FLOAT,
            c0623 FLOAT,
            c0630 FLOAT,
            c0690 FLOAT,
            c0711 FLOAT,
            c0712 FLOAT,
            c0713 FLOAT,
            c0721 FLOAT,
            c0722 FLOAT,
            c0723 FLOAT,
            c0724 FLOAT,
            c0732 FLOAT,
            c0733 FLOAT,
            c0734 FLOAT,
            c0735 FLOAT,
            c0736 FLOAT,
            c0810 FLOAT,
            c0820 FLOAT,
            c0830 FLOAT,
            c0911 FLOAT,
            c0912 FLOAT,
            c0913 FLOAT,
            c0914 FLOAT,
            c0931 FLOAT,
            c0933 FLOAT,
            c0934 FLOAT,
            c0935 FLOAT,
            c0941 FLOAT,
            c0942 FLOAT,
            c0943 FLOAT,
            c0951 FLOAT,
            c0952 FLOAT,
            c0954 FLOAT,
            c0960 FLOAT,
            c1010 FLOAT,
            c1020 FLOAT,
            c1040 FLOAT,
            c1050 FLOAT,
            c1111 FLOAT,
            c1112 FLOAT,
            c1120 FLOAT,
            c1211 FLOAT,
            c1213 FLOAT,
            c1232 FLOAT,
            c1252 FLOAT,
            c1254 FLOAT,
            c1270 FLOAT
        );
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STL_SEASONAL (
            ymd TEXT,
            c0111 FLOAT,
            c0112 FLOAT,
            c0113 FLOAT,
            c0114 FLOAT,
            c0115 FLOAT,
            c0116 FLOAT,
            c0117 FLOAT,
            c0118 FLOAT,
            c0119 FLOAT,
            c0121 FLOAT,
            c0122 FLOAT,
            c0211 FLOAT,
            c0212 FLOAT,
            c0213 FLOAT,
            c0220 FLOAT,
            c0312 FLOAT,
            c0314 FLOAT,
            c0321 FLOAT,
            c0322 FLOAT,
            c0411 FLOAT,
            c0431 FLOAT,
            c0432 FLOAT,
            c0441 FLOAT,
            c0442 FLOAT,
            c0443 FLOAT,
            c0444 FLOAT,
            c0451 FLOAT,
            c0452 FLOAT,
            c0454 FLOAT,
            c0511 FLOAT,
            c0520 FLOAT,
            c0531 FLOAT,
            c0533 FLOAT,
            c0540 FLOAT,
            c0551 FLOAT,
            c0552 FLOAT,
            c0561 FLOAT,
            c0562 FLOAT,
            c0611 FLOAT,
            c0613 FLOAT,
            c0621 FLOAT,
            c0622 FLOAT,
            c0623 FLOAT,
            c0630 FLOAT,
            c0690 FLOAT,
            c0711 FLOAT,
            c0712 FLOAT,
            c0713 FLOAT,
            c0721 FLOAT,
            c0722 FLOAT,
            c0723 FLOAT,
            c0724 FLOAT,
            c0732 FLOAT,
            c0733 FLOAT,
            c0734 FLOAT,
            c0735 FLOAT,
            c0736 FLOAT,
            c0810 FLOAT,
            c0820 FLOAT,
            c0830 FLOAT,
            c0911 FLOAT,
            c0912 FLOAT,
            c0913 FLOAT,
            c0914 FLOAT,
            c0931 FLOAT,
            c0933 FLOAT,
            c0934 FLOAT,
            c0935 FLOAT,
            c0941 FLOAT,
            c0942 FLOAT,
            c0943 FLOAT,
            c0951 FLOAT,
            c0952 FLOAT,
            c0954 FLOAT,
            c0960 FLOAT,
            c1010 FLOAT,
            c1020 FLOAT,
            c1040 FLOAT,
            c1050 FLOAT,
            c1111 FLOAT,
            c1112 FLOAT,
            c1120 FLOAT,
            c1211 FLOAT,
            c1213 FLOAT,
            c1232 FLOAT,
            c1252 FLOAT,
            c1254 FLOAT,
            c1270 FLOAT
        );
    """)
                 
                 
# Commit and close the connection
    conn.commit()
    conn.close()
    
# Export the DataFrames to the database
def export_to_database(dataframes, path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    for table_name, dataframe in dataframes.items():
        # If the table already exists, replace it
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Create the table
        dataframe.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()

# Call the functions
create_tables(path)
export_to_database(dataframes, path)    
