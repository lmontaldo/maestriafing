import pandas as pd
import sys
import os

# Append the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, DATA_BASE_PATH
from utils.adf_tests_arch import ModelsADF

df = pd.read_csv(DATA_BASE_PATH, sep=",", index_col='index')
df_drop=df.drop(["HOUSTMW"], axis=1)
print(df_drop.head())
print(df_drop.shape)