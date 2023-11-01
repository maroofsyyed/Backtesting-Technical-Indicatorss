"""
This file has functions for calculating MACD Indicators used for the data given.
MACD is one of the most important indiactors, which is primarily used for capturing the price trend features.
"""
import pandas as pd


def calculate_ema(data, window):
    """
    Calculating EMA
    :param data: Dataframe containing market data
    :param window: The time lag window setting
    :return: returns data with ema calculated
    """
    return data.ewm(span=window, adjust=False).mean()


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Calculate MACD on close price of the data
    :param data: Dataframe conaining market data
    :param short_window: Short window setting
    :param long_window: Long window setting
    :param signal_window: Signal window setting
    :return: returns three indicator values of macd_line, signal_line and macd_histogram
    """
    data = data['close']
    # Calculate the MACD line (12-day EMA - 26-day EMA)
    ema_short = calculate_ema(data, short_window)
    ema_long = calculate_ema(data, long_window)
    macd_line = ema_short - ema_long

    # Calculate the signal line (9-day EMA of MACD line)
    signal_line = calculate_ema(macd_line, signal_window)

    # Calculate the MACD histogram
    macd_histogram = macd_line - signal_line

    return macd_line, signal_line, macd_histogram
