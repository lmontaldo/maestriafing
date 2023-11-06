import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
prepro_file_path = os.path.join(project_root, "data", "prepro", "datos_fred_procesados.csv")
from utils.f_statistics_ADF_arch import TestStatistics
#
df = pd.read_csv(prepro_file_path, sep=",", index_col='index')
test_stats = TestStatistics()
selected_columns = ['HOUSTMW']
print("Se testea H_0)gamma=0")
results = test_stats.tau_tau(df, columns=selected_columns, critical_value=-3.41)
rh0_df = results['rh0']  # Columns that reject the null hypothesis
no_rh0_df = results['no_rh0']  # Columns that do not reject the null hypothesis
rho_list = results['rho_list']  # List of columns that reject the null hypothesis
no_rho_list = results['no_rho_list']  # List of columns that do not reject the null hypothesis
print("Columns that reject the null hypothesis:")
print(rh0_df.head())
print("\nColumns that do not reject the null hypothesis:")
print(no_rh0_df.head())
print("\nList of columns that reject the null hypothesis:")
print(rho_list)
print("\nList of columns that do not reject the null hypothesis:")
print(no_rho_list)
print("-------------------------------------------------------")
print("-------------------------------------------------------")
print("Se testea H_0) gamma=a_2=0")
results = test_stats.phi_3(df, cols_norho=selected_columns, critical_value=7.44)
rh0_df = results['rh0']  # Columns that reject the null hypothesis
no_rh0_df = results['no_rh0']  # Columns that do not reject the null hypothesis
rho_list = results['rho_list']  # List of columns that reject the null hypothesis
no_rho_list = results['no_rho_list']  # List of columns that do not reject the null hypothesis
print("Columns that reject the null hypothesis:")
print(rh0_df.head())
print("\nColumns that do not reject the null hypothesis:")
print(no_rh0_df.head())
print("\nList of columns that reject the null hypothesis:")
print(rho_list)
print("\nList of columns that do not reject the null hypothesis:")
print(no_rho_list)
print("-------------------------------------------------------")
print("-------------------------------------------------------")
print("Se testea H_0) gamma=a_2=0=a_0=0")
results = test_stats.phi_2(df, cols_norho=selected_columns, critical_value=7.44)
rh0_df = results['rh0']  # Columns that reject the null hypothesis
no_rh0_df = results['no_rh0']  # Columns that do not reject the null hypothesis
rho_list = results['rho_list']  # List of columns that reject the null hypothesis
no_rho_list = results['no_rho_list']  # List of columns that do not reject the null hypothesis
print("Columns that reject the null hypothesis:")
print(rh0_df.head())
print("\nColumns that do not reject the null hypothesis:")
print(no_rh0_df.head())
print("\nList of columns that reject the null hypothesis:")
print(rho_list)
print("\nList of columns that do not reject the null hypothesis:")
print(no_rho_list)
print("-------------------------------------------------------")
print("-------------------------------------------------------")
results_all = test_stats.tau_mu(df, columns=selected_columns)
print("Results for all columns:")
print("Reject Null Hypothesis Columns:")
print(results_all[0])
print("Do Not Reject Null Hypothesis Columns:")
print(results_all[1])
print("-------------------------------------------------------")
print("-------------------------------------------------------")
plt.figure(figsize=(12, 6))  # Set the figure size
sns.lineplot(x=df.index, y='HOUSTMW', data=df, label='Time Series')
plt.title('Time Series Line Plot')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
plt.savefig('time_series_plot.png', dpi=300, bbox_inches='tight')








