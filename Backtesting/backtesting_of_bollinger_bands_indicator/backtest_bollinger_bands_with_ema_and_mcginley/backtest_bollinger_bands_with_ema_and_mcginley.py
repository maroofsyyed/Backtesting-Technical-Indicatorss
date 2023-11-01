'''
The backtest_bollinger_bands_with_ema_and_mcginley function is a backtesting strategy that combines the
Bollinger Bands indicator, McGinley Dynamic Average, and Exponential Moving Average (EMA) Indicators.
It checks for price movements relative to the Bollinger Bands, the McGinley Dynamic Average being above
the closing price, and the EMA indicator being above the closing price to generate buy and sell signals.
The strategy also implements a trailing stop loss to limit losses.
'''

import math
from Indicators import bollinger_bands, mcginley_dynamic_average, exponential_moving_average


def backtest_bollinger_bands_with_ema_and_mcginley(data, investment, lookback=20, commission=5, share=0, stop_loss_pct=0.05):
    """
    Backtesting Bollinger Bands with EMA and McGinley Indicator Strategy
    :param data: pandas dataframe object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param lookback: The lookback period for McGinley Dynamic Strategy
    :param commission: Corresponding commission
    :param share: Number of shares we have before implementing the strategy
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :return: returns four list objects: entries, exits, roi and equity in order
    """
    bb_data = bollinger_bands.bollinger_bands(data)
    signals = bb_data['Signals']
    close = data['close']
    mcginley = mcginley_dynamic_average.mcginley_dynamic_average(data, lookback=lookback, feature='close', return_list=True)
    ema = exponential_moving_average.exponential_moving_average(data, period=10)

    # Initial conditions
    in_position = False
    equity = [investment]
    shares = share
    entry = []
    exit = []
    stop_loss_price = 0

    for i in range(1, len(data)):
        # If not in position and price is on uptrend -> buy
        if not in_position and signals[i] == 1 and mcginley[i] > close[i] and ema[i] > close[i]:
            shares = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= shares * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and price is not on uptrend or hits stop loss -> sell
        elif in_position and (signals[i] != 1 or close[i] < stop_loss_price):
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
    print(f'Earning from investing $100k by backtest_bollinger_bands_with_ema_and_mcginley is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity
