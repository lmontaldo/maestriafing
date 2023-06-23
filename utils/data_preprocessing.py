import data_loader

# Specify the database path
path = 'C:/Users/Transitorio/Desktop/tesis2023/tesis2023-1/data/mydatabase.db'

# Retrieve the DataFrames from data_loader
df_clases, df_univariado, df_fmi = data_loader.get_data(path)

# Perform preprocessing operations using the retrieved DataFrames
# ...
# Example preprocessing steps:
# - Remove unnecessary columns
# - Clean data
# - Transform data
# - Feature engineering
# - etc.

# Print the first few rows of the DataFrames
print("Table data for table 'Datosipc':")
print(df_clases.head())

print("Table data for table 'ipc_univariado':")
print(df_univariado.head())

print("Table data for table 'Datos_fmi_2022_external':")
print(df_fmi.head())
