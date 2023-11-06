import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


class STL_procedure:
    
    def __init__(self, df, seasonal=13, period=12):
        self.df = df
        self.seasonal = seasonal
        self.period = period

    def decompose_dataframe_stl(self):
        trend = pd.DataFrame(index=self.df.index)
        seasonal_df = pd.DataFrame(index=self.df.index)
        residual = pd.DataFrame(index=self.df.index)

        for column in self.df.columns:
            result = STL(self.df[column], period=self.period, seasonal=self.seasonal, robust=True).fit()
            
            trend[column] = result.trend
            seasonal_df[column] = result.seasonal
            residual[column] = result.resid

        return trend, seasonal_df, residual

    def STL_seasonal_adjusted(self):
        _, seasonal_df, _ = self.decompose_dataframe_stl()
        return self.df - seasonal_df
    
    def STL_detrend(self):
        trend, _, _ = self.decompose_dataframe_stl()
        return self.df - trend

