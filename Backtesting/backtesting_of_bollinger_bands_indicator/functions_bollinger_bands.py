'''
This file contains the functions of performance and Plotting of buy and sell signal.
'''

from Indicators import mcginley_dynamic_average
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt


def calculate_performance_measures(entry, exit, roi, equity, risk_free_rate=None, annualize_coefficient=None):
    '''

    :param entry:List of entry points for trades.
    :param exit:List of exit points for trades.
    :param roi:Return on investment in percentage.
    :param equity:List of equity values over time.
    :param risk_free_rate:Risk-free rate of return (default: 3%)
    :param annualize_coefficient:Coefficient to annualize returns (default: 98280).
    :return:Dictionary containing the calculated performance measures.
    '''
    trades = len(entry)  # Total trades executed
    net_profit = roi / 100 * 100000  # Net profit
    minimum = min(exit_point[1] - entry_point[1] for entry_point, exit_point in zip(entry, exit))  # Minimum drawdown
    maximum = max(exit_point[1] - entry_point[1] for entry_point, exit_point in zip(entry, exit))  # Maximum drawdown
    hit_ratio = len([trade for trade in exit if trade[1] > trade[0]]) / trades * 100  # Hit ratio
    expectancy = net_profit / trades  # Expectancy

    # Calculate returns from equity values
    returns = np.diff(equity) / equity[:-1]

    # Calculate average return and standard deviation of returns
    avg_return = np.mean(returns)
    std_return = np.std(returns)

    # Calculate annualized average return and standard deviation
    annualized_avg_return = avg_return * annualize_coefficient
    annualized_std_return = std_return * sqrt(annualize_coefficient)

    # Calculate excess return over the risk-free rate
    excess_return = annualized_avg_return - risk_free_rate

    # Calculate Sharpe ratio with annualization and root-n adjustment
    sharpe_ratio = excess_return / (annualized_std_return * sqrt(len(equity)))

    performance_measures = {
        "Hit Ratio": hit_ratio,
        "Expectancy": expectancy,
        "Minimum Drawdown": minimum,
        "Maximum Drawdown": maximum,
        "Net Profit": net_profit,
        "Trades": trades,
        "Sharpe Ratio": sharpe_ratio
    }
    return performance_measures


def plot_buy_sell_signals_with_bollinger_bands(data, entry, exit):
    plot_df = data.reset_index()
    plot_df['index_str'] = plot_df['timestamp'].astype(str)

    # Create a larger figure
    plt.figure(figsize=(12, 8))

    # Plotting buy and sell signals
    plt.plot(plot_df['index_str'], plot_df['close'], color='blue', alpha=0.8, label='Close Price')

    for entry_point in entry:
        plt.scatter(plot_df['index_str'][entry_point[0]], entry_point[1], color='lime', marker='^', s=100)

    for exit_point in exit:
        plt.scatter(plot_df['index_str'][exit_point[0]], exit_point[1], color='red', marker='v', s=100)

    # Plotting Bollinger Bands
    plt.plot(plot_df['index_str'], plot_df['Final Lower Band'], color='#7FFF7F', alpha=0.8, label='Lowerband')
    plt.plot(plot_df['index_str'], plot_df['Final Upper Band'], color='#FF7F7F', alpha=0.8, label='Upperband')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Bollinger Bands Buy and Sell Signals')
    plt.legend()

    # Adjust the x-axis tick placement and rotation
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))  # Limit the number of ticks
    # Add informative padding and gridlines
    plt.margins(x=0.02, y=0.1)  # Add padding to x-axis and y-axis
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add gridlines
    # Display the plot
    plt.show()

def plot_signals_with_bollinger_mcginley(df, entry, exit):
    # Calculate McGinley Dynamic Average
    mcginley_average = mcginley_dynamic_average.mcginley_dynamic_average(df, lookback=20, feature='close', return_list=False)
    mcginley_average = mcginley_average['mcginley_avg']
    mcginley_average_list = mcginley_average.tolist()

    # Plotting buy and sell signals with Bollinger Bands and McGinley Dynamic Average
    plot_df = df.reset_index()
    plot_df['index_str'] = plot_df['timestamp'].astype(str)

    # Create a larger figure
    plt.figure(figsize=(12, 8))

    # Plotting buy and sell signals
    plt.plot(plot_df['index_str'], plot_df['close'], color='blue', alpha=0.8, label='Close Price')

    for entry_point in entry:
        plt.scatter(plot_df['index_str'][entry_point[0]], entry_point[1], color='lime', marker='^', s=100)

    for exit_point in exit:
        plt.scatter(plot_df['index_str'][exit_point[0]], exit_point[1], color='red', marker='v', s=100)

    # Plotting Bollinger Bands
    plt.plot(plot_df['index_str'], plot_df['Final Lower Band'], color='#7FFF7F', alpha=0.8, label='Lowerband')
    plt.plot(plot_df['index_str'], plot_df['Final Upper Band'], color='#FF7F7F', alpha=0.8, label='Upperband')

    # Plotting McGinley Dynamic Average
    plt.plot(plot_df['index_str'], mcginley_average_list, color='purple', alpha=0.8, label='McGinley')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Bollinger Bands with McGinley Buy and Sell Signals')
    plt.legend()

    # Adjust the x-axis tick placement and rotation
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))  # Limit the number of ticks
    # Add informative padding and gridlines
    plt.margins(x=0.02, y=0.1)  # Add padding to x-axis and y-axis
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add gridlines
    # Display the plot
    plt.show()
