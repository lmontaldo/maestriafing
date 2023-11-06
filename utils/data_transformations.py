import pandas as pd
import numpy as np

def prepare_missing(fred, tcodes):
    columns = fred.columns
    transformed_data = pd.DataFrame(index=fred.index)
    
    for column in columns:
        tcode = tcodes.loc[column, 'transformations_code']
        transformed_data[column] = transxf(fred[column], tcode)
    
    return transformed_data

def transxf(x, tcode):
    n = len(x)
    y = np.empty(n)
    y[:] = np.NaN
    small = 1e-6
    
    if tcode == 1:  # Level (i.e. no transformation)
        y = x
        
    elif tcode == 2:  # First difference
        y[1:] = x.values[1:] - x.values[:-1]
        
    elif tcode == 3:  # Second difference
        y[2:] = x.values[2:] - 2*x.values[1:-1] + x.values[:-2]
        
    elif tcode == 4:  # Natural log
        if min(x) >= small:
            y = np.log(x)
        
    elif tcode == 5:  # First difference of natural log
        if min(x) >= small:
            x = np.log(x)
            y[1:] = x.values[1:] - x.values[:-1]
            
    elif tcode == 6:  # Second difference of natural log
        if min(x) >= small:
            x = np.log(x)
            y[2:] = x.values[2:] - 2*x.values[1:-1] + x.values[:-2]
            
    elif tcode == 7:  # First difference of percent change
        y1 = np.empty(n)
        y1[:] = np.NaN
        y1[1:] = (x.values[1:] - x.values[:-1]) / x.values[:-1]
        y[2:] = y1[2:] - y1[1:-1]
        
    return y
