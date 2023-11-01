'''
This python file contains the backtesting performance and plots of just the bollinger band Indicator on historical stock data
'''
import numpy as np

# import Backtesting

# import backtest_ichimoku_indicator as bmi
import backtest_ichimoku_indicator as bii
import functions_ichimoku as fm
import alpacaUtils.historical_data
from Indicators.macd_indicator import calculate_macd
import pandas as pd
# from Backtesting.backtesting_of_bollinger_bands_indicator import functions_bollinger_bands
# from Backtesting.backtesting_of_bollinger_bands_indicator.backtest_ichimoku_clouds import backtest_ichimoku_clouds
# from Backtesting.backtesting_of_bollinger_bands_indicator.config_backtesting_bollinger_bands_ import API_KEY, SECRET_KEY, START_DATE, TICKER, investment, STOP_LOSS_PCT, RISK_FREE_RATE, ANNUALIZE_COEFFICIENT

# df = alpacaUtils.historical_data.get_historical_stock_data(api_key=API_KEY, secret_key= SECRET_KEY, ticker=TICKER,
#                               start_date=START_DATE, timeframe='Min', return_df=True)

data = pd.read_csv('forex_data_EUR_USD.csv')
# macd_line, signal_line, macd_histogram = calculate_macd(data)

# print(signal_line.sum()/len(signal_line))

entry, exit, roi, equity = bii.backtest_ichimoku(data, investment=100000, commission=5,
                                                 stop_loss_pct=0.0005, threshold=1.0784500000000743)

results = fm.calculate_performance_measures(entry, exit, roi, equity, risk_free_rate=3.8,
                                            annualize_coefficient=98280)
# Calculate Performance Measures
print(results)
signal_line = data['base_line']
signal_line = signal_line[~signal_line.isnull()]
# print(signal_line)
# Plotting buy and sell signals
# print(fm.plot_buy_sell_signals_with_bollinger_bands(data, entry, exit))

# max_sr = -100
# thresh = 0
# for i in np.arange(min(signal_line), max(signal_line), 0.00001):
#     print(i)
#     entry, exit, roi, equity = bii.backtest_ichimoku(data, investment=100000, commission=5, stop_loss_pct=0.0005,
#                                                  threshold=i)
#     results = fm.calculate_performance_measures(entry, exit, roi, equity, risk_free_rate=3.8,
#                                                 annualize_coefficient=98280)
#     temp_sr = results['Net Profit']
#     if max_sr < temp_sr:
#         max_sr = temp_sr
#         thresh = i

# print(max_sr, thresh)

# 10.0 1.0784500000000743