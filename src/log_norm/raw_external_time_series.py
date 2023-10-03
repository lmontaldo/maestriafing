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
    df_idx=externos_usd.set_index('ymd')
    df_fb = df_idx[lista_fb]
    avg_food_idx= df_fb.mean(axis=1).to_frame('avg_fb')
    avg_food=avg_food_idx.reset_index()
    log_AVG_food_idx = transform_log1(avg_food, index_column='ymd')
    log_AVG_food = log_AVG_food_idx.reset_index()
    return normalization(log_AVG_food, index_column='ymd')

def prepare_external_prices(externos_usd):
    AVG_food_log_norm = compute_avg_food(externos_usd)
    lst_external = ['PBEEF','POILAPSP','PSOYB']
    externos_usd_idx = externos_usd.set_index('ymd')
    ext_prices = externos_usd_idx.filter(lst_external)
    df_external_idx = pd.concat([ext_prices, AVG_food_log_norm], axis=1)
    return df_external_idx.reset_index()

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
    df_externos = prepare_external_prices(externos_usd)
    create_tables(path)
    dataframes = {'externos_log_norm': df_externos}
    export_to_database(dataframes, path)
    
    return df_externos

if __name__ == "__main__":
    df_externos = main()
    print(df_externos.head())

