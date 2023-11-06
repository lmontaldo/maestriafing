import pandas as pd
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
from utils.kpss_tests_arch import KPSSAnalysis
prepro_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
imputed_file_path = os.path.join(project_root, "data", "prepro", "imputed_na_fred_data.csv")

df = pd.read_csv(imputed_file_path, sep=",")
df.set_index('date', inplace=True)

print(f"Cantidad de columnas a testear: {df.shape[1]}\n")
print("################################ TESTS KPSS #########################################################")

kpss_analysis = KPSSAnalysis(df)
kpss_analysis.perform_test()

trends = ['ct', 'c']

# Initialize variables to keep track of the maximum stationary count and its associated trend, nlags, and stationary/non-stationary series lists
max_stationary_count = 0
best_model = None
best_lags = None
best_stationary_series = []
best_non_stationary_series = []

for trend in trends:
    for nlags in kpss_analysis.nlags_list:
        print(f"Results for model={trend} and nlags method={nlags}:")
        df_results = kpss_analysis.get_results_for_trend_nlags(trend, nlags)
        stationary_df = kpss_analysis.get_stationary_for_trend_nlags(trend, nlags)
        non_stationary_df = kpss_analysis.get_non_stationary_for_trend_nlags(trend, nlags)

        # Fetch and print counts
        stationary_count = kpss_analysis.get_stationary_count_for_trend_nlags(trend, nlags)
        non_stationary_count = kpss_analysis.get_non_stationary_count_for_trend_nlags(trend, nlags)

        print(f"\nCount of Stationary series for model={trend} and nlags method={nlags}: {stationary_count}\n")
        print(f"\nCount of Non-Stationary series for model={trend} and nlags method={nlags}: {non_stationary_count}")

        if stationary_count > max_stationary_count:
            max_stationary_count = stationary_count
            min_non_estat_count=non_stationary_count
            best_model = trend
            best_lags = nlags
            best_stationary_series = list(stationary_df.index)
            best_non_stationary_series = list(non_stationary_df.index)

        print("-------------------------------------------------------------")

print(f"\nBest model and lags combination with the highest stationary count:")
print(f"Model={best_model}, NLags={best_lags}, Count_stationaries={max_stationary_count}, Count_non_stationaries={min_non_estat_count}")
print(f"\nList of Stationary series for the best combination:")
print(best_stationary_series)
print(f"\nList of Non-Stationary series for the best combination:")
print(best_non_stationary_series)




