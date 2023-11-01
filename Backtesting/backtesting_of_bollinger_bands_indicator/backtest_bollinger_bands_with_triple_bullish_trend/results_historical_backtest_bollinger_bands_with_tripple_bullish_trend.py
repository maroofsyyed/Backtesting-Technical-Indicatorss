'''
This python file contains the backtesting performance and plots of supertrend indicator on historical stock data with
triple bullish trend.
'''

import alpacaUtils.historical_data
from Backtesting.backtesting_of_bollinger_bands_indicator import functions_bollinger_bands
from Backtesting.backtesting_of_bollinger_bands_indicator.backtest_bollinger_bands_with_triple_bullish_trend import backtest_bollinger_bands_with_triple_bullish_trend
from Backtesting.backtesting_of_bollinger_bands_indicator.config_backtesting_bollinger_bands_ import API_KEY,SECRET_KEY,START_DATE,TICKER, investment, STOP_LOSS_PCT, RISK_FREE_RATE,ANNUALIZE_COEFFICIENT

df = alpacaUtils.historical_data.get_historical_stock_data(api_key=API_KEY, secret_key= SECRET_KEY, ticker=TICKER,
                              start_date=START_DATE, timeframe='Min', return_df=True)

entry, exit, roi, equity = backtest_bollinger_bands_with_triple_bullish_trend.triple_bullish_trend(df, investment, commission=5, share=0, periods=[5,15,25], std_multiplier=[2, 2, 2], stop_loss_pct=STOP_LOSS_PCT)


# Calculate Performance Measures
print(functions_bollinger_bands.calculate_performance_measures(entry, exit, roi, equity, risk_free_rate= RISK_FREE_RATE, annualize_coefficient = ANNUALIZE_COEFFICIENT))

# Plotting buy and sell signals
print(functions_bollinger_bands.plot_buy_sell_signals_with_bollinger_bands(df, entry, exit))