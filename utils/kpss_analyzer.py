import pandas as pd
from statsmodels.tsa.stattools import kpss

class KPSSAnalyzer:
    """
    KPSSAnalyzer performs the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test
    for stationarity on time series data in a pandas DataFrame.

    Parameters:
        dataframe (pandas.DataFrame): The input DataFrame containing the time series data.
        regressions (list, optional): A list of regression types for the KPSS test.
                                      Choose 'c' for constant or 'ct' for trend.
                                      Default is ['c'].
        nlags (int, str, list, optional): The number of lags to be used for the KPSS test.
                                         Valid options: 'lshort', 'legacy', 'auto', an integer value, or a list of integers.
                                         Default is 'auto'.

    Methods:
        kpss_test(columns=None):
            Performs the KPSS test on the specified columns.

        run_tests(columns=None):
            Runs the KPSS test on the specified columns for all combinations of regression types and nlags.
            If no columns are specified, the test is performed on all columns in the DataFrame.
    """

    def __init__(self, dataframe, regressions=['c'], nlags='auto'):
        self.dataframe = dataframe
        self.regressions = regressions
        self.nlags = nlags

        self._validate_inputs()

    def _validate_inputs(self):
        valid_regression_options = ['c', 'ct']
        valid_nlags_options = ['lshort', 'legacy', 'auto']

        if not isinstance(self.regressions, list):
            self.regressions = [self.regressions]

        for regression in self.regressions:
            if regression not in valid_regression_options:
                raise ValueError(f"Invalid regression type '{regression}'. Choose 'c' for constant or 'ct' for trend.")

        if isinstance(self.nlags, int) and self.nlags <= 0:
            raise ValueError("Invalid value for nlags. It must be a positive integer, a list of integers, or one of 'lshort', 'legacy', or 'auto'.")

        if isinstance(self.nlags, str) and self.nlags not in valid_nlags_options:
            raise ValueError(f"Invalid value for nlags. Choose one of {valid_nlags_options}, an integer value, or a list of integers.")

        if isinstance(self.nlags, int) or isinstance(self.nlags, str):
            self.nlags = [self.nlags]

    def kpss_test(self, regression, nlags, columns=None):
        if columns is None:
            columns = self.dataframe.columns

        for column in columns:
            if column not in self.dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the DataFrame.")

            for nlag in nlags:
                print(f"Results of KPSS Test for {regression.capitalize()} Stationarity - Column: {column}, nlag: {nlag}")
                kpsstest = kpss(self.dataframe[column], regression=regression, nlags=nlag, store=True)
                kpss_output = pd.Series(
                    kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
                )
                print("KPSS Test Summary:")
                print(kpss_output)

                print("Critical Values:")
                for key, value in kpsstest[3].items():
                    print(f"  {key}: {value}")

                print("------------------")

    def run_tests(self, columns=None):
        if columns is None:
            columns = self.dataframe.columns

        for regression in self.regressions:
            self.kpss_test(regression, self.nlags, columns)
