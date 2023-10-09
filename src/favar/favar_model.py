# -------------------------------
# IMPORTS
# -------------------------------
# Standard Libraries
import os
import sys
sys.path.append("C:\\Users\\user\\Desktop\\preprocesamiento")
from config import DATA_BASE_PATH
import pandas as pd
import numpy as np
import sqlite3
import time
import warnings
import datetime as dt
import math
import numbers
from statsmodels.tools.sm_exceptions import InterpolationWarning
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from utils import data_loader
from utils.datetime import *
from src.decomposition.stl_loess import *
# -------------------------------
# CONFIGURATIONS
# -------------------------------
warnings.simplefilter('ignore', InterpolationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="seaborn")
#############################################
# Retrieve the DataFrames from database
#############################################
residual_c, residual_ext, _ = load_and_process_data()


# Perform PCA without reducing dimensionality
pca = PCA(n_components=15)
pca.fit(residual_c)

# Get the loadings
loadings = pca.components_

# Identify the column with the largest absolute loading for each component
most_influential_vars = residual_c.columns[np.argmax(np.abs(loadings), axis=1)]

# Get the explained variance by each component
explained_variance = pca.explained_variance_

# Plot the bar scree plot
plt.figure(figsize=(12, 7))
plt.bar(most_influential_vars, explained_variance, alpha=0.7, align='center', label='Individual explained variance')
plt.xlabel('Most Influential Variable for Component')
plt.ylabel('Eigenvalue')
plt.title('Scree Plot (Bar) for the First 15 Components')
plt.gca().yaxis.grid(True, which='major')
plt.xticks(rotation=45)  # Rotate x labels for better visibility
plt.tight_layout()

# Highlight the elbow point
average_variance = np.mean(explained_variance)
elbow = np.where(explained_variance < average_variance)[0][0]
plt.axvline(x=elbow, color='red', linestyle='--', label=f'Elbow at Component {elbow + 1}')
plt.legend()

plt.show()
 
 