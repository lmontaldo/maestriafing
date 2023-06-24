import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
import data_loader
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Specify the database path
path = 'C:/Users/Transitorio/Desktop/tesis2023/tesis2023-1/data/mydatabase.db'
# Retrieve the DataFrames from data_loader
df_clases, df_univariado, df_fmi, df_clases_filter, df_IPC_gral, df_CLASES_IPC, df_EXTERNAL = data_loader.get_data(path)
#############################################
print(df_IPC_gral.head())
