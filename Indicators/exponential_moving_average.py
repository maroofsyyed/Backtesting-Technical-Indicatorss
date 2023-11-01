'''
Exponential Moving Average (EMA) is similar to Simple Moving Average (SMA), measuring trend direction
over a period of time. However, whereas SMA simply calculates an average of price data, EMA applies
more weight to data that is more current. Because of its unique calculation, EMA will follow prices
more closely than a corresponding SMA.
'''
from finta import TA

def exponential_moving_average(data, period=10):
    return TA.EMA(data, period).values

