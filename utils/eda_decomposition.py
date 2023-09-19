import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def to_datetime_str(df, column):
    df[column] = pd.to_datetime(df[column]).dt.strftime('%Y-%m-%d')
    return df

def line_plot_dataframe(df, title=None, xlabel=None, ylabel=None):
    """
    Plot the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to plot.
        title (str): The title for the plot. Default is None.
        xlabel (str): The label for the x-axis. Default is None.
        ylabel (str): The label for the y-axis. Default is None.
    """
    plt.figure(figsize=(10, 10))  # Set the figure size
    df.plot()
    plt.xticks(rotation=45, ha='right')  # Rotate and align x-axis tick labels
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(8))  # Set maximum number of x-axis tick labels
    if title:
        plt.title(title)  # Set the title if provided
    if xlabel:
        plt.xlabel(xlabel)  # Set the x-axis label if provided
    if ylabel:
        plt.ylabel(ylabel)  # Set the y-axis label if provided
    plt.show()
    
def save_plot(plot_func, data, save_folder, filename):
    plt.figure(figsize=(10, 10))  # Set the figure size
    plot_func(data)
    save_path = os.path.join(save_folder, filename)
    plt.savefig(save_path)
    plt.close()
    print(f"Plot saved at {save_path}")    
    
    
def decompose_dataframe(df, model='additive', period=12):
    """
    Perform seasonal decomposition on each column of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to decompose.
        model (str): The type of seasonal decomposition model to use. Default is 'additive'.
        period (int): The frequency of the time series. Required for 'multiplicative' model.

    Returns:
        dict: A dictionary of statsmodels.tsa.seasonal.DecomposeResult objects for each column.
    """
    decompositions = {}
    for column_name in df.columns:
        decompositions[column_name] = seasonal_decompose(df[column_name], model=model, period=period)
    return decompositions

def perform_seasonal_adjustment(df):
    """
    Perform seasonal adjustment on all columns of a DataFrame using seasonal decomposition.

    Args:
        df (pd.DataFrame): The DataFrame containing the time series.

    Returns:
        pd.DataFrame: The DataFrame with the seasonal adjustment applied to all columns.
    """
    adjusted_df = pd.DataFrame(index=df.index)

    for column in df.columns:
        # Perform seasonal decomposition
        decomposition = seasonal_decompose(df[column], model='additive')

        # Retrieve the trend and residual components
        trend = decomposition.trend
        residual = decomposition.resid

        # Apply seasonal adjustment by subtracting the seasonal component
        adjusted_series = df[column] - decomposition.seasonal

        # Add the adjusted series to the adjusted DataFrame
        adjusted_df[column] = adjusted_series

    return adjusted_df 

def differentiate_dataframe(df, periods=1):
    """
    Perform differencing on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to differentiate.
        periods (int): The number of periods to difference. Default is 1.

    Returns:
        pd.DataFrame: The differenced DataFrame.
    """
    diff = df.diff(periods=periods)
    return diff

def plot_rolling_mean(df, columns):
    """
    Calculate the rolling mean with a window size of 12 for the specified columns
    in the time series DataFrame and plot the results.

    Args:
        df (pd.DataFrame): The time series DataFrame.
        columns (list): A list of column names to calculate the rolling mean on.
    """
    rolling_mean_df = df[columns].rolling(window=12).mean()
    rolling_mean_df.plot(figsize=(8, 4))
    plt.title("Rolling Mean over 12 month period")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend(loc="best")
    plt.show()
    
def plot_rolling_variance(df, column):
    """
    Calculate the rolling variance with a window size of 12 for the specified column
    in the DataFrame and plot the results.

    Args:
        df (pd.DataFrame): The DataFrame.
        column (str): The column name to calculate the rolling variance on.
    """
    rolling_variance = df[column].rolling(window=12).var()
    rolling_variance.plot(figsize=(8, 4), color="tab:red", title="Rolling Variance over 12 month period")
    plt.xlabel("Date")
    plt.ylabel("Variance")
    plt.show()
    
def plot_acf_pacf(df: pd.DataFrame, acf_lags: int, pacf_lags: int) -> None:
    """
    This function plots the Autocorrelation and Partial Autocorrelation lags.

    Args:
        df (pd.DataFrame): DataFrame containing the time series data.
        acf_lags (int): Number of ACF lags.
        pacf_lags (int): Number of PACF lags.
    Returns: None
    """

    # Figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9), facecolor='w')

    # ACF & PACF
    plot_acf(df, ax=ax1, lags=acf_lags)
    plot_pacf(df, ax=ax2, lags=pacf_lags, method="ols-adjusted")

    # Labels
    ax1.set_title("Autocorrelation", fontsize=15, pad=10)
    ax1.set_xlabel("Lags (months)", fontsize=12)

    ax2.set_title("Partial Autocorrelation", fontsize=15, pad=10)
    ax2.set_xlabel("Lags (months)", fontsize=12)

    # Legend & Grid
    ax1.grid(linestyle=":", color='grey')
    ax2.grid(linestyle=":", color='grey')

    plt.show()
    
def perform_seasonal_adjustment(df, period=12):
    """
    Perform seasonal adjustment on all columns of a DataFrame using seasonal decomposition.

    Args:
        df (pd.DataFrame): The DataFrame containing the time series.

    Returns:
        pd.DataFrame: The DataFrame with the seasonal adjustment applied to all columns.
    """
    adjusted_df = pd.DataFrame(index=df.index)

    for column in df.columns:
        # Perform seasonal decomposition
        decomposition = seasonal_decompose(df[column], model='additive')

        # Retrieve the trend and residual components
        trend = decomposition.trend
        residual = decomposition.resid

        # Apply seasonal adjustment by subtracting the seasonal component
        adjusted_series = df[column] - decomposition.seasonal

        # Add the adjusted series to the adjusted DataFrame
        adjusted_df[column] = adjusted_series

    return adjusted_df     

def STL_seasonal_adjusted(df, period=12):
    """
    Uses the STL method: Seasonal-Trend Decomposition Procedure Based on Loess to:
    * Handle any type of seasonality
    * Allow the user to control the rate of change of the seasonal component
    * Ensure robustness to outliers

    The seasonal argument is set to 12 by default. The larger the integer, the more 'smooth' 
    the seasonal component becomes. This causes less of the variation in the data to be attributed to its seasonal component.

    This function subtracts the seasonal component from the original series and returns the adjusted series.

    Args:
        df (pd.DataFrame): The DataFrame containing the time series data.
        seasonal (int): The parameter controlling the rate of change of the seasonal component. Default is 12.

    Returns:
        pd.DataFrame: The DataFrame with the seasonal component removed from the original series.
    """
    output = pd.DataFrame(index=df.index)

    for column in df.columns:
        # Perform STL decomposition
        x = STL(df[column], period=period, robust=False).fit()

        # Subtract seasonal component from the original series
        adjusted_series = df[column] - x.seasonal

        # Add the adjusted series to the output DataFrame
        output[column] = adjusted_series

    return output