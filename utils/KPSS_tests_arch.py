import pandas as pd
import math
from arch.unitroot import KPSS

class KPSSAnalysis:
    
    def __init__(self, data, alpha=0.05, nlags_list=['legacy', 'lshort', None], trends=['c','ct']):
        self.data = data
        self.alpha = alpha
        self.nlags_list = nlags_list
        self.trends = trends
        self.n = len(data)
        self.results_df = pd.DataFrame(index=data.columns)
    
    def perform_test(self):
        for trend in self.trends:
            for nlags in self.nlags_list:
                key = f"{trend}_{nlags}"
                self.results_df[key] = self._test_for_params(trend, nlags)
    
    def _test_for_params(self, trend, nlags):
        result_data = {}
        for column in self.data.columns:
            if nlags == 'legacy':
                actual_nlags = -1
            elif nlags == 'lshort': 
                actual_nlags = math.trunc(4 * (self.n/100)**0.25)
            else:
                actual_nlags = None

            kpsstest = KPSS(self.data[column], trend=trend, lags=actual_nlags)
            RH0 = kpsstest.pvalue <= self.alpha
            result_data[column] = RH0

        return pd.Series(result_data)

    def get_result(self):
        return self.results_df

    def get_RH0_true_columns(self):
        return {col: self.results_df.index[self.results_df[col]].tolist() for col in self.results_df.columns}

    def get_RH0_false_columns(self):
        return {col: self.results_df.index[~self.results_df[col]].tolist() for col in self.results_df.columns}
