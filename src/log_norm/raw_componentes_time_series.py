import os
import sys
sys.path.append("C:\\Users\\user\\Desktop\\preprocesamiento")
import pandas as pd
import numpy as np
import sqlite3
from config import DATA_BASE_PATH
from config import TABLE_SCHEMA_C
from utils.data_loader import *
from utils.log_norm import transform_log1, normalization
from sklearn.preprocessing import StandardScaler

# Constants
MONTHS = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'set', 'oct', 'nov', 'dic']

# Function to retrieve dataframes
def retrieve_dataframes():
    path = DATA_BASE_PATH
    tables_list = ['Datosipc', 'clases_ipc_filtradas']
    return get_data(path, tables_list)

# Function to preprocess 'clases_ipc'
def preprocess_clases_ipc(df_clases, df_clases_filter):
    ipc_codes_list = df_clases_filter['c_codigo'].unique()
    clases_ipc = df_clases[df_clases['c_codigo'].isin(ipc_codes_list)]
    clases_ipc_df = clases_ipc.drop(columns=['codigo', 'DivisionesGruposClasesFamiliasyProductos'])
    long_clases = pd.melt(clases_ipc_df, id_vars='c_codigo', var_name='date', value_name='value')
    long_clases[['month', 'year']] = long_clases['date'].str.split('-', expand=True)
    long_clases['year'] = '20' + long_clases['year']
    month_dict = dict(zip(MONTHS, range(1, 13)))
    long_clases['month'] = long_clases['month'].replace(month_dict, regex=True)
    long_clases['ymd'] = pd.to_datetime(long_clases[['year', 'month']].assign(day=1))
    long_clases = long_clases.sort_values('ymd').drop(['date', 'month', 'year'], axis=1)
    wide_clases_idx = long_clases.pivot(index='ymd', columns='c_codigo', values='value')
    wide_clases = wide_clases_idx.reset_index()
    wide_clases = wide_clases.rename_axis(None)
    return wide_clases 

# Function to transform and normalize 'clases_ipc'
def transform_and_normalize(wide_clases):
    if 'ymd' in wide_clases.columns:
        wide_clases.set_index('ymd', inplace=True)
    scaler = StandardScaler()
    log_clases_idx = np.log1p(wide_clases)
    normalized_log_clases_idx = scaler.fit_transform(log_clases_idx)
    log_clases_idx[:] = normalized_log_clases_idx
    log_norm_clases = log_clases_idx.reset_index()
    log_norm_clases['ymd'] = log_norm_clases['ymd'].astype(str)
    start_time_clases = log_norm_clases['ymd'].min()
    end_time_clases = log_norm_clases['ymd'].max()
    return log_norm_clases, start_time_clases, end_time_clases


# Function to create table in database
def create_tables(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    sql_statement = f"CREATE TABLE IF NOT EXISTS componentes_log_norm ({TABLE_SCHEMA_C});"
    cursor.execute(sql_statement)
    conn.commit()
    conn.close()

# Function to export processed data back to database
def export_to_database(dataframes, path):
    conn = sqlite3.connect(path)
    for table_name, dataframe in dataframes.items():
        dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

# Main execution
def main():
    path=DATA_BASE_PATH
    df_dict = retrieve_dataframes()
    df_clases_filter = df_dict['clases_ipc_filtradas']
    df_clases = df_dict['Datosipc']
    wide_clases= preprocess_clases_ipc(df_clases, df_clases_filter)
    log_norm_clases, start_time_clases, end_time_clases = transform_and_normalize(wide_clases)
    dataframes = {'componentes_log_norm': log_norm_clases}
    create_tables(path)
    export_to_database(dataframes, path)
    return log_norm_clases, start_time_clases, end_time_clases

if __name__ == '__main__':
    log_norm_clases, start_time_clases, end_time_clases= main()
    print(log_norm_clases.head())
    