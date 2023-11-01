'''
The triple_bullish_trend function backtests the Triple Bullish Trend strategy with a trailing stop loss,
In this strategy, the function determines the presence of an uptrend based on Supertrend Indicators
calculated using different periods and multipliers. It checks for a triple uptrend condition and executes
buy and sell trades accordingly.
'''
import math
from Indicators import supertrend


def triple_bullish_trend(data, investment, commission=5, share=0, multipliers=None, periods=None, stop_loss_pct=0.005):
    """
    Backtesting Triple Bullish trend Strategy with Stop Loss
    :param data: pandas dataframe object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param commission: corresponding commission
    :param share: Number of shares we have before implementing the strategy
    :param multipliers: List of multipliers with length of 3.
    :param periods: List of periods with length 3.
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :return: returns three list objects i.e. entries, exits, and roi and equity list in the order stated.
    """

    is_uptrend1 = supertrend.supertrend(data, period=periods[0], atr_multiplier=multipliers[0])['Supertrend']
    is_uptrend2 = supertrend.supertrend(data, period=periods[1], atr_multiplier=multipliers[1])['Supertrend']
    is_uptrend3 = supertrend.supertrend(data, period=periods[2], atr_multiplier=multipliers[2])['Supertrend']
    close = data['close']

    # Initial conditions
    in_position = False
    equity = [investment]
    shares = 0
    entry = []
    exit = []
    stop_loss_price = 0

    for i in range(2, len(data)):
        # If not in position and price is on uptrend -> buy
        if not in_position and is_uptrend1[i] and is_uptrend2[i] and is_uptrend3[i]:
            shares = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= shares * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and price is not on uptrend or hits stop loss -> sell
        elif in_position and (not is_uptrend1[i] or not is_uptrend2[i] or not is_uptrend3[i] or close[i] < stop_loss_price):
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
