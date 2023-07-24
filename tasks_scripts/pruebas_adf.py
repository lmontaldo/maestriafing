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
from utils.unitroot import UnitRootTests
from utils.eda_decomposition import *
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['EXTERNAL', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df_ext = df_dict['EXTERNAL']
df_clases=df_dict['CLASES_IPC']
df_gral = df_dict['IPC_gral']
############################################
# IPC GENERAL: EDA
############################################
df_gral['ymd'] = pd.to_datetime(df_gral['ymd'], format='%Y-%m-%d')
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
#######################################
# Unit root ADF test on IPC general
#######################################
print('\n----------\n')
print('\nThe IPC general has been detrended and deseasonalized so it is expected to be stationary.')
print('Performing Unit Root ADF test')
unit_root = UnitRootTests(df_gral_idx_diff_des)
# tau_tau results
rh0, no_rh0 = unit_root.tau_tau()
print("Columns rejecting the null hypothesis H0)\gamma=0 :")
print(rh0.columns.tolist())
print("Columns not rejecting the null hypothesis H0)\gamma=0 :")
print(no_rh0.columns.tolist())
# Conclusions
# ------------------------------
# Write your conclusions here
conclusion_1 = "It is possible to reject the null hypothesis of unit root at a 5% level."
conclusion_2 = "At a 5% level of significance, the data is stationary."
conclusion_3 = "The data related to IPC general is stationary because it has been detrended and deseasonalized."
############################################
# Clases IPC: EDA
 ############################################
print('\n----------\n')
print('\nThe IPC classes have been detrended and deseasonalized so it is expected to be stationaries.')
print('Performing Unit Root ADF test')
df_clases['ymd'] = pd.to_datetime(df_clases['ymd'], format='%Y-%m-%d')
df_clases_idx=df_clases.set_index('ymd')
# ADF test over normalized logarithms of IPC classes
unit_root_classes = UnitRootTests(df_clases_idx)
# from general to particular
# is \gamma=0?
print('\n----------\n')
print('Estimating model (c), is \gamma=0?') 
rh0_tt, no_rh0_tt = unit_root_classes.tau_tau()
list_rho_tt=rh0_tt.columns.tolist()
list_no_rho_tt=no_rh0_tt.columns.tolist()
#print(f'Columns List that reject H0)\gamma=0 :\n {list_rho_tt}') # No RU then stationary 
print(f'# columns that No RH0): {len(list_no_rho_tt)}\n It is not possible to reject H0)\gamma=0.So test a2=0 given gamma=0.')
print(f'# columns that Rh0): {len(list_rho_tt)}\n It is possible to reject H0)\gamma=0. Then series might be stationary with a 95% confidence level.')
#print(f'Columns List that not reject H0)\gamma=0 :\n {list_no_rho_tt}')

print('\n----------\n')
# phi_2
rh0_phi2, no_rh0_phi2 = unit_root_classes.phi_2(cols_norho=list_no_rho_tt)
print('Using phi_2 statistic for testing \nH0) a_0=a_2=\gamma=0 \nH1) a_0 !=0 and/or a_2 !=0 and/or \gamma !=0: ')
list_no_rh0_phi2=no_rh0_phi2.columns.tolist()
list_rh0_phi2=rh0_phi2.columns.tolist()
#print(f'\nList that Not reject H0) a_0=a_2=\gamma=0 : \n {no_rh0_phi2.columns.tolist()}\nThe coefficients a_0, a_2 and \gamma are zero.')
print(f'# columns that No RH0): {len(list_no_rh0_phi2)}\nIt is possible to accept the null hypothesis of random walk.')
#print(f'\nList that reject H0) a_0=a_2=\gamma=0 : \n {rh0_phi2.columns.tolist()}\nIt is possible to reject the null hypothesis of random walk, so one or more of the coefficients a_0, a_2 and \gamma are not zero.')
print(f'# columns that Rh0): {len(list_rh0_phi2)}\nIt is possible to reject the null hypothesis of random walk against that one or more coefficientes are not equal to zero.')
print('\n----------\n') 

# phi_3
rh0_phi3, no_rh0_phi3 = unit_root_classes.phi_3(cols_norho=list_no_rho_tt)
print('Using phi_3 statistic for testing \nH0) a_2=\gamma=0 \nH1) a_2 !=0 and/or \gamma !=0: ')
list_no_rh0_phi3=no_rh0_phi3.columns.tolist()
list_rh0_phi3=rh0_phi3.columns.tolist()
#print(f'\nList that Not reject H0) a_2=\gamma=0 : \n {no_rh0_phi3.columns.tolist()}\nThe coefficients a_2 and \gamma are zero.')
print(f'# columns that No RH0): {len(list_no_rh0_phi3)}\n It is possible to mantain the hypothesis that the series contain unit root and/or a deterministic trend. Continue to test model (b)')
#print(f'\nList that reject H0) a_2=\gamma=0 : \n {rh0_phi3.columns.tolist()}\nIt is possible to reject the null hypothesis taht one or more of the coefficients a_2 or/and \gamma are not zero.')
print(f'# columns that Rh0): {len(list_rh0_phi3)}\n It is possible to accept that the columns are TS. Algorithm should continue, test id \gamma=0 with normal distribution')

# is \gamma=0?
print('\n----------\n')
print('Estimating model (b), is \gamma=0?') 
rh0_tmu, no_rh0_tmu = unit_root_classes.tau_mu()
list_rho_tmu=rh0_tmu.columns.tolist()
list_no_rho_tmu=no_rh0_tmu.columns.tolist()
#print(f'\nList that Not reject H0) a_0=a_2=\gamma=0 : \n {no_rh0_phi2.columns.tolist()}\nThe coefficients a_0, a_2 and \gamma are zero.')
print(f'# columns that Rh0): {len(list_rho_tmu)}\nIt is possible to reject H0)\gamma=0. Then series might be stationary with a 95% confidence level.')
print(f'# columns that No RH0): {len(list_no_rho_tmu)}\nIt is possible to not reject H0)\gamma=0.')
#print(f'\nList that reject H0) a_0=a_2=\gamma=0 : \n {rh0_phi2.columns.tolist()}\nIt is possible to reject the null hypothesis of random walk, so one or more of the coefficients a_0, a_2 and \gamma are not zero.')
print('\n----------\n') 
rh0_phi1, no_rh0_phi1 = unit_root_classes.phi_1(cols_norho=list_no_rho_tmu)
print('Using phi_1 statistic for testing \nH0) a_0=\gamma=0 \nH1) a_0 !=0 and/or \gamma !=0: ')
list_no_rh0_phi1=no_rh0_phi1.columns.tolist()
list_rh0_phi1=rh0_phi1.columns.tolist()
#print(f'\nList that Not reject H0) a_2=\gamma=0 : \n {no_rh0_phi3.columns.tolist()}\nThe coefficients a_2 and \gamma are zero.')
print(f'# columns that No RH0): {len(list_no_rh0_phi1)}\n It is possible to mantain the hypothesis that the series contain unit root and/or a constant.')
#print(f'\nList that reject H0) a_2=\gamma=0 : \n {rh0_phi3.columns.tolist()}\nIt is possible to reject the null hypothesis taht one or more of the coefficients a_2 or/and \gamma are not zero.')
print(f'# columns that Rh0): {len(list_rh0_phi1)}\n Algorithm should continue, test id \gamma=0 with normal distribution.')
print('\n----------\n') 
print('Estimating model (a), is \gamma=0?') 
rh0_t, no_rh0_t = unit_root_classes.tau()
list_rho_t=rh0_t.columns.tolist()
list_no_rho_t=no_rh0_t.columns.tolist()
#print(f'\nList that Not reject H0) a_0=a_2=\gamma=0 : \n {no_rh0_phi2.columns.tolist()}\nThe coefficients a_0, a_2 and \gamma are zero.')
print(f'# columns that Rh0): {len(list_rho_t)}\nIt is possible to reject H0)\gamma=0. Then series might be stationary with a 95% confidence level.')
print(f'# columns that No RH0): {len(list_no_rho_t)}\nIt is possible to not reject H0)\gamma=0.')
#print(f'\nList that reject H0) a_0=a_2=\gamma=0 : \n {rh0_phi2.columns.tolist()}\nIt is possible to reject the null hypothesis of random walk, so one or more of the coefficients a_0, a_2 and \gamma are not zero.')
print('\n----------\n') 


'''
# Continue ADF with no stationary series
# Is \gamma=a2=0?
rh0, no_rh0 = unit_root_classes.phi_2_adf()
print("\nColumns rejecting the null hypothesis H0)a2=\gamma=0 :")
list_rho_phi2=rh0.columns.tolist()
print(list_rho_phi2)
print("At 5% of significance level, it is possible to accept the alternative hypothesis that the series are TS.")
print("\nColumns not rejecting the null hypothesis H0)a2=\gamma=0 :")
list_norho_phi2=no_rh0.columns.tolist()
print(list_norho_phi2)
print("At 5% of significance level, it is possible to mantain the hypothesis that the series contain a unit root or/and a deterministic trend.")
#
no_step2_ipc=df_clases_idx[list_rho_phi2]
#test_a2


# 1 diff
#d1_clases_idx=differentiate_dataframe(df_clases_idx)
''' 
 
 