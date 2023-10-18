import pandas as pd
import sys
import os
from utils.KPSS_tests_arch import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, DATA_BASE_PATH
from utils.kpss_tests_arch import KPSSAnalysis

df = pd.read_csv(DATA_BASE_PATH, sep=",", index_col='index')
print(f"Cantidad de columnas a testear: {df.shape[1]}\n")


print("################################ TESTS KPSS #########################################################")

kpss_analysis = KPSSAnalysis(df)

# Performing the test
kpss_analysis.perform_test()

# Restricting the loop to only 'c' trend
trends = ['ct', 'c']

for trend in trends:
    for nlags in kpss_analysis.nlags_list:
        print(f"Results for model={trend} and nlags method={nlags}:")
        
        # Retrieve and print results
        df_results = kpss_analysis.get_results_for_trend_nlags(trend, nlags)
        stationary_df = kpss_analysis.get_stationary_for_trend_nlags(trend, nlags)
        non_stationary_df = kpss_analysis.get_non_stationary_for_trend_nlags(trend, nlags)

        print(f"\nDataFrame named {trend}_{nlags}:")
        print(df_results)
        
        print(f"\nList of Stationary series for model={trend} and nlags method={nlags}:")
        print(list(stationary_df.index))  # Get the index (column names) of the stationary DataFrame
        
        print(f"\nList of Non-Stationary series for model={trend} and nlags method={nlags}:")
        print(list(non_stationary_df.index))
        
        # Fetch and print counts
        stationary_count = kpss_analysis.get_stationary_count_for_trend_nlags(trend, nlags)
        non_stationary_count = kpss_analysis.get_non_stationary_count_for_trend_nlags(trend, nlags)
        
        print(f"Count of Stationary series for model={trend} and nlags method={nlags}: {stationary_count}")
        print(f"Count of Non-Stationary series for model={trend} and nlags method={nlags}: {non_stationary_count}")

        print("-------------------------------------------------------------")

