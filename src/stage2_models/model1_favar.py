import pandas as pd
import numpy as np
import sys
import os
import pickle
from sklearn.decomposition import PCA
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)
# Now you can import config
from config import PKL_X_SLOW_FAST_PATH

with open(PKL_X_SLOW_FAST_PATH, 'rb') as file:
    xdf = pickle.load(file)
#
print(xdf.head())    
    