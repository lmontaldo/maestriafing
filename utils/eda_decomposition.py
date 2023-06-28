import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from config import image_path


def to_datetime_str(df, column):
    df[column] = pd.to_datetime(df[column]).dt.strftime('%Y-%m-%d')
    return df

def save_line_plot_df(df, save_path=image_path, title=None, xlabel=None, ylabel=None):
    """
    Plot the DataFrame and save it to a specified path.

    Args:
        df (pd.DataFrame): The DataFrame to plot.
        save_path (str): The path where the plot should be saved.
        title (str): The title for the plot. Default is None.
        xlabel (str): The label for the x-axis. Default is None.
        ylabel (str): The label for the y-axis. Default is None.
    Returns:
        ax: An Axes object with the plot.
    """
    plt.figure(figsize=(15, 15))  # Set the figure size
    ax = df.plot()
    plt.xticks(rotation=45, ha='right', fontsize=8)  # Rotate and align x-axis tick labels
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(8))  # Set maximum number of x-axis tick labels
    if title:
        plt.title(title)  # Set the title if provided
    if xlabel:
        plt.xlabel(xlabel)  # Set the x-axis label if provided
    if ylabel:
        plt.ylabel(ylabel)  # Set the y-axis label if provided

    # Save the plot
    plt.savefig(os.path.join(save_path, input("Enter the line plot name: ") + ".png"), bbox_inches='tight')
    plt.close()  # Close the figure to free up memory

    return ax
   
def decompose_dataframe(df, model='additive', freq=None):
    """
    Perform seasonal decomposition on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to decompose.
        model (str): The type of seasonal decomposition model to use. Default is 'additive'.
        freq (int): The frequency of the time series. Required for 'multiplicative' model.

    Returns:
        statsmodels.tsa.seasonal.DecomposeResult: The result of the seasonal decomposition.
    """
    decomposition = seasonal_decompose(df, model=model, freq=freq)
    return decomposition

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
    
def perform_seasonal_adjustment(df, model='additive', freq=12):
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
        decomposition = seasonal_decompose(df[column], model=model, period=freq)

        # Retrieve the trend and residual components
        trend = decomposition.trend
        residual = decomposition.resid

        # Apply seasonal adjustment by subtracting the seasonal component
        adjusted_series = df[column] - decomposition.seasonal

        # Add the adjusted series to the adjusted DataFrame
        adjusted_df[column] = adjusted_series

    return adjusted_df     

def STL_seasonal_adjusted(df, seasonal=12):
    """
    1- Uses a STL method: Seasonal-Trend Decomposition Procedure Based on Loess
    * It handles any type of seasonality
    * The user can control the rate of change of the seasonal component
    * It is robust to outliers
    The seasonal argument is set to 12 by default. The larger the integer, the more 'smooth'
    the seasonal component becomes. This causes less of the variation in the data to be attributed to its seasonal component.
    2- Keeps only the seasonal component (sc) and creates a DataFrame with the seasonal component of each IPC component
    3- Removes the seasonal component from the original series

    Args:
        df (pd.DataFrame): The DataFrame containing the time series data.
        seasonal (int): The parameter controlling the rate of change of the seasonal component. Default is 7.

    Returns:
        pd.DataFrame: The DataFrame with the seasonal component removed from the original series.
    """
    output = pd.DataFrame(index=df.index)

    for column in df.columns:
        # Perform STL decomposition
        x = STL(df[column], robust=False).fit()

        # Subtract seasonal component from the original series
        adjusted_series = df[column] - x.seasonal

        # Add the adjusted series to the output DataFrame
        output[column] = adjusted_series

    return output
  
def convert_to_long_format(df, id_vars='ymd', var_name='c_codigo', value_name='value'):
    """
    Convert the DataFrame from wide to long format.

    Args:
        df (pd.DataFrame): The DataFrame to convert.
        id_vars (str or list): Column(s) to use as identifier variable(s). Default is 'ymd'.
        var_name (str): Name to use for the variable column. Default is 'c_codigo'.
        value_name (str): Name to use for the value column. Default is 'value'.

    Returns:
        pd.DataFrame: The DataFrame in long format.
    """
    df_long = pd.melt(df, id_vars=id_vars, var_name=var_name, value_name=value_name)
    return df_long
         
       
