'''
This python file contains the backtesting performance and plots of just the bollinger band Indicator on historical stock data
'''

import backtest_macd_indicator as bmi
import functions_macd as fm
import alpacaUtils.historical_data
from Indicators.macd_indicator import calculate_macd
import pandas as pd
import numpy as np

data = pd.read_csv('forex_data_EUR_USD.csv')
macd_line, signal_line, macd_histogram = calculate_macd(data)

# print(signal_line.sum()/len(signal_line))

entry, exit, roi, equity = bmi.backtest_macd(data, investment=100000, commission=5, stop_loss_pct=0.0005, threshold=-0.00023028665481321793)

results = fm.calculate_performance_measures(entry, exit, roi, equity, risk_free_rate = 3.8, annualize_coefficient = 98280)
# Calculate Performance Measures
print(results)

# Plotting buy and sell signals
# print(fm.plot_buy_sell_signals_with_bollinger_bands(data, entry, exit))

# max_sr = -100
# thresh = 0
# for i in np.arange(min(signal_line), max(signal_line), 0.00001):
#     print(i)
#     entry, exit, roi, equity = bmi.backtest_macd(data, investment=100000, commission=5, stop_loss_pct=0.0005,
#                                                  threshold=i)
#     results = fm.calculate_performance_measures(entry, exit, roi, equity, risk_free_rate=3.8,
#                                                 annualize_coefficient=98280)
#     temp_sr = results['Net Profit']
#     if max_sr < temp_sr:
#         max_sr = temp_sr
#         thresh = i
#
# print(max_sr, thresh)

# 10.0 -0.00023028665481321793
