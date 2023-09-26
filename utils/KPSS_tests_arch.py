import pandas as pd
from arch.unitroot import KPSS

class KPSSAnalyzer:
    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input data must be a pandas DataFrame")

        self.data = data
        self.results = {}

    def run_tests(self):
        for trend in ['c', 'ct']:
            for nlags in ['auto', 'legacy']:
                key = f'{trend}_{nlags}'
                self.results[key] = self.kpss_test(trend, nlags)

    def kpss_test(self, trend, nlags):
        if nlags == 'legacy':
            nlags = int(12 * (len(self.data) / 100) ** (1/4))
        elif nlags == 'auto':
            nlags = None  # Assuming 'auto' means letting arch select lags

        return self._kpss_test_dataframe(trend, nlags)

    def _kpss_test_dataframe(self, trend, nlags):
        results = {}
        for column in self.data.columns:
            kpsstest = KPSS(self.data[column], trend=trend, lags=nlags)
            is_significant = kpsstest.pvalue <= 0.05
            results[column] = is_significant
        return results