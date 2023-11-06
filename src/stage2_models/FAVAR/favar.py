import pandas as pd
import sys
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import cholesky, sqrtm
from statsmodels.multivariate.pca import PCA
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

pca_model = PCA(sdata, standardize=False, demean=True)
pca_model.plot_scree(log_scale=False)
plt.show()


data_centered = sdata - sdata.mean()
# Perform the Cholesky decomposition for factor normalization
factor_loadings = cholesky(data_centered.T @ data_centered, lower=True).T
# Compute the factors
factors = data_centered @ factor_loadings
# Fit a PCA model to your factors
pca_model = PCA(factors, ncomp=15)

# Calculate the eigenvalues from the PCA
eigenvalues = pca_model.eigenvals

# Calculate the proportion of explained variance
explained_variance_ratio = eigenvalues / eigenvalues.sum()

# Plot the scree plot
plt.plot(np.arange(1, 16), explained_variance_ratio, marker='o')
plt.xlabel('Number of Factors')
plt.ylabel('Proportion of Explained Variance')
plt.title('Scree Plot')
plt.grid(True)

# Calculate the information criteria (IC_P2)
aic_values = []
bic_values = []

for k in range(1, 16):
    var_model = VAR(factors[:, :k])
    var_results = var_model.fit()
    aic_values.append(var_results.aic)
    bic_values.append(var_results.bic)

# Plot AIC and BIC values
plt.figure()
plt.plot(np.arange(1, 16), aic_values, marker='o', label='AIC')
plt.plot(np.arange(1, 16), bic_values, marker='x', label='BIC')
plt.xlabel('Number of Factors')
plt.ylabel('Information Criteria Value')
plt.title('Information Criteria (AIC and BIC)')
plt.legend()
plt.grid(True)

plt.show()
