import pandas as pd
from arch.unitroot import ADF


class ModelsADF:
    
    def __init__(self, df, alfa=0.05):
        self.df = df
        self.alfa = alfa
    
    def adf_ct(self):
        return self._perform_adf_test(trend="ct")

    def adf_c(self):
        return self._perform_adf_test(trend="c")

    def adf_n(self):
        return self._perform_adf_test(trend="n")

    def _perform_adf_test(self, trend):
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
            unit_root_results.append('No RU' if adf_result.pvalue <= self.alfa else 'RU')

        df_results = pd.DataFrame({
            'stat': stats,
            'p-value': p_values,
            'number of lags': lags_used,
            'Result': unit_root_results
        }, index=columns)

        RU = df_results[df_results['Result'] == 'RU']
        not_RU = df_results[df_results['Result'] == 'No RU']
        RU_count = RU.shape[0]
        not_RU_count = not_RU.shape[0]
        RU_series = list(RU.index)
        not_RU_series = list(not_RU.index)
        return df_results, RU, not_RU, RU_count, not_RU_count, RU_series, not_RU_series
