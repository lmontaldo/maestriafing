import os
import sys
# Get the current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the module search path
sys.path.append(parent_dir)
import pandas as pd
import numpy as np
import sqlite3
from config import DATA_BASE_PATH
from utils.data_loader import *
from utils.log_norm import transform_log1, normalization

def retrieve_dataframes():
    path = DATA_BASE_PATH
    tables_list = ['ipc_general_ine']
    df_univariado = get_data(path, tables_list)
    return get_data(path, tables_list)



def preprocess_ipc_general(df_univariado):
    df_gral = df_univariado.copy()
    df_gral[['month', 'year']] = df_gral.fecha.str.split('-', expand=True)
    df_gral['year'] = '20' + df_gral['year']
    
    months = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'set', 'oct', 'nov', 'dic']
    month_mapping = dict(zip(months, np.arange(1, 13)))
    df_gral['month'] = df_gral['month'].replace(month_mapping)
    df_gral['ymd'] = pd.to_datetime(df_gral[['year', 'month']].assign(day=1))
    return df_gral.loc[:, ["ymd", "indice"]]

def create_tables(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS IPC_gral_log1_norm(
            ymd TEXT,
            indice FLOAT
        );
    """)
    conn.commit()
    conn.close()

def export_to_database(dataframes, path):
    conn = sqlite3.connect(path)
    for table_name, dataframe in dataframes.items():
        dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def main():
    path = DATA_BASE_PATH
    tables_list = ['ipc_general_ine']
    df_dict = get_data(path, tables_list)
    df_univariado = df_dict['ipc_general_ine']
    ipc_gral = preprocess_ipc_general(df_univariado)
    log1_ipc_idx = transform_log1(ipc_gral, index_column='ymd')
    log1_ipc = log1_ipc_idx.reset_index()
    transf_ipc_idx = normalization(log1_ipc, index_column='ymd')
    transf_ipc = transf_ipc_idx.reset_index()

    dataframes = {'IPC_gral': transf_ipc}
    create_tables(path)
    export_to_database(dataframes, path)
    return transf_ipc

if __name__ == '__main__':
    transf_ipc=main()
