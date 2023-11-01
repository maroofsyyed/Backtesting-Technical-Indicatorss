'''
The triple_bullish_trend strategy combines Bollinger Bands with a triple bullish trend condition.
It generates buy signals when all three Bollinger Bands indicate an upward trend and sells when any
of the Indicators turn bearish or the price hits the stop loss. The strategy aims to capture bullish
market trends while using stop loss for risk management.
'''
import math
from Indicators import bollinger_bands


def triple_bullish_trend(data, investment, commission=5, share=0, periods=None, std_multiplier=None, stop_loss_pct=0.005):
    """
    Backtesting Triple Bullish trend Strategy with Stop Loss using Bollinger Bands
    :param data: pandas dataframe object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param commission: corresponding commission
    :param share: Number of shares we have before implementing the strategy
    :param periods: List of periods with length 3 for Bollinger Bands
    :param std_multiplier: List of standard deviation multipliers with length 3 for Bollinger Bands
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :return: returns four list objects: entries, exits, roi and equity in order
    """

    bb_data1 = bollinger_bands.bollinger_bands(data, period=periods[0], std_multiplier=std_multiplier[0])
    bb_data2 = bollinger_bands.bollinger_bands(data, period=periods[1], std_multiplier=std_multiplier[1])
    bb_data3 = bollinger_bands.bollinger_bands(data, period=periods[2], std_multiplier=std_multiplier[2])
    signals1 = bb_data1['Signals']
    signals2 = bb_data2['Signals']
    signals3 = bb_data3['Signals']
    close = data['close']

    # Initial conditions
    in_position = False #if share > 0 else False
    equity = [investment]
    shares = share
    entry = []
    exit = []
    stop_loss_price = 0

    for i in range(1, len(data)):
        # If not in position and price is on uptrend -> buy
        if not in_position and signals1[i] == 1 and signals2[i] == 1 and signals3[i] == 1:
            shares = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= shares * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and price is not on uptrend or hits stop loss -> sell
        elif in_position and (signals1[i] != 1 or signals2[i] != 1 or signals3[i] != 1 or close[i] < stop_loss_price):
            equity[-1] += shares * close[i] - commission
            exit.append((i, close[i]))
            in_position = False
            stop_loss_price = 0  # Reset stop loss price

        # Update stop loss price if price increases
        if in_position and close[i] > stop_loss_price:
            stop_loss_price = close[i] * (1 - stop_loss_pct)

        equity.append(equity[-1])  # Append the current account value to the list

    # If still in position, sell all shares at the last closing price
    if in_position:
        equity[-1] += shares * close[-1] - commission
        exit.append((len(data) - 1, close[-1]))

    earning = equity[-1] - investment
    roi = round(earning / investment * 100, 2)
    print(f'Earning from investing $100k by triple_bullish_trend is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity
