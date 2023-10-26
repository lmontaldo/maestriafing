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
# Define the optimization problem and constraints
def objective_function(params, *args):
    Lambda, F = params[:n * r], params[n * r:]
    X, Sigma_e_inv = args[0], args[1]
    T = X.shape[0]
    # Reshape Λ and F
    Λ = Λ.reshape(n, r)
    F = F.reshape(r, T)
    # Calculate the residuals
    residuals = X.T -  @ F
    # Calculate the weighted sum of squared residuals
    weighted_residuals = np.sum((residuals.T @ Sigma_e_inv) * residuals.T, axis=1)
    return np.mean(weighted_residuals)  # Mean over time periods

# Define the constraint for N^(-1)Λ'Λ = I
def constraint(params):
    Lambda=params[:n * r]
    Lambda_t= Lambda.reshape(r, n)
    return  (1/T)*Lambda_t@Lambda- np.eye(r), Lambda_t, Lambda

# Estimate the diagonal weight matrix Σ_e_inv
residuals = X - F_estimated @ Λ.T
Σ_e = np.cov(residuals, rowvar=False)
Σ_e_inv = inv(Σ_e)  

# Set up the optimization problem
initial_guess = np.random.randn(n * r + r * T)
constraints = [{'type': 'eq', 'fun': constraint}]

# Perform the optimization
result = minimize(objective_function, initial_guess, args=(X, Σ_e_inv), constraints=constraints)

# Extract the optimized values
optimized_params = result.x
Λ_optimized = optimized_params[:n * r].reshape(n, r)
F_optimized = optimized_params[n * r:].reshape(r, T)

print("Optimized Λ:")
print(Λ_optimized)
print("Optimized F:")
print(F_optimized)


