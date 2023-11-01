"""
This file contains the function to calculate On Balance Volume indicator,
specially used for volume following purposes.
"""


def calculate_obv(data):
    """
    On-Balance Volume indicator. dependent on both close and volume attributes of data.
    :param data: Dataframe containing market data. Make sure volume data is also present
    :return: returns whole data with indicator values added
    """
    obv = [0]  # Initialize OBV with 0 as the first value
    for i in range(1, len(data)):
        if data['close'][i] > data['close'][i-1]:
            obv.append(obv[i-1] + data['volume'][i])
        elif data['close'][i] < data['close'][i-1]:
            obv.append(obv[i-1] - data['volume'][i])
        else:
            obv.append(obv[i-1])
    data['obv'] = obv
    return data
