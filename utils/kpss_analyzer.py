import pandas as pd
from statsmodels.tsa.stattools import kpss

class KPSSAnalyzer:
    ...
    def __init__(self, data, regressions=['c'], nlags=None):
        self.data = data
        self.regressions = regressions
        self.nlags = nlags

        self._validate_inputs()

    def _validate_inputs(self):
        ...
        if not isinstance(self.data, (pd.DataFrame, pd.Series)):
            raise ValueError("Invalid data type. Data must be a pandas DataFrame or Series.")

    def kpss_test(self, regression, nlag, columns=None):
        if isinstance(self.data, pd.DataFrame):
            if columns is None:
                columns = self.data.columns

            for column in columns:
                if column not in self.data.columns:
                    raise ValueError(f"Column '{column}' not found in the DataFrame.")
                
                print(f"Results of KPSS Test for {regression.capitalize()} Stationarity - Column: {column}, nlag: {nlag}")
                kpsstest = kpss(self.data[column], regression=regression, nlags=nlag, store=True)
                kpss_output = pd.Series(
                    [kpsstest.stat, kpsstest.p_value, kpsstest.lags],
                    index=["Test Statistic", "p-value", "Lags Used"]
                )
                print("KPSS Test Summary:")
                print(kpss_output)

                print("Critical Values:")
                for key, value in kpsstest.critical_values.items():
                    print(f"  {key}: {value}")

                print("------------------")
        elif isinstance(self.data, pd.Series):
            print(f"Results of KPSS Test for {regression.capitalize()} Stationarity - nlag: {nlag}")
            kpsstest = kpss(self.data, regression=regression, nlags=nlag, store=True)
            kpss_output = pd.Series(
                [kpsstest.stat, kpsstest.p_value, kpsstest.lags],
                index=["Test Statistic", "p-value", "Lags Used"]
            )
            print("KPSS Test Summary:")
            print(kpss_output)

            print("Critical Values:")
            for key, value in kpsstest.critical_values.items():
                print(f"  {key}: {value}")

            print("------------------")

    def run_tests(self, columns=None):
        if isinstance(self.data, pd.DataFrame):
            if columns is None:
                columns = self.data.columns
            
            for regression in self.regressions:
                self.kpss_test(regression, self.nlags, columns)
        elif isinstance(self.data, pd.Series):
            for regression in self.regressions:
                self.kpss_test(regression, self.nlags)
