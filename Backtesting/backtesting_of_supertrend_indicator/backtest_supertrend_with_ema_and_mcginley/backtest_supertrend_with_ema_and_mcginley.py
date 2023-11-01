'''
The backtest_supertrend_with_ema_and_mcginley function is a backtesting strategy that combines the
Supertrend indicator with the McGinley Dynamic Average and Exponential Moving Average (EMA) Indicators
In this strategy, the function calculates the Supertrend indicator, the McGinley Dynamic Average
indicator, and the EMA indicator based on the input data. It checks for an uptrend based on the
Supertrend indicator, the McGinley indicator being above the closing price, and the EMA indicator
being above the closing price. It executes buy and sell trades based on these conditions and implements
a trailing stop loss to limit losses.
'''
import math
from Indicators import supertrend, mcginley_dynamic_average, exponential_moving_average


def backtest_supertrend_with_ema_and_mcginley(data, investment, commission=5, share=0, period=8, lookback=20, stop_loss_pct=0.005):
    """
    Backtesting Supertrend with McGinley and EMA Indicators Strategy
    :param data: pandas dataframe object containing the stock or crypto data
    :param investment: Amount in USD to be invested in the strategy
    :param commission: corresponding commission
    :param share: Number of shares we have before implementing the strategy
    :param lookback: The lookback period for McGinley Dynamic Strategy
    :param period: The period for exponential moving average
    :param stop_loss_pct: Percentage value to set the trailing stop loss
    :return: returns three list objects i.e. entries, exits,roi and equity list in the same order.
    """

    is_uptrend = supertrend.supertrend(data)['Supertrend']
    close = data['close']
    mcginley = mcginley_dynamic_average.mcginley_dynamic_average(data, lookback=lookback, feature='close', return_list=True)
    ema = exponential_moving_average.exponential_moving_average(data, period=period)

    # Initial conditions
    in_position = False
    equity = [investment]
    entry = []
    exit = []
    shares = 0
    stop_loss_price = 0

    for i in range(2, len(data)):
        # If not in position and price is on uptrend -> buy
        if not in_position and is_uptrend[i] and mcginley[i] > close[i] and ema[i] > close[i]:
            shares = math.floor(equity[-1] / close[i] / 100) * 100
            equity[-1] -= shares * close[i]
            entry.append((i, close[i]))
            in_position = True
            stop_loss_price = close[i] * (1 - stop_loss_pct)  # Set initial stop loss price

        # If in position and (price is not on uptrend or hits stop loss) -> sell
        elif in_position and (not is_uptrend[i] or close[i] < stop_loss_price):
            equity[-1] += shares * close[i] - commission
            exit.append((i, close[i]))
            in_position = False

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
    print(f'Earning from investing $100k is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, roi, equity
