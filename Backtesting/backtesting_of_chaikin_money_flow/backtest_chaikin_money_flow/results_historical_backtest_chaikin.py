'''
This python file contains the backtesting performance and plots of just the bollinger band Indicator on historical stock data
'''

import backtest_chaikin_money_flow as bcm
import functions_chaikin as fm
import alpacaUtils.historical_data
from Indicators.chaikin_money_flow_index import chaikin_money_flow
import pandas as pd
import numpy as np

data = pd.read_csv('forex_data_EUR_USD.csv')

data = chaikin_money_flow(data, period=20)
entry, exit, roi, equity = bcm.backtest_chaikin_money_flow(data, investment=100000, commission=5, stop_loss_pct=0.0005, threshold=-0.29594943384545214)

results = fm.calculate_performance_measures(entry, exit, roi, equity, risk_free_rate = 3.8, annualize_coefficient = 98280)
# Calculate Performance Measures
print(results)
signal_line = data['cmf']
signal_line = signal_line[~signal_line.isnull()]
# print(signal_line)

# Plotting buy and sell signals
# print(fm.plot_buy_sell_signals_with_bollinger_bands(data, entry, exit))

# max_sr = -1000000
# thresh = 0
# for i in np.arange(min(signal_line), max(signal_line), 0.001):
#     print(i)
#     entry, exit, roi, equity = bcm.backtest_macd(data, investment=100000, commission=5, stop_loss_pct=0.0005,
#                                                  threshold=i)
#     results = fm.calculate_performance_measures(entry, exit, roi, equity, risk_free_rate=3.8,
#                                                 annualize_coefficient=98280)
#     temp_sr = results['Net Profit']
#     if max_sr < temp_sr:
#         max_sr = temp_sr
#         thresh = i
#
# print(max_sr, thresh)

# 59.99999999999999 -0.29594943384545214