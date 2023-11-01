'''
The backtest_enhanced_fibonacci function is a backtesting strategy that uses the EFMA indicator.
It generates buy signals when the price crosses above the Fibonacci High and sell signals
when the price crosses below the Fibonacci Low.
'''

import math


def backtest_enhanced_fibonacci(data, units, commission=5):
    """
    Backtesting Enhanced Fibonacci Strategy
    :param data: pandas DataFrame object containing the stock or crypto data
    :param units: Amount in USD to be invested in the strategy
    :param commission: Corresponding commission
    :return: Returns four list objects: entries, exits, roi, and equity in order
    """
    signals = data['signal']
    close = data['close']

    # Initial conditions
    in_position = False
    equity = [units]
    shares = 0
    entry = []
    exit = []

    for i in range(1, len(data)):
        # If not in position and signal is buy (1) -> buy
        if not in_position and signals[i] == 1:
            shares = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= shares * close[i]
            entry.append((i, close[i]))
            in_position = True

        # If in position and signal is sell (-1) -> sell
        elif in_position and signals[i] == -1:
            equity[-1] += shares * close[i] - commission
            exit.append((i, close[i]))
            in_position = False

        equity.append(equity[-1])  # Append the current account value to the list

    # If still in position, sell all shares at the last closing price
    if in_position:
        equity[-1] += shares * close[-1] - commission
        exit.append((len(data) - 1, close[-1]))

    earning = equity[-1] - units
    roi = round(earning / units * 100, 2)
    print(f'Earning from investing $100k by backtest_enhanced_fibonacci is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity
