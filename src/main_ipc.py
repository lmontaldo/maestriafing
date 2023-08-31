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
from utils.eda_decomposition import decompose_dataframe, perform_seasonal_adjustment
from utils.unitroot import *
from utils.pruebas_KPSS import *
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
import matplotlib.pyplot as plt
from arch.unitroot import ADF
import warnings
from statsmodels.tools.sm_exceptions import InterpolationWarning

warnings.simplefilter('ignore', InterpolationWarning)
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

#df_gral_idx = df_gral.set_index('ymd')
# Plot the IPC general and save in docs/images
#save_line_plot_df(df_gral_idx, image_path, title='Evolución IPC general en logaritmos y normalizado', xlabel='Fecha', ylabel='Valores IPC')
# Differenciate IPC general
#df_gral_idx_diff = df_gral_idx.diff().dropna()
#print(df_gral_idx_diff)

# df_gral['ymd'] is in format 'YYYY-MM-DD'
df_gral['ymd'] = pd.to_datetime(df_gral['ymd']).dt.normalize()


# Create a trace
trace = go.Scatter(x=df_gral['ymd'], y=df_gral['indice'], mode='lines', name='IPC general')

# Create a layout
layout = go.Layout(
    title=dict(text='IPC general en primeras diferencias', font=dict(size=24)),
    xaxis=dict(
        title=dict(text='fecha', font=dict(size=18)),
        tickfont=dict(size=20),
    ),
    yaxis=dict(
        title=dict(text='valores en logaritmos y con normalización z', font=dict(size=20)),
        tickfont=dict(size=20),
        range=[0, df_gral['indice'].max()+1]
    )
)

# Create a figure
fig = go.Figure(data=[trace], layout=layout)

# Show the figure
fig.show()

############
df_gral_idx = df_gral.set_index('ymd')
df_gral_idx_diff = df_gral_idx.diff().dropna()
###############################
# Decompose the time series
##############################
result = seasonal_decompose(df_gral_idx_diff['indice'], model='additive', period=12)

# Create subplots
fig = make_subplots(rows=4, cols=1, shared_xaxes=True, 
                     subplot_titles=('Observed', 'Trend', 'Seasonal', 'Residual'))

fig.add_trace(go.Scatter(x=df_gral_idx_diff.index, y=result.observed, mode='lines', showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=df_gral_idx_diff.index, y=result.trend, mode='lines', showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=df_gral_idx_diff.index, y=result.seasonal, mode='lines', showlegend=False), row=3, col=1)
fig.add_trace(go.Scatter(x=df_gral_idx_diff.index, y=result.resid, mode='lines', showlegend=False), row=4, col=1)

fig.update_layout(title='Decomposición de la primer diferencia del IPC general', height=1000, 
                   xaxis_title='Date')

fig.update_yaxes(title_standoff=0)

fig.show()

###############################
# Deseasonalize the time series
##############################
ipc_gral_desea=perform_seasonal_adjustment(df_gral_idx_diff)

# Create a trace
trace = go.Scatter(x=ipc_gral_desea.index, y=ipc_gral_desea['indice'], mode='lines', name='IPC generl en primeras diferencias y desestacionalizado')

# Create a layout
layout = go.Layout(
    title=dict(text='IPC general en primeras diferencias y desestacionalizado', font=dict(size=24)),
    xaxis=dict(
        title=dict(text='fecha', font=dict(size=18)),
        tickfont=dict(size=20),
    ),
    yaxis=dict(
        title=dict(text='valores', font=dict(size=20)),
        tickfont=dict(size=20)
    )
)

# Create a figure
fig = go.Figure(data=[trace], layout=layout)

# Show the figure
fig.show()
#################
mean_value = ipc_gral_desea['indice'].mean()

#########################################
# Compute the ACF and PACF
#######################################
lag_acf = acf(ipc_gral_desea['indice'], nlags=20)
lag_pacf = pacf(ipc_gral_desea['indice'], nlags=20, method='ols')

# Compute the 95% confidence interval
conf_interval = 1.96/np.sqrt(len(ipc_gral_desea['indice']))

# Create subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=('ACF', 'PACF'))

# Create traces
trace_acf = go.Bar(
    x = np.arange(21),
    y = lag_acf,
    name = 'ACF'
)

trace_pacf = go.Bar(
    x = np.arange(21),
    y = lag_pacf,
    name = 'PACF'
)

trace_conf_upper = go.Scatter(
    x = np.arange(21),
    y = [conf_interval]*21,
    mode = 'lines',
    name = '95% Confidence Interval',
    line = dict(dash='dash')
)

trace_conf_lower = go.Scatter(
    x = np.arange(21),
    y = [-conf_interval]*21,
    mode = 'lines',
    name = '95% Confidence Interval',
    line = dict(dash='dash'),
    showlegend=False
)

# Add traces to the figure
fig.add_trace(trace_acf, row=1, col=1)
fig.add_trace(trace_conf_upper, row=1, col=1)
fig.add_trace(trace_conf_lower, row=1, col=1)
fig.add_trace(trace_pacf, row=2, col=1)
fig.add_trace(trace_conf_upper, row=2, col=1)
fig.add_trace(trace_conf_lower, row=2, col=1)

# Set the layout of the figure
fig.update_layout(
    title='ACF y PACF del IPC general en primeras diferencias y desestacionalizado', height=1000,
    template="ggplot2", showlegend=False
)

fig.update_yaxes(title_text="Correlation", row=1, col=1)
fig.update_yaxes(title_text="Correlation", row=2, col=1)
fig.update_xaxes(title_text="Lag", row=2, col=1)

# Show the figure
fig.show()


################################
# ADF with constant
################################
adf_ipc_gral = ADF(ipc_gral_desea)
reg_res = adf_ipc_gral.regression

latex_summary = adf_ipc_gral.summary().as_latex()
#print(latex_summary)

latex_reg_res=reg_res.summary().as_latex()
#print(latex_reg_res)


# instantiate the UnitRootTests class
unit_root_tests = UnitRootTests(ipc_gral_desea)
# call the methods you need
tau_mu_values= unit_root_tests.tau_mu(return_values='tau_mu')
phi_1_values = unit_root_tests.phi_1(return_values='phi_1')
print(f' tau_mu: {tau_mu_values}')
print(f' phi_1: {phi_1_values}')

####################3
# KPSS
####################
analyzer = KPSSAnalyzer(ipc_gral_desea)
analyzer.run_tests()
print(analyzer.results['c_auto'])
print(analyzer.results['c_legacy'])


############################################
# COMPONENTES DEL IPC
############################################
