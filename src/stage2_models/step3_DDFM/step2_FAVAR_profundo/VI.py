import pandas as pd
import sys
import os
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_f_PATH = os.path.join(project_root, "data", "FAVAR_profundo", 'F_inv.csv') 
CSV_x_PATH = os.path.join(project_root, "data", "scaled_train_test", 'scaled_train.csv') 

F1= pd.read_csv('/Users/lauramontaldo/Documents/GitHub/n1_draft_tesis/data/FAVAR_profundo/F_inv.csv', sep=",")
train= pd.read_csv('/Users/lauramontaldo/Documents/GitHub/n1_draft_tesis/data/scaled_train_test/scaled_train.csv', sep=",")
print(train.head())
import shap
import xgboost
F1_idx=F1.set_index('date')
train_idx=train.set_index('Index')
y=F1_idx.values
X = train_idx.values
model = xgboost.XGBRegressor().fit(X, y)
explainer = shap.Explainer(model)
shap_values = explainer(X)
shap.summary_plot(shap_values, X)

