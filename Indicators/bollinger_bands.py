'''
Bollinger bands are a type of technical indicator that allows us to analyze the volatility of a
stock and whether the price is high or low on a relative basis. The top band is typically two
standard deviations above the SMA and the bottom band is typically two standard deviations below
the SMA. where SMA is Simple Moving Average
'''
import numpy as np
def bollinger_bands(data=None, period=10, std_multiplier=2):
    '''
    The function calculates the Bollinger Bands indicator for intraday trading. It generates buy signals
    when the current stock price is lower than the lower band of the current period, and sell signals
    when the current stock price is higher than the upper band of the current period.
    :param data: Stock Data. pd.Dataframe is applicable
    :param period: The period for which bolinger-bands in features is to be obtained.
    :param std_multiplier:
    :return: DataFrame with 'Signals', 'Final Lower Band', 'Final Upper Band', 'Upper Band', and 'Lower Band' values.
    '''
    rolling_mean = data['close'].rolling(window=period).mean()
    rolling_std = data['close'].rolling(window=period).std()

    upper_band = rolling_mean + (std_multiplier * rolling_std)
    lower_band = rolling_mean - (std_multiplier * rolling_std)

    final_upper_band = upper_band.copy()
    final_lower_band = lower_band.copy()

    signals = [0] * len(data)

    for i in range(1, len(data.index)):
        curr, prev = i, i - 1

        if data['close'][curr] > upper_band[prev]:
            signals[curr] = -1
        elif data['close'][curr] < lower_band[prev]:
            signals[curr] = 1
        else:
            signals[curr] = signals[prev]

            if signals[curr] == 1 and lower_band[curr] < lower_band[prev]:
                final_lower_band[curr] = lower_band[prev]
            if signals[curr] == -1 and upper_band[curr] > upper_band[prev]:
                final_upper_band[curr] = upper_band[prev]

        if signals[curr] == 1:
            final_upper_band[curr] = np.nan
        elif signals[curr] == -1:
            final_lower_band[curr] = np.nan

    data['Signals'] = signals
    data['Final Lower Band'] = final_lower_band
    data['Final Upper Band'] = final_upper_band
    data['Upper Band'] = upper_band
    data['Lower Band'] = lower_band

    return data
