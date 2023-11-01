'''
The backtest_bollinger bands function is a backtesting strategy that uses the bollinger band indicator with
a trailing stop loss.  It generates buy signals when the price crosses above the upper band and sell signals
when the price crosses below the lower band or hits the stop loss level.
'''
import math
from Indicators import chaikin_money_flow_index


def backtest_chaikin_money_flow(data, investment, commission=5, stop_loss_pct=0.005, threshold=0):
    """
    Backtesting Bollinger Bands Strategy with Stop Loss
    :param data: pandas DataFrame object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param commission: corresponding commission
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :return: returns four list objects: entries, exits, roi and equity in order
    """
    data = chaikin_money_flow_index.chaikin_money_flow(data, period=20)
    signals = data['cmf']
    close = data['close']

    # Initial conditions
    in_position = False
    equity = [investment]
    shares = 0
    entry = []
    exit = []
    stop_loss_price = 0
    threshold = threshold

    for i in range(1, len(data)):
        # If not in position and price crosses the upper band -> buy
        if not in_position and signals[i] < threshold:
            shares = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= shares * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and price crosses the lower band or hits stop loss -> sell
        elif in_position and (signals[i] > threshold or close[i] < stop_loss_price):
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
        try:
            equity[-1] += shares * close[-1] - commission
            exit.append((len(data) - 1, close[-1]))
        except:
            print('Hehe')

    earning = equity[-1] - investment
    roi = round(earning / investment * 100, 2)
    print(f'Earning from investing $100k by backtest_bollinger_bands is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity
