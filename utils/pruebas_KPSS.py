import pandas as pd
from statsmodels.tsa.stattools import kpss

class KPSSAnalyzer:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def kpss_test_c(self):
        print("Results of KPSS Test for Constant Stationarity:")
        self._kpss_test("c")

    def kpss_test_ct(self):
        print("Results of KPSS Test for Trend Stationarity:")
        self._kpss_test("ct")

    def _kpss_test(self, regression):
        for column in self.dataframe.columns:
            print("Column:", column)
            kpsstest = kpss(self.dataframe[column], regression=regression, nlags="auto", store=True)
            kpss_output = pd.Series(
                kpsstest[0:4], index=["Test Statistic", "p-value", "Lags Used", "critical_values"]
            )
            for key, value in kpsstest[3].items():
                kpss_output["Critical Value (%s)" % key] = value
            print(kpss_output)
            print("------------------")

# nlags models:
# lshort=int(4*(len(series)/100)**0.25)
# nlags=lshort
# nlags='legacy'
# nlags='auto'