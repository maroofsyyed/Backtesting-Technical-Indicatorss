'''
This file contains the functions of performance and Plotting of buy and sell signal.
'''
import numpy as np
from math import sqrt
import plotly.graph_objects as go
import configparser
import os

# Get the path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the config_efma.ini file
config_path = os.path.join(current_dir, 'config_efma.ini')
config = configparser.ConfigParser()
config.read(config_path)

units = float(config.get('OANDA', 'units'))


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
    net_profit = roi / 100 * units  # Net profit
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



def plot_fibonacci_signals(data):
    # Plot Fibonacci high, low, and close
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Fib_MA_3_high'], mode='lines', name='Fibonacci High'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Fib_MA_3_low'], mode='lines', name='Fibonacci Low'))
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name='Close'))

    # Add buy and sell signals
    buy_signals = data[data['signal'] == 1]
    sell_signals = data[data['signal'] == -1]

    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['close'], mode='markers', name='Buy Signal', marker=dict(color='green', size=8), showlegend=True))
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['close'], mode='markers', name='Sell Signal', marker=dict(color='red', size=8), showlegend=True))

    fig.update_layout(showlegend=True)
    fig.show()


# plot_fibonacci_signals(enhanced_fib_ma_data_with_signals)