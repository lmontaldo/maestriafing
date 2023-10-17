import pandas as pd
import numpy as np

def prepare_missing(fred, tcodes):
    transformed_data = []

    for column in fred.columns:
        tcode = tcodes.loc[column, 'transformations_code']
        x = fred[column]

        if tcode == 1:  # Level (no transformation)
            y = x

        elif tcode == 2:  # First difference
            y = x.diff()

        elif tcode == 3:  # Second difference
            y = x.diff().diff()

        elif tcode == 4:  # Natural log (you can replace with log1)
            y = np.log1p(x)

        elif tcode == 5:  # First difference of natural log (you can replace with log1)
            y = np.log1p(x).diff()

        elif tcode == 6:  # Second difference of natural log (you can replace with log1)
            y = np.log1p(x).diff().diff()

        elif tcode == 7:  # First difference of percent change
            y = x.pct_change().diff()

        transformed_data.append(y)

    transformed_data = pd.concat(transformed_data, axis=1)
    
    # Fill missing values with the mean of each column
    #transformed_data.fillna(transformed_data.mean(), inplace=True)

    return transformed_data


