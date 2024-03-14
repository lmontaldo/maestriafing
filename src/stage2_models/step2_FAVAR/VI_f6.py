import pandas as pd
import sys
import os
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
sys.path.append(project_root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_Y_PATH = os.path.join(project_root, "data", "variable_importance", 'abs_lambda_F6.csv') 
# read data  
ng= pd.read_csv("/Users/lauramontaldo/Desktop/lau/maestriafing/data/variable_importance/ng.csv")
df= pd.read_csv("/Users/lauramontaldo/Desktop/lau/maestriafing/data/variable_importance/abs_lambda_F6.csv", sep=",",  index_col=0)
df=df.T
df_sin_idx=df.reset_index()
print(df)
print(ng)
merged_df = pd.merge(df, ng[['fred', 'group']], left_index=True, right_on='fred', how='left')
#grouped_df = merged_df.groupby('group')
#mean_by_group = grouped_df.mean()

#mean_by_group = grouped_df.mean()
merged_df.drop('fred', axis=1, inplace=True)
#print(merged_df.head()) 
#print(mean_by_group) 
mean_df=merged_df.groupby('group').mean()

mean_df.columns = mean_df.columns.str.replace('^matriz_fhat', '', regex=True)
print(mean_df)

import seaborn as sns
import matplotlib.pyplot as plt

# Assuming df is your DataFrame

# Create a heatmap
# Create a heatmap with 'Blues' colormap
# Create a heatmap with 'Blues' colormap and 14-point font size for annotations
plt.figure(figsize=(15, 8))  # Adjust the figure size as needed
sns.heatmap(mean_df, cmap='Blues', annot=True, fmt=".2f", annot_kws={"size": 14})  # Set font size to 14
plt.title('Contribución de cada grupo de variables a cada PC', fontsize=16)  # Set the title font size to 16
plt.xlabel('Componentes principales', fontsize=14)  # Set the label font size to 14
plt.ylabel('Grupo de variables', fontsize=14)  # Set the label font size to 14
plt.tight_layout()  # Adjust layout to ensure all labels fit within the plot
plt.show()
