'''
This file contains the Enhanced Fibonacci Indicator code. Enhanced Fibonacci is the updated version of
fibonacci indcator where we use the high and low price also instead of just close proce to calculate
the fibonacci averages.
'''

import ta
import pandas as pd
pd.set_option('display.max_columns', None)
from ta import trend


def ema(data, column, period=10):
    return ta.trend.ema_indicator(data[column], period).values


def enhanced_fibonacci_moving_average(data):
    # Calculate Fibonacci Moving Averages
    data['Fib_MA_3_high'] = ema(data, 'high', 3)
    data['Fib_MA_5_high'] = ema(data, 'high', 5)
    data['Fib_MA_8_high'] = ema(data, 'high', 8)
    data['Fib_MA_13_high'] = ema(data, 'high', 13)
    data['Fib_MA_21_high'] = ema(data, 'high', 21)
    data['Fib_MA_34_high'] = ema(data, 'high', 34)
    data['Fib_MA_55_high'] = ema(data, 'high', 55)
    data['Fib_MA_89_high'] = ema(data, 'high', 89)
    data['Fib_MA_144_high'] = ema(data, 'high', 144)
    data['Fib_MA_233_high'] = ema(data, 'high', 233)
    data['Fib_MA_377_high'] = ema(data, 'high', 377)
    data['Fib_MA_610_high'] = ema(data, 'high', 610)


    data['Fib_MA_3_low'] = ema(data, 'low', 3)
    data['Fib_MA_5_low'] = ema(data, 'low', 5)
    data['Fib_MA_8_low'] = ema(data, 'low', 8)
    data['Fib_MA_13_low'] = ema(data, 'low', 13)
    data['Fib_MA_21_low'] = ema(data, 'low', 21)
    data['Fib_MA_34_low'] = ema(data, 'low', 34)
    data['Fib_MA_55_low'] = ema(data, 'low', 55)
    data['Fib_MA_89_low'] = ema(data, 'low', 89)
    data['Fib_MA_144_low'] = ema(data, 'low', 144)
    data['Fib_MA_233_low'] = ema(data, 'low', 233)
    data['Fib_MA_377_low'] = ema(data, 'low', 377)
    data['Fib_MA_610_low'] = ema(data, 'low', 610)


    # Calculate Enhanced Fibonacci Moving Averages
    data['Enhanced_Fib_MA_3_high'] = (data['Fib_MA_3_high'] + data['Fib_MA_5_high'] + data['Fib_MA_8_high'] + data['Fib_MA_13_high'] + data['Fib_MA_21_high'] + data['Fib_MA_34_high'] + data['Fib_MA_55_high'] + data['Fib_MA_89_high'] + data['Fib_MA_144_high'] + data['Fib_MA_233_high'] + data['Fib_MA_377_high'] + data['Fib_MA_610_high']) / 12
    data['Enhanced_Fib_MA_3_low'] = (data['Fib_MA_3_low'] + data['Fib_MA_5_low'] + data['Fib_MA_8_low'] + data['Fib_MA_13_low'] + data['Fib_MA_21_low'] + data['Fib_MA_34_low'] + data['Fib_MA_55_low'] + data['Fib_MA_89_low'] + data['Fib_MA_144_low'] + data['Fib_MA_233_low'] + data['Fib_MA_377_low'] + data['Fib_MA_610_low']) / 12
    data = data.dropna()

    # Generate signals
    data['signal'] = 0
    signal_values = [0]  # Append 0 for the first row

    for i in range(1, len(data)):
        if (
            data['close'].iloc[i] > data['Enhanced_Fib_MA_3_high'].iloc[i] and
            data['close'].iloc[i-1] <= data['Enhanced_Fib_MA_3_high'].iloc[i-1] and
            data['signal'].iloc[i-1] != -1
        ):
            signal_values.append(-1)
        elif (
            data['close'].iloc[i] < data['Enhanced_Fib_MA_3_low'].iloc[i] and
            data['close'].iloc[i-1] >= data['Enhanced_Fib_MA_3_low'].iloc[i-1] and
            data['signal'].iloc[i-1] != 1
        ):
            signal_values.append(1)
        else:
            signal_values.append(0)

    data['signal'] = signal_values
    return data