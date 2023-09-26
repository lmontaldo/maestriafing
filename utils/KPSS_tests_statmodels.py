import pandas as pd
from statsmodels.tsa.stattools import kpss

class KPSSAnalyzer:
    def __init__(self, data):
        self.data = data
        self.results = {}

    def run_tests(self):
        for regression in ['c', 'ct']:
            for nlags in ['auto', 'legacy']:
                self.results[f'{regression}_{nlags}'] = self.kpss_test(regression, nlags)

    def kpss_test(self, regression, nlags):
        title = f"Results of KPSS Test for {'Constant' if regression == 'c' else 'Trend'} Stationarity and nlags = {nlags}:"
        print(title)
        results = []
        if nlags == 'legacy':
            nlags = int(12*(len(self.data)/100)**(1/4))
        if isinstance(self.data, pd.DataFrame):
            for column in self.data.columns:
                print("Column:", column)
                kpsstest = kpss(self.data[column], regression=regression, nlags=nlags)
                kpss_output = self.create_kpss_output(kpsstest)
                kpss_output.name = title + f' Column: {column}'
                print(kpss_output)
                print(kpss_output.to_latex())
                print("------------------")
                results.append(kpss_output)
            results_df = pd.concat(results, axis=1)
        elif isinstance(self.data, pd.Series):
            kpsstest = kpss(self.data, regression=regression, nlags=nlags)
            kpss_output = self.create_kpss_output(kpsstest)
            kpss_output.name = title
            print(kpss_output)
            print(kpss_output.to_latex())
            print("------------------")
            results_df = kpss_output
        else:
            raise TypeError("Input data must be a pandas DataFrame or Series")
        return results_df

    def create_kpss_output(self, kpsstest):
        kpss_output = pd.Series(
            [kpsstest[0], kpsstest[1], kpsstest[2]],
            index=["Test Statistic", "p-value", "Lags Used"]
        )
        for key, value in kpsstest[3].items():
            kpss_output[f'Critical Value ({key})'] = value
        return kpss_output

# Usage:
# data = pd.DataFrame(...) or pd.Series(...)  # your data
# analyzer = KPSSAnalyzer(data)
# analyzer.run_tests()
# print(analyzer.results['c_auto'])
# print(analyzer.results['ct_legacy'])

