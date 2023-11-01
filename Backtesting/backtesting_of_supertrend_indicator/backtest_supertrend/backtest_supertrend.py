'''
The backtest_supertrend function is a backtesting strategy that uses the Supertrend indicator with
a trailing stop loss. It checks for an uptrend based on the Supertrend indicator and executes buy
and sell trades accordingly.
'''

import math
from Indicators import supertrend

def backtest_supertrend(data, investment, commission=5, share=0, stop_loss_pct=0.05):
    """
    Backtesting Supertrend Strategy with Trailing Stop Loss
    :param data: pandas dataframe object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param commission: corresponding commission
    :param share: Number of shares we have before implementing the strategy
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :return: returns three list objects i.e. entries, exits, roi, and equity in the order stated.
    """

    data['Supertrend'] = supertrend.supertrend(data)['Supertrend']
    is_uptrend = data['Supertrend']
    close = data['close']

    # Initial conditions
    in_position = False
    equity = [investment]  # Account value over time
    shares = 0
    entry = []
    exit = []
    stop_loss_price = 0

    for i in range(2, len(data)):
        # If not in position and price is on uptrend -> buy
        if not in_position and is_uptrend[i]:
            shares = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= shares * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and price is on downtrend or hits stop loss -> sell
        elif in_position and (not is_uptrend[i] or close[i] < stop_loss_price):
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
    print(f'Earning from investing $100k by backtest_supertrend is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity







