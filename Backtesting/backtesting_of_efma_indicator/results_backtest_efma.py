'''
This python file contains the backtesting performance and plots of just the EFMA Indicator on historical stock data
'''
import configparser
import pandas as pd
import os
from Indicators import efma_indicator
from backtest_efma_indicator import backtest_enhanced_fibonacci
from functions_efma import calculate_performance_measures, plot_fibonacci_signals
import historical_oanda_forex_data

pd.set_option('display.max_columns', None)

# Get the path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config_efma.ini file
config_path = os.path.join(current_dir, 'config_efma.ini')

config = configparser.ConfigParser()
config.read(config_path)


api_key = config.get('OANDA', 'api_key')
account_id = config.get('OANDA', 'account_id')
stop_loss_pct = float(config.get('OANDA', 'stop_loss_pct'))
units = float(config.get('OANDA', 'units'))
period = int(config.get('OANDA', 'period'))
atr_multiplier = int(config.get('OANDA', 'atr_multiplier'))
instrument = config.get('OANDA', 'instrument')
start_date = config.get('OANDA', 'start_date')
timeframe = config.get('OANDA', 'timeframe')
annualize_coefficient = float(config.get('OANDA', 'annualize_coefficient'))
risk_free_rate = float(config.get('OANDA', 'risk_free_rate'))


data = historical_oanda_forex_data.get_historical_forex_data(api_key, instrument=instrument, start_date=start_date, timeframe=timeframe)
print(data)

# Assuming your DataFrame has a "close" column containing the closing prices
enhanced_fib_ma_data = efma_indicator.enhanced_fibonacci_moving_average(data)

# print(enhanced_fib_ma_data_with_signals)


entry, exit, roi, equity = backtest_enhanced_fibonacci(data=enhanced_fib_ma_data, units= units, commission=5)

performance_measures = calculate_performance_measures(entry, exit, roi, equity, risk_free_rate, annualize_coefficient)
print(performance_measures)


plot_fibonacci_signals(data = enhanced_fib_ma_data)