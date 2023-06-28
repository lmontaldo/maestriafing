import numpy as np
from arch.unitroot import ADF

class ADFModelComparison:
    def __init__(self, data):
        self.data = data
        self.T = data.shape[0]
    
    def compare_model_c_with_a(self, r, k, significance_level=0.05):
        model_c = ADF(self.data, trend='ct')
        model_a = ADF(self.data, trend='nc')
        results_c = model_c.fit()
        results_a = model_a.fit()
        
        # Calculate the test statistic
        test_stat = (results_a.stat - results_c.stat) * (self.T - r - k) / r
        
        # Calculate the p-value
        p_value = 1 - np.abs(test_stat)
        
        # Compare with the significance level
        is_significant = p_value < significance_level
        
        return test_stat, p_value, is_significant
    
    def compare_model_b_with_a(self, r, k, significance_level=0.05):
        model_b = ADF(self.data, trend='c')
        model_a = ADF(self.data, trend='nc')
        results_b = model_b.fit()
        results_a = model_a.fit()
        
        # Calculate the test statistic
        test_stat = (results_a.stat - results_b.stat) * (self.T - r - k) / r
        
        # Calculate the p-value
        p_value = 1 - np.abs(test_stat)
        
        # Compare with the significance level
        is_significant = p_value < significance_level
        
        return test_stat, p_value, is_significant



