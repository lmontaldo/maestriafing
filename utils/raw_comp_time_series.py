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
from utils.log_norm import *
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
import lista_food
#############################################
# Retrieve the DataFrames from data_loader
#############################################
path=DATA_BASE_PATH
tables_list= ['Datosipc', 'clases_ipc_filtradas']
df_dict = data_loader.get_data(path, tables_list)
df_clases_filter=df_dict['clases_ipc_filtradas']
df_clases = df_dict['Datosipc']

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
start_time_clases=wide_clases['ymd'].min()
end_time_clases=wide_clases['ymd'].min()
log1_clases_idx = transform_log1(wide_clases, index_column='ymd')
log1_clases= log1_clases_idx.reset_index()
transf_clases_idx=normalization(log1_clases, index_column='ymd')
print(transf_clases_idx.head())





#########################################
# DB storage
#########################################
# Store the DataFrames in a dictionary
dataframes = {
    'CLASES_IPC': transf_clases_idx
}

# Create tables in the database
def create_tables(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # Create log_clases_idx table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transf_componentes (
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
