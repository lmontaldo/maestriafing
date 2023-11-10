import pandas as pd
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
from utils.adf_tests_arch import ModelsADF
prepro_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
imputed_file_path = os.path.join(project_root, "data", "prepro", "imputed_na_fred_data.csv")
#df = pd.read_csv(prepro_file_path, sep=",", index_col='index')
df = pd.read_csv(imputed_file_path, sep=",")
print(df.head())
df.set_index('date', inplace=True)
#
print(f"\nCantidad de columnas a testear: {df.shape[1]}")
print(f"Cantidad de filas: {df.shape[0]}\n")
#
adf_model = ModelsADF(df, alpha=0.05)
results = adf_model.perform_adf_test()

for trend, trend_results in results.items():
    print("-----------------------------------")
    print("-----------------------------------")
    print(f"Results for trend '{trend}':")

    print("ADF Test Results:")
    #print(trend_results.get('df_results'))  # Using .get() to handle missing key gracefully

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
    





