import pandas as pd
import math
from arch.unitroot import KPSS

class KPSSAnalysis:
    
    def __init__(self, data, alpha=0.05, nlags_list=['old_method', 'Hobijn_et_al'], trends=['c','ct']):
        self.data = data
        self.alpha = alpha
        self.nlags_list = nlags_list
        self.trends = trends
        self.n = len(data)
        self.results = {}

    def perform_test(self):
        for trend in self.trends:
            results_for_trend = {}
            for nlags in self.nlags_list:
                df_results = self._test_for_params(trend, nlags)
                RH0_true = df_results[df_results['Result'] == 'Stationary']
                RH0_false = df_results[df_results['Result'] == 'Non-Stationary']
                
                results_for_trend[nlags] = {
                    'df_results': df_results,
                    'Stationary': RH0_true,
                    'Non-Stationary': RH0_false,
                    'Stationary_count': RH0_true.shape[0],
                    'Non-Stationary_count': RH0_false.shape[0],
                    'Stationary_series': list(RH0_true.index),
                    'Non-Stationary_series': list(RH0_false.index)
                }
            self.results[trend] = results_for_trend
    
    def _test_for_params(self, trend, nlags):
        columns = self.data.columns.tolist()
        stats, p_values, lags_used, results = [], [], [], []

        for column in self.data.columns:
            if nlags == 'old_method':
                actual_nlags = math.trunc(12 * (self.n/100) ** (1/4))
            else:  
                actual_nlags = math.trunc(4 * (self.n/100)**0.25)

            kpsstest = KPSS(self.data[column], trend=trend, lags=actual_nlags)
            is_stationary = kpsstest.pvalue <= self.alpha

            stats.append(kpsstest.stat)
            p_values.append(kpsstest.pvalue)
            lags_used.append(actual_nlags)
            results.append('Stationary' if is_stationary else 'Non-Stationary')

        df_results = pd.DataFrame({
            'stat': stats,
            'p-value': p_values,
            'number of lags': lags_used,
            'Result': results
        }, index=columns)
        
        return df_results

    # Methods to fetch results
    def get_results_for_trend_nlags(self, trend, nlags):
        return self.results.get(trend, {}).get(nlags, {}).get('df_results', None)

    def get_stationary_for_trend_nlags(self, trend, nlags):
        return self.results.get(trend, {}).get(nlags, {}).get('Stationary', None)

    def get_non_stationary_for_trend_nlags(self, trend, nlags):
        return self.results.get(trend, {}).get(nlags, {}).get('Non-Stationary', None)

