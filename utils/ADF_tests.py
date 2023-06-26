import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

# Activate automatic conversion between pandas and R objects
pandas2ri.activate()

def adf_test(dataframe):
    # Convert the dataframe to an R dataframe
    r_dataframe = pandas2ri.conversion.py2rpy(dataframe)
    
    # Load the required R package for ADF test
    robjects.r('library(tseries)')
    
    adf_results = {}
    
    # Apply ADF test to each variable in the R dataframe
    for column in dataframe.columns:
        variable = f'df${column}'
        r_code = f"result <- adf.test({variable})"
        
        robjects.r(r_code)
        
        # Retrieve the ADF test results as an R object
        adf_result = robjects.r['result']
        
        # Convert the ADF test results to a pandas dataframe
        adf_result_df = pandas2ri.ri2py(adf_result)
        
        adf_results[column] = adf_result_df
    
    return adf_results
