import os
import sys
sys.path.append("C:\\Users\\user\\Desktop\\preprocesamiento")
import pandas as pd
import numpy as np
import sqlite3
from config import DATA_BASE_PATH
from utils.data_loader import *
from utils.log_norm import transform_log1, normalization
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
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
        CREATE TABLE IF NOT EXISTS IPC_gral_log_norm(
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

    # Apply log1p transformation
    ipc_gral['indice'] = np.log1p(ipc_gral['indice'])

    # Apply normalization using scaler
    ipc_gral['indice'] = scaler.fit_transform(ipc_gral[['indice']])[:, 0]  # Flatten the array and assign

    ipc_gral = ipc_gral.reset_index()  # Reset the index so 'ymd' becomes a column again
    ipc_gral['ymd'] = ipc_gral['ymd'].astype(str)
    
    dataframes = {'IPC_gral_log_norm': ipc_gral}
    create_tables(path)
    export_to_database(dataframes, path)
    return ipc_gral

if __name__ == '__main__':
    transf_ipc = main()
    print(transf_ipc.head())




