import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from config import image_path
from utils import data_loader 
#from utils.ADF_tests import adf_test 
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from utils.eda_decomposition import *
from utils.plot_saver import PlotSaver
from arch.unitroot import ADF
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Specify the database path
DATA_BASE_PATH
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['EXTERNAL', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df_ext = df_dict['EXTERNAL']
df_clases=df_dict['CLASES_IPC']
df_gral = df_dict['IPC_gral']
############################################
# IPC GENERAL EDA
############################################
df_gral = to_datetime_str(df_gral, 'ymd')
df_gral_idx = df_gral.set_index('ymd')
# Plot the IPC general and save in docs/images
#save_line_plot_df(df_gral_idx, image_path, title='Evolución IPC general en logaritmos y normalizado', xlabel='Fecha', ylabel='Valores IPC')
# Differenciate IPC general
df_gral_idx_diff = df_gral_idx.diff().dropna()
# Plot the differenciated IPC general and save in docs/images
#save_line_plot_df(df_gral_idx_diff, image_path, title='Evolución IPC general en primeras diferencias', xlabel='Fecha', ylabel='Valores')
# Deseasonalize IPC general
df_gral_idx_diff_des = perform_seasonal_adjustment(df_gral_idx_diff)
#save_line_plot_df(df_gral_idx_diff_des, image_path, title='Evolución IPC general en primeras diferencias con ajuste estacional', xlabel='Fecha', ylabel='Valores')
T=len(df_gral_idx_diff_des)
# model c 
def gamma_test(df, critical_value=-3.45):
    results = {}
    gamma_not_zero = pd.DataFrame()
    gamma_zero = pd.DataFrame()
    
    for col in df.columns:
        adf_c = ADF(df[col], trend='ct')
        reg_res_c = adf_c.regression
        tau_tau = reg_res_c.tvalues[0]
        reject_c = tau_tau < critical_value
        
        if reject_c:
            gamma_zero[col] = df[col]
        else:
            gamma_not_zero[col] = df[col]
    
    return gamma_not_zero, gamma_zero

gamma_zero, gamma_not_zero = gamma_test(df_gral_idx_diff_des)

# If gamma=0 then test a_2 given gamma=0: phi_3  
def a_2_test(gamma_zero, critical_value=7.44,r=2,T=T):
    results = {}
    a2_not_zero = pd.DataFrame()
    a2_zero = pd.DataFrame()
    for col in gamma_zero.columns:
    # model c: unrestricted 
        adf_c = ADF(gamma_zero[col], trend='ct')
        reg_res_c = adf_c.regression
        SSR_u = reg_res_c.resid.dot(reg_res_c.resid)
        k=len(reg_res_c.params)
        # model b: restricted
        adf_b = ADF(gamma_zero[col], trend='c')
        reg_res_b = adf_b.regression
        SSR_r = reg_res_b.resid.dot(reg_res_b.resid)
        phi_3=((SSR_r-SSR_u)/r)/(SSR_u/(T-k))
        reject_a2_0 = phi_3 < critical_value
        if reject_a2_0:
            a2_not_zero[col] = gamma_zero[col]
        else:
            a2_zero[col] = gamma_zero[col]
        return a2_not_zero, a2_zero
       
a2_not_zero, a2_zero = a_2_test(df_gral_idx_diff_des)                
            
    
    
    
    