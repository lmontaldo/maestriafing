import pandas as pd
from arch.unitroot import ADF


class ModelsADF:
    """
    Class to perform Augmented Dickey-Fuller test on given DataFrame.
    """
    def __init__(self, df, alpha=0.05):
        """
        Initialize the class with DataFrame and significance level.

        Parameters:
        - df (pd.DataFrame): Data to be tested.
        - alpha (float): Significance level. Default is 0.05.
        """
        self.df = df
        self.alpha = alpha

    def perform_adf_test(self, trends=None):
        """
        Perform ADF test on the series with different trends.

        Parameters:
        - trends (list): List of trends for the test. Default is ['ct', 'c', 'n'].

        Returns:
        - dict: Results of the tests.
        """
        if trends is None:
            trends = ['ct', 'c', 'n']

        results = {}
        for trend in trends:
            columns = []
            stats = []
            p_values = []
            lags_used = []
            unit_root_results = []

            for column in self.df.columns:
                series = self.df[column]
                adf_result = ADF(series, trend=trend, method="aic")
                columns.append(column)
                stats.append(adf_result.stat)
                p_values.append(adf_result.pvalue)
                lags_used.append(adf_result.lags)
                unit_root_results.append('Stationary' if adf_result.pvalue <= self.alpha else 'Non-stationary')

            df_results = pd.DataFrame({
                'stat': stats,
                'p-value': p_values,
                'number of lags': lags_used,
                'Result': unit_root_results
            }, index=columns)

            stationary_df = df_results[df_results['Result'] == 'Stationary']
            non_stationary_df = df_results[df_results['Result'] == 'Non-stationary']
            stationary_count = stationary_df.shape[0]
            non_stationary_count = non_stationary_df.shape[0]
            stationary_series = list(stationary_df.index)
            non_stationary_series = list(non_stationary_df.index)

            results[trend] = {
                'df_results': df_results,
                'Stationary': stationary_df,
                'Non-stationary': non_stationary_df,
                'Stationary_count': stationary_count,
                'Non_stationary_count': non_stationary_count,
                'Stationary_series': stationary_series,
                'Non_stationary_series': non_stationary_series
            }

        return results
