'''
Collecting or Extracting Historical forex data from oanda api can be achieved from this file.
"""
'''
import pandas as pd
import oandapyV20
import oandapyV20.endpoints.instruments as instruments




def get_historical_forex_data(api_key, instrument, start_date, timeframe, return_df=True, count = 5000):
    """
    Function returns historical Forex data for the given instrument sampled with the timeframe provided.
    :param api_key: Your Oanda API access token
    :param instrument: The Forex instrument symbol (e.g., "EUR_USD")
    :param start_date: The start date of the data in "YYYY-MM-DD" format
    :param end_date: The end date of the data in "YYYY-MM-DD" format
    :param timeframe: The data sampling period. Can be a value from ['S', 'M', 'H', 'D', 'W', 'M']
    :param return_df: Whether to return the data in the form of a pandas DataFrame or numpy Array
    :return: The Forex data collected
    """

    client = oandapyV20.API(access_token=api_key)

    params = {
        "from": start_date,
        "granularity": timeframe,
        "count": count
    }

    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    client.request(r)

    data = []
    for candle in r.response['candles']:
        time = candle['time']
        volume = float(candle['volume'])
        open_price = float(candle['mid']['o'])
        high_price = float(candle['mid']['h'])
        low_price = float(candle['mid']['l'])
        close_price = float(candle['mid']['c'])
        data.append([time, volume, open_price, high_price, low_price, close_price])

    df = pd.DataFrame(data, columns=['timestamp', 'volume', 'open', 'high', 'low', 'close'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    df['symbol'] = instrument  # Add the 'symbol' column with the provided instrument
    # print(type(volume))
    # print(type(high_price))
    if return_df is True:
        return df
    elif return_df is False:
        return df.values




# #
# df = get_historical_forex_data(api_key, instrument = instrument, start_date = start_date, timeframe = timeframe, count =5000)
# print(df)
# print(df.info())
# #
# df.to_csv('forex_data_EUR_USD.csv', index=True)