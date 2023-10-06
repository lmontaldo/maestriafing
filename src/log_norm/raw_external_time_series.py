import os
import sys
sys.path.append("C:\\Users\\user\\Desktop\\preprocesamiento")
import pandas as pd
import numpy as np
import sqlite3
from config import DATA_BASE_PATH
from utils.data_loader import *
from utils.log_norm import transform_log1, normalization
from raw_componentes_time_series import main as componentes_main
from utils.lista_food import lista_fb
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
def retrieve_dataframes():
    path = DATA_BASE_PATH
    tables_list = ['Datos_fmi_2022_external']
    return get_data(path, tables_list)

def prepare_fmi_data(df_fmi, start_time_clases, end_time_clases):
    cols_px = df_fmi.iloc[:,1:].select_dtypes(exclude=['float']).columns
    df_fmi[cols_px] = df_fmi[cols_px].apply(pd.to_numeric, downcast='float', errors='coerce')
    df_fmi[['year','month']] = df_fmi.date.str.split('M',expand=True)
    df_fmi['ymd'] = pd.to_datetime(df_fmi[['year', 'month']].assign(day=1), format='%d/%b/%Y')
    p_usd = df_fmi.drop(['year', 'month','date'], axis=1)
    p_usd = p_usd.sort_values('ymd')
    externos_usd= p_usd[(p_usd['ymd'] >= start_time_clases) & (p_usd['ymd'] <= end_time_clases)]
    return externos_usd


def compute_avg_food(externos_usd, lista_fb=lista_fb):
    if 'ymd' in externos_usd.columns: 
        externos_usd.set_index('ymd', inplace=True)
    food_df = externos_usd[lista_fb]
    log_food_idx = np.log1p(food_df)
    normalized_log_food_idx= scaler.fit_transform(log_food_idx)
    log_food_idx[:]=normalized_log_food_idx
    avg_food_idx = log_food_idx.mean(axis=1).to_frame('avg_fb')
    log_norm_avg_f=avg_food_idx.reset_index()
    log_norm_avg_f['ymd'] = log_norm_avg_f['ymd'].astype(str)
    return log_norm_avg_f

def prepare_external_prices(externos_usd):
    if 'ymd' in externos_usd.columns: 
        externos_usd.set_index('ymd', inplace=True)    
    lst_external = ['PBEEF','POILAPSP','PSOYB']
    ext_prices_df = externos_usd.filter(lst_external)
    log_ext_prices_df = np.log1p(ext_prices_df)
    normalized_log_ext = scaler.fit_transform(log_ext_prices_df)
    log_ext_prices_df[:]=normalized_log_ext
    log_ext_prices_df = log_ext_prices_df.reset_index()  # Reset the index so 'ymd' becomes a column again
    log_ext_prices_df['ymd'] = log_ext_prices_df['ymd'].astype(str)
    return log_ext_prices_df

def join_df(avg_food_df, log_ext_prices_df):
    return avg_food_df.merge(log_ext_prices_df, on='ymd')




def create_tables(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS externos_log_norm (
            ymd TEXT,
            PBEEF FLOAT,
            POILAPSP FLOAT,
            PSOYB FLOAT,
            avg_fb FLOAT
        );
    """)
    conn.close()
    
def export_to_database(dataframes, path):
    conn = sqlite3.connect(path)
    for table_name, dataframe in dataframes.items():
        dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()    

def main():
    path = DATA_BASE_PATH
    _, start_time_clases, end_time_clases = componentes_main()
    df_dict = retrieve_dataframes()
    df_fmi = df_dict['Datos_fmi_2022_external']
    externos_usd = prepare_fmi_data(df_fmi, start_time_clases, end_time_clases)
    food_avg=compute_avg_food(externos_usd)
    precios_ext = prepare_external_prices(externos_usd)
    df_exter=join_df(food_avg, precios_ext)
    create_tables(path)
    dataframes = {'externos_log_norm': df_exter}
    export_to_database(dataframes, path)
    return df_exter

if __name__ == "__main__":
    f_exter = main()
    print(f_exter)

