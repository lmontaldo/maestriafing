import numpy as np
from statsmodels.tsa.stattools import adfuller
import pandas as pd
# model c
def adf_test_ct(df, regression='ct', autolag='AIC'):
    # Create an empty DataFrame to store the results
    columns = ['Column', 'ADF Statistic', 'p-value', '#Lags Used', 'Result']
    results = pd.DataFrame(columns=columns)

    for column in df.columns:
        # Apply ADF test
        adf_result = adfuller(df[column], regression=regression, autolag=autolag)

        # Determine the result based on p-value
        if adf_result[1] < 0.05:
            result_str = "not RU"
        else:
            result_str = "RU"
        
        # Add results to the dataframe using loc
        results.loc[len(results)] = [column, 
                                     adf_result[0], 
                                     adf_result[1], 
                                     adf_result[2], 
                                     result_str]

    # Splitting the dataframe into two based on the 'Result' column
    RU = results[results['Result'] == "RU"]
    not_RU = results[results['Result'] == "not RU"]

    # Getting the count of series that are RU and not RU
    RU_count = len(RU)
    not_RU_count = len(not_RU)

    # Getting the lists of series names that are RU and not RU
    RU_columns = RU['Column'].tolist()
    not_RU_columns = not_RU['Column'].tolist()

    return RU, not_RU, RU_count, not_RU_count, RU_columns, not_RU_columns
# model b
def adf_test_c(df, regression='c', autolag='AIC'):
    # Create an empty DataFrame to store the results
    columns = ['Column', 'ADF Statistic', 'p-value', '#Lags Used', 'Result']
    results = pd.DataFrame(columns=columns)

    for column in df.columns:
        # Apply ADF test
        adf_result = adfuller(df[column], regression=regression, autolag=autolag)

        # Determine the result based on p-value
        if adf_result[1] < 0.05:
            result_str = "not RU"
        else:
            result_str = "RU"
        
        # Add results to the dataframe using loc
        results.loc[len(results)] = [column, 
                                     adf_result[0], 
                                     adf_result[1], 
                                     adf_result[2], 
                                     result_str]

    # Splitting the dataframe into two based on the 'Result' column
    RU = results[results['Result'] == "RU"]
    not_RU = results[results['Result'] == "not RU"]

    # Getting the count of series that are RU and not RU
    RU_count = len(RU)
    not_RU_count = len(not_RU)

    # Getting the lists of series names that are RU and not RU
    RU_columns = RU['Column'].tolist()
    not_RU_columns = not_RU['Column'].tolist()

    return RU, not_RU, RU_count, not_RU_count, RU_columns, not_RU_columns

# model n
def adf_test_c(df, regression='n', autolag='AIC'):
    # Create an empty DataFrame to store the results
    columns = ['Column', 'ADF Statistic', 'p-value', '#Lags Used', 'Result']
    results = pd.DataFrame(columns=columns)

    for column in df.columns:
        # Apply ADF test
        adf_result = adfuller(df[column], regression=regression, autolag=autolag)

        # Determine the result based on p-value
        if adf_result[1] < 0.05:
            result_str = "not RU"
        else:
            result_str = "RU"
        
        # Add results to the dataframe using loc
        results.loc[len(results)] = [column, 
                                     adf_result[0], 
                                     adf_result[1], 
                                     adf_result[2], 
                                     result_str]

    # Splitting the dataframe into two based on the 'Result' column
    RU = results[results['Result'] == "RU"]
    not_RU = results[results['Result'] == "not RU"]

    # Getting the count of series that are RU and not RU
    RU_count = len(RU)
    not_RU_count = len(not_RU)

    # Getting the lists of series names that are RU and not RU
    RU_columns = RU['Column'].tolist()
    not_RU_columns = not_RU['Column'].tolist()

    return RU, not_RU, RU_count, not_RU_count, RU_columns, not_RU_columns