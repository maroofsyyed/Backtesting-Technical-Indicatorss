"""
This file contains the function to calculate chaikin money flow index indicator,
specially used for volume feature capturing purposes.
"""


def chaikin_money_flow(data, period=20):
    """
    Chaikin Money flow index. Volume dependent indicator.
    :param data: Dataframe containing market data, along with volume attribute
    :param period: Lag period window setting of the indicator
    :return: returns whole data with indicator values added
    """
    mf_volume = ((data['close'] - data['low']) - (data['high'] - data['close'])) / (data['high'] - data['low'])
    mf_multiplier = mf_volume * data['volume']
    cmf = mf_multiplier.rolling(window=period).sum() / data['volume'].rolling(window=period).sum()

    data['cmf'] = cmf
    return data
