import pandas as pd
import sys
import os

# Append the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, DATA_BASE_PATH
from utils.adf_tests_arch import ModelsADF

df = pd.read_csv(DATA_BASE_PATH, sep=",", index_col='index')
print(f"\nCantidad de columnas a testear: {df.shape[1]}")
print(f"Cantidad de filas: {df.shape[0]}\n")
adf_model = ModelsADF(df, alpha=0.05)
results = adf_model.perform_adf_test()

for trend, trend_results in results.items():
    print("-----------------------------------")
    print("-----------------------------------")
    print(f"Results for trend '{trend}':")

    print("ADF Test Results:")
    print(trend_results.get('df_results'))  # Using .get() to handle missing key gracefully

    # Filter column names for stationary and non-stationary series
    stationary_series = trend_results.get('Stationary_series', [])
    non_stationary_series = trend_results.get('Non_stationary_series', [])
    print("-----------------------------------")
    print("Stationary Series Count:", len(stationary_series))
    print("Non-Stationary Series Count:", len(non_stationary_series))
    print("-----------------------------------")

    # Print the series data for stationary series
    print("Stationary Series as a List:")
    print(stationary_series) 

    # Print the non-stationary series as a list
    print(f"\nNon-Stationary Series as a List:")
    print(non_stationary_series)
    print()
    





