import pandas as pd
import sys
import os
import pickle
from numpy.linalg import inv
import numpy as np
from sklearn.decomposition import PCA
from scipy.optimize import minimize
from numpy.linalg import inv
import matplotlib.pyplot as plt
from scipy.linalg import cholesky, sqrtm
#from statsmodels.multivariate.pca import PCA
from statsmodels.tsa.api import VAR
from statsmodels.tools.tools import add_constant
import seaborn as sns
from psynlig import pca_scree
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PKL_X_SLOW_FAST_PATH = os.path.join(project_root, "data", "prepro", 'x_slow_fast.pkl') 
PKL_X_SLOW_PATH = os.path.join(project_root, "data", "prepro", 'x_slow.pkl')
PKL_X_FAST_PATH = os.path.join(project_root, "data", "prepro", 'x_fast.pkl')
with open(PKL_X_SLOW_PATH, 'rb') as file:
    sdata = pickle.load(file)
sdata = pd.DataFrame(sdata)
with open(PKL_X_FAST_PATH, 'rb') as file:
    fdata = pickle.load(file)
fdata = pd.DataFrame(fdata)
#
X = sdata.values  # Extract the data as a numpy array
T, n = X.shape  # T is the number of time periods, n is the number of variables
r=5
# Perform PCA to estimate the factors
pca = PCA(n_components=r)  # Choose the number of factors 'r'
F_estimated = pca.fit_transform(X)  # Estimated factors
# Calculate the residual matrix
residuals = X - F_estimated @ Λ.T
# Estimate the covariance matrix of the residuals
Sigma_e = np.cov(residuals, rowvar=False)
# Calculate the inverse of the estimated covariance matrix
Sigma_e_inv = inv(Sigma_e)


