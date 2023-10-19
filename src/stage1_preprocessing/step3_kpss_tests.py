import pandas as pd
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
prepro_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
from utils.kpss_tests_arch import KPSSAnalysis

df = pd.read_csv(prepro_file_path, sep=",", index_col='index')
print(f"Cantidad de columnas a testear: {df.shape[1]}\n")


print("################################ TESTS KPSS #########################################################")

kpss_analysis = KPSSAnalysis(df)
kpss_analysis.perform_test()
trends = ['ct', 'c']
for trend in trends:
    for nlags in kpss_analysis.nlags_list:
        print(f"Results for model={trend} and nlags method={nlags}:")
        df_results = kpss_analysis.get_results_for_trend_nlags(trend, nlags)
        stationary_df = kpss_analysis.get_stationary_for_trend_nlags(trend, nlags)
        non_stationary_df = kpss_analysis.get_non_stationary_for_trend_nlags(trend, nlags)
        print("-------------------------------------------------------------")
        #print(f"\nDataFrame named {trend}_{nlags}:")
        #print(df_results)
        print(f"\nList of Stationary series for model={trend} and nlags method={nlags}:")
        print(list(stationary_df.index))  # Get the index (column names) of the stationary DataFrame
        print(f"\nList of Non-Stationary series for model={trend} and nlags method={nlags}:")
        print(list(non_stationary_df.index))
        
        # Fetch and print counts
        stationary_count = kpss_analysis.get_stationary_count_for_trend_nlags(trend, nlags)
        non_stationary_count = kpss_analysis.get_non_stationary_count_for_trend_nlags(trend, nlags)
        
        print(f"\nCount of Stationary series for model={trend} and nlags method={nlags}: {stationary_count}")
        print(f"\nCount of Non-Stationary series for model={trend} and nlags method={nlags}: {non_stationary_count}")

        print("-------------------------------------------------------------")

