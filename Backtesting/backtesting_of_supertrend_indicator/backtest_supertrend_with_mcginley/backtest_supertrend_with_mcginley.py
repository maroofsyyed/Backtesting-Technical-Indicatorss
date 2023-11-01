'''
The backtest_supertrend_with_mcginley function is a backtesting strategy that combines the Supertrend
indicator with the McGinley Dynamic Average indicator. The function iterates through the data, tracking
the current position and equity value. It buys shares when the Supertrend is in an uptrend and the
McGinley indicator is above the closing price. It sells shares when the Supertrend turns bearish or
the price hits the stop loss. The equity value is updated based on trade executions and commissions.
'''
import math
from Indicators import supertrend, mcginley_dynamic_average


def backtest_supertrend_with_mcginley(data, investment, lookback=20, commission=5, share=0, stop_loss_pct=0.05):
    """
    Backtesting Supertrend with McGinley Indicator Strategy
    :param data: pandas dataframe object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param commission: corresponding commission
    :param share: Number of shares we have before implementing the strategy
    :param lookback: The lookback period for McGinley Dynamic Strategy
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :return: returns three list objects i.e. entries, exits, roi and equity list in the order stated.
    """

    data['Supertrend'] = supertrend.supertrend(data)['Supertrend']
    is_uptrend = data['Supertrend']
    close = data['close']
    mcginley = mcginley_dynamic_average.mcginley_dynamic_average(data, lookback=20, feature='close', return_list=True)

    # Initial conditions
    in_position = False
    equity = [investment]
    entry = []
    exit = []
    stop_loss_price = 0

    for i in range(2, len(data)):
        # If not in position and price is on uptrend -> buy
        if not in_position and is_uptrend[i] and mcginley[i] > close[i]:
            share = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= share * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and price is not on uptrend or hits stop loss -> sell
        elif in_position and (not is_uptrend[i] or close[i] < stop_loss_price):
            equity[-1] += share * close[i] - commission
            exit.append((i, close[i]))
            in_position = False
            stop_loss_price = 0  # Reset stop loss price

        # Update stop loss price if price increases
        if in_position and close[i] > stop_loss_price:
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Update stop loss price

        equity.append(equity[-1])  # Append the current account value to the list

    # If still in position, sell all shares at the last closing price
    if in_position:
        equity[-1] += share * close[-1] - commission
        exit.append((len(data) - 1, close[-1]))

    earning = equity[-1] - investment
    roi = round(earning / investment * 100, 2)
    print(f'Earning from investing $100k by backtest_supertrend_with_mcginley is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity
