import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# Append the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR, DATA_BASE_PATH
from utils.adf_tests_arch import ModelsADF
from arch.unitroot import ADF

df = pd.read_csv(DATA_BASE_PATH, sep=",", index_col='index')
HOUSTMW=df['HOUSTMW']
stl_result = STL(HOUSTMW, seasonal=13, period=12).fit()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))

# Original Time Series
ax1.plot(HOUSTMW)
ax1.set_title('Original Time Series')

# Trend Component
ax2.plot(stl_result.trend)
ax2.set_title('Trend Component')

# Seasonal Component
ax3.plot(stl_result.seasonal)
ax3.set_title('Seasonal Component')

# Residual Component
ax4.plot(stl_result.resid)
ax4.set_title('Residual Component')

plt.tight_layout()
plt.show()

# Plot ACF and PACF for the original time series
plt.figure(figsize=(12, 4))
plt.subplot(121)
plot_acf(HOUSTMW, lags=40, ax=plt.gca())
plt.title('ACF for Original Time Series')

plt.subplot(122)
plot_pacf(HOUSTMW, lags=40, ax=plt.gca())
plt.title('PACF for Original Time Series')

plt.tight_layout()
plt.show()
adf_test = ADF(stl_result.resid,trend='ct' )
adf_test_result = adf_test.summary()
print(adf_test_result)


result = sm.tsa.seasonal_decompose(HOUSTMW, model='additive', period=12)  # Change 'period' according to your data's seasonality
fig, axs = plt.subplots(4, 1, figsize=(10, 8))

axs[0].plot(HOUSTMW)
axs[0].set_title('Original Time Series')

axs[1].plot(result.trend)
axs[1].set_title('Trend Component')

axs[2].plot(result.seasonal)
axs[2].set_title('Seasonal Component')

axs[3].plot(result.resid)
axs[3].set_title('Residual Component')

plt.tight_layout()
plt.show()






