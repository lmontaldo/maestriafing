import pandas as pd
import sys
import os
import pickle
from sklearn.decomposition import PCA 
from statsmodels.multivariate.pca import PCA
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.linalg import sqrtm
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
print(f'Chequeo la presencia de datos faltantes: {sdata.isna().sum().sum()}')
r = 10 # Reemplaza con tu elección
X_t=sdata
pca = PCA(n_components=r)
pca.fit(X_t)
normalized_components = pca.transform(X_t)
# Get the eigenvalues
# Get the explained variances for all components
explained_variances = np.array(pca.explained_variance_ratio_)

# Create an array of component indices (0 to 10)
component_indices = np.arange(10)

# Plot the scree plot with eigenvalues on the y-axis
plt.figure(figsize=(8, 6))
plt.bar(component_indices, explained_variances[:10], color='b', alpha=0.7)
plt.title('Scree Plot with Eigenvalues')
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance (Eigenvalues)')
plt.xticks(component_indices)
plt.grid(axis='y')

plt.show()


PC_values = np.arange(pca.n_components_) + 1
plt.plot(PC_values, 
         pca.explained_variance_ratio_, 
         'ro-')
plt.title('Figure 3: Scree Plot')
plt.xlabel('Principal Components')
plt.ylabel('Proportion of Variance Explained')
plt.show()


max_factors = min(X_t.shape[0], X_t.shape[1])  # Maximum possible number of factors
icp2_values = []

for r in range(1, max_factors + 1):
    # Fit PCA with r components
    pca = PCA(n_components=r)
    pca.fit(X_t)
    
    # Calculate the residual sum of squares (RSS) for the model with r factors
    rss_r = np.sum(np.square(X_t - pca.inverse_transform(pca.transform(X_t))))
    
    # Calculate ICp2
    icp2 = np.log(rss_r) + r * (2 * X_t.shape[0] / X_t.shape[1]) * np.log(X_t.shape[1])
    
    icp2_values.append(icp2)

# Find the optimal number of factors that minimizes ICp2
optimal_num_factors = np.argmin(icp2_values) + 1  # Add 1 because factors are 1-indexed

print(f"Optimal Number of Factors (ICp2): {optimal_num_factors}")


pc = PCA(X_t, standardize=False)
pc.factors.shape