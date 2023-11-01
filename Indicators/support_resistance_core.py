"""This file contains functions to find support and resistances calculated with the help of fibonacci levels and bollinger bands.
   Not giving a single support or resistance
"""

from scipy.signal import argrelextrema
import numpy as np
import pandas as pd


forex_data = pd.read_csv('forex_data_EUR_USD.csv')
print((forex_data.timestamp.values[0]))
forex_data['timestamp'] = pd.to_datetime(forex_data.timestamp)
print(forex_data)
print(type(forex_data.timestamp.values[0]))
# forex_data.set_index('timestamp', inplace=True)
# forex_data.rename(columns={'timestamp':Date})
# mpf.plot(forex_data)

def mm_sr(dataframe):
    """Function to get max min for support and resistance"""
    n = 5
    dataframe['min_sr'] = dataframe.iloc[argrelextrema(dataframe.close.values, np.less_equal, order=n)[0]]['Close']
    dataframe['max_sr'] = dataframe.iloc[argrelextrema(dataframe.close.values, np.greater_equal, order=n)[0]]['Close']
    return dataframe
def mm_sr(dataframe):
    """Function to get max min for chart patterns"""
    dataframe['min'] = dataframe.close[(dataframe.close.shift(1) > dataframe.close) & (dataframe.close.shift(-1) > dataframe.close)]
    dataframe['max'] = dataframe.close[(dataframe.close.shift(1) < dataframe.close) & (dataframe.close.shift(-1) < dataframe.close)]
    return dataframe

low = 12

def levels(df, sensitivity=3, tests=3, noise_r=0.01):
    # Get list of all minimum and maximum levels
    df['min'] = df.close[(df.close.shift(1) > df.close) & (df.close.shift(-1) > df.close)]
    df['max'] = df.close[(df.close.shift(1) < df.close) & (df.close.shift(-1) < df.close)]
    max_sr = [(row.timestamp, row.max) for row in df.itertuples() if row.max > 0]
    min_sr = [(row.timestamp, row.min) for row in df.itertuples() if row.min > 0]
    min_sr = [(row.timestamp, row.min) for row in df.itertuples() if row.min > 0]
    sr = sorted([[mx for mx in max_sr] + [mn for mn in min_sr]][0])

    # Init dictionary to store level strength
    sr_dict = {}

    # itereate through rows to establish and test levels
    for row in df.itertuples():
        body = abs(row.close - row.open)
        wick = abs(row.high - row.low)
        candle_ratio = body / (wick + 1)
        for point in sr:
            price = point[1]
            date = point[0]
            if price in sr_dict and row.timestamp > date:

                # Close bullish inside and wick above
                if (row.close >= (price - sensitivity) and row.close <= (price + sensitivity)) and candle_ratio > 0.5:
                    sr_dict[price] += 1


            else:
                sr_dict[price] = 0

    # Filter dictionary to only store levels that have been tested
    sr_dict = dict(filter(lambda val: val[1] >= tests, sr_dict.items()))

    # Filters strength dictionary to only include levels above a strength level
    sr = sorted([level for level, strength in sr_dict.items() if strength >= tests])

    # Conduct noise reduction using noise_reduction parameter
    sr_df = pd.DataFrame(sr, columns=["lvl"])
    sr_df["lvl p"] = sr_df.pct_change()

    # Filter noise
    sr = [sr_df.iloc[row[0]]['lvl'] for row in sr_df.itertuples() if row[0] > 0 if abs(row[2]) > noise_r]

    # Filter dictionary with values from list
    sr_dict = {key:sr_dict[key] for key in sr if key in sr_dict.keys()}

    # Return the levels and their strengths as a list and dictionary
    return sr, sr_dict

# Testing the indicator
# sr, sr_dict = levels(forex_data, sensitivity = .5)
# print(sr)
# print(sr_dict)

# Conclusion: Not worth it
