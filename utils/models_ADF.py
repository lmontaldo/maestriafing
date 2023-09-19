import pandas as pd
from arch.unitroot import ADF
import statsmodels.api as sm
from scipy import stats
from scipy.stats import norm
import numpy as np
from scipy import stats


class ModelsADF:
    
    @staticmethod
    def adf_ct(df, alfa=0.05):
        """
        Perform the Augmented Dickey-Fuller (ADF) test with a constant and linear time trend on all columns of a given DataFrame.

        The ADF test tests the null hypothesis that a unit root is present in a time series. 
        A rejection of the null hypothesis indicates that the time series is stationary.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the time series data. Each column is treated as a separate time series.
                
        alfa : float, optional
            Significance level for the test. Default is 0.05.

        Returns:
        --------
        df_results : pandas.DataFrame
            A DataFrame with columns 'stat', 'p-value', 'number of lags', and 'Result', indexed by the original column names.
        
        RU : pandas.DataFrame
            A subset of df_results containing only the series that have a unit root.
        
        not_RU : pandas.DataFrame
            A subset of df_results containing only the series that do not have a unit root.
        
        RU_count : int
            The number of series that have a unit root.
        
        not_RU_count : int
            The number of series that do not have a unit root.
        
        RU_series : list
            List of names of the series that have a unit root.
        
        not_RU_series : list
            List of names of the series that do not have a unit root.
                
        Note:
        -----
        This function uses the arch.unitroot.ADF function with the "ct" (constant and linear time trend) option.
        
        """
        # Lists to store results
        columns = []
        stats = []
        p_values = []
        lags_used = []
        unit_root_results = []
        df = df.copy()
        for column in df.columns:
            series = df[column]
            adf_result = ADF(series,trend="ct", method="aic")
            columns.append(column)
            stats.append(adf_result.stat)
            p_values.append(adf_result.pvalue)
            lags_used.append(adf_result.lags)
            unit_root_results.append('No RU' if adf_result.pvalue <= alfa else 'RU')

        df_results = pd.DataFrame({
            'stat': stats,
            'p-value': p_values,
            'number of lags': lags_used,
            'Result': unit_root_results
        }, index=columns)
         # Split df_results based on 'Result' column
        RU = df_results[df_results['Result'] == 'RU']
        not_RU = df_results[df_results['Result'] == 'No RU']
        # Get the count of RU and not_RU
        RU_count = RU.shape[0]
        not_RU_count = not_RU.shape[0]
        # Get the series names (column names from original df) that are RU and not_RU
        RU_series = list(RU.index)
        not_RU_series = list(not_RU.index)
        return df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series
    
    @staticmethod
    def adf_c(df, alfa=0.05):
        """
        Perform the Augmented Dickey-Fuller (ADF) test with a constant deterministic trend on all columns of a given DataFrame.

        The ADF test tests the null hypothesis that a unit root is present in a time series. 
        A rejection of the null hypothesis indicates that the time series is stationary.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the time series data. Each column is treated as a separate time series.
                
        alfa : float, optional
            Significance level for the test. Default is 0.05.

        Returns:
        --------
        df_results : pandas.DataFrame
            A DataFrame with columns 'stat', 'p-value', 'number of lags', and 'Result', indexed by the original column names.
        
        RU : pandas.DataFrame
            A subset of df_results containing only the series that have a unit root.
        
        not_RU : pandas.DataFrame
            A subset of df_results containing only the series that do not have a unit root.
        
        RU_count : int
            The number of series that have a unit root.
        
        not_RU_count : int
            The number of series that do not have a unit root.
        
        RU_series : list
            List of names of the series that have a unit root.
        
        not_RU_series : list
            List of names of the series that do not have a unit root.
                
        Note:
        -----
        This function uses the arch.unitroot.ADF function with the "c" (constant deterministic trend) option.
        
        """
        # Lists to store results
        columns = []
        stats = []
        p_values = []
        lags_used = []
        unit_root_results = []
        df = df.copy()
        for column in df.columns:
            series = df[column]
            adf_result = ADF(series,trend="c", method="aic")
            columns.append(column)
            stats.append(adf_result.stat)
            p_values.append(adf_result.pvalue)
            lags_used.append(adf_result.lags)
            unit_root_results.append('No RU' if adf_result.pvalue <= alfa else 'RU')

        df_results = pd.DataFrame({
            'stat': stats,
            'p-value': p_values,
            'number of lags': lags_used,
            'Result': unit_root_results
        }, index=columns)
         # Split df_results based on 'Result' column
        RU = df_results[df_results['Result'] == 'RU']
        not_RU = df_results[df_results['Result'] == 'No RU']
        # Get the count of RU and not_RU
        RU_count = RU.shape[0]
        not_RU_count = not_RU.shape[0]
        # Get the series names (column names from original df) that are RU and not_RU
        RU_series = list(RU.index)
        not_RU_series = list(not_RU.index)
        return df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series
    
    @staticmethod
    def adf_n(df, alfa=0.05):
        """
        Perform the Augmented Dickey-Fuller (ADF) test with no deterministic trend on all columns of a given DataFrame.

        The ADF test tests the null hypothesis that a unit root is present in a time series. 
        A rejection of the null hypothesis indicates that the time series is stationary.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the time series data. Each column is treated as a separate time series.
            
        alfa : float, optional
            Significance level for the test. Default is 0.05.

        Returns:
        --------
        df_results : pandas.DataFrame
            A DataFrame with columns 'stat', 'p-value', 'number of lags', and 'Result', indexed by the original column names.
        
        RU : pandas.DataFrame
            A subset of df_results containing only the series that have a unit root.
        
        not_RU : pandas.DataFrame
            A subset of df_results containing only the series that do not have a unit root.
        
        RU_count : int
            The number of series that have a unit root.
        
        not_RU_count : int
            The number of series that do not have a unit root.
        
        RU_series : list
            List of names of the series that have a unit root.
        
        not_RU_series : list
            List of names of the series that do not have a unit root.
            
        Note:
        -----
        This function uses the arch.unitroot.ADF function with the "n" (no deterministic trend) option.
        """
        columns = []
        stats = []
        p_values = []
        lags_used = []
        unit_root_results = []
        df = df.copy()
        for column in df.columns:
            series = df[column]
            adf_result = ADF(series,trend="n", method="aic")
            columns.append(column)
            stats.append(adf_result.stat)
            p_values.append(adf_result.pvalue)
            lags_used.append(adf_result.lags)
            unit_root_results.append('No RU' if adf_result.pvalue <= alfa else 'RU')

        df_results = pd.DataFrame({
            'stat': stats,
            'p-value': p_values,
            'number of lags': lags_used,
            'Result': unit_root_results
        }, index=columns)
         # Split df_results based on 'Result' column
        RU = df_results[df_results['Result'] == 'RU']
        not_RU = df_results[df_results['Result'] == 'No RU']
        # Get the count of RU and not_RU
        RU_count = RU.shape[0]
        not_RU_count = not_RU.shape[0]
        # Get the series names (column names from original df) that are RU and not_RU
        RU_series = list(RU.index)
        not_RU_series = list(not_RU.index)
        return df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series