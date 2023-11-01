'''
 The triple_bullish_with_ema function backtests Triple Bullish Trend strategy with the EMA indicator and
 a stop loss. In this strategy, the function determines the presence of an uptrend based on Supertrend
 Indicators calculated using different periods and multipliers. Additionally, it checks if the 20-day
 EMA (Used 20 days for reference this could vary between 8-20 for intraday and 50-200 for long term) is
 above the closing price as a confirmation signal.It buys shares when all three Supertrend Indicators
 indicate an uptrend and the 20-day EMA is above the closing price. It sells shares when any of the
 Indicators turn bearish, the 20-day EMA is below the closing price, or the price hits the stop loss.
'''

import math
from Indicators import supertrend, exponential_moving_average

def triple_bullish_with_ema(data, investment, multipliers=None, commission=5, share=0, periods=None, ema_period=20, stop_loss_pct=0.005):
    """
    Backtesting Triple Bullish trend with EMA indicator and Stop Loss Strategy
    :param data: pandas dataframe object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param commission: corresponding commission
    :param share: Number of shares we have before implementing the strategy
    :param multipliers: List of multipliers with length of 3.
    :param periods: List of periods with length 3.
    :param ema_period: period for EMA indicator
    :param stop_loss_pct: Percentage value to set the stop loss
    :return: returns three list objects i.e. entries, exits, roi and equity list in the order stated.
    """

    is_uptrend1 = supertrend.supertrend(data, period=periods[0], atr_multiplier=multipliers[0])['Supertrend']
    is_uptrend2 = supertrend.supertrend(data, period=periods[1], atr_multiplier=multipliers[1])['Supertrend']
    is_uptrend3 = supertrend.supertrend(data, period=periods[2], atr_multiplier=multipliers[2])['Supertrend']
    ema = exponential_moving_average.exponential_moving_average(data, period=ema_period)
    close = data['close']

    # Initial conditions
    in_position = False
    equity = [investment]
    entry = []
    exit = []
    stop_loss_price = 0

    for i in range(2, len(data)):
        # If not in position and price is on uptrend and the 20-day EMA is above the closing price -> buy
        if not in_position and is_uptrend1[i] and is_uptrend2[i] and is_uptrend3[i] and ema[i] > close[i]:
            share = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= share * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and price is not on uptrend or the 20-day EMA is below the closing price or hits stop loss -> sell
        elif in_position and (not is_uptrend1[i] or not is_uptrend2[i] or not is_uptrend3[i] or ema[i] < close[i] or close[i] < stop_loss_price):
            equity[-1] += share * close[i] - commission
            exit.append((i, close[i]))
            in_position = False

        # Update stop loss price if price increases
        if in_position and close[i] > stop_loss_price:
            stop_loss_price = close[i] * (1 - stop_loss_pct)

        equity.append(equity[-1])  # Append the current account value to the list

    # If still in position, sell all shares at the last closing price
    if in_position:
        equity[-1] += share * close[-1] - commission

    earning = equity[-1] - investment
    roi = round(earning / investment * 100, 2)
    print(f'Earning from investing $100k by triple_bullish_with_ema_with_stop_loss is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity
