'''
This python file contains the backtesting performance and plots of supertrend indicator on historical stock data with
mcginley dynamic average
'''

import alpacaUtils.historical_data
from Backtesting.backtesting_of_supertrend_indicator import functions_supertrend
from Backtesting.backtesting_of_supertrend_indicator.backtest_supertrend_with_mcginley import backtest_supertrend_with_mcginley
from Backtesting.backtesting_of_supertrend_indicator.config_backtest_supertrend import API_KEY,SECRET_KEY,START_DATE,TICKER, investment, STOP_LOSS_PCT, RISK_FREE_RATE,ANNUALIZE_COEFFICIENT

df = alpacaUtils.historical_data.get_historical_stock_data(api_key=API_KEY, secret_key= SECRET_KEY, ticker=TICKER,
                              start_date=START_DATE, timeframe='Min', return_df=True)

entry, exit, roi, equity = backtest_supertrend_with_mcginley.backtest_supertrend_with_mcginley(df, investment, lookback=10, commission=5, share=0, stop_loss_pct=STOP_LOSS_PCT)

# Calculate Performance Measures
print(functions_supertrend.calculate_performance_measures(entry, exit, roi, equity,risk_free_rate= RISK_FREE_RATE, annualize_coefficient =ANNUALIZE_COEFFICIENT))

# Plotting buy and sell signals with Supertrend bands
print(functions_supertrend.plot_signals_with_supertrend_mcginley(df, entry, exit))