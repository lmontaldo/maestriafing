import numpy as np

def remove_outliers(x):
    if isinstance(x, (int, float)):
        # Handle scalar values (int or float)
        return x
    else:
        # Calculate the median of the series, ignoring NaN values
        median_X = np.nanmedian(x)

        # Calculate quartiles, ignoring NaN values
        Q25 = np.nanpercentile(x, 25)
        Q50 = np.nanpercentile(x, 50)
        Q75 = np.nanpercentile(x, 75)

        # Calculate interquartile range (IQR) of the series
        IQR = Q75 - Q25

        # Determine outliers
        Z = np.abs(x - median_X)
        outlier = Z > (10 * IQR)

        # Replace outliers with NaN
        cleaned_series = x.copy()
        cleaned_series[outlier] = np.nan

        return cleaned_series