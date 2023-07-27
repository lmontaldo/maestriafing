import sys
import os
# Get the current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the module search path
sys.path.append(parent_dir)
import data_loader
from config import DATA_BASE_PATH
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Specify the database path
path=DATA_BASE_PATH
#path = 'C:/Users/Transitorio/Desktop/tesis2023/tesis2023-1/data/mydatabase.db'
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['Datosipc', 'ipc_general_ine','Datos_fmi_2022_external', 'clases_ipc_filtradas']
df_dict = data_loader.get_data(path, tables_list)
df_univariado = df_dict['ipc_general_ine']
df_clases_filter=df_dict['clases_ipc_filtradas']
df_clases = df_dict['Datosipc']
df_fmi = df_dict['Datos_fmi_2022_external']
###########################################
# Preprocessing functions
###########################################
# Create an instance of StandardScaler
scaler = StandardScaler()
#####################################
# IPC general preprocessing
#####################################
df_gral=df_univariado
df_gral[['month','year']]=df_gral.fecha.str.split('-',expand=True)
df_gral['year']=str('20')+df_gral['year']
months = ['ene','feb','mar','abr','may','jun','jul','ago','set','oct','nov','dic']
d = dict(zip(months, np.arange(1, 13)))
df_gral['month']=df_gral['month'].replace(d, regex=True)
df_gral['ymd'] = pd.to_datetime(df_gral[['year', 'month']].assign(day=1), format='%d/%b/%Y')
ipc_gral=df_gral.loc[:,["ymd","indice"]]
ipc_gral_idx=ipc_gral.set_index('ymd')
# log transform
log_gral_idx = np.log1p(ipc_gral_idx)
log_IPC_gral = log_gral_idx.reset_index()

#########################################
# Clases IPC preprocessing
#########################################
ipc_codes_list=df_clases_filter['c_codigo'].unique()
# Filter df based on the values in the list
clases_ipc = df_clases[df_clases['c_codigo'].isin(ipc_codes_list)]
columns_to_drop =['codigo', 'DivisionesGruposClasesFamiliasyProductos']
# Drop the specified columns 
clases_ipc_df = clases_ipc.drop(columns=columns_to_drop)
long_clases= pd.melt(clases_ipc_df, id_vars='c_codigo', var_name='date', value_name='value')
# creating datetime column from date
# Split 'date' column into 'month' and 'year'
long_clases[['month', 'year']] = long_clases['date'].str.split('-', expand=True)
# Update 'year' column to have the complete year format
long_clases['year'] = '20' + long_clases['year']
# Map month abbreviations to month numbers
months = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'set', 'oct', 'nov', 'dic']
month_dict = dict(zip(months, range(1, 13)))
long_clases['month'] = long_clases['month'].replace(month_dict, regex=True)
# Create 'ymd' column with the first day of the month
long_clases['ymd'] = pd.to_datetime(long_clases[['year', 'month']].assign(day=1), format='%d/%b/%Y')
# Sort the DataFrame by the 'ymd' column
long_clases = long_clases.sort_values('ymd')
# Drop 'date', 'month', and 'year' columns
long_clases = long_clases.drop(['date', 'month', 'year'], axis=1)
start_time_clases = long_clases['ymd'].min()
end_time_clases = long_clases['ymd'].max()
wide_clases_idx = long_clases.pivot(index='ymd', columns='c_codigo', values='value')
wide_clases = wide_clases_idx.reset_index()
wide_clases = wide_clases.rename_axis(None)
# log transform
log_clases_idx = np.log1p(wide_clases_idx)
# z-score rescaling
# Apply z-score normalization to the DataFrame
normalized_log_clases_idx = scaler.fit_transform(log_clases_idx)
# Update the DataFrame with the normalized values
log_clases_idx[:] = normalized_log_clases_idx
log_clases=log_clases_idx.reset_index()
#########################################
# IMF data preprocessing- df_fmi
#########################################
cols_px = df_fmi.iloc[:,1:].select_dtypes(exclude=['float']).columns
df_fmi[cols_px] = df_fmi[cols_px].apply(pd.to_numeric, downcast='float', errors='coerce')
df_fmi[['year','month']]=df_fmi.date.str.split('M',expand=True)
df_fmi['ymd'] = pd.to_datetime(df_fmi[['year', 'month']].assign(day=1), format='%d/%b/%Y')
p_usd=df_fmi.drop(['year', 'month','date' ], axis=1)
p_usd = p_usd.sort_values('ymd')
# Truncate the datetime part of fmi prices to match the time span of ipc clases
externos_usd = p_usd[(p_usd['ymd'] >= start_time_clases) & (p_usd['ymd'] <= end_time_clases)]
externos_usd_idx=externos_usd.set_index('ymd')
# log transform
log_externos_usd_idx = np.log1p(externos_usd_idx)
# z-score rescaling
# Apply z-score normalization to the DataFrame
normalized_log_fmi_idx = scaler.fit_transform(log_externos_usd_idx)
# Update the DataFrame with the normalized values
log_externos_usd_idx[:] = normalized_log_fmi_idx
# variables associated with food and beverage
lista_fb=['PBANSOP',
'PBARL',
'PBEEF',
'PCOCO',
'PCOFFOTM',
'PCOFFROB',
'PROIL',
'PFSHMEAL',
'PGNUTS',
'PLAMB',
'PMAIZMT',
'POLVOIL',
'PORANG',
'PPOIL',
'PPORK',
'PPOULT',
'PRICENPQ',
'PSALM',
'PSHRI',
'PSMEA',
'PSOIL',
'PSOYB',
'PSUGAISA',
'PSUGAUSA',
'PSUNO',
'PTEA',
'PWHEAMT', 
'PSORG',
'PTOMATO',
'PMILK', 
'PAPPLE']
# creating a df for food and beverages
df_fb=log_externos_usd_idx[lista_fb]
avg_fb=df_fb.mean(axis = 1).to_frame('avg_fb')
# df for external prices to keep: soy, petroleum, beef and average food
lst_external=['PBEEF','POILAPSP','PSOYB']
ext_prices=log_externos_usd_idx.filter(lst_external)
df_external_idx=pd.concat([ext_prices, avg_fb], axis=1)
df_external=df_external_idx.reset_index()

#########################################
# DB storage
#########################################
# Store the DataFrames in a dictionary
dataframes = {
    'IPC_gral': log_IPC_gral, 
    'CLASES_IPC': log_clases,
    'EXTERNAL': df_external
}

# Create tables in the database
def create_tables(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # If the table already exists, replace it
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS IPC_gral(
            ymd TEXT,
            indice FLOAT
        );
    """)

    # Create log_clases_idx table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CLASES_IPC (
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

    # Create df_external table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EXTERNAL (
            ymd TEXT,
            PBEEF FLOAT,
            POILAPSP FLOAT,
            PSOYB FLOAT,
            avg_fb FLOAT
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
